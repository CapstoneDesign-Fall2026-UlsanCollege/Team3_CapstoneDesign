"""Owner login and signed, expiring browser sessions."""
import hashlib
import hmac
import os
import secrets
import time

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

SESSION_KEY = os.getenv("SMARTSERVE_SESSION_SECRET", secrets.token_hex(32)).encode()
COOKIE = "smartserve_owner"
SESSION_SECONDS = 8 * 60 * 60


def authenticated(request: Request) -> bool:
    token = request.cookies.get(COOKIE, "")
    try:
        expires, signature = token.split(".", 1)
        expected = hmac.new(SESSION_KEY, expires.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected) and int(expires) > time.time()
    except (ValueError, TypeError):
        return False


class Login(BaseModel):
    username: str
    password: str


def install_owner_auth(app):
    @app.middleware("http")
    async def protect_owner(request: Request, call_next):
        path = request.url.path.rstrip("/")
        owner_route = path == "/owner" or path.startswith("/owner/")
        public_recipe_read = path == "/owner/menu" and request.method == "GET"
        protected = (owner_route and not public_recipe_read) or path == "/dashboard" or path.startswith("/dashboard/")
        if protected and request.method != "OPTIONS" and not authenticated(request):
            return JSONResponse({"detail": "Owner login required."}, status_code=401)
        return await call_next(request)

    @app.get("/auth/session")
    def session(request: Request, response: Response):
        response.headers["Cache-Control"] = "no-store"
        return {"authenticated": authenticated(request)}

    @app.post("/auth/login")
    def login(credentials: Login, request: Request, response: Response):
        username = os.getenv("SMARTSERVE_OWNER_USERNAME", "sherap")
        password_hash = os.getenv("SMARTSERVE_OWNER_PASSWORD_SHA256")
        if not password_hash:
            password = os.getenv("SMARTSERVE_OWNER_PASSWORD", "1234$")
            password_hash = hashlib.sha256(password.encode()).hexdigest()
        supplied_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
        if not (hmac.compare_digest(credentials.username.encode(), username.encode())
                and hmac.compare_digest(supplied_hash, password_hash)):
            raise HTTPException(status_code=401, detail="Incorrect username or password.")
        expires = str(int(time.time()) + SESSION_SECONDS)
        signature = hmac.new(SESSION_KEY, expires.encode(), hashlib.sha256).hexdigest()
        secure = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
        response.set_cookie(COOKIE, expires + "." + signature, max_age=SESSION_SECONDS,
                            httponly=True, secure=secure, samesite="strict", path="/")
        response.headers["Cache-Control"] = "no-store"
        return {"authenticated": True}

    @app.post("/auth/logout")
    def logout(response: Response):
        response.delete_cookie(COOKIE, path="/", samesite="strict")
        response.headers["Cache-Control"] = "no-store"
        return {"authenticated": False}
