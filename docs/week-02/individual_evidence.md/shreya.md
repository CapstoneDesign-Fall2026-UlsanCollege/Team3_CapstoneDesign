# Individual Evidence Receipt

**Student:** Shreya  
**GitHub username:** @shrey776  
**Team:** Team 3  
**Week:** 2  
**Date:** 2026-09-16  

## Receipt 1 — Ingredient-Availability Investigation

- **What I did:** Investigated when SmartServe should check whether enough ingredients are available to complete an order.
- **Evidence link:** [Investigation #5 — When should SmartServe check ingredient availability?](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/5)
- **How I checked it:** Compared checking ingredient availability when a cashier adds an item against performing the final check immediately before payment. I used a two-order scenario in which only one latte could be prepared and reviewed PostgreSQL row-level locking documentation.
- **What I learned or changed:** I learned that an early stock check can become outdated if another order consumes the remaining ingredient before payment. SmartServe should show an early warning while the cashier creates the order but must perform the final stock check immediately before payment.

## Receipt 2 — Cashier-Layout Teammate Review

- **What I did:** Reviewed Shuzita’s two cashier-layout prototypes and provided feedback about which layout SmartServe should use for its MVP.
- **Evidence link:** [My prototype analysis on Investigation #6](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/6#issuecomment-5692952866)
- **How I checked it:** Compared the product-grid and searchable-list layouts using the same sample-order task. I checked product visibility, number of required actions, order-summary visibility, suitability for a small menu, and possible scaling problems.
- **What I learned or changed:** Both layouts required the same number of core actions, but the product grid made the small café menu easier to scan. I supported using the product-grid layout for the MVP while keeping search as a possible future improvement.

## Receipt 3 — Stock-Validation Requirements

- **What I did:** Helped define the expected system behaviour when an order does not have enough ingredient stock.
- **Evidence link:** [SmartServe Design Doc — Functional Requirements](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-02/design-doc-v1.md#9-functional-requirements)
- **How I checked it:** Used the ingredient-availability scenario to identify the required result: reject the simulated payment, keep the order open, identify the unavailable ingredient, leave inventory unchanged, and prevent negative stock.
- **What I learned or changed:** I learned that SmartServe needs both an early warning for usability and a final payment-time check for inventory accuracy. These requirements were added to the project’s order, payment, inventory, and cashier-interface design.

## Week 2 Reflection

My main contribution this week was investigating how SmartServe should respond when ingredient quantities change while multiple orders are being created.

The resulting decision is:

> SmartServe may show an early stock warning while an order is being created, but it must perform the final ingredient check immediately before payment.

My next step is to prepare and perform test cases for sufficient stock, insufficient stock, competing orders, and repeated payment attempts.
