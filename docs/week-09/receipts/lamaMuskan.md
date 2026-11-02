# Week 9 Individual Evidence Receipt — Lama Muskan

**GitHub:** `Sammygit15`  
**Team:** Team 3 — SmartServe POS  
**Week:** 9  
**Focus:** MVP validation, regression evidence and release-readiness review

## 1. Week 9 validation workflow

- **Contribution:** Added a repeatable GitHub Actions validation workflow for the backend unit tests, frontend production build and isolated browser/API transaction regression checks.
- **Evidence:** [Workflow file](../../.github/workflows/week9-validation.yml) · [Week 9 validation documentation](validation-workflow.md) · [Run history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/workflows/week9-validation.yml).
- **Verification status:** Results must be taken from the actual completed Actions run. Do not mark a job as passed until its run summary confirms success.

## 2. Previous transaction-flow evidence reviewed

The following evidence was produced on October 28, 2026, against application source commit `b68df10eb46d25bc2ac00e28412b71df792deb7f`. The recorded operator was Codex automation at daydevil80's request. I include it as prior team verification context, not as a test I personally executed.

- [October 28 verification summary](../week-08/evidence/2026-10-28/README.md)
- [24 backend unit-test output](../week-08/evidence/2026-10-28/backend-tests.txt)
- [Frontend build output](../week-08/evidence/2026-10-28/frontend-build.txt)
- [27 browser/API expected-versus-actual checks](../week-08/evidence/2026-10-28/browser-results.json)
- [12 screenshot gallery](../week-08/evidence/2026-10-28/SCREENSHOTS.md)

### Previously recorded scenarios

1. Cashier creates two lattes and an unpaid order is saved for ₩9,000.
2. Refresh restores the saved order.
3. Failed simulated payment returns HTTP 402; order, inventory and sales remain unchanged.
4. Successful retry returns HTTP 200; milk and coffee beans are deducted once.
5. Repeated payment returns HTTP 409 and does not deduct stock again.
6. Recipe edit converts 18 g to 0.018 kg.
7. Historical receipt retains the original Caffè Latte name and ₩4,500 saved price after menu rename.
8. A second paid sale updates stock and sales totals correctly.
9. Anonymous protected requests return HTTP 401; login grants the local owner session and logout removes it.

## 3. Scope and evidence boundaries

- The October 28 results are earlier automated developer verification, not a new Week 9 run and not my independent test.
- The Week 9 GitHub Actions run will create a separate result set and screenshots using isolated sample data.
- Payments are simulated. These checks do not establish real payment-provider behavior, production security, public deployment reliability or concurrent-load performance.
- Record any failure as well as passing results; do not omit failed checks.

## 4. Learning and next action

The key release-readiness question is whether the order, payment, receipt, inventory movement and sales records agree across success, failure and retry paths. The evidence should make each expected value comparable with the actual result and identify the application commit and test environment.
