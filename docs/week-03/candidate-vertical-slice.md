
# Candidate Vertical Slice — Week 3

**Team:** Team 3  
**Project:** SmartServe POS  
**Last updated:** September 21, 2026

This is a planning candidate, not a promise that the whole feature will be built. Revisit it in Week 5 when the implementation plan is more detailed.

## Midterm Demo Sentence

## User Path

1. The user selects menu items and quantities to create an order.
2. The system calculates the order total using the stored menu prices and creates a unique order.
3. The user can see the order total, simulate payment, and see the order status change to `paid` while the required inventory is deducted.

## In Scope for This Slice

- Create an order with menu items and quantities.
- Calculate the total using the stored menu price.
- Simulate payment and change the order status to `paid`.
- Deduct the required recipe ingredients from inventory after successful payment.
- Prevent inventory from being deducted more than once for the same order.

## Out of Scope for This Slice

- Real payment gateway integration.
- Customer accounts or loyalty features.
- Advanced inventory management or supplier management.
- Full production-ready UI design.

## First Three Build Issues

| Issue | Owner | Definition of Done |
|---|---|---|
| Create order and calculate total | TBD | A user can select menu items and quantities, and the backend calculates the total using the stored menu prices. A test confirms that the calculated total is correct. |
| Simulate payment and update order status | TBD | An order can be submitted for simulated payment, receives a unique order ID, and changes to `paid` after successful payment. |
| Deduct recipe inventory after payment | TBD | When an order becomes `paid`, the required recipe ingredients are deducted from inventory. A Latte test confirms the correct ingredients are deducted, and `inventory_deducted` prevents duplicate deduction. |

## Biggest Risk or Uncertainty

What could prevent this path from working, and what is the smallest test that would reduce the uncertainty?

> **Risk:** The order, payment status, recipe information, and inventory deduction may not be connected correctly, which could cause incorrect totals or duplicate inventory deductions.
>
> **Smallest test:** Create one Latte order, simulate payment, verify that the order becomes `paid`, and confirm that the correct Latte ingredients are deducted exactly once.
>
> **Owner:** TBD

## Evidence Links

- Issue list:
- Wireframe:
- Architecture sketch:
- Stack comparison:

## Week 5 Restart Move

When this candidate becomes an implementation plan, the team will:

- break the path into build Issues;
- confirm owners and Definitions of Done;
- name the shared preview or test path; and
- update the risk and bridge task.
