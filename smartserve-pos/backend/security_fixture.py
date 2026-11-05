"""Private, isolated browser-test seed; no HTTP endpoint and no real email."""
import os
import time
from uuid import uuid4

if os.getenv("SMARTSERVE_ENV") != "test" or not os.getenv("SMARTSERVE_TEST_MAIL_OUTBOX"):
    raise RuntimeError("Browser fixtures require explicit test mode and a private test outbox")

from sqlalchemy import select
from app.main import create_tables
from app.identity_models import User
from app.security import identity_db
from app.security_primitives import password_hash

create_tables()
with identity_db() as db:
    if db.scalar(select(User.id).where(User.platform_admin.is_(True))):
        raise RuntimeError("Test fixture will not overwrite an existing platform administrator")
    db.add(User(id=uuid4().hex, email="browser-admin@example.test", name="Test platform administrator", platform_admin=True,
                active=True, mfa_required=True, password_hash=password_hash(os.environ["SMARTSERVE_TEST_PASSWORD"]), created_at=time.time()))
    db.commit()
print("Isolated browser-test administrator created. No credential values were printed.")
