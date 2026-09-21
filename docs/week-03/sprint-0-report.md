# Sprint 0 Report — Launch and Scope

**Team:** Team 3

**Project:** SmartServe POS

**Sprint:** Sprint 0 — Launch and Scope

**Date:** 2026-09-22

**Status:** [ ] Ready to close  [x] Ready with explicitly owned exceptions

This is the Sprint 0 exit summary for Week 3. The [Week 3 Weekly Report](weekly-report.md) contains the detailed weekly progress.

## Sprint 0 outcome

Team 3 has selected SmartServe POS, defined a candidate midterm path, and built an initial prototype. The next work is to verify the complete sale, confirm issue ownership, and record evidence that another team member can run the demo.

## Project snapshot

| Field | Current answer | Evidence link |
|---|---|---|
| Project purpose | Help a small café record orders, simulated payments, receipts, ingredient stock changes, and daily sales in one workflow. | [Design Doc v1](../week-02/design-doc-v1.md) |
| Target users | Cashiers who complete orders and managers who check inventory and sales. | [Design Doc v1](../week-02/design-doc-v1.md) |
| In-scope boundary | Menu and recipe data, cashier orders, simulated payments, receipts, one-time ingredient deduction, and basic inventory and sales views. | [Design Doc v1](../week-02/design-doc-v1.md) |
| Out-of-scope boundary | Real payments, supplier management, multiple branches, customer loyalty, mobile apps, and AI features. | [Design Doc v1](../week-02/design-doc-v1.md) |
| Possible midterm demo sentence | A cashier creates a two-latte order, completes a simulated payment, sees a receipt, and verifies the stock and daily sales changes. | [Candidate Vertical Slice](candidate-vertical-slice.md) |

## Sprint 0 exit evidence

| Requirement | Evidence link | Status or short note |
|---|---|---|
| Team repository and Project board work | [Team repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign), [Team 3 Project board](https://github.com/orgs/CapstoneDesign-Fall2026-UlsanCollege/projects/4) | Repository and board are recorded in the Week 1 report; current board state needs confirmation. |
| Team Working Agreement is linked and current | [Team Working Agreement](../week-01/team-working-agreement.md) | Document exists; team should confirm it is still current. |
| Six to ten next-work Issues exist | Add GitHub Issues link | Issues exist according to the team; count and links need verification. |
| Important Issues have first owners | Add GitHub Issues link | Pending verification of issue assignees. |
| At least three Issues have a checkable Definition of Done | [Candidate Vertical Slice](candidate-vertical-slice.md), [duplicate-deduction investigation #2](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/2), [implementation issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3) | Two issue Definitions of Done were provided. A third issue Definition of Done is pending. |
| Tech stack comparison is recorded | [Tech Stack Comparison](tech-stack-comparison.md) | Two stacks and the selected FastAPI stack are documented; team review link remains pending. |
| Rough wireframe placeholders are linked | [Wireframe Notes](wireframe-notes.md), [cashier wireframe](wireframe-Landing-page.jpg), [inventory wireframe](wireframe-Inventory.jpg), [owner dashboard wireframe](wireframe-Owner-dashboard.jpg) | Three pen-drawn screen wireframes are linked; prototype screenshots or a recorded demo are pending. |
| Rough architecture placeholder is linked | [Architecture Sketch](architecture-sketch.md) | Complete as a planning sketch. |
| Candidate vertical slice is linked | [Candidate Vertical Slice](candidate-vertical-slice.md) | Complete as a planning candidate. |
| Sprint 0 Quality Quick Checks are complete | Add check document or result link | Pending: no recorded quick-check result is linked here. |
| Week 3 Weekly Report is complete | [Week 3 Weekly Report](weekly-report.md) | Draft exists; demo results and individual evidence remain pending. |

## Candidate vertical slice

- **User or actor:** Café cashier.
- **Start state:** A small menu and its ingredient recipes are available; the cashier needs to complete a customer order.
- **Smallest end-to-end path:**
  1. Select two lattes and create an order.
  2. Check the total calculated from the stored menu price.
  3. Complete a simulated payment.
  4. View the paid order and receipt.
  5. Check that the required milk and coffee beans were deducted once.
  6. Check that the sale appears on the daily dashboard.
- **What the demo should prove:** One sale updates the order, payment, receipt, inventory, and sales views consistently. Repeating payment does not deduct stock again.
- **Deliberately out of scope:** Real payment processing, supplier management, customer accounts, and production-ready interface design.
- **Evidence:** [Candidate Vertical Slice](candidate-vertical-slice.md).

## Risks and owned exceptions

| Risk or exception | Owner | Next action | Due or review point |
|---|---|---|---|
| The full two-latte demo and repeat-payment result have not been recorded. | Sherap Hyolmo, then Lama Muskan; Shuzita Majhi supporting | Run the scenario and link expected and actual results. | Week 5 restart |
| The seed data and Week 2 example use different latte milk quantities. | Sherap Hyolmo and Lama Muskan | Agree on one recipe value and update demo expectations. | Before demo recording |
| Build Issues, owners, and Definitions of Done are not fully linked in the documents. | Team 3 | Confirm the GitHub Issues and add their links. | Week 5 restart |
| Prototype screenshots or a recorded demo are missing. | Shuzita Majhi | Capture actual screens or record the demo; planning wireframes are now linked. | Week 5 restart |

## Bridge into Week 4 and Sprint 1

- **Week 4 Chuseok checkpoint:** Share a rough screen sketch or photo, the midterm demo sentence, and one blocker or question for Week 5.
- **Rough sketch or photo link:** [Week 2 user-flow sketch](../week-02/user-flow-sketch.png); Week 4 image pending.
- **One question for Week 5:** Can another team member run and verify the complete two-latte sale using the documented setup?
- **First action after the break:** Confirm issue ownership and the recipe quantity, then record the end-to-end demo and repeat-payment check.

## Final check

- [ ] Every evidence link resolves for a reader with team-repository access.
- [x] The team can use the design doc and candidate slice to explain the purpose, users, scope, and demo path.
- [ ] The next work is represented by small GitHub Issues with owners and checkable completion criteria.
- [ ] Confirm no personal data, secrets, or unapproved real-user data appear in the submitted evidence.
- [ ] Link this report from the Week 3 Weekly Report.
