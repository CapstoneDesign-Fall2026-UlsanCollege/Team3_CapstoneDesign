
# Weekly Report — Week 8: Midterm Gate, Feedback Review & MVP Scope Reset

**Course:** Capstone Design — Fall 2026  
**Team:** Team 3 — SmartServe POS  
**Week:** 8 (Midterm Gate Checkpoint)  
**Date:** Wednesday, October 28, 2026  
**Status:** Midterm presentation completed  
**Repository:** [Team3_CapstoneDesign](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign)  
**Working Branch:** `smartserve-mvp`

---

## 1. This Week's Goal

The goal for Week 8 was to review the SmartServe POS project following the midterm presentation, assess the current implementation, identify remaining MVP gaps, and establish development priorities for the next stage.

The team focused on reviewing the existing point-of-sale workflow, evaluating the connection between order processing, simulated payment, and inventory management, and identifying areas that require further testing and improvement.

Rather than expanding the project with unnecessary features, the focus is on completing and verifying the main POS workflow.

---

## 2. Post-Midterm Lessons Learned

### Lesson 1: Course Lesson — Focus on a Verifiable MVP

- **Reflection:** A project does not become more complete simply by adding more features. A smaller workflow that can be clearly demonstrated and verified provides stronger evidence of implementation progress.
- **What We Learned:** The team should prioritize the main user workflow and make sure that each important step works consistently.
- **Week 9 Decision:** Focus on completing and testing the existing SmartServe POS workflow before considering additional features.

### Lesson 2: Project Lesson — Order and Inventory Consistency

- **Reflection:** A POS system must maintain consistency between order information, payment status, and inventory records. Recording an order alone is not enough if the related stock changes are not handled correctly.
- **What We Learned:** Payment confirmation and recipe-based inventory deduction must be handled carefully to avoid incorrect or repeated stock changes.
- **Week 9 Decision:** Continue verifying the transaction workflow, including payment status, inventory deduction, and inventory movement records.

---

## 3. Current Project Proof

The current SmartServe POS implementation is organized around the following workflow:

1. **Menu Selection:** Users select menu items and enter quantities.
2. **Order Calculation:** The system calculates the order total using stored item prices.
3. **Order Creation:** The system creates a unique order record.
4. **Simulated Payment:** Payment confirmation updates the order status to `paid`.
5. **Inventory Deduction:** Recipe ingredients are deducted from inventory after successful payment.
6. **Inventory Movement Records:** Stock changes are recorded through inventory movement records.

The project also includes work on recipe management and order item history.

**Previously documented evidence:**

- Recipe editing was improved to convert units before saving and comparing ingredient quantities.
- Order records were improved to preserve item names and saved prices at the time of order creation.
- The Week 7 contribution record identifies backend tests in `smartserve-pos/backend/test_owner_management.py` and reports that 24 backend tests passed.
- Commit `67cf5d0` is associated with payment and inventory verification work.

These are previously documented results and should not be treated as new Week 8 test results.

---

## 4. MVP Status Assessment: Still Has a Gap

The project has implemented important parts of the POS workflow, but further verification and improvement are required before considering the MVP complete.

| What Is Implemented or Previously Documented | What Still Requires Attention |
|---|---|
| Menu item selection and quantity handling | Verify different order combinations and quantities |
| Order total calculation using stored prices | Verify price accuracy in different order scenarios |
| Unique order creation | Verify order creation and duplicate-submission handling |
| Simulated payment status update | Define and verify the payment boundary |
| Recipe-based inventory deduction | Verify stock deduction for different recipes |
| Inventory movement records | Verify that movements match actual stock changes |
| Recipe unit conversion improvements | Test additional unit conversion cases |
| Saved item names in order records | Verify receipt and order history consistency |

**MVP Assessment:** The project has an implemented core workflow, but it should remain classified as **Still Has a Gap** until the complete transaction flow and its important edge cases are verified.

---

## 5. Main Focus Milestone for Sprint 2 (Week 9–11)

### Milestone 1: Complete and Verify the SmartServe POS Transaction Workflow

- **Objective:** Ensure that menu selection, order creation, simulated payment confirmation, and recipe-based inventory deduction work together consistently.
- **Main Focus:** Verify the relationship between order status, payment confirmation, inventory deduction, and inventory movement records.
- **Additional Focus:** Improve error handling and test important edge cases involving quantities, recipes, and repeated requests.
- **Success Signal:** A test order can be created, marked as paid through the simulated payment flow, and have its required ingredients deducted exactly once, with corresponding inventory movement records.

This milestone focuses on the existing SmartServe POS functionality rather than introducing a new payment provider or unrelated features.

---

## 6. Week 8 Deliverables

- Review the project following the midterm presentation.
- Record lessons learned from the course and technical implementation.
- Assess the current MVP status.
- Identify the remaining gaps in the main POS workflow.
- Establish priorities for Weeks 9–11.
- Define expected behavior for completing and verifying the transaction workflow.
- Organize available project evidence and individual contributions.

