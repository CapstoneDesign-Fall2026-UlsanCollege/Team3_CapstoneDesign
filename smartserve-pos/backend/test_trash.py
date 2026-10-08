"""Order trash lifecycle checks using an isolated SQLite database."""
import os
os.environ['DATABASE_URL'] = 'sqlite://'
import unittest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import Base, engine
from app import models
from app.main import (create_order, cancel_order, trash_order, restore_order,
                      delete_trashed_order, list_orders, purge_expired_trash,
                      simulate_payment, get_order)
from app.schemas import OrderCreate, PaymentCreate
from app.seed import seed_demo_data


class OrderTrashTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.db = Session(engine)
        seed_demo_data(self.db)
        item = self.db.scalar(select(models.MenuItem).where(models.MenuItem.name == 'Americano'))
        self.order = create_order(OrderCreate(order_type='takeaway', items=[{'menu_item_id': item.id, 'quantity': 1}]), self.db)

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(engine)

    def test_trash_restore_and_permanent_delete(self):
        cancel_order(self.order['id'], self.db)
        trashed = trash_order(self.order['id'], self.db)
        self.assertIsNotNone(trashed['delete_after'])
        self.assertEqual(list_orders(self.db), [])
        self.assertEqual([o['id'] for o in list_orders(self.db, trash=True)], [self.order['id']])
        with self.assertRaises(HTTPException):
            get_order(self.order['id'], self.db)
        restored = restore_order(self.order['id'], self.db)
        self.assertEqual(restored['status'], 'cancelled')
        self.assertIsNone(restored['trashed_at'])
        self.assertEqual(len(list_orders(self.db)), 1)
        trash_order(self.order['id'], self.db)
        delete_trashed_order(self.order['id'], self.db)
        self.assertIsNone(self.db.get(models.Order, self.order['id']))
        self.assertEqual(self.db.scalars(select(models.OrderItem)).all(), [])

    def test_open_and_paid_orders_cannot_be_trashed(self):
        with self.assertRaises(HTTPException) as error:
            trash_order(self.order['id'], self.db)
        self.assertEqual(error.exception.status_code, 409)
        self.db.rollback()
        simulate_payment(self.order['id'], PaymentCreate(method='cash'), self.db)
        with self.assertRaises(HTTPException):
            trash_order(self.order['id'], self.db)
        self.db.rollback()
        self.assertEqual(get_order(self.order['id'], self.db)['status'], 'paid')

    def test_auto_expiry_and_payment_guard(self):
        cancel_order(self.order['id'], self.db)
        trash_order(self.order['id'], self.db)
        with self.assertRaises(HTTPException) as error:
            simulate_payment(self.order['id'], PaymentCreate(method='cash'), self.db)
        self.assertEqual(error.exception.status_code, 409)
        self.db.rollback()
        order = self.db.get(models.Order, self.order['id'])
        order.trashed_at = datetime.now(timezone.utc) - timedelta(days=29)
        self.db.commit()
        purge_expired_trash(self.db)
        self.assertIsNotNone(self.db.get(models.Order, self.order['id']))
        order.trashed_at = datetime.now(timezone.utc) - timedelta(days=30, seconds=1)
        self.db.commit()
        purge_expired_trash(self.db)
        self.assertIsNone(self.db.get(models.Order, self.order['id']))


if __name__ == '__main__':
    unittest.main()
