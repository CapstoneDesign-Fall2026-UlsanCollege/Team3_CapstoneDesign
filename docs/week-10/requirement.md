# MVP Requirement Review — Week 10

**Project:** SmartServe POS  
**Team:** Team 3  
**Week:** 10  
**Review Period:** November 5–11, 2026  
**Purpose:** Review the existing MVP workflows and prepare evidence-based verification for Week 11.

## 1. Review Method

Each requirement must be checked against the current application.

For every requirement, record:

- Verification date
- Person performing the check
- Application environment
- Steps performed
- Expected result
- Actual result
- Pass, Fail, or Blocked status
- Screenshot, log, API response, or other evidence
- Related issue or commit, if applicable

A requirement must remain **Not Verified** until an actual check has been performed and its evidence recorded.

## 2. MVP Functional Requirements

### FR-01: Menu and Item Selection

**Requirement:** A user can view available menu items and select an item for an order.

**Verification procedure:**
1. Open the application.
2. Navigate to the menu or ordering screen.
3. Select an available item.
4. Confirm that the selected item appears in the order.

**Expected result:** The selected item is added to the order correctly.

**Required evidence:**
- Menu screen screenshot
- Screenshot showing the selected item
- Test notes describing the result

**Status:** Not Verified

### FR-02: Quantity and Order Total

**Requirement:** The application calculates the order total using the selected item prices and quantities.

**Verification procedure:**
1. Select an available menu item.
2. Increase or decrease its quantity.
3. Observe the order total.
4. Compare the displayed total with a manual calculation.

**Expected result:** The total matches the sum of item prices multiplied by their quantities.

**Required evidence:**
- Screenshot showing item prices and quantities
- Screenshot showing the calculated total
- Manual calculation and comparison result

**Status:** Not Verified

### FR-03: Order Creation and Saved Prices

**Requirement:** The application creates an order and preserves the relevant item and price information at the time of order creation.

**Verification procedure:**
1. Create an order with one or more items.
2. Record the item names, quantities, and prices.
3. Save the order.
4. Review the saved order information.

**Expected result:** The saved order contains the expected item information and prices.

**Required evidence:**
- Order creation screenshot
- Saved order record or API response
- Comparison between the submitted and saved information

**Status:** Not Verified

### FR-04: Simulated Payment

**Requirement:** The application supports the existing simulated payment workflow.

**Verification procedure:**
1. Create an order.
2. Select the available simulated payment method.
3. Complete the payment action.
4. Review the resulting order status.

**Expected result:** The simulated payment action completes and the order receives the expected paid status.

**Required evidence:**
- Payment screen screenshot
- Payment response or relevant order record
- Screenshot or record showing the final status

**Limitation:** This requirement verifies simulated payment only. It does not demonstrate integration with a real payment gateway.

**Status:** Not Verified

### FR-05: Receipt Information

**Requirement:** The application displays the relevant information for a completed order.

**Verification procedure:**
1. Complete a simulated payment.
2. Open the corresponding receipt or order details.
3. Compare the displayed information with the saved order.

**Expected result:** The receipt displays the correct order information, including applicable item names, quantities, prices, and total.

**Required evidence:**
- Receipt screenshot
- Corresponding saved order record
- Comparison notes

**Status:** Not Verified

### FR-06: Recipe-Based Inventory Deduction

**Requirement:** A completed eligible sale deducts the required ingredient quantities according to the configured recipe.

**Verification procedure:**
1. Identify an item with a configured recipe.
2. Record the relevant ingredient stock before the sale.
3. Complete an eligible simulated sale.
4. Record the ingredient stock after the sale.
5. Compare the difference with the expected recipe deduction.

**Expected result:** The correct ingredient quantities are deducted according to the recipe configuration.

**Required evidence:**
- Recipe configuration screenshot or record
- Inventory before the sale
- Completed order record
- Inventory after the sale
- Calculation showing expected versus actual deduction

**Status:** Not Verified

### FR-07: Duplicate Inventory Deduction Prevention

**Requirement:** Repeated processing of the same eligible order must not deduct the same inventory more than once.

**Verification procedure:**
1. Record the initial inventory quantity.
2. Complete an eligible simulated sale.
3. Record the inventory deduction.
4. Repeat the relevant processing action for the same order, where the application permits it.
5. Check the inventory quantity and inventory movement records.

**Expected result:** The same order does not cause a second inventory deduction.

**Required evidence:**
- Initial inventory record
- First deduction record
- Repeated-processing attempt or API response
- Final inventory record
- Inventory movement history

**Status:** Not Verified

### FR-08: Owner-Facing Information

**Requirement:** Review the existing owner-facing screens and information supported by the current MVP.

**Verification procedure:**
1. Access the existing owner-facing area.
2. Review the available information.
3. Check that displayed information corresponds with the relevant application records.
4. Record any missing or incorrect information.

**Expected result:** Existing owner-facing information is displayed consistently with the underlying application records.

**Required evidence:**
- Screenshots of the reviewed screens
- Relevant record or API response, where applicable
- Review notes and identified gaps

**Status:** Not Verified

## 3. Cross-Feature Review

The following areas must also be considered during verification:

| Review Area | What to Check | Required Evidence |
|---|---|---|
| Data consistency | Order, payment, receipt, and inventory records agree | Record comparison |
| Input validation | Invalid or incomplete inputs are handled appropriately | Test steps and response |
| Recipe units | Ingredient quantities and units are converted correctly | Input, saved value, and calculation |
| Order history | Previously saved order information is displayed consistently | Order history screenshot and record |
| Error handling | Failed operations do not silently produce incorrect results | Error response or application log |

These are review areas, not claims that every possible edge case has already been tested.

## 4. Review Results

Complete this section only after performing the actual checks.

| Requirement | Status | Evidence Reference | Notes |
|---|---|---|---|
| FR-01 Menu selection | Not Verified | Pending | |
| FR-02 Quantity and total | Not Verified | Pending | |
| FR-03 Order creation and saved prices | Not Verified | Pending | |
| FR-04 Simulated payment | Not Verified | Pending | |
| FR-05 Receipt information | Not Verified | Pending | |
| FR-06 Inventory deduction | Not Verified | Pending | |
| FR-07 Duplicate deduction prevention | Not Verified | Pending | |
| FR-08 Owner-facing information | Not Verified | Pending | |

## 5. Known Verification Limitations

The following limitations must be considered when interpreting results:

- Historical automated test results must not be presented as new Week 10 test results.
- Tests performed against isolated or temporary databases do not automatically verify the live deployment database.
- Simulated payment does not prove real payment processing.
- Automated checks do not replace independent human verification.
- Historical order records may not contain information that was overwritten before the current data structure preserved it.
- A successful individual workflow does not prove that every application workflow is correct.

## 6. Week 10 Review Outcome

At the end of the review, document:

1. Requirements successfully verified with evidence.
2. Requirements that failed verification.
3. Requirements that remain unverified.
4. Newly discovered bugs or gaps.
5. Related GitHub issues.
6. Items requiring fixes or additional verification in Week 11.

**Review principle:** Every requirement needs an observable result and a traceable evidence reference before it can be considered verified.
