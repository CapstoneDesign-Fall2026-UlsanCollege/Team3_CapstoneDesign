import os
from contextvars import ContextVar

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://smartserve:smartserve_dev@localhost:5432/smartserve")
for prefix in ("postgres://", "postgresql://"):
    if DATABASE_URL.startswith(prefix):
        DATABASE_URL = DATABASE_URL.replace(prefix, "postgresql+psycopg://", 1)
        break

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
tenant_scope: ContextVar[str | None] = ContextVar("smartserve_tenant", default=None)


class Base(DeclarativeBase):
    pass


def get_db():
    from fastapi import HTTPException
    from .tenancy import tenant_engine
    namespace = tenant_scope.get()
    if namespace is None:
        raise HTTPException(403, "Select an authorized business first")
    db = sessionmaker(bind=tenant_engine(namespace), autocommit=False, autoflush=False)()
    try:
        yield db
    finally:
        db.close()
