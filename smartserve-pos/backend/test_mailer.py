import base64
import io
import json
import os
import unittest
from unittest.mock import patch

from app.mailer import send_login_code
from app.security_primitives import email_address, email_code_mac


class Response(io.BytesIO):
    status = 200


class GmailDeliveryTests(unittest.TestCase):
    def test_gmail_uses_https_token_refresh_and_send_only_endpoint(self):
        requests = []
        def urlopen(request, **kwargs):
            requests.append(request)
            return Response(json.dumps({"access_token": "test-access"} if len(requests) == 1 else {"id": "test-message"}).encode())
        settings = dict(SMARTSERVE_ENV="local", MAIL_PROVIDER="gmail_api", GMAIL_SENDER="sender@example.test",
                        GMAIL_CLIENT_ID="test-client", GMAIL_CLIENT_SECRET="test-secret", GMAIL_REFRESH_TOKEN="test-refresh")
        with patch.dict(os.environ, settings), patch("app.mailer.urllib.request.urlopen", side_effect=urlopen):
            send_login_code("owner@example.test", "123456")
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0].full_url, "https://oauth2.googleapis.com/token")
        self.assertEqual(requests[1].full_url, "https://gmail.googleapis.com/gmail/v1/users/me/messages/send")
        raw = json.loads(requests[1].data)["raw"]
        message = base64.urlsafe_b64decode(raw).decode()
        self.assertIn("To: owner@example.test", message)
        self.assertIn("123456", message)
        self.assertEqual(requests[1].get_header("Authorization"), "Bearer test-access")

    def test_email_header_injection_and_multiple_recipients_rejected(self):
        for value in ("a@example.com\r\nBcc: x@example.com", "victim@example.com,attacker", "a<b@example.com", "a@example.com;attacker"):
            with self.assertRaises(ValueError):
                email_address(value)

    def test_email_code_hash_is_bound_to_its_session(self):
        self.assertNotEqual(email_code_mac("session-one", "123456"), email_code_mac("session-two", "123456"))


if __name__ == "__main__":
    unittest.main()
