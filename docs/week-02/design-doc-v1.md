# Design Doc v1

**Team:** Team 3  
**Project name:** SmartServe POS  
**Last updated:** 2026-09-10

## 1. Project purpose

SmartServe POS is a web application for small cafes and restaurants. It combines menu management, order processing, simulated payments, ingredient inventory, receipts, and daily sales records in one workflow.

Small food businesses may record orders, stock, expenses, and sales in separate places. This makes it difficult to know which ingredients remain available, how much was sold during the day, and whether a completed order was recorded correctly.

## 2. Target users

| Role | Main responsibilities |
|---|---|
| Administrator or manager | Manage menu items, recipes, ingredients, employees, and view sales records. |
| Cashier | Create customer orders, review totals, process simulated payments, and provide receipts. |

## 3. Smallest useful version

The smallest useful version is a web application that supports this complete workflow:

1. An administrator creates an ingredient, a recipe, and a menu item.
2. A cashier selects one or more menu items and creates an order.
3. The system calculates the order total and accepts a simulated payment.
4. The system marks the order as completed and generates a receipt.
5. The system deducts the recipe quantities from inventory exactly once.
6. The system records the sale and displays it in a daily sales view.

### Rough user flow

`Start -> Configure Menu and Ingredients -> Create Order -> Complete Mock Payment -> Generate Receipt and Update Inventory -> Sale Visible on Dashboard`

**Evidence / sketch link:** To be added after the first wireframe is completed.

## 4. In scope

- Administrator or manager view for ingredients, recipes, and menu items.
- Cashier view for creating orders and reviewing totals.
- Simulated cash or card payment.
- Receipt generation for completed orders.
- Inventory deduction based on menu item recipes.
- Daily sales and low-stock dashboard.
- Audit records for inventory deductions.

## 5. Out of scope

- Real payment gateway integration.
- Tax reporting and accounting integration.
- Supplier purchasing and delivery management.
- Multiple store branches.
- Customer loyalty programs.
- Mobile applications.
- Advanced forecasting or AI recommendations.

## 6. Midterm demo sentence

Our midterm demo will show:

> A cashier creating a two-latte order, completing a simulated payment, generating a receipt, and verifying that the correct coffee and milk quantities were deducted from inventory and added to the daily sales dashboard.

## 7. Final demo sentence

Our final demo will prove:

> SmartServe POS can complete a cafe sale while keeping the order, payment, receipt, inventory, and daily sales records synchronized and preventing duplicate stock deductions.

## 8. MVP features

| Feature | Required for MVP? | Primary implementation owner | Research, design, or testing support | Issue link |
|---|---|---|---|---|
| Ingredient and recipe management | Yes | Lama Muskan | Ualson Tamang: requirements research | To be added |
| Menu item management | Yes | Sherap Hyolmo | Shuzita Majhi: interface design and documentation | To be added |
| Cashier order creation | Yes | Lama Muskan | Shuzita Majhi: cashier-view design; Ualson Tamang: workflow research | To be added |
| Simulated payment | Yes | Sherap Hyolmo | Ualson Tamang: payment-flow research | To be added |
| Receipt generation | Yes | Sherap Hyolmo | Shuzita Majhi: receipt layout and documentation | To be added |
| Inventory deduction and audit record | Yes | Lama Muskan | Shreya: test-case preparation and verification | To be added |
| Sales and low-stock dashboard | Yes | Sherap Hyolmo | Shuzita Majhi: dashboard design; Ualson Tamang: reporting requirements research | To be added |
| Manual test cases and verification | Yes | Shreya | Lama Muskan and Sherap Hyolmo: fix implementation defects | To be added |

## 9. Functional requirements

### Menu and recipes

- Create, view, update, and deactivate menu items.
- Define the ingredients and quantities required for each menu item.
- Show whether the available stock is sufficient for an order.

### Inventory

