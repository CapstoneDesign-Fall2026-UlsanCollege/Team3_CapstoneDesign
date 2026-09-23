---
name: Risk or Blocker
about: Record a project risk, blocker, or decision needed
title: "Risk/Blocker: Verify payment and inventory stay consistent"
labels: risk, blocker
assignees: " Team"
---

## What is the risk or blocker?

A failed or repeated simulated payment could leave order, payment, and inventory records inconsistent or deduct ingredients more than once.

## Why does it matter?

SmartServe POS must show the correct receipt, stock quantity, and daily sales after each completed order. Incorrect deductions would make the main midterm demo unreliable.

## What have we tried?

The FastAPI backend processes payment and inventory updates in one PostgreSQL transaction. It locks the order and affected ingredients and uses database constraints to allow only one payment per order and one inventory movement per order and ingredient.

The implementation exists, but the team has not yet recorded the full two-latte demo and repeat-payment test result.

## What decision or help do we need?

We need to verify the complete workflow and agree on the latte recipe quantity before recording the demo. The seeded recipe uses **250 ml milk and 18 g coffee beans per latte**, while the Week 2 design document gives **200 ml milk** as an example.

## Owner

1. Sherap Hyolmo — primary owner
2. Lama Muskan — second owner

**Supporting:** Shuzita Majhi

## Next action

- [ ] Agree on the latte recipe quantity used for the demo.
- [ ] Record starting milk and coffee-bean stock.
- [ ] Create an order for two lattes and complete a simulated payment.
- [ ] Check the order status, receipt, inventory, and daily sales dashboard.
- [ ] Repeat the payment request and confirm no second deduction or payment record is created.
- [ ] Record the expected and actual results and link them to the Week 3 report.
