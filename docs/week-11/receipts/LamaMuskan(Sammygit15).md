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
| November 13, 2026 | Updated Week 11 matrix, evidence index, weekly report, and this receipt with initial frontend diagnostics and successful frontend tests/build | [Frontend test and build evidence](../evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Updated CI validation, evidence index, test matrix, weekly report, and this receipt with verified GitHub Actions run #8 | [CI run evidence](../evidence/github-actions/w11-run-8-success.md) |

## 3. Testing and CI Contributions

| Date | Task | Actual result | Evidence |
|---|---|---|---|
| November 13, 2026 | Reviewed and executed existing backend automated tests | 25 tests passed, 0 failed, 0 skipped; exit code 0; runtime 0.539 seconds | [Backend test output](../evidence/test-results/w11-backend-tests.txt) |
| November 13, 2026 | Installed/configured Vitest and wrote four OwnerManagement component tests | Initial run exposed a component import/render setup issue; diagnostic run retained | [Initial frontend run record](../evidence/test-results/w11-frontend-initial-run.md) |
| November 13, 2026 | Corrected named component import, test cleanup/isolation, accessible label selectors, and menu-card button scoping; reran frontend tests | 4/4 tests passed, 0 failed. Covered data loading, ingredient POST payload, menu/recipe POST payload, and cancelled removal without DELETE | [Frontend test and build evidence](../evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Ran frontend TypeScript and Vite production build | `npm.cmd run build` passed; latest local build transformed 16 modules and completed in 137 ms | [Frontend test and build evidence](../evidence/test-results/w11-frontend-success-and-build.md) |
| November 13, 2026 | Added frontend component tests to GitHub Actions | Added `npm test` to the frontend production build job before the build; pushed on `main` as commit `6db97df` | [Workflow run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598) |
| November 13, 2026 | Verified GitHub Actions run #8 | Overall success; all 3 jobs passed, including backend unit tests, frontend component tests + production build, and browser/API transaction regression; 3 artifacts uploaded | [Detailed CI evidence](../evidence/github-actions/w11-run-8-success.md) |

## 4. Commit Record

| Commit | Description | Link |
|---|---|---|
| `87cc833` | Add Week 11 work plan | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/87cc83336311adcf0b73962662cac87b3844d772) |
| `63e6a4c` | Add Week 11 automated testing plan | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/63e6a4cbaba9361091ca08f0a928886c38734e35) |
| `c7dbf9e` | Add Week 11 automated test matrix | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c7dbf9e655f2e47fdb699e1abd8e9cab94f4ff91) |
| `c827f21` | Add Week 11 backend test evidence | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c827f21) |
| `4019157` | Add successful frontend test and production build evidence | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/4019157ce374eced8f3dda184987972310474d4c) |
| `6db97df` | Add frontend component tests to CI | [View commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/6db97df1cfa60b31940379d97827e4676c42ab8f) |

## 5. Evidence Links

- [Week 11 evidence index](../evidence-index.md)
- [CI validation record](../ci-validation.md)
- [Automated test matrix](../test-matrix.md)
- [Backend test output — 25 passed](../evidence/test-results/w11-backend-tests.txt)
- [Initial frontend test run — 4 failed before assertions](../evidence/test-results/w11-frontend-initial-run.md)
- [Successful frontend test run — 4 passed and production build passed](../evidence/test-results/w11-frontend-success-and-build.md)
- [GitHub Actions run #8 — all 3 jobs passed](../evidence/github-actions/w11-run-8-success.md)
- [Live GitHub Actions run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598)

## 6. Integrity Note

The backend local result is from commit `6a539122899e0d67edc15405786ccb5f42dc0d5f`. The successful frontend tests and local production build were run on November 13, 2026; their exact local source SHA was not captured. The initial frontend failure is retained as diagnostic history and was followed by a successful 4/4 run. The local production build passed with a non-blocking Vite configuration-loader warning. GitHub Actions run #8 independently confirms that all three configured jobs passed on commit `6db97df1cfa60b31940379d97827e4676c42ab8f`, including the frontend component-test step, frontend production build, backend unit-test job, and browser/API regression job. Three workflow artifacts were uploaded. No claim is made for security, load, or live payment-provider testing.
