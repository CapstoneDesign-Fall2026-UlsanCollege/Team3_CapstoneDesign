
# Week 9 Work Checklist — Lessons to Final Demo Roadmap

**Date:** Thu 2026-10-29 to Wed 2026-11-04  
**Team:** 3 — SmartServe POS

> Use evidence and lessons from the first half of the semester to choose a feasible route to the final demo. Keep the next step specific and owned.

## 1. Start from lessons and evidence

### Midterm and first-half debrief

- [x] Bring current project evidence, including deployed demo screenshots, backend test results, and project documentation.
- [ ] Review instructor midterm feedback and record the main points.
- [ ] Prepare one question for the instructor about the final-demo roadmap.
- [x] Identify one course lesson about evidence and project progress.
- [x] Identify project lessons from building and testing the SmartServe POS workflow.
- [ ] Discuss and confirm the lessons with the whole team.

### Course lesson

**Lesson:** A feature should not be considered complete simply because it has been implemented. It needs supporting evidence, such as a test result, screenshot, issue, or reproducible demonstration.

**Project application:** Continue connecting completed work to GitHub Issues, test reports, screenshots, and documentation.

**Evidence:**
- [Final Demo Evidence folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/smartserve-pos/docs/Final-Demo/Evidence)
- [Backend test results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt)

### Project lesson 1 — Verify the complete transaction

**Lesson:** An order, payment, receipt, and inventory deduction should be verified together. A successful order by itself does not prove that the complete workflow works.

**Supporting experience:** Render Order #4 recorded an Americano ×1 for ₩3,500 with simulated cash payment. The receipt showed payment complete, and coffee bean inventory decreased from 1,128 g to 1,110 g.

