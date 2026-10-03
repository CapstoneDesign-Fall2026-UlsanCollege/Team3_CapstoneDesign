# Weekly Report — Week 5

**Team:** Team 3
**Week:** Week 5
**Date:** 2026-10-03

## Main focus

This week focused on moving SmartServe from Sprint 0 decisions into Sprint 1 implementation and verifying the payment, inventory, and order-price behaviour.

## Work completed

* Continued the SmartServe MVP implementation using FastAPI and PostgreSQL.
* Verified that each order item stores the unit price used when the order was created.
* Added a test confirming that changing the current menu price does not change an existing order.
* Verified repeated payment handling and inventory deduction.
* Confirmed that a repeated payment request for the same order returns HTTP 409 without another inventory deduction.
* Continued preparing implementation and test evidence for the checkpoint.

## Evidence

| Item                            | Link                                                                                                                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Unit-price decision / Issue #12 | [Issue #12](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12)                                                                            |
| Payment & inventory Issue #3    | [Issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3)                                                                              |
| Two-Latte payment evidence      | [Payment test evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-04-chuseok/payment-test-evidence/README.md) |
| Two-Latte browser evidence      | [Two-Latte demo](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/evidence/two-latte-demo/README.md)              |
| Issue #3 verification evidence  | [Issue #3 verification](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-03/issues/issue-03/README.md)               |
| Backend implementation          | [`smartserve-pos/backend`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/smartserve-mvp/smartserve-pos/backend)                            |

## Verification result

The current implementation stores the historical price in `OrderItem.unit_price`. Changing a menu item's current price therefore does not change the price saved for an existing order.

The payment test also confirms that a successful payment deducts inventory once. A repeated payment request for the same order returns **HTTP 409** and does not create another payment or inventory deduction.

## Current issue

The local Windows environment required additional Python dependencies before the backend could run. PostgreSQL connectivity still needs to be confirmed locally.

## Next step

Continue Sprint 1 implementation, verify the complete flow in a clean environment, and add the final checkpoint evidence.
