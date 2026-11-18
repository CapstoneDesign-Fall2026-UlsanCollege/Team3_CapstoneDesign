# Week 11 live two-latte verification — Issue #22

Coordinator: `daydevil80`. Non-author tester: awaiting confirmation in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22).

## November 18 preflight

- **Target:** [SmartServe POS on Render](https://smartserve-pos-ycbj.onrender.com/), from the existing [demo handoff](../week-09/verification-handoff.md).
- **Environment:** Codex-assisted Windows command-line requests to the public Render URL. A GET to `/api/health` timed out at 25 seconds and a GET to `/` timed out at 15 seconds. Both returned zero HTTP response bytes. A subsequent GET to the homepage with a 60-second limit returned HTTP 200 in 1.353 seconds. Homepage reachability passed on retry.
- **Deployment confirmed:** Render lists [deploy `dep-dbqmcnijnfac73bnhv5g`](https://dashboard.render.com/web/srv-dbc8jbifngtc739d85q0/deploys/dep-dbqmcnijnfac73bnhv5g) as live on `eb2c88ebab8d98ed68932c4dee800c1605616269`. GET `/health` returned HTTP 200 with `{"status":"ok"}`.
- **Live sale:** Blocked before order creation. GET `/menu` returned HTTP 401 with “Sign in and complete two-factor verification.” An authenticated session for the approved demo café is needed. No live order, payment, receipt, or stock change was observed. The independent check is still pending.
- **Freeze:** Keep the promised demo scope fixed. Hold build sign-off pending independent live verification and team approval. The [isolated retry regression](../../smartserve-pos/backend/test_week11_ualsom.py) and [PR CI run #9](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43902224014) document separate environments.

## Non-author run

1. Confirm the current Render revision from Deploys and record the full SHA, browser/device, and time in KST. Use an approved demo café workspace with simulated payments. Ask for access privately.
2. Record starting milk (ml), beans (g), and the recipe and price. The expected recipe is 250 ml milk and 18 g beans per latte at ₩4,500. If the recipe or price differs, capture the discrepancy before running payment.
3. Use the same order ID throughout the following checks. The [existing handoff](../week-09/verification-handoff.md) describes the simulated payment API steps.

| Step | Expected | Actual on Render |
|---|---|---|
| Create two lattes | One open order for ₩9,000. Stock unchanged. | Not run |
| Simulate a failed card payment | HTTP 402, same order still open, no stock deduction. | Not run |
| Retry the same order with successful cash payment | Paid receipt for two lattes and ₩9,000. Stock drops exactly 500 ml and 36 g. For example, 5,000 ml and 1,200 g would become 4,500 ml and 1,164 g. | Not run |
| Repeat the paid request | HTTP 409 and no further deduction. | Not run |

Post the result in Issue #22 under the tester's own login. Include pass, fail, or blocked, the order ID, actual before/after stock, payment and receipt evidence, and the tested revision. If Render still does not load, record the client, time, and error. `daydevil80` owns confirming the URL, revision, and workspace access before the next attempt, then recording the outcome and team's decision in the shared report.
