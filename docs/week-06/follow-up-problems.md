# Follow-up problems from the Week 6 check

October 14, 2026 · Application source [df2f357](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/df2f357b0246fd71b76d7be8a7fa03d29dee68fe) · Related [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20)

These are recorded problems, not completed fixes. Application code and issue state are outside this documentation push. Proposed owner for review: `daydevil80`.

## F1 — menu rename changes historical receipt names

1. Pay for two Caffè Lattes at ₩4,500 each.
2. In Owner dashboard, rename that product to Caffè Latte test and change its price to ₩6,000.
3. Reopen the original paid order from Orders.

Expected: the old receipt still identifies Caffè Latte and retains the ₩9,000 total and ₩4,500 saved unit price.

Actual: total and unit price remain correct, but the old receipt now says Caffè Latte test.

Proof: [original receipt](evidence/2026-10-14/screenshots/04-paid-original-receipt.png), [receipt after edit](evidence/2026-10-14/screenshots/08-historical-receipt-after-menu-edit.png), and raw result `historical-product-name` in [results.json](evidence/2026-10-14/results.json).

Code observation: `order_view` reads the name from the current MenuItem record; OrderItem stores the unit price but has no name snapshot in this source version. Suggested next work: define whether historical product labels should be snapshots, add that protection if agreed, and repeat the same rename test.

## F2 — alternate recipe unit is ignored when editing

1. Convert Coffee beans inventory from g to kg.
2. Edit Americano's recipe.
3. Choose Recipe unit g, enter 18, and save.
4. Inspect the recipe and refresh Cashier availability.

Expected: 18 g stores as 0.018 kg. With 1.146 kg in stock, Americano remains available.

Actual: the edited recipe stores/displays 18 kg. Cashier disables Americano and reports 18 kg required, 1.146 kg available. Stock itself remains unchanged.

Proof: [18 g input](evidence/2026-10-14/screenshots/12-recipe-edit-18-grams.png), [saved 18 kg recipe](evidence/2026-10-14/screenshots/13-recipe-saved-wrong-unit.png), [incorrect shortage](evidence/2026-10-14/screenshots/14-incorrect-americano-shortage.png), and raw results `recipe-edit-unit-conversion` / `availability-after-recipe-edit`.

Code observation: the create-menu path calls `normalize_recipe_units`; the update-menu path in this source version does not. Suggested next work: apply the same compatible-unit validation/conversion on edit, add a regression covering edit rather than creation alone, and rerun the UI/payment path.

## Loading observation and test correction

The first scripted recovery check inspected the page before the saved-order request finished. The screenshot showed Order #1 / Open alongside Choose menu items to start, without the saved total yet. The first run marked recovery failed because it checked too early.

The script was corrected to wait for the saved total, and the entire check repeated with a new empty sample database. Recovery passed; F1 and F2 still failed. No application code was changed between runs. [Initial result](evidence/2026-10-14/initial-run/results.json), [initial loading screenshot](evidence/2026-10-14/initial-run/screenshots/03-recovered-unpaid-order.png), and [repeat recovery screenshot](evidence/2026-10-14/screenshots/03-recovered-unpaid-order.png) are retained.

Possible interface improvement: show an explicit Loading saved order label and disable payment until the order details arrive. This is a follow-up usability suggestion, not a verified completed change.
