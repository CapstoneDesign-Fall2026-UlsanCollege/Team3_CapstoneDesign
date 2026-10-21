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
| Sherap Hyolmo (`daydevil80`) | Prepared SmartServe for cloud deployment by configuring production API requests, adding a cloud server entry point and Render deployment configuration, and documenting free hosting setup. Verified the production frontend build and cloud server routes. Started SmartServe with Docker and published a temporary public demo through Cloudflare Tunnel; confirmed HTTP 200 responses for the homepage, health endpoint, and menu API. | [Public demo](https://brighton-complications-while-workers.trycloudflare.com) — verified October 21, 2026; available while the host PC, Docker, and tunnel remain running. Cloud deployment files are local and have not been pushed. |
| Ualson Tamang (`ualsom`) | Week 7 contribution to be confirmed by the member. | |
| Shuzita Majhi (`Shuzita`) | Week 7 contribution to be confirmed by the member. |  |
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
