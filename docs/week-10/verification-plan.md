# MVP Verification Plan — Week 10

**Project:** SmartServe POS  
**Team:** Team 3  
**Verification Period:** November 5–11, 2026  
**Main Objective:** Prepare a repeatable verification process for the existing MVP before Week 11 feature freeze and verification.

## 1. Purpose

This document defines the verification procedure for the current SmartServe POS MVP.

The verification process aims to confirm that the main ordering, payment, receipt, and inventory workflows behave as expected.

Every test must have:
- A unique test ID.
- A clear objective.
- Required test data.
- Reproducible steps.
- An expected result.
- An actual result.
- A test status.
- Supporting evidence.

This document defines the test plan. It does not claim that the tests have already passed.

## 2. Verification Environment

Record the actual environment before testing.

| Environment Detail | Recorded Value |
|---|---|
| Environment | Pending |
| Application URL | Pending |
| Frontend version or commit | Pending |
| Backend version or commit | Pending |
| Database environment | Pending |
| Browser | Pending |
| Test date | Pending |
| Tester | Pending |

Do not assume the live deployment uses the same database or configuration as a local or isolated test environment.

## 3. Test Status Definitions

| Status | Meaning |
|---|---|
| Not Run | Test has not been performed. |
| In Progress | Test is currently being performed. |
| Passed | Actual result matches the expected result and evidence is recorded. |
| Failed | Actual result does not match the expected result. |
| Blocked | Test cannot be performed because of an identified blocker. |
| Retest Required | A change has been made and the test must be repeated. |

A test is not Passed simply because the application builds or automated tests succeed.

## 4. Test Cases

### TC-01: Menu Item Selection

**Objective:** Verify that an available menu item can be selected.

**Preconditions:** Application is accessible and menu data is available.

**Steps:**
1. Open the ordering screen.
2. Locate an available menu item.
3. Select the item.
4. Check the order summary.

**Expected Result:** The selected item appears in the order summary with the correct item information.

**Evidence Required:**
- Screenshot of the menu.
- Screenshot of the order summary.
- Test result notes.

**Status:** Not Run

### TC-02: Quantity and Total Calculation

**Objective:** Verify quantity updates and order total calculation.

**Preconditions:** At least one available menu item has a known price.

**Steps:**
1. Select a menu item.
2. Record its displayed price.
3. Change the quantity.
4. Observe the updated total.
5. Calculate the expected total manually.
6. Compare both values.

**Expected Result:** The displayed total matches the expected calculation.

**Evidence Required:**
- Item price and quantity screenshot.
- Order total screenshot.
- Manual calculation record.

**Status:** Not Run

### TC-03: Order Creation and Saved Information

**Objective:** Verify that an order is saved with the correct item and price information.

**Steps:**
1. Create an order with a known item and quantity.
2. Record the item name, quantity, and price.
3. Submit the order.
4. Retrieve the saved order.
5. Compare the saved information with the submitted information.

**Expected Result:** The saved order contains the expected information and price values.

**Evidence Required:**
- Order creation screenshot.
- Saved order record or API response.
- Comparison notes.

**Status:** Not Run

### TC-04: Simulated Payment

**Objective:** Verify the existing simulated payment workflow.

**Steps:**
1. Create an eligible order.
2. Select the available simulated payment method.
3. Complete the payment action.
4. Check the resulting order status.

**Expected Result:** The simulated payment completes and the order status reflects the expected paid state.

**Evidence Required:**
- Payment screen screenshot.
- API response or saved order record.
- Final order status evidence.

**Limitation:** This test does not verify real payment gateway integration.

**Status:** Not Run

### TC-05: Receipt Verification

**Objective:** Verify that the receipt matches the saved order.

**Steps:**
1. Complete a simulated payment.
2. Open the corresponding receipt or order details.
3. Compare the receipt with the saved order.
4. Check item names, quantities, prices, and total.

**Expected Result:** The receipt displays information consistent with the saved order.

**Evidence Required:**
- Receipt screenshot.
- Saved order record.
- Comparison notes.

**Status:** Not Run

### TC-06: Recipe-Based Inventory Deduction

**Objective:** Verify that a completed eligible sale deducts the correct ingredient quantities.

**Preconditions:** A menu item has a configured recipe and sufficient stock.

**Steps:**
1. Select a menu item with a configured recipe.
2. Record the relevant ingredient stock.
3. Complete an eligible simulated sale.
4. Record the updated ingredient stock.
5. Calculate the expected deduction from the recipe.
6. Compare the expected and actual inventory changes.

