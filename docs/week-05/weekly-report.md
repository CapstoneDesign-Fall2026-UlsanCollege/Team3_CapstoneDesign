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
- Published screenshots, machine-readable results, and repeatable browser checks.

These results describe implementation and automated verification on the existing development PC. Independent teammate reproduction remains pending.

## Evidence

- [Cashier implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0ec28f2)
- [Cashier source](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/frontend/src/main.tsx)
- [Two-Latte verification report and screenshots](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/cashier-evidence.md)
- [Two-Latte repeatable browser check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/verify-cashier.cjs)
- [Shuzita's mixed-order evidence upload](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c9f526f)
- [Mixed-order evidence report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/README.md)
- [Mixed-order machine-readable results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/results.json)
- [Mixed-order repeatable check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/verify.cjs)
- [Issue #18 — Chuseok Checkpoint](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18)
- [Issue #19 — Order Data and Order-State Model](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/19)
- [Issue #12 — Stored unit price decision](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12)
- [Earlier payment test evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-04-chuseok/payment-test-evidence/README.md)

## Individual receipts

| Student / GitHub login | Contribution / status | Evidence |
| --- | --- | --- |
| **Lama Muskan (`Sammygit15`)** | The existing report credits payment/inventory verification, unit-price handling, and repeated-payment testing. The professor's review credits Issues #18 and #12. Confirmation of the current personal test result remains pending. | [Issue #12](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/12); [Issue #18](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/18); [Earlier payment evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-04-chuseok/payment-test-evidence/README.md) |
| **Ualson Tamang (`ualsom`)** | Authored the order-state proposal in Issue #19. Current implementation/test contribution and observed results await member confirmation. | [Issue #19](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/19) |
| **Sherap Hyolmo (`daydevil80`)** | Added a separate Create order action, creation-error handling, and saved-order recovery. Automated verification passed for the two-Latte ₩9,000 order, simulated payment, receipt, inventory deductions, and duplicate-payment protection. Frontend build and eight backend tests passed. | [Implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0ec28f2); [Verification report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/cashier-evidence.md); [Repeatable check](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/verify-cashier.cjs); [Saved order screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/screenshots/01-created-order.png); [Receipt screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/screenshots/02-paid-receipt.png) |
| **Shuzita Majhi (`Shuzita`)** | Uploaded the Week 5 mixed-order receipt/inventory evidence, results, repeatable check, and six screenshots to main. The supplied automated check verifies one Americano + one Milk Tea, takeaway, ₩8,500, simulated card payment, ingredient deductions, refresh recovery, sales, and duplicate-payment protection. Personal review and independent reproduction remain pending in the uploaded evidence. | [Upload commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c9f526f); [Evidence report](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/README.md); [Results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/results.json); [Receipt screenshot](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/04-paid-card-receipt.png); [Inventory before](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/01-inventory-before.png); [Inventory after](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/05-inventory-after.png) |
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

[Complete two-Latte test evidence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/cashier-evidence.md)

### Additional mixed-order receipt/inventory check

This Codex-assisted automated check ran on October 7 at 14:56 Korea time against commit `a36f83a`, on the existing developer PC. Shuzita subsequently uploaded the evidence to main.

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

Screenshots:

1. [Starting inventory](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/01-inventory-before.png)
2. [Starting daily sales](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/02-sales-before.png)
3. [Unpaid mixed order](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/03-unpaid-mixed-order.png)
4. [Paid card receipt](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/04-paid-card-receipt.png)
5. [Inventory after payment](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/05-inventory-after.png)
6. [Sales after payment and duplicate request](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/06-sales-after-repeat.png)

[Machine-readable results](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/results.json)

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

Planning and setup:

- [Sprint 1 plan](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/sprint-1.md)
- [Owned task sequence](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/work-checklist.md)
- [Application setup instructions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/README.md)
- [Cashier check instructions](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-05/cashier-evidence.md)

## Current issues

- PostgreSQL connectivity and backend startup succeeded in the October 7 Docker checks on this development PC.
- Independent teammate setup and complete two-Latte reproduction remain pending.
- Shuzita's personal receipt/inventory review and evidence comment remain pending.
- Other members need to confirm their contribution rows and actual evidence.
- The mixed-order evidence package is published in [Shuzita's upload commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/c9f526f).
- The local four-task sequence still needs corresponding GitHub Issue ownership, completion checks, and evidence links connected to Issue #19.

## Next steps

1. Have a second teammate follow the setup instructions and reproduce the full two-Latte path.
2. Record expected versus actual results and attach that teammate's evidence to Issue #18.
3. Have Shuzita review or personally run the receipt/inventory check and record her findings.
4. Add her personal observations to the published mixed-order evidence.
5. Confirm every member's contribution row.
6. Update the GitHub task sequence connected to Issue #19 with confirmed owners and checkable results.
7. Keep Issue #18's independent-reproduction checkbox unchecked until the complete check actually passes.