**Evidence:**
- [Order #4 receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png)
- [Inventory after Order #4](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-inventory-after-order-4.png)
- [Paid order history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/08-Owner-Dashboard/render-paid-order-history.png)

**What the team will continue:** Verify important workflows from beginning to end and preserve before-and-after evidence.

### Project lesson 2 — Automated tests and deployed evidence are different

**Lesson:** Automated backend tests verify application logic, while a deployed demo shows that users can access and operate the application. Both types of evidence are important.

**Supporting experience:** The recorded backend test report shows 12 tests passing. Separate Render screenshots demonstrate the Order #4 workflow.

**Evidence:**
- [Backend test report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt)
- [Final Demo evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/smartserve-pos/docs/Final-Demo/Evidence)

**What the team will change:** Record automated test results and live application evidence separately. Add missing error-case and regression checks before the final demo.

## 2. Set the roadmap destination

### Final demo claim

SmartServe POS is designed to help small cafés and food-service businesses manage menu orders, payments, receipts, and ingredient inventory through one point-of-sale system.

The final demo will show:

1. A cashier selecting menu items and quantities.
2. The system calculating the order total.
3. A simulated payment being completed.
4. A receipt being generated.
5. Ingredient inventory being deducted according to the menu recipe.
6. The owner viewing relevant order and inventory information.

**Proof:** A repeatable end-to-end demonstration, screenshots or recording, backend test results, and setup instructions.

### What the final demo will not claim

- Real payment-gateway integration. The demonstrated payment is simulated.
- Production readiness for real businesses without further validation.
- Complete verification of every browser, device, and deployment condition.
- Independent user testing unless it has actually been conducted and recorded.
- Complete error handling or reliability beyond the cases tested and documented.

### Current project state

| Area | Status | Evidence / next check |
|---|---|---|
| Order and simulated payment | Demonstrated for Order #4 | [Receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png) |
| Receipt generation | Demonstrated for Order #4 | [Receipt screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png) |
| Recipe-based inventory deduction | Demonstrated for the Americano order | [Menu recipes](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-menu-recipes.png) · [Inventory after order](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-inventory-after-order-4.png) |
| Paid order history | Demonstrated for Order #4 | [Order history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/08-Owner-Dashboard/render-paid-order-history.png) |
| Backend tests | 12 tests passed in the recorded run | [Test report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt) |
| Error and empty states | Not fully verified by current evidence | Perform targeted checks |
| Accessibility and usability | Not yet evidenced here | Conduct and record a basic review |
| Setup and handoff | Setup instructions exist; independent handoff trial remains to be confirmed | Ask another person to follow the instructions |
| Full final-demo rehearsal | Not yet evidenced | Complete and record rehearsal |

### MVP decision

**Current assessment:** The central order → simulated payment → receipt → inventory deduction workflow has been demonstrated. However, the complete MVP should not yet be marked fully verified until the team checks every agreed MVP requirement.

**Smallest credible path to Week 11:**

- [ ] Compare the current application against the MVP Contract.
- [ ] Mark each requirement verified, partly verified, or not verified.
- [ ] Recheck the main cashier workflow from a clean start.
- [ ] Test important payment and inventory failure cases.
- [ ] Verify that duplicate payment or order actions cannot cause duplicate inventory deduction.
- [ ] Record bugs with severity, owner, and next action.
- [ ] Make and document the Week 11 feature-freeze decision.

## 3. Final Demo Roadmap — Weeks 10–16

| Week | Milestone | Checkable result | Owner | Evidence path | Dependency / risk |
|---|---|---|---|---|---|
| **Week 10** | MVP gap review | MVP requirements compared with current implementation; missing checks identified | Team lead + feature owners | MVP Contract, GitHub Issues | Requirements must be clear |
| **Week 11** | MVP verification and feature freeze | Main workflow verified; critical bugs recorded; freeze decision documented | Whole team | Final Demo docs, test reports, Issues | Critical defects may delay freeze |
| **Week 12** | QA and bug triage | Main path, validation, error states, and regression tests checked | QA owner + feature owners | QA checklist, test report, bug Issues | Fixes may introduce regressions |
| **Week 13** | Handoff trial | Another teammate or outside reviewer follows setup and demo instructions | Documentation owner + reviewer | Setup guide, handoff checklist, reviewer notes | Missing or unclear setup steps |
| **Week 14** | Demo lock | Final demo path, test data, evidence, roles, and fallback confirmed | Whole team | Final Demo guide and evidence folder | Late changes may break the demo |
| **Week 15** | Final readiness | Full rehearsal completed; blockers and fallback reviewed; presentation roles confirmed | Whole team | Rehearsal record, readiness report | Deployment or network failure |
| **Week 16** | Final demo and handoff | Demo delivered; source code, setup, test evidence, known limitations, and handoff materials organized | Whole team | Repository and Final Demo folder | Missing documentation or inaccessible deployment |

### Next one or two weeks — GitHub Issues

Create or update Issues for immediate work. Confirm actual assignees with the team before assigning.

| Proposed task | Priority | Suggested owner | Definition of done |
|---|---|---|---|
| Verify MVP requirements against the current application | High | Team lead + feature owners | Every MVP requirement has a status and evidence or a documented gap |
| Test payment and inventory failure cases | High | Backend / payment / inventory owners | Important failure cases tested and results recorded |
| Create a known-bug list | High | Team lead + feature owners | Every known bug has severity, owner, reproduction details, and next action |
| Review setup and clean-start instructions | Medium | Documentation / deployment owner | Another teammate follows the instructions and records the result |

*Use confirmed GitHub usernames when creating and assigning Issues. Do not assume role suggestions are confirmed assignments.*

## 4. Risks, blockers, and fallback

| Risk / incomplete item | Owner | Next action | Review point |
|---|---|---|---|
| Full MVP requirement coverage is not yet documented here | Team lead + feature owners | Compare the MVP Contract with current evidence and record gaps | Week 11 |
| Payment and inventory failure cases need further verification | Backend / payment / inventory owners | Test failure and duplicate-action scenarios | Week 11 |
| Error, empty-state, and regression checks remain to be recorded | QA owner + feature owners | Complete checks and link results | Week 12 |
| Independent setup and handoff trial is not yet evidenced | Documentation / deployment owner | Ask another person to follow the setup guide | Week 13 |
| Deployed application or network may fail during the final demo | Deployment owner + team lead | Preserve a tested local setup and recorded walkthrough | Before Week 14 |

### Biggest risk and fallback

**Biggest risk:** The deployed application or network may become unavailable during the final presentation, or a late code change may break the main order workflow.

**Prevention:**
- Keep a known-good version of the project.
- Avoid unnecessary feature additions after the Week 11 freeze.
- Retest the main workflow after important changes.
- Keep screenshots and a recorded walkthrough of the verified workflow.

**Fallback:** Use the local Docker setup if it has been tested successfully. If neither live environment works, present the verified screenshots, backend test report, and recorded walkthrough. Explain clearly that this is recorded evidence, not a live demonstration.

## 5. Review and record

### Cross-team roadmap review

- [ ] Compare the SmartServe POS roadmap with another team's roadmap.
- [ ] Explain why Week 11 is the MVP verification and feature-freeze checkpoint.
- [ ] Ask one question that tests a claim or assumption.
- [ ] Offer one specific suggestion tied to evidence, ownership, risk, or a milestone.
- [ ] Revise one unclear part of the roadmap using the feedback.

**Question for another team:** What evidence will prove that your MVP is complete, rather than only showing that its main feature works once?

**Suggestion for SmartServe POS:** Every Week 11 MVP requirement should have a named owner and a repeatable verification step. The Order #4 evidence is useful, but it does not prove every order or payment scenario.

### Shared Weekly Report

- [ ] Update the team's one shared Week 9 Weekly Report.
- [ ] Each student adds their own contribution and evidence link.
- [ ] Record incomplete work with a reason, owner, and next action.
- [ ] Check shared evidence for passwords, secrets, private information, and unapproved real-user data.

## 6. Evidence to link

- [ ] Final Demo Roadmap with lessons, current-state proof, milestones, and owners.
- [ ] Evidence supporting the course and project lessons.
- [ ] GitHub Issues for the next one or two weeks.
- [ ] Risk or blocker record and fallback action.
- [ ] Shared Weekly Report with a contribution and evidence row from every student.

**Existing project evidence:**
- [Final Demo Evidence folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/smartserve-pos/docs/Final-Demo/Evidence)
- [Order #4 receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png)
- [Inventory after Order #4](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-inventory-after-order-4.png)
- [Menu recipes](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-menu-recipes.png)
- [Paid order history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/08-Owner-Dashboard/render-paid-order-history.png)
- [Backend test results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt)
- [Team 3 GitHub repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)

## 7. Stretch work — optional after core work

### Stronger final demo

- [ ] Ask someone outside the development discussion to explain the intended demo after reading the roadmap.
- [ ] Test the local demo fallback and clean-start instructions.
- [ ] Remove obsolete backlog items that do not support the final demo or handoff.

### Stronger quality

- [ ] Choose one evidence-based quality improvement, such as setup reliability, accessibility, or a high-value usability fix.
- [ ] Define a measurable check and owner without weakening the Week 11 feature-freeze target.

## 8. Final Week 9 check

- [ ] Every teammate can explain the final demo claim.
- [ ] Every teammate knows the next milestone, their own action, and the evidence they must produce.
- [ ] The Week 11 MVP verification plan has owners.
- [ ] The next one or two weeks have actionable GitHub Issues.
- [ ] The biggest demo risk has a fallback.
- [ ] The roadmap distinguishes demonstrated behavior from unverified behavior.
- [ ] The shared Weekly Report contains a contribution and evidence row from every student.

**Week 9 completion target:** By Wed 2026-11-04, Team 3 should have a realistic final-demo route, a clear Week 11 MVP verification and feature-freeze plan, and named owners for immediate next actions.
