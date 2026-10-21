
# Week 7 Weekly Report — SmartServe POS

Team 3 · October 15–21, 2026 · Updated October 21 (Korea)

We are preparing a short café order demo. A cashier selects two lattes, checks ₩9,000, makes a simulated payment, shows the receipt, and checks the ingredient deduction and daily sales. [Midterm Prep Issue #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21) tracks the remaining work and follows up on #20.

The October 19 review found no current Week 7 evidence. Since then, the repository has received Sammygit15's documentation package, and this update adds the edit fixes, current test output, and daydevil80's receipt. We have not completed the independent test or a timed spoken rehearsal.

## This week's goal

This week, the team focused on reviewing the SmartServe POS vertical slice, checking the project's sprint quality, and organizing technical documentation and evidence.

The main objective was to review the café workflow from order creation to simulated payment, receipt generation, inventory deduction, and daily sales reporting. We also reviewed known implementation limitations and identified the evidence and verification work still required.

## What we committed to do

- [x] Review the main SmartServe order-to-payment workflow and documented project scope.
- [x] Review the Sprint 1 quality checks and existing technical evidence.
- [x] Organize the Week 7 project quality checklist and supporting documentation.
- [x] Identify known implementation limitations and follow-up work.
- [x] Run fresh isolated automated checks; browser/demo setup verification remains pending.
- [ ] Complete an independent setup and verification by another teammate.
- [ ] Collect and link each member's Week 7 contribution evidence.


| Evidence | Link |
|---|---|
| Issue(s) | [Issue #3 – Payment and Inventory Deduction](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3), [Issue #20 – Menu and Ingredient Editing Follow-up](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) |
| PR(s) / commits | [Repository commit history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commits/main) |
| Screenshot / demo evidence | [October 14 Evidence Package](../../week-06/evidence/2026-10-14/), [Evidence README](../../week-06/evidence/2026-10-14/README.md) |
| Test/check note | [Week 6 Automated Check](../../week-06/automated-check.md), [Week 6 Test Plan](../../week-06/test-plan.md) |
| Known problems | [Week 6 Follow-up Problems](../../week-06/follow-up-problems.md) |
| Sprint quality review | [Week 7 Sprint Quality Quick Checks](./sprint-quality-quick-checks.md), [Week 7 Work Checklist](./work-checklist.md) |
| Project documentation | [Main README](../../../README.md), [SmartServe POS README](../../../smartserve-pos/README.md), [Week 6 Weekly Report](../../week-06/weekly-report.md) |



## Current results

| Work | Result | Proof |
|---|---|---|
| Recipe edit with stock in kg | Fixed: 18 g saves as 0.018 kg; a following sale deducts the correct amount | [Expected/actual results](evidence/2026-10-21/demo-results.json) |
| Receipt name after menu rename | Fixed for new orders: original name and price stay on the receipt | [Results](evidence/2026-10-21/demo-results.json) |
| Older receipt history | Migration keeps the current label; original names not stored previously cannot be recovered | [Check notes](evidence/2026-10-21/README.md) |
| Backend tests | 24 passed, including four new regression tests | [Output](evidence/2026-10-21/backend-tests.txt) |
| Frontend production build | Passed, with existing Vite configuration warning | [Output](evidence/2026-10-21/frontend-build.txt) |
| Two-latte service check and payment fallback | ₩9,000; milk −500 ml, beans −36 g; failed/duplicate payment leaves stock unchanged | [Current evidence](evidence/2026-10-21/README.md) |
| Independent browser test | Pending | [Steps and result fields](retest-and-rehearsal.md) |
| Timed spoken rehearsal | Pending; target four minutes | [Script](midtern-demoscript.md) |

The new checks use isolated SQLite and call backend service functions. They do not replace browser testing, PostgreSQL validation, or a teammate's independent result. October 14 screenshots remain historical Week 6 evidence.

## Individual contributions

Each person must confirm their own entry and supply their own result. Suggested tasks below are not completed contributions or confirmed speaking assignments.

| GitHub login | Current contribution/evidence | Remaining action |
|---|---|---|
| `daydevil80` | Fixed alternate-unit recipe editing and receipt-name snapshots, added regression tests, ran current automated checks, and assembled the shared report/retest notes. [Receipt](receipts/daydevil80.md), [test output](evidence/2026-10-21/backend-tests.txt) | Review/explain the changes, rehearse the fix/results segment, coordinate non-author retest |
| `Sammygit15` | Reviewed and organized Week 7 project quality documentation. Updated the Sprint Quality Quick Checks to document the SmartServe vertical slice, technical workflow, and supporting evidence. Created and updated the Week 7 Work Checklist to organize project-scope review, technical evidence, individual contribution records, and remaining quality checks. [Quality-check commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c0356bc2c9b44410e7dbc6bdfc1dc820afa69d0b), [checklist commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/60459efb1b68fefa5f083c41d8a5ba1acf6ccf1d) | Report identifies Lama Muskan as Sammygit15; confirm this mapping and add own current receipt/rehearsal result |
| `ualsom` | No new Week 7 test result recorded here. [Earlier unit observation](../../week-06/receipts/ualsom.md) is Week 6 evidence | Suggested non-author tester: run corrected behavior and record exact values and screenshots |
| `Shuzita` | Current contribution/result awaiting member entry | Suggested task: run a failed-payment/empty-state check and link own receipt |
| `shrey776` | Current contribution/result awaiting member entry | Suggested task: time a clean-start rehearsal and record the actual duration/proof |

## Decision record

Record only decisions that change scope, approach, ownership, or the next plan.

| Decision | Why we chose it | Owner | Evidence / Issue link |
|---|---|---|---|
| Keep the current SmartServe vertical slice focused on order creation, simulated payment, receipt generation, and inventory deduction. | This is the main documented workflow and the clearest representation of the current MVP. | `Sammygit15`| [Sprint Quality Quick Checks](./sprint-quality-quick-checks.md), [Issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3) |
| Keep known failures visible in the project documentation. | Passing backend tests and a frontend build do not resolve separately observed browser-level failures. |`Sammygit15` | [Automated Check](../../week-06/automated-check.md), [Follow-up Problems](../../week-06/follow-up-problems.md) |
| Prioritize verification and correction of existing behavior before expanding the MVP. | The historical receipt and recipe-unit editing problems affect data correctness. |`daydevil80` | [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) |


## Risks and next actions

| Item | Owner | Next action/status |
|---|---|---|
| Independent verification | daydevil80 coordinates; non-author tester unconfirmed | Follow [retest steps](retest-and-rehearsal.md), record login/commit and proof |
| Spoken demo timing | Team 3; speakers to confirm | Run the four-minute plan and enter actual duration |
| Missing personal evidence | Each member | Complete own row/receipt before the October 21 EOD deadline |
| Old receipt names cannot be reconstructed | daydevil80 | Explain migration boundary; use new sample orders for rename proof |
| Payments simulated; owner permissions not enforced | Team 3 | Say this during the demo; no real-payment/security claim |
| PostgreSQL/browser behavior not rechecked in this run | daydevil80 coordinates | Test the pushed version in the actual demo setup |

Code and documentation were prepared and checked with coding-agent assistance. Review and explain the changes before presenting them. We have kept teammate tests and rehearsal fields pending until those people provide results.