---

## 7. Evidence Links & Document Matrix

| Category | Evidence | Description |
|---|---|---|
| Main Repository | [Team 3 GitHub Repository](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign) | Main source code and project documentation |
| Working Branch | [smartserve-mvp](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/smartserve-mvp) | Development branch |
| Payment and Inventory | [Commit 67cf5d0](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/67cf5d0e23ed4a19846b619a4f236594822bbe61) | Fix for duplicate inventory deduction after payment |
| Backend Test File | [test_owner_management.py](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/smartserve-pos/backend/test_owner_management.py) | Backend tests covering owner management, recipes, orders, payments, and inventory |
| Week 6 Automated Checks | [automated-check.md](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-06/automated-check.md) | Recorded workflow checks and their results |
| Week 6 Individual Evidence | [Week 6 Receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-06/receipts/daydevil80.md) | Evidence and findings related to recipe conversion and historical order information |
| Week 7 Individual Evidence | [Week 7 Receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-07-docs/Week7/receipts/daydevil80.md) | Documents recipe unit conversion and preserving saved order item names and prices |
| Week 7 Weekly Report | [Week 7 Weekly Report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/smartserve-mvp/docs/week-07-docs/Week7/weekly-report.md) | Team progress, identified issues, and follow-up actions |

**Evidence Note:** The links above refer to existing repository records. The Week 6 and Week 7 evidence should be treated as previous work, not as newly completed Week 8 testing. New Week 8 evidence can be added as the team completes further verification.

---

## 8. Individual Contribution Entries

### Lama Muskan — `Sammygit15`

**Week 8 Contribution: Documentation and MVP Planning**

- Prepared the Week 8 post-midterm weekly report for Team 3 — SmartServe POS.
- Organized the project's current implementation status and identified remaining MVP gaps.
- Documented lessons learned and priorities for the next development stage.
- Prepared the development direction for Weeks 9–11, focusing on the main POS transaction workflow.

**Previously Documented Technical Contributions (Week 7):**

- Improved recipe editing by converting ingredient quantities into the correct stock units before saving and comparing values.
- Worked on preserving menu item names and saved prices in order records so that later menu renaming does not change historical order information.
- Documented backend testing evidence in `smartserve-pos/backend/test_owner_management.py`, with 24 backend tests reported as passed.

