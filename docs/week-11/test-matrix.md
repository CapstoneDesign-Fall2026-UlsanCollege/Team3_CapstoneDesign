# Week 11 Automated Test Matrix — SmartServe POS

**Week:** 11  
**Branch:** `main`  
**Status:** Planned test coverage; execution results must be recorded after tests run.

## 1. Purpose

This matrix lists candidate behaviours to verify during Week 11. It is a planning and tracking document, not proof that any test has already been implemented or passed.

Before adding a test, inspect the current application code and existing tests. Keep only scenarios that match implemented features and avoid duplicating existing coverage without a reason.

## 2. Backend Test Matrix

| ID | Feature / area | Scenario to verify | Expected result | Status |
|---|---|---|---|---|
| BE-01 | Owner management | Valid owner-management operation | Operation completes and persisted state is correct | To inspect |
| BE-02 | Owner management | Invalid or incomplete input | Request is rejected safely; no unintended state change | To inspect |
| BE-03 | Orders | Create an order with valid items and quantities | Order is created with correct item and total values | To inspect |
| BE-04 | Orders | Submit invalid item or quantity data | Invalid order is rejected; no unintended order or stock change | To inspect |
| BE-05 | Payment | Successful payment flow, if implemented | Order/payment state is updated consistently | To inspect |
| BE-06 | Payment | Failed payment flow, if implemented | Failure is handled and order/payment state remains consistent | To inspect |
| BE-07 | Payment | Repeat the same payment operation, if supported | Duplicate processing is prevented or handled according to the implementation | To inspect |
| BE-08 | Inventory | Complete a valid sale | Inventory changes by the expected amount | To inspect |
| BE-09 | Inventory | Attempt a sale with insufficient stock, if enforced | Operation is rejected or handled according to the defined business rule | To inspect |
| BE-10 | Recipe conversion | Convert recipe ingredient quantities between supported units | Calculated ingredient usage is correct | To inspect |
| BE-11 | Historical records | Update or remove related current data | Historical order/receipt information remains available as designed | To inspect |
| BE-12 | Trash / deletion | Delete and restore an eligible record | Record state changes correctly and restoration behaves as expected | To inspect |

## 3. Frontend Test Matrix

The frontend currently has no configured test runner in the inspected `package.json`. These are candidate tests to implement after selecting a compatible framework.

| ID | Feature / area | Scenario to verify | Expected result | Status |
|---|---|---|---|---|
| FE-01 | Application rendering | Render the selected page/component | Main content appears without runtime errors | Pending setup |
| FE-02 | Form validation | Submit a form with missing or invalid required values | Validation feedback appears and invalid submission is prevented | Pending setup |
| FE-03 | User interaction | Trigger a primary button or action | The expected UI state or action occurs | Pending setup |
| FE-04 | Loading / error states | Simulate a failed data request where practical | Error state is displayed and the UI remains usable | Pending setup |
| FE-05 | Order display | Render order data | Correct item details and totals are displayed | Pending setup |

## 4. CI Validation Matrix

| ID | Check | Evidence required | Status |
|---|---|---|---|
| CI-01 | Backend test job | Actual GitHub Actions run, commit SHA, job result, and test output | To verify |
| CI-02 | Frontend production build | Actual build job result and uploaded output, if configured | To verify |
| CI-03 | Frontend automated test job | Actual job result after frontend tests are configured and added to CI | Pending implementation |
| CI-04 | Browser/API regression job | Actual workflow result and generated artifacts, if the existing workflow runs this check | To verify |
| CI-05 | Workflow failure visibility | A controlled local test failure or safe test-branch check shows a failing result; restore changes afterward | To verify |

## 5. Test Execution Record

Add one record for each actual test run. Do not fill in results from memory or copy Week 10 results into this table.

| Date | Tester | Commit SHA | Command / workflow run | Result | Evidence file or URL |
|---|---|---|---|---|---|
| Not run yet | — | — | — | — | — |

## 6. Result Status Definitions

- **To inspect:** Existing implementation and test coverage have not yet been checked.
- **Pending setup:** Required test tooling or test implementation is not yet in place.
- **Passed:** Test was executed and the expected result was observed.
- **Failed:** Test was executed and did not meet the expected result.
- **Not applicable:** The feature or behaviour is not implemented; record the reason.

## 7. Notes

- A production build is not a substitute for frontend unit/component tests.
- A workflow configuration is not proof of a successful workflow run.
- Use isolated test data and databases where possible; do not run destructive tests against production data.
- Record known limitations, simulated integrations, skipped scenarios, and unresolved failures.
- Keep Week 10 evidence separate from all Week 11 execution records.
