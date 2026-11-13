# Week 11 Weekly Report — SmartServe POS

**Period:** November 12–18, 2026  
**Main focus:** Automated testing  
**Status:** In progress

## 1. Objective

Improve confidence in SmartServe POS by reviewing existing automated tests, checking frontend test options, and validating the existing GitHub Actions workflow.

## 2. Work Completed

| Date | Activity | Result | Evidence |
|---|---|---|---|
| November 13, 2026 | Created Week 11 planning and documentation structure | Planning, test matrix, CI, bug review, evidence index, weekly report, and individual receipt documents created | [Week 11 docs](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-11) |
| November 13, 2026 | Reviewed and ran existing backend automated tests | 25 tests passed, 0 failed; exit code 0; tested commit `6a539122899e0d67edc15405786ccb5f42dc0d5f` | [Backend test output](evidence/test-results/w11-backend-tests.txt) |

## 3. Test Results

| Test area | Tests run | Passed | Failed | Skipped | Evidence |
|---|---:|---:|---:|---:|---|
| Backend | 25 | 25 | 0 | 0 | [w11-backend-tests.txt](evidence/test-results/w11-backend-tests.txt) |
| Frontend | Not run yet | — | — | — | Pending |
| GitHub Actions | Not verified yet | — | — | — | Pending |

**Backend command:** `python -B -m unittest -v test_issue3 test_owner_management test_trash`  
**Run date/time:** November 13, 2026, 19:47:39 (local machine time)  
**Runtime:** 0.539 seconds  
**Exit code:** 0

## 4. Issues and Limitations

- The backend test suite passed locally using the existing Python unittest tests.
- PowerShell displayed a `NativeCommandError` record while streaming Python's test progress through `Tee-Object`; the completed test output ended with `Ran 25 tests`, `OK`, and exit code 0. This shell display issue did not indicate a test failure.
- The local test result does not prove that GitHub Actions passed.
- Frontend automated tests and CI verification remain outstanding.

## 5. Next Steps

- Check compatibility and configure a frontend test framework if appropriate.
- Add and run meaningful frontend tests if feasible.
- Trigger and inspect the existing GitHub Actions workflow.
- Capture workflow evidence and update the CI validation record.
- Continue recording confirmed bugs, fixes, and retest results.

## 6. Summary

The existing backend suite was executed successfully during Week 11: 25 tests passed with no failures. Frontend testing and GitHub Actions verification are still in progress, so no completion claim is made for those areas.
