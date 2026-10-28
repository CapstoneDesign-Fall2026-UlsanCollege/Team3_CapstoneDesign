
# Post-Midterm Reset & MVP Gap Analysis — SmartServe POS

**Course:** Capstone Design — Fall 2026  
**Team:** Team 3 — SmartServe POS  
**Week:** 8 (Midterm Gate)  
**Date:** October 28, 2026  
**Repository:** [Team3_CapstoneDesign](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)  
**Working Branch:** `smartserve-mvp`

---

## 1. Executive Summary & Review Context

During Week 8, Team 3 reached the Midterm Gate for **SmartServe POS**, a point-of-sale and inventory management system designed to connect order processing, payment confirmation, and ingredient stock management.

The project focuses on providing a reliable workflow in which users can select menu items, enter quantities, calculate order totals, complete a payment step, and update inventory based on the ingredients used in each order.

The established vertical-slice workflow includes:

- Selecting menu items and quantities.
- Calculating order totals using stored menu prices.
- Creating a unique order.
- Processing a simulated payment.
- Deducting recipe ingredients from inventory after successful payment.
- Recording inventory movements to maintain an auditable stock history.

The purpose of this Week 8 document is to review the project's current position after the midterm, identify remaining MVP gaps, and establish a realistic development direction for Weeks 9–11.

**Important status distinction:** Previously documented implementation and test evidence should not automatically be treated as a new Week 8 verification. Any new demonstration, test, or deployment claim must be supported by corresponding evidence.

---

## 2. Core Lessons Learned

### Course Lesson

**Context:** During the development process, the team worked on connecting multiple parts of the POS system, including order management, payment processing, and inventory deduction.

**Core Insight:** A feature is not complete simply because its interface exists. The team needs to demonstrate that the underlying process works correctly, that data remains consistent, and that important edge cases are handled.

**Decision Pattern:**

> We initially focused on implementing the main application workflow. Our development and testing experience showed that the reliability of the connection between different system components is equally important. Therefore, our next development phase will prioritize completing and verifying the core POS workflow rather than expanding optional features.

### Project Lesson

**Context:** SmartServe POS connects order creation, simulated payment, and recipe-based inventory deduction.

**Core Insight:** Payment and inventory operations must remain consistent. An order should not deduct ingredients multiple times, and inventory changes should be traceable through inventory movement records.

The project also uses `inventory_deducted` as a value derived from inventory movements rather than treating it as an independent source of truth.

**Decision Pattern:**

> We learned that a successful order requires more than saving an order record. Payment status, inventory deduction, and stock movement records must remain consistent. Therefore, our next priority is to strengthen the transaction workflow, test failure scenarios, and ensure that inventory is deducted exactly once.

---

## 3. MVP Gap Analysis

| Feature Area | Established Current State | Target MVP State | Remaining Gap | Priority |
|---|---|---|---|---|
| Menu Selection | Users can select menu items and quantities. | Reliable item selection and quantity handling. | Verify edge cases and complete workflow. | P1 |
| Order Creation | Orders receive unique identifiers and use stored prices. | Reliable order creation with consistent order data. | Verify duplicate submissions and invalid quantities. | P1 |
| Payment Processing | Simulated payment changes the order to `paid`. | Reliable payment confirmation and failure handling. | Payment is simulated rather than connected to a real payment gateway. | P1 |
| Inventory Deduction | Recipe-based stock deduction is connected to successful payment. | Deduct ingredients exactly once after successful payment. | Verify retry, duplicate request, and failure scenarios. | P0 |
| Inventory Movements | Stock changes are recorded through inventory movement records. | Complete and traceable stock history. | Verify movement records against actual stock changes. | P0 |
| Data Consistency | Payment and inventory operations are designed to commit together. | No partial or inconsistent order transactions. | Continue testing transaction rollback and failure handling. | P0 |
| Recipe Management | Recipe-related functionality has been developed and tested. | Reliable recipe editing and unit conversion. | Verify equivalent-unit handling and order restrictions. | P1 |
| Order Item History | Order items preserve the menu name and price at creation. | Historical orders retain their original item information. | Verify historical data and migration limitations. | P1 |
| Deployment & Setup | The project uses a containerized development setup. | A reproducible environment for reviewers and team members. | Verify the latest clean-clone setup and documentation. | P1 |

**Priority definitions:**

- **P0:** Critical for the reliability of the MVP.
- **P1:** Important for completing and verifying the main workflow.
- **P2:** Improvement that can be postponed if it is outside the core demonstration scope.

---

## 4. Sprint 2 Scope Cut Contract — What We Will Not Prioritize

To protect the remaining development time, Team 3 should avoid expanding the application beyond the essential POS workflow.

