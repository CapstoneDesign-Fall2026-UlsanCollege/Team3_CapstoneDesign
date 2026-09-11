# Weekly Report

**Team:** Team 3  
**Week:** 2  
**Date:** 2026-09-10

## This week's goal

The team compared the two finalist projects, selected one primary direction, and defined a realistic first version that can be demonstrated and tested during the semester.

## What we committed to do

- [x] Compare SmartServe POS and Chimeki Market Nepal and select a primary project.
- [x] Define the target users, smallest useful version, scope boundaries, and midterm demonstration.
- [x] Document the core order, payment, receipt, inventory, and sales workflow for SmartServe POS.

## Evidence links



| Evidence | Link |
|---|---|
| Issue(s) | Week 1 planning Issue and finalist discussion links are recorded in the [Week 1 Launch Report](../week-01/week-01-launch-report.md); Week 2 implementation Issues are not yet created. |
| PR(s) / commits | To be added after the documentation commit or pull request. |
| Screenshot / demo | To be added after the first wireframe or prototype is created. |
| Test/check note | [Design document](design-doc-v1.md) has no diagnostics errors. |
| Document update | [Idea Selection Table](idea-selection-table.md) and [Design Doc v1](design-doc-v1.md) |

## Individual receipts

| Student | What they did | Evidence link |
|---|---|---|
| Sherap Hyolmo | Coordinated the project decision and helped define implementation priorities. | [Idea Selection Table](idea-selection-table.md) |
| Lama Muskan | Contributed to the technical discussion and core order, payment, and inventory workflow. | [Design Doc v1](design-doc-v1.md) |
| Ualson Tamang | Supported project comparison, requirements discussion, and risk identification. | [Idea Selection Table](idea-selection-table.md) |
| Shuzita Majhi | Contributed to interface and documentation planning for cashier and manager views. | [Design Doc v1](design-doc-v1.md) |
| Shreya | Contributed to reliability concerns and testing needs for stock and duplicate completion. | [Design Doc v1](design-doc-v1.md) |

## Blockers or risks

| Blocker/risk | Owner | Next action |
|---|---|---|
| Technology stack and database are not confirmed. | Team | Agree on the stack and record the decision in a GitHub Issue. |
| Inventory could be deducted twice or not at all after payment. | Lama Muskan and Sherap Hyolmo | Implement order-state validation and test the inventory workflow. |
| The project scope could expand beyond the schedule. | Sherap Hyolmo | Prioritize the order-to-inventory workflow and defer non-essential features. |
| Version 1 will use simulated payments and demonstration data. | Team | Keep real payment integration and production data outside the MVP. |

## Decision record

Record only decisions that change scope, approach, ownership, or the next plan.

| Decision | Why we chose it | Owner | Evidence / Issue link |
|---|---|---|---|
| Select SmartServe POS as the primary project. | It has a focused workflow that can demonstrate order, receipt, inventory, and sales changes. | Team 3 | [Idea Selection Table](idea-selection-table.md) |
| Keep Chimeki Market Nepal as the backup project. | It remains viable but has larger safety, trust, messaging, and moderation risks. | Team 3 | [Idea Selection Table](idea-selection-table.md) |
| Prioritize simulated payments and one-store cafe operations for Version 1. | This keeps the project testable and avoids real payment, tax, supplier, and multi-branch complexity. | Sherap Hyolmo | [Design Doc v1](design-doc-v1.md) |

## Next week's bridge task

- Confirm the web framework, database, and local setup process.
- Create implementation Issues for the data model, cashier workflow, inventory logic, dashboard, wireframes, and test cases.
