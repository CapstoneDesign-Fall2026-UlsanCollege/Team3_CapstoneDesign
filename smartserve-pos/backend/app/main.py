from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from uuid import uuid4
import asyncio

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import delete, func, inspect, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine
from . import models  # Registers models before create_all.
from .database import get_db
from .schemas import IngredientCreate, MenuItemCreate, MenuItemOut, OrderCreate, PaymentCreate
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
    if "trashed_at" not in {column["name"] for column in inspect(engine).get_columns("orders")}:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE orders ADD COLUMN trashed_at TIMESTAMP WITH TIME ZONE NULL"))
    # Existing demo databases predate the ingredient archive flag.
    if "active" not in {column["name"] for column in inspect(engine).get_columns("ingredients")}:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE ingredients ADD COLUMN active BOOLEAN NOT NULL DEFAULT TRUE"))
    with Session(engine) as db:
        seed_demo_data(db)


def permanently_delete_cancelled(order: models.Order, db: Session) -> None:
    if order.status != "cancelled" or db.scalar(select(models.Payment.id).where(models.Payment.order_id == order.id)) or inventory_was_deducted(order.id, db):
        raise HTTPException(status_code=409, detail="Orders with payment or inventory history cannot be deleted.")
    db.execute(delete(models.OrderItem).where(models.OrderItem.order_id == order.id))
    db.delete(order)


def purge_expired_trash(db: Session) -> None:
    expired = db.scalars(select(models.Order).where(models.Order.trashed_at <= datetime.now(timezone.utc) - timedelta(days=30), models.Order.status == "cancelled").with_for_update()).all()
    for order in expired:
        if not db.scalar(select(models.Payment.id).where(models.Payment.order_id == order.id)) and not inventory_was_deducted(order.id, db):
            permanently_delete_cancelled(order, db)
    db.commit()


def run_trash_cleanup() -> None:
    with Session(engine) as db:
        purge_expired_trash(db)


async def trash_cleanup_loop() -> None:
    while True:
        try:
            await asyncio.to_thread(run_trash_cleanup)
        except Exception:
            import logging
            logging.exception("Order trash cleanup failed; retrying in one minute")
        await asyncio.sleep(60)


@app.on_event("startup")
async def start_trash_cleanup() -> None:
    app.state.trash_cleanup = asyncio.create_task(trash_cleanup_loop())


@app.on_event("shutdown")
async def stop_trash_cleanup() -> None:
    app.state.trash_cleanup.cancel()
    try:
        await app.state.trash_cleanup
    except asyncio.CancelledError:
        pass


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/menu", response_model=list[MenuItemOut])
def list_menu(db: Session = Depends(get_db)):
    return db.scalars(select(models.MenuItem).where(models.MenuItem.active.is_(True)).order_by(models.MenuItem.name)).all()


def ingredient_view(ingredient: models.Ingredient, db: Session | None = None) -> dict:
    return {
        "id": ingredient.id, "name": ingredient.name, "unit": ingredient.unit,
        **({"unit_editable": not (db.scalar(select(models.RecipeItem.id).where(models.RecipeItem.ingredient_id == ingredient.id).limit(1)) or db.scalar(select(models.InventoryMovement.id).where(models.InventoryMovement.ingredient_id == ingredient.id).limit(1)))} if db is not None else {}),
        "stock_quantity": float(ingredient.stock_quantity),
        "reorder_level": float(ingredient.reorder_level),
        "low_stock": ingredient.stock_quantity <= ingredient.reorder_level,
        "active": ingredient.active,
    }


def owner_menu_view(item: models.MenuItem, db: Session) -> dict:
    recipe = db.scalars(select(models.RecipeItem).where(models.RecipeItem.menu_item_id == item.id)).all()
    ingredients = {ingredient.id: ingredient.name for ingredient in db.scalars(select(models.Ingredient)).all()}
    return {
        "id": item.id, "name": item.name, "price": float(item.price), "active": item.active,
        "recipe": [{"ingredient_id": line.ingredient_id, "ingredient_name": ingredients[line.ingredient_id], "quantity": float(line.quantity)} for line in recipe],
    }


