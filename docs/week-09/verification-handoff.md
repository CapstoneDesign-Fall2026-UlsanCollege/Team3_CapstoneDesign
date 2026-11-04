# Issue #22 — non-author verification handoff

**Prepared:** November 4, 2026, with Codex assistance. **Status: NOT EXECUTED.**

Coordinator: `daydevil80`. Tester: **unconfirmed**; must not be the author of the recipe/history fix. Tracking: [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22).

This carries the frozen scenario forward from the handoff in historical commit `0b84c06`; the old Week 8 handoff was removed upstream. Existing files are not restored or overwritten.

## Setup and version

1. Confirm tester login and actual demo target with the coordinator. Record URL, database type, date/time KST, browser/device and exact application commit. Reference checkout reviewed for these instructions: `2052e9c770a512c6bcad932ce66af1a71a980693`; this is not a tested/deployed-version claim. If the deployed commit cannot be established, record that limitation.
2. Use a fresh checkout of the agreed commit and [application setup](../../smartserve-pos/README.md). For a local fallback, from `smartserve-pos`, use a new unused Compose project name such as `docker compose -p smartserve-week9-nonauthor up -d --build`. Check ports 5173/8000/5432 first. A different project name does not avoid port conflicts. Do not remove another project's database or volumes. Record startup/health output and any intervention; Docker startup has not been verified in this follow-up.
3. Local frontend: `http://localhost:5173`; API docs: `http://localhost:8000/docs`. Render target, if agreed: `https://smartserve-pos-ycbj.onrender.com/`. Local success does not verify Render. Use owner login `/etalogin` and privately supplied credentials. Never publish passwords, cookies or session tokens.
4. Use dedicated approved sample data. Record actual milk/beans, units, latte recipe/price, paid-order count and selected day's KST sales before touching data. Never reset the shared Render database. If its baseline differs, record expected deltas before the test; uncontrolled simultaneous orders make the result inconclusive.

## Frozen checks and tester result form

All Actual cells deliberately remain **not run**. Add screenshot/log paths and observed values for each row; retain failures.

| Step | Expected for fresh seed data | Actual / result / evidence |
|---|---|---|
| Baseline | Milk 5,000 ml; beans 1,200 g; latte ₩4,500 with 250 ml milk + 18 g beans; no paid orders/sales | Not run |
| Create two lattes | Open order, total ₩9,000; stock/sales unchanged; save order ID | Not run |
| Refresh tab | Same saved order ID and ₩9,000 after loading | Not run |
| Simulated failure | For same order, failed card payment returns HTTP 402; order open; stock/sales unchanged | Not run |
| Successful cash retry | Same order paid; receipt two lattes at ₩4,500; milk 4,500 ml; beans 1,164 g; one paid order; sales ₩9,000 | Not run |
| Duplicate payment | HTTP 409 on same order; no additional stock movement, paid order or sales | Not run |
| Change beans g to kg | Stock 1.164 kg; reorder threshold 0.25 kg; per-latte beans 0.018 kg | Not run |
| Rename/reprice/edit | Record new name; price ₩6,000; enter beans 18 g and verify saved recipe 0.018 kg | Not run |
| Reopen original receipt/history | Original Caffè Latte name, ₩4,500 each, total ₩9,000 retained after edit | Not run |
| Sell one renamed latte | Milk 4,250 ml; beans 1.146 kg; two paid orders; sales ₩15,000; new receipt uses new name/₩6,000 | Not run |
| Owner boundary | Anonymous inventory/sales requests 401; owner can access; logout restores denial | Not run |

For nonzero baselines, first sale deducts 500 ml milk and 36 g beans and adds ₩9,000/one paid order; second sale deducts 250 ml/18 g and adds ₩6,000/one paid order. Compare inventory movement records to the same order IDs. Record unrelated activity or a KST date rollover as a test limitation.

The UI has no dedicated failed-payment button. Using API docs for the selected environment, submit the existing order's payment endpoint with `{"method":"card","result":"failed"}`; then retry with `{"method":"cash","result":"paid"}`. Repeat that paid request to check 409. Record endpoint, order ID, HTTP status and sanitized response. Consult [regression source](run_validation.py) for route examples; it is comparison material, not a replacement for the tester's observation.

## Required completion details

- Tester login / non-author confirmation: **pending**.
- Date/time KST / browser / device: **pending**.
- Exact source hash / deployment revision / URL / database: **pending**.
- Setup steps and help received; was the handoff followed without live coaching?: **pending**.
- Baselines, order IDs, expected/actual values and screenshot/log links: **pending**.
- Overall outcome (pass/fail/blocked), first failing/confusing step: **pending**.
- Failure owner, next action and retest evidence: **pending**.

Save the completed receipt and sanitized screenshots under `evidence/<date>-<tester-login>/`, add the tester's own row to [the shared report](weekly-report.md), and link the outcome in Issue #22. These are planned steps, not completed publication. Existing [October 28 results](../week-08/evidence/2026-10-28/README.md) are developer automation; [Week 9 CI](validation-workflow.md) uses isolated SQLite. Neither closes this human acceptance gate.
