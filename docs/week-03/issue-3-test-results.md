# Issue #3 — Payment and inventory verification

Date: 2026-09-23

Prepared for Team 3 / `daydevil80`. These are local automated results; this file has not been posted to GitHub.

## Implementation

- Orders already have unique database primary keys.
- A failed simulated payment (`result: "failed"`) returns HTTP 402 without changing stock or creating a completed payment. The order stays open for retry.
- A successful simulated payment marks the order paid and commits the payment, ingredient deductions, and inventory movement records together.
- `inventory_deducted` is checked before deduction and returned in the order response. It is derived from the durable inventory movement ledger rather than a separate Boolean column that could drift out of sync.
- An already paid order or an order with existing deduction records returns HTTP 409: “This order has already been processed. Inventory was not deducted again.”
- The existing order row lock and unique constraints remain in place. Ingredient locks are acquired in ID order.
- The cashier blocks overlapping Pay clicks and retains the pending order ID in session storage. A payment retry after refresh uses that order. An already paid response retrieves the existing receipt.

## Automated backend results

Test source: [test_issue3.py](../../smartserve-pos/backend/test_issue3.py).

Executed with Python 3.12, FastAPI 0.115.8, SQLAlchemy 2.0.38, and an isolated SQLite database. No application data was changed.

| Test | Result |
|---|---|
| Failed payment leaves stock unchanged, creates no payment/movements, and allows retry | PASS |
| Insufficient milk rejects payment without stock/payment/movement changes | PASS |
| One Latte deducts 250 ml milk and 18 g beans; a duplicate in a new session returns 409 with no additional deductions | PASS |
| Existing ledger records prevent another deduction even if order status is inconsistent | PASS |
| Two created orders receive different IDs | PASS |

The Latte test also verifies two recorded ingredient movements, their quantities, timestamps, and order ID; exactly one completed payment remains after retry.

```text
Ran 5 tests in 0.089s
OK
```

To rerun with backend dependencies installed, from `smartserve-pos/backend`:

```text
python -B -m unittest -v test_issue3
```

The test module forces an isolated SQLite database and recreates only that in-memory database.

## Frontend verification

`npm ci` and `npm run build` passed (TypeScript and Vite production build). The build emitted a nonblocking Vite configuration module-format warning.

## Remaining verification before closing

- Run simultaneous payment requests against PostgreSQL. SQLite does not exercise PostgreSQL row locking.
- In the browser, rapidly click Pay and verify only one order is created and charged; refresh during a pending payment and retry to verify the same order ID and receipt are used.
- Post or commit this evidence so the instructor can open it from Issue #3. No screenshots were captured and no GitHub issue was updated or closed.

## Suggested issue update

Implemented the inventory/payment safeguards locally. Five automated backend tests pass, including the Latte deduction (250 ml milk + 18 g beans), failed-payment retry, recorded movements, and duplicate prevention across database sessions. Duplicate attempts return a safe HTTP 409 message. The frontend production build passes. PostgreSQL concurrency and browser click/refresh checks remain pending before closure.
