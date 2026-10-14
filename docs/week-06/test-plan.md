# Week 6 test steps and expected results

**Team:** 3 — SmartServe POS  
**Implementation owner:** `daydevil80`  
**Plan date:** 2026-10-14, Korea time  
**Related issue:** [#20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20)  
**Checkout:** `f4e8a6d3c185d3b9c9090d6daaf875080902cf1a`  
**Application source commit:** [df2f357](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/df2f357b0246fd71b76d7be8a7fa03d29dee68fe)

The expected results below were written before the October 14 check. The checkout adds Week 6 documents after df2f357 but has the same application source. Use a fresh, separate sample database. Do not reset the shared store.

## Starting point

- Milk: 5,000 ml; reorder level 1,000 ml.
- Coffee beans: 1,200 g; reorder level 250 g.
- Caffè Latte: ₩4,500; recipe 250 ml milk and 18 g coffee beans.
- Americano: ₩3,500; recipe 18 g coffee beans.
- No orders or sales in this sample database.
- Cashier screen open. Use Refresh availability after editing inventory or recipes.

## Steps

| Step | Action | Expected result |
|---|---|---|
| 1 | Record inventory and today's Korea-time sales | Starting quantities match the values above; sales and paid-order count are zero |
| 2 | Add two lattes and select Create order | One open order with a unique ID and total ₩9,000; no stock deducted |
| 3 | Reload the same browser tab | Same saved order and ₩9,000 total return |
| 4 | Request a failed simulated payment for this order through the API | HTTP 402; order stays open; stock and sales unchanged |
| 5 | Select Pay cash | Order becomes paid; receipt total ₩9,000; milk 4,500 ml and beans 1,164 g |
| 6 | Repeat the payment request for the same ID | HTTP 409; no extra payment, movement, stock deduction, or sale |
| 7 | Edit Coffee beans from g to kg and save the converted form | Stock 1.164 kg, reorder level 0.25 kg, latte/americano recipe 0.018 kg per serving; existing movement 0.036 kg for two lattes |
| 8 | Rename Caffè Latte to Caffè Latte test, change price to ₩6,000, keep recipe amounts unchanged, and save | New menu details saved; ingredient stock unchanged |
| 9 | Reopen the earlier paid receipt from Orders | It still shows its original ₩9,000 total, ₩4,500 unit price, and original product name Caffè Latte |
| 10 | Refresh availability, buy one renamed latte, and pay by card | New receipt total ₩6,000; beans 1.146 kg and milk 4,250 ml; total daily sales ₩15,000 from two paid orders |
| 11 | Edit Americano recipe: choose g and enter 18 while beans are stored in kg; save | Recipe is stored/displayed as 0.018 kg, stock is unchanged, and Americano remains available |
| 12 | Refresh Cashier availability | Americano is selectable because 1.146 kg is enough for a serving needing 0.018 kg |

Use the local API docs for step 4 and step 6. For a failed payment, send `{"method":"cash","result":"failed"}` to `POST /orders/{id}/pay`. For the duplicate, send `{"method":"cash"}` again for the paid order.

## Independent teammate test

A teammate other than daydevil80 should start from the written instructions, without coaching, and record the exact login, date, first confusing or failing step, actual values, and proof. A failed step stays incomplete. The October 14 scripted run does not fill this role.

Use [tested-by-note.md](tested-by-note.md) for the teammate result. The developer-run results will be linked separately in [automated-check.md](automated-check.md).
