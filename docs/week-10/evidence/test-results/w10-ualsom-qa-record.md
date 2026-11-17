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

**Later CI verification:** Pending from the main-based review branch at the time this note was created; once a run completes, record its exact URL and outcome separately. Do not backdate later CI results to November 11.

**Limitations:** Isolated SQLite and simulated payments. The separate student Week 11 regression is not evidence for the original Week 10 run. Independent non-author repetition remains unrecorded.
