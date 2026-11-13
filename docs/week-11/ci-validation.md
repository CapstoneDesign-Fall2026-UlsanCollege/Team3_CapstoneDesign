# Week 11 CI Validation — SmartServe POS

**Week:** 11  
**Workflow under review:** `.github/workflows/week9-validation.yml`  
**Status:** Planned; verification has not yet been recorded.

## 1. Purpose

Document how the existing GitHub Actions workflow will be reviewed and how Week 11 automated tests will be validated in CI.

## 2. Planned Checks

- Review the current workflow triggers, jobs, commands, and uploaded artifacts.
- Confirm that backend tests run successfully in CI.
- Confirm that the frontend production build runs successfully.
- Check whether browser/API regression validation is configured and runs.
- After frontend tests are introduced, update the existing workflow if needed so those tests also run in CI.
- Inspect the completed run for the exact commit being evaluated.

## 3. Execution Record

| Field | Record |
|---|---|
| Workflow file | `.github/workflows/week9-validation.yml` |
| Workflow run URL | Not recorded yet |
| Branch | Not recorded yet |
| Commit SHA | Not recorded yet |
| Run date | Not recorded yet |
| Overall result | Not run / not verified |
| Backend job | Not verified |
| Frontend build job | Not verified |
| Frontend test job | Not configured / to review |
| Browser/API job | Not verified |
| Artifacts | Not reviewed yet |

## 4. Evidence to Save

Save the actual run URL, commit SHA, job results, and downloaded artifacts or logs in `evidence/github-actions/`. Screenshots may be stored in `evidence/screenshots/`.

## 5. Reporting Rules

- A workflow file existing does not prove that CI passed.
- Record failed or skipped jobs as they appear; do not describe them as successful.
- Do not use Week 9 or Week 10 workflow results as Week 11 results.
- Record any simulated services, isolated test databases, or other limitations.
