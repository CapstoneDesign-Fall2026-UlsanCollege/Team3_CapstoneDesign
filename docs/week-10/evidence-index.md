# Week 10 Evidence Index — SmartServe POS

**Team:** Team 3  
**Period:** November 5–11, 2026  
**Purpose:** Maintain a traceable index of evidence supporting Week 10 tasks and verification results.

## 1. Evidence Rules

- Link original evidence files; do not replace them with unsupported summaries.
- Record the date, person, environment, and application commit for test evidence.
- Keep historical Week 9 evidence clearly labeled as historical.
- A planned evidence item is not proof that a test passed.
- Redact passwords, API keys, tokens, personal data, and other secrets before committing evidence.
- Do not commit production credentials, database dumps containing personal data, or private customer information.

## 2. Evidence Status

| Status | Meaning |
|---|---|
| Planned | Evidence is expected but has not been collected |
| Collected | Original artifact exists and is ready to be indexed |
| Linked | Artifact is stored and its repository path or URL is recorded |
| Blocked | Evidence cannot be collected; reason is documented |

## 3. Document and Task Evidence

| ID | Task / Document | Evidence Expected | Evidence Link | Status |
|---|---|---|---|---|
| E10-01 | Week 10 work plan | Approved plan in repository | [Expanded work plan](work-plan-expanded.md) | Linked |
| E10-02 | Work checklist | Task/status checklist | [work-checklist.md](work-checklist.md) | Linked |
| E10-03 | MVP requirement review | Requirement checks and results | [mvp-requirement-review.md](mvp-requirement-review.md) | Linked |
| E10-04 | Bug review | Reproduction records and issue links | [bug-review.md](bug-review.md) | Linked |
| E10-05 | Verification preparation | Test cases and result records | [verification-plan.md](verification-plan.md) | Linked |
| E10-06 | Weekly report | Actual work summary with references | [weekly-report.md](weekly-report.md) | Linked |
| E10-07 | Contribution record | Individual contributions and proof | [contribution-record.md](contribution-record.md) | Linked |

## 4. Verification Evidence Register

| Evidence ID | Test ID | Description | Date | Tester | Environment / Commit | File or URL | Status |
|---|---|---|---|---|---|---|---|
| EV10-01 | TC-01 | Menu selection | Pending | Pending | Pending | Pending | Planned |
| EV10-02 | TC-02 | Quantity and total calculation | Pending | Pending | Pending | Pending | Planned |
| EV10-03 | TC-03 | Order creation and saved information | Pending | Pending | Pending | Pending | Planned |
| EV10-04 | TC-04 | Simulated payment | Pending | Pending | Pending | Pending | Planned |
| EV10-05 | TC-05 | Receipt verification | Pending | Pending | Pending | Pending | Planned |
| EV10-06 | TC-06 | Recipe-based inventory deduction | Pending | Pending | Pending | Pending | Planned |
| EV10-07 | TC-07 | Duplicate deduction prevention | Pending | Pending | Pending | Pending | Planned |
| EV10-08 | TC-08 | Recipe unit conversion | Pending | Pending | Pending | Pending | Planned |
| EV10-09 | TC-09 | Owner-facing information | Pending | Pending | Pending | Pending | Planned |

## 5. Build, Test, and CI Evidence

| ID | Check | Run Date | Commit | Result | Original Evidence | Status |
|---|---|---|---|---|---|---|
| CI10-01 | Backend unit test suites (owner management, Issue 3, trash) | 2026-11-10 | `0bcd9da` | PASS: 24/24 (12 + 9 + 3); Python 3.13 virtual environment; isolated SQLite | [Summary](evidence/test-results/w10-backend-test-summary.md); [Owner management log](evidence/test-results/w10-owner-management-tests.txt); [Issue 3 log](evidence/test-results/w10-issue3-tests.txt); [Trash log](evidence/test-results/w10-trash-tests.txt). Tester name was not recorded in the supplied logs. | Linked |
| CI10-02 | Frontend production build | Pending | Pending | Not Run | Pending |
| CI10-03 | Browser/API verification | Pending | Pending | Not Run | Pending |
| CI10-04 | CI workflow | Pending | Pending | Not Run | Pending |

The four linked CI10-01 artifacts are the original repository evidence for this run. Do not copy historical Week 9 results into these rows as Week 10 results. Add a dated row for each actual run.

## 6. Bug and Independent Review Evidence

| ID | Related Record | Required Evidence | Link | Status |
|---|---|---|---|---|
| BUG10-01 | Bug register | Reproduction steps and original artifacts | Pending | Planned |
| REV10-01 | Independent review | Reviewer identity, tested commit, result, and reviewer-captured evidence | Pending | Planned |

## 7. Suggested Folder Structure

```text
docs/week-10/
├── evidence-index.md
└── evidence/
    ├── screenshots/
    ├── logs/
    ├── test-results/
    └── independent-review/
```

## 8. Evidence Naming Convention

Use descriptive names, for example:
- `w10-tc01-menu-selection.png`
- `w10-tc02-order-total.png`
- `w10-tc04-simulated-payment.png`
- `w10-tc05-receipt.png`
- `w10-tc06-inventory-before.png`
- `w10-tc06-inventory-after.png`
- `w10-tc07-duplicate-deduction.txt`
- `w10-backend-tests.txt`
- `w10-frontend-build.txt`
- `w10-independent-review.md`

## 9. Historical Week 9 Evidence

Week 9 records mention 24 backend tests, a frontend build, 27 browser/API checks, and 12 screenshots. These remain historical Week 9 evidence. They are not proof that Week 10 checks have been executed, and their original artifacts should be linked only from the Week 9 evidence records.

## 10. Evidence Review Checklist

- [ ] Original artifact is saved in the correct folder.
- [ ] Filename identifies the task or test.
- [ ] Date and responsible person are recorded.
- [ ] Environment and tested commit are recorded.
- [ ] Result matches the actual artifact.
- [ ] Secrets and personal data are removed.
- [ ] Evidence is linked from the relevant document.
- [ ] Any failure or limitation is documented.

**Evidence principle:** Every completion claim must point to traceable evidence.