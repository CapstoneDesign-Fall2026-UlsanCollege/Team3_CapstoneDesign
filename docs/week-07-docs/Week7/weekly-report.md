# Week 7 Weekly Report — SmartServe POS

**Team:** Team 3  
**Week:** 7  
**Date:** 2026-10-19  
**Project:** SmartServe POS

## This week's goal

This week, the team focused on reviewing the SmartServe POS vertical slice, checking the project's sprint quality, and organizing technical documentation and evidence.

The main objective was to review the café workflow from order creation to simulated payment, receipt generation, inventory deduction, and daily sales reporting. We also reviewed known implementation limitations and identified the evidence and verification work still required.

## What we committed to do

- [x] Review the main SmartServe order-to-payment workflow and documented project scope.
- [x] Review the Sprint 1 quality checks and existing technical evidence.
- [x] Organize the Week 7 project quality checklist and supporting documentation.
- [x] Identify known implementation limitations and follow-up work.
- [ ] Confirm the latest implementation against the recorded evidence with a fresh check.
- [ ] Complete an independent setup and verification by another teammate.
- [ ] Collect and link each member's Week 7 contribution evidence.


| Evidence | Link |
|---|---|
| Issue(s) | [Issue #3 – Payment and Inventory Deduction](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3), [Issue #20 – Menu and Ingredient Editing Follow-up](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) |
| PR(s) / commits | [Repository commit history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commits/main) |
| Screenshot / demo evidence | [October 14 Evidence Package](../week-06/evidence/2026-10-14/), [Evidence README](../week-06/evidence/2026-10-14/README.md) |
| Test/check note | [Week 6 Automated Check](../week-06/automated-check.md), [Week 6 Test Plan](../week-06/test-plan.md) |
| Known problems | [Week 6 Follow-up Problems](../week-06/follow-up-problems.md) |
| Sprint quality review | [Week 7 Sprint Quality Quick Checks](./sprint-quality-quick-checks.md), [Week 7 Work Checklist](./work-checklist.md) |
| Project documentation | [Main README](../../../README.md), [SmartServe POS README](../../../smartserve-pos/README.md), [Week 6 Weekly Report](../week-06/weekly-report.md) |


## Individual contribution entries — one row per student

| Student | What they did | Evidence link |
|---|---|---|
| **Lama Muskan (`Sammygit15`)** | Reviewed and organized Week 7 project quality documentation. Updated the Sprint Quality Quick Checks to document the SmartServe vertical slice, technical workflow, and supporting evidence. Created and updated the Week 7 Work Checklist to organize project-scope review, technical evidence, individual contribution records, and remaining quality checks. | [Commit – Updated Sprint Quality Quick Checks](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c0356bc2c9b44410e7dbc6bdfc1dc820afa69d0b), [Commit – Updated Week 7 Work Checklist](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/60459efb1b68fefa5f083c41d8a5ba1acf6ccf1d) |
| Sherap Hyolmo (`daydevil80`) | Completed the recipe-edit and receipt-history fixes with coding-agent assistance. Recipe editing now converts 18 g to 0.018 kg, and new orders preserve their original item names after menu renaming. Added four regression tests and recorded fresh verification: 24 backend tests passed, the frontend build passed, and the two-latte check confirmed the expected payment, stock and sales results. Prepared my Week 7 receipt and tracked the remaining independent test and rehearsal in Issue #21. | [Implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0d5fecdf827deb12b7d4d560e392bfb06d868591), [24 passing tests](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0d5fecdf827deb12b7d4d560e392bfb06d868591/docs/week-07-docs/Week7/evidence/2026-10-21/backend-tests.txt), [Expected/actual results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0d5fecdf827deb12b7d4d560e392bfb06d868591/docs/week-07-docs/Week7/evidence/2026-10-21/demo-results.json), [Individual receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0d5fecdf827deb12b7d4d560e392bfb06d868591/docs/week-07-docs/Week7/receipts/daydevil80.md), [Midterm Prep Issue #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21) |
| Ualson Tamang (`ualsom`) | Week 7 contribution to be confirmed by the member. | |
| Shuzita Majhi (`Shuzita`) | Week 7 payment-failure and recovery evidence package prepared with coding-agent assistance. The recorded browser checks show that failed simulated payment returns HTTP 402, keeps the order open, and leaves stock and sales unchanged. Successful cash retry pays the same ₩9,000 order and deducts 500 ml milk and 36 g beans. Duplicate payment returns HTTP 409 without another deduction. Personal review or independent retest remains to be confirmed. | [Actual results](./shuzita_ben/03-result.md), [Individual receipt](./shuzita_ben/receipt.md), [Screenshot evidence](./shuzita_ben/evidence/agent-run-2026-10-21/SCREENSHOTS.md), [Raw browser checks](./shuzita_ben/evidence/agent-run-2026-10-21/results.json) |
| Shreya (`shrey776`) | Week 7 contribution to be confirmed by the member. |  |

## Blockers or risks

| Blocker/risk | Owner | Next action |
|---|---|---|
| Historical receipts display the current menu name after a menu rename. |  `Sammygit15` `daydevil80` | Decide whether product names should be stored as order-item snapshots and retest historical receipts. |
| Editing a recipe using an alternate unit can save an incorrect quantity. |  `Sammygit15` `daydevil80` | Apply unit conversion during recipe editing and add a regression test. |
| Independent teammate verification is not yet recorded. | Not Yet | Ask a non-author teammate to follow the written setup and test steps and record the result. |
| Week 7 individual contributions are not yet confirmed. | All five members | Each member should add their own work and a direct evidence link. |
| Existing technical evidence is dated October 14. | All five members | Capture updated evidence if implementation or test results have changed since then. |

## Decision record

Record only decisions that change scope, approach, ownership, or the next plan.

| Decision | Why we chose it | Owner | Evidence / Issue link |
|---|---|---|---|
| Keep the current SmartServe vertical slice focused on order creation, simulated payment, receipt generation, and inventory deduction. | This is the main documented workflow and the clearest representation of the current MVP. | `Sammygit15`| [Sprint Quality Quick Checks](./sprint-quality-quick-checks.md), [Issue #3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/3) |
| Keep known failures visible in the project documentation. | Passing backend tests and a frontend build do not resolve separately observed browser-level failures. |`Sammygit15` | [Automated Check](../week-06/automated-check.md), [Follow-up Problems](../week-06/follow-up-problems.md) |
| Prioritize verification and correction of existing behavior before expanding the MVP. | The historical receipt and recipe-unit editing problems affect data correctness. |`daydevil80` | [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) |

### Contributor Information

Contributor: Lama Muskan

GitHub username: Sammygit15

Commit author clarification: The Week 7 documentation commits were authored under the display name LamaMuskan. This is the same contributor associated with the GitHub account Sammygit15. Git author configuration has been updated so future commits use Sammygit15 as the author name.


## Next week's bridge task

- Review and address the historical receipt-name and alternate recipe-unit problems.
- Repeat the relevant test steps after any fixes and attach new evidence.
- Have a non-author teammate independently follow the setup and verification instructions.
- Collect each member's Week 7 contribution and evidence record.
- Keep project limitations, unresolved issues, and ownership up to date.
