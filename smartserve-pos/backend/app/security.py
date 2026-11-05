"""Invite-only accounts, mandatory privileged MFA, opaque sessions and role gates."""
from dataclasses import dataclass
import hmac
import json
import os
import secrets
import time
from contextlib import contextmanager

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from .database import engine, tenant_scope
from .identity_models import Audit, EmailChallenge, Invitation, LoginSession, Membership, Store, Throttle, User
from .security_primitives import COOKIE, PASSWORDS, PRODUCTION, config, email_code_mac, email_address, password_hash, password_valid, recovery_codes, token_hash


@dataclass
class Principal:
    user_id: str
    email: str
    name: str
    role: str
    store_id: str | None
    namespace: str | None
    purpose: str
    csrf_token: str
    token_hash: str
    mfa_at: float | None


def lock_write(db):
    if engine.dialect.name == "sqlite" and not db.in_transaction():
        db.connection().exec_driver_sql("BEGIN IMMEDIATE")


@contextmanager
def identity_db():
    with Session(engine) as db:
        lock_write(db)
        yield db


def audit(db, action, user_id=None, store_id=None, detail=""):
    db.add(Audit(action=action, user_id=user_id, store_id=store_id, detail=detail[:300], created_at=time.time()))


def memberships(db, user_id):
    rows = db.execute(select(Membership, Store).join(Store).where(Membership.user_id == user_id, Membership.active.is_(True), Store.active.is_(True))).all()
    return [{"id": store.id, "name": store.name, "role": member.role, "namespace": store.namespace} for member, store in rows]


def mfa_required(db, user):
    return user.platform_admin or user.mfa_required or bool(db.scalar(select(Membership.id).where(Membership.user_id == user.id, Membership.role == "owner", Membership.active.is_(True)).limit(1)))


def resolve_session(request):
    raw = request.cookies.get(COOKIE, "")
    if not raw or len(raw) > 200:
        return None
    with identity_db() as db:
        session = db.get(LoginSession, token_hash(raw))
        if not session or session.revoked or session.expires_at <= time.time():
            return None
        user = db.get(User, session.user_id)
        if not user or not user.active:
            return None
        idle = 900 if user.platform_admin else 1800
        if time.time() - session.last_seen > idle:
            session.revoked = True
            db.commit()
            return None
        allowed = memberships(db, user.id)
        selected = next((item for item in allowed if item["id"] == session.store_id), None)
        store = db.get(Store, session.store_id) if session.store_id else None
        if not user.platform_admin and not selected:
            return None
        if user.platform_admin and session.store_id and (not store or not store.active):
            return None
        role = "platform_admin" if user.platform_admin else selected["role"]
        if session.purpose == "full" and mfa_required(db, user) and session.mfa_at is None:
            return None
        session.last_seen = time.time()
        result = Principal(user.id, user.email, user.name, role, session.store_id,
                           store.namespace if user.platform_admin and store else selected["namespace"] if selected else None,
                           session.purpose, session.csrf_token, session.token_hash, session.mfa_at)
        db.commit()
        return result


def principal(request: Request, *roles, full=True):
    result = getattr(request.state, "principal", None)
    if not result or (full and result.purpose != "full"):
        raise HTTPException(401, "Sign in and complete two-factor verification")
    if roles and result.role not in roles:
        raise HTTPException(403, "Your account does not have permission for this action")
    return result


def authenticated(request):
    identity = getattr(request.state, "principal", None)
    return bool(identity and identity.purpose == "full")


def recent_mfa(identity):
    if not identity.mfa_at or time.time() - identity.mfa_at > 600:
        raise HTTPException(403, "Verify your password and second factor again before this sensitive action")


