# Week 11 Individual Contribution — Ualson Tamang (`ualsom`)

**Period:** November 12–18, 2026
**Scope:** One bounded SmartServe POS demo regression for payment and inventory integrity
**Attribution:** Prepared with AI assistance under the connected `ualsom` GitHub account; verification result must be recorded from actual execution.

## Demo step and acceptance criteria

1. Start from the isolated SQLite seeded demo database.
2. Create an order for **two Caffè Lattes** for **₩9,000**; order creation alone should not change inventory.
3. Simulate a successful cash payment. Expect paid status, milk decrease **500 ml**, coffee beans decrease **36 g**, exactly one payment and two inventory movements.
4. Reopen the SQLAlchemy session and retry payment by card. Expect **HTTP 409**, unchanged remaining stock, one payment row and two inventory movements.

## Expected versus actual

| Check | Expected | Actual as of initial submission |
|---|---|---|
| Two-latte order | ₩9,000, inventory unchanged before payment | Assertions written; not yet executed for this branch |
| First simulated payment | Paid; milk −500 ml; beans −36 g | Assertions written; not yet executed for this branch |
| Retry after reopening session | HTTP 409; no second payment or inventory deduction | Assertions written; not yet executed for this branch |

**Command:** From `smartserve-pos/backend`, run `python -B -m unittest -v test_week11_ualsom`.

**Evidence:** [Bounded regression test](../../../smartserve-pos/backend/test_week11_ualsom.py); [CI workflow change](../../../.github/workflows/week9-validation.yml).

**Execution status:** Pending. A passing test result must come from a recorded local execution or the GitHub Actions pull-request run and be linked here before claiming PASS.

**Limits:** Uses isolated SQLite and a simulated payment path, not the live Render database or a real payment provider. Previous Week 10 results are not counted as Week 11 evidence.
