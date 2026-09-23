from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import Base, engine
from . import models  # Registers models before create_all.
from .database import get_db
from .schemas import MenuItemOut, OrderCreate, PaymentCreate
from .seed import seed_demo_data

app = FastAPI(title="SmartServe POS MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_demo_data(db)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/menu", response_model=list[MenuItemOut])
def list_menu(db: Session = Depends(get_db)):
    return db.scalars(select(models.MenuItem).where(models.MenuItem.active.is_(True)).order_by(models.MenuItem.name)).all()


def inventory_was_deducted(order_id: int, db: Session) -> bool:
    # The durable movement ledger is the source of truth; no schema migration needed.
    return db.scalar(select(models.InventoryMovement.id).where(
        models.InventoryMovement.order_id == order_id
    ).limit(1)) is not None


def order_view(order: models.Order, db: Session) -> dict:
    lines = db.scalars(select(models.OrderItem).where(models.OrderItem.order_id == order.id)).all()
    menu = {item.id: item for item in db.scalars(select(models.MenuItem).where(models.MenuItem.id.in_([line.menu_item_id for line in lines]))).all()} if lines else {}
    payment = db.scalar(select(models.Payment).where(models.Payment.order_id == order.id))
    return {
        "id": order.id,
        "order_type": order.order_type,
        "status": order.status,
        "inventory_deducted": inventory_was_deducted(order.id, db),
        "total": float(order.total),
        "created_at": order.created_at,
        "paid_at": order.paid_at,
        "items": [{"name": menu[line.menu_item_id].name, "quantity": line.quantity, "unit_price": float(line.unit_price)} for line in lines],
        "payment_method": payment.method if payment else None,
        "simulated_reference": payment.simulated_reference if payment else None,
    }


@app.post("/orders", status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    requested_ids = [line.menu_item_id for line in payload.items]
    menu_items = db.scalars(select(models.MenuItem).where(models.MenuItem.id.in_(requested_ids), models.MenuItem.active.is_(True))).all()
    menu_by_id = {item.id: item for item in menu_items}
    missing = sorted(set(requested_ids) - set(menu_by_id))
    if missing:
        raise HTTPException(status_code=404, detail=f"Menu item(s) not found: {missing}")

    total = sum((Decimal(str(menu_by_id[line.menu_item_id].price)) * line.quantity for line in payload.items), Decimal("0"))
    order = models.Order(order_type=payload.order_type, status="open", total=total)
    db.add(order)
    db.flush()
    db.add_all([models.OrderItem(order_id=order.id, menu_item_id=line.menu_item_id, quantity=line.quantity, unit_price=menu_by_id[line.menu_item_id].price) for line in payload.items])
    db.commit()
    db.refresh(order)
    return order_view(order, db)


@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_view(order, db)


@app.post("/orders/{order_id}/pay")
def simulate_payment(order_id: int, payload: PaymentCreate, db: Session = Depends(get_db)):
    # A row lock means two near-simultaneous Pay clicks are processed one at a time.
    order = db.scalar(select(models.Order).where(models.Order.id == order_id).with_for_update())
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    inventory_deducted = inventory_was_deducted(order.id, db)
    if order.status == "paid" or inventory_deducted:
        raise HTTPException(status_code=409, detail="This order has already been processed. Inventory was not deducted again.")
    if payload.result == "failed":
        raise HTTPException(status_code=402, detail="Simulated payment failed. Inventory is unchanged; you can retry this order.")

    lines = db.scalars(select(models.OrderItem).where(models.OrderItem.order_id == order.id)).all()
    quantities_by_menu: dict[int, int] = {}
    for line in lines:
        quantities_by_menu[line.menu_item_id] = quantities_by_menu.get(line.menu_item_id, 0) + line.quantity
    recipe_rows = db.scalars(select(models.RecipeItem).where(models.RecipeItem.menu_item_id.in_(quantities_by_menu))).all()
    required: dict[int, Decimal] = {}
    for recipe in recipe_rows:
        required[recipe.ingredient_id] = required.get(recipe.ingredient_id, Decimal("0")) + Decimal(str(recipe.quantity)) * quantities_by_menu[recipe.menu_item_id]

    ingredients = db.scalars(select(models.Ingredient).where(models.Ingredient.id.in_(required)).order_by(models.Ingredient.id).with_for_update()).all()
    ingredient_by_id = {ingredient.id: ingredient for ingredient in ingredients}
    shortages = [f"{ingredient_by_id[i].name} needs {amount}{ingredient_by_id[i].unit}" for i, amount in required.items() if Decimal(str(ingredient_by_id[i].stock_quantity)) < amount]
    if shortages:
        raise HTTPException(status_code=409, detail={"message": "Insufficient inventory", "shortages": shortages})

    # Successful simulated payment and stock changes commit atomically.
    order.status = "paid"
    order.paid_at = datetime.now(timezone.utc)
    for ingredient_id, amount in required.items():
        ingredient = ingredient_by_id[ingredient_id]
        ingredient.stock_quantity = Decimal(str(ingredient.stock_quantity)) - amount
        db.add(models.InventoryMovement(ingredient_id=ingredient_id, order_id=order.id, quantity_change=-amount, reason="paid_order"))
    db.add(models.Payment(order_id=order.id, method=payload.method, amount=order.total, simulated_reference=f"SIM-{uuid4().hex[:10].upper()}"))
    db.commit()
    db.refresh(order)
    return {"message": "Simulated payment successful. Ingredients deducted once.", "order": order_view(order, db)}


@app.get("/inventory")
def list_inventory(db: Session = Depends(get_db)):
    ingredients = db.scalars(select(models.Ingredient).order_by(models.Ingredient.name)).all()
    return [{
        "id": ingredient.id,
        "name": ingredient.name,
        "unit": ingredient.unit,
        "stock_quantity": float(ingredient.stock_quantity),
        "reorder_level": float(ingredient.reorder_level),
        "low_stock": ingredient.stock_quantity <= ingredient.reorder_level,
    } for ingredient in ingredients]


@app.get("/dashboard/sales")
def sales_dashboard(db: Session = Depends(get_db)):
    today = date.today()
    count, total = db.execute(
        select(func.count(models.Order.id), func.coalesce(func.sum(models.Order.total), 0))
        .where(models.Order.status == "paid", func.date(models.Order.paid_at) == today)
    ).one()
    recent = db.scalars(
        select(models.Order).where(models.Order.status == "paid").order_by(models.Order.paid_at.desc()).limit(8)
    ).all()
    return {
        "date": today.isoformat(),
        "paid_orders": count,
        "sales_total": float(total),
        "recent_sales": [order_view(order, db) for order in recent],
    }
