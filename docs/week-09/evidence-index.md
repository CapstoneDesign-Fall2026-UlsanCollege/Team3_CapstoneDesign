# Week 9 evidence index and limits

**Prepared:** November 4, 2026. This index links existing artifacts without changing their authorship or claiming fresh execution.

| Evidence category | Actual artifact | What it supports / limitation |
|---|---|---|
| November 2 manual screen review | [Lama Muskan receipt](receipts/lamaMuskan.md) | Author's recorded screen observations; not independent reproduction of the frozen two-latte scenario |
| Dashboard/history | [Screenshot](evidence/render-paid-order-history.png) | Recorded ₩12,500 / three paid orders; snapshot, not a before/after deduction test |
| Menu/recipes | [Screenshot](evidence/render-menu-recipes.png) | Visible recipe configuration |
| Inventory | [Screenshot](evidence/render-inventory-after-order-4.png) | Observed inventory after Order #4; baseline evidence still required for independent test |
| Receipt | [Screenshot](evidence/render-receipt-4.png) | Order #4 Americano, simulated CASH ₩3,500; different scenario from two lattes |
| Week 9 CI | [Recorded Run #5](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/actions/runs/41421184139), [workflow](../../.github/workflows/week9-validation.yml), [script](run_validation.py), [notes](validation-workflow.md) | Existing report records three passing jobs and uploaded artifacts; browser/API uses isolated SQLite. Remote artifact availability was not reverified in this follow-up |
| October 28 developer automation | [Summary](../week-08/evidence/2026-10-28/README.md), [24 unit tests](../week-08/evidence/2026-10-28/backend-tests.txt), [build](../week-08/evidence/2026-10-28/frontend-build.txt), [27 checks](../week-08/evidence/2026-10-28/browser-results.json) | Codex at daydevil80's request, source `b68df10eb46d25bc2ac00e28412b71df792deb7f`; unit tests isolated SQLite; browser/API temporary PostgreSQL; historical automation, not a human Week 9 test |
| October 28 screenshot package | [12-image gallery](../week-08/evidence/2026-10-28/SCREENSHOTS.md), [hash manifest](../week-08/evidence/2026-10-28/screenshot-sha256.json) | Before/after evidence for the historical automated run |
| Final Demo recorded backend output | [Test output](../../smartserve-pos/docs/Final-Demo/Evidence/06-Backend-Testing/backend-test-results.txt) | Separate historical report; do not merge its count with later runs |
| Earlier development evidence | [Existing roadmap evidence index](Roadmap.md#2-complete-evidence-index) | Weeks 2–8 and Final Demo links retained; earlier failures remain historical failures |
| Acceptance gate | [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22), [new handoff](verification-handoff.md) | Issue read November 4: open, non-author result pending; old Week 8 handoff link was removed upstream |
| Current documentation contribution | [daydevil80 receipt](receipts/daydevil80.md), [feedback follow-up](feedback-follow-up.md) | AI-assisted documentation, student confirmation pending; no application test executed |

The existing validation notes still contain an older “Awaiting run result” table; the shared report and Lama Muskan receipt subsequently record Run #5 as passed. Their original text is retained. Use the specific run reference rather than treating the older table as a new failure or claiming a fresh run.

Payments remain simulated. No new live Render database, production-security, concurrency, or real-payment-provider verification is claimed. Missing personal contributions and the independent result remain open; existing screenshots must not be substituted for them.
