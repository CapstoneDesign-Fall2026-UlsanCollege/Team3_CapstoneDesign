"""Week 12 HTTP regression for the two-latte receipt and payment ledger."""

from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app import models, security, tenancy
from app.database import Base
from app.main import app
from app.seed import seed_demo_data


class Week12PaymentRetryTest(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory(prefix="smartserve-week12-"))
        owner = security.Principal(
            user_id="test-owner", email="owner@example.test", name="Test owner",
            role="owner", store_id="week12", namespace=f"store_{uuid4().hex}",
            purpose="full", csrf_token="week12-test-csrf", token_hash="test", mfa_at=None,
        )
        db_path = (Path(directory) / "pos.db").as_posix()
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.addCleanup(self.engine.dispose)
        Base.metadata.create_all(self.engine)
        with Session(self.engine) as db:
            seed_demo_data(db)

        # Substitute session lookup and the physical workspace database for this fixture.
        self.enterContext(patch.object(security, "resolve_session", return_value=owner))
        self.workspace_engine = self.enterContext(
            patch.object(tenancy, "tenant_engine", return_value=self.engine)
        )
        self.workspace_namespace = owner.namespace
        self.client = TestClient(app, headers={"X-CSRF-Token": owner.csrf_token})
        self.addCleanup(self.client.close)

    def get_json(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def ledger(self):
        with Session(self.engine) as db:
            payments = db.execute(select(
                models.Payment.id, models.Payment.order_id, models.Payment.method,
                models.Payment.amount, models.Payment.simulated_reference,
                models.Payment.created_at,
            ).order_by(models.Payment.id)).all()
            movements = db.execute(select(
                models.InventoryMovement.id, models.InventoryMovement.order_id,
                models.Ingredient.name, models.InventoryMovement.quantity_change,
                models.InventoryMovement.reason, models.InventoryMovement.created_at,
            ).join(models.Ingredient).order_by(models.InventoryMovement.id)).all()
        return payments, movements

    def test_two_latte_http_retry_preserves_receipt_and_ledger(self):
        latte = next(item for item in self.get_json("/menu") if item["name"] == "Caffè Latte")
        inventory_before = self.get_json("/inventory")
        created = self.client.post("/orders", json={
            "order_type": "takeaway", "items": [{"menu_item_id": latte["id"], "quantity": 2}],
        })
        self.assertEqual(created.status_code, 201, created.text)
        order = created.json()
        order_path = f"/orders/{order['id']}"
        self.assertEqual((order["status"], order["total"]), ("open", 9000))
        self.assertEqual(order["items"], [{
            "menu_item_id": latte["id"], "name": latte["name"], "quantity": 2, "unit_price": 4500,
        }])
        self.assertEqual(self.get_json("/inventory"), inventory_before)
        self.assertEqual(self.ledger(), ([], []))

        payment = self.client.post(f"{order_path}/pay", json={"method": "cash"})
        self.assertEqual(payment.status_code, 200, payment.text)
        receipt = self.get_json(order_path)
        self.assertEqual(receipt, payment.json()["order"])
        self.assertEqual(receipt["id"], order["id"])
        self.assertEqual(receipt["items"], order["items"])
        self.assertEqual(
            (receipt["status"], receipt["total"], receipt["payment_method"]), ("paid", 9000, "cash")
        )
        self.assertTrue(receipt["inventory_deducted"])
        self.assertTrue(receipt["paid_at"])
        reference = receipt["simulated_reference"]
        self.assertTrue(reference and reference.startswith("SIM-"))

        inventory_paid = self.get_json("/inventory")
        before = {item["name"]: item for item in inventory_before}
        after = {item["name"]: item for item in inventory_paid}
        self.assertEqual(after.keys(), before.keys())
        deductions = {"Milk": ("ml", 500), "Coffee beans": ("g", 36)}
        for name, original in before.items():
            unit, delta = deductions.get(name, (original["unit"], 0))
            self.assertEqual((original["unit"], after[name]["unit"]), (unit, unit))
            self.assertEqual(original["stock_quantity"] - after[name]["stock_quantity"], delta, name)

        payments, movements = self.ledger()
        self.assertEqual(
            [(row.order_id, row.method, row.amount, row.simulated_reference) for row in payments],
            [(order["id"], "cash", Decimal("9000"), reference)],
        )
        self.assertCountEqual(
            [(row.order_id, row.name, row.quantity_change, row.reason) for row in movements],
            [(order["id"], name, Decimal(-delta), "paid_order") for name, (_, delta) in deductions.items()],
        )

        retry = self.client.post(f"{order_path}/pay", json={"method": "card"})
        self.assertEqual(retry.status_code, 409, retry.text)
        self.assertIn("already been processed", retry.json()["detail"])
        self.assertEqual(self.get_json(order_path), receipt)
        self.assertEqual(self.get_json("/inventory"), inventory_paid)
        self.assertEqual(self.ledger(), (payments, movements))
        self.workspace_engine.assert_called_with(self.workspace_namespace)

        print(
            f"\nOrder {order['id']}: create HTTP {created.status_code}; {order['items'][0]['quantity']} lattes, "
            f"KRW {receipt['total']:.0f}; cash HTTP {payment.status_code}; reference {reference}"
        )
        for name in deductions:
            print(f"{name}: {before[name]['stock_quantity']:g} -> {after[name]['stock_quantity']:g} {after[name]['unit']}")
        print(f"Payment row {payments[0].id}: {payments[0].method}, KRW {payments[0].amount:.0f}")
        for movement in movements:
            print(f"Movement row {movement.id}: {movement.name} {movement.quantity_change:+g} ({movement.reason})")
        print(
            f"Card retry HTTP {retry.status_code}; receipt and stock unchanged; "
            f"{len(payments)} payment and {len(movements)} movements unchanged"
        )
