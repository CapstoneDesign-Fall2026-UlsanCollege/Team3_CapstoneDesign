from decimal import Decimal

from pydantic import BaseModel, Field


class MenuItemOut(BaseModel):
    id: int
    name: str
    price: float


class OrderLineIn(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, le=20)


class OrderCreate(BaseModel):
    order_type: str = Field(pattern="^(dine_in|takeaway)$")
    items: list[OrderLineIn] = Field(min_length=1)


class PaymentCreate(BaseModel):
    result: str = Field(default="paid", pattern="^(paid|failed)$")
    method: str = Field(pattern="^(cash|card|qr)$")


class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    unit: str = Field(min_length=1, max_length=20)
    stock_quantity: Decimal = Field(ge=0, max_digits=18, decimal_places=6)
    reorder_level: Decimal = Field(ge=0, max_digits=18, decimal_places=6)


class RecipeLineCreate(BaseModel):
    ingredient_id: int
    quantity: Decimal = Field(gt=0, max_digits=18, decimal_places=6)


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=0)
    recipe: list[RecipeLineCreate] = Field(min_length=1)
