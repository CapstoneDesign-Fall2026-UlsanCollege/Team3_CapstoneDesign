"""Platform-only provisioning and owner-only staff/settings operations."""
import os
import secrets
import time
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from . import models
from .database import get_db
from .identity_models import ArchivedStore, Audit, Invitation, LoginSession, Membership, Store, User
from .security import audit, identity_db, memberships, principal, recent_mfa
from .mailer import send_owner_activation
from .security_primitives import config, email_address, token_hash
from .tenancy import provision_store

router = APIRouter()


class StoreInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class InviteInput(BaseModel):
    email: str = Field(max_length=254)
    name: str = Field(min_length=1, max_length=120)
    store_id: str = Field(max_length=32)
    role: Literal["owner", "cashier"] = "cashier"
    require_mfa: bool = False

    @field_validator("email")
    @classmethod
    def valid_email(cls, value):
        return email_address(value)


class ActiveInput(BaseModel):
    active: bool


class SettingsInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    address: str = Field(default="", max_length=300)
    phone: str = Field(default="", max_length=40)
    receipt_footer: str = Field(default="", max_length=300)


def invite_member(db, payload, actor, origin):
    store = db.get(Store, payload.store_id)
    if not store or not store.active:
        raise HTTPException(404, "Business not found")
    user = db.scalar(select(User).where(User.email == payload.email).with_for_update())
    if payload.email == config("SMARTSERVE_PLATFORM_ADMIN_EMAIL").strip().lower() or (user and user.platform_admin):
        raise HTTPException(409, "The platform administrator is managed outside business memberships")
    if user is None:
        user = User(id=uuid4().hex, email=payload.email, name=payload.name.strip() or payload.email,
                    active=True, platform_admin=False, mfa_required=payload.require_mfa or payload.role == "owner", created_at=time.time())
        db.add(user)
        db.flush()
    member = db.scalar(select(Membership).where(Membership.user_id == user.id, Membership.store_id == store.id))
    if member is not None:
        if not (member.active and member.role == payload.role == "owner" and user.password_hash is None):
            raise HTTPException(409, "This person already has a membership in this business")
    else:
        other_membership = db.scalar(select(Membership.id).where(
            Membership.user_id == user.id, Membership.active.is_(True),
        ).limit(1))
        if other_membership is not None:
            raise HTTPException(409, "This email is already assigned to another business")
        db.add(Membership(user_id=user.id, store_id=store.id, role=payload.role, active=True))
    if payload.require_mfa:
        user.mfa_required = True
    activation = None
    if user.password_hash is None:
        # Revoke older outstanding activation links without affecting other memberships.
        db.execute(update(Invitation).where(Invitation.user_id == user.id).values(consumed=True))
        raw = secrets.token_urlsafe(48)
        db.add(Invitation(token_hash=token_hash(raw), user_id=user.id, expires_at=time.time() + 86400, consumed=False))
        activation = origin.rstrip("/") + "/activate#" + raw
    email_sent = bool(activation and payload.role == "owner")
    if email_sent:
        try:
            send_owner_activation(user.email, activation)
        except Exception:
            db.rollback()
            raise HTTPException(503, "Could not send the owner invitation. Try again shortly.") from None
        activation = None
    audit(db, "member_invited", actor.user_id, store.id, f"role={payload.role}; member={user.id}")
    db.commit()
    message = "Membership added. They can use their existing account."
    if email_sent:
        message = "Owner activation email sent."
    elif activation:
        message = "Share this one-use link privately. No email has been sent."
    return {"activation_url": activation, "existing_account": user.password_hash is not None,
            "expires_in_hours": 24 if activation or email_sent else None, "message": message}



@router.get("/platform/businesses")
def stores(request: Request):
    principal(request, "platform_admin")
    with identity_db() as db:
        archives = dict(db.execute(select(ArchivedStore.store_id, ArchivedStore.delete_at)).all())
        owners = {}
        rows = db.execute(select(Membership.store_id, User.email, User.password_hash.is_not(None)).join(
            User, User.id == Membership.user_id,
        ).where(Membership.role == "owner", Membership.active.is_(True)).order_by(User.email))
        for store_id, email, activated in rows:
            owners.setdefault(store_id, []).append({"email": email, "activated": activated})
        return [{"id": store.id, "name": store.name, "active": store.active,
                 "owners": owners.get(store.id, []), "delete_at": archives.get(store.id)}
                for store in db.scalars(select(Store).order_by(Store.created_at.desc()))]


@router.patch("/platform/businesses/{store_id}/access")
def update_store_access(store_id: str, payload: ActiveInput, request: Request):
    actor = principal(request, "platform_admin")
    recent_mfa(actor)
    with identity_db() as db:
        store = db.scalar(select(Store).where(Store.id == store_id).with_for_update())
        if not store:
            raise HTTPException(404, "Business not found")
        archive = db.get(ArchivedStore, store_id)
        if archive and archive.delete_at <= time.time():
            raise HTTPException(409, "The restoration period has ended")
        if payload.active and archive:
            db.delete(archive)
        if store.active != payload.active:
            set_store_access(db, store, payload.active, actor)
        db.commit()
        return {"id": store.id, "active": store.active}


