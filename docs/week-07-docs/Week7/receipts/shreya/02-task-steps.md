# Shreya: timed demo rehearsal and evidence audit

Owner: shrey776 (Shreya). Status: ready to perform, not yet run by the member.

Use the separate setup in 01-setup.md. Your task is to run/time a real rehearsal, identify any weak step and verify that the report's claims have direct proof.

## Rehearsal

1. Record tested commit, browser/device, date/time KST and starting inventory/sales. Use a fresh isolated database if possible. Save 01-start-inventory.png and 02-start-sales.png.
2. Start a real timer or screen recording when the introduction begins. If only rehearsing your own segment, label it a solo rehearsal. Do not label it a complete team rehearsal unless all planned speaking segments are included.
3. Follow the four-minute speaking plan in 05-speaking-notes.md: introduce the café problem, create two lattes, pay with simulated cash, show the receipt, inventory and sales, and explain the product limits.
4. Expected: order total 9,000 KRW, milk -500 ml, beans -36 g, one additional paid order and sales +9,000 KRW. Use before/after differences if your starting data is not fresh.
5. Stop the timer after the final limitation/next-action statement. Record actual minutes:seconds and proof. The target is 3–5 minutes, not an assumed result. Save receipt, final inventory and sales screenshots and the recording if available.
6. If outside 3–5 minutes or interrupted, record why. Adjust one specific part and rehearse again if possible. Record each attempt separately; repeated runs add sales and change stock. Use an unused isolated project or record the new baseline for each attempt.

## Fallback and evidence audit

7. Open the copied reference-only evidence. Practice explaining it as recorded developer evidence if the live app stops. Record whether links/files opened. This checks the fallback material, not a new live successful payment.
8. Check each claim against its direct source:
   - Simulated payment and stock deductions: current demo-results.json (automated); your own browser screenshots after the rehearsal.
   - Recipe-unit and receipt-name fixes: developer regression evidence. Only describe as independently browser-tested if you actually repeat the written retest.
   - Payments: simulated; no real payment gateway claim.
   - Original names of older pre-migration receipts: cannot be recovered automatically.
   - Independent test and actual rehearsal duration: must point to a named human result, not just a plan or build log.
9. Fill 03-result.md and 04-report-entry.md. Link an exact screenshot/result per claim and record any broken link or unsupported claim. Put the first blocker and next action in the result if the demo cannot finish.

You can make a useful contribution through timing, evidence checking and recording problems. Do not claim another person's fixes or test execution as your own.