@app.get("/owner/menu")
def owner_menu(db: Session = Depends(get_db)):
    items = db.scalars(select(models.MenuItem).order_by(models.MenuItem.name)).all()
    return [owner_menu_view(item, db) for item in items]


@app.post("/owner/menu", status_code=201)
def add_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Menu name is required")
    if db.scalar(select(models.MenuItem.id).where(func.lower(models.MenuItem.name) == name.lower())):
        raise HTTPException(status_code=409, detail="A menu item with this name already exists")
    ingredient_ids = [line.ingredient_id for line in payload.recipe]
    if len(ingredient_ids) != len(set(ingredient_ids)):
        raise HTTPException(status_code=422, detail="Use each ingredient only once in a recipe")
    available = set(db.scalars(select(models.Ingredient.id).where(models.Ingredient.id.in_(ingredient_ids), models.Ingredient.active.is_(True)).with_for_update()).all())
    if available != set(ingredient_ids):
        raise HTTPException(status_code=422, detail="Recipe ingredients must be active inventory items")
    item = models.MenuItem(name=name, price=payload.price, active=True)
    db.add(item)
    try:
        db.flush()
        db.add_all([models.RecipeItem(menu_item_id=item.id, ingredient_id=line.ingredient_id, quantity=line.quantity) for line in payload.recipe])
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Menu item could not be added; check its name and recipe")
    return owner_menu_view(item, db)


@app.put("/owner/menu/{item_id}")
def update_menu_item(item_id: int, payload: MenuItemCreate, db: Session = Depends(get_db)):
    item = db.scalar(select(models.MenuItem).where(models.MenuItem.id == item_id).with_for_update())
    if not item or not item.active:
        raise HTTPException(status_code=404, detail="Active menu item not found")
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Menu name is required")
    if db.scalar(select(models.MenuItem.id).where(func.lower(models.MenuItem.name) == name.lower(), models.MenuItem.id != item_id)):
        raise HTTPException(status_code=409, detail="A menu item with this name already exists")
    ingredient_ids = [line.ingredient_id for line in payload.recipe]
    if len(ingredient_ids) != len(set(ingredient_ids)):
        raise HTTPException(status_code=422, detail="Use each ingredient only once in a recipe")
    available = set(db.scalars(select(models.Ingredient.id).where(models.Ingredient.id.in_(ingredient_ids), models.Ingredient.active.is_(True)).with_for_update()).all())
    if available != set(ingredient_ids):
        raise HTTPException(status_code=422, detail="Recipe ingredients must be active inventory items")
    old_recipe = {(line.ingredient_id, Decimal(str(line.quantity))) for line in db.scalars(select(models.RecipeItem).where(models.RecipeItem.menu_item_id == item_id)).all()}
    new_recipe = {(line.ingredient_id, line.quantity) for line in payload.recipe}
    if old_recipe != new_recipe and db.scalar(select(models.OrderItem.id).join(models.Order).where(models.OrderItem.menu_item_id == item_id, models.Order.status == "open").limit(1)):
        raise HTTPException(status_code=409, detail="Pay or cancel open orders for this item before changing its recipe")
    item.name, item.price = name, payload.price
    db.execute(delete(models.RecipeItem).where(models.RecipeItem.menu_item_id == item_id))
    try:
        db.flush()
        db.add_all([models.RecipeItem(menu_item_id=item.id, ingredient_id=line.ingredient_id, quantity=line.quantity) for line in payload.recipe])
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Menu item could not be added; check its name and recipe")
    return owner_menu_view(item, db)


@app.delete("/owner/menu/{item_id}")
def remove_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.scalar(select(models.MenuItem).where(models.MenuItem.id == item_id).with_for_update())
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if not item.active:
        raise HTTPException(status_code=409, detail="Menu item is already removed")
    item.active = False
    db.commit()
    return owner_menu_view(item, db)


@app.get("/owner/inventory")
def owner_inventory(db: Session = Depends(get_db)):
    ingredients = db.scalars(select(models.Ingredient).order_by(models.Ingredient.name)).all()
    return [ingredient_view(ingredient, db) for ingredient in ingredients]


