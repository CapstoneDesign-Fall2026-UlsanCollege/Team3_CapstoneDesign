# Week 7 contribution — daydevil80

Sherap Hyolmo · Team 3 · October 21, 2026 (Korea)

My task was to follow up on the two failures from Week 6 and make the results easy to check for the midterm.

The recipe edit route was missing the unit conversion already used when adding a menu item. It now converts before comparing and saving the recipe. Entering 18 g with stock stored in kg saves 0.018 kg. Equivalent amounts also pass the open-order guard.

Orders now save the item name at creation, alongside the saved price. Renaming the menu item no longer changes a new order's receipt. Older orders did not store that name, so the migration keeps the label present at migration time. It cannot recover a name that was already overwritten.

Evidence:

- [Fixes and regression tests](../../../../smartserve-pos/backend/test_owner_management.py): alternate units, invalid units, old receipt/new order behavior and legacy migration.
- [24 backend tests passed](../evidence/2026-10-21/backend-tests.txt).
- [Frontend build passed](../evidence/2026-10-21/frontend-build.txt).
- [Two-latte check: expected and actual values](../evidence/2026-10-21/demo-results.json), reproduced with [this script](../verify_demo.py).
- [Shared report](../weekly-report.md), [demo script](../midtern-demoscript.md), and [Midterm Prep Issue #21](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21), which follows up on #20.

These checks were run with coding-agent assistance on isolated SQLite sample data. They are developer-side automated checks, not a teammate's browser result or a timed spoken rehearsal. The frontend build checks compilation; it does not prove every screen works.

Next: review and explain these changes, rehearse my segment, and have a non-author teammate follow [the retest steps](../retest-and-rehearsal.md). Independent testing and the timed rehearsal remain pending.
