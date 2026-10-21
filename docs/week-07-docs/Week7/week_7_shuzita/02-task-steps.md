# Shuzita: failed-payment recovery test

Owner: Shuzita (Shuzita Majhi). Status: ready to perform, not yet run by the member.

This task checks a failure case and recovery for the frozen demo. Use separate sample data from 01-setup.md. Record your real result, even if it fails.

1. In the app, open Inventory and Dashboard. Record starting milk, beans, paid-order count and sales. Fresh seed: milk 5,000 ml, beans 1,200 g, zero paid orders/sales. Save 01-before-inventory.png and 02-before-sales.png in evidence.
2. Open http://localhost:8000/docs. Expand GET /menu, choose Try it out, Execute, and find the Caffè Latte ID. Record the actual ID; do not guess it.
3. Expand POST /orders. Submit this body, replacing LATTE_ID with the number from step 2:

```json
{"order_type":"takeaway","items":[{"menu_item_id":LATTE_ID,"quantity":2}]}
```

Expected: HTTP 201, status open, total 9000. Record the returned order ID. Save 03-open-order.png. Check inventory and sales: unchanged.
4. Expand POST /orders/{order_id}/pay, enter that order ID and submit:

```json
{"method":"card","result":"failed"}
```

Expected: HTTP 402. GET /orders/{order_id} should still show open. Refresh Inventory and Dashboard; stock and sales should be unchanged. Save 04-failed-payment.png and 05-after-failure.png. The current app has no dedicated failed-payment button, so this step uses the API docs deliberately.
5. Repeat POST /orders/{order_id}/pay with the same order ID:

```json
{"method":"cash","result":"paid"}
```

Expected: HTTP 200, status paid, total 9000. Save 06-successful-retry.png. Inspect the order in the app's Orders view or GET /orders/{order_id}. Record receipt name, quantity and price.
6. Refresh Inventory and Dashboard. Expected differences from the start: milk -500 ml, beans -36 g, paid orders +1, sales +9000. With fresh seed, milk is 4,500 ml and beans 1,164 g. Save 07-final-inventory.png and 08-final-sales.png.
7. Repeat the successful-payment request for the same ID. Expected: HTTP 409; no further stock/sales change. Save 09-duplicate-payment.png and record stock again.
8. Complete 03-result.md, receipt.md and 04-report-entry.md using your actual values and screenshot names. If a step fails, keep it failed and describe the first error. A blocker record is useful evidence, but does not make the full path pass.

Record whether you followed the written steps without live coaching. Using a prepared checklist is fine; say how the check was performed. Do not claim you wrote the implementation or authored the reference automated tests.
