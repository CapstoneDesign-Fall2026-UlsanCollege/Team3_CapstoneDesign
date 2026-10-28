# Week 8 contribution — daydevil80

**Student:** Sherap Hyolmo

**GitHub login:** `daydevil80`

**Team:** 3 — SmartServe POS

**Date:** October 28, 2026, Korea time

## My Week 8 work

I followed up on the written midterm feedback by arranging fresh technical verification of the existing POS workflow with coding-agent assistance. I requested the automated check; Codex executed the tests and browser run. This receipt does not describe a non-author teammate test.

The verification used application commit `b68df10eb46d25bc2ac00e28412b71df792deb7f`. The check started a separate temporary PostgreSQL database, seeded sample data, and exercised the built frontend against the FastAPI HTTP routes. No shared store data changed.

I also prepared a Week 8 contribution and evidence addendum that connects the results to the course/project lessons, the MVP decision and a specific Week 9 verification milestone. These are additions to the shared documentation, not replacements for teammates' files.

## Results and direct proof

| Work | Actual result | Evidence |
|---|---|---|
| Backend regression suite | 24 tests passed | [Test output](../evidence/2026-10-28/backend-tests.txt) |
| Frontend production build | Passed, with an existing Vite configuration warning | [Build output](../evidence/2026-10-28/frontend-build.txt) |
| Current PostgreSQL browser/API path | 27 checks passed | [Raw expected/actual results](../evidence/2026-10-28/browser-results.json) |
| Two-latte sale | ₩9,000; milk 5,000 to 4,500 ml; beans 1,200 to 1,164 g | [Receipt](../evidence/2026-10-28/07-paid-receipt.png), [inventory](../evidence/2026-10-28/08-final-inventory.png), [sales](../evidence/2026-10-28/09-paid-sales.png) |
| Failure and retry | HTTP 402 leaves the order open with unchanged stock/sales; successful retry pays the same order | [Failure screenshot](../evidence/2026-10-28/06-payment-failure.png), [raw checks](../evidence/2026-10-28/browser-results.json) |
| Duplicate payment | HTTP 409 with no further stock deduction | [Raw checks](../evidence/2026-10-28/browser-results.json) |
| Recipe edit and historical receipt | 18 g saves as 0.018 kg; earlier receipt retains Caffè Latte, ₩4,500 unit price and ₩9,000 total | [Owner view](../evidence/2026-10-28/10-corrected-recipe-owner-view.png), [old receipt](../evidence/2026-10-28/11-original-receipt-after-rename.png) |
| Owner session boundary | Anonymous owner inventory/sales requests return 401; generated test credentials permit access; logout restores denial | [Login screen](../evidence/2026-10-28/02-owner-login.png), [raw checks](../evidence/2026-10-28/browser-results.json) |

## What I learned

Passing existing tests did not cover every data-correctness case. Week 6 recorded a recipe edit saving the wrong physical amount and a menu rename changing receipt labels. The fixes added conversion and original-name snapshots. This week, repeating the path through the browser and PostgreSQL provided evidence beyond the earlier SQLite regression checks.

My Week 9 decision is to keep the scope narrow and coordinate a non-author reproduction of this same flow before expanding features. [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) tracks the milestone. I coordinate it; the team will name the non-author tester before execution.

## Evidence boundaries

Payment remains simulated. This run does not establish public deployment, production security, concurrent-load behavior or a narrated presentation. Older original receipt names never stored cannot be reconstructed. Local owner-session protection is checked; it is more precise than the earlier Week 7 statement that owner access had no protection.

[Week 8 addendum](../week8-addendum.md) · [Evidence index](../evidence/2026-10-28/README.md) · [Repeatable check script](../verify_current.py)
