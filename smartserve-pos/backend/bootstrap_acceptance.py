import json
import os
from pathlib import Path
import time

if os.getenv("SMARTSERVE_ENV") != "test":
    raise RuntimeError("Isolated test settings required")

from sqlalchemy import select
from app.bootstrap import bootstrap_configured_admin
from app.identity_models import Invitation, User
from app.security import identity_db
from app.security_primitives import PASSWORDS
from app.tenancy import initialize_identity

initialize_identity()
bootstrap_configured_admin()
outbox = Path(os.environ["SMARTSERVE_TEST_MAIL_OUTBOX"])
messages = [json.loads(path.read_text()) for path in outbox.glob("*.json")]
assert len(messages) == 1 and messages[0]["to"] == "admin@example.test"
assert messages[0]["activation_url"].startswith("https://test.example/activate#")
bootstrap_configured_admin()
assert len(list(outbox.glob("*.json"))) == 1
os.environ["SMARTSERVE_PLATFORM_ADMIN_EMAIL"] = "other@example.test"
try:
    bootstrap_configured_admin()
    raise AssertionError("Administrator reassignment must fail")
except RuntimeError:
    pass
os.environ["SMARTSERVE_PLATFORM_ADMIN_EMAIL"] = "admin@example.test"
with identity_db() as db:
    invitation = db.scalars(select(Invitation)).one()
    invitation.expires_at = time.time() - 1
    db.commit()
bootstrap_configured_admin()
assert len(list(outbox.glob("*.json"))) == 2
with identity_db() as db:
    user = db.scalars(select(User)).one()
    assert user.email == "admin@example.test" and user.platform_admin
    user.password_hash = PASSWORDS.hash("A-test-passphrase-1234")
    db.commit()
bootstrap_configured_admin()
assert len(list(outbox.glob("*.json"))) == 2
print("PASS: configured-admin email bootstrap, one-admin policy, reissue and permanent signup closure")
