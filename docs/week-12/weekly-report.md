# Week 12 Weekly Report — SmartServe POS QA and Regression

**Team 3 · November 19–25, 2026 (KST)**

**Status as of November 25:** Local checkout QA passed on the reviewed commit. The active Render revision is confirmed. Independent Render checkout and team sign-off remain pending.

**GitHub baseline reviewed:** `main` at [`bcd1f3a`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/bcd1f3a12c8891d3a669fdd9f4e96251f500d3de).

## Goal

Verify café, retail, and service sales on the final-demo build using simulated payments. Compare each transaction with its receipt, stock movement where applicable, and final work status. Record defects, fixes, and retests against the revision that was actually tested. [Final demo roadmap](../week-10/final-roadmap.md)

## Evidence carried forward

| GitHub evidence | Result recorded | Week 12 follow-up |
|---|---|---|
| [Week 11 Render verification](../week-11/live-two-latte-verification.md) | A developer-coordinated browser run on `eb2c88e` recorded café order #1 at ₩9,000, milk 5,000 → 4,500 ml, and beans 1,000 → 964 g. | Confirm the deployed SHA and get a teammate who did not author the relevant change to repeat the check. |
| [Week 11 PR CI #9](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43902224014) | Ualson's isolated retry regression recorded HTTP 409 and a single stock deduction. | Re-run the regression on the Week 12 candidate. The Week 11 Render UI run left duplicate payment untested. |
| [Business workflow scenarios](../../smartserve-pos/business_scenarios.py) and [validation workflow](../../.github/workflows/week9-validation.yml) | The current repository already has automated retail checkout, appointment, and repair checks. | Capture results for the new revision and get a human walkthrough on the demo workspaces. |
| [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153545486) | The November 25 handoff records the live SHA and requests a non-author test. | The assigned next check is an independent café, retail, and service walkthrough. |

## Week 12 results

These automated checks ran locally on November 23 KST against the GitHub baseline above using simulated payments and fresh SQLite test data. The browser runs used the production frontend build and a local FastAPI server.

| ID | Test | Expected result | Actual result | Status | Evidence |
|---|---|---|---|---|---|
| C1 | Pay for two lattes at ₩4,500 each | One paid ₩9,000 receipt. Stock falls by 500 ml milk and 36 g beans. | Receipt #1 showed Caffè Latte × 2 and ₩9,000 cash. Milk went from 5,000 to 4,500 ml and beans from 1,200 to 1,164 g. | **Pass · Local** | [Café run](#café-browserapi-run) |
| C2 | Attempt payment with stock below the required recipe amount | Payment is rejected, with no payment recorded or stock change. | With milk set to 100 ml, payment returned HTTP 409. Stock stayed unchanged, with zero payment records and zero inventory movements. | **Pass · Local** | [Backend run](#backend-run) |
| C3 | Retry payment on the same paid order | The simulator rejects the duplicate with HTTP 409. Stock stays at the amount after the first payment. | Retrying order #1 returned HTTP 409. Milk stayed at 4,500 ml and beans at 1,164 g. | **Pass · Local** | [Café run](#café-browserapi-run) |
| C4 | Sell one latte with beans stocked in kilograms and the recipe set to 18 g | Beans decrease by 0.018 kg. | The recipe stored 0.018 kg. After the next sale, beans went from 1.164 to 1.146 kg. | **Pass · Local** | [Café run](#café-browserapi-run) |
| C5 | Rename and reprice a latte, then reopen the old receipt | The old receipt retains the original item name and pricing. | Receipt #1 still showed Caffè Latte × 2 and ₩9,000. The saved order still recorded a ₩4,500 unit price. | **Pass · Local** | [Café run](#café-browserapi-run) |
| R1 | Sell one unit of a stocked retail item | Paid receipt matches the item, quantity, and price. Stock drops by one. | Receipt #3 showed Cotton T-shirt × 1 for ₩19,000 cash. T-shirt stock went from 40 to 39. | **Pass · Local** | [Business run](#business-browserapi-run) |
| S1 | Check out an appointment or repair job | Checkout shows a paid receipt and the linked ticket reaches Completed. | Checkout displayed a receipt for both the Classic haircut appointment flow and the Repair diagnosis job flow. Each linked ticket returned `completed` after payment. | **Pass · Local** | [Business run](#business-browserapi-run) |

For any failure, link a GitHub issue and record its owner, the affected test and revision, expected and observed behavior, the fix PR or commit, and the retest result. Mark an attempted check **Blocked** when access or setup prevents a result and record the exact blocker. Each teammate should link an issue comment, PR, run, or screenshot for the checks they personally completed.

## Evidence from the November 23 runs

### Backend run

Ran `python -B -m unittest discover -v` from `smartserve-pos/backend`. The suite completed with 46 passing tests.

```text
test_insufficient_stock (test_issue3.InventoryPaymentTests.test_insufficient_stock) ... ok
Ran 46 tests in 16.221s
OK
```

The insufficient-stock test asserts HTTP 409, unchanged stock, zero payments, and zero inventory movements. [Test source at the reviewed commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/bcd1f3a12c8891d3a669fdd9f4e96251f500d3de/smartserve-pos/backend/test_issue3.py#L137-L148)

### Café browser/API run

The café runner reported **27 passing checks**, including a simulated decline followed by successful payment on the same order. The decline returned HTTP 402, kept order #1 open, left stock unchanged, and added ₩0 in sales. The cash retry returned HTTP 200.

| Recorded check | Actual |
|---|---|
| Saved order | Open, ₩9,000 before payment |
| Paid stock | 4,500 ml milk and 1,164 g beans |
| Duplicate payment | HTTP 409, stock unchanged |
| 18 g recipe edit | 0.018 kg stored |
| Historical receipt | Caffè Latte, ₩4,500 unit price, ₩9,000 total |
| Stock after next sale | 4,250 ml milk and 1.146 kg beans |

[Local café receipt screenshot](evidence/screenshots/w12-local-cafe-receipt.png). Source for the browser/API assertions and screenshot steps. [Café validation runner](../week-09/run_validation.py)

### Business browser/API run

The business runner reported **37 passing checks**. The retail receipt screenshot showed **Payment Complete**, **Receipt #3**, **Cotton T-shirt × 1**, and **₩19,000 cash**. The runner recorded a remaining stock count of 39. Both the appointment and repair scenarios displayed a receipt and returned `completed` for the linked work after checkout.

[Local retail receipt screenshot](evidence/screenshots/w12-local-retail-receipt.png). Sources for the retail and service assertions. [Business runner](../../smartserve-pos/verify_business.py) · [Checkout scenarios](../../smartserve-pos/business_scenarios.py)

## What would support an Exceed submission

1. **Close the independent verification gap.** The live SHA and peer-test request are recorded below. The remaining evidence is the tester’s own results for C1, R1, and S1, including receipt totals, before-and-after stock, and final ticket status.
2. **Make your own contribution traceable.** Personally reproduce C2–C5 on the candidate build, then post your environment, exact SHA, expected and actual values, and screenshots or output under your own login. A PR containing only this report falls outside the validation workflow's path filters. Link an existing run for the candidate SHA or manually dispatch the workflow on the candidate branch.
3. **Document one result end to end.** If the live walkthrough exposes a regression, link the failing evidence, issue, focused fix, and passing retest. If the walkthrough passes, ask the tester to record the simulated decline and retry wherever the demo tools support it, including the same order ID and before-and-after stock. The local run above provides the expected values for that comparison.

These steps address the traceable evidence and individual ownership criteria described in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22). The repository materials reviewed did not specify a formal Week 12 Exceed threshold.

## Decision and Week 13 handoff

**Demo transaction readiness:** Local checks passed and the Render revision was confirmed. Team sign-off awaits the independent results. Carry the tested live workspaces and receipts into Week 13 for owner-access and daily sales reconciliation. [Week 13 roadmap](../week-10/final-roadmap.md)

## November 25 feedback follow-up

At about 14:16 KST, the PowerShell HTTP preflight returned HTTP 200 for the health and sign-in endpoints. The menu, inventory, and service-work endpoints returned HTTP 401 and required sign-in with two-factor verification. Checkout was blocked before any transaction, so the independent walkthrough remains pending. [Issue #22 preflight results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153696090)

Render lists commit `a9a35d2a8fe6425e05a4ac8d8feeb54048ba80fd` as live. A public GET to `/health` timed out after 35 seconds at 14:12 KST. A retry returned HTTP 200 with `{"status":"ok"}`. [Render deployment record](https://dashboard.render.com/web/srv-dbc8jbifngtc739d85q0/deploys/dep-dbvafnh42hec73b7u5u0)

| GitHub login | Contribution | Direct evidence |
|---|---|---|
| `daydevil80` | Authored and published the Week 12 report, documented the automated local outcomes for C1–C5, R1, and S1, and coordinated the Render handoff. The local suites were executed by automated runners. | [Report commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/e89acd3ac1912446144cb93f1dba769ab721ea9f) · [Render handoff](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153545486) · [Individual receipt](receipts/daydevil80.md) |
| `ualsom` | Reported a November 24 local HTTP retry regression. The focused test passed and backend discovery passed 47/47 at `e89acd3` with the added test in the working tree. The retry returned HTTP 409 and preserved payment and stock records. | [Individual result](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7124147327) |
| `Sammygit15` | Recorded the local signup-email failure and added backend, frontend, and build evidence. The post-fix signup retest is pending. | [Individual receipt](receipts/LamaMuskan%28Sammygit15%29.md) · [Evidence index](evidence-index.md) |
| `shrey776` | Catch-up follow-up recorded November 26: owns a repeatable repair checkout check. **Expected:** paid receipt for Repair diagnosis and linked ticket `completed`. **Actual shared baseline:** the November 23 local automated run reported that the repair flow displayed a receipt and the linked ticket returned `completed`. This is team automation evidence, not my personal run; receipt contents and ticket ID were not preserved in the report summary. Shreya reports no time to repeat the run or capture SmartServe screenshots for this submission. | [Week 12 receipt](receipts/Shreya.md); [Issue #31](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/31); [S1 result](#week-12-results); [QA checklist W12-REG-05](qa-checklist.md) |

| Priority | Owner | Expected on Render | Actual / status | Next check |
|---|---|---|---|---|
| P1 | `daydevil80` coordinates | Two lattes produce a ₩9,000 receipt and deduct 500 ml milk and 36 g beans with the demo recipe. | Independent run **Not tested**. | Non-author posts receipt and stock before and after. |
| P1 | `daydevil80` coordinates | One retail sale produces a paid receipt and deducts one unit. | Independent run **Not tested**. | Non-author posts receipt and stock before and after. |
| P1 | `daydevil80` coordinates | Service checkout produces a paid receipt and the linked ticket reaches Completed. | Independent run **Not tested**. | Non-author posts receipt, ticket ID, and final status. |

`Shuzita` was invited to test if eligible, with another non-author teammate as backup. Capture KST time, active SHA, workspace, expected and actual values, and direct proof in the tester’s own reply. [Peer-test request](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7153545486)


## November 24 follow-up — owner registration email failure

A separate Week 12 QA target was recorded on November 24 in the local Docker Compose environment. The owner registration page displayed “Signup email is temporarily unavailable. Please try again later.” The API log excerpt showed OPTIONS /auth/register returning 200 and POST /auth/register returning 503.

The issue is tracked in [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27). Follow-up inspection on November 24 confirmed that the running API container had `GMAIL_SENDER`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, and `GMAIL_REFRESH_TOKEN` all missing; `MAIL_PROVIDER` used the `gmail_api` default and `SMARTSERVE_ENV` was unset. `docker compose config` showed the API service receives only `DATABASE_URL`, with no Gmail `environment` entries or `env_file`. The inspected `mailer.py` requires `GMAIL_SENDER` and all three OAuth values for the Gmail API flow, while `security.py` converts any exception from `deliver(...)` into the observed 503. This establishes missing Gmail runtime configuration as the confirmed configuration defect. Because no traceback was captured, the exact thrown exception for the observed request was not directly recorded; given the missing sender, the mailer code's sender-configuration guard is the first expected failure. No fix or controlled retest is recorded, and independent peer verification remains pending. The repository HEAD reviewed was e89acd3ac1912446144cb93f1dba769ab721ea9f; backend/app/tenancy.py also had an uncommitted local modification, and exact running container image provenance was not established.

See the [QA checklist](qa-checklist.md), [bug report](bug-report-27.md), [peer-test notes](peer-test-notes.md), and [evidence index](evidence-index.md). The original browser screenshot is embedded in the QA checklist and evidence index from the attachment already present on Issue #27. It is evidence of the failed attempt, not a post-fix result.
