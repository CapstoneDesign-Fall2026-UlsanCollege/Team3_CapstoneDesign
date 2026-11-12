# SmartServe POS Final Demo Roadmap

Team 3 · Weeks 11–16

## What SmartServe supports

- **Café, restaurant, and bakery:** Takeaway, table service, or both. A table can hold an open bill until payment or cancellation.
- **Retail and grocery:** In-store checkout, pickup, or both. Stocked products deduct units sold.
- **Barber and salon:** Walk-in queue, staff appointments, or both. Overlapping bookings for the same staff member are rejected.
- **Repair shop:** Immediate checkout, tracked repair jobs, or both. A linked payment completes the job.
- **Professional services:** Fixed-price checkout, appointments, or both.
- **Custom:** Choose which tools to enable and start with an empty catalog.
- **Shared tools:** One login, owner invitations and email verification, workspace permissions, catalog search, simulated payments, saved receipts, stock and daily sales. Superadmin can stop, resume, archive, or delete eligible workspaces.

## What the evidence covers

- Render lists **eb2c88e** as live. A later manual deploy of that same commit was canceled.
- On **eb2c88e**, 26 isolated browser/API checks passed. The suite covered the three-step setup, owner activation using a test inbox, café table and takeaway flows, retail stock dropping from 40 to 39, appointment overlap rejection, walk-ins, repair checkout, custom checkout, and mobile setup.
- The suite counted all ten preset choices. Its worked examples covered café, retail, barber, repair, and custom. Restaurant, bakery, grocery, salon, and professional services still need their own short preset checks.
- The independent two-latte reproduction remains open in Issue #22. Record that live result separately from the local browser run.


## P1 — Final demo MVP

- **Shared setup:** Superadmin creates a workspace, chooses its business type and workflow, and invites the owner. The owner sets a passphrase, verifies their email, and enters their assigned workspace.
- **Food and drink:** In a café, sell two lattes for **₩9,000**. A failed simulated payment leaves stock unchanged. A successful retry deducts **500 ml of milk and 36 g of beans** once. Keep the independent Render check in Issue #22.
- **Retail:** In a shop, complete an in-store or pickup sale. Check that the receipt shows the right price and product stock drops by the number sold.
- **Services:** In a barber or repair workspace, complete one appointment or job and take a simulated payment. Check that the work is marked complete and the receipt shows the service price.
- **Owner review:** Show the paid order and sales total for each example. Use two owner accounts to verify that each sees only their assigned business.

## Weeks 11–16

### Week 11 — Prepare three demo workspaces

- **P1:** Record the Render URL and deployed commit. Prepare one café, one retail shop, and one service business.
- **P1:** Ask a teammate who did not write the change to run the two-latte test.
- **P1:** Save the starting stock, order ID, payment results, final stock, and screenshots in Issue #22.
- **Done when:** The tester posts their own result and explains any step that failed or was blocked.

### Week 12 — Check food, retail, and service sales

- **P1:** Try a sale with too little stock. Check that the payment fails and stock stays the same.
- **P1:** Pay a test order and try paying it again. Check that stock is deducted only once.
- **P1:** Check recipe units, such as grams and kilograms. Change an item name or price and confirm the old receipt keeps its original details.
- **P1:** Sell a retail product and complete a service job or appointment. Check the receipt, stock where applicable, and work status.
- **P2:** Open restaurant, bakery, grocery, salon, and professional services. Check the available workflow choices and that each opens the correct tools.
- **Done when:** Each P1 workflow has expected and actual results, with a retest for any fix.

### Week 13 — Check accounts and owner reports

- **P1:** Invite a test owner and verify that they can activate their account and open their assigned workspace.
- **P1:** Use a second account to check that it cannot see the first workspace. Match paid orders, receipts, stock where applicable, and daily sales in each demo workspace.
- **P2:** On a test business, stop POS access, confirm the owner is blocked, then resume it and confirm the owner can sign in again.
- **Done when:** The team has screenshots or test results for workspace access and sales totals.

### Week 14 — Run the full demo and freeze the build

- **P1:** Start in a signed-out browser. Follow the demo from login through café checkout, retail stock, and service completion.
- **P1:** Fix anything that prevents the demo from finishing. Repeat the full run after a fix.
- **P1:** Record the commit that passed and freeze new features for the demo.
- **Done when:** A teammate can finish the demo by following the written steps without help.

### Week 15 — Rehearse and prepare a backup

- **P1:** Run two rehearsals on the chosen Render build. Check that sign-in and Gmail verification work.
- **P1:** Record the working demo and save screenshots of the receipt, inventory, and sales dashboard.
- **P1:** Put the recording, screenshots, test results, and code links in the evidence index.
- **Done when:** The team can show the full workflow using the recording if the live app is unavailable.

### Week 16 — Present and submit

- **P1:** Assign who introduces SmartServe, who runs the sale, and who explains the results.
- **P1:** Rehearse the handoffs and practice switching to the backup recording.
- **P1:** Check that the report, slides, recording, and individual evidence links open, then submit them.
- **Done when:** Everyone knows their part and the submission links work.


## Risks

- Render or Gmail is unavailable:** Check both before rehearsals. Keep an activated demo account and a backup recording.
- Stock or sales figures are wrong:** Record starting stock and the order ID. Compare the receipt, inventory, and sales after each payment attempt.
- Someone sees the wrong workspace:** Test two owners in separate browser sessions before the feature freeze.
- The live test is missing:** Name a non-author tester and record their actual result and deployed revision in Issue #22.
- Last-minute changes break the demo:** Pin the tested revision and rerun the affected workflows after any fix.


## Stretch goals in order

1. **QR receipts.** Put a QR code on a paid receipt so a customer can open a read-only copy without a POS login. Check that the link reveals only that receipt.
2. **Live kitchen or service board.** Show pending work on a second screen. A cashier marks an item ready and the board updates. Start with one café or repair workspace.
3. **End-of-day closeout.** Show sales and order counts by payment method, with a CSV export. Check the totals against the owner dashboard.
4. **Return and restock.** Record a partial return for a retail sale and restore only the returned units. Keep the original receipt and show the adjustment in sales.
5. **Smart low-stock list.** Show items below reorder level and how many servings a recipe can still make. Verify it after a sale.
6. **Invitation retry.** Resend a failed owner invitation from the saved workspace without creating another business or membership.
7. **Extra workflow demo.** Show a table bill, walk-in queue, or repair job that the main demo does not already cover.

