# Weekly Report — Week 5

**Team:** Team 3 — SmartServe POS  
**Week:** Week 5  
**Date:** 2026-10-03; contribution/evidence update: 2026-10-07

## Main focus

This week focused on moving SmartServe from Sprint 0 decisions into Sprint 1 implementation and verifying the cashier, receipt, payment, inventory, and order-price behaviour.

## Work completed

- Continued SmartServe MVP implementation using React, TypeScript, Vite, FastAPI, SQLAlchemy, and PostgreSQL.
- Verified that each order item stores the unit price used when the order was created.
- Added a test confirming that changing the current menu price does not change an existing order's saved price.
- Added a separate **Create order** action so the cashier can save an unpaid order before payment.
- Added creation-error handling that preserves the cart for retry.
- Verified saved-order recovery after refreshing the browser.
- Verified successful simulated payment, receipt contents, and correct inventory deductions.
- Confirmed that repeated payment for the same order returns HTTP 409 without another inventory deduction or sale.
- Recorded automated checks for both the two-Latte path and an additional Americano + Milk Tea path.
- Prepared screenshots, machine-readable results, and repeatable browser checks.

These results describe implementation and automated verification on the existing development PC. Independent teammate reproduction remains pending.

## Evidence

- [Cashier implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0ec28f2)
- [Cashier source](../../smartserve-pos/frontend/src/main.tsx)
- [Two-Latte verification results and screenshots](cashier-evidence.md)
- [Two-Latte repeatable browser check](verify-cashier.cjs)
- [Issue #18 — Chuseok Checkpoint](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18)
- [Issue #19 — Order Data and Order-State Model](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/19)
- [Issue #12 — Stored unit price decision](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12)
- [Earlier payment test evidence](../week-04-chuseok/payment-test-evidence/README.md)

The additional mixed-order package is saved locally at `docs/week-05/shuzita-ben`. Its GitHub evidence link is pending upload.

## Individual receipts

| Student / GitHub login | Contribution / status | Evidence |
| --- | --- | --- |
| **Lama Muskan (`Sammygit15`)** | The existing report credits payment/inventory verification, unit-price handling, and repeated-payment testing. The professor's review credits Issues #18 and #12. Confirmation of the current personal test result remains pending. | [Issue #12](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12); [Issue #18](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18); [Earlier payment evidence](../week-04-chuseok/payment-test-evidence/README.md) |
| **Ualson Tamang (`ualsom`)** | Authored the order-state proposal in Issue #19. Current implementation/test contribution and observed results await member confirmation. | [Issue #19](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/19) |
| **Sherap Hyolmo (`daydevil80`)** | Added a separate Create order action, creation-error handling, and saved-order recovery. Automated verification passed for the two-Latte ₩9,000 order, simulated payment, receipt, inventory deductions, and duplicate-payment protection. Frontend build and eight backend tests passed. | [Implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0ec28f2); [Current verification and screenshots](cashier-evidence.md); [Repeatable check](verify-cashier.cjs) |
| **Shuzita Majhi (`Shuzita`)** | A receipt/inventory evidence package was prepared with Codex for Shuzita to review: one Americano + one Milk Tea, takeaway, ₩8,500, simulated card payment. Automated checks on the existing developer PC passed. This is supplied evidence; Shuzita's personal review and independent reproduction remain pending. | Local package: `docs/week-05/shuzita-ben/README.md`, `results.json`, `verify.cjs`, and six screenshots. Published evidence and personal review comment pending. |
| **Shreya (`shrey776`)** | Personal contribution and current evidence awaiting member update. Checkpoint assignment alone is not completion proof. | [Issue #18](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18) |

## Verification results

### Two-Latte cashier path

The October 7 automated browser check verified:

| Check | Expected | Actual result |
| --- | --- | --- |
| Creation failure | Show error and preserve cart for retry | PASS |
| Create two-Latte order | Quantity 2; total ₩9,000; unpaid `open` order | PASS |
| Before payment | Inventory and paid-order count unchanged | PASS |
| Refresh | Recover the same saved order | PASS |
| Simulated cash payment | Paid receipt for the same order | PASS |
| Milk deduction | 500 ml | PASS |
| Coffee-bean deduction | 36 g | PASS |
| Duplicate payment | HTTP 409; no additional stock deduction or sale | PASS |
| Daily sales | One additional paid order and ₩9,000 | PASS |
| Backend regression checks | Existing tests pass | 8 tests passed |
| Frontend production build | TypeScript and Vite complete | PASS |

See [complete test evidence](cashier-evidence.md).

### Additional mixed-order receipt/inventory check

This Codex-assisted automated check ran on October 7 at 14:56 Korea time against commit `a36f83a`, on the existing developer PC.

**Order:** #3 — takeaway  
**Items:** one Americano + one Milk Tea  
**Total:** ₩8,500  
**Payment:** simulated card

| Check | Expected | Actual | Result |
| --- | --- | --- | --- |
| Receipt contents | Americano ₩3,500 + Milk Tea ₩5,000 | Correct items, quantities and ₩8,500 total | PASS |
| Create unpaid order | `open`; no inventory deduction | HTTP 201; `open`; inventory unchanged | PASS |
| Refresh recovery | Recover the same order and takeaway selection | Order #3 recovered | PASS |
| Card payment | Paid receipt for the same order | Paid receipt #3; card | PASS |
| Coffee beans | Deduct 18 g | 1,164 → 1,146 g | PASS |
| Milk | Deduct 200 ml | 4,500 → 4,300 ml | PASS |
| Sugar | Deduct 20 g | 2,500 → 2,480 g | PASS |
| Tea leaves | Deduct 8 g | 700 → 692 g | PASS |
| Daily sales | Add one paid order and ₩8,500 | 1 → 2 paid orders; ₩9,000 → ₩17,500 | PASS |
| Duplicate payment | HTTP 409; stock and sales unchanged | HTTP 409; no additional deduction or sale | PASS |

The package contains starting inventory, starting sales, unpaid order, paid receipt, ending inventory, and ending sales screenshots.

This additional check does not establish Shuzita's personal review or independent reproduction of the two-Latte demo.

### Historical price and order states

The implementation stores the historical price in `OrderItem.unit_price`. Changing a menu item's current price does not change the saved price of an existing order.

The current implementation uses `open → paid`. `open` is the unpaid state corresponding to the proposed pending stage in Issue #19. Inventory deduction is recorded in the movement ledger and committed within the successful payment transaction.

## Demo and boundaries

On October 8, demonstrate selecting two seeded Caffè Lattes, creating an unpaid order for ₩9,000, refreshing to recover it, completing simulated cash payment, showing its receipt, and checking that milk decreases by 500 ml and coffee beans by 36 g exactly once.

A duplicate payment must return HTTP 409 without another inventory deduction or sale.

**Real local software behaviour:**

- Order persistence in PostgreSQL.
- Stored order-item unit prices and totals.
- Payment records and inventory-movement ledger updates.
- Receipt, inventory, and sales displays.

**Simulated/sample elements:**

- Cash, card, and QR payment acceptance.
- Menu, recipe, and inventory sample records.
- No real money is charged.
- No physical stock is measured.

**Postponed:**

- Real payment integration.
- Authentication and role enforcement.
- Supplier management.
- Customer accounts and loyalty features.
- Multiple branches and advanced reporting.
- Additional features outside the selected demo path.

See the [Sprint 1 plan](sprint-1.md), [task sequence](work-checklist.md), and [setup/check instructions](cashier-evidence.md).

## Current issues

- PostgreSQL connectivity and backend startup succeeded in the October 7 Docker checks on this development PC.
- Independent teammate setup and complete two-Latte reproduction remain pending.
- Shuzita's personal receipt/inventory review and evidence comment remain pending.
- Other members need to confirm their contribution rows and actual evidence.
- The mixed-order evidence package has not yet been uploaded.
- The local four-task sequence still needs corresponding GitHub Issue ownership, completion checks, and evidence links connected to Issue #19.

## Next steps

1. Have a second teammate follow the setup instructions and reproduce the full two-Latte path.
2. Record expected versus actual results and attach that teammate's evidence to Issue #18.
3. Have Shuzita review or personally run the receipt/inventory check and record her findings.
4. Upload the mixed-order evidence package and replace its pending link.
5. Confirm every member's contribution row.
6. Update the GitHub task sequence connected to Issue #19 with confirmed owners and checkable results.
7. Keep Issue #18's independent-reproduction checkbox unchecked until the complete check actually passes.
