"""Fresh automated browser/API check. Never uses the shared demo database.

From the repository root, build the frontend, then run with backend requirements
and Playwright installed. Pass --postgres-bin for a temporary PostgreSQL cluster,
otherwise a temporary SQLite file is used. Personal teammate testing is separate.
"""
import argparse
import hashlib
import html
import json
import mimetypes
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import expect, sync_playwright

REPO = Path(__file__).resolve().parents[2]
FRONTEND = REPO / "smartserve-pos/frontend/dist"
ORIGIN = "http://127.0.0.1:18990"
API = "http://127.0.0.1:18991"
HIDDEN = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


class Proxy(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        pathname = self.path.split("?")[0]
        if pathname.startswith(("/auth/", "/owner/", "/orders", "/menu", "/inventory", "/dashboard/", "/health")):
            return self.proxy()
        filename = (FRONTEND / pathname.lstrip("/")).resolve()
        if not filename.is_relative_to(FRONTEND.resolve()) or not filename.is_file():
            filename = FRONTEND / "index.html"
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(filename))[0] or "application/octet-stream")
        self.end_headers()
        self.wfile.write(filename.read_bytes())

    def do_POST(self):
        self.proxy()

    def do_PUT(self):
        self.proxy()

    def proxy(self):
        payload = self.rfile.read(int(self.headers.get("Content-Length", 0))) if self.command != "GET" else None
        headers = {key: self.headers[key] for key in ("Content-Type", "Cookie") if key in self.headers}
        request = urllib.request.Request(API + self.path, data=payload, method=self.command, headers=headers)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            self.send_response(response.status)
            for key, value in response.getheaders():
                if key.lower() in ("content-type", "set-cookie", "cache-control"):
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.read())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--postgres-bin", type=Path)
    parser.add_argument("--browser", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "evidence/2026-10-28")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for port in (18990, 18991, 18992):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", port))
    if not (FRONTEND / "index.html").exists():
        raise RuntimeError("Build the frontend first: npm --prefix smartserve-pos/frontend run build")
    checks, errors = [], []

    def check(name, expected, actual):
        passed = expected == actual
        checks.append({"check": name, "expected": expected, "actual": actual, "result": "PASS" if passed else "FAIL"})
        if not passed:
            raise AssertionError((name, expected, actual))

    with tempfile.TemporaryDirectory(prefix="smartserve-week8-", ignore_cleanup_errors=True) as temp:
        temp = Path(temp)
        pg_started = False
        process, server, browser = None, None, None
        password = secrets.token_urlsafe(24)
        environment = os.environ.copy()
        environment.update({"PYTHONDONTWRITEBYTECODE": "1", "SMARTSERVE_OWNER_USERNAME": "week8-demo-owner",
                            "SMARTSERVE_OWNER_PASSWORD_SHA256": hashlib.sha256(password.encode()).hexdigest(),
                            "SMARTSERVE_SESSION_SECRET": secrets.token_hex(32)})
        try:
            if args.postgres_bin:
                def pg(command, *extra):
                    return subprocess.run([str(args.postgres_bin / command), *map(str, extra)], check=True,
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=HIDDEN, timeout=60)
                pg("initdb.exe" if os.name == "nt" else "initdb", "-D", temp / "pgdata", "-U", "week8_demo", "--auth=trust", "--encoding=UTF8", "--no-locale")
                pg("pg_ctl.exe" if os.name == "nt" else "pg_ctl", "-D", temp / "pgdata", "-l", temp / "postgres.log", "-o", "-h 127.0.0.1 -p 18992", "-w", "start")
                pg_started = True
                print("Temporary PostgreSQL cluster ready", flush=True)
                environment["DATABASE_URL"] = "postgresql+psycopg://week8_demo@127.0.0.1:18992/postgres"
                database = "fresh temporary PostgreSQL cluster on loopback port 18992"
            else:
                environment["DATABASE_URL"] = "sqlite:///" + str(temp / "sample.db").replace("\\", "/")
                database = "fresh temporary SQLite file"
            with open(temp / "api.log", "w", encoding="utf-8") as log:
                process = subprocess.Popen([sys.executable, "-B", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "18991"],
                                           cwd=REPO / "smartserve-pos/backend", env=environment, stdout=log, stderr=log, creationflags=HIDDEN)
                for _ in range(150):
                    try:
                        with urllib.request.urlopen(API + "/health", timeout=1) as health:
                            if json.load(health)["status"] == "ok":
                                break
                    except Exception:
                        time.sleep(0.1)
                else:
                    raise RuntimeError("Isolated API failed to start. Inspect the temporary startup environment.")
                server = ThreadingHTTPServer(("127.0.0.1", 18990), Proxy)
                print("Isolated API ready; starting browser checks", flush=True)
                threading.Thread(target=server.serve_forever, daemon=True).start()
                with sync_playwright() as playwright:
                    options = {"headless": True}
                    if args.browser:
                        options["executable_path"] = str(args.browser)
                    browser = playwright.chromium.launch(**options)
                    context = browser.new_context(viewport={"width": 1440, "height": 1080})
                    page = context.new_page()
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.route("**/docs.google.com/**", lambda route: route.abort())

                    def shot(name):
                        page.screenshot(path=str(args.output / name), full_page=True)

                    def get(endpoint):
                        response = context.request.get(ORIGIN + endpoint)
                        if response.status != 200:
                            raise AssertionError((endpoint, response.status))
                        return response.json()

                    def put(endpoint, data):
                        response = context.request.put(ORIGIN + endpoint, data=data)
                        check("PUT " + endpoint, 200, response.status)
                        return response.json()

                    page.goto(ORIGIN)
                    expect(page.get_by_role("button", name="Caffè Latte", exact=False)).to_be_enabled()
                    check("public navigation hides owner dashboard", 0, page.get_by_role("button", name="Owner dashboard", exact=True).count())
                    check("anonymous sales requires owner session", 401, context.request.get(ORIGIN + "/dashboard/sales").status)
                    check("anonymous owner inventory requires session", 401, context.request.get(ORIGIN + "/owner/inventory").status)
                    shot("01-public-cashier.png")
                    page.goto(ORIGIN + "/etalogin")
                    expect(page.get_by_role("heading", name="Owner login", exact=True)).to_be_visible()
                    shot("02-owner-login.png")
                    check("owner login accepts isolated test identity", 200, context.request.post(ORIGIN + "/auth/login", data={"username": "week8-demo-owner", "password": password}).status)
                    page.reload()
                    expect(page.get_by_role("heading", name="Owner sales dashboard", exact=True)).to_be_visible()
                    initial_sales = get("/dashboard/sales")
                    check("fresh sales", [0, 0], [initial_sales["paid_orders"], initial_sales["sales_total"]])
                    shot("03-starting-sales.png")
                    initial_stock = get("/inventory")
                    page.goto(ORIGIN)
                    page.get_by_role("button", name="inventory", exact=True).click()
                    expect(page.get_by_role("cell", name="5000 ml", exact=True)).to_be_visible()
                    shot("04-starting-inventory.png")
                    page.get_by_role("button", name="cashier", exact=True).click()
                    page.get_by_role("button", name="Caffè Latte", exact=False).click()
                    page.get_by_role("button", name="Add one Caffè Latte", exact=True).click()
                    with page.expect_response(lambda response: response.url == ORIGIN + "/orders" and response.request.method == "POST") as created:
                        page.get_by_role("button", name="Create order", exact=True).click()
                    order = created.value.json()
                    check("saved order HTTP", 201, created.value.status)
                    check("saved order", ["open", 9000], [order["status"], order["total"]])
                    check("unpaid stock unchanged", initial_stock, get("/inventory"))
                    oid = order["id"]
                    expect(page.get_by_role("status")).to_contain_text("created")
                    shot("05-unpaid-order.png")
                    page.reload()
                    expect(page.locator(".total")).to_contain_text("9,000")
                    check("refresh preserves saved order", oid, get(f"/orders/{oid}")["id"])
                    def fail_payment(route):
                        route.continue_(post_data=json.dumps({"method": "card", "result": "failed"}))
                    page.route("**/orders/*/pay", fail_payment)
                    with page.expect_response(lambda response: response.url.endswith("/pay")) as failed:
                        page.get_by_role("button", name="Pay card", exact=True).click()
                    check("failed payment HTTP", 402, failed.value.status)
                    expect(page.get_by_role("status")).to_contain_text("failed")
                    page.unroute("**/orders/*/pay", fail_payment)
                    check("failed order remains open", "open", get(f"/orders/{oid}")["status"])
                    check("failed stock unchanged", initial_stock, get("/inventory"))
                    check("failed sales unchanged", 0, get("/dashboard/sales")["sales_total"])
                    shot("06-payment-failure.png")
                    with page.expect_response(lambda response: response.url.endswith("/pay")) as paid:
                        page.get_by_role("button", name="Pay cash", exact=True).click()
                    check("retry payment HTTP", 200, paid.value.status)
                    expect(page.locator(".receipt")).to_contain_text("9,000")
                    shot("07-paid-receipt.png")
                    after = get("/inventory")
                    stock = {item["name"]: item for item in after}
                    check("paid stock", [4500, 1164], [stock["Milk"]["stock_quantity"], stock["Coffee beans"]["stock_quantity"]])
                    check("duplicate payment HTTP", 409, context.request.post(ORIGIN + f"/orders/{oid}/pay", data={"method": "cash"}).status)
                    check("duplicate stock unchanged", after, get("/inventory"))
                    page.get_by_role("button", name="inventory", exact=True).click()
                    expect(page.get_by_role("cell", name="4500 ml", exact=True)).to_be_visible()
                    shot("08-final-inventory.png")
                    page.goto(ORIGIN + "/etalogin")
                    expect(page.locator(".stats")).to_contain_text("9,000")
                    shot("09-paid-sales.png")
                    beans = stock["Coffee beans"]
                    put(f"/owner/inventory/{beans['id']}", {"name": beans["name"], "unit": "kg", "stock_quantity": 1.164, "reorder_level": 0.25})
                    latte = next(item for item in get("/owner/menu") if item["id"] == order["items"][0]["menu_item_id"])
                    recipe = [{"ingredient_id": line["ingredient_id"], "quantity": 18 if line["ingredient_id"] == beans["id"] else 250, "unit": "g" if line["ingredient_id"] == beans["id"] else "ml"} for line in latte["recipe"]]
                    edited = put(f"/owner/menu/{latte['id']}", {"name": "Latte verification", "price": 6000, "recipe": recipe})
                    check("18 g recipe edit stores kg", 0.018, next(line["quantity"] for line in edited["recipe"] if line["ingredient_id"] == beans["id"]))
                    old = get(f"/orders/{oid}")
                    check("historical receipt name and price", ["Caffè Latte", 4500, 9000], [old["items"][0]["name"], old["items"][0]["unit_price"], old["total"]])
                    page.reload()
                    expect(page.get_by_text("Latte verification", exact=True)).to_be_visible()
                    shot("10-corrected-recipe-owner-view.png")
                    page.goto(ORIGIN)
                    page.get_by_role("button", name="Orders", exact=True).click()
                    page.get_by_role("button", name="View receipt", exact=True).click()
                    expect(page.locator(".receipt")).to_contain_text("Caffè Latte")
                    shot("11-original-receipt-after-rename.png")
                    page.get_by_role("button", name="cashier", exact=True).click()
                    expect(page.get_by_role("button", name="Latte verification", exact=False)).to_be_enabled()
                    page.get_by_role("button", name="Latte verification", exact=False).click()
                    with page.expect_response(lambda response: response.url.endswith("/pay")) as next_sale:
                        page.get_by_role("button", name="Pay cash", exact=True).click()
                    check("next sale after unit edit", 200, next_sale.value.status)
                    final_stock = {item["name"]: item["stock_quantity"] for item in get("/inventory")}
                    check("stock after next sale", [4250, 1.146], [final_stock["Milk"], final_stock["Coffee beans"]])
                    totals = get("/dashboard/sales")
                    check("two paid sales", [2, 15000], [totals["paid_orders"], totals["sales_total"]])
                    page.goto(ORIGIN + "/etalogin")
                    expect(page.locator(".stats")).to_contain_text("15,000")
                    shot("12-final-sales-after-edit.png")
                    check("logout", 200, context.request.post(ORIGIN + "/auth/logout").status)
                    check("sales protected after logout", 401, context.request.get(ORIGIN + "/dashboard/sales").status)
                    check("uncaught browser errors", [], errors)
                    context.close()
                    browser.close()
                    browser = None
                    metadata = {"date_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(), "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
                                "operator": "Codex automation at daydevil80's request", "database": database, "browser": "Chromium, 1440 x 1080", "shared_data_changed": False,
                                "method": "Real built frontend and FastAPI HTTP routes through local same-origin proxy; failure injected with result=failed. Owner credentials generated per run and not recorded.",
                                "checks": checks, "limits": ["Automated verification; no human tester or narrated presentation is attested", "No public cloud deployment or concurrent-load claim", "Payment remains simulated", "Feedback iframe delivery not tested"]}
                    (args.output / "browser-results.json").write_text(json.dumps(metadata, ensure_ascii=True, indent=2), encoding="utf-8")
                    hashes = {file.name: hashlib.sha256(file.read_bytes()).hexdigest() for file in sorted(args.output.glob("*.png"))}
                    (args.output / "screenshot-sha256.json").write_text(json.dumps(hashes, indent=2), encoding="utf-8")
                    print(f"PASS: {len(checks)} checks; {len(hashes)} screenshots; {database}")
        finally:
            if browser:
                browser.close()
            if server:
                server.shutdown()
                server.server_close()
            if process:
                process.terminate()
                process.wait(timeout=15)
            if pg_started:
                pg("pg_ctl.exe" if os.name == "nt" else "pg_ctl", "-D", temp / "pgdata", "-m", "fast", "-w", "stop")


if __name__ == "__main__":
    main()
