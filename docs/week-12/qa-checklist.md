# Week 12 QA Checklist — SmartServe POS

**Team:** 3  
**Period:** November 19–25, 2026 (KST)  
**Repository HEAD reviewed:** e89acd3ac1912446144cb93f1dba769ab721ea9f  
**Primary QA target:** Owner registration email flow — [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27).

## Scope

Verify that an owner can submit registration and receive the configured signup/activation email, or receive a clear actionable response if delivery is unavailable. Do not treat HTTP 503 as success.

The November 23 café, retail, appointment, and repair checks are historical regression evidence from SHA bcd1f3a12c8891d3a669fdd9f4e96251f500d3de. They are not a retest on the November 24 repository HEAD.

## Environment and revision

| Field | Recorded value |
|---|---|
| Test date | November 24, 2026 (KST) |
| Runtime | Local Docker Compose |
| Backend | FastAPI API container |
| Repository HEAD | e89acd3ac1912446144cb93f1dba769ab721ea9f |
| Working-tree caveat | backend/app/tenancy.py had an uncommitted local modification. Available evidence does not establish whether that edit was mounted into the running API container or which exact image was running. |
| Browser result | “Signup email is temporarily unavailable. Please try again later.” |
| API log excerpt | OPTIONS /auth/register returned 200; POST /auth/register returned 503 |
| Independent tester | Pending |

## Test cases

| ID | Action | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|
| W12-AUTH-01 | Submit valid owner registration details to request signup email | Configured signup-email flow completes, or a clear actionable delivery error is returned | Frontend displayed temporary email-unavailable message | **Fail** | [Issue #27 screenshot/report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| W12-AUTH-02 | Inspect API log for registration request | Success or traceable error identifying underlying failure | OPTIONS returned 200; POST returned 503. Captured excerpt did not include exception | **Blocked — root cause unknown** | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| W12-AUTH-03 | Repeat after confirmed fix under same controlled setup | Signup email succeeds or actionable error is returned | Not repeated after a fix | **Not tested** | Pending |
| W12-AUTH-04 | Independent teammate repeats signup check | Tester login, timestamp, exact revision/environment, expected/actual, evidence | No independent result recorded | **Not tested** | Pending |
| W12-REG-01 | Pay for two Caffè Lattes at ₩4,500 each | One ₩9,000 receipt; milk −500 ml; beans −36 g | Receipt #1 showed Caffè Latte ×2, ₩9,000 cash; milk 5,000→4,500 ml; beans 1,200→1,164 g | **Pass — historical local run** | Weekly report, Nov 23, SHA bcd1f3a |
| W12-REG-02 | Pay with insufficient milk | HTTP 409; no payment or inventory movement | HTTP 409; stock unchanged; zero payment records and movements | **Pass — historical local run** | Weekly report, Nov 23, SHA bcd1f3 |
| W12-REG-03 | Retry payment on already-paid order | HTTP 409; no second stock deduction | HTTP 409; stock remained at post-payment quantities | **Pass — historical local run** | Weekly report, Nov 23, SHA bcd1f3 |
| W12-REG-04 | Sell one stocked retail item | Receipt matches item/quantity/price; stock −1 | Cotton T-shirt ×1, ₩19,000 cash; stock 40→39 | **Pass — historical local run** | Weekly report, Nov 23, SHA bcd1f3 |
| W12-REG-05 | Complete appointment and repair checkout | Receipt displayed; linked work reaches Completed | Both workflows displayed receipts and returned completed | **Pass — historical local run** | Weekly report, Nov 23, SHA bcd1f3 |

## Defect and retest rules

- Issue #27 tracks the signup 503. Root cause is unknown; provider configuration, connectivity, and exception handling are investigation hypotheses, not confirmed causes.
- Do not close the issue based only on a later successful attempt. Repeat the same controlled conditions and record revision, environment, request outcome, and email-delivery evidence.
- Keep historical November 23 transaction results tied to their original SHA.
- Record bug severity separately from work priority. Every open priority item needs an owner and next check.

## Evidence still required

1. Redacted traceback for a controlled registration request.
2. Runtime image/build provenance and confirmation whether the local tenancy edit was mounted.
3. Post-fix browser screenshot and corresponding API output.
4. Independent teammate retest.
5. Link each real artifact from evidence-index.md.
