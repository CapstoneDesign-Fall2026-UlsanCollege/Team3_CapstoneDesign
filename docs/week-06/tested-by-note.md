# Tested-By Note — independent test pending

**Team:** 3 — SmartServe POS  
**Behavior:** Editing menu/ingredient data after stock exists, followed by receipt-history and payment checks  
**Related issue:** [#20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20)  
**Implementation owner:** `daydevil80`  
**Tester other than the author:** Not yet confirmed  
**Independent test date:** Not yet recorded  
**Status:** Incomplete

No teammate has been reported as independently following these written steps yet. The October 14 scripted check is recorded in [automated-check.md](automated-check.md); it does not complete this note.

## Check steps

Follow [test-plan.md](test-plan.md) from its starting data. Record the exact application commit and use separate sample data. Do not reuse the changed data from an earlier test without documenting a reset or adjusted expected values.

## Expected result

Two lattes total ₩9,000. Failed/duplicate payments do not deduct stock. Successful payment deducts 500 ml milk and 36 g beans once. Converting beans to kg preserves the physical amounts and recipes. Menu edits do not change an old receipt's price or name. Editing an 18 g recipe with kg inventory stores 0.018 kg and leaves the item available.

## Actual result — teammate to complete

| Field | Actual information |
|---|---|
| Exact tester GitHub login | Pending |
| Test date/time in Korea | Pending |
| Machine/browser and source commit | Pending |
| Expected-versus-actual values | Pending |
| First confusing or failing step | Pending |
| Screenshot/result link | Pending |
| Whether steps were followed without coaching | Pending |

Do not replace these fields with the automated result or another member's display name. Keep failed criteria unchecked.

## Earlier teammate observations

These are linked for context, not presented as a newly completed independent test:

- `Sammygit15`: [initial editing problem](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20#issuecomment-6054901603), October 8, 16:27:54 KST.
- `Sammygit15`: [editing worked after a fix](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20#issuecomment-6054966665), October 8, 16:31:54 KST.
- `ualsom`: [unit-change screenshots](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20#issuecomment-6055077744), October 8, 16:38:10 KST.

Those comments do not supply the full starting data, expected values, source version, or whether the written October 14 steps were followed without coaching.

## Next action

`daydevil80` arranges the test with a non-author teammate. The tester completes this note and their own contribution row in the shared report. If they find the same failures, record them and link the follow-up problem rather than marking the behavior complete.
