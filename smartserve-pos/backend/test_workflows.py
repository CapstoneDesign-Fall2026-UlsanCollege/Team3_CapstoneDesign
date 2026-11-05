import os
os.environ.setdefault("DATABASE_URL", "sqlite://")

import unittest
from datetime import datetime, timezone
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app import models
from app.database import Base
from app.business import SetupInput, complete_setup, get_profile
from app.workflows import TicketInput, StatusInput, create_ticket, change_status, list_tables
from app.main import add_order_items, cancel_order, create_order, get_order, list_menu, permanently_delete_cancelled, restore_menu_item, simulate_payment
from app.schemas import AddOrderItems, OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)
        seed_demo_data(self.db)
        self.db.add(models.BusinessProfile(id=1, name="Store", business_type="cafe"))
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def setup_store(self, kind="cafe", mode="both", **kwargs):
        return complete_setup(SetupInput(name="Test business", business_type=kind, operation_mode=mode, **kwargs), self.db)

    def order(self, **kwargs):
        return create_order(OrderCreate(items=[{"menu_item_id": 1, "quantity": 1}], **kwargs), self.db)

    def test_table_bill_occupancy_append_and_release_after_payment(self):
        self.setup_store(table_count=4)
        order = self.order(order_type="dine_in", table_number=2)
        self.assertEqual(list_tables(self.db)[1]["order_id"], order["id"])
        with self.assertRaises(HTTPException) as conflict:
            self.order(order_type="dine_in", table_number=2)
        self.assertEqual(conflict.exception.status_code, 409)
        appended = add_order_items(order["id"], AddOrderItems(items=[{"menu_item_id": 1, "quantity": 2}]), self.db)
        self.assertEqual(appended["total"], order["total"] * 3)
        simulate_payment(order["id"], PaymentCreate(method="cash"), self.db)
        self.assertIsNone(list_tables(self.db)[1]["order_id"])
        self.assertEqual(get_order(order["id"], self.db)["table_number"], 2)
        with self.assertRaises(HTTPException):
            add_order_items(order["id"], AddOrderItems(items=[{"menu_item_id": 1, "quantity": 1}]), self.db)

    def test_takeaway_only_rejects_table_sales_and_tables_only_requires_table(self):
        self.setup_store(mode="takeaway")
        self.assertEqual(get_profile(self.db)["order_types"], ["takeaway"])
        self.assertEqual(list_tables(self.db), [])
        with self.assertRaises(HTTPException):
            self.order(order_type="dine_in", table_number=1)
        self.setup_store(mode="tables")
        with self.assertRaises(HTTPException):
            self.order(order_type="takeaway")
        with self.assertRaises(HTTPException):
            self.order(order_type="dine_in")

    def test_appointment_overlap_and_distinct_staff(self):
        self.setup_store("barbershop", "both")
        args = dict(kind="appointment", title="Cut", customer="Alex", resource="Sam", starts_at=datetime(2027, 1, 3, 10, tzinfo=timezone.utc), duration_minutes=30)
        first = create_ticket(TicketInput(**args), self.db)
        with self.assertRaises(HTTPException) as clash:
            create_ticket(TicketInput(**{**args, "resource": "sam"}), self.db)
        self.assertEqual(clash.exception.status_code, 409)
        create_ticket(TicketInput(**{**args, "resource": "Pat"}), self.db)
        create_ticket(TicketInput(**{**args, "starts_at": datetime(2027, 1, 3, 10, 30, tzinfo=timezone.utc)}), self.db)
        change_status(first["id"], StatusInput(status="cancelled"), self.db)
        create_ticket(TicketInput(**args), self.db)

    def test_job_bill_status_checkout_and_cancelled_bill_retry(self):
        self.setup_store("repair", "jobs", catalog_action="samples")
        job = create_ticket(TicketInput(kind="job", title="Repair phone", customer="Alex", notes="Cracked screen"), self.db)
        change_status(job["id"], StatusInput(status="in_progress"), self.db)
        change_status(job["id"], StatusInput(status="ready"), self.db)
        item = list_menu(self.db)[0]
        payload = OrderCreate(order_type="service", ticket_id=job["id"], items=[{"menu_item_id": item.id, "quantity": 1}])
        first = create_order(payload, self.db)
        with self.assertRaises(HTTPException):
            create_order(payload, self.db)
        with self.assertRaises(HTTPException):
            change_status(job["id"], StatusInput(status="cancelled"), self.db)
        cancel_order(first["id"], self.db)
        second = create_order(payload, self.db)
        simulate_payment(second["id"], PaymentCreate(method="cash"), self.db)
        self.assertEqual(self.db.get(models.WorkTicket, job["id"]).status, "completed")

    def test_setup_keeps_history_and_reactivates_samples_without_restock(self):
        order = self.order(order_type="takeaway")
        simulate_payment(order["id"], PaymentCreate(method="cash"), self.db)
        self.setup_store("retail", "both", catalog_action="samples")
        self.assertEqual(len(list_menu(self.db)), 3)
        restore_menu_item(1, self.db)
        self.assertEqual(len(list_menu(self.db)), 4)
        self.assertEqual(get_order(order["id"], self.db)["items"][0]["name"], "Caffè Latte")
        self.setup_store("custom", "custom", catalog_action="empty", features=["checkout", "appointments", "jobs"])
        self.assertEqual(list_menu(self.db), [])
        self.assertEqual(get_profile(self.db)["features"], ["checkout", "appointments", "jobs"])
        self.setup_store("retail", "both", catalog_action="samples")
        self.assertEqual(len(list_menu(self.db)), 3)

    def test_setup_cannot_orphan_open_bills_or_active_work(self):
        order = self.order(order_type="takeaway")
        with self.assertRaises(HTTPException):
            self.setup_store("retail", "both", catalog_action="empty")
        self.assertEqual(len(list_menu(self.db)), 3)
        cancel_order(order["id"], self.db)
        self.setup_store("barbershop", "walk_ins")
        create_ticket(TicketInput(kind="walk_in", title="Cut", customer="A"), self.db)
        with self.assertRaises(HTTPException):
            self.setup_store("retail", "both")

    def test_configuration_validation_and_disabled_workflow(self):
        for args in [dict(name=" ", business_type="cafe", operation_mode="both"), dict(name="A", business_type="retail", operation_mode="tables"), dict(name="A", business_type="retail", operation_mode="both", logo_url="javascript:alert(1)")]:
            with self.assertRaises(ValidationError):
                SetupInput(**args)
        self.setup_store(mode="takeaway")
        with self.assertRaises(HTTPException):
            create_ticket(TicketInput(kind="job", title="Repair", customer="A"), self.db)
        with self.assertRaises(ValidationError):
            TicketInput(kind="appointment", title="Cut", customer="A")

    def test_cancelled_table_order_can_be_deleted_without_orphaned_context(self):
        self.setup_store()
        order = self.order(order_type="dine_in", table_number=1)
        cancel_order(order["id"], self.db)
        permanently_delete_cancelled(self.db.get(models.Order, order["id"]), self.db)
        self.db.commit()
        self.assertIsNone(self.db.get(models.OrderContext, order["id"]))
        with self.assertRaises(HTTPException):
            get_order(order["id"], self.db)


if __name__ == "__main__":
    unittest.main()
