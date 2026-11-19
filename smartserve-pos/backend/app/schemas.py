from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class MenuItemOut(BaseModel):
    id: int
    name: str
    price: float
    category: str = "General"
    item_type: str = "prepared"
    sku: str = ""


class OrderLineIn(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, le=20)


class OrderCreate(BaseModel):
    order_type: str = Field(pattern="^(dine_in|takeaway|in_store|pickup|service)$")
    items: list[OrderLineIn] = Field(min_length=1)
    table_number: int | None = Field(default=None, ge=1, le=50)
    ticket_id: int | None = Field(default=None, ge=1)


class PaymentCreate(BaseModel):
    result: str = Field(default="paid", pattern="^(paid|failed)$")
    method: str = Field(pattern="^(cash|card|qr)$")


class AddOrderItems(BaseModel):
    items: list[OrderLineIn] = Field(min_length=1)


class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    unit: str = Field(min_length=1, max_length=20)
    stock_quantity: Decimal = Field(ge=0, max_digits=18, decimal_places=6)
    reorder_level: Decimal = Field(ge=0, max_digits=18, decimal_places=6)


class RecipeLineCreate(BaseModel):
    unit: str | None = None
    ingredient_id: int
    quantity: Decimal = Field(gt=0, max_digits=18, decimal_places=6)


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=0)
    recipe: list[RecipeLineCreate] = Field(default_factory=list)
    category: str = Field(default="General", min_length=1, max_length=60)
    item_type: Literal["prepared", "product", "service"] = "prepared"
    sku: str = Field(default="", max_length=60)
