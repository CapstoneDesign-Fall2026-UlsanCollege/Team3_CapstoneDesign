# Candidate Vertical Slice — Week 3

**Team:** Team 3

**Project:** SmartServe POS

**Last updated:** 2026-09-22

This is a planning candidate for the midterm demonstration. The Week 5 implementation plan should confirm its scope, owners, tests, and shared preview path.

## Midterm demo sentence

> A cashier creates a two-latte order, completes a simulated payment, sees a receipt, and verifies that the correct milk and coffee quantities were deducted once and the sale appears on the daily dashboard.

## User path

1. The cashier selects menu items and quantities and creates an order.
2. The backend calculates the total from stored menu prices and creates a unique order ID.
3. The cashier completes a simulated payment and sees the order status change to `paid`.
4. The receipt appears; recipe ingredients are deducted once and the sale appears on the daily dashboard.

## In scope for this slice

- Create an order with menu items and quantities.
- Calculate the total using stored menu prices.
- Simulate payment and mark the order `paid`.
- Show a receipt and the resulting daily sale.
- Deduct the required recipe ingredients after payment, exactly once per order and ingredient.

## Out of scope for this slice

- Real payment gateway integration.
- Customer accounts or loyalty features.
- Supplier management and advanced inventory management.
- Production-ready interface design.

## First three build issues

These are proposed issue scopes. Link the actual GitHub issues when they exist.

| Issue | Proposed owner | Definition of done |
|---|---|---|
| Create order and calculate total | Lama Muskan | A cashier can select menu items and quantities. The backend calculates the total from stored prices, and a check confirms the expected total. |
| Simulate payment and update order status | Sherap Hyolmo | A created order can receive a simulated payment, becomes `paid`, and returns a receipt. A repeated payment request returns the existing paid order. |
| Deduct recipe inventory after payment | Lama Muskan | A two-latte payment deducts the expected recipe quantities once. A repeated request creates no extra payment or inventory movement. Insufficient stock prevents payment. |

## Biggest risk or uncertainty

> **Risk:** Order payment, recipe data, and stock updates could become inconsistent or deduct ingredients twice.
>
> **Smallest check:** Record the initial stock, pay for two lattes, compare the final stock with the recipe quantities, and repeat the payment request.
>
> **Proposed owner:** Lama Muskan, with Sherap Hyolmo supporting payment handling and Shreya supporting verification.

The current backend uses a transaction, row locks, and unique database constraints for this rule. The check above still needs a recorded result.

## Evidence links

- [Design Doc v1](../week-02/design-doc-v1.md)
- [User-flow sketch](../week-02/user-flow-sketch.png)
- [SmartServe MVP README](../../smartserve-pos/README.md)
- [Backend order and payment implementation](../../smartserve-pos/backend/app/main.py)
- [Cashier, inventory, and owner screens](../../smartserve-pos/frontend/src/main.tsx)
- GitHub build issue list: link after issue scopes and ownership are confirmed.
- Demo or test result: link after the slice is run and recorded.

## Week 5 restart move

- Confirm the build issues, owners, and definitions of done.
- Record a shared run or preview path and the two-latte test result.
- Update the risk and next bridge task based on that result.
