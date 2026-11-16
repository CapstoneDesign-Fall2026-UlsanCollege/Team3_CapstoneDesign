"""Week 11 bounded demo regression: two lattes, payment, then retry in a new DB session.

Run from smartserve-pos/backend:
    python -B -m unittest -v test_week11_ualsom

Uses isolated SQLite and simulated payments; does not contact a live payment provider.
"""
import os
os.environ["DATABASE_URL"] = "sqlite://"

import unittest
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine
from app.main import create_order, simulate_payment
from app.schemas import OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class UalsomWeek11PaymentRetryTest(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.db = Session(engine)
        seed_demo_data(self.db)

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(engine)

    def stock(self):
        self.db.expire_all()
        return {
            ingredient.name: Decimal(str(ingredient.stock_quantity))
            for ingredient in self.db.scalars(select(models.Ingredient))
        }

    def count(self, model):
        return self.db.scalar(select(func.count()).select_from(model))

    def test_two_lattes_retry_from_new_session_does_not_deduct_twice(self):
        latte = self.db.scalar(
            select(models.MenuItem).where(models.MenuItem.name == "Caffè Latte")
        )
        self.assertIsNotNone(latte)

        before = self.stock()
        order = create_order(
            OrderCreate(
                order_type="dine_in",
                items=[{"menu_item_id": latte.id, "quantity": 2}],
            ),
            self.db,
        )

        # Creating an order alone must not consume stock.
        self.assertEqual(order["total"], 9000)
        self.assertEqual(self.stock(), before)

        paid = simulate_payment(
            order["id"], PaymentCreate(method="cash"), self.db
        )["order"]
        self.assertEqual(paid["status"], "paid")
        self.assertTrue(paid["inventory_deducted"])

        after = self.stock()
        self.assertEqual(before["Milk"] - after["Milk"], Decimal("500"))
        self.assertEqual(
            before["Coffee beans"] - after["Coffee beans"], Decimal("36")
        )
        self.assertEqual(self.count(models.Payment), 1)
        self.assertEqual(self.count(models.InventoryMovement), 2)

        # A retry from a fresh session must be rejected and leave stock intact.
        self.db.close()
        self.db = Session(engine)
        with self.assertRaises(HTTPException) as raised:
            simulate_payment(
                order["id"], PaymentCreate(method="card"), self.db
            )
        self.assertEqual(raised.exception.status_code, 409)
        self.db.rollback()

        self.assertEqual(self.stock(), after)
        self.assertEqual(self.count(models.Payment), 1)
        self.assertEqual(self.count(models.InventoryMovement), 2)


if __name__ == "__main__":
    unittest.main()
