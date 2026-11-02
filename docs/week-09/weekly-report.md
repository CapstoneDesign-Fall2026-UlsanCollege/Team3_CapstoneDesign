# Weekly Report — Week 9: POS Workflow Checks and Automated Validation

**Course:** Capstone Design — Fall 2026  
**Team:** Team 3 — SmartServe POS  
**Week:** 9  
**Evidence date:** November 2, 2026  
**Repository:** [Team 3 GitHub Repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)  
**Branch used for Week 9 validation:** `main`

---

## 1. This Week's Goal

The goal for Week 9 was to continue the post-midterm MVP work by checking the existing SmartServe POS features and improving the repeatability of project validation.

The team focus was to:

- Review the cashier and owner-facing POS screens.
- Check that sales, paid-order history, menu recipes, inventory, and receipts display the expected information.
- Improve repeatable validation of the backend, frontend, and main transaction flow.
- Keep evidence linked to the repository so that project progress can be reviewed.
- Identify remaining verification work instead of treating the MVP as complete based only on a successful build or screenshots.

## 2. Work Completed and Evidence

### 2.1 Manual POS feature review

On November 2, the following application screens were opened and reviewed. The screenshots record the visible application state at the time of the check.

| Feature reviewed | Observed result | Evidence |
|---|---|---|
| Sales dashboard and paid-order history | Sales for November 2 displayed **₩12,500** across **3 paid orders**. Orders #2 and #3 were Caffè Latte ×1 at ₩4,500 each (CASH and QR); order #4 was Americano ×1 at ₩3,500 (CASH). | [Dashboard and paid-order history](evidence/render-paid-order-history.png) |
| Menu and recipe display | Americano, Caffè Latte, and Milk Tea were displayed with their configured ingredient quantities. | [Menu and recipes](evidence/render-menu-recipes.png) |
| Inventory view | Coffee beans, milk, sugar babies, and tea leaves showed current stock, reorder levels, and OK status. | [Inventory after order #4](evidence/render-inventory-after-order-4.png) |
| Receipt | Receipt #4 displayed Americano ×1, ₩3,500, CASH, and payment complete. | [Receipt #4](evidence/render-receipt-4.png) |

These screenshots demonstrate what was visible in the application. They do not, by themselves, prove all transaction edge cases or production behavior.

### 2.2 Automated validation workflow

A GitHub Actions workflow was added and refined to make three validation stages repeatable:

1. **Backend unit tests**
2. **Frontend production build**
3. **Isolated browser/API transaction regression**

The browser/API regression script starts an isolated application and exercises important transaction behavior, including order creation, failed payment, successful retry, duplicate payment protection, inventory deduction, recipe unit conversion, historical receipt information, sales totals, and local owner-session behavior.

**Successful validation:** [GitHub Actions Run #5](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/41421184139)

All three jobs in Run #5 completed successfully. The browser/API job also uploaded its result and screenshot artifact.

The earlier Run #4 failed because the browser test used an owner login name that did not match the account created by the isolated CI setup. The test identity and workflow trigger were corrected before the subsequent successful run.

**Environment limitation:** The Week 9 browser/API CI run used an isolated application and temporary SQLite database. It did not use the live Render database and does not establish real payment-provider processing, production security, or concurrent-load behavior.

### 2.3 Implementation and documentation links

- [Week 9 GitHub Actions workflow](../../.github/workflows/week9-validation.yml)
- [Week 9 browser/API validation script](run_validation.py)
- [Week 9 validation workflow notes](validation-workflow.md)
- [Week 9 individual evidence receipt — Lama Muskan](receipts/lamaMuskan.md)
- [Week 9 screenshot evidence folder](evidence/)

## 3. Current MVP Status

| Area | Week 9 evidence | Assessment |
|---|---|---|
| Sales dashboard and paid-order history | Manually viewed and screenshots retained | Evidence captured |
| Menu and recipe display | Manually viewed and screenshot retained | Evidence captured |
| Inventory display | Manually viewed and screenshot retained | Evidence captured |
| Receipt display | Manually viewed and screenshot retained | Evidence captured |
| Backend tests | CI Run #5 backend job passed | Automated check passed |
| Frontend production build | CI Run #5 frontend job passed | Automated check passed |
| Browser/API transaction regression | CI Run #5 browser/API job passed in isolated SQLite environment | Automated check passed |
| Independent teammate reproduction | No completed non-author result is linked in this report | Still pending |
| Real payment gateway | Current payment flow is simulated | Not part of current verified scope |
| Production security and concurrent-load testing | Not established by the Week 9 evidence | Not verified |

**MVP assessment: Still has a gap.** Week 9 provides useful manual screen evidence and a successful automated validation run. The team should not mark the complete MVP transaction workflow as independently verified until a non-author teammate records the agreed reproduction and its results.

## 4. Individual Contributions

Each member should confirm their own entry and attach links to work they personally completed. Do not attribute another member's commits, AI-assisted work, or tests to yourself.

### Lama Muskan — `Sammygit15`

- Added and refined the Week 9 GitHub Actions validation workflow for backend tests, frontend production build, and isolated browser/API transaction regression.
- Corrected the CI browser-test login mismatch and workflow trigger, then checked the subsequent successful Run #5.
- Opened and reviewed the POS sales dashboard, paid-order history, menu/recipes, inventory view, and receipt on November 2.
- Recorded the visible results with screenshots and documented the manual checks and CI evidence in the Week 9 individual receipt.

**Evidence:**
- [Individual Week 9 receipt](receipts/lamaMuskan.md)
- [Successful CI Run #5](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/41421184139)
- [Workflow file](../../.github/workflows/week9-validation.yml)
- [Validation script](run_validation.py)
- [Screenshot evidence](evidence/)

### Sherap Hyolmo — `daydevil80`

**Contribution:** To be completed and confirmed by the member.

Add the actual Week 9 work, the member's role in any AI-assisted task, and direct evidence links. Earlier October 28 automated verification was recorded as Codex automation at daydevil80's request; do not describe that earlier run as a personal manual test or as another teammate's independent verification.

### Shuzita Majhi — `Shuzita`

**Contribution:** To be completed and confirmed by the member.

Add the actual Week 9 work, any personally reviewed or executed checks, findings, and direct evidence links.

### Shreya — `shrey776`

**Contribution:** To be completed and confirmed by the member.

Add the actual Week 9 work, any personally reviewed or executed checks, findings, and direct evidence links.

### Ualson Tamang — `ualsom`

**Contribution:** To be completed and confirmed by the member.

Add the actual Week 9 work, any personally reviewed or executed checks, findings, and direct evidence links.

## 5. Issues and Remaining Work

| Remaining item | Why it matters | Next action |
|---|---|---|
| Independent teammate reproduction | Developer/CI checks do not replace a separate teammate following the verification steps | Assign a non-author tester and record the exact tested commit, environment, expected/actual results, and screenshots |
| Before-and-after stock evidence | Screenshots of current stock alone do not prove the exact quantity deducted by a known order | Record starting stock, the order and recipe, ending stock, and matching inventory movement |
| Demo environment verification | CI used isolated SQLite rather than the live Render database | Run the agreed manual check in the demo environment and clearly record the environment |
| Individual contribution records | Team assessment requires each person's actual contribution to be identifiable | Have every member complete and confirm their own section |
| Payment scope | The current flow is simulated | Keep the limitation explicit; do not claim real payment processing |

## 6. Decisions

1. Continue prioritizing the existing order-to-payment-to-inventory workflow rather than expanding into unrelated features.
2. Keep automated CI results, deployed-interface screenshots, and independent teammate testing clearly distinguished.
3. Treat the current payment flow as simulated.
4. Do not claim production security, real payment processing, or concurrent-load validation without separate evidence.
5. Keep each member's work and any AI-assisted contribution accurately attributed.

## 7. Next Week's Bridge Tasks — Week 10

- Complete the independent non-author reproduction of the agreed transaction path.
- Record starting and ending inventory values for a known paid order.
- Confirm that a failed payment leaves the order unpaid/open and does not deduct stock.
- Confirm that a successful retry deducts the required ingredients once.
- Confirm that a duplicate payment attempt does not cause another deduction.
- Compare the receipt, order history, sales total, and inventory movement for the same transaction.
- Record the tested commit, environment, expected/actual results, screenshots, and any failure.
- Complete and review all five individual contribution entries.

## 8. Week 9 Conclusion

Week 9 added traceable validation evidence for SmartServe POS. The manual screenshots show the dashboard, paid-order history, menu and recipes, inventory view, and receipt. GitHub Actions Run #5 passed its backend, frontend, and isolated browser/API jobs. The main remaining gap is independent reproduction of the transaction workflow with clear before-and-after inventory evidence. The next stage should focus on closing that verification gap and preparing a reliable MVP demonstration.
