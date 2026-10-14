# Setup and short demo

Use the GitHub application source for this Week 6 check. The newer privately modified prototype is a different version and is not the source behind these screenshots.

## Repeat from a separate sample database

Install Git and Docker Desktop. From a fresh clone or checkout:

```powershell
git clone https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign.git
Set-Location Team3_CapstoneDesign
git checkout f4e8a6d3c185d3b9c9090d6daaf875080902cf1a
Set-Location smartserve-pos
docker compose -p smartserve-week6-independent up -d --build
```

Open http://localhost:5173. API docs: http://localhost:8000/docs. Wait for `/health` to return ok and for menu/stock data to load. Ports 5173, 8000, and 5432 must be free. Keep the Week 6 project name distinct from the shared store. If those ports are already used, stop or reconfigure the conflicting sample service after identifying it; do not delete a database volume to free a port.

Use [test-plan.md](test-plan.md) for the exact starting amounts and sequence. If the new project has been used before, its persisted data is no longer the stated fresh starting point. Record that fact and use a separate unused sample project rather than resetting someone else's data.

The October 14 automated check used native PostgreSQL 18.4, the checked-out FastAPI requirements, and a local production frontend build. A loopback test proxy mapped the frontend's fixed API address to the isolated API. No application source was changed for that address mapping. Docker's exact startup was not run during this check; the repository's standard instructions above should be verified by the independent teammate.

## Backend checks

From smartserve-pos:

```powershell
docker compose -p smartserve-week6-independent exec -T api python -m unittest -v test_issue3 test_owner_management test_trash
docker compose -p smartserve-week6-independent exec -T web npm run build
```

The 20 backend tests use separate in-memory SQLite data. They do not establish the human independent test or cover every UI/history case.

## Five-step midterm demo

1. Record Milk, Coffee beans, and the selected day's KST sales.
2. Create two lattes at ₩9,000. Confirm the order is open and stock unchanged.
3. Reload the tab, wait for the saved total, and pay cash.
4. Show the paid receipt, stock deduction once, and matching sales increase.
5. Repeat payment for the same ID through the API and show HTTP 409 with unchanged stock/sales.

After the main path, show the inventory conversion and historical-price check. Present the rename and alternate-unit edit problems as failures still being worked on, not as completed behavior.

The tester records their exact GitHub login, date, expected/actual values, screenshots, and first confusing step in [tested-by-note.md](tested-by-note.md).
