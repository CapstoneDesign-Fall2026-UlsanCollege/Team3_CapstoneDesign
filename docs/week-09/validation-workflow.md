# Week 9 Validation Workflow

**Team:** Team 3 — SmartServe POS  
**Branch:** `main`  
**Purpose:** Run repeatable backend tests, a frontend production build and an isolated browser/API transaction regression check.

## Workflow and run history

- [Week 9 GitHub Actions workflow](../../.github/workflows/week9-validation.yml)
- [GitHub Actions run history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/workflows/week9-validation.yml)
- [Week 9 browser/API regression script](run_validation.py)

## Automated checks

1. **Backend unit tests** — runs `test_issue3`, `test_owner_management` and `test_trash` using isolated test data.
2. **Frontend production build** — runs TypeScript compilation and the Vite production build.
3. **Browser/API transaction regression** — builds the frontend, starts the app against a fresh temporary SQLite database, and exercises cashier order creation, refresh recovery, failed payment, successful retry, duplicate payment, inventory deduction, recipe unit conversion, historical receipt preservation, sales totals and local owner-session behavior.
4. **Artifacts** — uploads backend/frontend logs and the browser/API JSON result plus screenshots, when produced.

The browser/API regression uses isolated local sample data and does not touch the shared Render/demo database. The CI run uses SQLite; do not describe it as PostgreSQL verification.

## Previous evidence — October 28, 2026

These are prior team results, not the Week 9 CI result and not an independent test by the author of this Week 9 document.

- [Verification summary](../week-08/evidence/2026-10-28/README.md)
- [24 backend test output](../week-08/evidence/2026-10-28/backend-tests.txt)
- [Frontend build output](../week-08/evidence/2026-10-28/frontend-build.txt)
- [27 browser/API expected-versus-actual checks](../week-08/evidence/2026-10-28/browser-results.json)
- [12 screenshots](../week-08/evidence/2026-10-28/SCREENSHOTS.md)

The October 28 run was performed by Codex automation at daydevil80's request against source commit `b68df10eb46d25bc2ac00e28412b71df792deb7f`.

## Evidence status

A workflow configuration is not proof of a passing run. Use the Actions run summary and downloadable artifacts after the run completes. Record the exact run, tested commit, job status and any failures.

| Evidence | Link | Status |
|---|---|---|
| Workflow configuration | [week9-validation.yml](../../.github/workflows/week9-validation.yml) | Committed |
| Browser/API test script | [run_validation.py](run_validation.py) | Committed |
| Backend unit tests | [GitHub Actions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/workflows/week9-validation.yml) | Awaiting run result |
| Frontend build | [GitHub Actions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/workflows/week9-validation.yml) | Awaiting run result |
| Browser/API regression + screenshots | [GitHub Actions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/workflows/week9-validation.yml) | Awaiting run result |

## Limits

The browser run uses a local temporary database and simulated payment. It does not verify the public Render deployment, real payment processing, production security, feedback-form delivery or concurrent load. Local owner-session checks are not a complete production security audit.