**Expected Result:** Inventory is deducted according to the configured recipe.

**Evidence Required:**
- Recipe configuration.
- Inventory before the sale.
- Completed order record.
- Inventory after the sale.
- Expected-versus-actual calculation.

**Status:** Not Run

### TC-07: Duplicate Inventory Deduction Prevention

**Objective:** Verify that processing the same eligible order again does not deduct inventory twice.

**Steps:**
1. Record the initial inventory quantity.
2. Complete an eligible simulated sale.
3. Record the first inventory deduction.
4. Repeat the relevant processing action for the same order, if the application permits.
5. Check the inventory quantity and movement history.

**Expected Result:** The same order does not create an additional inventory deduction.

**Evidence Required:**
- Initial inventory record.
- First deduction record.
- Repeated-processing attempt or API response.
- Final inventory record.
- Inventory movement history.

**Status:** Not Run

### TC-08: Recipe Unit Conversion

**Objective:** Review whether recipe quantities are handled correctly when different units are entered and stored.

**Steps:**
1. Identify an ingredient with a known stock unit.
2. Open its recipe configuration.
3. Enter a recipe quantity using a supported alternative unit.
4. Save the recipe.
5. Review the stored quantity and unit.
6. Compare the stored value with the expected conversion.

**Expected Result:** The saved recipe quantity is equivalent to the entered quantity after the required unit conversion.

**Evidence Required:**
- Original input screenshot.
- Saved recipe record or API response.
- Conversion calculation.

**Status:** Not Run

### TC-09: Owner-Facing Information

**Objective:** Review the existing owner-facing information for consistency.

**Steps:**
1. Open the available owner-facing screens.
2. Review the displayed information.
3. Compare relevant figures with underlying records where possible.
4. Record any inconsistencies.

**Expected Result:** The reviewed information is consistent with its corresponding application records.

**Evidence Required:**
- Screenshots.
- Relevant API responses or records.
- Review notes.

**Status:** Not Run

## 5. Test Data Record

Record the actual test data used for each test.

| Data Item | Value |
|---|---|
| Menu item | Pending |
| Item price | Pending |
| Order quantity | Pending |
| Order ID | Pending |
| Payment method | Pending |
| Ingredient | Pending |
| Initial inventory | Pending |
| Recipe quantity | Pending |
| Expected deduction | Pending |

Do not reuse example values as actual test results.

## 6. Test Result Record

Complete one record for every executed test.

| Field | Result |
|---|---|
| Test ID | |
| Test date | |
| Tester | |
| Environment | |
| Application commit | |
| Expected result | |
| Actual result | |
| Status | |
| Evidence links | |
| Related issue | |
| Notes or limitations | |

## 7. Independent Verification

Independent verification should be performed by a person who did not author the specific changes being tested.

The reviewer should:
1. Receive the test instructions.
2. Use the recorded test environment.
3. Perform the steps independently.
4. Record actual results.
5. Capture their own evidence.
6. Report failures or blockers.
7. Identify the tested application version or commit.

**Required reviewer record:**

| Field | Value |
|---|---|
| Reviewer | Pending |
| Reviewer GitHub username | Pending |
| Review date | Pending |
| Tested commit | Pending |
| Environment | Pending |
| Result | Pending |
| Evidence | Pending |

If an independent reviewer is unavailable, record the blocker. Do not describe self-testing as independent verification.

## 8. Evidence Storage

Store original evidence under:

`docs/week-10/evidence/`

Suggested organization:

```text
evidence/
├── screenshots/
├── logs/
├── test-results/
└── independent-review/
```

Use the evidence index to link each file to its corresponding test ID.

## 9. Verification Limitations

The following limitations must be documented:

- Simulated payment is not real payment processing.
- Local testing does not automatically verify the deployed environment.
- Isolated database tests do not prove live database correctness.
- Automated tests do not replace independent verification.
- A successful test of one order does not prove every possible order scenario works.
- Any blocked test must include the reason and the required next action.

## 10. Week 10 Exit Criteria

Verification preparation is complete when:

- Test cases are documented.
- Expected results are defined.
- Required test data is identified.
- The environment is recorded before execution.
- Evidence storage is prepared.
- Independent verification instructions are ready.
- Unresolved questions and blockers are documented.

Actual test completion and results will be recorded separately.

**Final principle:** Every test result must be traceable to its procedure, environment, application version, and supporting evidence.
