# Issue #22 — independent Render result

Coordinator: @daydevil80. Tester: pending confirmation by a teammate who did not author the fix. The tester should post the completed record under their own GitHub login in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22).

Use the [frozen Week 9 handoff](../week-09/verification-handoff.md) for the full scenario. Confirm the demo URL and deployed commit with the coordinator before starting. Use approved demo data and record the baseline without resetting the shared database.

- Tester GitHub login and non-author confirmation:
- Date/time KST, browser, exact demo URL and database:
- Deployed application SHA and how it was verified:
- Latte unit price, recipe quantities and units:
- Order ID and evidence links:
- Overall result, help received and any interfering demo activity:

| Step | Expected with the original seed | Actual / evidence |
|---|---|---|
| Baseline | Milk 5,000 ml, beans 1,200 g, latte ₩4,500 with 250 ml milk and 18 g beans per item | Pending |
| Create order and refresh | Same open order ID, quantity 2, ₩9,000, stock unchanged | Pending |
| Simulated failed card payment | HTTP 402, same open order, stock unchanged | Pending |
| Retry with cash | Same order paid, receipt quantity 2 at ₩4,500 each, milk 4,500 ml, beans 1,164 g | Pending |
| Duplicate payment | HTTP 409, stock and paid-order count unchanged | Pending |

For a different baseline, record the expected absolute values before running the test. The original recipe deducts 500 ml milk and 36 g beans once. Record paid-order count and sales before and after, and complete the remaining frozen handoff checks in the same record. Keep credentials and session tokens out of evidence.