**GitHub:** [Sammygit15](https://github.com/Sammygit15)

### Sherap Hyolmo — `daydevil80`

**Week 8 Contribution: Current Verification, Evidence and Week 9 Planning**

- Requested and documented a fresh check of the SmartServe POS workflow with coding-agent assistance. Codex executed the automated tests and browser run.
- Recorded **24 passing backend tests** and a **successful frontend production build** on the current application source.
- Recorded **27 passing browser/API checks** against a separate temporary **PostgreSQL database**, with no changes to the shared store data.
- Collected **12 screenshots** and expected-versus-actual results covering order creation, refresh recovery, failed-payment handling, successful retry, duplicate-payment protection, inventory deduction and sales updates.
- Verified that entering **18 g** in a recipe with stock stored in kilograms saves **0.018 kg**, and that an earlier receipt retains its original item name and price after menu editing.
- Checked the local owner-session boundary: anonymous protected requests return **HTTP 401**, owner login permits access, and logout removes access.
- Prepared the Week 8 contribution receipt and supporting addendum, connecting the technical results to the course lesson, project lesson and MVP-gap decision.
- Recorded the next verification milestone in **Issue #22**, with `daydevil80` coordinating the non-author handoff before expanding the feature scope.

**Previously Documented Technical Contributions (Week 7):**

- Corrected recipe editing so quantities convert into the stored ingredient unit before comparison and saving.
- Added original-name snapshots to new order items so later menu renaming does not change their receipt labels. Saved order prices remain unchanged.
- Added **four regression tests** covering alternate recipe units, incompatible units, historical receipt information and the legacy migration.
- Documented the limitation that original names never stored for older orders cannot be reconstructed automatically.

**Evidence:**

- [Week 8 individual receipt](receipts/daydevil80.md)
- [October 28 verification summary](evidence/2026-10-28/README.md)
- [Backend test output — 24 passed](evidence/2026-10-28/backend-tests.txt)
- [Frontend build output](evidence/2026-10-28/frontend-build.txt)
- [Browser/API checks — expected and actual results](evidence/2026-10-28/browser-results.json)
- [Twelve screenshot records](evidence/2026-10-28/SCREENSHOTS.md)
- [Week 8 lessons and milestone addendum](week8-addendum.md)
- [Week 9 milestone — Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22)
- [Week 7 implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0d5fecdf827deb12b7d4d560e392bfb06d868591)

**Verification boundary:** The supplied checks were agent-run developer verification. They do not establish a teammate's independent test, a narrated presentation, public deployment or production payment processing.

**GitHub:** [daydevil80](https://github.com/daydevil80)

### Shuzita Majhi — `Shuzita`

**Week 8 Contribution: Payment Recovery Evidence Review and Week 9 Test Planning**

- Reviewed the recorded payment-failure, successful-retry and duplicate-payment evidence for SmartServe POS.
- Compared the expected behavior with the actual values reported in the October 28 automated verification.
- Documented the payment boundary: payments are simulated, and the recorded checks demonstrate application behavior rather than real payment-provider processing.
- Selected payment-failure recovery as my proposed Week 9 verification task.

**Review Details**

- **Review date:** [Enter the actual date.]
- **Evidence I personally opened:** [List the result file and screenshot links reviewed.]
- **My finding or question:** [Write your own observation from the evidence.]

**Course Lesson**

A completed interface or presentation does not establish that a workflow is verified. Important claims need evidence, and each student should explain their own contribution. Therefore, I will distinguish reviewing existing results from personally executing a test.

**Source:** [Midterm Presentation Rubric](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/course-materials/blob/main/student-starter-kit/docs/midterm-presentation-rubric.md)

**Project Lesson**

The recorded results show why payment status and inventory changes must stay consistent. Failed simulated payment returns HTTP 402 and leaves the order open without changing stock or sales. A successful retry pays the same order. Repeating payment returns HTTP 409 without another deduction.

Therefore, my next verification task will check both recovery and duplicate protection, rather than only a successful payment.

**Current Evidence**

- [October 28 verification summary](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0b84c062adc05f082e70d6c1dba67dacd1d82d93/docs/week-08/evidence/2026-10-28/README.md)
- [Expected and actual browser/API results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0b84c062adc05f082e70d6c1dba67dacd1d82d93/docs/week-08/evidence/2026-10-28/browser-results.json)
- [Failure screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0b84c062adc05f082e70d6c1dba67dacd1d82d93/docs/week-08/evidence/2026-10-28/06-payment-failure.png)
- [Successful retry receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/0b84c062adc05f082e70d6c1dba67dacd1d82d93/docs/week-08/evidence/2026-10-28/07-paid-receipt.png)

**MVP Status: Still Has a Gap**

The current automated evidence supports the simulated sale. The team still needs to complete the verification milestone recorded in Issue #22 before treating the path as fully handed off.

**My Proposed Week 9 Action**

- **Owner:** Shuzita (`Shuzita`), after I confirm this assignment.
- **Task:** Follow the written setup and personally test failed payment, successful retry and duplicate payment using separate sample data.
- **Success signal:** Failure leaves stock and sales unchanged; successful retry deducts 500 ml milk and 36 g beans once for two lattes; repeated payment creates no additional deduction.
- **Evidence to record:** Tested commit, date, browser, starting values, expected/actual results, screenshots and the first failure if one occurs.
- **Tracking:** [Week 9 verification milestone — Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22)

**Evidence boundary:** The linked automated run was executed by Codex at daydevil80’s request. My contribution recorded here is my personal review and planning; it does not claim that I executed that earlier run.

**GitHub:** [Shuzita](https://github.com/Shuzita)

### Other Team Members

| Team Member | Week 8 Contribution | Evidence |
|---|---|---|
| Ualson Tamang | |  |
| Shreya | |  |

---

## 9. Risks and Mitigation Strategy

| Risk | Potential Impact | Mitigation Strategy |
|---|---|---|
| Incorrect inventory deduction | Stock quantities may become inaccurate | Verify recipe calculations and stock changes |
| Repeated payment requests | Ingredients may be deducted more than once | Verify duplicate-submission and deduction protection |
| Recipe unit conversion errors | Incorrect ingredient quantities | Test equivalent quantities across supported units |
| Order history inconsistency | Receipts may show incorrect item information | Preserve and verify saved order item details |
| Incomplete transaction testing | Important workflow errors may remain undetected | Perform end-to-end testing of the main POS workflow |

---

## 10. Decision Record

| Decision | Reason | Priority |
|---|---|---|
| Prioritize the existing POS workflow | The main transaction flow is the core purpose of the project | High |
| Verify payment and inventory consistency | Order and stock records must remain consistent | High |
| Test recipe calculations and unit conversion | Ingredient deductions depend on correct quantities | High |
| Preserve order item history | Historical order information should remain reliable | Medium |
| Postpone unrelated advanced features | Avoid unnecessary scope expansion before MVP completion | Medium |

---

## 11. Next Week's Bridge Task — Week 9

- Review the current implementation and confirm the remaining MVP requirements.
- Test the complete order-to-payment-to-inventory workflow.
- Verify that inventory deduction occurs only once for a paid order.
- Test recipe unit conversions and inventory movement records.
- Identify and fix issues discovered during testing.
- Update the project documentation with verified evidence.

**Week 8 Conclusion**

Week 8 marked the transition from the midterm checkpoint to the next stage of SmartServe POS development. The team reviewed the existing implementation, identified areas requiring further verification, and established a focused direction for completing the MVP. The priority for the coming weeks is to deliver a reliable and verifiable POS transaction workflow.
