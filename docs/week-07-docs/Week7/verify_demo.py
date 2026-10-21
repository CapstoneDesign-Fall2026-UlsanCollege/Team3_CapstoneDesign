"""Automated service check, not a browser or spoken rehearsal.

Run from the repository root with the backend requirements installed:
python -B docs/week-07-docs/Week7/verify_demo.py
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

os.environ['DATABASE_URL'] = 'sqlite://'
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'smartserve-pos' / 'backend'))
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import Base, engine
from app.main import (create_order, simulate_payment, list_inventory, sales_dashboard,
                      owner_menu, update_menu_item, update_ingredient, get_order)
from app.schemas import OrderCreate, PaymentCreate, MenuItemCreate, IngredientCreate
from app.seed import seed_demo_data

checks = []
def check(label, expected, actual):
    assert actual == expected, (label, expected, actual)
    checks.append({'check': label, 'expected': expected, 'actual': actual, 'result': 'PASS'})

Base.metadata.create_all(engine)
try:
    with Session(engine) as db:
        seed_demo_data(db)
        stock = lambda: {i['name']: i for i in list_inventory(db)}
        latte = next(i for i in owner_menu(db) if i['name'] == 'Caffè Latte')
        order = create_order(OrderCreate(order_type='takeaway', items=[{'menu_item_id': latte['id'], 'quantity': 2}]), db)
        check('two-latte total', 9000, order['total'])
        before = stock()
        try:
            simulate_payment(order['id'], PaymentCreate(method='card', result='failed'), db)
            raise AssertionError('failed payment was accepted')
        except HTTPException as error:
            check('failed payment status', 402, error.status_code)
        check('failed payment leaves stock unchanged', before, stock())
        simulate_payment(order['id'], PaymentCreate(method='cash'), db)
        check('paid stock: milk ml / beans g', [4500, 1164], [stock()['Milk']['stock_quantity'], stock()['Coffee beans']['stock_quantity']])
        try:
            simulate_payment(order['id'], PaymentCreate(method='cash'), db)
            raise AssertionError('duplicate payment was accepted')
        except HTTPException as error:
            check('duplicate payment status', 409, error.status_code)
        check('duplicate leaves stock unchanged', [4500, 1164], [stock()['Milk']['stock_quantity'], stock()['Coffee beans']['stock_quantity']])
        beans = stock()['Coffee beans']
        update_ingredient(beans['id'], IngredientCreate(name=beans['name'], unit='kg', stock_quantity=1.164, reorder_level=0.25), db)
        edited = update_menu_item(latte['id'], MenuItemCreate(name='Latte test', price=6000, recipe=[{'ingredient_id': line['ingredient_id'], 'quantity': 18 if line['ingredient_id'] == beans['id'] else 250, 'unit': 'g' if line['ingredient_id'] == beans['id'] else 'ml'} for line in latte['recipe']]), db)
        check('18 g edit stores kg', 0.018, next(i['quantity'] for i in edited['recipe'] if i['ingredient_id'] == beans['id']))
        receipt = get_order(order['id'], db)
        check('old receipt name / unit price / total', ['Caffè Latte', 4500, 9000], [receipt['items'][0]['name'], receipt['items'][0]['unit_price'], receipt['total']])
        new = create_order(OrderCreate(order_type='takeaway', items=[{'menu_item_id': latte['id'], 'quantity': 1}]), db)
        simulate_payment(new['id'], PaymentCreate(method='cash'), db)
        check('next sale stock: milk ml / beans kg', [4250, 1.146], [stock()['Milk']['stock_quantity'], stock()['Coffee beans']['stock_quantity']])
        sales = sales_dashboard(db)
        check('daily paid orders / sales', [2, 15000], [sales['paid_orders'], sales['sales_total']])
    print(json.dumps({'date_kst': datetime.now(timezone(timedelta(hours=9))).isoformat(), 'method': 'automated service functions with isolated in-memory SQLite; no browser or human rehearsal', 'checks': checks}, ensure_ascii=True, indent=2))
finally:
    Base.metadata.drop_all(engine)
