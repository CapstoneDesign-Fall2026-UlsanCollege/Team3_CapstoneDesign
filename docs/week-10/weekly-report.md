# Weekly Report — Week 10: SmartServe POS MVP Verification and Final Demo Preparation

**Course:** Capstone Design — Fall 2026  
**Team:** Team 3 — SmartServe POS  
**Week:** 10  
**Date:** Thursday, November 5, 2026  
**Repository:** [Team 3 GitHub Repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)  
**Working Branch:** `smartserve-mvp`  
**Report status:** Team draft — individual entries must be confirmed by each member

---

## 1. This Week's Goal

Prepare SmartServe POS for the final MVP stage by reviewing the current implementation, checking the main order-to-payment-to-inventory workflow, identifying unfinished verification, and organizing evidence for the final demonstration.

The focus is to make the existing POS workflow reliable and easy to demonstrate rather than adding features that are not required for the MVP.

## 2. What We Committed to Do

- Review the current GitHub commits and record each member's actual code and documentation contributions.
- Review and document AI-assisted development activities, including who requested the work, what was generated or changed, and who reviewed the result.
- Recheck the cashier workflow: menu selection, order creation, simulated payment, receipt generation, and recipe-based inventory deduction.
- Verify failed-payment recovery and duplicate-payment protection without allowing extra stock deduction.
- Compare inventory values before and after a known paid order and retain the matching evidence.
- Review owner/manager functions, menu and recipe editing, inventory, sales history, and receipt display.
- Identify remaining MVP gaps and update the final completion roadmap for Weeks 10–16.
- Prepare the next independent, non-author verification of the frozen SmartServe transaction path.

## 3. Evidence Links

If it is not linked, it does not count. Links below point to existing project records; pending tasks are not presented as completed.

