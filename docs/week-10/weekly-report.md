# Week 10 Weekly Report — SmartServe POS

**Team:** Team 3  
**Period:** November 5–11, 2026  
**Main Focus:** MVP Gap Review and Verification Preparation  
**Report Status:** Working draft — update as work and evidence are collected.

## 1. Weekly Objective

Review the existing MVP scope, identify and document gaps, prepare repeatable end-to-end verification, and organize evidence for Week 11 verification and feature-freeze decisions.

## 2. Work Record

This report is a living record. Documentation preparation and backend unit-test success do not mean that all end-to-end MVP requirements have passed.

| Work Item | Current Status | Evidence / Reference |
|---|---|---|
| Week 10 plan and task tracking | Documentation prepared | [Expanded work plan](work-plan-expanded.md), [Checklist](work-checklist.md) |
| MVP requirement review | Review document prepared; functional execution remains pending | [Requirement review](mvp-requirement-review.md) |
| Bug and gap investigation | Register prepared; investigation pending | [Bug review](bug-review.md) |
| Verification procedure | Test plan prepared; end-to-end test execution remains pending | [Verification plan](verification-plan.md) |
| Backend automated unit tests | **Passed: 24/24 tests** across owner management (12), Issue 3 (9), and trash (3), run November 10, 2026 | [Backend test summary](evidence/test-results/w10-backend-test-summary.md); [Evidence index](evidence-index.md) |
| Evidence organization | Backend test artifacts and frontend production-build log published and linked; functional and independent-review evidence remains outstanding | [Evidence index](evidence-index.md) |
| Frontend production build | **Passed** on November 10, 2026 (`tsc -b` + Vite 8.3.0; exit code 0; 16 modules transformed). Vite config compatibility warning retained in log; exact source SHA not captured. | [Frontend build log](evidence/frontend-build/w10-frontend-production-build.txt); [Evidence index](evidence-index.md#5-build-test-and-ci-evidence) |
| Independent verification | Not yet recorded | Pending reviewer evidence |

## 3. Backend Automated Test Summary

On November 10, 2026, three backend unittest modules were executed using the project's Python 3.13 virtual environment. All 24 tests passed:

| Test suite | Result |
|---|---:|
| Owner management | 12/12 passed |
| Issue 3 | 9/9 passed |
| Trash | 3/3 passed |
| **Total** | **24/24 passed; 0 failures** |

**Tested application commit:** `0bcd9da`  
**Database context:** Isolated in-memory SQLite test database configured by the test modules.  
**Evidence published:** [Consolidated summary](evidence/test-results/w10-backend-test-summary.md), [owner management log](evidence/test-results/w10-owner-management-tests.txt), [Issue 3 log](evidence/test-results/w10-issue3-tests.txt), and [trash log](evidence/test-results/w10-trash-tests.txt).

These results establish the outcome of the listed automated backend unit tests only. They do not establish live PostgreSQL behavior, production deployment readiness, frontend build success, browser/API end-to-end behavior, or independent user acceptance. All four raw/summary backend evidence artifacts are committed and linked in the repository.

## 3A. Frontend Production Build

On November 10, 2026, the frontend production build command `npm run build` completed successfully. The script ran `tsc -b && vite build`; TypeScript compilation completed, Vite 8.3.0 transformed 16 modules, and the production bundle was generated. The command was rerun with output redirected to the evidence file and returned exit code `0`.

**Result:** PASS. **Evidence:** [Original frontend build log](evidence/frontend-build/w10-frontend-production-build.txt). The log records a Vite configuration compatibility warning concerning ESM syntax in `vite.config.ts` being loaded as CommonJS. This warning did not stop the build. The exact source commit SHA was not captured at execution time; the evidence file was committed in `d35dc49`.

A successful production build verifies compilation and bundle generation only. It does not verify browser workflows, API integration, deployment, or the functional requirements below.

## 4. Functional Verification Summary

| Area | Result | Evidence |
|---|---|---|
| Menu and item selection | Not Run | Pending |
| Quantity and order total | Not Run | Pending |
| Order creation and saved prices | Not Run | Pending |
| Simulated payment | Not Run | Pending |
| Receipt information | Not Run | Pending |
| Recipe-based inventory deduction | Not Run | Pending |
| Duplicate deduction prevention | Not Run | Pending |
| Recipe unit conversion | Not Run | Pending |
| Owner-facing information | Not Run | Pending |

Update each result only after the corresponding end-to-end test is executed. Use Passed, Failed, or Blocked and link the original evidence. Backend unit-test results above must not be used as substitutes for these functional checks.

## 5. Bugs and Gaps

No new Week 10 bugs are confirmed in this report.

| Item | Status | Reference |
|---|---|---|
| New defects | Pending investigation | [Bug review](bug-review.md) |
| Previously documented project limitations | Retain as context; verify impact where relevant | [Bug review](bug-review.md) |
| Week 11 follow-up items | Pending review results | Pending |

## 6. Historical Context

Week 9 documentation recorded automated checks: 24 backend tests, frontend build, 27 browser/API checks, and 12 screenshots. These are historical Week 9 results and must not be counted as Week 10 execution.

The Week 9 records also noted that simulated payments are not real payment processing, isolated database checks do not prove live database correctness, and independent non-author verification was still required.

## 7. Risks and Blockers

| Risk / Blocker | Impact | Action | Status |
|---|---|---|---|
| Backend unit tests used isolated SQLite | Does not verify live PostgreSQL integration | Run and capture a separate database integration check | Open |
| Week 10 end-to-end evidence not yet collected | MVP functional requirements cannot be marked verified | Capture original artifacts during each test | Open |
| Vite configuration compatibility warning | Build passed, but Vite reports ESM syntax in `vite.config.ts` loaded as CommonJS under the current config loader | Review the Vite config/module setup in a separate maintenance task; do not suppress the warning as a substitute for fixing it | Recorded; follow-up may be needed |
| Independent reviewer not yet recorded | Independent verification remains outstanding | Arrange reviewer and document any blocker | Open |
| Historical evidence may be mistaken for new results | Incorrect progress reporting | Keep Week 9 and Week 10 evidence separate | Controlled by documentation |

## 8. Evidence Links

- [Week 10 Expanded Work Plan](work-plan-expanded.md)
- [Work Checklist](work-checklist.md)
- [MVP Requirement Review](mvp-requirement-review.md)
- [Bug Review](bug-review.md)
- [Verification Plan](verification-plan.md)
- [Evidence Index](evidence-index.md)
- [Contribution Record](contribution-record.md)
- [Backend Test Summary](evidence/test-results/w10-backend-test-summary.md)

## 9. Week 11 Handoff

The following work is expected to continue in Week 11:
1. Execute the documented end-to-end verification cases.
2. Keep the [published backend test logs and summary](evidence-index.md#5-build-test-and-ci-evidence) linked from the evidence index.
3. Attach dated screenshots, logs, API responses, and test outputs for functional checks.
4. Review the recorded Vite configuration warning and decide whether a configuration cleanup is needed.
5. Investigate and prioritize confirmed defects.
6. Arrange and record independent non-author verification.
7. Retest fixes and document remaining blockers.
8. Support feature-freeze decisions with evidence.

## 10. Final Weekly Summary

Complete this section at the end of the week using actual results:

**Completed work:** Week 10 documentation prepared; three backend unit-test suites passed (24/24) and the frontend production build passed on November 10, 2026.  
**Failed checks:** No failures in the three recorded backend unit-test suites or frontend build. The frontend build emitted a Vite configuration compatibility warning, documented in its log.  
**Blocked work:** Live PostgreSQL, end-to-end functional checks, and independent review remain unverified.  
**Evidence collected:** Three backend unittest output logs, one consolidated summary, and the frontend production-build log published under `docs/week-10/evidence/`; see the [evidence index](evidence-index.md#5-build-test-and-ci-evidence).  
**Outstanding issues:** Complete remaining verification and complete remaining functional and independent-review evidence.  
**Next actions:** Execute end-to-end checks, verify database integration, review the Vite configuration warning, and arrange independent review.

**Reporting rule:** Report only work actually performed, and link evidence for every completion claim.

## 11. Code Ownership and Independent Verification

See the [shared code ownership audit](code-ownership-audit.md) for each member's slice and repeatable check. @daydevil80's scope is simulated payment and recipe-based inventory deduction. The [backend regression log](evidence/test-results/daydevil80-issue3.txt) covers isolated SQLite. The [Issue #22 Render result form](issue-22-render-check.md) is awaiting a non-author tester's observations.

## 12. Two-Latte Backend Regression

On November 11, the Week 10 payment and inventory slice added a [two-latte regression](../../smartserve-pos/backend/test_issue3.py). The run passed **25/25 tests** across Issue 3, owner management and trash. The [execution log](evidence/test-results/daydevil80-two-latte.txt) records the exact tested commit and isolated SQLite environment.

| Step | Expected and verified by the automated test |
|---|---|
| Create and reload | Two lattes at ₩4,500 each; open order total ₩9,000; milk 5,000 ml and beans 1,200 g |
| Simulate failed card payment | HTTP 402; same order remains open; stock unchanged; zero payments and inventory movements |
| Retry with cash | Same order paid for ₩9,000; milk 4,500 ml and beans 1,164 g; two inventory movements tied to the order |
| Submit payment again | HTTP 409; stock stays at 4,500 ml and 1,164 g; one payment and two movements remain |

The [independent Render check](issue-22-render-check.md) is pending a named non-author tester's result.
