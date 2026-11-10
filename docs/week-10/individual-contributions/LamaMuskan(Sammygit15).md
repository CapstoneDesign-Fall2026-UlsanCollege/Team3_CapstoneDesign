# Week 10 Individual Contribution — LamaMuskan (Sammygit15)

**Team:** Team 3 — SmartServe POS  
**Contributor name:** LamaMuskan  
**GitHub username:** `Sammygit15`  
**Reporting period:** November 5–11, 2026

## 1. Verified Contributions

| Date | Contribution | Result | Evidence |
|---|---|---|---|
| 2026-11-10 | Ran the frontend production build from `smartserve-pos/frontend` using `npm run build` after installing the project dependencies | **PASS** — TypeScript build and Vite 8.3.0 production build completed; 16 modules transformed; command exit code 0 was confirmed in the terminal | [Frontend production build log](../evidence/frontend-build/w10-frontend-production-build.txt) |
| 2026-11-10 | Captured and committed the frontend production-build output to the Week 10 evidence folder | **Completed** — evidence file committed in `d35dc492dca6743c54056f24181d2813970453a2` | [Evidence commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/d35dc492dca6743c54056f24181d2813970453a2) |
| 2026-11-10 | Coordinated the Week 10 evidence documentation and ensured the frontend build result was linked from the evidence index and weekly report | **Documented** — build evidence is linked in the [evidence index](../evidence-index.md) and [weekly report](../weekly-report.md) | [Evidence index](../evidence-index.md#5-build-test-and-ci-evidence); [Weekly report](../weekly-report.md) |

## 2. Supporting Shared Team Evidence

The following evidence is included as project context. The original backend test logs do not identify the person who ran the tests, so they are **not claimed here as an individually performed test**.

- [Backend test summary — 24/24 passed](../evidence/test-results/w10-backend-test-summary.md)
- [Owner management test log](../evidence/test-results/w10-owner-management-tests.txt)
- [Issue 3 test log](../evidence/test-results/w10-issue3-tests.txt)
- [Trash test log](../evidence/test-results/w10-trash-tests.txt)

## 3. Files and Records Related to This Contribution

- [Frontend build evidence](../evidence/frontend-build/w10-frontend-production-build.txt)
- [Week 10 evidence index](../evidence-index.md)
- [Week 10 weekly report](../weekly-report.md)
- [Week 10 contribution record](../contribution-record.md)

## 4. Limitations and Outstanding Work

The successful frontend build confirms compilation and production bundle generation only. It does not establish that browser workflows, API integration, live PostgreSQL behavior, or all MVP requirements have passed.

The following work remains unverified and should be completed with the team:
- Browser/API end-to-end workflow checks (TC-01 to TC-09)
- Receipt and payment workflow verification
- Inventory deduction and duplicate-deduction verification
- Live PostgreSQL integration verification
- Independent review by a team member who did not author the relevant changes

## 5. Individual Summary

During Week 10, LamaMuskan (`Sammygit15`) ran the frontend production build, confirmed its successful exit status, captured the terminal output, committed the build evidence, and coordinated its inclusion in the Week 10 evidence documentation. The Vite configuration compatibility warning was retained in the log and reported rather than hidden.

**Contribution rule:** This record credits only work supported by the available terminal output, commit history, and linked project documentation. Shared test results are referenced as team evidence and are not assigned to this contributor without a recorded tester identity.
