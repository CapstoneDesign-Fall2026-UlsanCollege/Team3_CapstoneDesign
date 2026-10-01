"""Run: python -B -m unittest -v test_owner_management (isolated SQLite database)."""
import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine
from app import models
from app.main import (
    add_ingredient, add_menu_item, create_order, get_order, list_inventory,
    list_menu, owner_inventory, owner_menu, remove_ingredient, remove_menu_item,
    simulate_payment,
)
from app.schemas import IngredientCreate, MenuItemCreate, OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class OwnerManagementTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.db = Session(engine)
        seed_demo_data(self.db)

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(engine)

    def add_tea(self):
        ingredient = add_ingredient(IngredientCreate(name='  Matcha powder  ', unit='g', stock_quantity=100, reorder_level=10), self.db)
        item = add_menu_item(MenuItemCreate(name='Matcha Latte', price=6000, recipe=[{'ingredient_id': ingredient['id'], 'quantity': 5}]), self.db)
        return ingredient, item

    def test_add_menu_with_recipe_pay_and_archive_without_losing_history(self):
        ingredient, item = self.add_tea()
        self.assertEqual(ingredient['name'], 'Matcha powder')
        self.assertEqual(item['recipe'][0]['quantity'], 5)
        order = create_order(OrderCreate(order_type='takeaway', items=[{'menu_item_id': item['id'], 'quantity': 2}]), self.db)
        self.assertEqual(order['total'], 12000)
        paid = simulate_payment(order['id'], PaymentCreate(method='cash'), self.db)['order']
        self.assertEqual(paid['status'], 'paid')
        self.assertEqual(next(i for i in list_inventory(self.db) if i['id'] == ingredient['id'])['stock_quantity'], 90)
        self.assertFalse(remove_menu_item(item['id'], self.db)['active'])
        self.assertNotIn(item['id'], [i.id for i in list_menu(self.db)])
        self.assertFalse(remove_ingredient(ingredient['id'], self.db)['active'])
        self.assertNotIn(ingredient['id'], [i['id'] for i in list_inventory(self.db)])
        self.assertEqual(get_order(order['id'], self.db)['items'][0]['name'], 'Matcha Latte')
        self.assertEqual(len(self.db.scalars(select(models.InventoryMovement).where(models.InventoryMovement.order_id == order['id'])).all()), 1)
        self.assertTrue(any(i['id'] == item['id'] for i in owner_menu(self.db)))
        self.assertTrue(any(i['id'] == ingredient['id'] for i in owner_inventory(self.db)))

    def test_cannot_archive_ingredient_used_by_active_menu_or_open_order(self):
        ingredient, item = self.add_tea()
        with self.assertRaises(HTTPException) as active_error:
            remove_ingredient(ingredient['id'], self.db)
        self.assertEqual(active_error.exception.status_code, 409)
        order = create_order(OrderCreate(order_type='dine_in', items=[{'menu_item_id': item['id'], 'quantity': 1}]), self.db)
        remove_menu_item(item['id'], self.db)
        with self.assertRaises(HTTPException) as open_error:
            remove_ingredient(ingredient['id'], self.db)
        self.assertEqual(open_error.exception.status_code, 409)
        simulate_payment(order['id'], PaymentCreate(method='card'), self.db)
        self.assertFalse(remove_ingredient(ingredient['id'], self.db)['active'])

    def test_reject_duplicate_names_and_inactive_recipe_ingredient(self):
        ingredient, item = self.add_tea()
        with self.assertRaises(HTTPException) as duplicate:
            add_menu_item(MenuItemCreate(name='matcha latte', price=6000, recipe=[{'ingredient_id': ingredient['id'], 'quantity': 5}]), self.db)
        self.assertEqual(duplicate.exception.status_code, 409)
        remove_menu_item(item['id'], self.db)
        remove_ingredient(ingredient['id'], self.db)
        with self.assertRaises(HTTPException) as inactive:
            add_menu_item(MenuItemCreate(name='Matcha Shake', price=6500, recipe=[{'ingredient_id': ingredient['id'], 'quantity': 5}]), self.db)
        self.assertEqual(inactive.exception.status_code, 422)


if __name__ == '__main__':
    unittest.main()
