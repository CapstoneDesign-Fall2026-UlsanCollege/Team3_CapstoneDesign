# Week 9 Validation Workflow

**Team:** Team 3 — SmartServe POS  
**Branch:** `main`  
**Purpose:** Run repeatable backend unit tests and a frontend production build through GitHub Actions.

## Workflow

The GitHub Actions workflow configuration must live in the repository-level `.github/workflows/` directory for GitHub to recognize it. The Week 9 documentation and evidence index live in this folder.

- [Week 9 validation workflow file](../../.github/workflows/week9-validation.yml)
- [GitHub Actions runs](../../actions/workflows/week9-validation.yml)

## Checks configured

1. **Backend unit tests** — runs `python -m unittest -v test_issue3 test_owner_management test_trash` from `smartserve-pos/backend`.
2. **Frontend production build** — runs `npm install` and `npm run build` from `smartserve-pos/frontend`.
3. **Artifacts** — uploads backend test output and frontend build output when those files are produced.

## Evidence status

The workflow configuration has been committed to `main`. A passing test result must only be recorded after a GitHub Actions run completes successfully. Open the Actions link above and use the run summary and downloadable artifacts as the evidence.

| Evidence | Link | Status |
|---|---|---|
| Workflow configuration | [week9-validation.yml](../../.github/workflows/week9-validation.yml) | Committed |
| Backend unit-test run | [GitHub Actions](../../actions/workflows/week9-validation.yml) | Awaiting run result |
| Frontend build run | [GitHub Actions](../../actions/workflows/week9-validation.yml) | Awaiting run result |

## Scope and attribution

This workflow automates the listed backend and frontend checks. It does not perform a complete browser-based end-to-end test, verify the public Render deployment, test real payment processing, or establish production security. Do not describe those areas as tested based on this workflow alone.
