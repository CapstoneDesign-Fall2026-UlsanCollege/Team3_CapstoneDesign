# Week 11 Weekly Report — SmartServe POS

**Period:** November 12–18, 2026  
**Main focus:** Automated testing  
**Status:** In progress

## 1. Objective

Improve confidence in SmartServe POS by reviewing existing automated tests, configuring frontend component testing, and validating the existing GitHub Actions workflow.

## 2. Work Completed

| Date | Activity | Result | Evidence |
|---|---|---|---|
| November 13, 2026 | Created Week 11 planning and documentation structure | Planning, test matrix, CI, bug review, evidence index, weekly report, and individual receipt documents created | [Week 11 docs](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-11) |
| November 13, 2026 | Reviewed and ran existing backend automated tests | 25 tests passed, 0 failed; exit code 0; tested commit `6a539122899e0d67edc15405786ccb5f42dc0d5f` | [Backend test output](evidence/test-results/w11-backend-tests.txt) |
| November 13, 2026 | Configured Vitest and created four frontend component tests | Initial run found a component import/render setup issue; corrected the named import, test isolation, label queries, and menu removal selector | [Initial diagnostic run](evidence/test-results/w11-frontend-initial-run.md) |
| November 13, 2026 | Reran frontend component tests | 4/4 tests passed: inventory/menu loading, ingredient POST payload, menu/recipe POST payload, and cancelled removal sends no DELETE | [Frontend test and build evidence](evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Ran frontend production build | `npm.cmd run build` passed; TypeScript build and Vite production build completed in 424 ms | [Frontend test and build evidence](evidence/test-results/w11-frontend-success-and-build.md) |

## 3. Test Results

| Test area | Tests run | Passed | Failed | Skipped | Evidence |
|---|---:|---:|---:|---:|---|
| Backend | 25 | 25 | 0 | 0 | [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt) |
| Frontend successful run | 4 | 4 | 0 | 0 | [w11-frontend-success-and-build.md](evidence/test-results/w11-frontend-success-and-build.md) |
| Frontend initial diagnostic run | 4 | 0 | 4 | 0 | [w11-frontend-initial-run.md](evidence/test-results/w11-frontend-initial-run.md) |
| GitHub Actions | Not verified yet | — | — | — | Pending |

**Backend command:** `python -B -m unittest -v test_issue3 test_owner_management test_trash`  
**Backend run date/time:** November 13, 2026, 19:47:39 (local machine time)  
**Backend runtime:** 0.539 seconds  
**Backend exit code:** 0

**Frontend test command:** `npm.cmd test`  
**Frontend successful run time:** November 13, 2026, 20:05:48 (local machine time)  
**Frontend runner:** Vitest 4.1.12  
**Frontend result:** 1 test file passed; 4 tests passed; 0 failed; duration 1.14 seconds.

**Frontend build command:** `npm.cmd run build` (`tsc -b && vite build`)  
**Build result:** Passed; Vite 8.3.0 transformed 6 modules and completed in 424 ms. Generated assets: HTML 0.16 kB, CSS 12.48 kB, JavaScript 252.63 kB.

## 4. Issues and Limitations

- The backend test suite passed locally using the existing Python unittest tests.
- PowerShell displayed a `NativeCommandError` record while streaming Python's test progress through `Tee-Object`; the completed test output ended with `Ran 25 tests`, `OK`, and exit code 0. This shell display issue did not indicate a test failure.
- The first frontend test run failed before assertions because the component import resolved to `undefined`. This diagnostic run is retained; after correcting the test import and test selectors, all four frontend tests passed.
- Vite printed a non-blocking config-loader warning about ESM syntax in `vite.config.ts` being loaded as CommonJS. The tests and production build still completed successfully. The warning remains a cleanup item.
- Local test/build results do not prove that GitHub Actions passed.
- The exact frontend working-tree commit SHA was not captured at the time of the successful test and build runs.

## 5. Next Steps

- Inspect and verify the existing GitHub Actions workflow on the current branch.
- Confirm whether the workflow runs the new Vitest suite; add a dedicated frontend test step if needed.
- Capture the actual Actions run URL, commit SHA, job results, and artifacts.
- Consider cleaning up the Vite config-loader warning without changing working build behavior.
- Continue recording confirmed bugs, fixes, and retest results.

## 6. Summary

The Week 11 backend suite passed locally with 25/25 tests. The frontend component suite now passes with 4/4 tests, covering initial inventory/menu loading, ingredient creation payload, menu/recipe creation payload, and cancellation of menu-item removal. The frontend TypeScript and Vite production build also passed in 424 ms. A non-blocking Vite configuration warning remains. GitHub Actions has not yet been verified, so all successful results recorded here are local runs only.
