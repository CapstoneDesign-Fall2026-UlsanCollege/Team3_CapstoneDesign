"""Server-configured bootstrap delivered only to the designated administrator."""
import secrets
import time
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from .identity_models import Invitation, User
from .mailer import send_activation_link
from .security import audit, identity_db
from .security_primitives import config, email_address, token_hash


def bootstrap_configured_admin():
    if config("SMARTSERVE_BOOTSTRAP_ADMIN", "false").lower() != "true":
        return
    email = email_address(config("SMARTSERVE_PLATFORM_ADMIN_EMAIL"))
    origin = config("SMARTSERVE_PUBLIC_ORIGIN").rstrip("/")
    if not origin.startswith("https://"):
        raise RuntimeError("Automatic admin bootstrap requires an HTTPS public origin")
    with identity_db() as db:
        user = db.scalar(select(User).where(User.platform_admin.is_(True)).with_for_update())
        if user:
            if user.email != email:
                raise RuntimeError("Configured admin email does not match the existing administrator; automatic reassignment is forbidden")
            if user.password_hash:
                return
            outstanding = db.scalar(select(Invitation).where(Invitation.user_id == user.id, Invitation.consumed.is_(False), Invitation.expires_at > time.time()))
            if outstanding:
                return
        else:
            if db.scalar(select(User.id).where(User.email == email)):
                raise RuntimeError("A business account already uses the configured admin email; no automatic escalation is allowed")
            user = User(id=uuid4().hex, email=email, name="Platform administrator", platform_admin=True,
                        active=True, mfa_required=True, created_at=time.time())
            db.add(user)
            try:
                db.flush()
            except IntegrityError:
                db.rollback()
                # The unique admin index lets only one worker bootstrap the account.
                if db.scalar(select(User.id).where(User.platform_admin.is_(True))):
                    return
                raise
        db.execute(update(Invitation).where(Invitation.user_id == user.id).values(consumed=True))
        raw = secrets.token_urlsafe(48)
        db.add(Invitation(token_hash=token_hash(raw), user_id=user.id, expires_at=time.time() + 86400, consumed=False))
        send_activation_link(email, origin + "/activate#" + raw)
        audit(db, "configured_admin_invitation_emailed", user.id)
        db.commit()
