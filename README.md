# SmartServe POS

A café point-of-sale project built with React, TypeScript, FastAPI, and PostgreSQL.

## Start the project

Install Git and Docker Desktop, enable Linux containers, and start Docker Desktop. Then:

```bash
git clone https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign.git
cd Team3_CapstoneDesign/smartserve-pos
docker compose -p smartserve-week5-check up -d --build
```

Open **http://localhost:5173**. API documentation: http://localhost:8000/docs. Ports 5173, 8000, and 5432 must be free. Wait for first-start dependency installation and for http://localhost:8000/health to return `{"status":"ok"}`.

## Features

- Save unpaid dine-in/takeaway orders and recover them after refresh.
- Complete simulated cash/card/QR payments and view receipts.
- Deduct recipe ingredients once and inspect stock/low-stock indicators.
- Browse collapsible order-month folders with status/date filters and Korea-time timestamps.
- Move cancelled orders to Trash, restore them, or delete them permanently. Trash expires after 30 days.
- View sales for a selected Korea-time date with matching totals and rows.
- Add ingredients using a unit dropdown and create menu-item recipes.
- Remove items from active lists while preserving historical records.
- Switch White, Dark, and Code themes using the bottom-left palette button.

Payments are simulated. All users share the database; test purchases change stock and sales. Owner-only access is not enforced yet.

## Guides

- [Complete setup, usage, tests, and troubleshooting](smartserve-pos/README.md)
- [Free public-link setup](docs/online/README.md)
- [Current verification](docs/online/latest-checks.md)
- [Week 5 shared report](docs/week-05/weekly-report.md)

The public sharing option uses this PC as the server and requires it to remain running. It is not permanent cloud hosting.
