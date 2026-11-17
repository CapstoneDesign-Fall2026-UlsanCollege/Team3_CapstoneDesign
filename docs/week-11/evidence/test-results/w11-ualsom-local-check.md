# Week 11 — ualsom local regression check

**Contributor:** Ualson Tamang (`ualsom`)
**Source:** Terminal output supplied by the student during the guided local run (Windows PowerShell; local working copy)
**Execution location:** `smartserve-pos/backend`
**Command:** `python -B -m unittest -v test_week11_ualsom`
**Test scope:** Two-latte simulated cash payment, inventory deduction, duplicate payment retry from a new database session (isolated SQLite)

## Expected result

Create two Caffè Lattes for ₩9,000. Stock remains unchanged before payment; simulated payment marks order paid, consumes 500 ml milk and 36 g coffee beans, creating one payment and two inventory movements. Retrying payment after reopening the session raises HTTP 409 without further changes.

## Actual result — PASS

The student's first local run failed before these assertions because the seeded Caffè Latte name could not be matched in the copied test file. After restoring the exact UTF-8 test from `origin/main`, the student reran the test and supplied this output:

```text
test_two_lattes_retry_from_new_session_does_not_deduct_twice (test_week11_ualsom.UalsomWeek11PaymentRetryTest.test_two_lattes_retry_from_new_session_does_not_deduct_twice) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.047s

OK
```

**Result:** 1 test passed, 0 failures in the final local rerun. Screenshot capture/upload is separate and pending. The terminal output did not include an exact execution timestamp or commit SHA of the student's local working tree.

**Limitations:** SQLite unit test and simulated payments only, not real payment-provider or deployed-database verification.
