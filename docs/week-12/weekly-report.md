# Week 12 Weekly Report — SmartServe POS QA and Regression

**Team 3 · November 19–25, 2026 (KST)**

**Status as of November 23:** Local QA passed on the reviewed commit. Independent Render verification and team sign-off are pending.

**GitHub baseline reviewed:** `main` at [`bcd1f3a`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/bcd1f3a12c8891d3a669fdd9f4e96251f500d3de).

## Goal

Verify café, retail, and service sales on the final-demo build using simulated payments. Compare each transaction with its receipt, stock movement where applicable, and final work status. Record defects, fixes, and retests against the revision that was actually tested. [Final demo roadmap](../week-10/final-roadmap.md)

## Evidence carried forward

| GitHub evidence | Result recorded | Week 12 follow-up |
|---|---|---|
| [Week 11 Render verification](../week-11/live-two-latte-verification.md) | A developer-coordinated browser run on `eb2c88e` recorded café order #1 at ₩9,000, milk 5,000 → 4,500 ml, and beans 1,000 → 964 g. | Confirm the deployed SHA and get a teammate who did not author the relevant change to repeat the check. |
| [Week 11 PR CI #9](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/43902224014) | Ualson's isolated retry regression recorded HTTP 409 and a single stock deduction. | Re-run the regression on the Week 12 candidate. The Week 11 Render UI run left duplicate payment untested. |
| [Business workflow scenarios](../../smartserve-pos/business_scenarios.py) and [validation workflow](../../.github/workflows/week9-validation.yml) | The current repository already has automated retail checkout, appointment, and repair checks. | Capture results for the new revision and get a human walkthrough on the demo workspaces. |
| [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) | The issue was open with zero comments at review. Its acceptance calls for a named non-author result and individual evidence. | Have the tester post their own result and link it below. |

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

Source for the browser/API assertions and screenshot steps. [Café validation runner](../week-09/run_validation.py)

### Business browser/API run

The business runner reported **37 passing checks**. The retail receipt screenshot showed **Payment Complete**, **Receipt #3**, **Cotton T-shirt × 1**, and **₩19,000 cash**. The runner recorded a remaining stock count of 39. Both the appointment and repair scenarios displayed a receipt and returned `completed` for the linked work after checkout.

Sources for the retail and service assertions. [Business runner](../../smartserve-pos/verify_business.py) · [Checkout scenarios](../../smartserve-pos/business_scenarios.py)

## Individual contributions

| Contributor | Week 12 contribution | Tested revision and environment | Result and evidence | Independent verification |
|---|---|---|---|---|
| Ualson Tamang (`ualsom`) | Added one HTTP regression for C1/C3 that checks the persisted receipt and exact payment and inventory ledger rows across a duplicate retry. | [`e89acd3`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/e89acd3ac1912446144cb93f1dba769ab721ea9f) with the uncommitted test in the working tree. November 24 KST, local Windows, Python 3.13.7, temporary SQLite, simulated payments. | **Pass · Local. Blocked · Deployed.** [Individual report](receipts/UalsonTamang%28ualsom%29.md) · [Test source](../../smartserve-pos/backend/test_week12_ualsom.py) · [Focused terminal output](evidence/ualsom-focused.txt) · [Full backend terminal output](evidence/ualsom-backend-suite.txt) | **Pending.** [Teammate procedure](ualsom-manual-verification.md) · [@ualsom’s result and request for an independent milk check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7124147327) |

| Check | Expected | Observed in the November 24 local run |
|---|---|---|
| Create and pay for two lattes | HTTP 201 and an open order at 2 × KRW 4,500 with unchanged stock. Cash payment returns HTTP 200 and a paid receipt for KRW 9,000. | Order #1 opened at KRW 9,000 with stock and ledgers unchanged. Cash returned HTTP 200 and the saved paid receipt matched the payment response. |
| Stock and ledger after payment | Milk −500 ml, beans −36 g, one KRW 9,000 cash payment tied to the receipt reference and two `paid_order` movements tied to the order. | Milk 5,000 → 4,500 ml, beans 1,200 → 1,164 g. One cash payment for KRW 9,000 and two movements for the expected ingredients and quantities. |
| Retry the same order by card | HTTP 409. Original cash receipt, reference, payment timestamp, stock and ledger rows remain unchanged. | HTTP 409. The saved receipt and inventory snapshots matched exactly, as did the one payment row and two movement rows. |

Week 10 covered a same-session handler retry, and Week 11 covered a fresh-session handler retry. This contribution exercises the HTTP create, pay, read-back, inventory and retry routes through FastAPI TestClient, with a signed-in principal and workspace engine supplied by the test fixture. It compares persisted receipt fields and exact ledger rows before and after retry. The focused run passed 1 test, and backend discovery passed all 47 tests, including the Week 10 and 11 regressions. The pinned HTTP client emitted a Starlette deprecation warning in both runs. The local focused rerun also passed. [Rerun output](evidence/ualsom-focused-rerun.txt)

**Deployed manual check · Blocked (November 24 KST).** Ualson reached the 2FA prompt and requested a new code after the first verification email failed to arrive. Neither email arrived during the attempt. The payment and inventory steps were not reached. Independent teammate verification remains **Pending**.

## What would support an Exceed submission

1. **Close the independent verification gap.** As `daydevil80`, confirm the Render revision and coordinate the run. Ask a teammate who did not author the checkout change to carry out C1, R1, and S1 and post their own results in Issue #22. Link the comment here. Include receipt totals, before-and-after stock, and final ticket status. This is the clearest missing evidence in the GitHub record.
2. **Make your own contribution traceable.** Personally reproduce C2–C5 on the candidate build, then post your environment, exact SHA, expected and actual values, and screenshots or output under your own login. A PR containing only this report falls outside the validation workflow's path filters. Link an existing run for the candidate SHA or manually dispatch the workflow on the candidate branch.
3. **Document one result end to end.** If the live walkthrough exposes a regression, link the failing evidence, issue, focused fix, and passing retest. If the walkthrough passes, ask the tester to record the simulated decline and retry wherever the demo tools support it, including the same order ID and before-and-after stock. The local run above provides the expected values for that comparison.

These steps address the traceable evidence and individual ownership criteria described in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22). The repository materials reviewed did not specify a formal Week 12 Exceed threshold.

## Decision and Week 13 handoff

**Demo transaction readiness:** Local checks passed. Before sign-off, confirm the deployed SHA and record the independent Render walkthrough in Issue #22 with the tester's login, KST timestamp, workspace, order or ticket IDs, and evidence. Carry those live workspaces and receipts into Week 13 so the team can verify owner access and reconcile the daily sales totals. [Week 13 roadmap](../week-10/final-roadmap.md)
