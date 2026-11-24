# Week 12 Peer Test Notes — SmartServe POS

**Target:** Owner registration signup-email flow  
**Tracking issue:** [#27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27)

## Current status

**Pending.** No independent tester result has been recorded. Do not enter a tester name or PASS result until the teammate performs the check.

## Peer-test record

| Field | Entry |
|---|---|
| Tester GitHub login | Pending |
| Relationship to implementation | Pending |
| Date/time (KST) | Pending |
| Repository commit SHA | Pending |
| Docker image/build provenance | Pending |
| Working tree clean? | Pending |
| Browser / OS | Pending |
| Test account | Safe test identifier only; no password or personal data |
| Result | Not tested |
| Evidence links | Pending |

## Controlled procedure

1. Confirm exact commit and that the tested container was built from that revision.
2. Confirm runtime configuration without exposing credentials or tokens.
3. Start the app and open owner registration.
4. Submit valid test details using a designated test inbox.
5. Record visible result and corresponding API status/logs.
6. If email succeeds, verify receipt and activation behavior without publishing the token.
7. If it fails, capture status and redacted exception.
8. Mark PASS, FAIL, BLOCKED, or NOT TESTED and record expected/actual outcomes.
9. Add the independent result to Issue #27 and link it here.

## Result table

| Check | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| Original registration request | Request accepted and signup email requested | POST returned HTTP 503 | **Fail — original observed run** | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| Email receipt and activation | Test inbox receives email and activation works | Not verified | **Not tested** | Pending |
| Independent repeat after fix | Same controlled scenario passes on identified revision | No peer retest recorded | **Not tested** | Pending |

## Interpretation

- Peer verification must be performed and reported by the peer; documentation assistance is not independent verification.
- A pass on a different setup or revision does not prove the original failure is fixed.
- Exclude secrets, activation tokens, and real customer information from screenshots and logs.
