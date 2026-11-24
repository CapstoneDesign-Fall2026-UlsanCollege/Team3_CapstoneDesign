# Week 12 individual contribution — Ualson Tamang (`ualsom`)

| Environment and date | Status | Expected | Observed |
|---|---|---|---|
| Local · November 24 KST | **Pass** | Two lattes total KRW 9,000. Cash payment deducts 500 ml milk and 36 g beans. A card retry returns HTTP 409 and leaves the receipt, stock and ledger unchanged. | Order #1 totaled KRW 9,000. Cash returned HTTP 200. Milk fell from 5,000 to 4,500 ml and beans from 1,200 to 1,164 g. The card retry returned HTTP 409. The original receipt, one cash payment and both inventory movement rows stayed intact. |
| Deployed demo · November 24 KST | **Blocked** | Receive the 2FA email, sign in, and perform the two-latte check. | I reached the verification-code step. The email did not arrive, even after I requested a new code. I could not proceed to checkout. The deployed total, stock changes and duplicate-payment behavior are unverified. |
| Independent teammate reproduction | **Pending** | A non-author records the milk level before and after one two-latte payment and identifies the environment. | Awaiting the tester’s own result. [Procedure](../ualsom-manual-verification.md) · [Handoff on Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22#issuecomment-7124147327) |

The local runs used Windows, Python 3.13.7, temporary SQLite and simulated payments on base commit [`e89acd3`](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/e89acd3ac1912446144cb93f1dba769ab721ea9f) with the [Week 12 test](../../../smartserve-pos/backend/test_week12_ualsom.py) in the working tree. The original runs passed [1 focused test](../evidence/ualsom-focused.txt) and [47 backend tests](../evidence/ualsom-backend-suite.txt). The [22:26 KST focused rerun](../evidence/ualsom-focused-rerun.txt) passed 1 test in 0.220 s. Each log records the test file’s SHA-256.

The deployed attempt is my manual observation. The deployed commit and the cause of the missing email were not established.
