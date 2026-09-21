# Tech Stack Comparison

**Team:** Team 3

**Project:** SmartServe POS

**Week:** 3

Compare two buildable stacks for the SmartServe POS midterm path.

## Comparison table

| Criteria | Stack A: React + FastAPI + PostgreSQL | Stack B: Django full stack + PostgreSQL |
|---|---|---|
| **Frontend** | React, TypeScript, and Vite | Django templates, HTML, CSS, and JavaScript |
| **Backend** | FastAPI | Django |
| **Data** | PostgreSQL through SQLAlchemy | PostgreSQL through Django ORM |
| **Authentication** | Not included in the current MVP | Not included in the proposed midterm scope |
| **Team's current knowledge** | The team has an existing prototype using this stack; individual familiarity still needs confirmation. | Individual Django familiarity has not been recorded. |
| **Learning required** | Keep React state, API requests, and FastAPI responses aligned. | Rebuild the current frontend and migrate order, payment, and inventory logic. |
| **Development speed** | Continue and verify the existing prototype. | Slower initially because the prototype would need migration. |
| **Code organization** | Separate frontend and API projects with clear endpoints. | One Django project could combine pages and backend logic. |
| **Reusable components** | React supports reusable interface components. | Django templates support reusable page fragments. |
| **Project growth** | Can add features to the existing UI and API structure. | Can support growth, but would change the current structure. |
| **Midterm demo** | Order → simulated payment → receipt → inventory deduction → sales dashboard. | The same path would first need to be rebuilt. |
| **Main risk** | Frontend and API integration; correct database transaction behavior. | Migration effort could delay the midterm path. |
| **First feature** | Verify the existing cashier order and payment flow. | Build a cashier page and migrate the order and payment logic. |
| **Overall consideration** | Matches the implemented SmartServe MVP and its documented architecture. | Viable alternative if the team intentionally chooses a migration. |

## Stack A

- **Stack name:** React, TypeScript, Vite, FastAPI, PostgreSQL, and Docker Compose.
- **What can we build with this?** An interactive cashier view, simulated payment, receipt, inventory view, and owner sales dashboard backed by one database.
- **What does the team already know?** The repository contains a working code path using this stack. Each member should confirm which layer they can maintain.
- **What must we learn?** How to test the full workflow, handle API errors clearly, and verify transaction and duplicate-payment behavior.
- **How can we demo it by midterm?** Create a two-latte order, pay, show the receipt, check stock and daily sales, then repeat the payment request to confirm stock does not change twice.
- **What could go wrong?** Incorrect recipe data, insufficient stock, API connection errors, or untested repeated requests could undermine the demo.
- **Simplest first screen or feature:** The seeded menu and cashier order screen.

## Stack B

- **Stack name:** Django templates, Django backend, and PostgreSQL.
- **What can we build with this?** The same POS workflow using server-rendered cashier and manager pages.
- **What does the team already know?** Individual Django experience has not been recorded in the team documents.
- **What must we learn?** How to migrate the current FastAPI logic and React interactions into Django views, templates, and models.
- **How can we demo it by midterm?** Rebuild the order-to-sales path and test it before the midterm.
- **What could go wrong?** Migration could consume time needed for integration and verification.
- **Simplest first screen or feature:** A server-rendered cashier menu page.

## Decision

We choose:

> **Stack A: React, TypeScript, Vite, FastAPI, PostgreSQL, and Docker Compose.**

The current SmartServe prototype already uses this stack for the order, simulated payment, receipt, inventory, and dashboard path. Continuing it lets the team focus on correctness, shared setup, and demo evidence.

## Midterm scope

```text
Select two lattes
       ↓
Create order and calculate total from stored prices
       ↓
Complete simulated payment
       ↓
Show paid receipt
       ↓
Deduct recipe ingredients once
       ↓
Show sale on daily dashboard
```

Real payments, supplier management, customer accounts, and advanced reporting are outside this midterm path.

## Team review / instructor notes

- The selected stack matches the current [SmartServe MVP implementation](../../smartserve-pos/README.md) and [Architecture Sketch](architecture-sketch.md).
- Team member responses and any instructor feedback should be linked here after review.
- A repeatable demo result is still needed to verify the complete path.
