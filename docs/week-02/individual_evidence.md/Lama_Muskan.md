# Individual Evidence Receipt

Student: LAMA MUSKAN
Team: TEAM 3
Week: WEEK 2
Date: 9/16/2026

Post 2–3 receipts per week when contribution tracking matters.

## Receipt 1

- **What I did:** Investigated how SmartServe should calculate the total price of an order before simulated payment, focusing on the relationship between menu prices, item quantities, order data, and payment amounts.
- **Evidence link:** [SmartServe Order Total Calculation Issue](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/4#issue-5426348197)
- **How I checked it:** Compared two possible approaches: calculating the total in the frontend and calculating the total from stored order data. I considered how each approach would affect consistency between the order information and simulated payment.
- **What I learned or changed:** I recommended calculating the final order total from stored order data because this keeps the payment amount consistent with the stored order information and reduces the possibility of inconsistencies between the frontend and the actual order data.

## Receipt 2

* **What I did:** Reviewed the payment and inventory protection approach and identified the remaining testing needed to verify that inventory is not deducted more than once.
* **Evidence link:** [SmartServePOS Industry Standards Issue #17](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/17)
* **How I checked it:** Reviewed the current approach using payment status checks, database transactions, row locks, and unique database constraints. I also identified repeated payment and insufficient-stock scenarios that should be tested.
* **What I learned or changed:** I confirmed that the current implementation does not use an `inventory_deducted` field. Instead, duplicate protection is handled through the paid-status check, transaction handling, row locking, and database constraints. The remaining verification should be recorded through repeatable tests before claiming the protection has been fully demonstrated.

## Receipt 3, optional

- **What I did:** Investigated how SmartServe should handle menu-price changes after an order has been created so that historical orders and sales records remain accurate.
- **Evidence link:** [SmartServe Order Total Calculation Issue](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/4#issue-5426348197)
- **How I checked it:** Considered a scenario where the Latte price changes from ₩4,000 to ₩4,500 after an order has already been created. I evaluated whether the existing order should continue using the original price.
- **What I learned or changed:** I decided that SmartServe should store the unit price used when the order item is created. This ensures that later menu-price changes do not modify existing orders or historical sales records. The final order amount can then be used consistently for payment and sales records.
