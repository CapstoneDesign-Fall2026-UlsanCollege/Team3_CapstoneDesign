# Week 8 Individual Evidence Receipt — Shreya

**GitHub login:** `shrey776`
**Team:** Team 3 — SmartServe POS
**Week:** 8
**Date:** October 28, 2026

## Contribution: Evidence Review and Verification Planning

Reviewed the October 28 verification package and compared the documented claims with the recorded results and screenshots. Recorded the review, lessons and proposed Week 9 action in the shared report.

**Contribution record:** [Week 8 Weekly Report](../weekly-report.md)

## Evidence Reviewed

- [Verification summary](../evidence/2026-10-28/README.md)
- [Expected and actual browser/API results](../evidence/2026-10-28/browser-results.json)
- [Backend test output](../evidence/2026-10-28/backend-tests.txt)
- [Frontend build output](../evidence/2026-10-28/frontend-build.txt)
- [Screenshot gallery](../evidence/2026-10-28/SCREENSHOTS.md)

## Review Findings

| Claim reviewed | Recorded evidence | Finding |
|---|---|---|
| Backend regression tests | Test output reports 24 passing tests | Supports the checked backend cases |
| Frontend production build | TypeScript and Vite completed | Supports successful compilation, not every live behavior |
| Current browser/API behavior | 27 passing checks against temporary PostgreSQL | Supports the specific recorded cases |
| Payment and inventory consistency | Receipt, stock and sales screenshots with raw results | Two lattes total ₩9,000 and deduct 500 ml milk and 36 g beans once |
| Owner access | Anonymous protected requests return 401; login permits access; logout removes access | Current local session checks differ from older documentation describing unenforced access |
| Verification boundaries | Results identify the source commit, environment and automation operator | These records do not establish public deployment or independent human testing |

## Course Lesson

Different forms of evidence support different claims. A screenshot, passing build and independent teammate test cannot be treated as interchangeable proof. Important claims should link directly to the evidence that supports them.

**Source:** [Midterm Presentation Rubric](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/course-materials/blob/main/student-starter-kit/docs/midterm-presentation-rubric.md)

## Project Lesson

Project evidence needs a date, application commit and test environment. Older records may describe an earlier version or different verification method. Therefore, current claims should reference the relevant current results and clearly preserve their limitations.

**Decision:** Record the tested version and actual results when performing the next verification task.

## MVP Status

**Still has a gap.** Current automated evidence supports the checked simulated transaction path. The team’s next milestone is the documented verification handoff, tracked in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22).

## Proposed Week 9 Action

- **Owner:** Shreya (`shrey776`), after confirming the assignment.
- **Task:** Personally follow the setup instructions and repeat the frozen two-latte path using separate sample data.
- **Success signal:** A ₩9,000 paid order produces the correct receipt, deducts 500 ml milk and 36 g beans once, and creates the matching sales update.
- **Evidence to record:** Tester login, date, application commit, setup, browser/device, starting values, expected/actual results, screenshots and the first failure if one occurs.
- **Instructions:** [Verification handoff](../verification-handoff.md)

## Assistance and Evidence Boundary

Codex automation executed the reviewed browser/API run at daydevil80’s request. My contribution is the personal review and planning described above, provided that I completed that review. This receipt does not claim that I independently executed the supplied tests or completed a narrated rehearsal.
