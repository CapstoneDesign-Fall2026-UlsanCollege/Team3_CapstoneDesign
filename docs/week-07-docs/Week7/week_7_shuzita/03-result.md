# Week 7 result — Payment failure and recovery

Prepared for Shuzita Majhi (`Shuzita`). Browser execution and file preparation: Codex automation at daydevil80's request. This records completed assisted verification; it does not attest to the member's personal execution or review.

Team 3 — SmartServe POS. Run timestamp: 2026-10-21T15:37:01.112602+09:00.
Application commit: `0d5fecdf827deb12b7d4d560e392bfb06d868591`.
Environment: fresh temporary SQLite database, FastAPI, built React frontend, Chromium, 1440 × 1080 desktop viewport. Loopback proxy adapted the frontend API address; application business logic was unchanged. Shared store data was not touched.

## Recorded results

| Check | Expected | Actual | Evidence |
|---|---|---|---|
| Start | Milk 5,000 ml; beans 1,200 g; sales zero | Same | [Inventory](evidence/agent-run-2026-10-21/01-before-inventory.png), [empty sales](evidence/agent-run-2026-10-21/02-before-sales-empty-state.png) |
| Two-latte order | Open; total ₩9,000; no stock deduction | HTTP 201; open; ₩9,000; stock unchanged | [Cart](evidence/agent-run-2026-10-21/03-two-latte-cart.png), [saved order](evidence/agent-run-2026-10-21/04-unpaid-order.png) |
| Failed simulated card payment | HTTP 402; order remains open; stock/sales unchanged | Same | [Failure message](evidence/agent-run-2026-10-21/05-failed-payment-message.png), [stock](evidence/agent-run-2026-10-21/06-stock-after-failure.png), [sales](evidence/agent-run-2026-10-21/07-sales-after-failure.png) |
| Successful cash payment | HTTP 200; paid receipt; ₩9,000 | Same | [Receipt](evidence/agent-run-2026-10-21/08-paid-receipt.png) |
| Final stock | Milk 4,500 ml; beans 1,164 g | Same: −500 ml milk and −36 g beans | [Inventory](evidence/agent-run-2026-10-21/09-final-inventory.png) |
| Final sales | One paid order; ₩9,000 | Same | [Dashboard](evidence/agent-run-2026-10-21/10-final-sales-dashboard.png) |
| Duplicate payment | HTTP 409; no further stock or sales changes | Same | [Raw HTTP checks](evidence/agent-run-2026-10-21/results.json) |
| Receipt history | Paid order and original receipt accessible | Same | [Orders](evidence/agent-run-2026-10-21/11-paid-order-history.png), [reopened receipt](evidence/agent-run-2026-10-21/12-reopened-receipt.png) |
| Uncaught browser exceptions | None | None | [Raw checks](evidence/agent-run-2026-10-21/results.json) |

Total: **16 automated checks passed**.

[Recording](evidence/agent-run-2026-10-21/automated-browser-walkthrough.webm) · [Screenshot gallery](evidence/agent-run-2026-10-21/SCREENSHOTS.md) · [Generated verification report](evidence/agent-run-2026-10-21/http-browser-report.html). The generated report is labelled as a report; the other screenshots capture the actual app.

## Failure trigger and finding

Automation changed the outgoing simulated card-payment body to `{"method":"card","result":"failed"}`. The real backend returned 402 and the app displayed “Simulated payment failed. Inventory is unchanged; you can retry this order.” The successful retry paid that same saved order. The app has no separate failed-payment button, so the failure trigger must be explained as API-driven.

The observed behavior supports the recovery rule: stock and sales change only when payment succeeds. Duplicate-payment protection prevented a second deduction. No application failure was found in this sequence.

## Limits and next action

This run uses SQLite; it does not establish PostgreSQL concurrency or production readiness. Payments are simulated. Original names of pre-migration orders cannot be reconstructed. The member should review this assisted evidence and explain the result before presenting it. A non-author human run and the team's real timed spoken rehearsal remain separate course requirements.
