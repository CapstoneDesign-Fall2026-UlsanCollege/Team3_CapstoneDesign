
# SmartServe POS — Architecture and Setup

**Project:** SmartServe POS
**Team:** Team 3
**Course:** Capstone Design — Fall 2026
**Updated:** Week 5

## Overview

SmartServe is a POS system for managing orders, payments, and inventory.

**MVP flow:**

Order → Payment → Inventory Deduction → Receipt

## Technology Stack

* **Frontend:** React + TypeScript + Vite
* **Backend:** Python + FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Development:** Docker

## Architecture

```text
React Frontend
      │
      │ HTTP requests
      ▼
FastAPI Backend
      │
      │ SQLAlchemy
      ▼
PostgreSQL
```

## Main Flow

1. Cashier selects menu items and quantities.
2. System calculates the order total.
3. Order is created with a unique ID.
4. Simulated payment is processed.
5. Successful payment changes the order to `paid`.
6. Required ingredients are deducted once.
7. Payment and inventory records are saved.

## Project Structure

```text
smartserve-pos/
├── backend/
│   └── app/
├── frontend/
├── docs/
└── docker-compose.yml
```

## Backend Setup

```bash
cd backend
py -3.13 -m pip install fastapi uvicorn sqlalchemy psycopg[binary]
py -3.13 -m uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

## Key API Areas

* Orders
* Simulated payments
* Inventory
* Dashboard/sales
* Receipts

## Payment & Inventory Rule

A successful payment deducts the recipe ingredients exactly once.

A repeated payment request for the same paid order returns **HTTP 409** and must not create another payment or inventory movement.

## Testing

The Sprint 0/Week 4 verification covers:

* Successful payment
* Failed payment
* Insufficient stock
* Duplicate payment
* Inventory deduction
* Unique order IDs
* Original order price preservation

## Week 5 Focus

The current focus is continuing implementation from the existing SmartServe MVP and preparing a small, demonstrable vertical slice for the next checkpoint.
