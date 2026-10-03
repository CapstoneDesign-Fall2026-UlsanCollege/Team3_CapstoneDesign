
# Week 5 Work Checklist — Start the Vertical Slice

**Date:** Thu 2026-10-01 to Wed 2026-10-07
**Team:** Team 3

## Core work — complete all

### Chosen vertical slice

The team selected the SmartServe POS payment and inventory flow as the implementation slice:

**Create Order → Calculate Total → Simulate Payment → Update Order Status → Deduct Inventory → Show Receipt**

The system uses the stored order-item unit price when calculating the order total. A successful payment changes the order to `paid` and deducts the required ingredients once.

**Visible proof for Oct 8:** demonstrate a two-Latte order, successful payment, correct inventory deduction, and a repeated payment request returning HTTP 409 without changing the saved payment, inventory, or sales results.

### Implementation work

* Reviewed the previous SmartServe architecture, candidate slice, and Chuseok checkpoint evidence.
* Continued implementation using **FastAPI + PostgreSQL + SQLAlchemy**.
* Verified that `OrderItem.unit_price` stores the price used when the order is created.
* Added a test confirming that changing the current menu price does not change an existing order's saved price.
* Verified successful payment and inventory deduction.
* Verified repeated payment protection and the HTTP 409 response.
* Added/updated evidence in GitHub for the implementation and tests.

## Evidence

* [Issue #3 — Payment and inventory verification](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3)
* [Issue #12 — Store unit price in order item](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12)
* [Two-Latte demo evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/evidence/two-latte-demo/README.md)
* [Payment test evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-04-chuseok/payment-test-evidence/README.md)
* [Issue #3 verification evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/issues/issue-03/README.md)
* [SmartServe backend](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/smartserve-mvp/smartserve-pos/backend)

## Stretch target

### 1. Add a repeatable smoke check

Create or maintain a repeatable test for the payment flow so that a successful payment and a repeated payment can be verified consistently.

**Why:** This reduces the risk of accidentally deducting inventory twice.

### 2. Improve setup/run instructions

Document the backend setup requirements, including Python dependencies and database requirements.

**Why:** Another teammate should be able to start the project and reproduce the implementation.

## Risks and exceptions

| Item                         | Owner | Next action                                                           | Review point            |
| ---------------------------- | ----- | --------------------------------------------------------------------- | ----------------------- |
| Local PostgreSQL environment | sherap| Confirm the database is running and the backend connects successfully | Before Oct 8 demo       |
| Local Python setup           | Lama Muskan | Keep the required Python dependencies documented                | Before final checkpoint |

## Final check

* The team can demonstrate the complete payment → inventory flow.
* The next implementation/testing step is visible in GitHub.
* Evidence for the payment, inventory, and order-price decisions is linked.
* The team has a visible, testable proof ready for the Oct 8 checkpoint.
