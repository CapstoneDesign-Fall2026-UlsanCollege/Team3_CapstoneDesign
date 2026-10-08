# SmartServe POS

Café POS built with React/TypeScript/Vite, FastAPI/SQLAlchemy, PostgreSQL, and Docker Compose.

## Requirements and startup

Start Docker Desktop with Linux containers. Keep ports 5173, 8000, and 5432 free. From this directory:

```bash
docker compose -p smartserve-week5-check up -d --build
docker compose -p smartserve-week5-check ps
```

Open http://localhost:5173. API docs: http://localhost:8000/docs. Health: http://localhost:8000/health. Wait for frontend dependency installation on the first start.

No host Python or Node.js is required for ordinary Docker use. Host Node.js 22+ is needed only for local builds, browser checks, and the public-link helper. Database credentials in Compose are for local development.

A new empty database seeds Caffè Latte (₩4,500), Americano (₩3,500), Milk Tea (₩5,000), and recipes/inventory. Existing data is retained. Removed seed items are not automatically recreated.

## Cashier

1. Select items and adjust quantities using +/−.
2. Choose Dine in or Takeaway.
3. Click **Create order** to save before payment, or use a Pay button for direct checkout.
4. An unpaid order is **Open**; stock and sales remain unchanged.
5. Complete simulated cash/card/QR payment to display a receipt and deduct recipe ingredients once.
6. Refresh the same browser tab to recover its saved unpaid order. Other open orders can be resumed from Orders.

Each submitted order line supports up to 20 units. Creation failure preserves the cart for retry.

## Orders and Trash

Orders are grouped by creation month in Korea time. The newest matching month starts expanded; click a heading to fold/unfold it. Filter by status/date or refresh to see other users' changes.

- **Open:** Resume payment or Cancel. Cancellation changes neither stock nor sales.
- **Cancelled:** Move to Trash to remove it from Orders.
- **Trash:** Restore or Delete forever. Restore returns an order as cancelled, not open.
- Retention is **30 days** from the first move. The automatic deletion deadline is displayed.
- Cleanup checks every minute while the API runs and on startup after downtime.
- Paid orders and orders with payment/inventory history cannot be permanently deleted through this feature.

## Inventory and owner management

Inventory shows active ingredients, quantities, thresholds, and low-stock indicators.

In Owner dashboard → Manage menu & inventory:

1. Add an ingredient with g, kg, ml, l, or pcs as its unit.
2. Enter starting stock and low-stock threshold in that unit.
3. Add a menu item, price in KRW, and recipe amounts for one serving.
4. Recipe quantities must use each ingredient's stored unit; units are not automatically converted.

Removed items disappear from active lists while historical records remain. Ingredients used by active menu items or open orders cannot be removed until dependencies are settled. Archived names remain reserved. Owner-only access is not enforced yet.

## Sales and appearance

Choose a Sales date: totals and paid-order rows use the same Korea-time day. All users share the database, so test purchases and teammate purchases contribute to sales. The app does not identify individual cashiers. Refresh sales to fetch changes.

The bottom-left palette button switches White, Dark, and Code themes. The current browser remembers the choice; Escape closes the selector.

## Payment correctness

A PostgreSQL transaction locks the order and ingredients, records payment/stock movements, updates stock, and marks the order paid atomically. Database constraints enforce one payment per order and one movement per order/ingredient.

Duplicate payment requests return HTTP 409 without another deduction. The UI can recover the already-paid receipt. Failed simulated payments and insufficient stock leave the order unpaid and stock unchanged. Creation-time unit prices preserve historical totals.

## Tests and build

From this directory:

```bash
docker compose -p smartserve-week5-check exec -T api python -m unittest -v test_issue3 test_owner_management test_trash
docker compose -p smartserve-week5-check exec -T web npm run build
```

Backend tests use isolated in-memory SQLite and do not reset running PostgreSQL data. Browser checks create/pay sample orders; run them against dedicated sample data. [Latest verification](../docs/online/latest-checks.md).

## Stop, restart, update

```bash
# Stop without deleting data.
docker compose -p smartserve-week5-check stop

# Restart.
docker compose -p smartserve-week5-check up -d

# Update from main and rebuild.
git pull --ff-only origin main
docker compose -p smartserve-week5-check up -d --build
```

Keep the same project name to retain the same named database volume. Do not remove volumes unless you intend to erase data.

## Troubleshooting

- Docker connection error: start Docker Desktop and wait for its Linux engine.
- Startup failure: inspect `docker compose -p smartserve-week5-check logs --tail 50 api web`.
- Port already allocated: stop the conflicting service/project.
- Old UI: refresh. Public access also needs the production frontend rebuilt.
- Ingredient removal rejected: remove dependent active menu items and settle open orders.
- Unexpected sales: inspect the selected date's paid rows; test purchases are included.

## Public link and limits

[Public-link instructions](../docs/online/README.md) cover prerequisites, startup, stopping, and temporary URL behaviour. The actual app and PostgreSQL database run on this PC, which must remain awake and connected.

Payments and stock are sample/simulated data. Real gateways, enforced user roles, physical stock measurement, supplier workflows, multi-branch support, and production hosting are not included.

### Editing existing items

In Owner dashboard, select Edit beside a menu item or ingredient. Change the prefilled values and select Save, or Cancel editing to discard the draft. Menu fields include name, price and recipe; ingredient fields include name, current stock, threshold and unit. Stock changes set the current balance directly. Saved orders keep their original unit prices. Pay or cancel open orders before changing a recipe. Units already used in recipes or stock history cannot be changed; create a new ingredient for a different unit.

The Add menu item and Add ingredient sections start collapsed. Click their headers to expand or collapse each form. Existing lists stay visible. Edit opens the relevant form; successful saving or cancelling editing closes it. Folding a form retains its draft until saved or cancelled.

When an ingredient has recipe or stock history, the Unit selector is disabled with an explanation before saving. Owner notices can be dismissed, and cancelling editing clears the previous notice.

Adding a removed ingredient name brings the existing ingredient back using the entered stock and threshold. Its ID and history are retained. A different unit is allowed only when it has no recipe or stock history. Active duplicate names remain blocked; use Edit instead.
