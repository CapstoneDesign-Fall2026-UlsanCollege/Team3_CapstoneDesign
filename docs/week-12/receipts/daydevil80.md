# Week 12 Individual Contribution Receipt — Sherap Hyolmo

**Team:** 3 — SmartServe POS

**GitHub login:** `daydevil80`

**Period:** November 19–25, 2026 (KST)

## Contribution and evidence

| Work I owned | Evidence |
|---|---|
| Published the shared QA report. Carried forward the Week 11 two-latte baseline and documented the Week 12 café, retail, and service results with expected and actual values. | [Week 11 baseline](../../week-11/live-two-latte-verification.md) · [Week 12 report commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/e89acd3ac1912446144cb93f1dba769ab721ea9f) |
| Confirmed the active Render revision and recorded the PowerShell HTTP preflight. Published the results under my GitHub login and linked them from the shared report. | [Render deployment](https://dashboard.render.com/web/srv-dbc8jbifngtc739d85q0/deploys/dep-dbvafnh42hec73b7u5u0) · [My preflight comment](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153696090) · [Report link commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/6c993ad76eeb159d3d8d84bc4d97f8c32132cd2b) |
| Coordinated the independent walkthrough by posting the three test cases, expected outcomes, and evidence required from a non-author teammate. | [My peer-test handoff](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153545486) |

## Technical evidence

| Check | Expected | Observed | Status |
|---|---|---|---|
| Local regression, November 23 KST, `bcd1f3a12c8891d3a669fdd9f4e96251f500d3de` | Simulated checkout keeps receipts, stock, and ticket status consistent. | Automated runners reported 46 backend tests, 27 café checks, and 37 business-flow checks passing. Café receipt #1 showed ₩9,000 and stock fell by 500 ml milk and 36 g beans. The duplicate payment returned HTTP 409 and left stock unchanged. | **Pass · Local SQLite** |
| Render preflight, November 25 at about 14:16 KST, `a9a35d2a8fe6425e05a4ac8d8feeb54048ba80fd` | The public service and sign-in page respond. Demo checkout requires an authenticated session. | `/health` and `/login` returned HTTP 200. `/menu`, `/inventory`, and `/owner/work` returned HTTP 401 and required sign-in with two-factor verification. | **Pass · Reachability. Blocked · Checkout.** |
| Non-author walkthrough | One teammate verifies café, retail, and service checkout on the deployed revision and posts their own results. | The request is posted in Issue #22. No independent Render result was recorded as of this receipt. | **Not tested · Independent Render** |

[Local café receipt](../evidence/screenshots/w12-local-cafe-receipt.png) · [Local retail receipt](../evidence/screenshots/w12-local-retail-receipt.png) · [Shared QA results](../weekly-report.md#week-12-results)

The original local runner outputs are attached here. The café output records the full tested SHA. The business output came from the same isolated archive of that revision.

- [Backend unittest output](../evidence/daydevil80/local-backend-unittest.txt)
- [Café browser/API results](../evidence/daydevil80/local-cafe-results.json)
- [Retail and service browser/API results](../evidence/daydevil80/local-business-results.json)

Ualson's November 24 [local retry result](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7124147327) separately confirmed HTTP 409 and unchanged stock and payment records. Their report used a local working tree with an additional regression test.

## What the checks establish

The two-latte test reconciles three records from the same order: a ₩9,000 receipt, a 500 ml milk deduction, and a 36 g bean deduction. The retry uses the same order ID and checks for zero additional stock movement. Render's HTTP 200 confirms service reachability. Checkout on that revision still needs evidence from an authenticated demo session.

My ownership for this slice covers QA reporting, deployment verification, and the handoff. The local outcomes came from the test runners, and the Render preflight came from read-only PowerShell requests. The peer walkthrough remains the P1 follow-up. As coordinator, I will link the tester's own Issue #22 comment and record the exact deployed SHA, receipt or ticket IDs, expected and actual values, and any required retest once the result is available.
