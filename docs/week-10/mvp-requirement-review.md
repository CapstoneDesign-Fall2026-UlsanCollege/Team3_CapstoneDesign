# MVP Requirement Review — Week 10

**Project:** SmartServe POS  
**Team:** Team 3  
**Review Period:** November 5–11, 2026  
**Purpose:** Review the existing MVP workflows and prepare evidence-based verification for Week 11.

## 1. Review Method

For every requirement, record the date, tester, environment, application commit, steps, expected result, actual result, status, evidence reference, and related issue if applicable.

A requirement remains **Not Verified** until an actual check has been performed and supporting evidence is recorded.

## 2. Functional Requirements

| ID | Requirement | Verification Focus | Required Evidence | Status |
|---|---|---|---|---|
| FR-01 | Menu and item selection | Select an available menu item and confirm it appears in the order | Menu and order screenshots; test notes | Not Verified |
| FR-02 | Quantity and order total | Change quantity and compare displayed total with manual calculation | Price/quantity screenshot; calculation record | Not Verified |
| FR-03 | Order creation and saved prices | Create an order and compare submitted details with saved details | Order screenshot; saved record or API response | Not Verified |
| FR-04 | Simulated payment | Complete the existing simulated payment flow and inspect order status | Payment response; saved order status | Not Verified |
| FR-05 | Receipt information | Compare receipt item names, quantities, prices, and total with the saved order | Receipt screenshot; corresponding order record | Not Verified |
| FR-06 | Recipe-based inventory deduction | Compare inventory before and after an eligible sale against recipe quantities | Recipe record; before/after stock; calculation | Not Verified |
| FR-07 | Duplicate deduction prevention | Repeat the relevant processing action for the same order and inspect stock movements | Reprocessing response; final stock; movement history | Not Verified |
| FR-08 | Owner-facing information | Review existing owner-facing screens and compare displayed data with records | Screenshots; relevant records/API responses | Not Verified |

## 3. Cross-Feature Review

| Area | Review Focus | Required Evidence |
|---|---|---|
| Data consistency | Order, payment, receipt, and inventory records agree | Record comparison |
| Input validation | Invalid or incomplete inputs are handled appropriately | Test steps and response |
| Recipe units | Quantities and units are converted and stored correctly | Input, stored value, and conversion calculation |
| Order history | Saved order information is displayed consistently | History screenshot and record |
| Error handling | Failed operations do not silently create incorrect data | Error response or application log |

These are investigation areas, not confirmed defects.

## 4. Review Results

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

### Supporting Automated Backend Evidence

The backend unit-test suites recorded on November 10, 2026 passed 24/24: [owner management (12)](evidence/test-results/w10-owner-management-tests.txt), [Issue 3 (9)](evidence/test-results/w10-issue3-tests.txt), and [trash (3)](evidence/test-results/w10-trash-tests.txt). See the [consolidated summary](evidence/test-results/w10-backend-test-summary.md).

This evidence supports backend unit-level behavior only. It does not change the Not Verified status of FR-01 through FR-08 above, which require their own functional evidence.

## 5. Known Verification Limitations

- Historical automated results are not new Week 10 test results.
- Isolated or temporary database tests do not verify the live deployment database.
- Simulated payment does not prove real payment processing.
- Automated checks do not replace independent human verification.
- A successful individual workflow does not prove every workflow or edge case.
- Historical overwritten item names may not be recoverable from existing records.

## 6. Review Outcome

Complete this section after performing checks:
1. Requirements verified with evidence.
2. Requirements that failed.
3. Requirements still unverified or blocked.
4. Newly discovered bugs or gaps.
5. Related GitHub issues.
6. Follow-up items for Week 11.

**Review principle:** Every verified requirement must have an observable result and a traceable evidence reference.