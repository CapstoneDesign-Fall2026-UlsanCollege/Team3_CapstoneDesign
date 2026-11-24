# Week 12 Individual Contribution Receipt — LamaMuskan (Sammygit15)

**Team:** 3 — SmartServe POS  
**Week:** 12  
**Date of recorded QA:** November 24, 2026 (KST)  
**GitHub login:** Sammygit15

## Contribution summary

| Contribution | What was done | Evidence |
|---|---|---|
| Owner signup failure reproduction | Tested owner registration in local Docker Compose and observed signup-email-unavailable message | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| API behavior capture | Ran API log inspection and recorded OPTIONS /auth/register → 200 and POST /auth/register → 503 | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| Defect reporting | Created Issue #27 with reproduction steps, expected/actual behavior, investigation status, screenshot, and acceptance criteria | [Issue #27](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/27) |
| Week 12 QA documentation | Prepared QA checklist, bug report, peer-test plan, evidence index, and AI/code-ownership audit with AI documentation assistance | [Week 12 folder](../) |

## Technical record

- Repository: CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign
- Repository HEAD reviewed: e89acd3ac1912446144cb93f1dba769ab721ea9f
- Runtime: local Docker Compose; FastAPI API container.
- Observed API responses: CORS preflight 200; registration POST 503.
- Frontend message: “Signup email is temporarily unavailable. Please try again later.”
- Working-tree caveat: backend/app/tenancy.py had an uncommitted local modification; evidence does not establish whether it was present in the running API container.

## Result and limitations

- **Signup test:** FAIL — registration email request returned HTTP 503.
- **Root cause:** Unknown; not confirmed.
- **Fix / retest:** Not completed or evidenced.
- **Independent peer verification:** Pending.
- **Implementation ownership:** No backend fix or code implementation is claimed in this receipt.

## AI use disclosure

AI assisted with documentation structure, troubleshooting guidance, and organizing the evidence record. The actual browser observation, Docker log command, and creation of Issue #27 were user-performed actions. AI did not execute the application test or generate its result.

## Next steps

1. Identify backend owner and capture the redacted exception for a controlled registration request.
2. Confirm container image/revision provenance and state of the local tenancy modification.
3. Verify the fix using the same controlled Docker Compose setup.
4. Ask a teammate who did not implement the fix to repeat signup.
5. Add real screenshots and backend output to the [evidence index](../evidence-index.md).
