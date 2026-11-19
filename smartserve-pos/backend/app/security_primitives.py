"""Password, MFA, token and deployment configuration primitives."""
import hashlib
import hmac
import json
import os
import re
import secrets
import time

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from .tenancy import LOCAL_ROOT

PASSWORDS = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)
DUMMY_HASH = PASSWORDS.hash(secrets.token_urlsafe(32))
PRODUCTION = os.getenv("SMARTSERVE_ENV") == "production" or os.getenv("RENDER") == "true"
COOKIE = "__Host-smartserve" if PRODUCTION else "smartserve_session"


def config(name, default=""):
    if name in os.environ:
        return os.environ[name]
    if not PRODUCTION:
        path = LOCAL_ROOT / "security-config.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")).get(name, default)
    return default


def auth_key():
    configured = config("SMARTSERVE_AUTH_SECRET")
    if configured:
        if len(configured) < 32:
            raise RuntimeError("SMARTSERVE_AUTH_SECRET must contain at least 32 random characters")
        return configured.encode()
    if PRODUCTION:
        raise RuntimeError("Set SMARTSERVE_AUTH_SECRET before enabling secure production accounts")
    LOCAL_ROOT.mkdir(parents=True, exist_ok=True)
    path = LOCAL_ROOT / "development-auth.key"
    if not path.exists():
        try:
            with path.open("xb") as file:
                file.write(secrets.token_urlsafe(48).encode())
            path.chmod(0o600)
        except FileExistsError:
            pass
    return path.read_bytes().strip()


def token_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()


def email_address(value):
    value = value.strip().lower()
    if len(value) > 254 or not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,63}", value):
        raise ValueError("Enter a valid email address")
    return value


def password_hash(password):
    if not 14 <= len(password) <= 128:
        raise ValueError("Use a passphrase between 14 and 128 characters")
    if password.lower() in {"passwordpassword", "12345678901234", "qwertyqwerty1234"}:
        raise ValueError("Choose a less predictable passphrase")
    return PASSWORDS.hash(password)


def password_valid(encoded, password):
    try:
        return PASSWORDS.verify(encoded or DUMMY_HASH, password)
    except (VerificationError, InvalidHashError):
        return False


def email_code_mac(session_hash, code):
    return hmac.new(auth_key(), f"email-otp:{session_hash}:{code}".encode(), hashlib.sha256).hexdigest()


def recovery_codes():
    codes = [secrets.token_hex(16) for _ in range(10)]
    return codes, json.dumps([token_hash(code) for code in codes])
