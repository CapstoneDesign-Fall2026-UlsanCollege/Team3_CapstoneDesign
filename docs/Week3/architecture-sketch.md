# Architecture Sketch

**Team:** Team 3

**Project:** SmartServe POS

**Last updated:** 2026-09-22

## One-sentence architecture

> **Frontend:** React, TypeScript, and Vite / **Backend:** FastAPI / **Data:** PostgreSQL through SQLAlchemy / **Local setup:** Docker Compose / **External services:** None in the current MVP

## Simple diagram

```text
Cashier or manager
       ↓
SmartServe POS website
       ↓
React frontend
  ├── Cashier order and receipt
  ├── Ingredient inventory
  └── Owner sales dashboard
       ↓ HTTP requests
FastAPI backend
  ├── Menu and order endpoints
  ├── Simulated payment and receipt data
  ├── Recipe-based inventory deduction
  └── Daily sales summary
       ↓
PostgreSQL
  ├── Menu items and recipes
  ├── Ingredients and stock
  ├── Orders and order items
  ├── Payments
  └── Inventory movements
```

## Main parts

| Part | What it does | Proposed owner | Risk / uncertainty |
|---|---|---|---|
| UI | Lets a cashier select items, review the total, simulate payment, and view a receipt; also shows inventory and sales screens. | Sherap Hyolmo, with Shuzita Majhi supporting screen design | The current screens have not yet been recorded in a shared demo or screenshot. |
| Data | Stores menu items, recipes, ingredients, orders, payments, and inventory movements in PostgreSQL. | Lama Muskan | Recipe quantities and stock must stay accurate. |
| Logic/API | Calculates totals from stored prices, creates orders, processes simulated payments, checks stock, deducts ingredients, and returns sales data. | Sherap Hyolmo and Lama Muskan | A failed or repeated payment must not leave partial records or deduct stock twice. |
| Setup/docs | Starts the frontend, API, and database with Docker Compose and records the design and demo path. | Sherap Hyolmo, with team documentation support | Startup and the full demo still need a recorded check on another team member's machine. |

Owner names follow the proposed roles in the Team 3 design and candidate slice. Confirm them with the team before submission.

## Evidence links

- [SmartServe POS MVP README](../../smartserve-pos/README.md)
- [Frontend implementation](../../smartserve-pos/frontend/src/main.tsx)
- [FastAPI implementation](../../smartserve-pos/backend/app/main.py)
- [Database models](../../smartserve-pos/backend/app/models.py)
- [Docker Compose setup](../../smartserve-pos/docker-compose.yml)
- [Week 2 design doc](../week-02/design-doc-v1.md)
- GitHub build issues and Week 3 demo evidence: links pending verification.

## Important decisions

| Decision | Why we chose it | Risk |
|---|---|---|
| React and TypeScript | Organize the cashier, inventory, and owner views in one web frontend. | State and API errors must be clear to users. |
| FastAPI | Provide endpoints for orders, simulated payments, inventory, and sales. | Frontend and backend behavior must stay aligned. |
| PostgreSQL | Store related sale and stock records and support transactions, row locks, and unique constraints. | Transaction handling must be checked with repeated and failed requests. |
| Simulated payment | Demonstrate a complete sale without a real payment provider. | Demo results must be clearly identified as simulated. |
| Deduct inventory after payment | Unpaid orders should not reduce stock. | A repeated request must never cause another deduction. |
| One complete midterm path | Show an order, payment, receipt, stock change, and dashboard result together. | Other management features may remain outside the midterm demo. |

## What could break?

- The frontend might create an order but fail to complete payment, leaving an open order.
- Incorrect recipe data could produce the wrong stock deduction.
- Insufficient stock should stop payment without changing the order or stock.
- A repeated payment request could cause a duplicate deduction if database protections fail.
- The dashboard's daily total could be wrong if its date does not match the intended local day.
- Docker or database startup could fail on another team member's machine.

## Recipe quantity to confirm before the demo

The seeded latte recipe uses **250 ml milk and 18 g coffee beans per latte**. Two lattes should therefore deduct **500 ml milk and 36 g beans**. The Week 2 design doc gives **400 ml milk** as an example; agree on one recipe quantity before recording the demo.