@app.post("/owner/inventory", status_code=201)
def add_ingredient(payload: IngredientCreate, db: Session = Depends(get_db)):
    name, unit = payload.name.strip(), payload.unit.strip()
    if not name or not unit:
        raise HTTPException(status_code=422, detail="Ingredient name and unit are required")
    if db.scalar(select(models.Ingredient.id).where(func.lower(models.Ingredient.name) == name.lower())):
        raise HTTPException(status_code=409, detail="An ingredient with this name already exists")
    ingredient = models.Ingredient(name=name, unit=unit, stock_quantity=payload.stock_quantity, reorder_level=payload.reorder_level, active=True)
    db.add(ingredient)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An ingredient with this name already exists")
    db.refresh(ingredient)
    return ingredient_view(ingredient, db)


@app.put("/owner/inventory/{ingredient_id}")
def update_ingredient(ingredient_id: int, payload: IngredientCreate, db: Session = Depends(get_db)):
    ingredient = db.scalar(select(models.Ingredient).where(models.Ingredient.id == ingredient_id).with_for_update())
    if not ingredient or not ingredient.active:
        raise HTTPException(status_code=404, detail="Active ingredient not found")
    name, unit = payload.name.strip(), payload.unit.strip()
    if not name or not unit:
        raise HTTPException(status_code=422, detail="Ingredient name and unit are required")
    if db.scalar(select(models.Ingredient.id).where(func.lower(models.Ingredient.name) == name.lower(), models.Ingredient.id != ingredient_id)):
        raise HTTPException(status_code=409, detail="An ingredient with this name already exists")
    if unit != ingredient.unit and (db.scalar(select(models.RecipeItem.id).where(models.RecipeItem.ingredient_id == ingredient_id).limit(1)) or db.scalar(select(models.InventoryMovement.id).where(models.InventoryMovement.ingredient_id == ingredient_id).limit(1))):
        raise HTTPException(status_code=409, detail="Unit is used by recipes or stock history. Create a new ingredient for a different unit")
    ingredient.name, ingredient.unit = name, unit
    ingredient.stock_quantity, ingredient.reorder_level = payload.stock_quantity, payload.reorder_level
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An ingredient with this name already exists")
    db.refresh(ingredient)
    return ingredient_view(ingredient, db)


@app.delete("/owner/inventory/{ingredient_id}")
def remove_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.scalar(select(models.Ingredient).where(models.Ingredient.id == ingredient_id).with_for_update())
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not ingredient.active:
        raise HTTPException(status_code=409, detail="Ingredient is already removed")
    used_by_menu = db.scalar(select(models.RecipeItem.id).join(models.MenuItem, models.MenuItem.id == models.RecipeItem.menu_item_id).where(models.RecipeItem.ingredient_id == ingredient_id, models.MenuItem.active.is_(True)).limit(1))
    used_by_open_order = db.scalar(select(models.OrderItem.id).join(models.Order, models.Order.id == models.OrderItem.order_id).join(models.RecipeItem, models.RecipeItem.menu_item_id == models.OrderItem.menu_item_id).where(models.RecipeItem.ingredient_id == ingredient_id, models.Order.status == "open").limit(1))
    if used_by_menu or used_by_open_order:
        raise HTTPException(status_code=409, detail="Ingredient is used by a menu item or open order. Remove the menu item and settle open orders first.")
    ingredient.active = False
    db.commit()
    return ingredient_view(ingredient, db)


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
        "trashed_at": order.trashed_at,
        "delete_after": order.trashed_at + timedelta(days=30) if order.trashed_at else None,
        "items": [{"name": menu[line.menu_item_id].name, "quantity": line.quantity, "unit_price": float(line.unit_price)} for line in lines],
        "payment_method": payment.method if payment else None,
        "simulated_reference": payment.simulated_reference if payment else None,
    }


