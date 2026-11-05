"""Isolated HTTP acceptance scenarios. Refuses to run against non-test settings."""
import json
import os
from pathlib import Path
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

if os.getenv("SMARTSERVE_ENV") != "test":
    raise RuntimeError("Security acceptance must use SMARTSERVE_ENV=test and isolated databases")

from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.identity_models import EmailChallenge, LoginSession, User
from app.security import identity_db
from app.security_primitives import COOKIE, password_valid, token_hash
from manage_security import bootstrap

PASSWORD = "A-unique-test-passphrase-2026!"
OUTBOX = Path(os.environ["SMARTSERVE_TEST_MAIL_OUTBOX"])
RESULTS = []


def check(name, expected, actual):
    RESULTS.append({"check": name, "passed": expected == actual})
    assert expected == actual, f"Failed: {name} (values omitted to protect test credentials)"


def csrf(client):
    return {"X-CSRF-Token": client.get("/auth/session").json().get("csrf_token", "")}


def post(client, path, body=None, method="POST"):
    return client.request(method, path, json=body, headers=csrf(client))


def latest_code(email):
    messages = [json.loads(path.read_text()) | {"mtime": path.stat().st_mtime_ns} for path in OUTBOX.glob("*.json")]
    return max((item for item in messages if item["to"] == email), key=lambda item: item["mtime"])["code"]


def activate(url, email, verify=True):
    client = TestClient(app)
    result = client.post("/auth/activate", json={"token": url.split("#", 1)[1], "name": email.split("@")[0], "password": PASSWORD})
    check("invitation activation accepted", 200, result.status_code)
    recovery = []
    if result.json().get("challenge"):
        check("password alone cannot access business", 401, client.get("/menu").status_code)
        if verify:
            proof = post(client, "/auth/mfa/verify", {"code": latest_code(email)})
            check("email code completes MFA", 200, proof.status_code)
            recovery = proof.json().get("recovery_codes", [])
    return client, recovery


def login(email, verify=True):
    client = TestClient(app)
    response = client.post("/auth/login", json={"email": email, "password": PASSWORD})
    check("password login starts valid challenge", 200, response.status_code)
    if response.json().get("challenge") and verify:
        check("email challenge is not a full session", False, client.get("/auth/session").json()["authenticated"])
        response = post(client, "/auth/mfa/verify", {"code": latest_code(email)})
        check("login second factor accepted", 200, response.status_code)
    return client


