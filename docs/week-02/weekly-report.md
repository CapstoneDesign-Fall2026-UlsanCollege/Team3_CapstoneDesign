# Week 2 Weekly Report

**Team:** Team 3  
**Week:** 2  
**Date:** 2026-09-10

## Work Completed

- Compared the two finalist ideas from Week 1.
- Selected **SmartServe POS** as the primary project direction.
- Kept **Chimeki Market Nepal** as a backup direction.
- Documented the target users, problem, smallest useful version, and main risk for both directions.
- Created Design Document v1 for SmartServe POS.
- Defined the minimum order, payment, inventory, receipt, and sales workflow.
- Identified the main data entities and the risk of duplicate or missing stock deductions.

## Project Decision

SmartServe POS was selected because the team can build and demonstrate a focused workflow within the course schedule. Its main value can be shown through observable changes: a completed cafe order produces a receipt, deducts ingredients, and updates the daily sales record.

## Evidence
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
| PR(s) / commits | To be added after the Week 2 documentation commit or pull request. |
| Screenshot / demo | To be added after the first wireframe or prototype is created. |
| Test/check note | [Design document diagnostics: no errors found](design-doc-v1.md) |
| Document update | [Week 2 Idea Selection Table](idea-selection-table.md) and [SmartServe POS Design Doc v1](design-doc-v1.md) |

## Individual receipts

| Student | What they did | Evidence link |
|---|---|---|
| Sherap Hyolmo | Coordinated the project decision and helped define the SmartServe POS direction and implementation priorities. | [Week 2 Idea Selection Table](idea-selection-table.md) |
| Lama Muskan | Contributed to the technical discussion and the core order, payment, and inventory workflow. | [SmartServe POS Design Doc v1](design-doc-v1.md) |
| Ualson Tamang | Supported project comparison, requirements discussion, and identification of the main project risks. | [Week 2 Idea Selection Table](idea-selection-table.md) |
| Shuzita Majhi | Contributed to the interface and documentation planning for the cashier and manager views. | [SmartServe POS Design Doc v1](design-doc-v1.md) |
| Shreya | Contributed to reliability concerns and the need for tests covering stock and duplicate completion. | [SmartServe POS Design Doc v1](design-doc-v1.md) |

## Blockers or risks

| Blocker/risk | Owner | Next action |
|---|---|---|
| Technology stack and database are not confirmed. | Team | Agree on the stack and record the decision in a GitHub Issue before implementation. |
| Inventory could be deducted twice or not at all after payment. | Development leads | Implement order-state validation and test successful, insufficient-stock, and duplicate-completion cases. |
| Scope could expand beyond the schedule. | Project coordinator | Prioritize the order-to-inventory workflow and defer non-essential features. |

## Decision record

Record only decisions that change scope, approach, ownership, or the next plan.

| Decision | Why we chose it | Owner | Evidence / Issue link |
|---|---|---|---|
| Select SmartServe POS as the primary project. | It has a focused, practical workflow that can be demonstrated through observable order, receipt, inventory, and sales changes. | Team 3 | [Week 2 Idea Selection Table](idea-selection-table.md) |
| Keep Chimeki Market Nepal as the backup project. | It remains viable but has larger safety, trust, messaging, and moderation risks for the available schedule. | Team 3 | [Week 2 Idea Selection Table](idea-selection-table.md) |
| Prioritize simulated payments and one-store cafe operations for Version 1. | This keeps the project testable and avoids real payment, tax, supplier, and multi-branch complexity. | Sherap Hyolmo | [Design Doc v1](design-doc-v1.md) |

## Next week's bridge task

- Confirm the web framework, database, and local setup process.
- Create implementation Issues for the data model, cashier workflow, inventory logic, dashboard, wireframes, and test cases.
| Area | Status | Notes |
|---|---|---|
| Team and repository setup | Complete | Completed during Week 1. |
| Technical stack | To decide | Must be agreed before implementation begins. |
| Prototype implementation | Not started | Planned for the next work period. |

## Risks and Limitations

- The team has not yet verified the technical stack or database approach.
- Inventory consistency is still a design risk and needs an implementation test.
- The first version will use simulated payments and demonstration data.
- Detailed authentication and role permissions may need to be reduced if they threaten the core workflow deadline.

| Confirm the technology stack | Team | Stack and setup steps are recorded in a GitHub Issue. |
| Create the initial application structure | Development leads | The project starts locally and includes a basic navigation or home screen. |
| Define the database schema | Development leads with research support | Tables or models for ingredients, menu items, orders, payments, and inventory transactions are reviewed. |
| Prepare wireframes for cashier and manager views | Design lead | Wireframes cover the core order and dashboard workflow. |
| Write core test cases | Testing lead | Test cases cover successful payment, insufficient stock, and duplicate completion prevention. |
| Create GitHub Issues for implementation tasks | Project coordinator | Each task has an owner, deadline, and Definition of Done. |

## Blockers

No current blockers. The next dependency is agreement on the technology stack before implementation work begins.
