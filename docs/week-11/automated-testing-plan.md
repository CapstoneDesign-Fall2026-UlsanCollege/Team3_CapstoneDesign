# Week 11 Automated Testing Plan — SmartServe POS

**Week:** 11  
**Period:** November 12–18, 2026  
**Branch:** `main`  
**Focus:** Improving automated test coverage and validating the existing CI workflow

## 1. Purpose

This document defines the testing work planned for Week 11. The goal is to find defects earlier, reduce regressions when features change, and keep repeatable evidence of test execution.

This is a plan, not a record of completed tests. Results will be added only after the corresponding tests have actually been run.

## 2. Current Starting Point

Based on the project files inspected before this plan was created:

- The backend contains Python test files, including `test_trash.py`.
- The frontend is a React and TypeScript application built with Vite.
- The frontend `package.json` currently has a production build script but no test script or configured test runner.
- The repository already contains `.github/workflows/week9-validation.yml`.

Week 11 work should extend the existing setup where practical. It should not create a duplicate CI workflow or count Week 10 test results as Week 11 results.

## 3. Backend Testing

### Planned work

1. Review the existing backend test modules and understand what each one covers.
2. Identify important uncovered behaviour and edge cases.
3. Add focused tests where a real coverage gap is found.
4. Run the relevant tests locally using the project's existing test framework.
5. Save the command, date, commit, pass/fail summary, and full output.

### Areas to review

- Owner and user-management behaviour.
- Order and payment behaviour, including invalid or failed operations.
- Prevention of duplicate payment processing, where supported by the current implementation.
- Inventory deduction and recipe unit conversion.
- Trash or soft-delete behaviour and restoration.
- Preservation of historical order and receipt information.

The list is a review scope. A test will be added only where the corresponding feature exists and can be tested reliably.

## 4. Frontend Testing

### Planned work

1. Review the frontend components and current project dependencies.
2. Select a test framework and supporting libraries compatible with the installed Vite, React, TypeScript, and Node versions.
3. Add a test command to `package.json`.
4. Write focused tests for important component behaviour and user interactions.
5. Run the tests and retain the actual output.

Do not install a testing framework until compatibility has been checked. Do not report frontend tests as complete merely because the production build succeeds; building and testing are different checks.

## 5. Continuous Integration (GitHub Actions)

### Planned work

1. Inspect the existing `.github/workflows/week9-validation.yml` workflow.
2. Confirm which backend, frontend, and browser/API checks it already runs.
3. Reuse or update that workflow to run any new Week 11 tests when appropriate.
4. Trigger the workflow on GitHub Actions and inspect the result for the exact commit.
5. Save the workflow run URL, commit SHA, job statuses, and relevant artifacts.

A workflow file existing in the repository does not by itself prove that a run passed. Only an actual completed run can be recorded as passing evidence.

## 6. Test Design and Quality Checks

For each selected feature, consider:

- **Normal case:** expected behaviour with valid input.
- **Invalid case:** missing, malformed, or unsupported input.
- **Failure case:** expected behaviour when an operation fails.
- **Regression case:** a previously fixed issue that should not return.

Where practical, check that a test can detect an incorrect result by temporarily changing an expectation locally, confirming that the test fails, and then restoring the correct expectation. Do not commit the intentional incorrect change.

## 7. Evidence and Documentation

Store Week 11 evidence separately from earlier weeks:

| Evidence | Location |
|---|---|
| Backend and frontend test output | `evidence/test-results/` |
| GitHub Actions run details and artifacts | `evidence/github-actions/` |
| Relevant test or CI screenshots | `evidence/screenshots/` |

For each run, record:

- Date and time.
- Tester.
- Branch and commit SHA.
- Exact command or workflow run.
- Pass/fail result and test count, where available.
- Known warnings, failures, limitations, and follow-up work.

## 8. Completion Criteria

Week 11 testing work can be marked complete only when the relevant evidence exists:

- Existing backend tests have been reviewed and the selected test suite has been run.
- Any newly added backend tests have been run and their results recorded.
- A compatible frontend test setup has been evaluated; implemented tests have been run and recorded.
- The existing CI workflow has been checked, and any claimed successful CI result is supported by an actual run.
- Test limitations and unresolved failures are documented.

## 9. Reporting Rule

This plan describes intended work. Do not mark a task complete, claim a test passed, or claim a bug was fixed until it has been verified. Week 10 evidence remains in the Week 10 documentation and must not be presented as Week 11 evidence.
