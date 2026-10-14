# October 14 automated check

**Team:** 3 — SmartServe POS  
**Related issue:** [#20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20)  
**Check time:** 2026-10-14 14:42:37–14:42:40 KST  
**Method:** Scripted browser, HTTP API, and database checks  
**Human independent tester:** None; [Tested-By Note](tested-by-note.md) remains pending

## Version and environment

The checkout is [f4e8a6d](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/f4e8a6d3c185d3b9c9090d6daaf875080902cf1a). Its application source is identical to [df2f357](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/df2f357b0246fd71b76d7be8a7fa03d29dee68fe); the intervening commits change Week 6 documents.

The run used a fresh isolated PostgreSQL 18.4 sample database, FastAPI 0.115.8, SQLAlchemy 2.0.38, psycopg 3.2.5, and the frontend lockfile's installed dependencies. The frontend was built from the checked-out source and served on a loopback test proxy. The proxy changed only the browser API address from localhost:8000 to the isolated API; it did not change business logic. The browser was installed Google Chrome with Playwright automation, viewport 1440 × 1080. The shared store and the newer private prototype were not the target of this run.

[Test steps and expected results](test-plan.md) were saved before the run. Their SHA-256 is `f0f0d634caf3d527c16610cf139721ce58a146bbeef2b122c65a43e686517969` and is also in the raw results.

## Expected and actual results

We checked this by following the planned order → payment → inventory conversion → menu edit → historical receipt → new payment → alternate recipe-unit edit sequence. Expected result: consistent saved stock, prices, labels, recipes, and sales. Actual result: **12 passed checks, 3 failed checks**. Proof is linked for every row.

| Check | Expected | Actual | Result | Proof |
|---|---|---|---|---|
| Fresh sample data | Milk 5,000 ml; beans 1,200 g; sales zero | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/01-inventory-before.png) |
| Save unpaid order | Open, ₩9,000, stock unchanged | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/02-unpaid-two-latte-order.png) |
| Recover after refresh | Same order and ₩9,000 total | Same after awaiting loaded total | PASS | [Evidence](evidence/2026-10-14/screenshots/03-recovered-unpaid-order.png) |
| Failed payment | HTTP 402; open; stock/sales unchanged | Same | PASS | [Evidence](evidence/2026-10-14/results.json) |
| Successful payment | Paid; ₩9,000; milk 4,500 ml; beans 1,164 g | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/04-paid-original-receipt.png) |
| Duplicate payment | HTTP 409; one payment; no further deduction/sale | Same | PASS | [Evidence](evidence/2026-10-14/results.json) |
| Ingredient g/kg conversion | Beans 1.164 kg; threshold 0.25 kg; recipe 0.018 kg | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/06-saved-ingredient-in-kilograms.png) |
| Save menu name/price edit | Name Caffè Latte test; price ₩6,000; stock unchanged | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/07-menu-renamed-and-repriced.png) |
| Original price and total | Earlier total ₩9,000 and unit price ₩4,500 | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/08-historical-receipt-after-menu-edit.png) |
| Original product name | Earlier name remains Caffè Latte | Earlier receipt name becomes Caffè Latte test | FAIL | [Evidence](evidence/2026-10-14/screenshots/08-historical-receipt-after-menu-edit.png) |
| New sale after conversion | ₩6,000; beans 1.146 kg; milk 4,250 ml | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/09-new-price-card-receipt.png) |
| KST daily sales | Two paid orders; ₩15,000 | Same | PASS | [Evidence](evidence/2026-10-14/screenshots/11-daily-sales.png) |
| Alternate recipe unit on edit | 18 g stores as 0.018 kg; stock unchanged | Stores as 18 kg; stock unchanged | FAIL | [Evidence](evidence/2026-10-14/screenshots/13-recipe-saved-wrong-unit.png) |
| Availability after recipe edit | Americano selectable with 1.146 kg stock | Disabled; needs 18 kg | FAIL | [Evidence](evidence/2026-10-14/screenshots/14-incorrect-americano-shortage.png) |
| Uncaught browser errors | No uncaught exceptions | None | PASS | [Evidence](evidence/2026-10-14/results.json) |

## Database confirmation

The PostgreSQL read-back found one Payment record and two ingredient movements for each of the two paid orders. After converting beans to kg, order #1's bean movement is −0.036 kg and order #2's is −0.018 kg; milk movements are −500 ml and −250 ml. See [database-check.json](evidence/2026-10-14/database-check.json). This confirms the serial duplicate check did not add a second payment or another deduction.

## Existing tests and build

- [Backend output](evidence/2026-10-14/backend-tests.txt): 20 tests passed, using isolated in-memory SQLite.
- [Frontend output](evidence/2026-10-14/frontend-build.txt): TypeScript and Vite production build passed.
- No uncaught browser exceptions occurred in the recorded run.

These results do not establish independent teammate testing, real payment processing, production security, public deployment, PostgreSQL concurrency under load, or every browser/device. The serial duplicate check is not a new concurrent-payment test. A build/test pass does not override the three failed browser checks.

## First run and repeat

The [initial scripted run](evidence/2026-10-14/initial-run/results.json) checked refresh recovery before the order details finished loading, producing a timing false negative. Its original screenshots are retained. The script was changed to await the visible saved total, and the whole sequence repeated on a new empty sample database. No application code changed. Recovery then passed; the historical-name and recipe-edit problems remained.

## Problems and next action

See [follow-up-problems.md](follow-up-problems.md): F1 is a historical product-name problem; F2 is an alternate recipe-unit edit problem and its incorrect availability result. These criteria remain incomplete in [definition-of-done.md](definition-of-done.md). Next: choose a linked fix, repeat the same checks, and have a non-author teammate run the written steps without coaching.
