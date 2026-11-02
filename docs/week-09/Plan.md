
# Week 9 Work Checklist — Lessons to Final Demo Roadmap

**Date:** Thu 2026-10-29 to Wed 2026-11-04  
**Team:** 3 — SmartServe POS

> Use the evidence and lessons from the first half of the semester to choose a realistic route to the final demo. Every near-term action should have an owner and a checkable result.

## 1. Start from lessons and evidence

### Course lesson

**Lesson:** A feature should not be considered complete just because its code exists. The team should connect each important claim to a test result, screenshot, issue, or reproducible demo.

**Supporting experience:** During the SmartServe POS demo, the team recorded a paid order, receipt, and inventory change. The backend test report also records 12 passing tests.

**Evidence:**
- [Final Demo evidence folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/smartserve-pos/docs/Final-Demo/Evidence)
- [Backend test results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt)

**What the team will change:** Continue attaching evidence to completed work. For each remaining milestone, record what was checked, the result, and any limitation.

### Project lesson 1 — Verify the complete transaction path

**Lesson:** The order, payment, receipt, and inventory deduction should be checked together because a successful order alone does not prove that the whole workflow is correct.

**Supporting experience:** Render Order #4 recorded an Americano ×1 for ₩3,500 with simulated cash payment. The receipt showed payment complete, and coffee bean inventory decreased from 1,128 g to 1,110 g.

