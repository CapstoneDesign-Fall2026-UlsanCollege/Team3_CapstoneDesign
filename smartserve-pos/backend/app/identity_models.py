"""Control-plane identity tables; never replicated into a tenant schema."""
from sqlalchemy import Boolean, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class IdentityBase(DeclarativeBase):
    pass


class Store(IdentityBase):
    __tablename__ = "security_stores"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    namespace: Mapped[str] = mapped_column(String(64), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[float] = mapped_column(Float)


class User(IdentityBase):
    __tablename__ = "security_users"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    platform_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    mfa_required: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified_at: Mapped[float | None] = mapped_column(Float, nullable=True)
    recovery_hashes: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[float] = mapped_column(Float)
    __table_args__ = (Index("uq_single_platform_admin", "platform_admin", unique=True,
                           postgresql_where=text("platform_admin = true"), sqlite_where=text("platform_admin = 1")),)


class Membership(IdentityBase):
    __tablename__ = "security_memberships"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("security_users.id"))
    store_id: Mapped[str] = mapped_column(ForeignKey("security_stores.id"))
    role: Mapped[str] = mapped_column(String(20))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    __table_args__ = (UniqueConstraint("user_id", "store_id", name="uq_user_store_membership"),)


class LoginSession(IdentityBase):
    __tablename__ = "security_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("security_users.id"))
    store_id: Mapped[str | None] = mapped_column(ForeignKey("security_stores.id"), nullable=True)
    purpose: Mapped[str] = mapped_column(String(20))
    csrf_token: Mapped[str] = mapped_column(String(64))
    expires_at: Mapped[float] = mapped_column(Float)
    last_seen: Mapped[float] = mapped_column(Float)
    mfa_at: Mapped[float | None] = mapped_column(Float, nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)


class Invitation(IdentityBase):
    __tablename__ = "security_invitations"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("security_users.id"))
    expires_at: Mapped[float] = mapped_column(Float)
    consumed: Mapped[bool] = mapped_column(Boolean, default=False)


class EmailChallenge(IdentityBase):
    __tablename__ = "security_email_challenges"
    session_hash: Mapped[str] = mapped_column(ForeignKey("security_sessions.token_hash"), primary_key=True)
    code_mac: Mapped[str] = mapped_column(String(64))
    purpose: Mapped[str] = mapped_column(String(20))
    expires_at: Mapped[float] = mapped_column(Float)
    sent_at: Mapped[float] = mapped_column(Float)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    used: Mapped[bool] = mapped_column(Boolean, default=False)


class Throttle(IdentityBase):
    __tablename__ = "security_throttles"
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    reset_at: Mapped[float] = mapped_column(Float)


class Audit(IdentityBase):
    __tablename__ = "security_audit"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    store_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    action: Mapped[str] = mapped_column(String(80))
    detail: Mapped[str] = mapped_column(String(300), default="")
    created_at: Mapped[float] = mapped_column(Float)
