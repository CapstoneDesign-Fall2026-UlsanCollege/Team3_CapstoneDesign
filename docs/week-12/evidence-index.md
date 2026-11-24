# Week 12 Evidence Index — SmartServe POS

**Period:** November 19–25, 2026 (KST)  
**Repository HEAD reviewed:** e89acd3ac1912446144cb93f1dba769ab721ea9f

This index separates evidence already available from artifacts still to capture. Link files only after they exist in the repository or are attached to the relevant issue/run.

## Evidence available now

| ID | Evidence | Supports | Revision/date | Location |
|---|---|---|---|---|
| E12-01 | Owner signup error screenshot | Frontend displays temporary signup-email-unavailable message | Nov 24, 2026; Docker local run | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| E12-02 | API request log excerpt | OPTIONS preflight 200; POST /auth/register 503 | Nov 24, 2026; Docker local run | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
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
