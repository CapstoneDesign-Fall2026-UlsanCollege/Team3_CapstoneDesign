# Week 11 Automated Test Matrix — SmartServe POS

**Week:** 11  
**Branch:** `main`  
**Status:** Backend suite passed locally; initial frontend test run was blocked by a component import/render error; CI checks remain pending.

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

Vitest 4.1.12 was installed and configured. Four component tests were added in `src/OwnerManagement.test.tsx`. The initial run discovered all four tests but all four failed during React rendering with an invalid element type (the imported component was `undefined`). The failure occurred before the test assertions could verify application behaviour. The component export/import mismatch is under investigation.

| ID | Feature / area | Scenario to verify | Expected result | Status |
|---|---|---|---|---|
| FE-01 | Initial data rendering | Load inventory and menu from mocked API | Inventory and menu entries appear | Blocked — component render error |
| FE-02 | Ingredient creation | Submit ingredient form and inspect POST payload | Correct inventory payload is sent and callback runs | Blocked — component render error |
| FE-03 | Menu item creation | Submit menu item and recipe form | Correct menu/recipe payload is sent and callback runs | Blocked — component render error |
| FE-04 | Removal cancellation | Cancel menu removal confirmation | No DELETE request is sent | Blocked — component render error |

**Initial frontend run:** November 13, 2026, 19:57:36 local machine time. Command: `npm.cmd test`. Result: 1 test file, 4 tests discovered, 0 passed, 4 failed. Error: `Element type is invalid ... got: undefined`. This is a test setup/import failure and does not establish that the four application features are defective. See [w11-frontend-initial-run.md](evidence/test-results/w11-frontend-initial-run.md).

## 4. CI Validation Matrix

| ID | Check | Evidence required | Status |
|---|---|---|---|
| CI-01 | Backend test job | Actual GitHub Actions run, commit SHA, job result, and test output | To verify |
| CI-02 | Frontend production build | Actual build job result and uploaded output, if configured | To verify |
| CI-03 | Frontend automated test job | Actual job result after frontend tests are fixed and added to CI | Pending implementation |
| CI-04 | Browser/API regression job | Actual workflow result and generated artifacts, if the existing workflow runs this check | To verify |
| CI-05 | Workflow failure visibility | A controlled local test failure or safe test-branch check shows a failing result; restore changes afterward | To verify |

## 5. Test Execution Record

| Date | Tester | Tested commit SHA | Command | Result | Evidence |
|---|---|---|---|---|---|
| November 13, 2026 | Lama Muskan (Sammygit15) | `6a539122899e0d67edc15405786ccb5f42dc0d5f` | `python -B -m unittest -v test_issue3 test_owner_management test_trash` | 25 passed; 0 failed; exit code 0 | [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt) |
| November 13, 2026 | Lama Muskan (Sammygit15) | Local frontend working tree; commit SHA not captured for this run | `npm.cmd test` | 4 discovered; 0 passed; 4 failed before assertions due to component import/render error | [w11-frontend-initial-run.md](evidence/test-results/w11-frontend-initial-run.md) |

## 6. Result Status Definitions

- **To inspect:** Existing implementation and test coverage have not yet been checked.
- **Pending setup:** Required test tooling or test implementation is not yet in place.
- **Passed:** Test was executed and the expected result was observed.
- **Failed:** Test was executed and did not meet the expected result.
- **Blocked:** Test execution could not reach its assertions because of a test setup, import, or environment error.
- **Not applicable:** The feature or behaviour is not implemented; record the reason.

## 7. Notes

- A production build is not a substitute for frontend unit/component tests.
- A workflow configuration is not proof of a successful workflow run.
- Backend tests were run locally; this result does not establish a successful GitHub Actions run.
- The first frontend run is retained as diagnostic evidence; rerun after fixing the component import/export issue.
- Keep Week 10 evidence separate from all Week 11 execution records.
