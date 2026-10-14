# Week 6 Weekly Report — SmartServe POS

**Team:** 3  
**Week:** 6, Sprint 1  
**Dates:** October 8–14, 2026  
**Updated:** October 14, 2026, Korea time  
**Status:** Evidence recorded; failures and independent test remain open

## This week's goal

Check that editing a menu item or ingredient after stock exists saves correctly, keeps stock and historical orders accurate, and still supports a simulated sale. Record what passes and what fails rather than adding more features.

## What we committed to do

- [x] Define a small behavior, a clear starting point, and expected results before testing.
- [x] Run the existing backend tests and a fresh browser/API check with separate sample data.
- [x] Record actual results, screenshots, and the failing steps.
- [x] Link the implementation issue and exact source commit.
- [ ] Have a non-author teammate follow the written steps without coaching.
- [ ] Fix the observed failures and rerun the same steps.
- [ ] Have each member confirm their own contribution entry and receipt.

## What was checked

We checked this by creating and paying a two-latte order, converting coffee-bean stock from g to kg, editing the latte's name and price, reopening its old receipt, and making another sale. Expected result: saved stock and recipes convert consistently, old receipt information stays unchanged, and the next order uses the new price. Actual result: payment, stock conversion, original prices, and daily sales passed; the old receipt's name changed, and editing an 18 g recipe while stock was in kg saved 18 kg. Proof: [check note](automated-check.md), [raw results](evidence/2026-10-14/results.json), and [screenshots](evidence/2026-10-14/README.md).

The repeat browser/API run recorded **12 passed checks and 3 failed checks**, with two underlying data/history problems. The 20 existing backend tests and frontend build passed. The existing tests do not cover both newly observed cases, so their pass does not make these failures disappear.

### Main results

| Behavior | Expected | Actual | Status |
|---|---|---|---|
| Save two-latte order | Open, ₩9,000, no stock change | Same | Pass |
| Recover saved order after refresh | Same ID, items, and total | Same after data finishes loading | Pass |
| Failed simulated payment | HTTP 402, open order, unchanged stock/sales | Same | Pass |
| Successful cash payment | Milk −500 ml; beans −36 g | Milk 4,500 ml; beans 1,164 g | Pass |
| Repeat payment | HTTP 409; no second deduction/payment | Same; one payment and two ingredient movements for the order | Pass |
| Convert beans g → kg | 1.164 kg stock, 0.25 kg threshold, 0.018 kg recipe | Same; earlier movement converts to −0.036 kg | Pass |
| Edit menu price | New price ₩6,000; old unit price ₩4,500 | Same; old receipt total stays ₩9,000 | Pass |
| Rename menu item | Old receipt keeps Caffè Latte | Old receipt becomes Caffè Latte test | Fail |
| New sale after conversion | ₩6,000; beans 1.146 kg; milk 4,250 ml | Same | Pass |
| Edit recipe using 18 g with stock in kg | Stored recipe 0.018 kg; item available | Stored recipe 18 kg; item disabled as unavailable | Fail |
| Daily sales | Two paid orders, ₩15,000 | Same | Pass |

## Evidence links

| Evidence | Link |
|---|---|
| Implementation issue | [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) |
| Owner editing implementation | [dccc291](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/dccc291) |
| Stock-unit conversion implementation | [de97f86](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/de97f86) |
| Exact application source tested | [df2f357](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/df2f357b0246fd71b76d7be8a7fa03d29dee68fe) |
| Checkout tested | [f4e8a6d](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/f4e8a6d3c185d3b9c9090d6daaf875080902cf1a); its application source matches df2f357 |
| Written steps and expected results | [Test plan](test-plan.md) |
| October 14 actual results | [Automated check](automated-check.md) |
| Independent tester result | [Tested-By Note](tested-by-note.md), pending |
| Current completion criteria | [Definition of Done](definition-of-done.md) |
| Failure reproduction and next actions | [Follow-up problems](follow-up-problems.md) |
| Backend/build output | [20 tests](evidence/2026-10-14/backend-tests.txt), [frontend build](evidence/2026-10-14/frontend-build.txt) |
| Database confirmation | [Payment and movement records](evidence/2026-10-14/database-check.json) |

## Individual contribution entries

These entries link visible records. They do not claim that all five people ran the October 14 check. Each member still needs to confirm or complete their own entry.

| GitHub login | Recorded contribution | Evidence | Remaining member action |
|---|---|---|---|
| `daydevil80` | Authored Issue #20 and the owner-editing, stock-conversion, and recipe-input implementation. This report connects those changes to fresh scripted verification and records the failures. | [#20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20), [dccc291](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/dccc291), [de97f86](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/de97f86), [df2f357](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/df2f357), [receipt](receipts/daydevil80.md) | Review this evidence, arrange a non-author test, and choose the follow-up fix |
| `Sammygit15` | Created/revised the Week 6 checklist/report files and posted menu/inventory editing observations on October 8. | [017fca3](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/017fca3), [f4e8a6d](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/f4e8a6d), [editing comment](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20#issuecomment-6054966665), [receipt draft](receipts/Sammygit15.md) | Confirm their entry; add exact expected/actual values for any new test. Commit display name LamaMuskan is not the canonical login |
| `ualsom` | Reported a unit-change problem on Issue #20 on October 8 and supplied screenshots. | [unit-change comment](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20#issuecomment-6055077744), [receipt draft](receipts/ualsom.md) | Confirm their entry and test g/kg separately from unsupported mass/volume conversion |
| `Shuzita` | Week 6 contribution entry is still awaiting the member's own result or blocker. | [receipt template](receipts/Shuzita.md) | Enter a concrete contribution with a proof link; a success/failure payment check is a possible bounded task |
| `shrey776` | Week 6 contribution entry is still awaiting the member's own result or blocker. | [receipt template](receipts/shrey776.md) | Enter a concrete contribution with a proof link; a clean-start cashier check is a possible bounded task |

The linked October 8 teammate comments are real earlier observations. They do not document that someone independently followed the new October 14 steps without coaching. That requirement remains incomplete.

## Blockers and next actions

| Blocker | Owner | Next action |
|---|---|---|
| Independent teammate test not run | `daydevil80` coordinates; tester not yet confirmed | Give the written steps to a non-author teammate and record their exact login, date, result, and proof |
| Old receipts use the current menu name | `daydevil80` | Review problem F1, select a fix, and rerun the rename/history check |
| Recipe edit ignores alternate input unit | `daydevil80` | Review problem F2, fix the edit path, and rerun conversion and availability checks |
| Member entries/receipts need confirmation | Each exact login above | Each person completes their own contribution/evidence entry |
| Issue #20 is closed despite the new history/recipe findings | `daydevil80` | Review whether to reopen it or create a linked follow-up; this documentation update does not change issue state |

## Decision record

| Decision | Reason | Owner / evidence |
|---|---|---|
| Use the GitHub application source for this check | The evidence must match a commit that reviewers can inspect | `daydevil80`; source links above |
| Use fresh isolated sample data | Avoid changing the team's shared stock and sales | [check environment](automated-check.md) |
| Publish documentation and evidence only | Application changes are outside this push | [evidence index](evidence/2026-10-14/README.md) |
| Keep independent testing and failures incomplete | Scripted checks do not replace a teammate result or a bug fix | [completion criteria](definition-of-done.md) |

## Week 7 bridge

Follow the [five-step midterm demo](setup-and-demo.md), fix and retest the first data/history problem, then have a non-author teammate repeat the same path. The team can currently prove simulated payment and preserved prices in this sample run. It cannot yet prove unchanged historical product names, correct alternate-unit recipe editing, or the required independent test.
