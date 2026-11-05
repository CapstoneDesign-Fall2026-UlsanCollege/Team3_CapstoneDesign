"""Offline, server-operator-only bootstrap. Never creates a shared password.

Set SMARTSERVE_PLATFORM_ADMIN_EMAIL, then:
python manage_security.py bootstrap-admin --output /private/admin-activation.txt
"""
import argparse
import getpass
import os
from pathlib import Path
import secrets
import subprocess
import time
import json
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.identity_models import Invitation, User
from app.security import audit, identity_db
from app.security_primitives import auth_key, config, email_address, token_hash
from app.tenancy import LOCAL_ROOT, initialize_identity


def private_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as file:
        file.write(content)
    path.chmod(0o600)
    if os.name == "nt":
        owner = os.environ.get("USERDOMAIN", "") + "\\" + getpass.getuser()
        subprocess.run(["icacls", str(path), "/inheritance:r", "/grant:r", f"{owner}:(F)", "SYSTEM:(F)"], check=True, stdout=subprocess.DEVNULL)


def bootstrap(output):
    configured = config("SMARTSERVE_PLATFORM_ADMIN_EMAIL")
    if not configured:
        raise RuntimeError("Set SMARTSERVE_PLATFORM_ADMIN_EMAIL to your private administrator email first")
    email = email_address(configured)
    auth_key()
    initialize_identity()
    if output.exists():
        raise RuntimeError("Choose a new private output file; existing files are never overwritten")
    with identity_db() as db:
        if db.scalar(select(User.id).where(User.platform_admin.is_(True))):
            raise RuntimeError("A platform administrator already exists; bootstrap is permanently closed for this database")
        if db.scalar(select(User.id).where(User.email == email)):
            raise RuntimeError("This email already belongs to a business account; no automatic privilege escalation is allowed")
        user = User(id=uuid4().hex, email=email, name="Platform administrator", platform_admin=True,
                    active=True, mfa_required=True, created_at=time.time())
        db.add(user)
        db.flush()
        raw = secrets.token_urlsafe(48)
        db.add(Invitation(token_hash=token_hash(raw), user_id=user.id, expires_at=time.time() + 86400, consumed=False))
        origin = config("SMARTSERVE_PUBLIC_ORIGIN", "http://localhost:8000").rstrip("/")
        private_file(output, f"Private SmartServe platform-admin activation\n\nAccount: {email}\n\n{origin}/activate#{raw}\n\nExpires in 24 hours. Use once, choose your own passphrase, verify the code sent to your email, and save recovery codes offline. Never commit or share this file. No email has been sent.\n")
        audit(db, "platform_admin_bootstrapped", user.id)
        db.commit()
    print(f"Created one-use activation instructions in: {output}")
    print("No password, factor seed or invitation token was printed.")


def configure_gmail_api(client_secrets, sender):
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.id_token import verify_oauth2_token
    if os.getenv("SMARTSERVE_ENV") == "production":
        raise RuntimeError("Run Google authorization on your own computer, then configure protected Render environment variables")
    email = email_address(sender)
    path = LOCAL_ROOT / "security-config.json"
    if path.exists():
        raise RuntimeError("Private configuration already exists. Back it up locally before re-authorizing; it is not overwritten automatically.")
    document = json.loads(client_secrets.read_text(encoding="utf-8"))
    installed = document.get("installed", {})
    if installed.get("token_uri") != "https://oauth2.googleapis.com/token" or installed.get("auth_uri") not in ("https://accounts.google.com/o/oauth2/auth", "https://accounts.google.com/o/oauth2/v2/auth"):
        raise RuntimeError("Use an official Google Desktop-app OAuth client JSON; custom authorization endpoints are not accepted")
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/gmail.send"], autogenerate_code_verifier=True)
    credentials = flow.run_local_server(host="localhost", port=0, open_browser=True, access_type="offline", prompt="consent", login_hint=email,
                                        authorization_prompt_message="Complete Google send-only authorization in the browser opened for you.", success_message="SmartServe authorization received. You can close this window.")
    claims = verify_oauth2_token(credentials.id_token, Request(), credentials.client_id)
    if not claims.get("email_verified") or claims.get("email", "").lower() != email:
        raise RuntimeError("The Google account does not match the requested sender. Nothing was saved.")
    if not credentials.refresh_token or "https://www.googleapis.com/auth/gmail.send" not in (credentials.granted_scopes or credentials.scopes or []):
        raise RuntimeError("Google did not grant offline send-only permission. Repeat consent with the required scope.")
    granted = credentials.granted_scopes or credentials.scopes or []
    if any(("/auth/gmail." in scope and scope != "https://www.googleapis.com/auth/gmail.send") or scope.startswith("https://mail.google.com/") for scope in granted):
        raise RuntimeError("Google returned broader mailbox permissions than send-only. Revoke the app's old grant and authorize only the requested scopes.")
    settings = {"MAIL_PROVIDER": "gmail_api", "GMAIL_SENDER": email, "GMAIL_CLIENT_ID": credentials.client_id,
                "GMAIL_CLIENT_SECRET": credentials.client_secret, "GMAIL_REFRESH_TOKEN": credentials.refresh_token,
                "SMARTSERVE_PLATFORM_ADMIN_EMAIL": email, "SMARTSERVE_PUBLIC_ORIGIN": "http://localhost:8000",
                "SMARTSERVE_AUTH_SECRET": secrets.token_urlsafe(48)}
    private_file(path, json.dumps(settings, indent=2))
    print(f"Saved private Gmail send-only configuration: {path}")
    print("No Google password, access token or refresh token was printed. Transfer secrets only to protected Render environment settings.")


def export_render_env(output, origin):
    from urllib.parse import urlsplit
    parsed = urlsplit(origin)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise RuntimeError("Provide only your HTTPS Render origin")
    names = ["MAIL_PROVIDER", "GMAIL_SENDER", "GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET", "GMAIL_REFRESH_TOKEN", "SMARTSERVE_PLATFORM_ADMIN_EMAIL", "SMARTSERVE_AUTH_SECRET"]
    values = {name: config(name) for name in names}
    if any(not value for value in values.values()):
        raise RuntimeError("Complete local Google OAuth authorization first")
    values.update(SMARTSERVE_ENV="production", SMARTSERVE_PUBLIC_ORIGIN=origin.rstrip("/"), SMARTSERVE_BOOTSTRAP_ADMIN="true")
    if any("\n" in value or "\r" in value for value in values.values()):
        raise RuntimeError("Environment values must not contain line breaks")
    private_file(output, "\n".join(f"{key}={value}" for key, value in values.items()) + "\n")
    print(f"Private Render environment file saved: {output}")
    print("Import it only into protected Render environment settings. Do not share or commit it.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["bootstrap-admin", "configure-gmail-api", "export-render-env"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--client-secrets", type=Path)
    parser.add_argument("--email")
    parser.add_argument("--origin")
    args = parser.parse_args()
    if args.command == "configure-gmail-api":
        if not args.client_secrets or not args.email:
            parser.error("configure-gmail-api requires --client-secrets and --email")
        configure_gmail_api(args.client_secrets.resolve(), args.email)
    elif args.command == "export-render-env":
        if not args.output or not args.origin:
            parser.error("export-render-env requires --output and --origin")
        export_render_env(args.output.resolve(), args.origin)
    elif args.output:
        bootstrap(args.output.resolve())
    else:
        parser.error("bootstrap-admin requires --output pointing to a private file")