def set_store_access(db, store, active, actor):
    store.active = active
    if not active:
        db.execute(update(LoginSession).where(
            LoginSession.store_id == store.id, LoginSession.user_id != actor.user_id,
        ).values(revoked=True))
        db.execute(update(LoginSession).where(
            LoginSession.store_id == store.id, LoginSession.user_id == actor.user_id,
        ).values(store_id=None))
    audit(db, "business_resumed" if active else "business_suspended", actor.user_id, store.id)


@router.delete("/platform/businesses/{store_id}")
def archive_store(store_id: str, request: Request):
    actor = principal(request, "platform_admin")
    recent_mfa(actor)
    if store_id == "legacy":
        raise HTTPException(409, "The original shared store can be stopped, but cannot be archived")
    with identity_db() as db:
        store = db.scalar(select(Store).where(Store.id == store_id).with_for_update())
        if not store:
            raise HTTPException(404, "Business not found")
        archive = db.get(ArchivedStore, store_id)
        if archive is None:
            archive = ArchivedStore(store_id=store_id, delete_at=time.time() + 30 * 86400)
            db.add(archive)
            if store.active:
                set_store_access(db, store, False, actor)
            audit(db, "business_archived", actor.user_id, store_id)
            db.commit()
        return {"id": store_id, "delete_at": archive.delete_at}


@router.post("/platform/businesses", status_code=201)
def create_store(payload: StoreInput, request: Request):
    actor = principal(request, "platform_admin")
    recent_mfa(actor)
    if not payload.name.strip():
        raise HTTPException(422, "Business name is required")
    store_id = uuid4().hex
    with identity_db() as db:
        store = Store(id=store_id, name=payload.name.strip(), namespace="store_" + store_id, active=True, created_at=time.time())
        db.add(store)
        db.flush()
        provision_store(store)
        audit(db, "business_created", actor.user_id, store.id)
        db.commit()
        return {"id": store.id, "name": store.name, "active": store.active}


@router.post("/platform/invitations")
def platform_invite(payload: InviteInput, request: Request):
    actor = principal(request, "platform_admin")
    recent_mfa(actor)
    with identity_db() as db:
        return invite_member(db, payload, actor, os.getenv("SMARTSERVE_PUBLIC_ORIGIN", str(request.base_url)))


@router.post("/owner/staff/invitations")
def staff_invite(payload: InviteInput, request: Request):
    actor = principal(request, "owner", "platform_admin")
    recent_mfa(actor)
    if payload.store_id != actor.store_id or payload.role != "cashier":
        raise HTTPException(403, "Owners can invite cashiers only to their own business")
    with identity_db() as db:
        return invite_member(db, payload, actor, os.getenv("SMARTSERVE_PUBLIC_ORIGIN", str(request.base_url)))


@router.get("/owner/staff")
def staff(request: Request):
    actor = principal(request, "owner", "platform_admin")
    with identity_db() as db:
        rows = db.execute(select(Membership, User).join(User).where(Membership.store_id == actor.store_id)).all()
        return [{"id": user.id, "name": user.name, "email": user.email, "role": member.role,
                 "active": member.active, "mfa_enabled": bool(user.email_verified_at)} for member, user in rows]


@router.put("/owner/staff/{user_id}/access")
def staff_access(user_id: str, payload: ActiveInput, request: Request):
    actor = principal(request, "owner", "platform_admin")
    recent_mfa(actor)
    with identity_db() as db:
        member = db.scalar(select(Membership).where(Membership.user_id == user_id, Membership.store_id == actor.store_id).with_for_update())
        if not member or member.role != "cashier" or user_id == actor.user_id:
            raise HTTPException(403, "Only a cashier membership in this business can be changed here")
        member.active = payload.active
        db.execute(update(LoginSession).where(LoginSession.user_id == user_id, LoginSession.store_id == actor.store_id).values(revoked=True))
        audit(db, "staff_access_changed", actor.user_id, actor.store_id, f"member={user_id}; active={payload.active}")
        db.commit()
        return {"active": member.active}


@router.put("/owner/settings")
def owner_settings(payload: SettingsInput, request: Request, db: Session = Depends(get_db)):
    principal(request, "owner", "platform_admin")
    if not payload.name.strip():
        raise HTTPException(422, "Business name is required")
    profile = db.get(models.BusinessProfile, 1)
    config = db.get(models.BusinessConfiguration, 1)
    if not profile or not config or not config.onboarding_complete:
        raise HTTPException(409, "The platform administrator must finish setup first")
    profile.name = payload.name.strip()
    config.address, config.phone, config.receipt_footer = payload.address.strip(), payload.phone.strip(), payload.receipt_footer.strip()
    db.commit()
    from .business import get_profile
    return get_profile(db)


@router.get("/platform/audit")
def platform_audit(request: Request):
    principal(request, "platform_admin")
    with identity_db() as db:
        return [{"action": item.action, "user_id": item.user_id, "store_id": item.store_id, "detail": item.detail, "created_at": item.created_at} for item in db.scalars(select(Audit).order_by(Audit.id.desc()).limit(100))]


@router.get("/owner/audit")
def owner_audit(request: Request):
    actor = principal(request, "owner", "platform_admin")
    with identity_db() as db:
        return [{"action": item.action, "detail": item.detail, "created_at": item.created_at} for item in db.scalars(select(Audit).where(Audit.store_id == actor.store_id).order_by(Audit.id.desc()).limit(100))]
