# Week 6 Definition of Done

Team 3 · Updated October 14, 2026 · Related [Issue #20](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/20)

The implementation issue is currently closed. The checklist below records what this new check actually proves; it does not change the issue's state or claim the full Week 6 work is complete.

- [x] Repeatable steps and expected results written before the scripted run.
- [x] Exact tested application commit linked.
- [x] Fresh sample data separated from the shared store.
- [x] Menu details can be edited after stock exists.
- [x] Ingredient g/kg conversion preserves current stock, threshold, linked recipe, and earlier movement quantities in the checked case.
- [x] Existing order unit prices and totals stay unchanged after a menu-price edit.
- [x] A new sale uses the new price and converted recipe correctly.
- [x] Failed and duplicate simulated payments leave stock/sales unchanged.
- [x] Fresh screenshots and raw actual results linked.
- [ ] Historical receipts keep the original product name after a rename. **Failed: old receipt adopts the new menu name.**
- [ ] Editing a recipe using a compatible alternate input unit stores the correct converted amount. **Failed: 18 g saves as 18 kg.**
- [ ] Cashier availability stays correct after that alternate-unit recipe edit. **Failed as a consequence of the wrong stored quantity.**
- [ ] A non-author teammate follows the written steps without coaching and completes the Tested-By Note.
- [ ] Each of the five members confirms or completes their own contribution row and requested receipt.
- [ ] The observed bugs are fixed and the same checks rerun against a linked implementation change.
- [ ] The relevant issue status is reviewed against these new results.

The current status is **partial verification with failures recorded**. See [automated-check.md](automated-check.md) and [follow-up-problems.md](follow-up-problems.md).
