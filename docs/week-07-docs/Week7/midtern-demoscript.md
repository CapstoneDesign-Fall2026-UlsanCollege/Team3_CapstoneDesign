
# Midterm Demo Script

**Team:** Team 3  
**Project:** SmartServe POS  
**Week:** 7–8

## Opening

**October 21 update:** [Current fixes/test evidence](evidence/2026-10-21/README.md) · [Shared report](weekly-report.md) · [Midterm Prep #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21). Automated checks pass; independent browser testing and the timed spoken rehearsal remain pending.

## Four-minute speaking plan

These are planned times, not a completed rehearsal. Confirm speakers as a team. `daydevil80` prepares the fix/results segment; the other assignments are still open.

| Time | Action and words to cover |
|---|---|
| 0:00–0:30 | “SmartServe is for café staff who need orders and ingredient stock to stay in sync. We'll show one sale from start to finish.” State that payments are simulated. |
| 0:30–1:10 | Show starting inventory and daily sales in a separate demo database. Select two Caffè Lattes and point to the ₩9,000 total. |
| 1:10–2:00 | Show a simulated failed payment: stock stays unchanged. Retry successfully, then show the paid receipt. |
| 2:00–2:45 | Show milk −500 ml, beans −36 g, and daily sales +₩9,000. Use the before/after values rather than assuming the store starts at zero. |
| 2:45–3:30 | daydevil80: “Last week an 18 g recipe edit saved as 18 kg, and menu renaming changed old receipt names. The edit now converts units, and new orders save their original item names.” Point to current expected/actual results. |
| 3:30–4:00 | State the old-name migration limit, simulated payment boundary and pending independent check if still incomplete. Close with the next action. |

Use [retest-and-rehearsal.md](retest-and-rehearsal.md) to record the actual start state, tester, duration and proof. If the app fails, show the dated recorded evidence and clearly say the live demo stopped. The recipe conversion is supporting proof, not an extra live feature tour.

- **Project name:** SmartServe POS
- **Target users:** Café staff and café owners who need to manage customer orders, payments, receipts, and ingredient inventory.
- **Problem:** Managing orders, payments, and ingredient stock separately can make café operations difficult and time-consuming.
- **Goal:** Demonstrate how SmartServe connects order creation, simulated payment, receipt generation, inventory deduction, and sales tracking in one system.

## Demo Path — Frozen Midterm Scope

1. **Application Opening:** Open SmartServe POS and introduce the project's purpose.
2. **Menu Selection:** Display the available menu items and select two Latte items.
3. **Order Summary:** Show the selected quantity and confirm the total price of ₩9,000.
4. **Payment:** Demonstrate the simulated payment process.
5. **Receipt:** Display the generated receipt after successful payment.
6. **Inventory:** Show the ingredient quantities deducted from inventory: 500 ml of milk and 36 g of coffee beans.
7. **Sales Dashboard:** Open the dashboard and show the updated daily sales information.

**Demo boundary:** The timed demonstration focuses on the order-to-payment-to-inventory workflow. Other features, such as menu management, inventory management, and owner dashboard functions, can be introduced separately if time permits.

## What Works Now

### Core Midterm Demo

- **Order Management:** Staff can select menu items and quantities to create customer orders.
- **Order Total:** The system calculates the total price based on selected items and quantities.
- **Simulated Payment:** The system supports simulated cash, card, and QR payment workflows.
- **Receipt Generation:** A receipt is generated after successful payment.
- **Inventory Deduction:** Ingredient quantities are deducted following successful payment.
- **Duplicate Payment Protection:** The system prevents duplicate payment requests from deducting inventory again.
- **Sales Dashboard:** Paid orders contribute to the sales information displayed on the dashboard.
- **Database:** PostgreSQL stores order, payment, and inventory information.

### Supporting Features

- **Menu Management:** Menu items and their information can be managed.
- **Ingredient Management:** Ingredient information and stock quantities can be maintained.
- **Inventory Management:** The system tracks ingredient quantities and inventory movements.
- **Owner Dashboard:** The dashboard provides an overview of sales and business information.
- **Order Management:** The system supports managing existing orders.

## Current Scope and Limitations

- **Payment Integration:** Payments are simulated. Real payment gateway integration is outside the current midterm scope.
- **Authentication and Authorization:** Full user authentication and role-based access control are not yet enforced.
- **Deployment:** The current focus is on the project development and demonstration environment.
- **External Services:** Live payment processing and other external business integrations are outside the current MVP scope.

## Failure and Fallback

- **Payment interruption:** Explain the simulated payment workflow and demonstrate it again from a fresh order.
- **Inventory display issue:** Show the relevant ingredient records and inventory movement information.
- **Application interruption:** Restart the local application using the documented setup instructions.
- **If the live demo cannot continue:** Use prepared screenshots or recorded evidence, clearly identifying them as recorded evidence rather than a live demonstration.

## Evidence Links

- **Repository:** [SmartServe POS – Team 3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)
- **Project Setup:** [SmartServe README](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/README.md)
- **Main Repository README:** [README](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/README.md)
- **Payment and Inventory Implementation:** [Issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3)
- **Owner and Menu Management:** [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20)
- **Technical Verification:** [Week 6 Automated Check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/automated-check.md)
- **Test Plan:** [Week 6 Test Plan](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/test-plan.md)
- **Demo Instructions:** [Week 6 Setup and Demo](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/setup-and-demo.md)
- **Recorded Evidence:** [October 14 Evidence Package](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-06/evidence/2026-10-14)
- **Sprint Quality Checks:** [Week 7 Sprint Quality Quick Checks](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-07-docs/Week7/sprint-quality-quick-checks.md)

## Contribution Summary

| Student | GitHub Username | Contribution | Evidence |
|---|---|---|---|
| Lama Muskan | `Sammygit15` | Reviewed the SmartServe backend implementation and existing test evidence, examined the payment and inventory workflow, documented technical progress, and prepared Week 7 project documentation. | [GitHub Repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign) · [Week 6 Automated Check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/automated-check.md) · [Week 6 Test Plan](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/test-plan.md) · [Week 6 Demo Instructions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-06/setup-and-demo.md) · [Issue #3 – Payment and Inventory](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3) |
| Sherap Hyolmo | `daydevil80` | Fixed recipe-unit editing and new-order receipt snapshots; added regression tests and current verification notes. Prepares the fix/results segment. | [Receipt](receipts/daydevil80.md) · [Current results](evidence/2026-10-21/README.md) |
| Ualson Tamang | `ualsom` |  |  |
| Shuzita Majhi | `Shuzita` |  |  |
| Shreya | `shrey776` |  |  |

## Next Steps After Midterm

- Continue improving the overall user interface and demonstration experience.
- Continue testing the main order, payment, and inventory workflow.
- Improve the system based on testing feedback.
- Prepare the final presentation and demonstration.
- Prioritize future improvements based on project requirements and professor feedback.
