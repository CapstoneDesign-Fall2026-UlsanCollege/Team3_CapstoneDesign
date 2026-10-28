# Week 8 addendum — current proof and next verification milestone

**Team:** 3 — SmartServe POS

**Prepared by:** `daydevil80`, with coding-agent assistance

**Date:** October 28, 2026, Korea time

This note supplements the [shared Weekly Report](weekly-report.md) and [post-midterm note](post-midterm-file.md). The previously uploaded documents remain unchanged. The individual entry below and the new evidence make the current verification work traceable without replacing anyone else's contribution.

## daydevil80 contribution for the shared report

| Student | Week 8 contribution | Evidence |
|---|---|---|
| Sherap Hyolmo (`daydevil80`) | Requested and documented fresh automated verification of the frozen POS path with coding-agent assistance. The current source passed 24 backend tests, the frontend build and 27 browser/API checks on a separate temporary PostgreSQL database. Recorded 12 screenshots and expected/actual values for payment failure/retry, duplicate protection, recipe conversion, receipt history and owner sessions. Connected those results to the Week 8 lessons and the Week 9 milestone. Codex executed the supplied automated run. | [Individual receipt](receipts/daydevil80.md), [current evidence](evidence/2026-10-28/README.md), [raw checks](evidence/2026-10-28/browser-results.json), [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) |

## Course lesson and source

We believed a completed presentation package would communicate readiness. The [supplied October 26 feedback](feedback-source.md) and the [midterm rubric](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/course-materials/blob/main/student-starter-kit/docs/midterm-presentation-rubric.md) distinguish presentation material, checked behavior and individual ownership. Therefore, our Week 9 decision is to make the current path reproducible and directly link its evidence before adding more features.

This is our interpretation of the written sources. It does not invent spoken comments from the midterm or an instructor grade.

## Project lesson and source

We believed the existing passing tests were sufficient for menu and ingredient editing. The [Week 6 failures](../week-06/automated-check.md) showed that an alternate-unit edit could save 18 g as 18 kg and that renaming a menu item could change historical labels. [The fix](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0d5fecdf827deb12b7d4d560e392bfb06d868591) added recipe normalization and original-name snapshots. The [fresh PostgreSQL browser/API results](evidence/2026-10-28/browser-results.json) now support those specific corrected cases. Therefore, the next milestone repeats the same bounded cases in a non-author handoff rather than broadening the feature list.

## What is currently proved

- **Current source:** `b68df10eb46d25bc2ac00e28412b71df792deb7f`. The later teammate uploads through `c007522` add Week 8 documents; the evidence records the actual tested source rather than relabelling it.
- **Backend regression:** 24 passed, on isolated SQLite used by the existing unit suite.
- **Build:** TypeScript and Vite completed. The existing Vite configuration warning remains visible in the log.
- **Browser/API:** 27 passed against a fresh temporary PostgreSQL cluster, with the actual built frontend and FastAPI routes. Twelve app screenshots accompany the checks.
- **Correctness:** failed payment leaves stock/sales unchanged, retry completes the same order, duplicate payment does not deduct again, an 18 g edit stores 0.018 kg, and a new order's original name/price survive later menu editing.
- **Owner boundary:** protected inventory and sales routes reject anonymous requests and reject access after logout. Login uses generated test credentials that are not published.

These results are developer-side automated proof. The complete index and environment limits are in [the current evidence note](evidence/2026-10-28/README.md).

## MVP decision

**Status: gap.** The implemented simulated checkout path has current technical proof. The next release gate is a named non-author reproduction using the actual team/demo setup, with an evidence-linked result and confirmed contribution records.

Real payment-provider integration remains **outside the agreed simulated-payment scope**, rather than an unfinished requirement for this milestone. Advanced analytics, optional UI customization and unrelated feature expansion stay deferred. The local session checks do not establish production-grade authentication or a verified public deployment.

## One Week 9 milestone

**Milestone:** independently reproduce the frozen two-latte path and corrected editing behavior.

**Accountable coordinator:** `daydevil80`.

**Tracking:** [Week 8 reset / Week 9 verification Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22).

**Next action:** provide [the verification handoff](verification-handoff.md), confirm a non-author tester's exact GitHub login, and record the tested commit and starting data before the run.

**Review point:** the Week 9 team review, before expanding the feature scope.

Success means the tester records setup, expected/actual values and proof for one sale, failed/duplicate payment handling, recipe conversion and receipt history. An error is recorded with its first failing step, owner and next check. Any required fix stays small and receives a repeat of the same failed case.

Each enrolled member adds their own current lesson/result and direct evidence in the existing shared report. This addendum supplies daydevil80's work only; it does not assign completed work to other members.

## Navigation and ownership clarifications

- The enrolled logins from the written feedback are `daydevil80`, `Sammygit15`, `Shuzita`, `shrey776` and `ualsom`.
- The existing report confirms the display-name mapping Lama Muskan / LamaMuskan / `Sammygit15`.
- [The implementation commit](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0d5fecdf827deb12b7d4d560e392bfb06d868591) and [daydevil80's Week 7 receipt](../week-07-docs/Week7/receipts/daydevil80.md) identify ownership of the recipe/history fix. Documentation or review contributions should link their own authored records separately.
- The report in this folder is [weekly-report.md](weekly-report.md), and the test source is [test_owner_management.py](../../smartserve-pos/backend/test_owner_management.py). These direct links supplement older branch/path references without editing the uploaded files.

## Week 8 requirements covered by this addendum

| Requirement | Where to open it |
|---|---|
| Course lesson with source | Course lesson above; [written feedback](feedback-source.md) and linked rubric |
| Project lesson with evidence | Project lesson above; failure, implementation and fresh-result links |
| Current project proof | [October 28 evidence](evidence/2026-10-28/README.md) |
| Explicit MVP status | Gap decision above |
| Focused milestone, owner and next action | Milestone above and [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22) |
| daydevil80's current contribution | Entry above and [receipt](receipts/daydevil80.md) |

The additive documents and the shared report should be read together. A complete personal contribution record still comes from each student's actual work, not the presence of a prepared file.
