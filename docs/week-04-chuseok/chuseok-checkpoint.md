# Week 4 — Chuseok Checkpoint

**Team:** Team 3 — SmartServe POS
**Prepared:** September 23, 2026
**Status:** Prepared for team review

This lightweight checkpoint records our midterm scope, current evidence, and first action after the Chuseok break.

## 1. Rough sketch

Our existing sketches show the cashier, inventory, and owner dashboard screens.

- [Cashier sketch](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/wireframe-Landing-page.jpg)
- [Inventory sketch](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/wireframe-Inventory.jpg)
- [Owner dashboard sketch](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/wireframe-Owner-dashboard.jpg)

These are planning sketches, not screenshots of a completed interface.

## 2. Midterm-demo sentence

Our midterm demo will show a cashier creating a two-Latte order, checking the calculated total, completing a simulated payment, viewing the receipt, and confirming that recipe ingredients are deducted exactly once and the sale appears on the daily dashboard.

## 3. Scope boundary

**In scope:**

- Select menu items and quantities.
- Create an order with a unique ID.
- Calculate the total using stored menu prices.
- Complete a simulated payment and display the receipt.
- Deduct recipe ingredients once after successful payment.
- Show inventory and basic daily sales.
- Handle failed and duplicate payments safely.

**Out of scope:**

- Real payment gateways.
- Customer accounts and loyalty programs.
- Supplier management.
- Multiple branches and advanced reporting.

## 4. Current evidence

Issue #3 implementation and verification cover:

- One Latte deducts 250 ml milk and 18 g coffee beans.
- Failed payments leave inventory unchanged.
- Ten concurrent payment requests produce one success and nine safe duplicate errors.
- Repeated clicks and refresh/retry do not cause additional deductions in the tested scenarios.
- PostgreSQL records one payment and two ingredient movements per tested Latte order.

Five backend unit tests and the frontend production build also passed.

[Issue #3 test results and screenshots](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/issues/issue-03/README.md)

These checks verify payment/inventory behavior. The complete two-Latte receipt-to-dashboard demo still needs a recorded walkthrough.

## 5. One question for Week 5

Can another teammate run SmartServe from the setup instructions and reproduce the complete two-Latte sale, including the receipt, inventory changes, and daily sales update?

This will check whether the project is reproducible beyond the original development machine.

## 6. First action after the break

Have a second teammate follow the setup instructions and run the two-Latte demo:

1. Record starting inventory and daily sales.
2. Create an order for two Lattes.
3. Confirm the seeded total is ₩9,000.
4. Complete simulated payment and inspect the receipt.
5. Verify milk decreases by 500 ml and coffee beans by 36 g.
6. Verify daily sales increase by one paid order and ₩9,000.
7. Repeat payment for the same order and confirm no additional stock or sales changes.
8. Attach screenshots and expected-versus-actual results to the shared report.

The team will confirm the demo runner and reviewer before this walkthrough.

## 7. Checkpoint checklist

- [x] Rough sketches linked.
- [x] Midterm-demo sentence recorded.
- [x] Scope boundary stated.
- [x] One Week 5 question identified.
- [x] First action after the break defined.
- [x] Team reviews the checkpoint and confirms the demo runner.
- [ ] Checkpoint Issue linked from the shared Weekly Report.
