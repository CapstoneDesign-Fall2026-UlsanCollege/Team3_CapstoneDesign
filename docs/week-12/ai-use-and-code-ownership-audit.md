# Week 12 AI Use and Code Ownership Audit — SmartServe POS

**Team:** 3 — SmartServe POS  
**Period:** November 19–25, 2026

AI assistance does not replace student understanding, execution, review, or responsibility. Follow course rules and record actual use accurately.

## AI use notes

| Work item | AI used? | Assistance provided | Student-owned work / verification |
|---|---|---|---|
| Week 12 documentation planning | Yes | Compared other teams' Week 12 documentation and organized SmartServe QA, bug, peer-test, evidence, and contribution records | Repository facts and test results are tied to SmartServe's own issue/report. Student should review final documents before submission |
| Owner signup 503 investigation record | Yes — documentation and troubleshooting guidance | Helped structure reproduction steps, separate observations from hypotheses, and identify safe configuration checks | User ran Docker Compose log inspection, observed browser error, and created Issue #27. Root cause remains unconfirmed |
| Actual application test execution | No AI-generated test outcomes | AI did not execute browser/Docker test or generate the 503 response | Browser message and API status are based on user's observed run and linked evidence |
| November 23 transaction QA and November 25 Render preflight | Yes | Executed the existing automated test runners and read-only PowerShell HTTP checks, and helped document their outputs | daydevil80 coordinated QA reporting and the peer-test handoff. The local runners recorded 46 backend, 27 café, and 37 business checks on bcd1f3a. Render checkout was blocked by sign-in. |

## Codebase area map

| Area | Repository boundary / responsibility | Steward / backup | Review check | Evidence |
|---|---|---|---|---|
| Frontend / UI | React + TypeScript + Vite; owner signup, POS screens, dashboards, interactions | Team assignment to be confirmed | Browser flow, validation, error states, responsive behavior | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| Backend / API | FastAPI endpoints, authentication, registration, business logic | Team assignment to be confirmed | Endpoint tests, status codes, exception handling, API logs | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| Data / tenancy | PostgreSQL, tenant isolation, local tenancy storage | Team assignment to be confirmed | Tenant boundary tests, migration and storage-path review | [Weekly report](weekly-report.md) |
| QA / integration | Automated tests, browser/API runners, peer verification, evidence | Sammygit15 — Week 12 QA documentation and defect reporting; broader stewardship to be confirmed | Exact SHA/environment, expected vs actual, reproducible evidence, independent retest | [QA checklist](qa-checklist.md) |
| Deployment / runtime | Docker Compose, container configuration, environment variables | Team assignment to be confirmed | Container provenance, service health, safe configuration, reproducible startup | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |

## Individual slice and ownership record

| Student | Week 12 slice | Area | Demonstrable understanding | Evidence |
|---|---|---|---|---|
| Sammygit15 | Recorded owner signup email failure in local Docker environment; captured API status; opened Issue #27; prepared QA/evidence documentation with AI assistance | QA documentation and defect reporting; implementation ownership not claimed | Can explain frontend message, OPTIONS 200 / POST 503, why root cause is unknown, and next evidence required | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27); [contribution receipt](receipts/LamaMuskan(Sammygit15).md) |
| daydevil80 (Sherap Hyolmo) | Published the Week 12 QA report, documented the café, retail, and service regression results, confirmed the live Render revision, and coordinated the non-author walkthrough | QA reporting and deployment verification | Can explain the expected receipt and stock changes, why the Render health check passed, and why HTTP 401 left checkout blocked pending sign-in | [Weekly report](weekly-report.md#november-25-feedback-follow-up) · [Issue #22 preflight](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153696090) |
| Other team members | Add each person's actual Week 12 roadmap slice and behavior | Confirm with team | Each member should explain their own changes and checks | Link PR, issue, commit, or test evidence |

## Open ownership questions

- Confirm backend owner for Issue #27 and person responsible for next check.
- Confirm frontend, backend, data, and deployment stewards and backups.
- Each contributor should identify actual files/functions and explain the behavior changed.
- Do not claim ownership of code changes not authored or reviewed by the student.