The following areas should remain outside the immediate MVP priority unless they are already required by the course rubric:

1. **Postpone — Advanced Analytics and Reporting**

   **Reason:** The primary objective is to ensure accurate order processing and inventory updates. Advanced dashboards and business analytics should not take priority over transaction reliability.

2. **Postpone — Unnecessary UI Customization**

   **Reason:** The existing interface should be improved only when necessary for usability, accessibility, or the main workflow.

3. **Postpone — Additional Payment Integrations**

   **Reason:** The immediate focus is to verify the existing simulated payment workflow and its connection to inventory deduction. Additional payment providers would increase implementation and testing complexity.

4. **Postpone — Optional Features Outside the Core POS Workflow**

   **Reason:** Features that do not directly improve menu selection, order processing, payment confirmation, or inventory management should be considered after the MVP is stable.

---

## 5. Focus Milestone Specification — Reliable Order and Inventory Workflow

### Overview

- **Milestone Title:** Milestone 1 — Complete and Verify the SmartServe POS Transaction Workflow
- **Target Sprint:** Sprint 2 (Weeks 9–11)
- **Primary Focus:** Order creation, payment confirmation, and inventory deduction.
- **Verification Focus:** Duplicate prevention, transaction consistency, and inventory movement accuracy.

### Technical Specifications

**1. Order Creation**

- Accept selected menu items and quantities.
- Calculate totals using stored menu prices.
- Generate a unique order identifier.
- Preserve the relevant order-item information.

**2. Payment Confirmation**

- Update the order to `paid` after successful simulated payment.
- Ensure unsuccessful payment does not trigger inventory deduction.
- Prevent repeated payment handling from creating inconsistent order states.

**3. Recipe-Based Inventory Deduction**

- Retrieve the recipe ingredients associated with the ordered menu items.
- Calculate the required ingredient quantities.
- Convert units where necessary.
- Deduct inventory only after successful payment.
- Prevent duplicate inventory deductions.

**4. Inventory Movement Records**

- Record each stock deduction as an inventory movement.
- Keep movement records consistent with the actual inventory balance.
- Use inventory movements as the source for determining whether inventory has been deducted.

**5. Transaction Consistency**

- Keep payment and inventory changes consistent.
- Handle failures without leaving partially completed transactions.
- Verify that repeated requests do not deduct the same ingredients twice.

### Acceptance Criteria & Success Signals

- [ ] A user can select menu items and quantities.
- [ ] The system calculates the correct order total.
- [ ] A unique order is created.
- [ ] Successful simulated payment updates the order status to `paid`.
- [ ] Inventory is deducted according to the recipe quantities.
- [ ] Inventory is deducted only once for each successfully processed order.
- [ ] Inventory movement records match the stock changes.
- [ ] Failed payment does not deduct inventory.
- [ ] Duplicate requests do not create duplicate deductions.
- [ ] Recipe unit conversion is handled correctly.
- [ ] The application can be set up using the documented project instructions.

---

## 6. Week 9–11 Roadmap

| Week | Focus | Expected Outcome |
|---|---|---|
| Week 9 | Review existing implementation and address critical workflow gaps. | A prioritized list of issues and fixes for the transaction workflow. |
| Week 10 | Test payment, inventory deduction, duplicate handling, and failure scenarios. | Documented test results and corrected issues. |
| Week 11 | Stabilization, regression testing, documentation, and MVP freeze preparation. | A stable and demonstrable MVP with supporting evidence. |

---

## 7. Evidence and Verification Policy

The team should maintain a clear distinction between implemented features, previously tested features, newly verified features, and planned work.

Evidence should include:

- Relevant backend test results.
- Screenshots or logs showing successful order processing.
- Evidence of payment status changes.
- Inventory balance before and after deduction.
- Inventory movement records.
- Tests demonstrating that duplicate deductions are prevented.
- Clean-clone setup and execution instructions.

Previously established evidence includes the backend test file `smartserve-pos/backend/test_owner_management.py` and a reported result of **24 backend tests passed** in the Week 7 contribution work. This should be identified as earlier evidence, not automatically presented as a new Week 8 test result.

---

## 8. Conclusion

Week 8 marks the transition from the midterm review into the final development and stabilization phase of SmartServe POS.

The team's immediate objective is not to increase the number of features, but to improve the reliability of the existing system. The most important work for the next sprint is to verify the complete order-to-payment-to-inventory workflow, ensure accurate stock deductions, handle duplicate requests safely, and prepare clear evidence for the final MVP evaluation.

By maintaining a bounded scope and prioritizing verifiable functionality, Team 3 aims to deliver a stable and reliable SmartServe POS MVP by the Week 11 freeze milestone.
