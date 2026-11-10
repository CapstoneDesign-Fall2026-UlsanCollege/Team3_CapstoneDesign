# Week 10 Individual Contribution — LamaMuskan (Sammygit15)

**Team:** Team 3 — SmartServe POS  
**Contributor name:** LamaMuskan  
**GitHub username:** `Sammygit15`  
**Reporting period:** November 5–11, 2026

## 1. Verified Technical and Build Contributions

| Date | Contribution | Result | Evidence |
|---|---|---|---|
| 2026-11-10 | Ran the frontend production build from `smartserve-pos/frontend` using `npm run build` after installing the project dependencies | **PASS** — TypeScript build and Vite 8.3.0 production build completed; 16 modules transformed; command exit code 0 was confirmed in the terminal | [Frontend production build log](../evidence/frontend-build/w10-frontend-production-build.txt) |
| 2026-11-10 | Captured and committed the frontend production-build output to the Week 10 evidence folder | **Completed** — evidence file committed in `d35dc492dca6743c54056f24181d2813970453a2` | [Evidence commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/d35dc492dca6743c54056f24181d2813970453a2) |

## 2. Verified Documentation Contributions

The following documentation updates are present in GitHub commit history under the `Sammygit15` account. These commits link and clarify existing test evidence; they do not claim that the underlying tests were personally executed by this contributor.

| Document updated | Document contribution | GitHub evidence |
|---|---|---|
| [evidence-index.md](../evidence-index.md) | Added traceable links and result details for the backend test evidence | [Commit `ac7c6ad`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/ac7c6ade2cc27e74cf7a2172035a072a375e34bf) |
| [weekly-report.md](../weekly-report.md) | Aligned the weekly report with the published backend evidence and stated verification limitations | [Commit `0ec1ebe`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0ec1ebedb018ec49991e4527a304b594e776c30b) |
| [work-checklist.md](../work-checklist.md) | Recorded the backend test evidence and distinguished completed unit tests from outstanding functional checks | [Commit `073cb0c`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/073cb0c2299be3d9254ef6c28c15e8e8bb34eb94) |
| [verification-plan.md](../verification-plan.md) | Linked backend unit-test evidence while keeping end-to-end test cases separate | [Commit `0cbe7dc`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0cbe7dca7441be99bbf60e5c169affa7098d2903) |
| [mvp-requirement-review.md](../mvp-requirement-review.md) | Clarified how backend test results support the review and what remains unverified | [Commit `0f4810b`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0f4810b4a931f8be8dca45119fae3500e0b602dd) |
| [work-plan-expanded.md](../work-plan-expanded.md) | Linked completed backend test evidence and preserved outstanding verification items | [Commit `f15b5e4`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/f15b5e4fe4265ac706ec4a151ad13560e7ee2837) |
| [evidence-index.md](../evidence-index.md) and [weekly-report.md](../weekly-report.md) | Ensured the frontend production-build evidence was indexed and reported | [Frontend evidence commit `d35dc49`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/d35dc492dca6743c54056f24181d2813970453a2) |

## 3. Supporting Shared Team Test Evidence

The following artifacts are included as supporting project evidence. The original backend test logs do not identify the person who ran the tests, so they are **not claimed here as individually performed tests**.

- [Backend test summary — 24/24 passed](../evidence/test-results/w10-backend-test-summary.md)
- [Owner management test log](../evidence/test-results/w10-owner-management-tests.txt)
- [Issue 3 test log](../evidence/test-results/w10-issue3-tests.txt)
- [Trash test log](../evidence/test-results/w10-trash-tests.txt)

## 4. Files and Records Related to This Contribution

- [Frontend build evidence](../evidence/frontend-build/w10-frontend-production-build.txt)
- [Week 10 evidence index](../evidence-index.md)
- [Week 10 weekly report](../weekly-report.md)
- [Week 10 contribution record](../contribution-record.md)
- [Week 10 work checklist](../work-checklist.md)
- [Week 10 verification plan](../verification-plan.md)
- [Week 10 MVP requirement review](../mvp-requirement-review.md)
- [Week 10 expanded work plan](../work-plan-expanded.md)

## 5. Limitations and Outstanding Work

The successful frontend build confirms compilation and production bundle generation only. It does not establish that browser workflows, API integration, live PostgreSQL behavior, or all MVP requirements have passed.

The following work remains unverified and should be completed with the team:
- Browser/API end-to-end workflow checks (TC-01 to TC-09)
- Receipt and payment workflow verification
- Inventory deduction and duplicate-deduction verification
- Live PostgreSQL integration verification
- Independent review by a team member who did not author the relevant changes

## 6. Individual Summary

During Week 10, LamaMuskan (`Sammygit15`) ran the frontend production build, confirmed its successful exit status, captured and committed the build evidence, and made traceable documentation updates to the Week 10 evidence index, weekly report, work checklist, verification plan, MVP requirement review, and expanded work plan. The Vite configuration compatibility warning was retained in the log and reported rather than hidden.

**Contribution rule:** This record credits only work supported by terminal output and GitHub commit history. Shared backend test results are referenced as team evidence and are not assigned to this contributor as personally executed tests because the supplied logs do not identify the tester.