@app.post("/orders", status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    requested_ids = [line.menu_item_id for line in payload.items]
    menu_items = db.scalars(select(models.MenuItem).where(models.MenuItem.id.in_(requested_ids), models.MenuItem.active.is_(True)).with_for_update()).all()
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
    if not order or order.trashed_at:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_view(order, db)


@app.get("/orders")
def list_orders(db: Session = Depends(get_db), trash: bool = False):
    purge_expired_trash(db)
    orders = db.scalars(select(models.Order).where(models.Order.trashed_at.is_not(None) if trash else models.Order.trashed_at.is_(None)).order_by(models.Order.created_at.desc(), models.Order.id.desc())).all()
    return [order_view(order, db) for order in orders]


@app.post("/orders/{order_id}/trash")
def trash_order(order_id: int, db: Session = Depends(get_db)):
    order = db.scalar(select(models.Order).where(models.Order.id == order_id).with_for_update())
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "cancelled" or inventory_was_deducted(order.id, db) or db.scalar(select(models.Payment.id).where(models.Payment.order_id == order.id)):
        raise HTTPException(status_code=409, detail="Cancel an unpaid order before moving it to Trash. Paid orders are retained.")
    if not order.trashed_at:
        order.trashed_at = datetime.now(timezone.utc)
    db.commit()
    return order_view(order, db)


@app.post("/orders/{order_id}/restore")
def restore_order(order_id: int, db: Session = Depends(get_db)):
    purge_expired_trash(db)
    order = db.scalar(select(models.Order).where(models.Order.id == order_id).with_for_update())
    if not order or not order.trashed_at:
        raise HTTPException(status_code=404, detail="Trashed order not found or already expired")
    order.trashed_at = None
    db.commit()
    return order_view(order, db)


@app.delete("/orders/{order_id}", status_code=204)
def delete_trashed_order(order_id: int, db: Session = Depends(get_db)):
    order = db.scalar(select(models.Order).where(models.Order.id == order_id).with_for_update())
    if not order or not order.trashed_at:
        raise HTTPException(status_code=404, detail="Move this order to Trash before deleting it permanently.")
    permanently_delete_cancelled(order, db)
    db.commit()


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.scalar(select(models.Order).where(models.Order.id == order_id).with_for_update())
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.trashed_at or order.status != "open" or inventory_was_deducted(order.id, db):
        raise HTTPException(status_code=409, detail="Only an unpaid open order can be cancelled.")
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order_view(order, db)


@app.post("/orders/{order_id}/pay")
def simulate_payment(order_id: int, payload: PaymentCreate, db: Session = Depends(get_db)):
    # A row lock means two near-simultaneous Pay clicks are processed one at a time.
    order = db.scalar(select(models.Order).where(models.Order.id == order_id).with_for_update())
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    inventory_deducted = inventory_was_deducted(order.id, db)
    if order.trashed_at:
        raise HTTPException(status_code=409, detail="This order is in Trash and cannot be paid.")
    if order.status == "paid" or inventory_deducted:
        raise HTTPException(status_code=409, detail="This order has already been processed. Inventory was not deducted again.")
    if order.status != "open":
        raise HTTPException(status_code=409, detail="Only an open order can be paid.")
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
    ingredients = db.scalars(select(models.Ingredient).where(models.Ingredient.active.is_(True)).order_by(models.Ingredient.name)).all()
    return [ingredient_view(ingredient) for ingredient in ingredients]


@app.get("/dashboard/sales")
def sales_dashboard(db: Session = Depends(get_db), selected_date: date | None = None):
    korea = timezone(timedelta(hours=9))
    today = selected_date or datetime.now(korea).date()
    start = datetime.combine(today, time.min, tzinfo=korea).astimezone(timezone.utc)
    end = start + timedelta(days=1)
    paid_on_day = (models.Order.status == "paid", models.Order.paid_at >= start, models.Order.paid_at < end)
    count, total = db.execute(
        select(func.count(models.Order.id), func.coalesce(func.sum(models.Order.total), 0))
        .where(*paid_on_day)
    ).one()
    recent = db.scalars(
        select(models.Order).where(*paid_on_day).order_by(models.Order.paid_at.desc(), models.Order.id.desc()).limit(100)
    ).all()
    return {
        "date": today.isoformat(),
        "timezone": "Asia/Seoul",
        "paid_orders": count,
        "sales_total": float(total),
        "recent_sales": [order_view(order, db) for order in recent],
    }
