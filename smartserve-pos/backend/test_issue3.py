"""Run: python -m unittest -v test_issue3 (isolated SQLite test database)."""
import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database import Base, engine
from app import models
from app.main import create_order, simulate_payment, get_order
from app.schemas import OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class InventoryPaymentTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.db = Session(engine)
        seed_demo_data(self.db)
        latte = self.db.scalar(select(models.MenuItem).where(models.MenuItem.name == 'Caffè Latte'))
        self.payload = OrderCreate(order_type='dine_in', items=[{'menu_item_id': latte.id, 'quantity': 1}])
        self.order = create_order(self.payload, self.db)

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(engine)

    def stock(self):
        self.db.expire_all()
        return {i.name: Decimal(str(i.stock_quantity)) for i in self.db.scalars(select(models.Ingredient))}

    def count(self, model):
        return self.db.scalar(select(func.count()).select_from(model))

    def test_latte_and_duplicate_after_new_session(self):
        before = self.stock()
        result = simulate_payment(self.order['id'], PaymentCreate(method='cash'), self.db)
        after = self.stock()
        self.assertEqual(before['Milk'] - after['Milk'], Decimal('250'))
        self.assertEqual(before['Coffee beans'] - after['Coffee beans'], Decimal('18'))
        self.assertTrue(result['order']['inventory_deducted'])
        self.assertEqual(result['order']['status'], 'paid')
        movements = self.db.scalars(select(models.InventoryMovement)).all()
        self.assertEqual(len(movements), 2)
        self.assertEqual(sorted(m.quantity_change for m in movements), [Decimal('-250'), Decimal('-18')])
        self.assertTrue(all(m.order_id == self.order['id'] and m.created_at for m in movements))
        self.db.close()
        self.db = Session(engine)
        with self.assertRaises(HTTPException) as error:
            simulate_payment(self.order['id'], PaymentCreate(method='card'), self.db)
        self.assertEqual(error.exception.status_code, 409)
        self.assertIn('not deducted again', error.exception.detail)
        self.db.rollback()
        self.assertEqual(self.stock(), after)
        self.assertEqual(self.count(models.Payment), 1)
        self.assertEqual(self.count(models.InventoryMovement), 2)

    def test_failed_payment_then_retry(self):
        before = self.stock()
        with self.assertRaises(HTTPException) as error:
            simulate_payment(self.order['id'], PaymentCreate(method='card', result='failed'), self.db)
        self.assertEqual(error.exception.status_code, 402)
        self.db.rollback()
        self.assertEqual(self.stock(), before)
        self.assertEqual(self.count(models.Payment), 0)
        self.assertEqual(self.count(models.InventoryMovement), 0)
        self.assertEqual(get_order(self.order['id'], self.db)['status'], 'open')
        self.assertFalse(get_order(self.order['id'], self.db)['inventory_deducted'])
        self.assertEqual(simulate_payment(self.order['id'], PaymentCreate(method='card'), self.db)['order']['status'], 'paid')

    def test_insufficient_stock(self):
        milk = self.db.scalar(select(models.Ingredient).where(models.Ingredient.name == 'Milk'))
        milk.stock_quantity = 100
        self.db.commit()
        before = self.stock()
        with self.assertRaises(HTTPException) as error:
            simulate_payment(self.order['id'], PaymentCreate(method='cash'), self.db)
        self.assertEqual(error.exception.status_code, 409)
        self.db.rollback()
        self.assertEqual(self.stock(), before)
        self.assertEqual(self.count(models.Payment), 0)
        self.assertEqual(self.count(models.InventoryMovement), 0)

    def test_unique_order_ids(self):
        other = create_order(self.payload, self.db)
        self.assertNotEqual(self.order['id'], other['id'])

    def test_ledger_guard_even_if_status_is_inconsistent(self):
        simulate_payment(self.order['id'], PaymentCreate(method='cash'), self.db)
        order = self.db.get(models.Order, self.order['id'])
        order.status = 'open'
        self.db.commit()
        before = self.stock()
        with self.assertRaises(HTTPException):
            simulate_payment(order.id, PaymentCreate(method='cash'), self.db)
        self.db.rollback()
        self.assertEqual(self.stock(), before)
        self.assertEqual(self.count(models.InventoryMovement), 2)


if __name__ == '__main__':
    unittest.main()
