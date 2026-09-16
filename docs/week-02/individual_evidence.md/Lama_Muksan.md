# Individual Evidence Receipt

Student: Sam
Team: TEAM 3
Week: WEEK 2
Date: 9/16/2026

Post 2–3 receipts per week when contribution tracking matters.

## Receipt 1

- **What I did:** Investigated how SmartServe should calculate the total price of an order before simulated payment, focusing on the relationship between menu prices, item quantities, order data, and payment amounts.
- **Evidence link:** [SmartServe Order Total Calculation Issue](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/4#issue-5426348197)
- **How I checked it:** Compared two possible approaches: calculating the total in the frontend and calculating the total from stored order data. I also planned a test using 2 Latte items at ₩4,000 each and 1 Americano at ₩3,000, followed by quantity changes, item removal, and simulated payment.
- **What I learned or changed:** I determined that the final payment amount should be based on stored order-item prices and quantities rather than relying only on a frontend-calculated value. This reduces the risk of the payment amount becoming inconsistent with the actual order data.

## Receipt 2

- **What I did:** Documented the order-total calculation decision and its effect on SmartServe's payment and sales-record flow.
- **Evidence link:** [SmartServe Order Total Calculation Issue](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/4#issue-5426348197)
- **How I checked it:** Evaluated how different quantities and menu prices affect the final order total and considered what should happen if a menu price changes after an order has been created.
- **What I learned or changed:** I recommended storing the unit price used at the time an order item is created. This means an existing order will keep its original price even if the menu price changes later. The final order amount can then be used consistently for simulated payment and sales records.

## Receipt 3, optional

- **What I did:** Connected the order-total calculation decision with the existing SmartServe payment and inventory workflow to identify how the final order state should be handled.
- **Evidence link:** [SmartServe Order Total Calculation Issue](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/4#issue-5426348197)
- **How I checked it:** Reviewed the payment flow together with the inventory deduction requirement, particularly the rule that inventory should only be deducted when an order reaches the `paid` status and should not be deducted more than once.
- **What I learned or changed:** I identified that the final order total and payment status should be handled consistently before the order is treated as completed. This helps keep payment, inventory deduction, and sales records synchronized and prevents incorrect processing.
