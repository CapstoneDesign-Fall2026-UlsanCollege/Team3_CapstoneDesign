"""Store-floor tables, appointments, walk-ins and repair jobs."""
from datetime import timedelta, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import AwareDatetime, BaseModel, Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models
from .business import get_profile
from .database import get_db

router = APIRouter()
FEATURE = {"appointment": "appointments", "walk_in": "walk_ins", "job": "jobs"}


class TicketInput(BaseModel):
    kind: Literal["appointment", "walk_in", "job"]
    title: str = Field(min_length=1, max_length=120)
    customer: str = Field(min_length=1, max_length=120)
    resource: str = Field(default="Any staff", min_length=1, max_length=80)
    starts_at: AwareDatetime | None = None
    duration_minutes: int = Field(default=30, ge=5, le=480)
    notes: str = Field(default="", max_length=1000)

    @model_validator(mode="after")
    def valid_ticket(self):
        if not self.title.strip() or not self.customer.strip() or not self.resource.strip():
            raise ValueError("Service, customer and staff/resource are required")
        if self.kind == "appointment" and self.starts_at is None:
            raise ValueError("An appointment needs a start time with timezone")
        return self


class StatusInput(BaseModel):
    status: Literal["in_progress", "ready", "completed", "cancelled"]


def ticket_view(ticket, db):
    context = db.scalar(select(models.OrderContext).where(models.OrderContext.ticket_id == ticket.id))
    order = db.get(models.Order, context.order_id) if context else None
    def iso(value):
        return value.replace(tzinfo=timezone.utc).isoformat() if value and value.tzinfo is None else value.isoformat() if value else None
    return {"id": ticket.id, "kind": ticket.kind, "title": ticket.title, "customer": ticket.customer,
            "resource": ticket.resource, "starts_at": iso(ticket.starts_at), "ends_at": iso(ticket.ends_at),
            "notes": ticket.notes, "status": ticket.status, "created_at": iso(ticket.created_at),
            "order_id": order.id if order else None, "order_status": order.status if order else None}


@router.get("/owner/work")
def list_work(db: Session = Depends(get_db)):
    tickets = db.scalars(select(models.WorkTicket).order_by(models.WorkTicket.created_at.desc(), models.WorkTicket.id.desc())).all()
    return [ticket_view(ticket, db) for ticket in tickets]


@router.post("/owner/work", status_code=201)
def create_ticket(payload: TicketInput, db: Session = Depends(get_db)):
    # Serializes scheduling decisions for this store on PostgreSQL.
    db.scalar(select(models.BusinessProfile).where(models.BusinessProfile.id == 1).with_for_update())
    if FEATURE[payload.kind] not in get_profile(db)["features"]:
        raise HTTPException(409, "Enable this workflow in the business profile first")
    start = payload.starts_at.astimezone(timezone.utc) if payload.starts_at else None
    end = start + timedelta(minutes=payload.duration_minutes) if start else None
    resource = payload.resource.strip()
    if payload.kind == "appointment":
        conflict = db.scalar(select(models.WorkTicket.id).where(
            models.WorkTicket.kind == "appointment", models.WorkTicket.status != "cancelled",
            func.lower(models.WorkTicket.resource) == resource.lower(),
            models.WorkTicket.starts_at < end, models.WorkTicket.ends_at > start).limit(1))
        if conflict:
            raise HTTPException(409, "This staff member already has an appointment in that time. Choose another time or staff member.")
    ticket = models.WorkTicket(kind=payload.kind, title=payload.title.strip(), customer=payload.customer.strip(),
                               resource=resource, starts_at=start, ends_at=end, notes=payload.notes.strip(), status="booked")
    db.add(ticket)
    db.commit()
    return ticket_view(ticket, db)


@router.put("/owner/work/{ticket_id}/status")
def change_status(ticket_id: int, payload: StatusInput, db: Session = Depends(get_db)):
    ticket = db.scalar(select(models.WorkTicket).where(models.WorkTicket.id == ticket_id).with_for_update())
    if ticket is None:
        raise HTTPException(404, "Work item not found")
    allowed = {"booked": {"in_progress", "cancelled"}, "in_progress": {"ready", "completed", "cancelled"},
               "ready": {"completed", "cancelled"}, "completed": set(), "cancelled": set()}
    if payload.status not in allowed[ticket.status]:
        raise HTTPException(409, "That status change is not available")
    context = db.scalar(select(models.OrderContext).where(models.OrderContext.ticket_id == ticket.id))
    if context and db.get(models.Order, context.order_id).status == "open" and payload.status in ("completed", "cancelled"):
        raise HTTPException(409, "Pay or cancel the linked open bill first")
    ticket.status = payload.status
    db.commit()
    return ticket_view(ticket, db)


@router.get("/tables")
def list_tables(db: Session = Depends(get_db)):
    profile = get_profile(db)
    if "tables" not in profile["features"]:
        return []
    contexts = db.scalars(select(models.OrderContext).join(models.Order).where(models.Order.status == "open", models.OrderContext.table_number.is_not(None))).all()
    orders = {context.table_number: db.get(models.Order, context.order_id) for context in contexts}
    return [{"number": number, "order_id": orders[number].id if number in orders else None,
             "total": float(orders[number].total) if number in orders else 0}
            for number in range(1, profile["table_count"] + 1)]
