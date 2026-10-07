## Week 5 additional receipt/inventory evidence — prepared for Shuzita

This evidence package contains a Codex-assisted automated check on the existing development PC. It is available for Shuzita to review; it does not claim that Shuzita personally ran the test or reproduced the app on another PC.

**Test date:** October 7, 2026, 14:56 Korea time
**Tested commit:** `a36f83a`
**Environment:** Windows, Edge browser automation, isolated Docker PostgreSQL/FastAPI/Vite demo
**Order:** #3 — takeaway; one Americano + one Milk Tea
**Payment:** simulated card

### Actual results

| Check | Expected | Actual | Result |
| --- | --- | --- | --- |
| Receipt items and total | Americano ₩3,500 + Milk Tea ₩5,000 = ₩8,500 | Same items, quantities and total | PASS |
| Create unpaid order | Status `open`; inventory unchanged | HTTP 201; `open`; no inventory deduction | PASS |
| Refresh recovery | Same order and takeaway selection | Order #3 recovered | PASS |
| Card payment | Same order becomes paid with receipt | Paid receipt #3; card | PASS |
| Coffee beans | Deduct 18 g | 1,164 → 1,146 g | PASS |
| Milk | Deduct 200 ml | 4,500 → 4,300 ml | PASS |
| Sugar | Deduct 20 g | 2,500 → 2,480 g | PASS |
| Tea leaves | Deduct 8 g | 700 → 692 g | PASS |
| Daily sales | Add one paid order and ₩8,500 | 1 → 2 paid orders; ₩9,000 → ₩17,500 | PASS |
| Duplicate payment | HTTP 409; stock/sales unchanged | HTTP 409; no additional deductions or sale | PASS |

### Evidence

Upload the `docs/week-05/shuzita-ben` folder, then link its README/results here, or attach its six screenshot files directly to this comment:

1. `01-inventory-before.png`
2. `02-sales-before.png`
3. `03-unpaid-mixed-order.png`
4. `04-paid-card-receipt.png`
5. `05-inventory-after.png`
6. `06-sales-after-repeat.png`

### Limits and next action

Payment is simulated; menu and stock are sample records. This is an additional mixed-order check, not the required independent two-Latte reproduction. Keep Issue #18's second-teammate checklist item unchecked.

Shuzita's personal review or reproduction is still pending. After reviewing or running the check, she should add her actual observations and link them in her Week 5 report row.
