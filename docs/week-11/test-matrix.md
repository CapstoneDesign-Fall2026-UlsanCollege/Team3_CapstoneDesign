# Week 11 Automated Test Matrix — SmartServe POS

**Week:** 11  
**Branch:** `main`  
**Status:** Local backend and frontend tests passed; local frontend production build passed; GitHub Actions run #8 verified successful on commit `6db97df`.

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

**Local execution:** 25 tests passed, 0 failed, 0 skipped. Command: `python -B -m unittest -v test_issue3 test_owner_management test_trash`. Run date: November 13, 2026. Tested commit: `6a539122899e0d67edc15405786ccb5f42dc0d5f`. Evidence: [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt).

## 3. Frontend Test Matrix

Vitest 4.1.12 is configured and four component tests are implemented in `src/OwnerManagement.test.tsx`.

| ID | Feature / area | Scenario verified | Local result |
|---|---|---|---|
| FE-01 | Initial data rendering | Load inventory and menu from mocked API; verify entries appear | Passed |
| FE-02 | Ingredient creation | Submit ingredient form and inspect POST payload and callback | Passed |
| FE-03 | Menu item creation | Submit menu item and recipe form; inspect numeric price and recipe payload | Passed |
| FE-04 | Removal cancellation | Cancel menu removal confirmation and verify no DELETE request | Passed |

**Successful local frontend run:** November 13, 2026, 20:05:48 local machine time. Command: `npm.cmd test`. Result: 1 test file passed; 4 passed; 0 failed. Duration: 1.14 seconds. Evidence: [w11-frontend-success-and-build.md](evidence/test-results/w11-frontend-success-and-build.md).

The initial run remains recorded separately: 4 tests were discovered but failed before assertions due to an invalid component import/render setup. After correcting the named import, test isolation, accessible label queries, and menu-card scoping, the four tests passed. See [w11-frontend-initial-run.md](evidence/test-results/w11-frontend-initial-run.md).

**CI confirmation:** The frontend component-test step also completed successfully in GitHub Actions run #8 on commit `6db97df1cfa60b31940379d97827e4676c42ab8f`.

## 4. Frontend Production Build

**Local command:** `npm.cmd run build` (`tsc -b && vite build`). Result: passed. Vite 8.3.0 transformed 16 modules in the latest local run and completed in 137 ms. Output: HTML 0.16 kB, CSS 12.48 kB, JavaScript 252.63 kB. Evidence: [w11-frontend-success-and-build.md](evidence/test-results/w11-frontend-success-and-build.md).

**Warning retained:** Vite printed a config-loader warning about ESM syntax in `vite.config.ts` being loaded as CommonJS. It did not stop the tests or build and remains a cleanup item.

## 5. CI Validation Matrix

| ID | Check | Verified evidence | Status |
|---|---|---|---|
| CI-01 | Backend test job | Actions run #8; backend unit-test job completed successfully | Passed |
| CI-02 | Frontend production build | Actions run #8; frontend build step and artifact upload completed successfully | Passed |
| CI-03 | Frontend component tests | Actions run #8; `Run frontend component tests` step completed successfully before build | Passed |
| CI-04 | Browser/API regression job | Actions run #8; isolated browser/API regression and evidence upload completed successfully | Passed |
| CI-05 | Workflow failure visibility | No controlled failing CI run was performed | Not tested |

**CI run:** [Week 9 MVP validation — run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598)  
**Branch:** `main`  
**Commit:** `6db97df1cfa60b31940379d97827e4676c42ab8f`  
**Overall result:** Success; all 3 jobs completed successfully. Detailed record: [w11-run-8-success.md](evidence/github-actions/w11-run-8-success.md).

## 6. Test Execution Record

| Date | Tester | Tested commit SHA | Command / workflow | Result | Evidence |
|---|---|---|---|---|---|
| November 13, 2026 | Lama Muskan (Sammygit15) | `6a539122899e0d67edc15405786ccb5f42dc0d5f` | `python -B -m unittest -v test_issue3 test_owner_management test_trash` | 25 passed; 0 failed; exit code 0 | [Backend output](evidence/test-results/w11-backend-tests.txt) |
| November 13, 2026 | Lama Muskan (Sammygit15) | Local frontend working tree; SHA not captured | `npm.cmd test` | 4 passed; 0 failed | [Frontend test and build evidence](evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Lama Muskan (Sammygit15) | Local frontend working tree; SHA not captured | `npm.cmd run build` | TypeScript + Vite build passed; latest run 137 ms | [Frontend test and build evidence](evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Lama Muskan (Sammygit15) | `6db97df1cfa60b31940379d97827e4676c42ab8f` | GitHub Actions run #8 | 3/3 jobs passed; frontend test step passed | [CI run evidence](evidence/github-actions/w11-run-8-success.md) |

## 7. Result Status Definitions

- **To inspect:** Existing implementation and test coverage have not yet been checked.
- **Pending setup:** Required test tooling or test implementation is not yet in place.
- **Passed:** Test was executed and the expected result was observed.
- **Failed:** Test was executed and did not meet the expected result.
- **Blocked:** Test execution could not reach its assertions because of a test setup, import, or environment error.
- **Not applicable:** The feature or behaviour is not implemented; record the reason.
- **Not tested:** No execution was performed for the check.

## 8. Notes

- A production build is not a substitute for frontend unit/component tests.
- A workflow configuration alone is not proof of a successful workflow run; run #8 has now been checked directly.
- Local test runs and CI results are recorded separately because they were executed in different environments and commits.
- Keep the initial frontend diagnostic run as part of the testing history.
- Keep Week 10 evidence separate from all Week 11 execution records.