def main():
    with TestClient(app) as public:
        for endpoint in ("/menu", "/orders", "/inventory", "/business", "/tables", "/dashboard/sales", "/owner/menu", "/owner/work", "/platform/businesses"):
            check("anonymous denial " + endpoint, 401, public.get(endpoint).status_code)
        check("denials carry no-store policy", "no-store", public.get("/menu").headers.get("cache-control"))
        check("denials cannot be MIME-sniffed", "nosniff", public.get("/menu").headers.get("x-content-type-options"))
        public.cookies.set("smartserve_owner", "9999999999.invalid-old-signature")
        check("old shared cookie cannot authenticate", 401, public.get("/orders").status_code)
        activation_file = Path(os.environ["SMARTSERVE_LOCAL_DATA"]) / "admin-invitation.txt"
        bootstrap(activation_file)
        link = next(line for line in activation_file.read_text().splitlines() if "/activate#" in line)
        admin, codes = activate(link, "admin@example.test")
        check("privileged recovery codes generated once", 10, len(codes))
        check("invitation cannot be replayed", 400, public.post("/auth/activate", json={"token": link.split("#")[1], "name": "Other", "password": PASSWORD}).status_code)
        try:
            bootstrap(activation_file.with_name("second-admin.txt"))
            check("second platform admin bootstrap blocked", True, False)
        except RuntimeError:
            check("second platform admin bootstrap blocked", True, True)
        stores = []
        for name in ("Business A", "Business B"):
            result = post(admin, "/platform/businesses", {"name": name})
            check("platform creates isolated business", 201, result.status_code)
            store = result.json()
            stores.append(store)
            check("platform selects business", 200, post(admin, "/auth/switch-business", {"store_id": store["id"]}).status_code)
            result = post(admin, "/owner/business/setup", {"name": name, "business_type": "retail", "operation_mode": "both", "catalog_action": "samples"})
            check("platform alone configures business", 200, result.status_code)
            menu = admin.get("/owner/menu").json()
            item = menu[0]
            response = post(admin, f"/owner/menu/{item['id']}", {"name": name + " exclusive", "price": item["price"], "category": item["category"], "item_type": item["item_type"], "sku": item["sku"], "recipe": item["recipe"]}, method="PUT")
            check("business-specific catalog saved", 200, response.status_code)
        owner_links = []
        for store, email in zip(stores, ("ownera@example.test", "ownerb@example.test")):
            response = post(admin, "/platform/invitations", {"email": email, "name": "Business owner", "store_id": store["id"], "role": "owner"})
            check("platform invites store owner", 200, response.status_code)
            owner_links.append(response.json()["activation_url"])
        owner_a, recovery_a = activate(owner_links[0], "ownera@example.test")
        owner_b, _ = activate(owner_links[1], "ownerb@example.test")
        check("owner has owner role", "owner", owner_a.get("/auth/session").json()["user"]["role"])
        check("owner cannot open platform console API", 403, owner_a.get("/platform/businesses").status_code)
        check("owner cannot run setup", 403, post(owner_a, "/owner/business/setup", {"name": "Attack", "business_type": "retail", "operation_mode": "both"}).status_code)
        check("owner cannot choose another business", 403, post(owner_a, "/auth/switch-business", {"store_id": stores[1]["id"]}).status_code)
        check("owner cannot choose legacy business", 403, post(owner_a, "/auth/switch-business", {"store_id": "legacy"}).status_code)
        check("query parameter cannot switch tenant", True, all(item["name"] != "Business B exclusive" for item in owner_a.get("/menu?store_id=" + stores[1]["id"]).json()))
        item_a = next(item for item in owner_a.get("/menu").json() if item["name"] == "Business A exclusive")
        order = post(owner_a, "/orders", {"order_type": "in_store", "items": [{"menu_item_id": item_a["id"], "quantity": 1}]}).json()
        check("order ID is inaccessible in another tenant", 404, owner_b.get(f"/orders/{order['id']}").status_code)
        check("another tenant sees no first-tenant orders", [], owner_b.get("/orders").json())
        check("authenticated write without CSRF rejected", 403, owner_a.post("/orders", json={"order_type": "in_store", "items": [{"menu_item_id": item_a["id"], "quantity": 1}]}).status_code)
        check("cross-site request rejected", 403, owner_a.post("/auth/logout", headers={**csrf(owner_a), "Origin": "https://untrusted.example"}).status_code)
        check("authorized payment succeeds", 200, post(owner_a, f"/orders/{order['id']}/pay", {"method": "cash"}).status_code)
        check("other store sales remain zero", 0, owner_b.get("/dashboard/sales").json()["sales_total"])
        invite = post(owner_a, "/owner/staff/invitations", {"email": "cashier@example.test", "name": "Cashier", "store_id": stores[0]["id"], "role": "cashier", "require_mfa": False})
        check("owner can invite own cashier", 200, invite.status_code)
        cashier, _ = activate(invite.json()["activation_url"], "cashier@example.test")
        check("cashier can read authorized catalog", 200, cashier.get("/menu").status_code)
        for endpoint in ("/dashboard/sales", "/owner/inventory", "/owner/staff", "/platform/businesses"):
            check("cashier restricted " + endpoint, 403, cashier.get(endpoint).status_code)
        check("cashier cannot edit catalog", 403, post(cashier, "/owner/menu", {"name": "Bad", "price": 1, "item_type": "service"}).status_code)
        check("owner cannot grant admin role", 422, post(owner_a, "/owner/staff/invitations", {"email": "bad@example.test", "name": "Bad", "store_id": stores[0]["id"], "role": "platform_admin"}).status_code)
        check("owner cannot invite into another store", 403, post(owner_a, "/owner/staff/invitations", {"email": "bad@example.test", "name": "Bad", "store_id": stores[1]["id"], "role": "cashier"}).status_code)
        user_id = cashier.get("/auth/session").json()["user"]["id"]
        check("owner disables cashier", 200, post(owner_a, f"/owner/staff/{user_id}/access", {"active": False}, method="PUT").status_code)
        check("disabled cashier session revoked", 401, cashier.get("/menu").status_code)
        owner_raw = owner_a.cookies.get(COOKIE)
        check("logout succeeds", 200, post(owner_a, "/auth/logout").status_code)
        stolen = TestClient(app)
        stolen.cookies.set(COOKIE, owner_raw)
        check("logged-out cookie cannot be replayed", 401, stolen.get("/menu").status_code)
        challenge = login("ownera@example.test", verify=False)
        with identity_db() as db:
            stored = db.get(EmailChallenge, token_hash(challenge.cookies.get(COOKIE)))
            stored.expires_at = time.time() - 1
            db.commit()
        check("expired email code rejected", 401, post(challenge, "/auth/mfa/verify", {"code": latest_code("ownera@example.test")}).status_code)
        challenge = login("ownera@example.test", verify=False)
        saved_code = latest_code("ownera@example.test")
        pending_cookie = challenge.cookies.get(COOKIE)
        pending_headers = csrf(challenge)
        def use_code(_):
            isolated = TestClient(app)
            isolated.cookies.set(COOKIE, pending_cookie)
            return isolated.post("/auth/mfa/verify", json={"code": saved_code}, headers=pending_headers).status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            check("email code consumed atomically once", [200, 401], sorted(pool.map(use_code, range(2))))
        recovery_client = login("ownera@example.test", verify=False)
        check("one-use recovery code works with password", 200, post(recovery_client, "/auth/mfa/verify", {"code": recovery_a[0]}).status_code)
        replay = login("ownera@example.test", verify=False)
        check("recovery code cannot be reused", 401, post(replay, "/auth/mfa/verify", {"code": recovery_a[0]}).status_code)
        limited = login("ownerb@example.test", verify=False)
        original = latest_code("ownerb@example.test")
        wrong = "000000" if original != "000000" else "000001"
        for _ in range(5):
            check("wrong email code rejected", 401, post(limited, "/auth/mfa/verify", {"code": wrong}).status_code)
        check("correct code rejected after guessing limit", 401, post(limited, "/auth/mfa/verify", {"code": original}).status_code)
        check("resend has a cooldown", 429, post(limited, "/auth/mfa/resend").status_code)
        with identity_db() as db:
            db.get(EmailChallenge, token_hash(limited.cookies.get(COOKIE))).sent_at -= 61
            db.commit()
        check("resend after cooldown succeeds", 200, post(limited, "/auth/mfa/resend").status_code)
        check("resend invalidates previous email code", 401, post(limited, "/auth/mfa/verify", {"code": original}).status_code)
        check("new email code is accepted", 200, post(limited, "/auth/mfa/verify", {"code": latest_code("ownerb@example.test")}).status_code)
        original_owner_b_cookie = owner_b.cookies.get(COOKIE)
        check("sensitive action code sent", 200, post(owner_b, "/auth/mfa/resend").status_code)
        changed = post(owner_b, "/auth/password", {"password": PASSWORD, "new_password": PASSWORD + "-changed", "code": latest_code("ownerb@example.test")})
        check("passphrase change requires verified email and password", 200, changed.status_code)
        old_owner_b = TestClient(app)
        old_owner_b.cookies.set(COOKIE, original_owner_b_cookie)
        check("passphrase change revokes prior cookie", 401, old_owner_b.get("/menu").status_code)
        check("passphrase change revokes other sessions", 401, limited.get("/menu").status_code)
        attempt = TestClient(app)
        for _ in range(10):
            attempt.post("/auth/login", json={"email": "nonexistent@example.test", "password": "wrong-password"})
        check("password guessing rate limited", 429, attempt.post("/auth/login", json={"email": "nonexistent@example.test", "password": "wrong-password"}).status_code)
        with identity_db() as db:
            user = db.scalar(select(User).where(User.email == "ownerb@example.test"))
            check("password stored with Argon2id", True, user.password_hash.startswith("$argon2id$"))
            check("stored password verifies correctly", True, password_valid(user.password_hash, PASSWORD + "-changed"))
            active = db.get(LoginSession, token_hash(owner_b.cookies.get(COOKIE)))
            check("session token stored only as a hash", False, active.token_hash == owner_b.cookies.get(COOKIE))
            active.last_seen = time.time() - 2000
            db.commit()
        check("idle session expires", 401, owner_b.get("/menu").status_code)
        check("session provides same-origin CSRF proof", True, "csrf_token" in admin.get("/auth/session").json())
        with identity_db() as db:
            row = db.get(LoginSession, token_hash(admin.cookies.get(COOKIE)))
            row.mfa_at = time.time() - 700
            before_expiry = row.expires_at
            db.commit()
        check("business switching still allowed after recent-MFA window", 200, post(admin, "/auth/switch-business", {"store_id": stores[0]["id"]}).status_code)
        with identity_db() as db:
            row = db.get(LoginSession, token_hash(admin.cookies.get(COOKIE)))
            check("business switch does not refresh MFA age", True, row.mfa_at < time.time() - 600)
            check("business switch preserves absolute session expiry", before_expiry, row.expires_at)
        check("stale MFA cannot perform platform changes", 403, post(admin, "/platform/businesses", {"name": "Must reauthenticate"}).status_code)
    Path(os.environ["SMARTSERVE_SECURITY_RESULTS"]).write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")
    print(f"PASS: {len(RESULTS)} isolated security assertions")


if __name__ == "__main__":
    main()
