# Setup and evidence links

Use application commit `0d5fecdf827deb12b7d4d560e392bfb06d868591` for these steps. This is the version containing the recipe and receipt fixes. Check the actual version you run and record it.

## Separate demo setup

Install Git and Docker Desktop, then open PowerShell in a new folder of your choice:

```powershell
git clone https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign.git SmartServe-Week7-Test
Set-Location SmartServe-Week7-Test
git checkout 0d5fecdf827deb12b7d4d560e392bfb06d868591
Set-Location smartserve-pos
docker compose -p YOUR-UNUSED-PROJECT-NAME up -d --build
```

Replace YOUR-UNUSED-PROJECT-NAME with a fresh name such as shuzita-week7-01 or shreya-week7-01. A separate project uses a separate database volume, but still needs ports 5173, 8000 and 5432 free. If another app is using these ports, record the blocker and arrange a separate machine or agreed demo time. Do not delete shared volumes or reset shared stock. Reusing a project name may reuse earlier data.

Open the app at http://localhost:5173 and API docs at http://localhost:8000/docs. Wait until http://localhost:8000/health returns status ok. If setup fails, save the exact error and first failing step. These Docker setup instructions have not been independently executed by either member in this package.

## Links

- Shared report: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/docs/week-07-docs/Week7/weekly-report.md
- Midterm preparation: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/21
- Current app source: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/commit/0d5fecdf827deb12b7d4d560e392bfb06d868591
- Team automated evidence: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/tree/main/docs/week-07-docs/Week7/evidence/2026-10-21
- Project README: https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/blob/main/smartserve-pos/README.md

The copied evidence in reference-only is developer-side automated evidence from October 21, not a personal result by Shuzita or shrey776. It uses SQLite service calls and a frontend build. It does not prove their browser check, spoken rehearsal or PostgreSQL behavior.
