# Week 10 original QA regression — later CI rerun

**Original Week 10 work:** Ualson Tamang (`ualsom`), November 11, 2026, [PR #23](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/pull/23).  
**New verification date:** November 18, 2026 (Korea time; logs Nov 17 15:37 UTC)  
**GitHub Actions run:** [PR #25, workflow run 44116391737](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/44116391737)  
**Tested PR head:** `340ea390127a440a980f82e0ff0caabb00ba3352` (GitHub Actions checked out the PR merge ref)  
**Environment:** GitHub-hosted Ubuntu runner, Python 3.12, backend dependencies from `requirements.txt`, isolated SQLite test DB  
**Command:** `python -m unittest -v test_issue3 test_owner_management test_trash test_week10_ualsom test_week11_ualsom`

## Exact relevant lines from GitHub Actions backend job log

```text
2026-11-17T15:37:23.1439481Z test_two_lattes_duplicate_payment_same_session (test_week10_ualsom.Week10UalsomTests.test_two_lattes_duplicate_payment_same_session) ... ok
2026-11-17T15:37:23.1536633Z test_two_lattes_retry_from_new_session_does_not_deduct_twice (test_week11_ualsom.UalsomWeek11PaymentRetryTest.test_two_lattes_retry_from_new_session_does_not_deduct_twice) ... ok
2026-11-17T15:37:23.1538543Z Ran 27 tests in 0.381s
2026-11-17T15:37:23.1538949Z OK
```

**Actual:** The Week 10-specific test passed within a 27/27 passing suite. The CI result is **not the original November 11 local execution**; the 0.030-second original self-reported result is separately preserved in [the historical Week 10 note](w10-ualsom-qa-record.md). The newer suite also ran the Week 11 regression, but this does not make it original Week 10 work.

**To repeat the Week 10 test only:** From `smartserve-pos/backend` with dependencies installed, run `python -B -m unittest -v test_week10_ualsom`. Expect one test `... ok`, `Ran 1 test`, `OK`.

**Boundaries:** Isolated SQLite, simulated cash/card payment; not a live payment provider, deployed PostgreSQL validation, or independent teammate reproduction.
