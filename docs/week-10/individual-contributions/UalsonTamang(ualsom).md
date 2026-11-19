# Week 10 Individual Contribution — Ualson Tamang (`ualsom`)

**Team:** Team 3 — SmartServe POS  
**Original work date:** November 11, 2026  
**Week 10 period:** November 5–11, 2026  
**Declared area:** Backend QA — simulated payment retry and inventory integrity

## Bounded contribution

Wrote a separate regression test, `test_week10_ualsom.py`, for one order of **two Caffè Lattes**. This is a backend automated verification slice, not an independent acceptance test of the deployed app.

The original work was submitted in [PR #23](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/pull/23) on `ualsom/week10-qa` and documented in the [Week 10 contribution record](../contribution-record.md). Because the test was still on the older branch, it was copied without changing its test logic into the current main-based Week 10 evidence update.

## Expected vs. recorded result

| Step | Expected | Actual / evidence |
|---|---|---|
| Create order for two lattes, simulate cash payment | Order becomes `paid`, inventory deduction flag is true | Original Week 10 test asserts both; the contributor's November 11 PR reports PASS |
| Check ingredient changes | Milk −500 ml; coffee beans −36 g | Exact stock-difference assertions in the linked test |
| Submit second simulated payment in the same DB session | HTTP 409; no more stock deduction | Test asserts HTTP 409 and unchanged remaining stock |
| Check payment and inventory records | Exactly one payment, two inventory movements | Test asserts row counts of 1 and 2 |

**Original November 11 result:** PASS — 1 test in 0.030 seconds, **as reported in PR #23 and the existing contribution record**. The original raw terminal log/screenshot for that run is not included in this receipt. A new CI run, if performed, is a later verification and is **not** represented as a November 11 student-run test.

## One check another member can repeat

1. Check out a repository revision containing `smartserve-pos/backend/test_week10_ualsom.py`.
2. Open a terminal at `smartserve-pos/backend`. Activate a Python virtual environment and install dependencies if necessary with `python -m pip install -r requirements.txt`.
3. Run:

   ```powershell
   python -B -m unittest -v test_week10_ualsom
   ```

4. Expect one test named `test_two_lattes_duplicate_payment_same_session` with `... ok`, ending `Ran 1 test` and `OK`. On failure, preserve the actual traceback instead of claiming PASS.

**Test source:** [Week 10 backend regression](../../../smartserve-pos/backend/test_week10_ualsom.py)  
**Historical original:** [PR #23](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/pull/23)  
**Test execution evidence:** [Original Week 10 QA record](../evidence/test-results/w10-ualsom-qa-record.md); [verified later CI rerun](../evidence/test-results/w10-ualsom-ci-rerun.md) — November 18 KST, Week 10 test passed in a 27/27 backend suite. **Student's new local verification:** [terminal screenshot](../evidence/screenshots/w10-ualsom-local-test-pass.png), showing `test_two_lattes_duplicate_payment_same_session ... ok`, `Ran 1 test in 0.086s`, and final `OK`. The screenshot is an unaltered-content crop (with reduced colors) from the student's supplied image; it is **not** the original November 11 log, and its local source SHA was not recorded.

## Scope and limits

Uses isolated SQLite and simulated payment methods, not a live PostgreSQL/Render database or actual payment processor. This is the author's own test, **not** a separately recorded independent teammate rerun. No Week 11 local test or screenshot has been counted as original Week 10 execution.
