# Week 11 Automated Test Matrix — SmartServe POS

**Week:** 11  
**Branch:** `main`  
**Status:** Backend suite executed successfully; frontend and CI checks remain pending.

## 1. Purpose

This matrix tracks behaviours verified during Week 11. Results below reflect actual test execution, not planned coverage.

## 2. Backend Test Matrix

| ID | Feature / area | Scenario coverage | Status |
|---|---|---|---|
| BE-01 | Payment and orders | Payment success/failure and retry, duplicate-payment protection, cancellation guards, unique order IDs, original order pricing, Korea-local sales date | Passed |
| BE-02 | Inventory and recipes | Insufficient-stock guard, recipe deduction exactly once, unit conversions, ledger consistency | Passed |
| BE-03 | Owner management | Add/edit/archive menu and ingredients, duplicate-name validation, active/open-order guards, historical receipt preservation | Passed |
| BE-04 | Trash and deletion | Auto-expiry/payment guard, open/paid order protection, trash/restore/permanent deletion | Passed |
| BE-05 | Receipt migration | Legacy schema upgrade and one-time backfill | Passed |

**Execution:** 25 tests passed, 0 failed, 0 skipped. Command: `python -B -m unittest -v test_issue3 test_owner_management test_trash`. Run date: November 13, 2026. Tested commit: `6a539122899e0d67edc15405786ccb5f42dc0d5f`. Evidence: [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt).

## 3. Frontend Test Matrix

The frontend currently has no configured test runner in the inspected `package.json`. These remain candidate tests to implement after selecting a compatible framework.

| ID | Feature / area | Scenario to verify | Expected result | Status |
|---|---|---|---|---|
| FE-01 | Application rendering | Render the selected page/component | Main content appears without runtime errors | Pending setup |
| FE-02 | Form validation | Submit a form with missing or invalid required values | Validation feedback appears and invalid submission is prevented | Pending setup |
| FE-03 | User interaction | Trigger a primary button or action | The expected UI state or action occurs | Pending setup |
| FE-04 | Loading / error states | Simulate a failed data request where practical | Error state is displayed and the UI remains usable | Pending setup |
| FE-05 | Order display | Render order data | Correct item details and totals are displayed | Pending setup |

## 4. CI Validation Matrix

| ID | Check | Evidence required | Status |
|---|---|---|---|
| CI-01 | Backend test job | Actual GitHub Actions run, commit SHA, job result, and test output | To verify |
| CI-02 | Frontend production build | Actual build job result and uploaded output, if configured | To verify |
| CI-03 | Frontend automated test job | Actual job result after frontend tests are configured and added to CI | Pending implementation |
| CI-04 | Browser/API regression job | Actual workflow result and generated artifacts, if the existing workflow runs this check | To verify |
| CI-05 | Workflow failure visibility | A controlled local test failure or safe test-branch check shows a failing result; restore changes afterward | To verify |

## 5. Test Execution Record

| Date | Tester | Tested commit SHA | Command | Result | Evidence |
|---|---|---|---|---|---|
| November 13, 2026 | Lama Muskan (Sammygit15) | `6a539122899e0d67edc15405786ccb5f42dc0d5f` | `python -B -m unittest -v test_issue3 test_owner_management test_trash` | 25 passed; 0 failed; exit code 0 | [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt) |

## 6. Result Status Definitions

- **To inspect:** Existing implementation and test coverage have not yet been checked.
- **Pending setup:** Required test tooling or test implementation is not yet in place.
- **Passed:** Test was executed and the expected result was observed.
- **Failed:** Test was executed and did not meet the expected result.
- **Not applicable:** The feature or behaviour is not implemented; record the reason.

## 7. Notes

- A production build is not a substitute for frontend unit/component tests.
- A workflow configuration is not proof of a successful workflow run.
- Backend tests were run locally; this result does not establish a successful GitHub Actions run.
- Keep Week 10 evidence separate from all Week 11 execution records.
