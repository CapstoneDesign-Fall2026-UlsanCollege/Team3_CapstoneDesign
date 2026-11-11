# Week 10 Code Ownership Audit

Add or confirm your own row. Link the code or artifact you reviewed and record the command or steps, environment, revision, expected and actual result, and evidence. Suggested slices are available for teammates to confirm or replace.

| Member | Bounded slice | Repeatable check and result |
|---|---|---|
| @daydevil80 | [Simulated payment and recipe-based inventory deduction](../../smartserve-pos/backend/app/main.py) | [9/9 backend tests passed on isolated SQLite](evidence/test-results/daydevil80-issue3.txt). [Independent Render handoff](issue-22-render-check.md) awaits a tester result. |
| @Sammygit15 | Frontend production build | Existing [individual record](individual-contributions/LamaMuskan%28Sammygit15%29.md) and [build log](evidence/frontend-build/w10-frontend-production-build.txt). Member to confirm the ownership row. |
| @Shuzita | Suggested: cashier item quantity and total | Pending member entry and result. |
| @ualsom | Suggested: paid receipt and saved prices | Pending member entry and result. |
| @shrey776 | Suggested: owner sales and order visibility | Pending member entry and result. |

## @daydevil80 repeatable backend check

From the repository root, enter smartserve-pos/backend, install requirements.txt in a Python virtual environment, and run the command below. The suite uses seeded in-memory SQLite. The recorded run used Python 3.11.15 and Pydantic 2.10.6. See the log for the exact source revision and environment.

    python -m unittest -v test_issue3

The insufficient-stock case sets milk to 100 ml for a latte that requires 250 ml. It expects HTTP 409 and checks that stock is unchanged with zero payments and zero inventory movements. The suite also checks a failed payment followed by retry, repeat payment after a fresh session, and preservation of the original order price.

### Two-latte regression contribution

Added [an exact-quantity regression](../../smartserve-pos/backend/test_issue3.py) for order creation, failed card payment, cash retry, and duplicate payment. The [recorded run](evidence/test-results/daydevil80-two-latte.txt) passed 25/25 tests on isolated SQLite. To repeat the targeted case from the backend directory:

    python -m unittest -v test_issue3.InventoryPaymentTests.test_two_latte_order_deducts_recipe_once_after_cash_retry
