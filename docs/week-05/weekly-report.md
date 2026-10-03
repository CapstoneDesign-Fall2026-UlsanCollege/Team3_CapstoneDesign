
# Weekly Report — Week 5

**Team:** Team 3
**Week:** Week 5
**Date:** 2026-10-03

## Main focus

This week focused on moving SmartServe from Sprint 0 decisions into a working Sprint 1 implementation path, while verifying the payment and inventory behaviour already implemented.

### Completed / worked on

* Continued the SmartServe MVP implementation using the FastAPI + PostgreSQL architecture.
* Verified that order items store the **unit price used when the order was created**.
* Added/verified a test showing that changing the current menu price does not change an existing order's saved price.
* Verified the payment and inventory flow, including repeated payment attempts for the same order.
* Confirmed that a repeated payment request returns **HTTP 409** and does not deduct inventory or create another payment.
* Prepared evidence for the Sprint 1 checkpoint and continued organizing project documentation.

## Key evidence

| Item                             | Evidence                                  |
| -------------------------------- | ----------------------------------------- |
| Order unit-price decision        | Issue #12                                 |
| Payment / inventory verification | Issue #3 and Week 4 payment-test evidence |
| Backend implementation           | `smartserve-pos/backend`                  |
| Order-item model                 | `app/models.py`                           |
| Order creation logic             | `app/main.py`                             |
| Verification tests               | `test_issue3.py`                          |

## Verification result

The current implementation preserves the historical order price through `OrderItem.unit_price`.

For the payment flow, a successful payment changes the order to `paid` and deducts the required inventory once. A second payment request for the same order is rejected with **HTTP 409**, without another inventory deduction or payment record.

## Issue / risk

The local Windows environment required additional Python dependencies before the backend could be started. PostgreSQL connectivity also still needs to be confirmed in the local environment.

## Next step

Continue Sprint 1 implementation and evidence collection, then verify the complete SmartServe flow in a clean environment before the next checkpoint.
