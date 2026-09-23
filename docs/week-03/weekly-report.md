# Weekly Report — Week 3

**Team:** Team 3

**Project:** SmartServe POS

**Date:** 2026-09-22

**Last updated:** 2026-09-23

## This week's goal

Define a small midterm demo path, describe its main screens, and connect the Week 2 design to a buildable SmartServe POS prototype.

## What we committed to do

- [x] Confirm the React, TypeScript, FastAPI, PostgreSQL, and Docker Compose direction and document local startup.
- [x] Define the candidate order-to-payment-to-inventory vertical slice and the first three proposed build issues.
- [x] Describe the cashier, inventory, and owner interactions.
- [x] Add a prototype covering order creation, simulated payment, receipt, inventory, and daily sales views.
- [x] Record the automated two-Latte demo with inventory, receipt, and sales before/after evidence.
- [x] Record separate duplicate-payment, concurrency, and refresh/retry checks for Issue #3.
- [ ] Have another teammate independently review or reproduce the demo.
- [ ] Confirm issue links and individual contributions with the team.

## Evidence links

| Evidence | Link |
|---|---|
| Issue(s) | [Inventory-deduction investigation #2](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/2) and [implementation issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3); links for the other proposed build issues are pending. |
| PR(s) / commits | [MVP implementation commit `c78af82`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c78af82); branch: `smartserve-mvp`. Add a PR link if one is opened. |
| Screenshot / demo | [Cashier wireframe](wireframe-Landing-page.jpg), [inventory wireframe](wireframe-Inventory.jpg), and [owner dashboard wireframe](wireframe-Owner-dashboard.jpg); [Two-Latte demo and six screenshots](evidence/two-latte-demo/README.md) are recorded from a Codex-assisted automated run. |
| Test/check note | [Issue #3 test results](issues/issue-03/README.md): five local backend tests passed, including one-Latte deduction, duplicate prevention, failed payment, and insufficient stock; frontend build passed. PostgreSQL concurrency, browser rapid-click, and refresh/retry checks passed. The [two-Latte demo](evidence/two-latte-demo/README.md) also passed; independent teammate review remains pending. |
| Sprint 0 and checklists | [Sprint 0 Report](sprint-0-report.md), [Quality Quick Checks](sprint-quality-quick-checks.md), and [Week 3 Work Checklist](week-03-work-checklist.md). |
| Document update | [Candidate Vertical Slice](candidate-vertical-slice.md), [Wireframe Notes](wireframe-notes.md), and [Design Doc v1](../week-02/design-doc-v1.md). |

## Individual receipts

| Student | What they did | Evidence link |
|---|---|---|
| `daydevil80` (Sherap Hyolmo) | Added the SmartServe POS prototype. Implemented Issue #3 payment/inventory safeguards with Codex assistance: failed payments leave stock unchanged, successful payments record recipe deductions, and duplicate requests return a safe error. Added five backend tests and PostgreSQL/browser verification covering concurrent payments, rapid clicks, and refresh/retry. Organized the evidence and Week 3 document links. | [MVP commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c78af82); [Issue #3 implementation](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/67cf5d0); [test results and screenshots](issues/issue-03/README.md); [evidence organization](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/19475b1) |
| Lama Muskan | Updated the architecture sketch to identify FastAPI as the backend and align the proposed stack with the implementation. Additional evidence from my Week 2 work covers order-total calculation, payment and inventory protection, and the technology-stack investigation. | [Architecture update commit `16efb35`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/16efb35); [Week 2 individual evidence receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-02/individual_evidence.md/Lama_Muskan.md)
| Ualson Tamang | Week 3 contribution receipt pending. | Add an issue, sketch, review, or research link. |
| Shuzita Majhi | Created the Week 4 Chuseok checkpoint with sketches, the midterm-demo sentence, a Week 5 question, and the first action after the break. Uploaded the AI-assisted two-Latte demo evidence, including six screenshots and expected-versus-actual results. The automated demo was performed by Codex; personal review or reproduction is not yet recorded. | [Chuseok checkpoint](../week-04-chuseok/chuseok-checkpoint.md); [two-Latte demo evidence](evidence/two-latte-demo/README.md) |
| Shreya | Proposed verification support. Week 3 contribution receipt pending. | Add a test note, issue, or review link. |


## Blockers or risks

| Blocker/risk | Owner | Next action |
|---|---|---|
| Independent teammate reproduction of the recorded demo remains pending. | Team; confirm runner | Follow the setup instructions, reproduce the two-Latte scenario, and personally record the result. Automated evidence is already linked above. |
| Proposed build issues and ownership are not fully linked. | Team | Create or identify issues and add their links to the slice and design doc. |
| Personal review of the uploaded two-Latte evidence is not yet recorded. | Shuzita Majhi | Review the six screenshots and results, note findings, and personally confirm her contribution row with her exact GitHub login. |

## Decision record

| Decision | Why we chose it | Owner | Evidence / Issue link |
|---|---|---|---|
| Use one complete cafe sale as the candidate midterm slice. | It demonstrates the connection between ordering, payment, receipt, inventory, and sales in a short path. | Team 3 | [Candidate Vertical Slice](candidate-vertical-slice.md) |
| Deduct recipe ingredients only after simulated payment and prevent repeat deductions in the database. | An unpaid order must not reduce stock, and a repeated payment must not reduce it twice. | Team 3 | [Design Doc v1](../week-02/design-doc-v1.md), [investigation #2](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/2) |

## Next week's bridge task

- Use the light Week 4 Chuseok checkpoint to share a rough screen sketch or photo, restate the midterm demo sentence, and name one question for Week 5.
- In Week 5, confirm build-issue ownership and have another teammate reproduce the recorded candidate-slice demo.
- Confirm payment/inventory ownership in [Issue #11](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/11) and link the agreed decision.
