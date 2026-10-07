# Individual Evidence Receipt

**Student:** Sherap Hyolmo  
**GitHub username:** @daydevil80  
**Team:** Team 3  
**Week:** 2  
**Date:** 2026-09-16  

## Receipt 1 — Inventory-Deduction Investigation

- **What I did:** Investigated when SmartServe POS should deduct recipe ingredients and how the system can prevent the same completed order from deducting inventory more than once.
- **Evidence link:** [Investigation #2 — When should SmartServe deduct ingredients from inventory?](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/2)
- **How I checked it:** Compared deducting ingredients when an order is created against deducting them only after successful simulated payment. I reviewed PostgreSQL transactions, row-level locking, and unique constraints and considered repeated payment requests, page refreshes, cancelled orders, and partial failures.
- **What I learned or changed:** I learned that deducting inventory when an order is created could incorrectly reduce stock for unpaid or cancelled orders. SmartServe will deduct ingredients only after successful payment and will use database-level protection to prevent duplicate deductions.

## Receipt 2 — Design Doc and Project Scope

- **What I did:** Helped define and document the SmartServe MVP, including its target users, in-scope and out-of-scope features, data model, cashier workflow, midterm demonstration, risks, and technical direction.
- **Evidence link:** [SmartServe POS Design Doc v1](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-02/design-doc-v1.md)
- **How I checked it:** Reviewed the completed team investigations and connected their findings to the functional requirements and project decisions. I also checked that the document included the required users, scope boundaries, midterm-demo sentence, user flow, risk investigation, and evidence links.
- **What I learned or changed:** I learned that the project needed to focus on one complete and reliable workflow rather than many advanced features. The MVP now prioritizes menu selection, backend total calculation, final stock validation, simulated payment, receipt generation, one-time inventory deduction, and daily sales reporting.

## Receipt 3 — Implementation Planning

- **What I did:** Converted the inventory-deduction investigation into a buildable implementation task describing how SmartServe should complete payment and update inventory safely.
- **Evidence link:** [Implementation Issue #3 — Implement idempotent inventory deduction after payment](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3)
- **How I checked it:** Connected the implementation task to the selected database approach and identified the required order-status validation, transaction handling, inventory audit records, and duplicate-request protection.
- **What I learned or changed:** I learned that application-level button protection is not sufficient. The backend and database must enforce the rule so that repeated requests cannot create a second payment or deduct the same ingredients again.

## Week 2 Reflection

My main contribution this week was turning SmartServe’s largest technical risk into a documented decision and a buildable task.

The investigation changed the project from a general POS idea into a smaller MVP with a specific reliability rule:

> A completed order may deduct each required ingredient only once.

My next step is to implement and test the order-payment-inventory workflow using the decisions recorded in the investigation and Design Doc.