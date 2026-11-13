# Week 11 Weekly Report — SmartServe POS

**Period:** November 12–18, 2026  
**Main focus:** Automated testing  
**Status:** In progress; planned Week 11 CI validation completed successfully.

## 1. Objective

Improve confidence in SmartServe POS by reviewing existing automated tests, configuring frontend component testing, and validating the existing GitHub Actions workflow.

## 2. Work Completed

| Date | Activity | Result | Evidence |
|---|---|---|---|
| November 13, 2026 | Created Week 11 planning and documentation structure | Planning, test matrix, CI, bug review, evidence index, weekly report, and individual receipt documents created | [Week 11 docs](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-11) |
| November 13, 2026 | Reviewed and ran existing backend automated tests | 25 tests passed, 0 failed; exit code 0; tested commit `6a539122899e0d67edc15405786ccb5f42dc0d5f` | [Backend test output](evidence/test-results/w11-backend-tests.txt) |
| November 13, 2026 | Configured Vitest and created four frontend component tests | Initial run found a component import/render setup issue; corrected the named import, test isolation, label queries, and menu removal selector | [Initial diagnostic run](evidence/test-results/w11-frontend-initial-run.md) |
| November 13, 2026 | Reran frontend component tests | 4/4 tests passed: inventory/menu loading, ingredient POST payload, menu/recipe POST payload, and cancelled removal sends no DELETE | [Frontend test and build evidence](evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Ran frontend production build | `npm.cmd run build` passed; latest local TypeScript + Vite build completed in 137 ms | [Frontend test and build evidence](evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Added frontend component tests to the existing GitHub Actions workflow | Added `npm test` before the frontend production build; committed and pushed as `6db97df` | [Workflow run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598) |
| November 13, 2026 | Verified GitHub Actions run #8 | Overall success; backend tests, frontend component tests + production build, and browser/API regression jobs all passed; 3 artifacts uploaded | [Detailed CI evidence](evidence/github-actions/w11-run-8-success.md) |

## 3. Test Results

| Test area | Tests / checks | Passed | Failed | Skipped | Evidence |
|---|---:|---:|---:|---:|---|
| Local backend | 25 | 25 | 0 | 0 | [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt) |
| Local frontend successful run | 4 | 4 | 0 | 0 | [w11-frontend-success-and-build.md](evidence/test-results/w11-frontend-success-and-build.md) |
| Frontend initial diagnostic run | 4 | 0 | 4 | 0 | [w11-frontend-initial-run.md](evidence/test-results/w11-frontend-initial-run.md) |
| GitHub Actions jobs | 3 | 3 | 0 | 0 | [CI run evidence](evidence/github-actions/w11-run-8-success.md) |

**Backend command:** `python -B -m unittest -v test_issue3 test_owner_management test_trash`  
**Backend run date/time:** November 13, 2026, 19:47:39 (local machine time)  
**Backend runtime:** 0.539 seconds  
**Backend exit code:** 0

**Frontend test command:** `npm.cmd test`  
**Frontend successful run time:** November 13, 2026, 20:05:48 (local machine time)  
**Frontend runner:** Vitest 4.1.12  
**Frontend result:** 1 test file passed; 4 tests passed; 0 failed; duration 1.14 seconds. The later pre-push rerun also passed all 4 tests in 1.43 seconds.

**Frontend build command:** `npm.cmd run build` (`tsc -b && vite build`)  
**Latest local build result:** Passed; Vite 8.3.0 transformed 16 modules and completed in 137 ms. Generated assets: HTML 0.16 kB, CSS 12.48 kB, JavaScript 252.63 kB.

**GitHub Actions:** [Run #8 — Week 9 MVP validation](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598)  
- Commit: `6db97df1cfa60b31940379d97827e4676c42ab8f`
- Branch: `main`
- Overall conclusion: `success`
- Total duration shown in GitHub: 46 seconds
- Jobs: Backend unit tests — success; Frontend production build — success (including the frontend component-test step); Browser and API transaction regression — success.
- Artifacts: `week9-frontend-build-results`, `week9-backend-test-results`, and `week9-browser-api-evidence` (all listed as available and not expired at verification time).

## 4. Issues and Limitations

- The backend test suite passed locally using the existing Python unittest tests.
- PowerShell displayed a `NativeCommandError` record while streaming Python's test progress through `Tee-Object`; the completed test output ended with `Ran 25 tests`, `OK`, and exit code 0. This shell display issue did not indicate a test failure.
- The first frontend test run failed before assertions because the component import resolved to `undefined`. This diagnostic run is retained; after correcting the test import and test selectors, all four frontend tests passed.
- Vite printed a non-blocking config-loader warning about ESM syntax in `vite.config.ts` being loaded as CommonJS. The tests and local production build still completed successfully. The warning remains a cleanup item.
- The CI workflow retains its historical Week 9 name and artifact prefixes. The verified run is treated as Week 11 evidence because it was triggered by the Week 11 commit on November 13, 2026.
- The successful workflow confirms only the checks configured in its three jobs. Security testing, load testing, and live payment-provider validation are not claimed here.
- The exact frontend working-tree SHA for the earlier local successful test/build run was not captured; the CI run's tested commit is recorded exactly.

## 5. Next Steps

- Keep the Vite config-loader warning on the cleanup list and address it separately without masking warnings.
- If required by the project rubric, inspect/download the three Actions artifacts and preserve selected logs/screenshots in the repository.
- Continue recording confirmed bugs, fixes, and retest results for the remainder of Week 11.

## 6. Summary

Week 11 backend tests passed locally with 25/25 tests. The frontend component suite passed locally with 4/4 tests, covering initial inventory/menu loading, ingredient creation payload, menu/recipe creation payload, and cancellation of menu-item removal. The frontend TypeScript and Vite production build also passed. Most importantly, GitHub Actions run #8 was independently verified as successful on commit `6db97df1cfa60b31940379d97827e4676c42ab8f`: all three jobs passed, including the new frontend component-test step and production build, and three workflow artifacts were uploaded. A non-blocking Vite configuration warning remains.
