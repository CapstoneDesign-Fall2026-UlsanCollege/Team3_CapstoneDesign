# Week 11 CI Validation — SmartServe POS

**Week:** 11  
**Workflow:** `.github/workflows/week9-validation.yml`  
**Status:** **Verified — GitHub Actions run #8 succeeded.**

## 1. Purpose

Validate the Week 11 automated test changes in the existing GitHub Actions workflow and record the actual run, commit, jobs, and uploaded artifacts.

## 2. Workflow Changes

The existing workflow was updated to run the frontend component test command in the frontend production build job:

```yaml
- name: Run frontend component tests
  working-directory: smartserve-pos/frontend
  run: npm test
```

The component-test step runs after frontend dependency installation and before the production build. It appears once in the workflow.

## 3. Verified Execution Record

| Field | Record |
|---|---|
| Workflow file | `.github/workflows/week9-validation.yml` |
| Workflow name | Week 9 MVP validation (existing workflow name) |
| Run number | #8 |
| Run URL | [Open GitHub Actions run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598) |
| Branch | `main` |
| Commit SHA | `6db97df1cfa60b31940379d97827e4676c42ab8f` |
| Commit message | Add frontend component tests to CI |
| Trigger | Push |
| Completion | November 13, 2026, 14:53:35 UTC |
| Duration shown in Actions | 46 seconds |
| Overall result | **Success** |

## 4. Job and Step Results

| Job | Result | Notes |
|---|---|---|
| Backend unit tests | Passed | Backend test suite step and output upload completed successfully |
| Frontend production build | Passed | New frontend component-test step passed; frontend production build and artifact upload passed |
| Browser and API transaction regression | Passed | Isolated browser/API regression checks and evidence upload passed |

All three jobs have GitHub Actions conclusion `success`.

The frontend job's step list explicitly confirms:
1. Install frontend dependencies — success
2. Run frontend component tests — success
3. Build frontend — success
4. Upload frontend build output — success

## 5. Workflow Artifacts

GitHub Actions lists three non-expired artifacts for run #8:

- `week9-frontend-build-results` — artifact ID `14047714571`
- `week9-backend-test-results` — artifact ID `14047669837`
- `week9-browser-api-evidence` — artifact ID `14047414882`

They are scheduled to expire February 11, 2027. Their original names are retained because they are defined by the existing workflow.

## 6. Evidence

- [Detailed Week 11 Actions run evidence](evidence/github-actions/w11-run-8-success.md)
- [GitHub Actions run #8](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43446960598)
- [Week 11 evidence index](evidence-index.md)
- [Frontend local test/build record](evidence/test-results/w11-frontend-success-and-build.md)
- [Backend local test output](evidence/test-results/w11-backend-tests.txt)

## 7. Reporting Notes and Limitations

- A successful workflow run is now verified from GitHub's run metadata and job/step records; this is no longer pending.
- The workflow's historical name and artifact prefixes still say Week 9. The run is recorded as Week 11 evidence because it was triggered by the Week 11 commit on November 13, 2026.
- The workflow confirms the configured backend, frontend test/build, and browser/API regression jobs passed. It does not establish security, load, or production payment-provider validation.
- The Vite config-loader warning was observed in local development output; it did not prevent the local build from succeeding. CI build job passed.
