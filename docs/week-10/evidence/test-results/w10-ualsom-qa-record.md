# Week 10 — `ualsom` payment and inventory QA evidence

**Original reporting date:** November 11, 2026  
**Contributor:** Ualson Tamang (`ualsom`)  
**Declared area:** Backend QA — simulated payment and inventory integrity  
**Original source:** [PR #23](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/pull/23) and its [test file](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/ualsom/week10-qa/smartserve-pos/backend/test_week10_ualsom.py)

## Bounded step

In an isolated SQLite test database, seed demo menu and inventory; create one two-latte order; simulate a successful cash payment; retry with card **in the same session**; inspect the stock and payment/ledger counts.

| Verification | Expected result | Evidence / status |
|---|---|---|
| Initial simulated cash payment | Order is paid; 500 ml milk and 36 g beans deducted | Assertions in `test_week10_ualsom.py`; original PR reports local PASS |
| Duplicate simulated payment | HTTP 409; stock unchanged on retry | Asserted by the same unit test |
| Database integrity | 1 payment; 2 inventory movement rows | Asserted by the same unit test |

## Original recorded result

**PASS — 1 test in 0.030 seconds**, reported by the contributor on November 11 in [PR #23](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/pull/23) and the [Week 10 contribution record](../../contribution-record.md). The original command output and exact local tested SHA were not separately archived, so this is a **historical self-reported result**, not a newly verified raw execution log.

## Repeatable command

From `smartserve-pos/backend`, after installing `requirements.txt` in your virtual environment:

```powershell
python -B -m unittest -v test_week10_ualsom
```

Expected terminal result: `test_two_lattes_duplicate_payment_same_session ... ok`, `Ran 1 test`, `OK`.

**Later CI verification:** **PASS** in [PR #25 run 44116391737](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/44116391737), November 18 KST. The backend job log explicitly shows `test_two_lattes_duplicate_payment_same_session ... ok` and `Ran 27 tests ... OK`. [Recorded log excerpt and environment](w10-ualsom-ci-rerun.md). This is separate from, and must not be backdated to, the November 11 self-reported local result.

**Later student-run local verification:** A subsequent Windows PowerShell execution of `python -B -m unittest -v test_week10_ualsom` passed with `test_two_lattes_duplicate_payment_same_session ... ok`, `Ran 1 test in 0.086s`, and `OK`. [Uploaded terminal screenshot](../screenshots/w10-ualsom-local-test-pass.png) is a cropped and palette-optimized excerpt of the student's actual attachment; the original unedited screenshot remains in the conversation. This rerun was not performed during the original Week 10 reporting period and the local tested commit was not captured.

**Limitations:** Isolated SQLite and simulated payments. The separate student Week 11 regression is not evidence for the original Week 10 run. Independent non-author repetition remains unrecorded.
