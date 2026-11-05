"""Browser acceptance checks against isolated SQLite; never touches the store database.

Build the frontend first. Run with backend requirements, Playwright and Chromium.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parent
ORIGIN = "http://127.0.0.1:18994"
API = "http://127.0.0.1:18995"
HIDDEN = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


class Proxy(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "frontend/dist"), **kwargs)

    def log_message(self, *args):
        pass

    def forward(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        headers = {key: self.headers[key] for key in ("Content-Type", "Cookie", "X-CSRF-Token", "Origin") if key in self.headers}
        try:
            result = urllib.request.urlopen(urllib.request.Request(API + self.path, data=body or None, method=self.command, headers=headers))
        except urllib.error.HTTPError as error:
            result = error
        with result:
            self.send_response(result.status)
            for key, value in result.getheaders():
                if key.lower() in ("content-type", "set-cookie"):
                    self.send_header(key, value)
            self.end_headers()
            try:
                self.wfile.write(result.read())
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass  # Navigating away cancels in-flight browser requests.

    def do_GET(self):
        if self.path.startswith(("/platform/", "/business", "/auth/", "/owner/", "/menu", "/inventory", "/orders", "/dashboard/", "/tables")):
            return self.forward()
        if self.path.split("?")[0] in ("/etalogin", "/setup", "/platform", "/activate", "/login"):
            self.path = "/index.html"
        super().do_GET()

    do_POST = forward
    do_PUT = forward
    do_DELETE = forward


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser")
    parser.add_argument("--postgres-bin", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, expected, actual):
        checks.append({"check": name, "expected": expected, "actual": actual, "passed": expected == actual})
        assert expected == actual, (name, expected, actual)

    with tempfile.TemporaryDirectory(prefix="smartserve-business-", ignore_cleanup_errors=True) as temp:
        password = secrets.token_urlsafe(24)
        env = dict(os.environ, DATABASE_URL="sqlite:///" + str(Path(temp) / "business.db").replace("\\", "/"),
                   SMARTSERVE_ENV="test", SMARTSERVE_BOOTSTRAP_ADMIN="false", SMARTSERVE_TEST_PASSWORD=password,
                   SMARTSERVE_AUTH_SECRET=secrets.token_urlsafe(48), SMARTSERVE_PUBLIC_ORIGIN=ORIGIN,
                   SMARTSERVE_LOCAL_DATA=str(Path(temp) / "private"), SMARTSERVE_TEST_MAIL_OUTBOX=str(Path(temp) / "outbox"), PYTHONDONTWRITEBYTECODE="1")
        def pg(command, *arguments):
            subprocess.run([str(args.postgres_bin / (command + (".exe" if os.name == "nt" else ""))), *map(str, arguments)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=HIDDEN, timeout=60)
        if args.postgres_bin:
            pg("initdb", "-D", Path(temp) / "pgdata", "-U", "business_test", "--auth=trust", "--encoding=UTF8", "--no-locale")
            pg("pg_ctl", "-D", Path(temp) / "pgdata", "-l", Path(temp) / "pg.log", "-o", "-h 127.0.0.1 -p 18996", "-w", "start")
            env["DATABASE_URL"] = "postgresql+psycopg://business_test@127.0.0.1:18996/postgres"
        server = None
        with (args.output / "api.log").open("w", encoding="utf-8") as log:
            subprocess.run([sys.executable, "-B", "security_fixture.py"], cwd=ROOT / "backend", env=env, check=True, stdout=log, stderr=log, creationflags=HIDDEN)
            process = subprocess.Popen([sys.executable, "-B", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "18995"], cwd=ROOT / "backend", env=env, stdout=log, stderr=log, creationflags=HIDDEN)
            try:
                for _ in range(100):
                    try:
                        urllib.request.urlopen(API + "/health", timeout=1)
                        break
                    except Exception:
                        time.sleep(.15)
                else:
                    raise RuntimeError("API startup failed")
                server = ThreadingHTTPServer(("127.0.0.1", 18994), Proxy)
                threading.Thread(target=server.serve_forever, daemon=True).start()
                with sync_playwright() as pw:
                    browser = pw.chromium.launch(headless=True, **({"executable_path": args.browser} if args.browser else {}))
                    context = browser.new_context(viewport={"width": 1440, "height": 1080})
                    page = context.new_page()
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.route("**/docs.google.com/**", lambda route: route.abort())
                    check("business writes require owner", 401, context.request.put(ORIGIN + "/owner/business", data={"name": "No", "business_type": "retail"}).status)
                    check("preset writes require owner", 401, context.request.post(ORIGIN + "/owner/business/presets/retail").status)
                    from security_browser_scenarios import run_security_scenarios
                    run_security_scenarios(browser, page, context, check, args.output, password, ORIGIN, Path(temp) / "outbox")
                    from business_scenarios import run_scenarios
                    run_scenarios(page, context, check, args.output, password, ORIGIN)
                    check("no uncaught browser errors", [], errors)
                    browser.close()
            finally:
                (args.output / "results.json").write_text(json.dumps({"environment": f"isolated local {'PostgreSQL' if args.postgres_bin else 'SQLite'}, built frontend, simulated payments", "checks": checks}, indent=2), encoding="utf-8")
                if server:
                    server.shutdown()
                    server.server_close()
                process.terminate()
                process.wait(timeout=15)
                if args.postgres_bin:
                    pg("pg_ctl", "-D", Path(temp) / "pgdata", "-m", "fast", "-w", "stop")
    print(f"PASS: {len(checks)} business browser/API checks")


if __name__ == "__main__":
    main()