def new_session(db, user, response, request, purpose, old=None, selected=None, verified=False, mfa_timestamp=None, preserve_expiry=False):
    previous_expiry = None
    if old:
        existing = db.get(LoginSession, old)
        if existing:
            previous_expiry = existing.expires_at
            existing.revoked = True
    allowed = memberships(db, user.id)
    store_id = selected if selected is not None else (None if user.platform_admin else allowed[0]["id"] if allowed else None)
    if not user.platform_admin and store_id not in [item["id"] for item in allowed]:
        raise HTTPException(403, "This account has no active business membership")
    raw = secrets.token_urlsafe(48)
    lifetime = 600 if purpose != "full" else 7200 if user.platform_admin else 14400
    session = LoginSession(token_hash=token_hash(raw), user_id=user.id, store_id=store_id, purpose=purpose,
                           csrf_token=secrets.token_urlsafe(32), expires_at=min(time.time() + lifetime, previous_expiry) if preserve_expiry and previous_expiry else time.time() + lifetime,
                           last_seen=time.time(), mfa_at=time.time() if verified else mfa_timestamp, revoked=False)
    db.add(session)
    response.set_cookie(COOKIE, raw, max_age=lifetime, httponly=True, secure=PRODUCTION or request.url.scheme == "https", samesite="strict", path="/")
    response.headers["Cache-Control"] = "no-store"
    return session


def throttle(db, request, label, account="", limit=10):
    # Hash identifiers; neither passwords nor factor values enter logs/rate keys.
    keys = [(f"ip:{label}:{request.client.host if request.client else 'unknown'}", limit * 5), (f"account:{label}:{account}", limit)]
    for key, maximum in keys:
        key = token_hash(key)
        row = db.scalar(select(Throttle).where(Throttle.key == key).with_for_update())
        if row and row.reset_at > time.time() and row.attempts >= maximum:
            raise HTTPException(429, "Too many attempts. Please try again in 15 minutes.", headers={"Retry-After": "900"})
        if row is None:
            row = Throttle(key=key, attempts=0, reset_at=time.time() + 900)
            db.add(row)
        if row.reset_at <= time.time():
            row.attempts, row.reset_at = 0, time.time() + 900
        row.attempts += 1
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(429, "Please wait before trying again")
    lock_write(db)


class LoginInput(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=1, max_length=128)


class ActivateInput(BaseModel):
    token: str = Field(min_length=20, max_length=200)
    name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=14, max_length=128)


class FactorInput(BaseModel):
    code: str = Field(min_length=6, max_length=100)


class ReauthInput(FactorInput):
    password: str = Field(min_length=1, max_length=128)


class PasswordChangeInput(ReauthInput):
    new_password: str = Field(min_length=14, max_length=128)


class SwitchInput(BaseModel):
    store_id: str = Field(min_length=1, max_length=32)


def accept_factor(db, user, code, session_hash, purpose):
    challenge = db.scalar(select(EmailChallenge).where(EmailChallenge.session_hash == session_hash).with_for_update())
    normalized = code.strip().lower().replace("-", "")
    if len(normalized) == 32:
        hashes = json.loads(user.recovery_hashes)
        matched = next((value for value in hashes if hmac.compare_digest(value, token_hash(normalized))), None)
        if matched:
            hashes.remove(matched)
            user.recovery_hashes = json.dumps(hashes)
            if challenge:
                challenge.used = True
            audit(db, "recovery_code_used", user.id)
            return True
    if not challenge or challenge.used or challenge.purpose != purpose or challenge.expires_at <= time.time() or challenge.attempts >= 5:
        return False
    challenge.attempts += 1
    if hmac.compare_digest(challenge.code_mac, email_code_mac(session_hash, normalized)):
        challenge.used = True
        user.email_verified_at = time.time()
        return True
    return False


def issue_email(db, user, session, purpose):
    from .mailer import send_login_code
    previous = db.get(EmailChallenge, session.token_hash)
    if previous and time.time() - previous.sent_at < 60:
        raise HTTPException(429, "Please wait 60 seconds before requesting another code", headers={"Retry-After": "60"})
    code = f"{secrets.randbelow(1000000):06d}"
    while previous and hmac.compare_digest(previous.code_mac, email_code_mac(session.token_hash, code)):
        code = f"{secrets.randbelow(1000000):06d}"
    challenge = previous or EmailChallenge(session_hash=session.token_hash)
    challenge.code_mac = email_code_mac(session.token_hash, code)
    challenge.purpose, challenge.expires_at = purpose, time.time() + 300
    challenge.sent_at, challenge.attempts, challenge.used = time.time(), 0, False
    db.add(challenge)
    try:
        send_login_code(user.email, code)
        audit(db, "email_code_sent", user.id, session.store_id)
        return True
    except Exception:
        # Never print SMTP credentials or code values, and never grant access on failure.
        challenge.used = True
        audit(db, "email_delivery_failed", user.id, session.store_id)
        return False


