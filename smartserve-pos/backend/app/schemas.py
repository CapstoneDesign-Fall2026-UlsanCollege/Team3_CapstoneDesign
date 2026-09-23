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
