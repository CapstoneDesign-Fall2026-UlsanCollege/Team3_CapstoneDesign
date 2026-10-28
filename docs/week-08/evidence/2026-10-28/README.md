# October 28 current verification

**Operator:** Codex automation at `daydevil80`'s request

**Application source:** `b68df10eb46d25bc2ac00e28412b71df792deb7f`

**Browser/API timestamp:** October 28, 2026, 15:13 KST

**Shared store data changed:** no

## Results

| Check set | Actual result | Direct evidence |
|---|---|---|
| Existing backend suite | 24 tests passed, using isolated SQLite | [Output](backend-tests.txt) |
| Frontend production build | TypeScript and Vite passed, with existing config warning | [Output](frontend-build.txt) |
| Fresh browser/API run | 27 checks passed on temporary PostgreSQL 18.4 | [Expected/actual JSON](browser-results.json) |
| Captured app proof | 12 screenshots | [Gallery](SCREENSHOTS.md), [SHA-256 values](screenshot-sha256.json) |

The browser run started a fresh temporary PostgreSQL cluster on loopback, then ran FastAPI and the built production frontend through a same-origin loopback proxy. It used Chromium at 1440 × 1080. Owner credentials and the session secret were generated per run and were not recorded. The script stopped its temporary services after the checks.

## Main observed values

- Two lattes: HTTP 201, open, ₩9,000, stock unchanged before payment.
- Refresh retained the saved order.
- Failed payment: HTTP 402, order remains open, unchanged stock and sales.
- Successful retry: HTTP 200, milk 4,500 ml and beans 1,164 g from the seeded 5,000 ml and 1,200 g.
- Duplicate payment: HTTP 409, stock and sales unchanged.
- Recipe editing: entering 18 g with kg inventory saved 0.018 kg.
- Original receipt after renaming: Caffè Latte, ₩4,500 each, total ₩9,000.
- Next sale: milk 4,250 ml, beans 1.146 kg, two paid orders and ₩15,000 sales.
- Owner routes: anonymous protected requests returned 401, generated owner login allowed access, and logout restored denial.
- No uncaught browser exceptions were recorded.

## Repeat the automated check

From the repository root, with Node.js, uv, Python-compatible dependencies and an installed Chromium browser:

```powershell
uv run --with-requirements smartserve-pos/backend/requirements.txt python -B -m unittest discover -s smartserve-pos/backend -v
npm --prefix smartserve-pos/frontend run build
uv run --with playwright==1.64.0 --with-requirements smartserve-pos/backend/requirements.txt python -B docs/week-08/verify_current.py --postgres-bin "C:\Program Files\PostgreSQL\18\bin" --browser "C:\Users\shera\AppData\Local\ms-playwright\chromium-1228\chrome-win64\chrome.exe" --output docs/week-08/evidence/your-new-run
```

Adjust PostgreSQL/browser paths to the tester's machine. The script uses isolated sample data. Without `--postgres-bin`, it uses temporary SQLite; do not label that alternative as a PostgreSQL run. The recorded environment used the already cached dependency environment after a new package download stalled. That dependency-download attempt is not a product test result.

## Limits

This is automated developer verification, not a teammate's independent setup/test or a narrated presentation. The run does not verify a public cloud deployment, real payment processing, feedback-form delivery, production security or concurrent load. Requests are serial. Backend unit tests alone call service functions and do not establish HTTP authorization; the separate browser/API checks exercise the local owner-session boundary.

The browser failure case intentionally changes the outgoing simulated request to `result=failed` and observes the real server/UI response. It does not simulate a real bank failure. Source code added owner login after earlier Week 7 notes, so the current result should be used for that specific boundary.
