import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import unittest


class SecurityAcceptanceTests(unittest.TestCase):
    def test_private_automatic_admin_bootstrap(self):
        with tempfile.TemporaryDirectory(prefix="smartserve-bootstrap-tests-") as temp:
            directory = Path(temp)
            env = dict(os.environ, SMARTSERVE_ENV="test", DATABASE_URL="sqlite:///" + (directory / "identity.db").as_posix(),
                       SMARTSERVE_LOCAL_DATA=str(directory / "private"), SMARTSERVE_AUTH_SECRET=secrets.token_urlsafe(48),
                       SMARTSERVE_PLATFORM_ADMIN_EMAIL="admin@example.test", SMARTSERVE_PUBLIC_ORIGIN="https://test.example",
                       SMARTSERVE_BOOTSTRAP_ADMIN="true", SMARTSERVE_TEST_MAIL_OUTBOX=str(directory / "outbox"))
            result = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("bootstrap_acceptance.py"))], env=env,
                                    cwd=Path(__file__).parent, text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_account_mfa_permissions_and_cross_business_isolation(self):
        with tempfile.TemporaryDirectory(prefix="smartserve-security-tests-") as temp:
            directory = Path(temp)
            env = dict(os.environ, SMARTSERVE_ENV="test", DATABASE_URL="sqlite:///" + (directory / "identity.db").as_posix(),
                       SMARTSERVE_LOCAL_DATA=str(directory / "private"), SMARTSERVE_AUTH_SECRET=secrets.token_urlsafe(48),
                       SMARTSERVE_PLATFORM_ADMIN_EMAIL="admin@example.test", SMARTSERVE_PUBLIC_ORIGIN="http://testserver",
                       SMARTSERVE_BOOTSTRAP_ADMIN="false", SMARTSERVE_TEST_MAIL_OUTBOX=str(directory / "outbox"), SMARTSERVE_SECURITY_RESULTS=str(directory / "results.json"))
            result = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("security_acceptance.py"))], env=env,
                                    cwd=Path(__file__).parent, text=True, capture_output=True, timeout=120)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            results = json.loads((directory / "results.json").read_text())
            self.assertGreater(len(results), 50)
            self.assertTrue(all(item["passed"] for item in results))


if __name__ == "__main__":
    unittest.main()
