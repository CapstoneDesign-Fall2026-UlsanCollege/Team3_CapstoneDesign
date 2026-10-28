# Week 8 Individual Evidence Receipt — Shuzita Majhi

**GitHub login:** `Shuzita`
**Team:** Team 3 — SmartServe POS
**Week:** 8
**Date:** October 28, 2026

## Contribution: Payment Recovery Evidence Review and Test Planning

Reviewed the recorded payment-failure, successful-retry and duplicate-payment evidence, and documented the review and lessons in the shared Week 8 report.

**Contribution record:** [Week 8 Weekly Report](../weekly-report.md)

## Evidence Reviewed

- [October 28 verification summary](../evidence/2026-10-28/README.md)
- [Expected and actual browser/API results](../evidence/2026-10-28/browser-results.json)
- [Failed-payment screenshot](../evidence/2026-10-28/06-payment-failure.png)
- [Successful retry receipt](../evidence/2026-10-28/07-paid-receipt.png)
- [Inventory after successful payment](../evidence/2026-10-28/08-final-inventory.png)
- [Sales after successful payment](../evidence/2026-10-28/09-paid-sales.png)

## What the Recorded Evidence Shows

| Scenario | Expected behavior | Recorded result |
|---|---|---|
| Failed simulated payment | Order remains open; stock and sales unchanged | HTTP 402; expected behavior recorded |
| Successful cash retry | Same order becomes paid for ₩9,000 | HTTP 200; paid receipt recorded |
| Ingredient deduction | Two lattes deduct 500 ml milk and 36 g beans | Milk changed from 5,000 to 4,500 ml; beans changed from 1,200 to 1,164 g |
| Duplicate payment | No second deduction or additional sale | HTTP 409; stock and sales unchanged |

These are results from the linked automated run, not a new test executed by me.

## Course Lesson

A presentation or interface alone does not establish that a workflow is verified. Claims need direct evidence, and each student should explain their own contribution. Reviewing existing results and independently running a test are different activities.

**Source:** [Midterm Presentation Rubric](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/course-materials/blob/main/student-starter-kit/docs/midterm-presentation-rubric.md)

## Project Lesson

Payment status and inventory changes must remain consistent. Testing only a successful payment would miss important recovery and duplicate-request cases. The evidence shows why failed payment must leave stock unchanged and why retrying must not deduct ingredients twice.

**Decision:** Include failure, recovery and duplicate-payment checks in my next verification task.

## MVP Status

**Still has a gap.** The automated evidence supports the simulated transaction path. The team’s next verification milestone remains tracked in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22).

Real payment-provider integration is outside the current simulated-payment scope.

## Proposed Week 9 Action

- **Owner:** Shuzita (`Shuzita`), subject to confirming the assignment.
- **Task:** Personally follow the setup and repeat failed-payment recovery and duplicate-payment checks using separate sample data.
- **Success signal:** Failed payment changes neither stock nor sales; successful retry deducts the correct ingredients once; duplicate payment causes no additional deduction.
- **Evidence to record:** Date, tested commit, browser/device, starting values, expected and actual results, screenshots, and the first failure if one occurs.
- **Instructions:** [Verification handoff](../verification-handoff.md)

## Assistance and Evidence Boundary

The reviewed browser run was executed by Codex automation at daydevil80’s request. My contribution is the review and planning recorded in the shared report. This receipt does not claim that I independently executed that run or completed a narrated rehearsal.
