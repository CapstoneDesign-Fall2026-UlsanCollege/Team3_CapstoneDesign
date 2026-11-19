# Bug Review — Week 10

**Project:** SmartServe POS  
**Team:** Team 3  
**Review Period:** November 5–11, 2026  
**Focus:** MVP Gap Review and Verification Preparation

## 1. Purpose

Record bugs, unexpected behavior, and technical gaps discovered while reviewing the existing MVP. Each confirmed issue must have reproducible steps or other supporting evidence, an impact assessment, and a follow-up owner or status.

**No new Week 10 bugs are confirmed by this template.** Investigation targets below must not be treated as defects until observed and documented.

## 2. Reporting Rules

Every confirmed bug record should include:
- Clear title and affected feature.
- Date, reporter, environment, and application commit.
- Reproduction steps.
- Expected and actual behavior.
- Original screenshots, logs, API responses, or test output.
- Severity and priority.
- Assigned person and related GitHub issue, if applicable.
- Fix and retest result.

If a suspected problem cannot be reproduced, record it as an observation or investigation item rather than a confirmed bug.

## 3. Severity

| Severity | Meaning |
|---|---|
| Critical | Prevents core operation or causes serious data integrity problems |
| High | Breaks an important MVP workflow or produces incorrect business data |
| Medium | Affects a feature but has a reasonable workaround |
| Low | Minor UI, usability, or non-critical behavior issue |

Severity describes impact; priority describes urgency.

## 4. Bug Register

| ID | Title | Feature | Severity | Status | Evidence |
|---|---|---|---|---|---|
| W10-B01 | To be added after investigation | Pending | Not assessed | Not Reviewed | Pending |
| W10-B02 | To be added after investigation | Pending | Not assessed | Not Reviewed | Pending |
| W10-B03 | To be added after investigation | Pending | Not assessed | Not Reviewed | Pending |

Add rows only when an actual issue or observation is identified.

## 5. Investigation Targets

| Area | Investigation Focus | Evidence to Collect |
|---|---|---|
| Menu | Item selection and displayed prices | Screenshots and test result |
| Order calculation | Quantity changes and total calculation | Calculation comparison |
| Order creation | Saved order details and prices | Database record or API response |
| Payment | Simulated payment and order status | Payment response and order record |
| Receipt | Displayed order information | Receipt screenshot |
| Inventory | Recipe-based stock deduction | Before/after inventory records |
| Duplicate processing | Repeated processing of the same order | Inventory movement history |
| Recipe units | Unit conversion and saved quantities | Input and stored values |
| Owner-facing screens | Information consistency | Screenshots and relevant records |
| Error handling | Invalid inputs and failed operations | Logs and error responses |

## 6. Previously Documented Project Limitations

These are context from earlier project records, not newly discovered Week 10 bugs:

| Item | Known Context | Follow-up |
|---|---|---|
| Real payment integration | Current MVP uses simulated payment | Keep real gateway integration outside this verification scope |
| Historical item names | Older overwritten names may not be recoverable | Document limitation when reviewing historical records |
| Production verification | Previous automated checks included isolated test environments | Record and verify the actual demo environment separately |
| Independent verification | Earlier automated results do not replace non-author review | Arrange reviewer and preserve independent evidence |

Related tracking: GitHub Issue #22 — Week 8 reset and Week 9 milestone: verify the frozen SmartServe path.

## 7. Individual Bug Report Template

### Bug ID: W10-B__

**Title:**  
**Affected Feature:**  
**Date Discovered:**  
**Reported By:**  
**Environment:**  
**Application Commit:**  
**Severity:** Critical / High / Medium / Low  
**Priority:**  
**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**  
**Actual Result:**  
**Evidence Links:**  
**Related GitHub Issue:**  
**Assigned To:**  
**Status:** Reported / Investigating / Confirmed / Fix In Progress / Fixed / Retest Required / Closed / Blocked  
**Retest Result:** Not Tested / Passed / Failed  
**Additional Notes:**

## 8. Week 10 Summary

| Metric | Result |
|---|---|
| Confirmed bugs | Pending investigation |
| Observations requiring investigation | Pending investigation |
| Critical issues | Pending investigation |
| High-priority issues | Pending investigation |
| Issues assigned for follow-up | Pending investigation |
| Issues requiring Week 11 retesting | Pending investigation |

## 9. Completion Criteria

- Investigation targets are checked or blockers are recorded.
- Every confirmed bug has reproduction steps and evidence.
- Severity and responsibility are recorded.
- Related GitHub issues are linked where appropriate.
- Fixes are not marked complete without retesting.

**Final rule:** Do not invent bugs, claim fixes without retesting, or close issues without evidence.