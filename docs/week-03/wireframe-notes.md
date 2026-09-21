# Wireframe Notes — Week 3

**Team:** Team 3

**Project:** SmartServe POS

**Week:** 3

These interaction notes describe the current candidate screens. The [Week 2 user-flow sketch](../week-02/user-flow-sketch.png) shows their sequence. The linked Week 3 images are pen-drawn planning wireframes, not screenshots of a tested application.

## Screen / interaction 1

- **Name:** Cashier order and payment
- **Target user:** Cashier
- **What the user does:** Selects menu items, adjusts quantities, chooses dine-in or takeaway, and selects a simulated payment method.
- **What the screen shows:** Menu cards, current order, calculated total, payment actions, feedback, and a receipt after successful payment.
- **Sketch/photo link:** [Cashier landing-page wireframe](wireframe-Landing-page.jpg).

## Screen / interaction 2

- **Name:** Ingredient inventory
- **Target user:** Manager or cashier checking stock
- **What the user does:** Checks ingredient quantities after a sale.
- **What the screen shows:** Ingredient name, quantity and unit, reorder level, and low-stock status.
- **Sketch/photo link:** [Inventory wireframe](wireframe-Inventory.jpg).

## Screen / interaction 3

- **Name:** Owner sales dashboard
- **Target user:** Owner or manager
- **What the user does:** Confirms that the paid order appears in the day's sales.
- **What the screen shows:** Today's sales total, paid-order count, and recent paid orders.
- **Sketch/photo link:** [Owner dashboard wireframe](wireframe-Owner-dashboard.jpg).

## Easiest first screen to build

> The cashier menu and order screen.

It uses a small seeded menu and makes the main user path visible before payment, inventory, and dashboard verification. The current [frontend prototype](../../smartserve-pos/frontend/src/main.tsx) already implements this interaction.