def install_owner_auth(app):
    @app.middleware("http")
    async def enforce_security(request: Request, call_next):
        path = request.url.path.rstrip("/") or "/"
        identity = await run_in_threadpool(resolve_session, request)
        request.state.principal = identity
        unsafe = request.method not in ("GET", "HEAD", "OPTIONS")
        origin = request.headers.get("origin")
        allowed_origins = {str(request.base_url).rstrip("/")}
        if config("SMARTSERVE_PUBLIC_ORIGIN"):
            allowed_origins.add(config("SMARTSERVE_PUBLIC_ORIGIN").rstrip("/"))
        if not PRODUCTION:
            allowed_origins.update({"http://localhost:5173", "http://127.0.0.1:5173"})
        if unsafe and origin and origin not in allowed_origins:
            return JSONResponse({"detail": "Cross-site requests are not allowed"}, status_code=403)
        if unsafe and identity and path not in ("/auth/login", "/auth/activate"):
            if not hmac.compare_digest(request.headers.get("x-csrf-token", ""), identity.csrf_token):
                return JSONResponse({"detail": "Refresh your session and retry this action"}, status_code=403)
        domain = path.startswith(("/owner/", "/platform/", "/orders", "/inventory", "/menu", "/tables", "/business", "/dashboard"))
        if domain:
            if not identity or identity.purpose != "full":
                return JSONResponse({"detail": "Sign in and complete two-factor verification"}, status_code=401)
            platform_only = path.startswith("/platform/") or path == "/owner/business" or path.startswith("/owner/business/")
            if platform_only and identity.role != "platform_admin":
                return JSONResponse({"detail": "Platform administrator access required"}, status_code=403)
            if platform_only and unsafe and (not identity.mfa_at or time.time() - identity.mfa_at > 600):
                return JSONResponse({"detail": "Verify your password and email code again before changing platform settings"}, status_code=403)
            owner_only = path.startswith(("/dashboard", "/owner/")) and not path.startswith(("/owner/work", "/owner/menu"))
            if path.startswith("/owner/menu") and request.method != "GET":
                owner_only = True
            if request.method == "DELETE" and path.startswith("/orders"):
                owner_only = True
            if owner_only and identity.role not in ("platform_admin", "owner"):
                return JSONResponse({"detail": "Business owner access required"}, status_code=403)
            if not path.startswith("/platform/") and identity.namespace is None:
                return JSONResponse({"detail": "Choose an authorized business first"}, status_code=403)
        scope = tenant_scope.set(identity.namespace if identity and identity.purpose == "full" else None)
        try:
            response = await call_next(request)
        finally:
            tenant_scope.reset(scope)
        return response

    @app.middleware("http")
    async def harden_all_responses(request: Request, call_next):
        response = await call_next(request)
        path = request.url.path
        domain = path.startswith(("/owner/", "/platform/", "/orders", "/inventory", "/menu", "/tables", "/business", "/dashboard"))
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' https: data:; connect-src 'self' http://localhost:8000 http://127.0.0.1:8000 ws://localhost:5173 ws://127.0.0.1:5173; frame-src https://docs.google.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        if domain or path.startswith("/auth/"):
            response.headers["Cache-Control"] = "no-store"
        if PRODUCTION or request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response

    @app.get("/auth/session")
    def session_info(request: Request):
        identity = getattr(request.state, "principal", None)
        if not identity:
            return {"authenticated": False}
        with identity_db() as db:
            allowed = memberships(db, identity.user_id)
            return {"authenticated": identity.purpose == "full", "challenge": identity.purpose if identity.purpose != "full" else None,
                    "user": {"id": identity.user_id, "email": identity.email, "name": identity.name, "role": identity.role},
                    "store_id": identity.store_id, "businesses": [{k: v for k, v in item.items() if k != "namespace"} for item in allowed],
                    "csrf_token": identity.csrf_token}

    @app.post("/auth/login")
    def login(payload: LoginInput, request: Request, response: Response):
        email = payload.email.strip().lower()
        with identity_db() as db:
            throttle(db, request, "login", email)
            user = db.scalar(select(User).where(User.email == email))
            valid = password_valid(user.password_hash if user else None, payload.password)
            if not user or not user.active or not valid:
                audit(db, "login_failed")
                db.commit()
                raise HTTPException(401, "Email or passphrase is incorrect")
            if PASSWORDS.check_needs_rehash(user.password_hash):
                user.password_hash = PASSWORDS.hash(payload.password)
            purpose = "verify_email" if mfa_required(db, user) else "full"
            old = getattr(request.state, "principal", None)
            created = new_session(db, user, response, request, purpose, old.token_hash if old else None)
            sent = issue_email(db, user, created, "login") if purpose != "full" else False
            audit(db, "password_verified", user.id)
            db.commit()
            return {"authenticated": purpose == "full", "challenge": purpose if purpose != "full" else None, "email_sent": sent}

    @app.post("/auth/activate")
    def activate(payload: ActivateInput, request: Request, response: Response):
        with identity_db() as db:
            throttle(db, request, "activate", token_hash(payload.token))
            invite = db.scalar(select(Invitation).where(Invitation.token_hash == token_hash(payload.token)).with_for_update())
            if not invite or invite.consumed or invite.expires_at < time.time():
                raise HTTPException(400, "This invitation is invalid or expired")
            user = db.scalar(select(User).where(User.id == invite.user_id).with_for_update())
            if not user or not user.active or user.password_hash:
                raise HTTPException(400, "This invitation is no longer available")
            try:
                user.password_hash = password_hash(payload.password)
            except ValueError as error:
                raise HTTPException(422, str(error))
            user.name = payload.name.strip() or user.email
            invite.consumed = True
            db.execute(update(LoginSession).where(LoginSession.user_id == user.id).values(revoked=True))
            purpose = "verify_email" if mfa_required(db, user) else "full"
            created = new_session(db, user, response, request, purpose)
            sent = issue_email(db, user, created, "login") if purpose != "full" else False
            audit(db, "account_activated", user.id)
            db.commit()
            return {"authenticated": purpose == "full", "challenge": purpose if purpose != "full" else None, "email_sent": sent}

    @app.post("/auth/mfa/verify")
    def verify_factor(payload: FactorInput, request: Request, response: Response):
        identity = principal(request, full=False)
        if identity.purpose != "verify_email":
            raise HTTPException(403, "This session is not a second-factor challenge")
        with identity_db() as db:
            throttle(db, request, "factor", identity.user_id)
            user = db.scalar(select(User).where(User.id == identity.user_id).with_for_update())
            if not accept_factor(db, user, payload.code, identity.token_hash, "login"):
                audit(db, "email_verification_failed", user.id)
                db.commit()
                raise HTTPException(401, "The verification code is invalid, expired or already used")
            new_session(db, user, response, request, "full", identity.token_hash, identity.store_id, verified=True)
            codes = []
            if mfa_required(db, user) and user.recovery_hashes == "[]":
                codes, user.recovery_hashes = recovery_codes()
            audit(db, "login_mfa_completed", user.id)
            db.commit()
            return {"authenticated": True, "recovery_codes": codes}

    @app.post("/auth/reauth")
    def reauthenticate(payload: ReauthInput, request: Request):
        identity = principal(request)
        with identity_db() as db:
            throttle(db, request, "reauth", identity.user_id)
            user = db.scalar(select(User).where(User.id == identity.user_id).with_for_update())
            if not password_valid(user.password_hash, payload.password) or not accept_factor(db, user, payload.code, identity.token_hash, "reauth"):
                db.commit()
                raise HTTPException(401, "Could not verify your passphrase and second factor")
            db.get(LoginSession, identity.token_hash).mfa_at = time.time()
            audit(db, "sensitive_action_reauthenticated", user.id, identity.store_id)
            db.commit()
            return {"verified": True}

    @app.post("/auth/mfa/resend")
    def resend_email(request: Request):
        identity = principal(request, full=False)
        if identity.purpose not in ("verify_email", "full"):
            raise HTTPException(403, "This session cannot request a verification code")
        with identity_db() as db:
            throttle(db, request, "resend", identity.user_id, limit=5)
            user = db.get(User, identity.user_id)
            session = db.get(LoginSession, identity.token_hash)
            sent = issue_email(db, user, session, "login" if identity.purpose == "verify_email" else "reauth")
            db.commit()
            if not sent:
                raise HTTPException(503, "Email delivery is unavailable. Configure Gmail send-only OAuth or use a saved recovery code.")
            return {"email_sent": True}

    @app.get("/auth/security")
    def account_security(request: Request):
        identity = principal(request)
        with identity_db() as db:
            user = db.get(User, identity.user_id)
            return {"email": user.email, "email_verified": bool(user.email_verified_at),
                    "mfa_required": mfa_required(db, user), "recovery_codes_remaining": len(json.loads(user.recovery_hashes))}

    @app.post("/auth/password")
    def change_password(payload: PasswordChangeInput, request: Request, response: Response):
        identity = principal(request)
        with identity_db() as db:
            throttle(db, request, "password_change", identity.user_id)
            user = db.scalar(select(User).where(User.id == identity.user_id).with_for_update())
            if not password_valid(user.password_hash, payload.password) or not accept_factor(db, user, payload.code, identity.token_hash, "reauth"):
                db.commit()
                raise HTTPException(401, "Could not verify your passphrase and email code")
            try:
                user.password_hash = password_hash(payload.new_password)
            except ValueError as error:
                raise HTTPException(422, str(error))
            db.execute(update(LoginSession).where(LoginSession.user_id == user.id).values(revoked=True))
            new_session(db, user, response, request, "full", selected=identity.store_id, verified=True)
            audit(db, "password_changed_sessions_revoked", user.id, identity.store_id)
            db.commit()
            return {"changed": True, "message": "Passphrase changed. All earlier sessions were revoked."}

    @app.post("/auth/recovery-codes")
    def regenerate_recovery(payload: ReauthInput, request: Request):
        identity = principal(request)
        with identity_db() as db:
            throttle(db, request, "recovery_regeneration", identity.user_id)
            user = db.scalar(select(User).where(User.id == identity.user_id).with_for_update())
            if not password_valid(user.password_hash, payload.password) or not accept_factor(db, user, payload.code, identity.token_hash, "reauth"):
                db.commit()
                raise HTTPException(401, "Could not verify your passphrase and email code")
            codes, user.recovery_hashes = recovery_codes()
            db.get(LoginSession, identity.token_hash).mfa_at = time.time()
            audit(db, "recovery_codes_regenerated", user.id)
            db.commit()
            return {"recovery_codes": codes}

    @app.get("/auth/sessions")
    def active_sessions(request: Request):
        identity = principal(request)
        with identity_db() as db:
            rows = db.scalars(select(LoginSession).where(LoginSession.user_id == identity.user_id, LoginSession.revoked.is_(False), LoginSession.purpose == "full", LoginSession.expires_at > time.time()).order_by(LoginSession.last_seen.desc()).limit(20)).all()
            return [{"current": row.token_hash == identity.token_hash, "last_seen": row.last_seen, "expires_at": row.expires_at} for row in rows]

    @app.post("/auth/sessions/revoke-others")
    def revoke_others(request: Request):
        identity = principal(request)
        recent_mfa(identity)
        with identity_db() as db:
            db.execute(update(LoginSession).where(LoginSession.user_id == identity.user_id, LoginSession.token_hash != identity.token_hash).values(revoked=True))
            audit(db, "other_sessions_revoked", identity.user_id)
            db.commit()
            return {"revoked": True}

    @app.post("/auth/switch-business")
    def switch_business(payload: SwitchInput, request: Request, response: Response):
        identity = principal(request)
        with identity_db() as db:
            user = db.get(User, identity.user_id)
            store = db.get(Store, payload.store_id)
            if not store or not store.active or (not user.platform_admin and payload.store_id not in [item["id"] for item in memberships(db, user.id)]):
                raise HTTPException(403, "This business is not available to your account")
            new_session(db, user, response, request, "full", identity.token_hash, payload.store_id, mfa_timestamp=identity.mfa_at, preserve_expiry=True)
            audit(db, "business_selected", user.id, store.id)
            db.commit()
            return {"selected": store.id}

    @app.post("/auth/logout")
    def logout(request: Request, response: Response):
        identity = getattr(request.state, "principal", None)
        if identity:
            with identity_db() as db:
                db.get(LoginSession, identity.token_hash).revoked = True
                audit(db, "logout", identity.user_id, identity.store_id)
                db.commit()
        response.delete_cookie(COOKIE, path="/", secure=PRODUCTION or request.url.scheme == "https", httponly=True, samesite="strict")
        return {"authenticated": False}
