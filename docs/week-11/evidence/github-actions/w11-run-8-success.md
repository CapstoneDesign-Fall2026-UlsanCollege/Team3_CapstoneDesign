# Week 11 GitHub Actions Evidence — Run #8

**Date:** November 13, 2026  
**Workflow:** Week 9 MVP validation (`.github/workflows/week9-validation.yml`)  
**Trigger:** Push to `main`  
**Branch:** `main`  
**Commit:** `6db97df1cfa60b31940379d97827e4676c42ab8f` — Add frontend component tests to CI  
**Run:** [GitHub Actions run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598)  
**Overall status:** **Success**  
**Duration shown in GitHub Actions:** 46 seconds  
**Completed:** 2026-11-13 14:53:35 UTC (23:53:35 Korea Standard Time)

## 1. Job Results

| Job | Result | Verified details |
|---|---|---|
| Backend unit tests | Passed | Backend test suite step completed successfully; backend test output artifact uploaded |
| Frontend production build | Passed | Frontend component tests step completed successfully; production build step completed successfully; frontend build artifact uploaded |
| Browser and API transaction regression | Passed | Isolated browser/API regression checks completed successfully; browser/API evidence artifact uploaded |

All three jobs were completed with conclusion `success`.

## 2. Frontend CI Test Step

The frontend job included the new **Run frontend component tests** step. GitHub Actions reports that step as completed successfully before the **Build frontend** step. The production build also completed successfully.

The local Vitest run immediately before this CI push separately recorded 4/4 component tests passing. The Actions job-step record confirms the CI test command passed; the local detailed Vitest output is retained in [w11-frontend-success-and-build.md](../test-results/w11-frontend-success-and-build.md).

## 3. Uploaded Workflow Artifacts

Three artifacts were attached to run #8:

| Artifact | Artifact ID | Status |
|---|---:|---|
| `week9-frontend-build-results` | `14047714571` | Available; not expired |
| `week9-backend-test-results` | `14047669837` | Available; not expired |
| `week9-browser-api-evidence` | `14047414882` | Available; not expired |

Artifacts were listed by the GitHub Actions run API. They expire on February 11, 2027. The artifact names retain the workflow's original Week 9 naming; this record associates them with the Week 11 commit and run rather than renaming them.

## 4. Evidence Integrity and Scope

- The run metadata identifies commit `6db97df1cfa60b31940379d97827e4676c42ab8f` on `main`.
- The run completed with overall conclusion `success`; each of its three jobs also completed with conclusion `success`.
- The frontend component-test step is explicitly present and passed in the frontend production build job.
- The screenshot of the successful run was supplied in the conversation on November 13, 2026. The screenshot file itself has not been committed as a repository image; the live Actions run is the primary evidence.
- This record does not claim additional security, load, or production-payment testing beyond the checks named in the workflow.
