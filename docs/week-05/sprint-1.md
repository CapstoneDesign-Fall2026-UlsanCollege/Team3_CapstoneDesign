
# Sprint 1 Implementation Path

## Selected Path

Our Sprint 1 implementation path is:

Cashier Menu → Create Order → Calculate Total → Simulate Payment → Receipt → Inventory Deduction → Sales Dashboard

## Goal

Build one small end-to-end SmartServe POS user path that can be demonstrated at the next checkpoint.

## Success Condition

A cashier can select menu items and quantities, create an order, see the total calculated from stored menu prices, complete a simulated payment, receive a paid order/receipt, verify that the required recipe ingredients are deducted from inventory exactly once, and confirm that the paid order appears on the sales dashboard.

## Data

For Sprint 1, we will use the existing seeded SmartServe menu, recipe, and inventory data for testing. A small set of menu items such as Caffè Latte will be used to verify the complete order-to-payment-to-inventory flow.

## Out of Scope

* Real payment gateway integration
* Customer accounts or loyalty features
* Advanced inventory or supplier management
* Notifications or chat
* Full production-ready UI design
* Advanced reporting

## Evidence

### Week 5 demo scope and proof

For October 8, the bounded path is **select two Caffè Lattes → create unpaid order → simulate cash payment → show receipt**. Inventory and sales checks prove the transaction boundary; owner management and other menu features are postponed from this demo.

The existing stack is React/TypeScript/Vite + FastAPI/SQLAlchemy + PostgreSQL, run with Docker Compose. Current database status and runnable steps are recorded in [cashier evidence](cashier-evidence.md). Payment is simulated; ingredient and menu records are sample data, while order persistence and stock-ledger updates run in the local database.

The implementation uses `open → paid`, with inventory deduction committed in the same payment transaction. `open` is the current unpaid state corresponding to the proposed pending stage in Issue #19. Inventory deduction is represented by ledger records, rather than a separate order status. Cancellation applies only to an open order.

Proof: save two Lattes at ₩9,000 with no payment/stock changes; reload and recover the same order; pay and show the saved receipt; verify 500 ml milk and 36 g beans deducted; repeat payment and observe HTTP 409 with unchanged inventory/sales. See [repeatable browser check](verify-cashier.cjs) and [shared Week 5 report](weekly-report.md).

The [four-task sequence](work-checklist.md#week-5-owned-implementation-and-test-sequence) records Definitions of Done and proposed review owners. If the full path is blocked, demonstrate unpaid order creation and recovery, and report payment as blocked with the exact failing check. Do not label that fallback as a completed payment transaction.

* Candidate Vertical Slice: [Candidate Vertical Slice](../week-03/candidate-vertical-slice.md)
* Weekly Report: [Week 3 Weekly Report](../week-03/weekly-report.md)
* Architecture Sketch: [Architecture Sketch](../week-03/architecture-sketch.md)
* Stack Comparison: [Week 3 Stack Comparison](../week-03/tech-stack-comparison.md)
* Wireframe Notes: [Wireframe Notes](../week-03/wireframe-notes.md)
* Payment and Inventory Verification: [Issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3)
* Sprint 0 Report: [Sprint 0 Report](../week-03/sprint-0-report.md)
