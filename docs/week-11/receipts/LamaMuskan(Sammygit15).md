# Individual Contribution Receipt — LamaMuskan (Sammygit15)

**Project:** SmartServe POS  
**Week:** 11  
**Period:** November 12–18, 2026  
**Main focus:** Automated testing

## 1. Contribution Summary

This receipt tracks individual Week 11 work and its supporting evidence. Planned work is distinguished from completed and verified work.

## 2. Documentation Contributions

| Date | Contribution | Evidence |
|---|---|---|
| November 13, 2026 | Created Week 11 work plan | [plan.md](../plan.md) |
| November 13, 2026 | Created automated testing plan | [automated-testing-plan.md](../automated-testing-plan.md) |
| November 13, 2026 | Created automated test matrix | [test-matrix.md](../test-matrix.md) |
| November 13, 2026 | Created CI validation, bug review, evidence index, and weekly report documents | [Week 11 docs folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-11) |
| November 13, 2026 | Updated Week 11 matrix, evidence index, weekly report, and this receipt with the initial frontend test result | [Initial frontend run record](../evidence/test-results/w11-frontend-initial-run.md) |

## 3. Testing Contributions

| Date | Task | Actual result | Evidence |
|---|---|---|---|
| November 13, 2026 | Reviewed and executed existing backend automated tests | 25 tests passed, 0 failed, 0 skipped; exit code 0; runtime 0.539 seconds | [Backend test output](../evidence/test-results/w11-backend-tests.txt) |
| November 13, 2026 | Installed/configured Vitest and wrote four OwnerManagement component tests | Vitest discovered 4 tests; initial run had 4 failures during component rendering before assertions because the imported component was undefined | [Initial frontend run record](../evidence/test-results/w11-frontend-initial-run.md) |
| Pending | Frontend retest after correcting the component import | Not yet completed | Pending |
| Pending | GitHub Actions verification | Not yet completed | Pending |
| Pending | Bug investigation and retesting | Not yet completed | Pending |

## 4. Commit Record

| Commit | Description | Link |
|---|---|---|
| `87cc833` | Add Week 11 work plan | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/87cc83336311adcf0b73962662cac87b3844d772) |
| `63e6a4c` | Add Week 11 automated testing plan | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/63e6a4cbaba9361091ca08f0a928886c38734e35) |
| `c7dbf9e` | Add Week 11 automated test matrix | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c7dbf9e655f2e47fdb699e1abd8e9cab94f4ff91) |
| `c827f21` | Add Week 11 backend test evidence | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c827f21) |

## 5. Evidence Links

- [Week 11 evidence index](../evidence-index.md)
- [Backend test output — 25 passed](../evidence/test-results/w11-backend-tests.txt)
- [Initial frontend test run — 4 failed before assertions](../evidence/test-results/w11-frontend-initial-run.md)

## 6. Integrity Note

The backend result above is a local test run against commit `6a539122899e0d67edc15405786ccb5f42dc0d5f`. The initial frontend result is a separate local run on November 13, 2026; the tested frontend commit SHA was not captured. The frontend failures occurred before assertions because of a component import/render issue, so they are diagnostic evidence rather than proof that the tested application features are defective. Neither result is a claim that GitHub Actions passed. Frontend retesting and CI verification remain pending.
