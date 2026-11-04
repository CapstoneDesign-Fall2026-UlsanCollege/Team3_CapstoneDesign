"""Business presets must never overwrite a store's existing stock or history."""
import os
os.environ.setdefault("DATABASE_URL", "sqlite://")

import unittest
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app import models
from app.business import ProfileInput, apply_preset, get_profile, update_business
from app.database import Base
from app.main import add_menu_item, create_order, get_order, owner_menu, simulate_payment, update_menu_item
from app.schemas import MenuItemCreate, OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class BusinessTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)
        seed_demo_data(self.db)
        self.db.add(models.BusinessProfile(id=1, name="Original store", business_type="cafe"))
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_preset_is_repeatable_without_restocking_or_overwriting(self):
        initial = self.db.scalar(select(models.Ingredient).where(models.Ingredient.name == "Milk"))
        original_stock = initial.stock_quantity
        first = apply_preset("retail", self.db)
        self.assertEqual(len(first["added"]), 3)
        item = next(item for item in owner_menu(self.db) if item["name"] == "Cotton T-shirt")
        order = create_order(OrderCreate(order_type="in_store", items=[{"menu_item_id": item["id"], "quantity": 2}]), self.db)
        simulate_payment(order["id"], PaymentCreate(method="cash"), self.db)
        stock = self.db.get(models.Ingredient, item["recipe"][0]["ingredient_id"])
        self.assertEqual(stock.stock_quantity, Decimal(38))
        second = apply_preset("retail", self.db)
        self.assertEqual(second["added"], [])
        self.assertEqual(len(second["skipped"]), 3)
        self.assertEqual(stock.stock_quantity, Decimal(38))
        self.assertEqual(initial.stock_quantity, original_stock)
        self.assertEqual(get_order(order["id"], self.db)["total"], 38000)
        self.assertEqual(get_profile(self.db)["name"], "Original store")

    def test_service_payment_has_no_inventory_movement_and_duplicate_is_rejected(self):
        item = add_menu_item(MenuItemCreate(name="Consultation", price=30000, item_type="service", category="Consulting"), self.db)
        self.assertEqual(item["recipe"], [])
        order = create_order(OrderCreate(order_type="service", items=[{"menu_item_id": item["id"], "quantity": 1}]), self.db)
        simulate_payment(order["id"], PaymentCreate(method="card"), self.db)
        self.assertEqual(self.db.scalars(select(models.InventoryMovement)).all(), [])
        with self.assertRaises(HTTPException) as error:
            simulate_payment(order["id"], PaymentCreate(method="card"), self.db)
        self.assertEqual(error.exception.status_code, 409)
        edited = update_menu_item(item["id"], MenuItemCreate(name="Expert consultation", price=45000, item_type="service", category="Consulting"), self.db)
        self.assertEqual(edited["item_type"], "service")
        self.assertEqual(get_order(order["id"], self.db)["items"][0]["name"], "Consultation")

    def test_all_presets_coexist_and_unknown_preset_has_no_effect(self):
        for key in ("cafe", "restaurant", "retail", "grocery", "beauty", "services"):
            self.assertEqual(len(apply_preset(key, self.db)["added"]), 3)
        self.assertEqual(len(self.db.scalars(select(models.MenuItem)).all()), 21)
        with self.assertRaises(HTTPException) as error:
            apply_preset("unknown", self.db)
        self.assertEqual(error.exception.status_code, 404)

    def test_conflicting_stock_rolls_back_entire_preset(self):
        self.db.add(models.Ingredient(name="Tote stock", unit="kg", stock_quantity=12, reorder_level=1))
        self.db.commit()
        with self.assertRaises(HTTPException) as error:
            apply_preset("retail", self.db)
        self.assertEqual(error.exception.status_code, 409)
        self.assertIsNone(self.db.scalar(select(models.MenuItem).where(models.MenuItem.name == "Cotton T-shirt")))
        self.assertEqual(get_profile(self.db)["business_type"], "cafe")

    def test_product_and_service_recipe_rules(self):
        for payload in (
            MenuItemCreate(name="Missing recipe", price=1000),
            MenuItemCreate(name="Missing product stock", price=1000, item_type="product"),
            MenuItemCreate(name="Service with stock", price=1000, item_type="service", recipe=[{"ingredient_id": 1, "quantity": 1}]),
            MenuItemCreate(name="Product using milk", price=1000, item_type="product", recipe=[{"ingredient_id": 1, "quantity": 1}]),
        ):
            with self.assertRaises(HTTPException) as error:
                add_menu_item(payload, self.db)
            self.assertEqual(error.exception.status_code, 422)

    def test_profile_persists_and_rejects_blank_name(self):
        saved = update_business(ProfileInput(name="  Everyday Store  ", business_type="grocery"), self.db)
        self.assertEqual(saved["name"], "Everyday Store")
        self.db.expire_all()
        self.assertEqual(get_profile(self.db)["business_type"], "grocery")
        with self.assertRaises(HTTPException):
            update_business(ProfileInput(name="   ", business_type="retail"), self.db)
        self.assertEqual(get_profile(self.db)["name"], "Everyday Store")


if __name__ == "__main__":
    unittest.main()
