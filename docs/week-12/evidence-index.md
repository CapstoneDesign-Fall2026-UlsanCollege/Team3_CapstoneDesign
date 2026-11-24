# Week 12 Evidence Index — SmartServe POS

**Period:** November 19–25, 2026 (KST)  
**Repository HEAD reviewed:** e89acd3ac1912446144cb93f1dba769ab721ea9f

This index separates evidence already available from artifacts still to capture. Link files only after they exist in the repository or are attached to the relevant issue/run.

## Evidence available now

| ID | Evidence | Supports | Revision/date | Location |
|---|---|---|---|---|
| E12-01 | Owner signup error screenshot | Frontend displays temporary signup-email-unavailable message | Nov 24, 2026; Docker local run | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| E12-02 | API request log excerpt | OPTIONS preflight 200; POST /auth/register 503 | Nov 24, 2026; Docker local run | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| E12-02a | API container environment presence check | `GMAIL_SENDER`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, and `GMAIL_REFRESH_TOKEN` all absent; `MAIL_PROVIDER` defaults to `gmail_api`; `SMARTSERVE_ENV` unset | Nov 24, 2026; `docker compose exec api` | Captured terminal output in the Week 12 investigation |
| E12-02b | Resolved Docker Compose configuration | API service receives only `DATABASE_URL`; no Gmail variables or `env_file` configured | Nov 24, 2026; `docker compose config` | Captured terminal output in the Week 12 investigation |
| E12-02a-file | API container Gmail environment check | Captured output confirms Gmail sender/OAuth variables are missing and `SMARTSERVE_ENV` is unset | Nov 24, 2026; local Docker Compose | [w12-gmail-environment-check.txt](evidence/backend/w12-gmail-environment-check.txt) |
| E12-02b-file | Resolved API Compose environment check | Captured output confirms only `DATABASE_URL` is configured; Gmail variables and `env_file` are absent | Nov 24, 2026; `docker compose config --format json` | [w12-api-compose-environment.txt](evidence/backend/w12-api-compose-environment.txt) |
| E12-02d | Repeated signup API failures | Four recorded `POST /auth/register` requests returned HTTP 503 | Nov 24, 2026; local Docker Compose logs | [w12-signup-503-log.txt](evidence/backend/w12-signup-503-log.txt) |
| E12-02c | Mailer and signup exception-path inspection | Gmail sender/OAuth settings are required by `mailer.py`; `security.py` converts delivery exceptions to HTTP 503 | Nov 24, 2026; local source inspection | `smartserve-pos/backend/app/mailer.py` and `security.py` at local reviewed revision |
| E12-01a | Original signup error screenshot (embedded below) | Browser error message from the failed registration attempt; not a post-fix result | Nov 24, 2026 | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| E12-03 | Backend unit test summary | 46 tests passed in recorded local run | Nov 23, 2026; bcd1f3a | [Weekly report](weekly-report.md) |
| E12-04 | Café browser/API runner | 27 checks passed, including checkout, stock, duplicate payment, recipe units, receipt history | Nov 23, 2026; bcd1f3a | [Weekly report](weekly-report.md) |
| E12-05 | Business browser/API runner | 37 checks passed for retail and service checkout | Nov 23, 2026; bcd1f3a | [Weekly report](weekly-report.md) |
| E12-06 | Week 11 live two-latte baseline | Prior developer-coordinated Render transaction result | eb2c88e | [Week 11 verification](../week-11/live-two-latte-verification.md) |
| E12-07 | Week 11 retry regression CI | Isolated duplicate-payment regression | PR CI run #9 | [GitHub Actions run](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43902224014) |

## Required next evidence

| ID | Artifact | Required contents | Status |
|---|---|---|---|
| E12-08 | Redacted API traceback | Controlled request timestamp, endpoint, exception type/message, relevant stack; secrets removed | Pending |
| E12-09 | Runtime provenance | Container image/build source, commit SHA, whether local uncommitted tenancy edit was mounted | Pending |
| E12-10 | Post-fix signup screenshot | Browser result after confirmed fix; no personal data or activation token | Pending |
| E12-11 | Post-fix API output | Corresponding success/actionable response and redacted logs | Pending |
| E12-12 | Independent peer test | Tester login, timestamp, exact SHA/environment, expected/actual, evidence | Pending |

## Suggested evidence layout

```
docs/week-12/
├── evidence-index.md
└── evidence/
    ├── screenshots/
    ├── backend/
    └── runtime/
```

Do not create placeholder screenshots or fabricated logs. Add each real artifact with description, date, revision, and source.


## Existing screenshot preview

![Owner registration showing the temporary signup-email-unavailable message](https://github.com/user-attachments/assets/f44b7140-73d4-4bca-bb9d-09593ac24ff7)

This is the original screenshot attached to Issue #27. The repository documentation embeds the existing issue attachment; the image has not been separately uploaded as a binary file under the evidence directory.
