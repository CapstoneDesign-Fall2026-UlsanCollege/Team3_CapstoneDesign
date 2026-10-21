# October 21 checks

Follow-up to Week 6's receipt-name and recipe-unit failures. Base checkout: `4ae272b`; this evidence is committed with the fixes. All data was isolated in-memory SQLite. No shared store data was changed.

| Check | Expected | Actual | Evidence |
|---|---|---|---|
| Backend suite | All tests pass, including four new regressions | 24 passed | [Output](backend-tests.txt) |
| Frontend build | TypeScript and Vite complete | Passed; existing Vite config warning | [Output](frontend-build.txt) |
| Two lattes | Total ₩9,000; milk −500 ml; beans −36 g | Same | [Raw result](demo-results.json) |
| Failed / duplicate payment | 402 / 409; no extra deduction | Same | [Raw result](demo-results.json) |
| Edit using 18 g after g → kg conversion | Recipe 0.018 kg; next payment deducts 0.018 kg | Same | [Raw result](demo-results.json) |
| Rename/reprice after payment | Earlier receipt keeps original name, ₩4,500 unit price and ₩9,000 total | Same | [Raw result](demo-results.json) |
| Next sale and dashboard | Milk 4,250 ml; beans 1.146 kg; two paid orders, ₩15,000 | Same | [Raw result](demo-results.json) |
| Legacy schema upgrade | Add snapshot field; preserve first backfilled label on later starts | Passed | Backend migration regression |

From the repository root:

```powershell
uv run --with-requirements smartserve-pos/backend/requirements.txt python -B -m unittest discover -s smartserve-pos/backend -v
uv run --with-requirements smartserve-pos/backend/requirements.txt python -B docs/week-07-docs/Week7/verify_demo.py
npm --prefix smartserve-pos/frontend run build
```

The demo script calls service functions directly. No HTTP/browser run, PostgreSQL concurrency check, independent human test, or spoken rehearsal is claimed here. Existing pre-migration receipt names cannot be reconstructed; the migration preserves their current names. The new snapshot protects orders created after the change.
