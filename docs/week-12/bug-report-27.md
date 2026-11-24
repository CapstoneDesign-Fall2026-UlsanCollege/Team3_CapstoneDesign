# Bug Report — Issue #27: Owner Registration Email Returns 503

**GitHub issue:** [#27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27)  
**Observed:** November 24, 2026 (KST)  
**Status:** Open; missing Gmail runtime configuration confirmed; exact request exception not captured; no fix or retest.

## Summary

Submitting the owner registration form to request the signup/activation email results in a temporary email-unavailable message. The API log excerpt shows the registration POST returning HTTP 503.

## Reproduction

1. Start SmartServe POS using local Docker Compose.
2. Open the owner registration page.
3. Enter registration details and submit the form.
4. Observe the frontend response and API logs.

## Expected and actual behavior

| | Result |
|---|---|
| Expected | Configured signup-email flow completes, or an actionable error is returned if delivery is unavailable. |
| Actual | “Signup email is temporarily unavailable. Please try again later.” |
| API evidence | OPTIONS /auth/register → 200 OK; POST /auth/register → 503 Service Unavailable. |
| Missing evidence | Captured log excerpt does not include the underlying exception or establish the email provider's state. |

## Environment and revision

- Runtime: local Docker Compose; FastAPI API container.
- Date: November 24, 2026 (KST).
- Repository HEAD reviewed: e89acd3ac1912446144cb93f1dba769ab721ea9f.
- Working-tree caveat: backend/app/tenancy.py had an uncommitted local modification. Evidence does not establish whether the running container used that modified file or identify its exact image.
- Screenshot and request-log excerpt are attached to Issue #27.

## Severity and priority

- **Severity:** High — owner signup/email activation was blocked for the tested attempt.
- **Work priority:** P1 proposed — investigate and restore a core onboarding path promptly.
- Severity describes user impact; priority describes scheduling urgency.

## Investigation status

The confirmed configuration defect is that the running API container lacks all required Gmail settings, and the resolved Compose configuration does not provide them. The code inspection shows that `mailer.py` requires `GMAIL_SENDER` plus `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, and `GMAIL_REFRESH_TOKEN`; `security.py` catches delivery exceptions and returns the observed 503. The exact exception thrown during the captured registration request was not logged, so do not claim a directly captured traceback or successful Gmail API call. The immediate sender guard is expected to fail first while `GMAIL_SENDER` is absent. Inspect variable presence only; never publish credentials, tokens, or secrets.

## Owner and next check

- GitHub issue assignee: Unassigned when reviewed.
- Next check: configure valid Gmail sender/OAuth settings through a private, untracked environment file; recreate the API container; capture redacted delivery outcome; then repeat owner signup and activation.
- Retest owner: teammate who did not implement the fix.

## Acceptance criteria

- [ ] Confirm root exception or configuration fault with redacted evidence.
- [ ] Correct the underlying failure.
- [ ] Return appropriate success or actionable failure response.
- [ ] Verify actual email/activation flow in Docker Compose.
- [ ] Repeat under same controlled conditions and record exact revision/environment.
- [ ] Obtain independent peer verification.
- [ ] Link test output and screenshots in evidence-index.md.

A later non-reproduction does not erase this recorded failure. Close only after the cause/fix and controlled retest are documented.
