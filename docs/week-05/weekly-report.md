# Weekly Report — Week 5

**Team:** Team 3
**Week:** Week 5
**Date:** 2026-10-03; cashier contribution update: 2026-10-07

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

## Individual receipts

| **Student**       | **What they did**                                                                                         | **Evidence link**                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lama Muskan**   | Worked on payment and inventory verification, including unit-price handling and repeated-payment testing. | [Issue #12](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12); [Issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3); [Payment test evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-04-chuseok/payment-test-evidence/README.md) |
| **Ualson Tamang** |                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                        |
| **Sherap Hyolmo** |                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                        |
| **Shuzita Majhi** |                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                        |
| **Shreya**        |                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                        |

## Verification result

### Exact-login contribution evidence — October 7 update

The display-name receipts above are preserved. The table below uses the professor's canonical GitHub logins. Unconfirmed work is not claimed as completed.

| GitHub login | Contribution / status | Evidence |
| --- | --- | --- |
| `daydevil80` | Added a separate Create order action to save an unpaid cashier order before payment. Added error/retry handling and a repeatable browser check for creation, refresh recovery, payment, and duplicate-payment safety. | [Cashier source](../../smartserve-pos/frontend/src/main.tsx), [current verification](cashier-evidence.md), [repeatable check](verify-cashier.cjs). Local changes; GitHub commit/PR link pending publication. |
| `Sammygit15` | Professor's October 5 review credits Issues #18 and #12. This row does not assert a new implementation or test run; member confirmation is pending. | [Issue #18](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18), [Issue #12](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12). |
| `ualsom` | Professor's review credits the order-state proposal. Current implementation/test contribution awaiting member confirmation. | [Issue #19](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/19). |
| `Shuzita` | Personal contribution and current evidence awaiting member update; checkpoint assignment alone is not completion proof. | [Issue #18](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18). |
| `shrey776` | Personal contribution and current evidence awaiting member update; checkpoint assignment alone is not completion proof. | [Issue #18](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18). |

### Demo and boundaries

On October 8, demonstrate selecting two seeded Caffè Lattes, creating an unpaid order for ₩9,000, refreshing to recover it, completing simulated cash payment, showing its receipt, and checking that milk decreases by 500 ml and coffee beans by 36 g exactly once. A duplicate payment must return HTTP 409 without another deduction or sale.

Order storage and recipe-stock accounting run in the real local API/PostgreSQL database. Payment acceptance, ingredients, stock quantities, and menu data are demo simulations/sample data. No money is charged and no physical stock is measured. Real payment integration, authentication/role enforcement, suppliers, and additional features are postponed. Independent teammate reproduction remains pending.

See the [Sprint 1 plan](sprint-1.md), [owned task sequence](work-checklist.md), and [setup/check instructions](cashier-evidence.md). Earlier verification statements below describe existing evidence; the current cashier run is recorded separately.

The current implementation stores the historical price in `OrderItem.unit_price`. Changing a menu item's current price therefore does not change the price saved for an existing order.

The payment test also confirms that a successful payment deducts inventory once. A repeated payment request for the same order returns **HTTP 409** and does not create another payment or inventory deduction.

## Current issue

The earlier local Windows setup needed additional Python dependencies. The October 7 cashier check successfully ran the backend and PostgreSQL through Docker in this development environment; see [current results](cashier-evidence.md). Independent teammate setup and member evidence confirmation remain pending.

## Next step

Continue Sprint 1 implementation, verify the complete flow in a clean environment, and add the final checkpoint evidence.
