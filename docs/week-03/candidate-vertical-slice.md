# Candidate Vertical Slice — Week 3

**Team:** Team 3
**Project:** SmartServe POS
**Last updated:** September 23, 202

## Midterm Demo Sentence

At the midterm demo, the team will demonstrate a complete SmartServe order flow: selecting menu items and quantities, calculating the total from stored menu prices, simulating payment, changing the order status to `paid`, and deducting the required recipe ingredients from inventory exactly once.

## User Path

1. The user selects menu items and quantities to create an order.
2. The system calculates the order total using the stored menu prices and creates a unique order.
3. The user can see the order total, simulate payment, and see the order status change to `paid` while the required inventory is deducted.

## In Scope for This Slice

* Create an order with menu items and quantities.
* Calculate the total using the stored menu price.
* Simulate payment and change the order status to `paid`.
* Deduct the required recipe ingredients from inventory after successful payment.
* Prevent inventory from being deducted more than once for the same order.

## Out of Scope for This Slice

* Real payment gateway integration.
* Customer accounts or loyalty features.
* Advanced inventory management or supplier management.
* Full production-ready UI design.

## First Three Build Issues

| Issue                                    | Owner         | Definition of Done                                                                                                                                                                                            |
| ---------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create order and calculate total         | Lama Muskan   | A user can select menu items and quantities, and the backend calculates the total using the stored menu prices. A test confirms that the calculated total is correct.                                         |
| Simulate payment and update order status | Hyolmo Sherap | An order can be submitted for simulated payment, receives a unique order ID, and changes to `paid` after successful payment.                                                                                  |
| Deduct recipe inventory after payment    | Lama Muskan   | When an order becomes `paid`, the required recipe ingredients are deducted from inventory. A Latte test confirms the correct ingredients are deducted, and `inventory_deducted` prevents duplicate deduction. |

## Biggest Risk or Uncertainty

What could prevent this path from working, and what is the smallest test that would reduce the uncertainty?

> **Risk:** The order, payment status, recipe information, and inventory deduction may not be connected correctly, which could cause incorrect totals or duplicate inventory deductions.
>
> **Smallest test:** Create one Latte order, simulate payment, verify that the order becomes `paid`, and confirm that the correct Latte ingredients are deducted exactly once.
>
> **Owner:** Lama Muskan

## Evidence Links

* Issue #8: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/8
* Issue #9: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/9
* Issue #10: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/10
* Issue #14: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/14
* Wireframes: [screen notes](wireframe-notes.md), [cashier](wireframe-Landing-page.jpg), [inventory](wireframe-Inventory.jpg), and [owner dashboard](wireframe-Owner-dashboard.jpg).
* Architecture sketch: [architecture and confirmed stack](architecture-sketch.md).
* Stack comparison: [Week 3 comparison](tech-stack-comparison.md).
* Inventory/payment verification: [Issue #3 local test results](issues/issue-03/README.md); browser and PostgreSQL concurrency checks remain pending.

## Week 5 Restart Move

When this candidate becomes an implementation plan, the team will:

* break the path into build Issues;
* confirm owners and Definitions of Done;
* name the shared preview or test path; and
* update the risk and bridge task.
