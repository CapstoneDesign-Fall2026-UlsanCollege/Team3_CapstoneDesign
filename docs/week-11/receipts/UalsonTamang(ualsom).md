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
| Two-latte order | ₩9,000, inventory unchanged before payment | Passed as part of PR GitHub Actions run #9; individual test output not separately attached |
| First simulated payment | Paid; milk −500 ml; beans −36 g | Passed as part of PR GitHub Actions run #9; individual test output not separately attached |
| Retry after reopening session | HTTP 409; no second payment or inventory deduction | Passed as part of PR GitHub Actions run #9; individual test output not separately attached |

**Command:** From `smartserve-pos/backend`, run `python -B -m unittest -v test_week11_ualsom`.

**Evidence:** [Bounded regression test](../../../smartserve-pos/backend/test_week11_ualsom.py); [CI workflow change](../../../.github/workflows/week9-validation.yml).

**Execution status:** **PASS in GitHub Actions pull-request run #9** (https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43902224014). On the tested branch, the backend unit-test job ran the updated suite including `test_week11_ualsom` and its test-suite step finished successfully. Frontend build and browser/API regression jobs also passed. This is CI evidence, **not** a claim of personal local execution or independent teammate reproduction. A separately attributable manual execution remains outstanding.

**Limits:** Uses isolated SQLite and a simulated payment path, not the live Render database or a real payment provider. Previous Week 10 results are not counted as Week 11 evidence.
