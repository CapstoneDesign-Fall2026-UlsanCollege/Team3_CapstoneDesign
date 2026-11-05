from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    unit: Mapped[str] = mapped_column(String(20))
    stock_quantity: Mapped[float] = mapped_column(Numeric(18, 6))
    reorder_level: Mapped[float] = mapped_column(Numeric(18, 6), default=0)
    active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))


class MenuItem(Base):
    __tablename__ = "menu_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    active: Mapped[bool] = mapped_column(default=True)


class BusinessProfile(Base):
    __tablename__ = "business_profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="SmartServe POS")
    business_type: Mapped[str] = mapped_column(String(30), default="cafe")


class CatalogDetails(Base):
    __tablename__ = "catalog_details"
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), primary_key=True)
    category: Mapped[str] = mapped_column(String(60), default="General")
    item_type: Mapped[str] = mapped_column(String(20), default="prepared")
    sku: Mapped[str] = mapped_column(String(60), default="")
    starter_key: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)


class BusinessConfiguration(Base):
    __tablename__ = "business_configuration"
    id: Mapped[int] = mapped_column(primary_key=True)
    operation_mode: Mapped[str] = mapped_column(String(30), default="both")
    features: Mapped[str] = mapped_column(String(300), default="checkout,inventory,tables")
    address: Mapped[str] = mapped_column(String(300), default="")
    phone: Mapped[str] = mapped_column(String(40), default="")
    logo_url: Mapped[str] = mapped_column(String(2048), default="")
    receipt_footer: Mapped[str] = mapped_column(String(300), default="Thank you for your visit!")
    table_count: Mapped[int] = mapped_column(Integer, default=8)
    onboarding_complete: Mapped[bool] = mapped_column(default=False)


class WorkTicket(Base):
    __tablename__ = "work_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(120))
    customer: Mapped[str] = mapped_column(String(120))
    resource: Mapped[str] = mapped_column(String(80), default="Any staff")
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str] = mapped_column(String(1000), default="")
    status: Mapped[str] = mapped_column(String(20), default="booked")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class OrderContext(Base):
    __tablename__ = "order_context"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    table_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    ticket_id: Mapped[int | None] = mapped_column(ForeignKey("work_tickets.id"), unique=True, nullable=True)


class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id", ondelete="CASCADE"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    quantity: Mapped[float] = mapped_column(Numeric(18, 6))
    __table_args__ = (UniqueConstraint("menu_item_id", "ingredient_id", name="uq_recipe_ingredient"),)


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_type: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="open")
    total: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    trashed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    menu_item_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    method: Mapped[str] = mapped_column(String(30))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    simulated_reference: Mapped[str] = mapped_column(String(80), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    quantity_change: Mapped[float] = mapped_column(Numeric(18, 6))
    reason: Mapped[str] = mapped_column(String(40), default="paid_order")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("order_id", "ingredient_id", name="uq_order_ingredient_deduction"),)
