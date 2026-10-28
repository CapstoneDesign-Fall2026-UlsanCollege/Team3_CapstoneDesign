# Week 9 verification handoff

**Coordinator:** `daydevil80`

**Milestone:** [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22)

The next check uses a teammate who did not author the implementation. Confirm their canonical GitHub login before starting. This is the procedure and success signal, not a claim that the human handoff has happened.

## Setup

1. Use a clean checkout of the agreed current commit. Record its full hash and follow [the project setup](../../smartserve-pos/README.md).
2. Start a separate sample database/project. Do not erase shared data. Record actual starting quantities, menu prices and daily sales.
3. Open the cashier and owner login at `/etalogin`. Use credentials supplied privately by the demo owner; keep passwords and session cookies out of screenshots and notes.
4. Record the first failing or confusing setup step. A setup failure remains a valid observed blocker and must not be silently skipped.

## Expected behavior

| Step | Expected result with fresh sample data |
|---|---|
| Starting data | Milk 5,000 ml, beans 1,200 g, latte ₩4,500, no paid sales |
| Create two lattes | Open order, ₩9,000 total, no stock change |
| Refresh | Same saved order and total after loading |
| Simulated failed payment | HTTP 402, open order, stock and sales unchanged |
| Successful cash retry | Same order paid, original receipt, milk 4,500 ml, beans 1,164 g |
| Duplicate payment | HTTP 409, no second deduction or sale |
| Convert beans g to kg | Stock 1.164 kg, threshold 0.25 kg, per-latte recipe 0.018 kg |
| Rename/reprice latte and edit its beans as 18 g | Recipe saves as 0.018 kg, price ₩6,000 |
| Open earlier receipt | Caffè Latte, original unit price ₩4,500 and total ₩9,000 |
| Sell one renamed latte | Milk 4,250 ml, beans 1.146 kg, two paid orders and ₩15,000 sales |
| Owner boundary | Anonymous protected inventory/sales requests return 401; authorized owner can access; logout removes access |

The current UI has no dedicated failure button. Use the API docs or an explicitly recorded request with `{"method":"card","result":"failed"}` to exercise simulated failure. Compare against actual baselines if a sample environment has already been used.

## Completion record

The tester records their exact login, date/time KST, commit, browser/device, database/setup, whether the instructions were followed without live coaching, expected and actual values, screenshot/result links, and first failure if any. Put the result in the shared report and link it in Issue #22. If a case fails, name the fix owner and repeat that case after the change.

The existing [automated check script](verify_current.py) and [October 28 results](evidence/2026-10-28/README.md) provide a comparison. They do not replace the named teammate's own observation.
