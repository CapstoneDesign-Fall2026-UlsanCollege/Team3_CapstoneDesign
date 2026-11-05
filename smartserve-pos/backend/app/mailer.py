"""TLS-only SMTP delivery. Local test outboxes are impossible in production."""
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
import base64
import json
import os
from pathlib import Path
import secrets
import urllib.parse
import urllib.request

from .security_primitives import config, email_address


def deliver(recipient, subject, body, test_fields=None):
    if os.getenv("SMARTSERVE_ENV") == "test":
        directory = os.getenv("SMARTSERVE_TEST_MAIL_OUTBOX")
        if not directory:
            raise RuntimeError("Tests require a private test outbox; real email is disabled")
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        file = path / (secrets.token_hex(16) + ".json")
        file.write_text(json.dumps({"to": recipient, **(test_fields or {})}), encoding="utf-8")
        file.chmod(0o600)
        return
    provider = config("MAIL_PROVIDER", "gmail_api")
    if provider != "gmail_api":
        raise RuntimeError("Only the Gmail HTTPS API is enabled for this deployment")
    sender = config("GMAIL_SENDER")
    if not sender:
        raise RuntimeError("Gmail delivery is not configured. Authorize send-only Google OAuth in private server settings.")
    email_address(sender)
    email_address(recipient)
    message = EmailMessage()
    message["Subject"] = subject
    message["From"], message["To"] = sender, recipient
    message["Date"], message["Message-ID"] = formatdate(), make_msgid()
    message.set_content(body)
    if provider == "gmail_api":
        client_id, client_secret, refresh_token = config("GMAIL_CLIENT_ID"), config("GMAIL_CLIENT_SECRET"), config("GMAIL_REFRESH_TOKEN")
        if not all((client_id, client_secret, refresh_token)):
            raise RuntimeError("Google OAuth send-only credentials are missing")
        refresh = urllib.request.Request("https://oauth2.googleapis.com/token", data=urllib.parse.urlencode({
            "client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token, "grant_type": "refresh_token"}).encode(), headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
        with urllib.request.urlopen(refresh, timeout=12) as result:
            access_token = json.load(result)["access_token"]
        payload = json.dumps({"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}).encode()
        send = urllib.request.Request("https://gmail.googleapis.com/gmail/v1/users/me/messages/send", data=payload,
                                      headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(send, timeout=12) as result:
            if result.status not in (200, 202):
                raise RuntimeError("Google rejected the email delivery")
        return
    raise RuntimeError("Only the Gmail HTTPS API is enabled for this deployment")


def send_login_code(recipient, code):
    deliver(recipient, "Your SmartServe sign-in code", f"Your SmartServe verification code is:\n\n{code}\n\nIt expires in 5 minutes and can be used once. Never share this code. SmartServe support will never ask you for it. If you did not request it, do not use it.\n", {"code": code})


def send_activation_link(recipient, url):
    deliver(recipient, "Activate your private SmartServe platform-admin account", f"Your private platform-admin account is ready.\n\nOpen this one-use link to choose your own passphrase:\n{url}\n\nThis link expires after 24 hours. You must also verify an email code before accessing the platform. Do not share this link or your codes.\n", {"activation_url": url})
