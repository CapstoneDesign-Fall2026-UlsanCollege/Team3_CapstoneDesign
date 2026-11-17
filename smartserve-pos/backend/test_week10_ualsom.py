
"""Week 10 QA test by ualsom (Ualson Tamang).

Run: python -m unittest -v test_week10_ualsom
Uses an isolated SQLite test database.
"""

import os
os.environ["DATABASE_URL"] = "sqlite://"

import unittest
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.database import Base, engine
from app import models
from app.main import create_order, simulate_payment
from app.schemas import OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class Week10UalsomTests(unittest.TestCase):

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
            item.name: Decimal(str(item.stock_quantity))
            for item in self.db.scalars(select(models.Ingredient))
        }

    def test_two_lattes_duplicate_payment_same_session(self):
        # Find the latte menu item.
        latte = self.db.scalar(
            select(models.MenuItem).where(
                models.MenuItem.name.contains("Latte")
            )
        )
        self.assertIsNotNone(latte)

        # Record stock before ordering.
        before = self.stock()

        # Create an order containing two lattes.
        order = create_order(
            OrderCreate(
                order_type="dine_in",
                items=[{
                    "menu_item_id": latte.id,
                    "quantity": 2
                }]
            ),
            self.db
        )

        # First payment should succeed.
        result = simulate_payment(
            order["id"],
            PaymentCreate(method="cash"),
            self.db
        )

        after_payment = self.stock()

        self.assertEqual(result["order"]["status"], "paid")
        self.assertTrue(result["order"]["inventory_deducted"])

        self.assertEqual(
            before["Milk"] - after_payment["Milk"],
            Decimal("500")
        )
        self.assertEqual(
            before["Coffee beans"] - after_payment["Coffee beans"],
            Decimal("36")
        )

        # Try a second payment in the same session.
        with self.assertRaises(HTTPException) as error:
            simulate_payment(
                order["id"],
                PaymentCreate(method="card"),
                self.db
            )

        self.assertEqual(error.exception.status_code, 409)
        self.db.rollback()

        # Inventory must remain unchanged.
        self.assertEqual(self.stock(), after_payment)

        # Exactly one payment and two inventory movements.
        payment_count = self.db.scalar(
            select(func.count()).select_from(models.Payment)
        )
        movement_count = self.db.scalar(
            select(func.count()).select_from(
                models.InventoryMovement
            )
        )

        self.assertEqual(payment_count, 1)
        self.assertEqual(movement_count, 2)


if __name__ == "__main__":
    unittest.main()
