# Week 12 Individual Contribution Receipt — LamaMuskan (Sammygit15)

**Team:** 3 — SmartServe POS  
**Week:** 12  
**QA date:** November 24, 2026 (KST)  
**GitHub login:** Sammygit15

## Contribution summary

| Contribution | Work recorded | Evidence |
|---|---|---|
| Owner signup failure reproduction | Reproduced the owner registration email-unavailable message in the local Docker Compose environment | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| API behavior inspection | Inspected API logs showing OPTIONS /auth/register → 200 OK and POST /auth/register → 503 Service Unavailable | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| Runtime environment inspection | Checked the API container and found GMAIL_SENDER, GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, and GMAIL_REFRESH_TOKEN unset; MAIL_PROVIDER defaults to gmail_api and SMARTSERVE_ENV is unset | [Evidence index](../evidence-index.md), items E12-02a and E12-02b |
| Compose configuration inspection | Checked resolved Docker Compose configuration; the API service receives DATABASE_URL only and has no Gmail environment entries or env_file | [Evidence index](../evidence-index.md), item E12-02b |
| Signup code-path inspection | Located the delivery exception handler in security.py and the Gmail sender/OAuth configuration requirements in mailer.py | [Bug report #27](../bug-report-27.md) |
| Defect tracking and QA documentation | Recorded the reproduction, expected/actual behavior, environment caveats, priority, acceptance criteria, and outstanding evidence in the Week 12 QA documents | [Week 12 folder](../) · [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |

## Technical record

- Repository: CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign
- Repository HEAD reviewed: e89acd3ac1912446144cb93f1dba769ab721ea9f
- Runtime inspected: local Docker Compose; FastAPI API container.
- Browser result: “Signup email is temporarily unavailable. Please try again later.”
- API log excerpt: OPTIONS /auth/register returned 200; POST /auth/register returned 503.
- Gmail configuration check: all four required Gmail sender/OAuth variables were absent from the API container.
- Resolved Compose configuration: no Gmail variables or env_file were configured for the API service.
- Source inspection: mailer.py requires GMAIL_SENDER and the three Google OAuth values; security.py catches delivery exceptions and returns the observed 503.
- Working-tree caveat: backend/app/tenancy.py had an uncommitted local modification, and ../docs/week-10-local-backup/ was untracked. Both were left untouched. Available evidence does not establish whether the tenancy edit was mounted into the running API container or identify the exact running image.

## Result and limitations

- **Signup test:** FAIL — the tested registration attempt returned HTTP 503 and displayed the temporary email-unavailable message.
- **Configuration finding:** Confirmed — the inspected API runtime lacked the required Gmail sender/OAuth configuration, and the resolved Compose configuration did not provide it.
- **Exact request exception:** Not captured. The missing sender configuration is the first expected mailer guard to fail, but no traceback from the observed request was recorded.
- **Fix / controlled retest:** Not completed. The Gmail configuration issue is intentionally deferred.
- **Independent peer verification:** Pending.
- **Implementation ownership:** No backend fix or code implementation is claimed in this receipt.

## AI use disclosure

AI assisted with troubleshooting guidance, documentation structure, and updating the Week 12 Markdown records on GitHub. The user performed the application reproduction and local PowerShell/Docker inspection commands and supplied their outputs. The receipt does not claim that AI executed the application test or independently verified the runtime.

## Next steps

1. When work resumes, provide valid Gmail sender/OAuth settings through a private, untracked configuration source; do not commit credentials or tokens.
2. Recreate/restart the API container and capture a redacted delivery outcome.
3. Repeat owner signup and verify the actual activation email flow under the same controlled conditions.
4. Record exact revision, environment, and runtime provenance, including whether the local tenancy modification is mounted.
5. Obtain an independent teammate retest and add real screenshots/output to the [evidence index](../evidence-index.md).
