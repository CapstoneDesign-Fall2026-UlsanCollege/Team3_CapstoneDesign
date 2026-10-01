from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Ingredient, MenuItem, RecipeItem


def seed_demo_data(db: Session) -> None:
    if db.scalar(select(MenuItem.id).limit(1)):
        return

    milk = Ingredient(name="Milk", unit="ml", stock_quantity=5000, reorder_level=1000)
    beans = Ingredient(name="Coffee beans", unit="g", stock_quantity=1200, reorder_level=250)
    tea = Ingredient(name="Tea leaves", unit="g", stock_quantity=700, reorder_level=150)
    sugar = Ingredient(name="Sugar", unit="g", stock_quantity=2500, reorder_level=500)
    latte = MenuItem(name="Caffè Latte", price=4500)
    americano = MenuItem(name="Americano", price=3500)
    milk_tea = MenuItem(name="Milk Tea", price=5000)
    db.add_all([milk, beans, tea, sugar, latte, americano, milk_tea])
    db.flush()
    db.add_all([
        RecipeItem(menu_item_id=latte.id, ingredient_id=milk.id, quantity=250),
        RecipeItem(menu_item_id=latte.id, ingredient_id=beans.id, quantity=18),
        RecipeItem(menu_item_id=americano.id, ingredient_id=beans.id, quantity=18),
        RecipeItem(menu_item_id=milk_tea.id, ingredient_id=milk.id, quantity=200),
        RecipeItem(menu_item_id=milk_tea.id, ingredient_id=tea.id, quantity=8),
        RecipeItem(menu_item_id=milk_tea.id, ingredient_id=sugar.id, quantity=20),
    ])
    db.commit()
