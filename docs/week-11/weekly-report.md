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
| November 13, 2026 | Configured Vitest and created four frontend component tests | Test runner discovered all four tests; initial run failed during React rendering because the component import resolved to `undefined`; investigation pending | [Initial frontend run record](evidence/test-results/w11-frontend-initial-run.md) |

## 3. Test Results

| Test area | Tests run | Passed | Failed | Skipped | Evidence |
|---|---:|---:|---:|---:|---|
| Backend | 25 | 25 | 0 | 0 | [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt) |
| Frontend initial run | 4 | 0 | 4 | 0 | [w11-frontend-initial-run.md](evidence/test-results/w11-frontend-initial-run.md) |
| GitHub Actions | Not verified yet | — | — | — | Pending |

**Backend command:** `python -B -m unittest -v test_issue3 test_owner_management test_trash`  
**Backend run date/time:** November 13, 2026, 19:47:39 (local machine time)  
**Backend runtime:** 0.539 seconds  
**Backend exit code:** 0

**Frontend command:** `npm.cmd test`  
**Frontend run date/time:** November 13, 2026, 19:57:36 (local machine time)  
**Frontend runner:** Vitest 4.1.12  
**Frontend result:** 4 tests discovered; all 4 failed before their assertions ran. React reported an invalid element type because the component being rendered was `undefined`. The component export/import mismatch has not yet been confirmed or fixed.

## 4. Issues and Limitations

- The backend test suite passed locally using the existing Python unittest tests.
- PowerShell displayed a `NativeCommandError` record while streaming Python's test progress through `Tee-Object`; the completed test output ended with `Ran 25 tests`, `OK`, and exit code 0. This shell display issue did not indicate a test failure.
- The first frontend test run exposed a component import/render setup issue. Since rendering failed before assertions, it does not prove that the four tested application behaviours are broken.
- The local test results do not prove that GitHub Actions passed.
- Frontend retesting and CI verification remain outstanding.

## 5. Next Steps

- Inspect the actual export from `OwnerManagement.tsx` and correct the test import.
- Rerun the frontend tests and fix any genuine test or application issues revealed.
- Run the frontend production build after the test changes.
- Trigger and inspect the existing GitHub Actions workflow.
- Capture workflow evidence and update the CI validation record.
- Continue recording confirmed bugs, fixes, and retest results.

## 6. Summary

The existing backend suite was executed successfully during Week 11: 25 tests passed with no failures. The first frontend test run successfully demonstrated that Vitest discovers the four test cases, but all four were blocked by a React component import/render error before assertions. Frontend behaviour is not yet verified, and GitHub Actions remains unverified.