**Evidence:**
- [Receipt — Order #4](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png)
- [Inventory after Order #4](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-inventory-after-order-4.png)
- [Paid order history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/08-Owner-Dashboard/render-paid-order-history.png)

**What the team will continue:** Verify important workflows from beginning to end and preserve before-and-after evidence for inventory changes.

### Project lesson 2 — Automated tests and live evidence serve different purposes

**Lesson:** Backend tests help verify logic, while a deployed demo provides evidence that the application can be accessed and used. Neither one replaces the other.

**Supporting experience:** The backend `unittest` report records 12 passing tests. The Render screenshots separately show the Order #4 workflow.

**Evidence:**
- [Backend test results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt)
- [Final Demo evidence folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/smartserve-pos/docs/Final-Demo/Evidence)

**What the team will change:** Keep automated test results and deployed application evidence as separate evidence categories. Add checks for important failure and edge cases before final readiness.

## 2. Set the final demo destination

### Final demo claim

SmartServe POS is designed to help small cafés and food-service businesses manage menu orders, payments, receipts, and ingredient inventory through one point-of-sale workflow.

The final demo will show a cashier selecting a menu item, creating an order, completing a simulated payment, viewing the receipt, and checking the resulting inventory deduction. It will also show the owner-facing information supported by the implemented application.

**Proof required:** A reproducible end-to-end demo, screenshots or recording, relevant automated test results, and clear setup instructions.

### What the demo will not claim

- It will not claim that the payment process is connected to a real payment gateway. The demonstrated payment is simulated.
- It will not claim that the system is production-ready for real businesses without further validation.
- It will not claim that every error state, device, browser, or deployment condition has been tested.
- It will not claim that all features have passed independent user testing unless that testing is completed and recorded.
- It will not claim that inventory or sales reports have been verified beyond the evidence collected.

### Current project state

| Area | Current status | Supporting proof / next check |
|---|---|---|
| Order and payment workflow | Demonstrated | [Order #4 receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png) |
| Receipt generation | Demonstrated for Order #4 | [Receipt screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png) |
| Recipe-based inventory deduction | Demonstrated for the Americano order | [Recipe](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-menu-recipes.png) · [Inventory after order](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-inventory-after-order-4.png) |
| Paid order history | Demonstrated for Order #4 | [Order history screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/08-Owner-Dashboard/render-paid-order-history.png) |
| Backend tests | 12 tests passed in the recorded run | [Test report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt) |
| Error and empty states | Not fully verified by the evidence listed here | Add targeted checks and record results |
| Accessibility and usability | Not yet evidenced in this checklist | Conduct a basic review and record findings |
| Fresh setup and handoff | Instructions exist; independent handoff trial still needed | Test using another teammate or person outside the build work |
| Full final demo rehearsal | Not yet evidenced | Schedule and record rehearsal |

### MVP decision

**Provisional decision: The central order-to-simulated-payment-to-inventory workflow has been demonstrated, but the complete MVP should not be marked fully verified yet.**

Before the Week 11 checkpoint, the team should verify the agreed MVP requirements against the current application and record any gaps.

**Smallest credible path to close the gap by Week 11:**
1. List the agreed MVP requirements and mark each as verified, partly verified, or not verified.
2. Recheck the main cashier workflow from a clean start.
3. Verify important payment and inventory failure cases, including preventing duplicate inventory deduction.
4. Record known bugs with severity, owner, and next action.
5. Decide and document the feature freeze.

## 3. Final Demo Roadmap — Weeks 10–16

| Week | Milestone | Checkable result | Owner | Evidence path | Dependency / risk |
|---|---|---|---|---|---|
| **Week 10** | MVP gap review and verification preparation | MVP requirements reviewed; gaps and high-priority bugs listed | Team lead + feature owners | GitHub Issues; Final Demo Roadmap | Existing requirements and evidence must be reviewed |
| **Week 11** | MVP verification and feature freeze | Main MVP path checked; critical bugs recorded; freeze decision documented | Whole team; issue owners verify their areas | `docs/Final-Demo/` and GitHub Issues | Unresolved critical defects may delay freeze |
| **Week 12** | QA and bug fixing | Main path, validation, error states, and regression checks recorded | Assigned QA and feature owners | QA checklist, test report, bug Issues | Fixes must not introduce regressions |
| **Week 13** | Handoff trial | A teammate or outside reviewer follows setup and demo instructions without relying on the original developer | Documentation owner + reviewer | Setup guide, handoff checklist, reviewer notes | Missing environment variables or unclear setup steps |
| **Week 14** | Demo lock | Final demo path, data, screenshots, roles, and fallback selected; no unapproved feature additions | Whole team | Final Demo guide and evidence folder | Late changes can destabilize the demo |
| **Week 15** | Final readiness | Full rehearsal completed; blockers and fallback checked; all presenters know their roles | Whole team | Rehearsal record, final readiness report | Deployment or network failure |
| **Week 16** | Final demo and handoff | Final demonstration delivered; source, setup, test evidence, known limitations, and handoff materials organized | Whole team | Repository, Final Demo folder, handoff guide | Missing documentation or inaccessible deployment |

### Near-term GitHub Issues to create or update

Create detailed Issues for the next one or two weeks only. Confirm the assignee with the team before assigning.

| Proposed Issue | Priority | Owner | Definition of done |
|---|---|---|---|
| Verify MVP requirements against the deployed SmartServe POS workflow | High | Team lead + relevant feature owners | Each MVP requirement has a status and supporting evidence or a documented gap |
| Test payment and inventory failure cases | High | Backend / payment / inventory owners | Important failure cases are tested; results and bugs are recorded |
| Create a known-bug list with severity and owners | High | Team lead + all feature owners | Each known bug has severity, owner, reproduction details, and next action |
| Review setup and clean-start instructions | Medium | Documentation / deployment owner | Another teammate can follow the instructions and record the result |

*Replace role descriptions with confirmed GitHub usernames when the team assigns the Issues.*

## 4. Biggest risk and fallback plan

**Risk:** The deployed application or network may become unavailable during the final presentation, or a late change may break the main order workflow.

**Prevention:**
- Freeze new features after the Week 11 decision unless a change is essential and approved.
- Keep a known-good version of the project and its setup instructions.
- Recheck the main workflow after important changes.
- Keep screenshots and a short recorded walkthrough of the verified workflow.

**Fallback:** If the deployed application is unavailable, use the documented local Docker setup if it has been tested successfully. If neither live environment works, present the verified screenshots, test report, and recorded walkthrough, clearly explaining that this is recorded evidence rather than a live demonstration.

**Owner:** Team lead and deployment owner — confirm the individual names in GitHub.

## 5. Review and record

### Cross-team roadmap review

- [ ] Compare the SmartServe POS roadmap with another team's roadmap.
- [ ] Explain why Week 11 is the MVP verification and feature-freeze checkpoint.
- [ ] Ask one question that tests a roadmap assumption.
- [ ] Give one specific suggestion tied to evidence, ownership, risk, or a milestone.
- [ ] Revise one unclear part of this roadmap based on feedback.

**Question to ask another team:** What evidence will prove that your MVP is complete, rather than simply showing that the main feature works once?

**Suggested feedback for our roadmap:** Make sure every Week 11 MVP requirement has a named owner and a repeatable verification step. The current Order #4 evidence is useful, but it should not be treated as proof of every possible order or payment scenario.

### Weekly Report

- [ ] Update the team's one shared Week 9 Weekly Report.
- [ ] Each student adds their own contribution and evidence link.
- [ ] Record incomplete work with a reason, owner, and next action.
- [ ] Check that shared evidence contains no passwords, secrets, private information, or unapproved real-user data.

## 6. Evidence to link

- [Final Demo evidence folder](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/smartserve-pos/docs/Final-Demo/Evidence)
- [Order #4 receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/04-Receipts/render-receipt-4.png)
- [Inventory after Order #4](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-inventory-after-order-4.png)
- [Menu recipe evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/05-Inventory/render-menu-recipes.png)
- [Paid order history](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/08-Owner-Dashboard/render-paid-order-history.png)
- [Backend test report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt)
- [Team 3 repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)

## 7. Final Week 9 check

- [ ] Every teammate can explain the final demo claim.
- [ ] Every teammate knows the Week 10–11 milestone and their own next action.
- [ ] The MVP gap review has an owner and a review date.
- [ ] The next one or two weeks have actionable GitHub Issues.
- [ ] The biggest demo risk has a fallback.
- [ ] The roadmap distinguishes demonstrated behavior from unverified behavior.
- [ ] The shared Weekly Report includes a contribution and evidence row from every student.

**Week 9 completion target:** By Wed 2026-11-04, the team should have a realistic final-demo route, a clear MVP verification plan for Week 11, and named owners for the immediate next actions.
