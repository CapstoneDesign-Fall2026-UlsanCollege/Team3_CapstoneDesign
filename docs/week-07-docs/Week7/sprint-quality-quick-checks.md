# Sprint Quality Quick Checks

Complete the section for your current sprint at its final class meeting. These are quick evidence checks, not a demand for a perfect product.

## Sprint 0 - Launch and Scope (Week 3)

- [x] The team established the SmartServe POS project and its purpose.
- [x] The project repository and technology stack were established.
- [x] The project scope and development direction were documented.
- [x] The team created issues to organize project tasks and development work.

**Project:** SmartServe POS – Team 3  
**Repository:** [Team 3 GitHub Repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)  
**Technology stack:** React, TypeScript, Vite, FastAPI, PostgreSQL, and Docker.

## Sprint 1 - Vertical Slice (Week 7)

October 21: [24 current backend tests and frontend build](evidence/2026-10-21/README.md) pass. These are automated checks; independent browser verification and the spoken rehearsal remain incomplete. [Issue #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21) tracks them.

- [x] Failure/fallback checked in isolated service tests: failed payment returns 402 without changing stock; duplicate payment returns 409 without another deduction. [Expected/actual results](evidence/2026-10-21/demo-results.json).
- [x] Week 6 recipe-unit and new-order receipt-name defects fixed and covered by regression tests. Legacy original names cannot be reconstructed.
- [ ] A non-author teammate verifies the pushed app in a browser and links the result.
- [ ] Team completes and records a real 3–5 minute rehearsal.

- [x] The main order-to-payment workflow has been implemented.
- [x] The system supports simulated payment methods.
- [x] The system generates an order receipt.
- [x] Inventory deduction is connected to successful payment.
- [x] Duplicate-payment protection has been implemented.
- [x] The project includes backend tests and frontend build verification.
- [x] Setup and demonstration instructions are documented.

### October 21 Technical Check and Demonstration Path

SmartServe POS is designed to help café staff manage customer orders, payments, receipts, and ingredient inventory through one system.

The main demonstration path is:

1. Open the SmartServe POS application.
2. Select two Latte items.
3. Confirm the total price of ₩9,000.
4. Complete the simulated payment.
5. Display the generated receipt.
6. Verify the ingredient deduction: 500 ml of milk and 36 g of coffee beans.
7. Check the daily sales dashboard for the completed order.

### Technical Implementation

- **Order management:** Staff can select menu items and quantities to create orders.
- **Payment:** The application supports simulated cash, card, and QR payment workflows.
- **Receipt:** A receipt is generated after payment.
- **Inventory:** Ingredient quantities are deducted after successful payment.
- **Payment protection:** Duplicate payment requests are prevented from deducting inventory again.
- **Sales dashboard:** Paid orders contribute to the sales information displayed by the system.
- **Database:** PostgreSQL stores order, payment, and inventory information.

### Recorded Technical Evidence

The October 14 evidence package records:

- 20 passing backend tests.
- Successful frontend production build.
- Successful payment and duplicate-payment checks in the recorded demonstration.
- Successful checks for failed-payment handling and insufficient inventory handling.

**Supporting evidence:**

- [Project README](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/README.md)
- [SmartServe Setup and Project README](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/README.md)
- [Week 6 Automated Check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/automated-check.md)
- [Week 6 Test Plan](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/test-plan.md)
- [Week 6 Setup and Demo Instructions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/setup-and-demo.md)
- [October 14 Evidence Package](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-06/evidence/2026-10-14)
- [Issue #3 – Payment and Inventory Deduction](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3)

## Sprint 2 - MVP and Freeze (Week 11)

- [ ] The MVP happy path has been fully reviewed and documented.
- [ ] Known bugs are labeled by severity and have an owner or plan.
- [ ] New features are frozen or explicitly justified against the MVP contract.
- [ ] The project has basic input/error handling or a documented limitation.
- [ ] AI-assisted or outside material is reviewed, explainable, and attributed where relevant.

## Sprint 3 - QA and Handoff (Week 14)

- [ ] Main demo path, error/empty state, and key links or buttons have been checked.
- [ ] Keyboard access, visible labels, and readable contrast have received a basic review.
- [ ] Setup and handoff instructions work for someone outside the team.
- [ ] The project has safe demo data and no secrets or private data in shared evidence.
- [ ] Demo fallback and remaining blocker plan are documented.

## Sprint 4 - Final Readiness (Week 15)

- [ ] The final demo has been rehearsed with its fallback plan.
- [ ] Presentation and demo roles are assigned.
- [ ] Final evidence, contribution receipts, setup guide, and handoff links are easy to find.
- [ ] Blocker and major-bug status is current.
- [ ] The Final Readiness Report names any remaining action and owner.

## Week 7 Progress Summary

During Week 7, Team 3 reviewed the SmartServe implementation, organized technical evidence, and documented the main demonstration workflow.

The main focus was connecting order creation, simulated payment, receipt generation, inventory deduction, and sales reporting into one understandable café workflow.

The project has a documented setup process, a defined demonstration path, and recorded technical evidence supporting its current implementation.
