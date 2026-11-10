# Week 10 Work Plan — MVP Gap Review and Verification Preparation

**Date:** Thu 2026-11-05 to Wed 2026-11-11  
**Team:** 3 — SmartServe POS  
**Project:** SmartServe POS

> Week 10 focuses on reviewing the existing MVP, identifying remaining gaps, preparing repeatable verification, and collecting evidence needed for the Week 11 MVP verification and feature-freeze checkpoint.

## 1. Week 10 Objective

The main objective is to determine how much of the SmartServe POS MVP is supported by actual implementation and verification evidence.

The team will review existing functionality, compare it with the intended MVP requirements, identify unresolved issues, and prepare a clear verification process.

The team will prioritize reliability and evidence over adding new features.

### Expected outcomes

1. An MVP requirement review with a status for each requirement.
2. A prioritized list of known bugs and verification gaps.
3. A repeatable end-to-end verification procedure.
4. A documented plan for independent testing.
5. An organized evidence package for Week 11.

**Completion rule:** A task can only be marked completed when its implementation or review result has supporting evidence.

## 2. Starting Point — Previous Evidence

Week 9 established the following development evidence and limitations.

| Area | Previously recorded result | Limitation |
|---|---|---|
| Backend testing | 24 tests passed in the October 28 automated run | Does not prove independent testing |
| Frontend build | Build passed in the October 28 run | Does not prove every UI workflow |
| Browser/API checks | 27 checks passed against temporary PostgreSQL | Not a live Render database test |
| Screenshots | 12 screenshots recorded | Historical automated-run evidence |
| Owner-session checks | Recorded as passing locally | Independent reproduction remains pending |
| Main transaction | Order, simulated payment, receipt and inventory behavior demonstrated | Full independent reproduction still required |

References:
- [Week 8 automated evidence](../week-08/evidence/2026-10-28/README.md)
- [Week 9 evidence index](../week-09/evidence-index.md)
- [Week 9 verification handoff](../week-09/verification-handoff.md)
- [GitHub Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22)

These results are historical evidence. Week 10 must not describe them as newly executed tests.

## 3. Main Work Areas

### 3.1 MVP Requirement Review

Review the existing SmartServe POS MVP requirements and compare them with the current implementation.

Areas to review:

- Menu and item selection.
- Quantity selection and order calculation.
- Order creation and saved prices.
- Simulated payment processing.
- Paid-order status.
- Receipt generation.
- Recipe-based inventory deduction.
- Duplicate inventory deduction prevention.
- Owner-facing order and inventory information.

**Required evidence:**
- MVP requirement checklist.
- Relevant source-code or GitHub issue references.
- Screenshots or test results for verified requirements.
- Written explanations for partially verified or missing requirements.

**Expected result:** Every requirement receives one status: Verified, Partially Verified, Not Verified, or Blocked.

### 3.2 Bug and Gap Identification

Review existing issues and investigate problems that could affect the main MVP workflow.

Priority areas:

- Incorrect order totals or saved prices.
- Incorrect payment status.
- Receipt information inconsistencies.
- Recipe unit conversion.
- Inventory deduction accuracy.
- Duplicate inventory deduction.
- Owner-session and access restrictions.
- Errors during incomplete or invalid operations.

**Required evidence:**
- GitHub Issue links.
- Reproduction steps.
- Screenshots, logs, or test output.
- Severity and assigned owner.
- Expected and actual behavior.

**Expected result:** A prioritized bug and gap list with a clear next action for each unresolved problem.

### 3.3 End-to-End Verification Preparation

Prepare a repeatable test scenario for the central SmartServe POS workflow.

The verification should cover:

1. Open the application using the documented environment.
2. Access the cashier workflow.
3. Select menu items and quantities.
4. Confirm the calculated total.
5. Create the order.
6. Complete the simulated payment.
7. Confirm the paid status.
8. Open the generated receipt.
9. Check the corresponding inventory changes.
10. Confirm that inventory is not deducted twice.

**Required evidence:**
- Test procedure.
- Expected results.
- Actual results.
- Screenshots of important stages.
- Relevant logs or automated test output.
- Commit SHA and environment information.

**Expected result:** A repeatable verification procedure that another team member can follow.

### 3.4 Independent Verification Preparation

The previous milestone identified independent reproduction as an outstanding acceptance requirement.