| Evidence | Link | What it supports |
|---|---|---|
| Main repository | [Team3_CapstoneDesign](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign) | Source code and project documentation |
| Working branch | [smartserve-mvp](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/smartserve-mvp) | Main development branch |
| Week 9 validation workflow | [week9-validation.yml](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/.github/workflows/week9-validation.yml) | Backend, frontend, and browser/API CI jobs |
| Successful CI run | [Week 9 validation — Run #5](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/41421184139) | Successful result for all three jobs |
| Browser/API validation script | [run_validation.py](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-09/run_validation.py) | Repeatable isolated transaction regression |
| Validation notes | [Week 9 validation workflow](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-09/validation-workflow.md) | Scope and limitations of the automated checks |
| Manual POS screenshots | [Week 9 evidence folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-09/evidence) | Dashboard/order history, menu/recipes, inventory, and receipt |
| Individual evidence receipt | [Lama Muskan — Week 9](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-09/receipts/lamaMuskan.md) | Manual checks and CI contribution evidence |
| Week 8 project review | [Week 8 weekly report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-08/weekly-report.md) | Previous MVP assessment and lessons |
| MVP verification milestone | [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) | Non-author reproduction and contribution confirmations |
| Earlier verification follow-up | [Issue #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21) | Frozen two-latte demo path and outstanding checks |
| Menu/inventory edit follow-up | [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20) | Editing behavior and historical data consistency |
| Commit history | [GitHub commits](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commits/main) | Traceable implementation and documentation changes |

## 4. Current Feature Check Summary

The following is a summary of the evidence currently available. It distinguishes the November 2 manual screenshots from the isolated CI regression; neither should be described as a complete production acceptance test.

| Feature / workflow | Current evidence or result | Status |
|---|---|---|
| Sales dashboard | November 2 screenshot shows ₩12,500 across 3 paid orders | Manually viewed |
| Paid-order history | Screenshot shows orders #2–#4 with item, price, and payment method | Manually viewed |
| Menu and recipes | Screenshot shows Americano, Caffè Latte, and Milk Tea with configured ingredient quantities | Manually viewed |
| Inventory view | Screenshot shows coffee beans, milk, sugar babies, and tea leaves with stock/reorder values and OK status | Manually viewed |
| Receipt | Receipt #4 shows Americano ×1, ₩3,500, CASH, payment complete | Manually viewed |
| Simulated payment and inventory regression | CI browser/API job checks failed payment, retry, duplicate payment, stock deduction, receipt/history, and sales behavior in an isolated test environment | Automated CI passed |
| Backend unit tests | Backend test job completed successfully in CI Run #5 | Automated CI passed |
| Frontend production build | Frontend build job completed successfully in CI Run #5 | Automated CI passed |
| Independent teammate reproduction on the demo setup | Required by Issue #22; no completed non-author result is linked yet | Pending |
| Real payment processing | Payment is simulated; no payment provider integration is claimed | Out of MVP scope |

**Important environment boundary:** Week 9 CI Run #5 used an isolated application and temporary SQLite database. It did not test the live Render database or prove production security, real payment processing, or concurrent-load behavior. The November 2 screenshots document the visible deployed POS screens, but they do not independently prove every payment failure or duplicate-request scenario.

## 5. Individual Contribution Entries — One Row per Student

Each student should complete their own entry and add direct evidence links. Do not copy another member's work into your own entry. AI-assisted work must be identified honestly, including the person who requested it and the person who reviewed or tested the result.

| Student | What they did this week | Evidence link |
|---|---|---|
| **Lama Muskan — Sammygit15** | Added and refined the Week 9 GitHub Actions validation workflow, including backend tests, frontend build, and isolated browser/API transaction regression. Corrected the CI test login mismatch and workflow trigger, checked successful Run #5, manually reviewed the deployed POS dashboard, paid-order history, menu/recipes, inventory, and receipt on November 2, and documented the results with screenshots in the Week 9 receipt. | [Week 9 individual receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-09/receipts/lamaMuskan.md) · [Run #5](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/41421184139) · [Workflow commit history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commits/main) |
| **Sherap Hyolmo — daydevil80** | Add this week's work and evidence. Earlier Week 8 automated verification was performed by Codex at daydevil80's request; keep that attribution clear and do not present it as a teammate's independent test. | [Week 8 report and evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-08/weekly-report.md) |
| **Shuzita Majhi — Shuzita** | To be completed by the student: record the checks personally performed, findings, and any issue raised. | Pending |
| **Shreya — shrey776** | To be completed by the student: record the checks personally performed, findings, and any issue raised. | Pending |
| **Ualson Tamang — ualsom** | To be completed by the student: record the checks personally performed, findings, and any issue raised. | Pending |

## 6. Blockers or Risks

| Blocker / risk | Owner | Next action |
|---|---|---|
| Independent non-author reproduction of the frozen transaction path is not yet evidenced. | Team; coordinator recorded in Issue #22 | Confirm a teammate who did not author the fixes, then record exact setup, tested commit, expected/actual values, and screenshots. |
| Before-and-after inventory proof for a known paid order needs to be retained together. | Assigned tester / team | Record starting stock, paid order, ending stock, and matching inventory movement evidence. |
| CI uses temporary SQLite rather than the deployed PostgreSQL environment. | Team | Keep the environment distinction explicit and run the agreed demo-environment verification separately. |
| Payment is simulated, not processed by a real payment gateway. | Team | Keep simulated payment clearly labelled in the MVP and final presentation. |
| Production security and concurrent-load behavior are not established by the current checks. | Team | Do not claim these as verified; document them as limitations unless separately tested. |
| Individual contribution and AI-use records are incomplete until every member confirms their own entry. | All team members | Each member adds their actual work, evidence, AI-use disclosure where relevant, and a short reflection. |

## 7. Decision Record

| Decision | Why we chose it | Owner | Evidence / issue |
|---|---|---|---|
| Prioritize verification of the existing POS workflow over adding unrelated features. | A stable, reproducible order-to-payment-to-inventory flow is the core MVP demonstration. | All team members | [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) |
| Keep payment described as simulated. | The current implementation does not process real payments through a payment provider. | All team members | [Week 8 weekly report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-08/weekly-report.md) |
| Treat CI results and deployed manual checks as different evidence. | The CI run uses isolated test data and SQLite, while manual screenshots show the deployed interface. | All team members | [Week 9 validation notes](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-09/validation-workflow.md) |
| Do not mark the MVP verification milestone complete until a non-author teammate records the handoff result. | Automated developer checks do not replace independent reproduction. | All team members | [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) |
| Keep each member's contribution and AI-assisted work separately attributed. | The report must show who performed, requested, reviewed, and verified each task. | All team members | [Commit history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commits/main) |

## 8. Next Week's Bridge Tasks — Week 11

- Complete the non-author reproduction of the frozen SmartServe transaction path.
- Test a known order from starting inventory through simulated payment, receipt, and ending inventory.
- Verify failed payment leaves the order open and does not deduct stock; verify a successful retry deducts stock once; verify a duplicate payment does not deduct stock again.
- Record the exact tested commit, environment, starting values, expected/actual results, and screenshots.
- Review any failures and create small follow-up issues with an owner and retest evidence.
- Review all five members' contribution entries and AI-use records.
- Update the Weeks 10–16 project completion roadmap based on the actual remaining MVP work.

---

## 9. Team Conclusion

Week 10 should move SmartServe POS from developer-side verification toward a team-reproducible MVP demonstration. The current evidence shows that the main screens are available and that the automated backend, frontend, and isolated browser/API checks passed in CI Run #5. The main remaining proof is an independently recorded run of the frozen transaction path in the agreed demo environment, with clear before-and-after inventory evidence. The team will keep the scope focused on completing and explaining the existing POS workflow.
