"""Physical namespace isolation for each business's existing POS models."""
import os
import re
import time
from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from .database import Base, engine
from .identity_models import IdentityBase, Store

LOCAL_ROOT = Path(os.getenv("SMARTSERVE_LOCAL_DATA", str(Path(__file__).resolve().parents[3] / ".smartserve-local")))


@lru_cache(maxsize=256)
def tenant_engine(namespace: str):
    if namespace == "legacy":
        return engine
    if not re.fullmatch(r"store_[a-f0-9]{32}", namespace):
        raise ValueError("Invalid business namespace")
    if engine.dialect.name == "postgresql":
        return engine.execution_options(schema_translate_map={None: namespace})
    LOCAL_ROOT.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{(LOCAL_ROOT / (namespace + '.db')).as_posix()}", pool_pre_ping=True)


def initialize_identity():
    IdentityBase.metadata.create_all(engine)
    with Session(engine) as db:
        if db.get(Store, "legacy") is None:
            db.add(Store(id="legacy", name="Existing SmartServe store", namespace="legacy", active=True, created_at=time.time()))
            db.commit()


def provision_store(store: Store):
    from .models import BusinessProfile
    if engine.dialect.name == "postgresql":
        # Namespace is generated internally, never interpolated from user input.
        if not re.fullmatch(r"store_[a-f0-9]{32}", store.namespace):
            raise ValueError("Invalid business namespace")
        with engine.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{store.namespace}"'))
    scoped = tenant_engine(store.namespace)
    Base.metadata.create_all(scoped)
    with Session(scoped) as db:
        if db.get(BusinessProfile, 1) is None:
            db.add(BusinessProfile(id=1, name=store.name, business_type="custom"))
            db.commit()
