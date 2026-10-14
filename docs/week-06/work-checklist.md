# Week 6 Work Checklist – SmartServe POS

**Date:** October 11, 2026  
**Team:** Team 3
**Evidence update:** October 14, 2026

Checked test items below refer to the scripted verification in [automated-check.md](automated-check.md), unless a human test is explicitly recorded. The independent teammate test, issue-state update, member-confirmed rows, and final Week 6 completion are still pending. The existing report entry point now links to [the single shared report](weekly-report.md). Failed rename/recipe criteria are in [definition-of-done.md](definition-of-done.md).

## 1. Main Work

- [x] Test one main feature of SmartServe POS.
- [x] Check if a cashier can select menu items and enter quantities.
- [x] Check if the order total is calculated correctly.
- [x] Test the simulated payment process.
- [x] Check if the order status changes to `paid` after successful payment.
- [x] Check if inventory is deducted after payment.
- [x] Make sure inventory is not deducted twice for the same order.
- [ ] Ask another teammate to test the feature.
- [x] Write down what worked and what did not work.

## 2. Testing Evidence

- [x] Write down the testing steps.
- [x] Record the expected result.
- [x] Record the actual result.
- [ ] Add the tester's name and testing date.
- [x] Take screenshots or record a short video.
- [ ] Add the evidence link to the related GitHub Issue.
- [ ] If something does not work, create or update an Issue.

## 3. GitHub and Documentation

- [ ] Update the related GitHub Issue.
- [x] Update the Definition of Done.
- [x] Add the commit or pull request link.
- [x] Create the Week 6 Weekly Report.
- [ ] Add each member's contribution and evidence link.
- [ ] Complete an Individual Evidence Receipt.
- [ ] Make sure every team member adds their own evidence.

## 4. Extra Testing (If Time Allows)

- [x] Test what happens when payment fails.
- [x] Check if an existing order keeps its original price after the menu price changes.
- [x] Try repeating a payment request.
- [ ] Fix any bugs found during testing.
- [ ] Test the feature again after fixing the bug.
- [x] Prepare a simple demonstration path for the midterm presentation.

## 5. Problems and Next Actions

| Problem | Person Responsible | Next Action |
|---|---|---|
| Historical product name changes | daydevil80 | Review F1 and choose a linked fix |
| Alternate-unit recipe edit saves wrong amount | daydevil80 | Review F2; fix and rerun the edit/availability test |
| Independent tester missing | daydevil80 coordinates | Arrange a non-author test using the written steps |
| Member entries and receipts pending | Each member | Confirm or complete their own evidence row and receipt |

## 6. Final Check

- [ ] Another teammate successfully follows the testing steps.
- [x] Screenshots or other evidence are added.
- [ ] GitHub Issues are updated.
- [ ] Weekly Report is completed.
- [ ] Individual Evidence Receipts are completed.
- [ ] Remaining problems have an assigned person and next action.

**Week 6 Goal:** Test the main SmartServe POS order and payment process, find any problems, and record the results with proper evidence.

## Evidence links

[Shared report](weekly-report.md) · [Test plan](test-plan.md) · [Automated check](automated-check.md) · [Independent test pending](tested-by-note.md) · [Screenshots](evidence/2026-10-14/README.md) · [Current DoD](definition-of-done.md)