- Create and update ingredients with a unit and current quantity.
- Display current stock and low-stock status.
- Record each stock deduction with its related completed order.
- Prevent an order from completing when required stock is unavailable.

### Orders and payments

- Add menu items and quantities to an order.
- Calculate subtotal and total before payment.
- Support a simulated cash or card payment.
- Use clear order states such as `Draft`, `Paid`, `Completed`, and `Cancelled`.
- Prevent duplicate completion of the same order.

### Receipts and sales

- Generate a receipt containing the order number, items, quantities, total, payment status, and date.
- Record completed sales with enough information for a daily total.
- Display the number of completed orders, total sales, and low-stock ingredients on a dashboard.

## 10. Non-functional requirements

- The interface should be simple enough for a cashier to use during a busy shift.
- Inventory and sales updates should be consistent after a successful payment.
- The system should show validation errors instead of silently accepting incomplete data.
- Demonstration data must be clearly identifiable and must not represent real customer payment information.
- The application should work in a current desktop browser at minimum.

## 11. Core data model

| Entity | Important fields | Relationship |
|---|---|---|
| User | id, name, role | Creates or manages orders and records. |
| Ingredient | id, name, unit, quantity, reorder level | Used by one or more recipes. |
| RecipeItem | recipe id, ingredient id, quantity required | Connects a menu item to an ingredient. |
| MenuItem | id, name, price, active status | Has one recipe and can appear in order lines. |
| Order | id, status, subtotal, total, created time, completed time | Contains order lines and one payment record. |
| OrderLine | order id, menu item id, quantity, unit price | Stores the items purchased. |
| Payment | id, order id, method, amount, status, paid time | Records the simulated payment. |
| InventoryTransaction | id, ingredient id, order id, quantity change, time | Audits stock deductions and adjustments. |

## 12. Main workflow

```text
Cashier selects items
	|
	v
System checks recipe stock and calculates total
	|
	+--> Insufficient stock: show error and keep order open
	|
	v
Cashier confirms simulated payment
	|
	v
System completes order in one controlled operation
	|
	+--> Save payment and completed order
	+--> Deduct each recipe ingredient once
	+--> Save inventory transactions
	+--> Record sale and generate receipt
```

## 13. Risks and unknowns

| Risk / unknown | Why it matters | Plan |
|---|---|---|
| Duplicate or missing inventory deductions | Stock and sales records could become inaccurate after payment. | Check order status before completion, allow only one `Paid` to `Completed` transition, and link every deduction to the order ID. |
| Insufficient stock during checkout | A cashier could accept an order that cannot be prepared. | Check recipe quantities before payment and keep the order open when stock is insufficient. |
| Scope becoming too large | Authentication and advanced management features could delay the core demo. | Prioritize the order-to-inventory workflow and use seeded demonstration roles if necessary. |
| Technical stack not yet confirmed | Implementation cannot begin efficiently without a shared setup. | Agree on the framework and database before creating implementation Issues. |

## 14. Main risk mitigation detail

**Initial mitigation:** The order-completion operation will check the order status before changing inventory. Only a transition from `Paid` to `Completed` may create inventory deductions. Each deduction will reference the order ID, and the dashboard will expose the resulting stock and sales values for manual verification.

## 15. Midterm demonstration scenario

The team will configure a latte menu item using coffee beans and milk. A cashier will create an order for two lattes, complete a simulated payment, show the receipt, and then compare the before-and-after inventory quantities. The sales dashboard will show the completed order and updated daily total.

## 16. Evidence links

- Planning Issue: To be added.
- Weekly Report: [Week 2 Weekly Report](weekly-report.md)
- Idea Selection: [Week 2 Idea Selection Table](idea-selection-table.md)
- Wireframe or prototype proof: To be added.

## 17. Open questions for team review

- Which web framework and database will the team use?
- Will the first version include login screens, or will it use seeded demo roles?
- What currency and sample prices should be used in the demonstration?
- Which team member will own the order-completion and inventory transaction implementation?
