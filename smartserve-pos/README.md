# SmartServe POS — Small MVP

Small café/restaurant POS capstone MVP built with React + TypeScript + Vite, FastAPI, PostgreSQL, and Docker Compose.

## What it does

1. Shows a small café menu.
2. Lets a cashier create a dine-in or takeaway order.
3. Completes a simulated cash, card, or QR payment.
4. Deducts recipe ingredients **once** after payment.
5. Shows basic ingredient inventory and low-stock status.
6. Shows an owner view of today's sales and recent paid orders.
7. Lists recent orders in an Orders view so staff can resume or cancel an unpaid order.
8. Lets the owner view add menu items with recipes and add ingredients, then remove them from active use while retaining order history.

The Orders view shows `open`, `paid`, and `cancelled` orders. Only an `open` order can be paid or cancelled. Cancelling an unpaid order does not change stock or sales. The owner dashboard counts only paid orders. Role-based access and the fuller draft/pending/completed order lifecycle are future work; the current views share one app.

Removal archives menu items and ingredients rather than deleting historical records. An ingredient used by an active menu item or open order cannot be removed. The Owner view is currently a demo UI; it does not yet enforce owner-only access.

## The key inventory rule

Payment runs as one PostgreSQL transaction. The API locks the order, locks the affected ingredients, creates the payment and inventory-movement records, updates stock, and finally marks the order as `paid`.

It also enforces two database constraints:

- One payment per order.
- One inventory movement per `order + ingredient`.

So a duplicate Pay click returns the already-paid receipt; it cannot deduct ingredients a second time.

## Run it

```bash
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- API health check: http://localhost:8000/health

The first start automatically seeds Caffè Latte, Americano, and Milk Tea, including their recipes and inventory.

## Not part of this MVP

Real payment gateways, supplier management, employee salary, multi-branch support, hardware integration, online ordering/delivery, mobile app, advanced accounting, and AI features.
