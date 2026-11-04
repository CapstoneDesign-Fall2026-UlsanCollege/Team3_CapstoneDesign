# Shared automated evidence — Ualson Tamang (`ualsom`) submission package

Actual result: 24 backend tests passed; frontend build passed; 27 browser/API checks passed; 12 screenshots captured.

Execution timestamp KST: 2026-11-04T15:00:06.185603+09:00
Actual tested source: `0e54b1f2742a58942caa68cb48685c41627dbf2d`
Operator: Codex automation at daydevil80's request.

These are copies of the SAME shared November 4 run supplied for Sujita and Shreya, already committed under evidence/logs and evidence/screenshots. This is not a new run or a personal test/review performed by Ualson. Original source/timestamp/operator metadata and screenshots remain unchanged.

## Actual artifacts

- [24 backend tests](logs/backend-tests.txt): isolated SQLite.
- [Frontend production build](logs/frontend-build.txt): passed, existing Vite configuration warning retained.
- [27 expected/actual browser results](logs/browser-results.json): fresh temporary local PostgreSQL.
- [Browser execution output](logs/browser-run.txt).
- [Screenshot gallery](SCREENSHOTS.md).
- [Screenshot hashes](logs/screenshot-sha256.json).
- [Archived verification script](logs/verification-script.py): inspect this copy; execute the original repository path docs/week-08/verify_current.py because it resolves the repo from its location.

Browser: Chromium 1440 x 1080; built frontend/FastAPI on local ports 18990/18991, temporary PostgreSQL on 18992. Generated credentials were not published. Shared store data was not changed.

## Complete browser/API observations

| Check | Expected | Actual | Result |
|---|---|---|---|
| public navigation hides owner dashboard | 0 | 0 | PASS |
| anonymous sales requires owner session | 401 | 401 | PASS |
| anonymous owner inventory requires session | 401 | 401 | PASS |
| owner login accepts isolated test identity | 200 | 200 | PASS |
| fresh sales | [0, 0] | [0, 0.0] | PASS |
| saved order HTTP | 201 | 201 | PASS |
| saved order | ["open", 9000] | ["open", 9000.0] | PASS |
| unpaid stock unchanged | [{"id": 2, "name": "Coffee beans", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 1200.0, "reorder_level": 250.0, "low_stock": false, "active": true}, {"id": 1, "name": "Milk", "unit": "ml", "convertible_units": ["ml", "l"], "stock_quantity": 5000.0, "reorder_level": 1000.0, "low_stock": false, "active": true}, {"id": 4, "name": "Sugar", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 2500.0, "reorder_level": 500.0, "low_stock": false, "active": true}, {"id": 3, "name": "Tea leaves", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 700.0, "reorder_level": 150.0, "low_stock": false, "active": true}] | [{"id": 2, "name": "Coffee beans", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 1200.0, "reorder_level": 250.0, "low_stock": false, "active": true}, {"id": 1, "name": "Milk", "unit": "ml", "convertible_units": ["ml", "l"], "stock_quantity": 5000.0, "reorder_level": 1000.0, "low_stock": false, "active": true}, {"id": 4, "name": "Sugar", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 2500.0, "reorder_level": 500.0, "low_stock": false, "active": true}, {"id": 3, "name": "Tea leaves", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 700.0, "reorder_level": 150.0, "low_stock": false, "active": true}] | PASS |
| refresh preserves saved order | 1 | 1 | PASS |
| failed payment HTTP | 402 | 402 | PASS |
| failed order remains open | "open" | "open" | PASS |
| failed stock unchanged | [{"id": 2, "name": "Coffee beans", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 1200.0, "reorder_level": 250.0, "low_stock": false, "active": true}, {"id": 1, "name": "Milk", "unit": "ml", "convertible_units": ["ml", "l"], "stock_quantity": 5000.0, "reorder_level": 1000.0, "low_stock": false, "active": true}, {"id": 4, "name": "Sugar", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 2500.0, "reorder_level": 500.0, "low_stock": false, "active": true}, {"id": 3, "name": "Tea leaves", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 700.0, "reorder_level": 150.0, "low_stock": false, "active": true}] | [{"id": 2, "name": "Coffee beans", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 1200.0, "reorder_level": 250.0, "low_stock": false, "active": true}, {"id": 1, "name": "Milk", "unit": "ml", "convertible_units": ["ml", "l"], "stock_quantity": 5000.0, "reorder_level": 1000.0, "low_stock": false, "active": true}, {"id": 4, "name": "Sugar", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 2500.0, "reorder_level": 500.0, "low_stock": false, "active": true}, {"id": 3, "name": "Tea leaves", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 700.0, "reorder_level": 150.0, "low_stock": false, "active": true}] | PASS |
| failed sales unchanged | 0 | 0.0 | PASS |
| retry payment HTTP | 200 | 200 | PASS |
| paid stock | [4500, 1164] | [4500.0, 1164.0] | PASS |
| duplicate payment HTTP | 409 | 409 | PASS |
| duplicate stock unchanged | [{"id": 2, "name": "Coffee beans", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 1164.0, "reorder_level": 250.0, "low_stock": false, "active": true}, {"id": 1, "name": "Milk", "unit": "ml", "convertible_units": ["ml", "l"], "stock_quantity": 4500.0, "reorder_level": 1000.0, "low_stock": false, "active": true}, {"id": 4, "name": "Sugar", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 2500.0, "reorder_level": 500.0, "low_stock": false, "active": true}, {"id": 3, "name": "Tea leaves", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 700.0, "reorder_level": 150.0, "low_stock": false, "active": true}] | [{"id": 2, "name": "Coffee beans", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 1164.0, "reorder_level": 250.0, "low_stock": false, "active": true}, {"id": 1, "name": "Milk", "unit": "ml", "convertible_units": ["ml", "l"], "stock_quantity": 4500.0, "reorder_level": 1000.0, "low_stock": false, "active": true}, {"id": 4, "name": "Sugar", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 2500.0, "reorder_level": 500.0, "low_stock": false, "active": true}, {"id": 3, "name": "Tea leaves", "unit": "g", "convertible_units": ["g", "kg"], "stock_quantity": 700.0, "reorder_level": 150.0, "low_stock": false, "active": true}] | PASS |
| PUT /owner/inventory/2 | 200 | 200 | PASS |
| PUT /owner/menu/1 | 200 | 200 | PASS |
| 18 g recipe edit stores kg | 0.018 | 0.018 | PASS |
| historical receipt name and price | ["Caffè Latte", 4500, 9000] | ["Caffè Latte", 4500.0, 9000.0] | PASS |
| next sale after unit edit | 200 | 200 | PASS |
| stock after next sale | [4250, 1.146] | [4250.0, 1.146] | PASS |
| two paid sales | [2, 15000] | [2, 15000.0] | PASS |
| logout | 200 | 200 | PASS |
| sales protected after logout | 401 | 401 | PASS |
| uncaught browser errors | [] | [] | PASS |

## Scope and remaining work

Payments are simulated. This does not establish live Render database behavior, real payment processing, production security or concurrency. No personal work, review or independent execution by Ualson is attested. Issue #22's actual-demo non-author reproduction and each member's personal confirmation remain open. Ualson should follow the existing verification handoff and add his own observed outcome before claiming that requirement complete.
