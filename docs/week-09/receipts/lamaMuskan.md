# Week 9 Individual Evidence Receipt — Lama Muskan

**GitHub:** `Sammygit15`  
**Team:** Team 3 — SmartServe POS  
**Week:** 9  
**Focus:** Manual feature checks, automated regression validation and release-readiness evidence

## 1. Manual POS feature checks — November 2, 2026

I opened the POS application and checked the sales dashboard, menu/recipe display, inventory view and payment receipt. The screenshots captured during this check show:

1. **Sales dashboard:** November 2 sales displayed as ₩12,500 across 3 paid orders.
2. **Paid-order list:** Order #2 and #3 are Caffè Latte × 1 at ₩4,500 each (CASH and QR); order #4 is Americano × 1 at ₩3,500 (CASH).
3. **Menu and recipe display:** Americano, Caffè Latte and Milk Tea are listed with their configured ingredient quantities.
4. **Inventory view:** Coffee beans, milk, sugar babies and tea leaves display current stock, reorder levels and OK status.
5. **Receipt view:** Receipt #4 displays Americano × 1, ₩3,500, CASH, with a payment-complete status.

**Evidence:** Four screenshots were captured on November 2, 2026 and supplied with this Week 9 receipt. Add the original image files to the repository evidence folder when preparing the final submission so the instructor can open them directly from GitHub.

**Evidence boundary:** These screenshots document the state visible in the application during the manual check. They do not, by themselves, prove every possible payment, inventory, authorization or failure scenario.

## 2. GitHub Actions validation workflow

- **Contribution:** Added and refined a repeatable GitHub Actions workflow covering backend unit tests, the frontend production build and isolated browser/API transaction regression checks.
- **Implementation evidence:** [Workflow file](../../.github/workflows/week9-validation.yml) · [Browser/API validation script](../run_validation.py) · [Validation documentation](../validation-workflow.md).
- **Successful run:** [Week 9 validation — Run #5](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/41421184139).
- **Result:** All three jobs completed successfully: backend unit tests, frontend production build and browser/API transaction regression. The browser/API job also uploaded its result and screenshot artifact.
- **Troubleshooting:** An earlier run failed because the browser test used a different owner test username from the isolated CI setup. I corrected the test identity and workflow trigger, then checked the subsequent successful run.

**Environment boundary:** The browser/API regression ran against an isolated CI application and temporary SQLite database, not the live Render deployment or a production database. The automated checks are not a substitute for production security, real payment-provider or concurrent-load testing.

## 3. Previous transaction-flow evidence reviewed

The following evidence was produced on October 28, 2026, against application source commit `b68df10eb46d25bc2ac00e28412b71df792deb7f`. The recorded operator was Codex automation at daydevil80's request. I include it as prior team verification context, not as a test I personally executed.

- [October 28 verification summary](../week-08/evidence/2026-10-28/README.md)
- [24 backend unit-test output](../week-08/evidence/2026-10-28/backend-tests.txt)
- [Frontend build output](../week-08/evidence/2026-10-28/frontend-build.txt)
- [27 browser/API expected-versus-actual checks](../week-08/evidence/2026-10-28/browser-results.json)
- [12 screenshot gallery](../week-08/evidence/2026-10-28/SCREENSHOTS.md)

## 4. Learning and next action

The manual checks gave me a direct view of how the dashboard, paid orders, menu recipes, inventory status and receipt are presented together. The automated workflow adds repeatable regression checks and a traceable record of the tested code revision. For the next validation pass, I should compare before-and-after inventory values for a known order and retain the matching screenshots and test output in the repository.
