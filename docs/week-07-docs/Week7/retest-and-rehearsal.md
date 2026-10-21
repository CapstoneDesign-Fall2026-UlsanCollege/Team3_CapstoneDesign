# Teammate retest and rehearsal

Status: pending. Use this record for a real non-author test, not the automated run.

Start from [the project setup](../../../smartserve-pos/README.md) on the pushed commit. Use a separate fresh demo database. Do not delete or reset a shared database. Record actual starting stock/sales if they differ from the seed.

1. Confirm milk 5,000 ml, beans 1,200 g and zero sales in the isolated sample database.
2. Create two Caffè Lattes. Expected: ₩9,000 and no deduction before payment.
3. Use simulated failed payment. Expected: order stays open; stock and sales unchanged. Retry with successful cash payment.
4. Check the receipt, inventory and dashboard. Expected: original name; milk 4,500 ml; beans 1,164 g; one sale, ₩9,000. Repeat payment through the API: expected 409 and no extra deduction.
5. Convert beans to kg in owner editing. Expected: stock 1.164 kg, threshold 0.25 kg, latte bean recipe 0.018 kg.
6. Edit the latte name to Latte test and price to ₩6,000. Enter its bean recipe as 18 g using the recipe-unit selector; keep milk at 250 ml. Expected saved bean recipe: 0.018 kg; item remains selectable.
7. Reopen the earlier receipt. Expected: Caffè Latte, ₩4,500 each, ₩9,000 total.
8. Sell one renamed latte. Expected: milk 4,250 ml, beans 1.146 kg, two sales totaling ₩15,000. Save screenshots of the recipe, old receipt and final stock/sales.

| Record | Actual result — tester completes |
|---|---|
| Exact non-author GitHub login | Pending |
| Date/time KST and application commit | Pending |
| Browser/device and starting state | Pending |
| Setup followed without coaching? | Pending |
| Expected/actual values for steps 1–8 | Pending |
| First failure or confusing step | Pending |
| Screenshots or recording | Pending |

For the spoken rehearsal, reset only your isolated demo data, then follow the [four-minute script](midtern-demoscript.md). Record the actual duration; the planned timings are not results.

| Rehearsal record | Actual result — team completes |
|---|---|
| Speakers/tester and commit | Pending |
| Start state and date/time KST | Pending |
| Actual duration | Pending |
| Completed path and fallback result | Pending |
| Proof and remaining limitation | Pending |

`daydevil80` coordinates; `ualsom` is the suggested non-author tester, not yet confirmed. Link the completed record in [Issue #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21).
