# Week 7 Work Checklist — Project Quality and Evidence Review

**Date:** Thu 2026-10-15 to Wed 2026-10-21  
**Team:** 3 — SmartServe POS

### Review project scope and architecture

- [x] Identify the target users, problem, and project purpose in the [SmartServe project README](../../../smartserve-pos/README.md).
- [x] Review the [main repository README](../../../README.md).
- [x] Review the original [Week 3 project report](../../week-03/weekly-report.md).
- [x] Review the [Week 3 architecture sketch](../../week-03/architecture-sketch.md).
- [x] Review the [candidate vertical slice](../../week-03/candidate-vertical-slice.md).
- [x] Review the [technology stack comparison](../../week-03/tech-stack-comparison.md).
- [x] Review the [Week 3 risk and blocker record](../../week-03/risk-or-blocker.md).
- [x] Keep the current implementation scope consistent with the documented React, TypeScript, Vite, FastAPI, PostgreSQL, and Docker architecture.

### Check Sprint 1 and current implementation

- [x] Review the [Sprint Quality Quick Checks](./sprint-quality-quick-checks.md).
- [x] Review the [Week 6 Definition of Done](../../week-06/definition-of-done.md).
- [x] Review the [Week 6 Test Plan](../../week-06/test-plan.md).
- [x] Review the [Week 6 Automated Check](../../week-06/automated-check.md).
- [x] Review the [Week 6 Tested-by Note](../../week-06/tested-by-note.md).
- [x] Review the [Week 6 Follow-up Problems](../../week-06/follow-up-problems.md).
- [x] Review the [Week 6 Setup Instructions](../../week-06/setup-and-demo.md).
- [x] Keep [Issue #3 — Payment and Inventory Deduction](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3) as a reference for the payment and inventory workflow.
- [x] Keep [Issue #20 — Owner Editing and Inventory Follow-up](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) as a reference for implementation follow-up.
- [x] Document the current project boundaries: simulated payments, no real payment gateway integration, and no enforced owner-only access.
- [ ] Confirm the actual browser/demo setup matches the latest source; [current automated checks](evidence/2026-10-21/README.md) cover isolated service behavior and build only.
- [ ] Confirm that another team member can independently set up and verify the project from the written instructions.

### Review technical evidence and data integrity

- [x] Link the [October 14 recorded evidence package](../../week-06/evidence/2026-10-14/).
- [x] Review the documented order creation and payment workflow.
- [x] Review the documented inventory deduction and duplicate-payment safeguards.
- [x] Review the documented sales and order verification evidence.
- [x] Keep the distinction between simulated payment behavior and real payment-provider integration clear.

## Evidence to link


### Week 6 technical documentation

- [x] [Week 6 Documentation Overview](../../week-06/README.md).
- [x] [Week 6 Definition of Done](../../week-06/definition-of-done.md).
- [x] [Week 6 Test Plan](../../week-06/test-plan.md).
- [x] [Week 6 Automated Check](../../week-06/automated-check.md).
- [x] [Week 6 Tested-by Note](../../week-06/tested-by-note.md).
- [x] [Week 6 Follow-up Problems](../../week-06/follow-up-problems.md).
- [x] [Week 6 Setup and Demo Instructions](../../week-06/setup-and-demo.md).
- [x] [Week 6 Weekly Report](../../week-06/weekly-report.md).
- [x] [Week 6 Work Checklist](../../week-06/work-checklist.md).
- [x] [October 14 Evidence Package](../../week-06/evidence/2026-10-14/).

### Individual contribution and receipt records

- [x] [Week 6 Receipt Instructions](../../week-06/receipts/README.md).
- [x] [Lama Muskan — Sammygit15](../../week-06/receipts/Sammygit15.md).
- [x] [Sherap Hyolmo — daydevil80](../../week-06/receipts/daydevil80.md).
- [x] [Ualson Tamang — ualsom](../../week-06/receipts/ualsom.md).
- [x] [Shuzita Majhi — Shuzita](../../week-06/receipts/Shuzita.md).
- [x] [Shreya — shrey776](../../week-06/receipts/shrey776.md).

### Week 7 documentation

- [x] [Week 7 Sprint Quality Quick Checks](./sprint-quality-quick-checks.md).
- [x] Update the [Week 7 Work Checklist](./work-checklist.md) after the remaining checks are completed.
- [ ] Update the shared Weekly Report with each student's own Week 7 contribution and evidence.
- [ ] Confirm each student's Week 7 evidence receipt or update their existing receipt with the new evidence.

## Stretch menu — optional after the core work

### Stronger project quality

- [ ] Ask another teammate to perform a clean setup using the written instructions.
- [ ] Review the API and database workflow against the documented integrity requirements.
- [ ] Review whether payment and inventory changes remain consistent when an order is processed more than once.
- [ ] Review the current inventory and recipe-editing behavior against the follow-up issue.
- [ ] Update the technical documentation when implementation changes.

### Stronger evidence

- [ ] Capture new screenshots or test output for changes made after October 14.
- [ ] Link new evidence directly to the issue or documentation it supports.
- [ ] Record who performed each manual check and when it was completed.
- [ ] Verify that each student's contribution entry points to evidence of their own work.

## Risks and exceptions

If a core item remains incomplete, record its reason, owner, and next action in the team's GitHub documentation or issue tracker.

| Item | Owner | Next action | Review point |
|---|---|---|---|
| Latest implementation state needs confirmation against recorded evidence | Team 3 | Recheck the current application and update evidence if behavior has changed | Before final submission |
| Independent clean setup not confirmed | Team 3; tester to be confirmed | Ask another teammate to follow the setup instructions and record the result | Before final submission |
| Week 7 individual contribution and receipt confirmation incomplete | Each of the five students | Each student updates their own contribution and links current evidence | October 21 freeze |
| Payment remains simulated | Team 3 | Keep simulated payment clearly distinguished from a real payment integration | Documentation review |
| Owner-only access is not enforced | Team 3 | Preserve this limitation in project documentation | Documentation review |
| Receipt/recipe fixes need independent browser confirmation | daydevil80 coordinates; tester unconfirmed; [#21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21) | Automated checks pass; run [retest steps](retest-and-rehearsal.md) | Before midterm demo |
| Evidence package is dated October 14 | Team 3 | Add updated technical proof for any changes made after that date | Before final submission |

## Final check

- [x] Project purpose, target user, and technical architecture are documented.
- [x] Sprint quality checks and technical evidence are linked.
- [x] Payment and inventory implementation boundaries are documented.
- [x] Existing individual Week 6 receipt records are linked.
- [ ] Current implementation has been rechecked against the recorded evidence.
- [ ] Another teammate has independently verified the setup instructions.
- [ ] All five students have updated their own Week 7 contribution and evidence records.
- [ ] Shared evidence has been reviewed for secrets and private information.
- [ ] Remaining issues have an owner and next action.

**Course reference:** [Week 7 One-Pager](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/course-materials/blob/main/week-07/one-pager.md)
