# Weekly Report — Week 3

**Team:** Team 3

**Project:** SmartServe POS

**Date:** 2026-09-22

## This week's goal

Define a small midterm demo path, describe its main screens, and connect the Week 2 design to a buildable SmartServe POS prototype.

## What we committed to do

- [x] Confirm the React, TypeScript, FastAPI, PostgreSQL, and Docker Compose direction and document local startup.
- [x] Define the candidate order-to-payment-to-inventory vertical slice and the first three proposed build issues.
- [x] Describe the cashier, inventory, and owner interactions.
- [x] Add a prototype covering order creation, simulated payment, receipt, inventory, and daily sales views.
- [ ] Record a run of the two-latte demo, including stock before and after payment and a repeat-payment check.
- [ ] Confirm issue links and individual contributions with the team.

## Evidence links

| Evidence | Link |
|---|---|
| Issue(s) | [Inventory-deduction investigation #2](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/2) and [implementation issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3); links for the other proposed build issues are pending. |
| PR(s) / commits | [MVP implementation commit `c78af82`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c78af82); branch: `smartserve-mvp`. Add a PR link if one is opened. |
| Screenshot / demo | [Cashier wireframe](wireframe-Landing-page.jpg), [inventory wireframe](wireframe-Inventory.jpg), and [owner dashboard wireframe](wireframe-Owner-dashboard.jpg); Week 3 run or screenshots pending. |
| Test/check note | [Issue #3 test results](issues/issue-03/README.md): five local backend tests passed, including one-Latte deduction, duplicate prevention, failed payment, and insufficient stock; frontend build passed. The full two-latte browser demo and PostgreSQL concurrency check remain pending. |
| Sprint 0 and checklists | [Sprint 0 Report](sprint-0-report.md), [Quality Quick Checks](sprint-quality-quick-checks.md), and [Week 3 Work Checklist](week-03-work-checklist.md). |
| Document update | [Candidate Vertical Slice](candidate-vertical-slice.md), [Wireframe Notes](wireframe-notes.md), and [Design Doc v1](../week-02/design-doc-v1.md). |

## Individual receipts

| Student | What they did | Evidence link |
|---|---|---|
| Sherap Hyolmo | Added the SmartServe POS prototype and documented the payment and inventory approach. | [MVP commit `c78af82`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c78af82); [Week 2 individual receipt](../week-02/individual_evidence.md/sherap_Hyolmo.md). Confirm the Week 3 ownership split before submission. |
| Lama Muskan | Updated the architecture sketch to identify FastAPI as the backend and align the proposed stack with the implementation. | [Architecture update commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/16efb35); [Week 2 individual receipt](../week-02/individual_evidence.md/lama_muskan.md) |
| Ualson Tamang | Week 3 contribution receipt pending. | Add an issue, sketch, review, or research link. |
| Shuzita Majhi | Created the Week 4 Chuseok checkpoint, linking the sketches, midterm-demo sentence, Week 5 question, and first action after the break. | [Chuseok checkpoint](../week-04-chuseok/chuseok-checkpoint.md) |
| Shreya | Proposed verification support. Week 3 contribution receipt pending. | Add a test note, issue, or review link. |


## Blockers or risks

| Blocker/risk | Owner | Next action |
|---|---|---|
| The main payment and inventory path has no recorded end-to-end check. | Lama Muskan, Sherap Hyolmo, and Shreya | Run the two-latte scenario and record expected and actual totals, stock, receipt, dashboard, and repeat-payment result. |
| Proposed build issues and ownership are not fully linked. | Team | Create or identify issues and add their links to the slice and design doc. |
| Prototype screenshots or a recorded demo are missing. | Shuzita Majhi and team | Capture the prototype screens or record the two-latte demo; the three planning wireframes are linked in the Wireframe Notes. |

## Decision record

| Decision | Why we chose it | Owner | Evidence / Issue link |
|---|---|---|---|
| Use one complete cafe sale as the candidate midterm slice. | It demonstrates the connection between ordering, payment, receipt, inventory, and sales in a short path. | Team 3 | [Candidate Vertical Slice](candidate-vertical-slice.md) |
| Deduct recipe ingredients only after simulated payment and prevent repeat deductions in the database. | An unpaid order must not reduce stock, and a repeated payment must not reduce it twice. | Team 3 | [Design Doc v1](../week-02/design-doc-v1.md), [investigation #2](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/2) |

## Next week's bridge task

- Use the light Week 4 Chuseok checkpoint to share a rough screen sketch or photo, restate the midterm demo sentence, and name one question for Week 5.
- In Week 5, confirm build-issue ownership and record the first repeatable run of the candidate slice.
