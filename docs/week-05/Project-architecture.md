# SmartServe POS — Week 5 Architecture & Setup

**Team:** Team 3
**Sprint:** Sprint 1
**Week:** 5
**Course:** Capstone Design — Fall 2026

## Technology Stack

* **Frontend:** React + TypeScript + Vite
* **Backend:** Python + FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Development:** Docker

## Architecture

```text
React + TypeScript + Vite
          │
          │ HTTP requests
          ▼
     FastAPI Backend
          │
          │ SQLAlchemy
          ▼
       PostgreSQL
```

## Selected Vertical Slice

Cashier selects menu items and quantities
→ System calculates the total
→ Order is created
→ Simulated payment is completed
→ Inventory is deducted
→ Order/receipt result is shown

## Must Work

* Create an order
* Calculate the correct total
* Process simulated payment
* Change the order to `paid`
* Deduct inventory exactly once
* Show the resulting order/receipt

## Fallback

If the complete flow is not ready for the checkpoint, demonstrate the smaller payment → inventory deduction flow using seeded sample data.

## Week 5 Implementation

* Project setup and local backend run verified
* Payment and inventory flow tested
* Implementation work divided into small Issues
* Existing architecture and design documents connected to the slice
* Evidence prepared in GitHub

## Evidence

* Vertical Slice Plan
* Architecture and wireframe documents
* Implementation Issues
* Commit/PR
* Payment and inventory test evidence
* Week 5 Weekly Report

## Planned Checkpoint Proof

The team will demonstrate the selected SmartServe flow from order creation through simulated payment and inventory deduction, using seeded sample data.

The demonstration will show:

* The created order and calculated total
* Successful simulated payment
* Order status changing to `paid`
* Inventory being deducted exactly once
* The resulting order/receipt
