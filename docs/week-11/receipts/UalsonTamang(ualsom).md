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

| Check | Expected | Actual, verified by CI and local rerun |
|---|---|---|
| Two-latte order | ₩9,000, inventory unchanged before payment | PASS in CI run #9 and student's local unittest rerun (1 test, 0.047 s) |
| First simulated payment | Paid; milk −500 ml; beans −36 g | PASS in CI run #9 and student's local unittest rerun (1 test, 0.047 s) |
| Retry after reopening session | HTTP 409; no second payment or inventory deduction | PASS in CI run #9 and student's local unittest rerun (1 test, 0.047 s) |

**Command:** From `smartserve-pos/backend`, run `python -B -m unittest -v test_week11_ualsom`.

**Evidence:** [Bounded regression test](../../../smartserve-pos/backend/test_week11_ualsom.py); [student-supplied local output](../evidence/test-results/w11-ualsom-local-check.md); [CI workflow change](../../../.github/workflows/week9-validation.yml).

**Execution status:** **PASS in GitHub Actions pull-request run #9** (https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43902224014). On the tested branch, the backend unit-test job ran the updated suite including `test_week11_ualsom` and its test-suite step finished successfully. Frontend build and browser/API regression jobs also passed. The student subsequently ran the test locally using Windows PowerShell and supplied passing output: **Ran 1 test in 0.047s; OK**. [Local test evidence](../evidence/test-results/w11-ualsom-local-check.md). The initial local failure due to a mismatched copied test file was corrected by restoring the GitHub version. The screenshot remains pending; this is a student-run local test, not independent teammate reproduction.

**Student screenshot:** [Local passing test screenshot](../evidence/screenshots/w11-ualsom-local-test-pass.png). The cropped original visibly shows the test name ending in `... ok` and `Ran 1 test in 0.047s`; the final `OK` line is below the supplied screenshot boundary and is preserved in the text execution record.

**Limits:** Uses isolated SQLite and a simulated payment path, not the live Render database or a real payment provider. Previous Week 10 results are not counted as Week 11 evidence.