Week 10 will prepare a non-author verification session.

The reviewer must not be the person who authored the specific fix being checked.

The verification record must include:

- Reviewer GitHub username.
- Date and time.
- Application environment.
- Tested commit or version.
- Setup and login method.
- Steps performed.
- Expected and actual results.
- Evidence links.
- Any failure or blocker.

**Important:** Preparing the verification procedure is not the same as completing independent verification. A passing result must only be recorded after the reviewer actually performs the test.

### 3.5 Documentation and Evidence Organization

Organize the Week 10 evidence so that every important claim can be traced to an artifact.

Evidence should include:

- Requirement review.
- Bug investigation records.
- GitHub issues.
- Relevant commits.
- Test output.
- Screenshots.
- Independent reviewer notes, if execution occurs.
- Known limitations and unresolved blockers.

**Expected result:** A structured Week 10 evidence folder and an updated evidence index.

## 4. Week 10 Task and Evidence Tracking

| Task | Required evidence | Status |
|---|---|---|
| Review MVP requirements | Requirement checklist | Planned |
| Review existing functionality | Source references and screenshots | Planned |
| Identify remaining bugs | GitHub Issues and reproduction notes | Planned |
| Prepare end-to-end test | Verification procedure | Planned |
| Arrange independent reviewer | Reviewer confirmation | Planned |
| Perform verification | Actual reviewer results and screenshots | Planned |
| Organize evidence | Evidence index and linked artifacts | Planned |
| Prepare Week 11 handoff | Gap summary and next actions | Planned |

Statuses must be updated based on actual work. Do not change a status to Completed without evidence.

## 5. Evidence Collection Standards

Every completed task should have a corresponding evidence record.

| Evidence type | What must be recorded |
|---|---|
| Screenshot | What is shown, date, environment and file path |
| Automated test | Command, test count, result and output file |
| Manual verification | Tester, steps, expected result and actual result |
| GitHub commit | Commit SHA and changed files |
| Bug report | Issue number, reproduction steps and result |
| Independent review | Reviewer identity, tested version and confirmation |
| Documentation | File path and relevant links |

### Evidence naming convention

Use descriptive names, for example:

- `mvp-requirement-review.md`
- `bug-review.md`
- `end-to-end-test-results.md`
- `independent-verification.md`
- `screenshots/`
- `logs/`

Do not create empty evidence files and describe them as proof of completed work.

## 6. Scope and Limitations

Week 10 prioritizes verification of the existing MVP.

The following are outside the confirmed Week 10 scope unless the team explicitly approves a change:

- Real payment gateway integration.
- Major new feature development.
- Production security certification.
- Concurrent load testing.
- Claims of complete production readiness.

The payment workflow remains simulated.

Existing automated results against isolated test databases must not be presented as verification of the live production database.

## 7. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Existing features lack sufficient evidence | Perform targeted checks and save results |
| Critical bugs remain unresolved | Record severity, owner and next action |
| Independent tester unavailable | Record the blocker and arrange another reviewer |
| Deployment instability | Preserve a tested local setup as a fallback |
| Late code changes break existing behavior | Repeat relevant regression checks |
| Evidence is incomplete or unclear | Use a consistent evidence naming and indexing process |

## 8. Week 11 Handoff Criteria

Week 10 should prepare the following for the next milestone:

- [ ] MVP requirements reviewed.
- [ ] Known bugs and gaps documented.
- [ ] High-priority issues assigned or awaiting confirmed owners.
- [ ] Main workflow verification procedure prepared.
- [ ] Independent reviewer arranged.
- [ ] Existing evidence organized and linked.
- [ ] Unverified requirements clearly identified.
- [ ] Remaining blockers documented.
- [ ] Week 11 verification tasks identified.

These are targets, not claims of completion.

## 9. Final Week 10 Decision

The team should finish Week 10 with a clear understanding of:

1. What SmartServe POS currently demonstrates.
2. What has been verified through automated testing.
3. What has been demonstrated manually.
4. What still requires independent verification.
5. Which bugs must be addressed before the Week 11 feature freeze.

**Week 10 completion target:** Prepare an evidence-backed MVP gap review and a repeatable verification process so that the team can make an informed MVP verification and feature-freeze decision in Week 11.

**Core principle:** No evidence, no completion claim.
