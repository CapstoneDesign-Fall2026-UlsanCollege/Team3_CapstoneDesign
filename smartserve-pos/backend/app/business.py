"""Single-store business setup and non-destructive catalog starters."""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models
from .database import get_db

BusinessType = Literal["cafe", "restaurant", "bakery", "retail", "grocery", "barbershop", "beauty", "repair", "services", "custom"]
router = APIRouter()

# name, KRW price, category, type, stock components (name, unit, opening stock, per-sale usage)
STARTERS = {
    "cafe": ("Café & bakery", "Drinks, baked goods and ingredient recipes", [
        ("Espresso", 3000, "Coffee", "prepared", [("Espresso beans", "g", 1000, 18)]),
        ("Butter croissant", 3500, "Bakery", "product", [("Croissant stock", "pcs", 30, 1)]),
        ("Iced tea", 4000, "Tea", "prepared", [("Tea concentrate", "ml", 3000, 100)]),
    ]),
    "restaurant": ("Restaurant & takeaway", "Meals, drinks and recipe-based stock", [
        ("Classic burger", 9000, "Mains", "prepared", [("Burger buns", "pcs", 50, 1), ("Burger patties", "pcs", 50, 1)]),
        ("French fries", 4000, "Sides", "prepared", [("Frozen fries", "g", 10000, 150)]),
        ("Sparkling water", 2500, "Drinks", "product", [("Sparkling water bottles", "pcs", 60, 1)]),
    ]),
    "retail": ("Retail & boutique", "Products, SKUs and stock by piece", [
        ("Cotton T-shirt", 19000, "Clothing", "product", [("T-shirt stock", "pcs", 40, 1)]),
        ("Canvas tote", 12000, "Accessories", "product", [("Tote stock", "pcs", 25, 1)]),
        ("Everyday cap", 15000, "Accessories", "product", [("Cap stock", "pcs", 30, 1)]),
    ]),
    "grocery": ("Grocery & convenience", "Packaged essentials and stock by piece", [
        ("Bottled water", 1000, "Drinks", "product", [("Water bottle stock", "pcs", 100, 1)]),
        ("Whole milk 1L", 3000, "Dairy", "product", [("Milk carton stock", "pcs", 40, 1)]),
        ("Snack bar", 1500, "Snacks", "product", [("Snack bar stock", "pcs", 80, 1)]),
    ]),
    "beauty": ("Salon & beauty", "Services alongside take-home products", [
        ("Haircut", 25000, "Hair services", "service", []),
        ("Wash & styling", 18000, "Hair services", "service", []),
        ("Care shampoo", 16000, "Hair care", "product", [("Shampoo bottle stock", "pcs", 20, 1)]),
    ]),
    "services": ("Services & repair", "Fixed-price work without physical stock", [
        ("Consultation", 30000, "Consulting", "service", []),
        ("Device diagnosis", 15000, "Repairs", "service", []),
        ("Installation service", 45000, "Installation", "service", []),
    ]),
}

STARTERS.update({
    "bakery": ("Bakery & desserts", "Counter service, tables and fresh baked goods", [
        ("Sourdough loaf", 6500, "Bread", "product", [("Sourdough stock", "pcs", 25, 1)]),
        ("Cinnamon roll", 4000, "Pastries", "product", [("Cinnamon roll stock", "pcs", 30, 1)]),
        ("Chocolate cake slice", 6000, "Desserts", "product", [("Cake slice stock", "pcs", 20, 1)]),
    ]),
    "barbershop": ("Barbershop", "Walk-ins, appointments and grooming services", [
        ("Classic haircut", 20000, "Haircuts", "service", []),
        ("Beard trim", 10000, "Grooming", "service", []),
        ("Haircut & shave", 30000, "Packages", "service", []),
    ]),
    "repair": ("Repair & workshop", "Track jobs from drop-off to collection", [
        ("Repair diagnosis", 15000, "Diagnostics", "service", []),
        ("Screen replacement labor", 40000, "Repairs", "service", []),
        ("Device cleaning", 12000, "Maintenance", "service", []),
    ]),
    "custom": ("Custom setup", "Choose your own workflows and build your catalog", []),
})

MODES = {
    "cafe": ["takeaway", "tables", "both"], "restaurant": ["takeaway", "tables", "both"],
    "bakery": ["takeaway", "tables", "both"], "retail": ["in_store", "pickup", "both"],
    "grocery": ["in_store", "pickup", "both"], "barbershop": ["walk_ins", "appointments", "both"],
    "beauty": ["walk_ins", "appointments", "both"], "repair": ["immediate", "jobs", "both"],
    "services": ["immediate", "appointments", "both"], "custom": ["custom"],
}


def features_for(kind, mode):
    result = ["checkout", "inventory"]
    if kind in ("cafe", "restaurant", "bakery") and mode in ("tables", "both"):
        result.append("tables")
    if kind in ("barbershop", "beauty", "services") and mode in ("appointments", "both"):
        result.append("appointments")
    if kind in ("barbershop", "beauty") and mode in ("walk_ins", "both"):
        result.append("walk_ins")
    if kind == "repair" and mode in ("jobs", "both"):
        result.append("jobs")
    return result


class SetupInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    business_type: BusinessType
    operation_mode: str
    features: list[Literal["checkout", "inventory", "tables", "appointments", "walk_ins", "jobs"]] = Field(default_factory=list)
    address: str = Field(default="", max_length=300)
    phone: str = Field(default="", max_length=40)
    logo_url: str = Field(default="", max_length=2048)
    receipt_footer: str = Field(default="Thank you for your visit!", max_length=300)
    table_count: int = Field(default=8, ge=1, le=50)
    catalog_action: Literal["keep", "samples", "empty"] = "keep"

    @field_validator("name")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Business name is required")
        return value.strip()

    @field_validator("logo_url")
    @classmethod
    def safe_logo(cls, value):
        value = value.strip()
        if value and not value.startswith("https://"):
            raise ValueError("Logo must be an https image URL")
        return value

    @model_validator(mode="after")
    def valid_mode(self):
        if self.operation_mode not in MODES[self.business_type]:
            raise ValueError("Choose a workflow available for this business type")
        return self


class ProfileInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    business_type: BusinessType


def catalog_fields(item, db):
    details = db.get(models.CatalogDetails, item.id)
    return {"category": details.category if details else "General",
            "item_type": details.item_type if details else "prepared",
            "sku": details.sku if details else ""}


def save_catalog_fields(item, payload, db):
    details = db.get(models.CatalogDetails, item.id)
    if details is None:
        details = models.CatalogDetails(menu_item_id=item.id)
        db.add(details)
    details.category = payload.category.strip() or "General"
    details.item_type = payload.item_type
    details.sku = payload.sku.strip()


def get_profile(db):
    profile = db.get(models.BusinessProfile, 1)
    config = db.get(models.BusinessConfiguration, 1)
    kind = profile.business_type if profile else "cafe"
    mode = config.operation_mode if config else "both"
    features = config.features.split(",") if config else ["checkout", "inventory", "tables"]
    if kind in ("cafe", "restaurant", "bakery"):
        order_types = ["takeaway"] if mode == "takeaway" else ["dine_in"] if mode == "tables" else ["dine_in", "takeaway"]
    elif kind in ("retail", "grocery"):
        order_types = [mode] if mode in ("in_store", "pickup") else ["in_store", "pickup"]
    elif kind == "custom":
        order_types = ["in_store", "pickup", *(["dine_in"] if "tables" in features else []), *(["service"] if any(x in features for x in ("appointments", "jobs", "walk_ins")) else [])]
    else:
        order_types = ["service"]
    return {"name": profile.name if profile else "SmartServe POS",
            "business_type": profile.business_type if profile else "cafe",
            "currency": "KRW", "operation_mode": config.operation_mode if config else "both",
            "features": features, "order_types": order_types,
            "address": config.address if config else "", "phone": config.phone if config else "",
            "logo_url": config.logo_url if config else "", "receipt_footer": config.receipt_footer if config else "Thank you for your visit!",
            "table_count": config.table_count if config else 8,
            "onboarding_complete": config.onboarding_complete if config else False}


@router.get("/business")
def business_profile(db: Session = Depends(get_db)):
    return get_profile(db)


@router.get("/business/presets")
def business_presets():
    return [{"id": key, "name": name, "description": description,
             "modes": MODES[key],
             "items": [{"name": item[0], "price": item[1], "category": item[2], "item_type": item[3]} for item in items]}
            for key, (name, description, items) in STARTERS.items()]


@router.put("/owner/business")
def update_business(payload: ProfileInput, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(422, "Business name is required")
    profile = db.scalar(select(models.BusinessProfile).where(models.BusinessProfile.id == 1).with_for_update())
    if profile is None:
        profile = models.BusinessProfile(id=1)
        db.add(profile)
    profile.name, profile.business_type = name, payload.business_type
    db.commit()
    return get_profile(db)


@router.post("/owner/business/presets/{preset_id}")
def apply_preset(preset_id: str, db: Session = Depends(get_db)):
    if preset_id not in STARTERS:
        raise HTTPException(404, "Business preset not found")
    # Startup creates this singleton so concurrent applications serialize on PostgreSQL.
    profile = db.scalar(select(models.BusinessProfile).where(models.BusinessProfile.id == 1).with_for_update())
    if profile is None:
        profile = models.BusinessProfile(id=1, name="SmartServe POS")
        db.add(profile)
        db.flush()
    added, skipped = add_starter_items(preset_id, db)
    profile.business_type = preset_id
    db.commit()
    return {"profile": get_profile(db), "added": added, "skipped": skipped}


def add_starter_items(preset_id, db):
    added, skipped = [], []
    for index, (name, price, category, kind, components) in enumerate(STARTERS[preset_id][2]):
        key = f"{preset_id}:{index}"
        if (db.scalar(select(models.CatalogDetails.menu_item_id).where(models.CatalogDetails.starter_key == key))
                or db.scalar(select(models.MenuItem.id).where(func.lower(models.MenuItem.name) == name.lower()))):
            skipped.append(name)
            continue
        item = models.MenuItem(name=name, price=price, active=True)
        db.add(item)
        db.flush()
        db.add(models.CatalogDetails(menu_item_id=item.id, category=category, item_type=kind,
                                    sku=f"{preset_id.upper()}-{index + 1:03d}" if kind == "product" else "", starter_key=key))
        for stock_name, unit, stock, usage in components:
            ingredient = db.scalar(select(models.Ingredient).where(func.lower(models.Ingredient.name) == stock_name.lower()))
            if ingredient is not None and (not ingredient.active or ingredient.unit != unit):
                db.rollback()
                raise HTTPException(409, f"Existing stock '{stock_name}' has a different unit or is archived. No starter changes were saved.")
            if ingredient is None:
                ingredient = models.Ingredient(name=stock_name, unit=unit, stock_quantity=stock, reorder_level=usage * 5, active=True)
                db.add(ingredient)
                db.flush()
            db.add(models.RecipeItem(menu_item_id=item.id, ingredient_id=ingredient.id, quantity=usage))
        added.append(name)
    return added, skipped


@router.post("/owner/business/setup")
def complete_setup(payload: SetupInput, db: Session = Depends(get_db)):
    profile = db.scalar(select(models.BusinessProfile).where(models.BusinessProfile.id == 1).with_for_update())
    if profile is None:
        profile = models.BusinessProfile(id=1)
        db.add(profile)
        db.flush()
    config = db.get(models.BusinessConfiguration, 1)
    features = list(dict.fromkeys(["checkout", *(payload.features if payload.business_type == "custom" else features_for(payload.business_type, payload.operation_mode))]))
    # Reconfiguration never orphans an unpaid bill or an unfinished appointment/job.
    if db.scalar(select(models.Order.id).where(models.Order.status == "open").limit(1)):
        raise HTTPException(409, "Pay or cancel open orders before changing the business setup")
    for feature, kinds in (("appointments", ["appointment"]), ("jobs", ["job"]), ("walk_ins", ["walk_in"])):
        if feature not in features and db.scalar(select(models.WorkTicket.id).where(models.WorkTicket.kind.in_(kinds), models.WorkTicket.status.notin_(["completed", "cancelled"])).limit(1)):
            raise HTTPException(409, f"Complete or cancel existing {feature.replace('_', ' ')} before disabling that workflow")
    if config is None:
        config = models.BusinessConfiguration(id=1)
        db.add(config)
    if payload.catalog_action != "keep":
        for item in db.scalars(select(models.MenuItem).where(models.MenuItem.active.is_(True))):
            item.active = False
        db.flush()
    added, skipped = [], []
    if payload.catalog_action == "samples":
        # Reactivate previously used starters without changing their price or stock.
        for details in db.scalars(select(models.CatalogDetails).where(models.CatalogDetails.starter_key.like(f"{payload.business_type}:%"))):
            db.get(models.MenuItem, details.menu_item_id).active = True
        added, skipped = add_starter_items(payload.business_type, db)
    profile.name, profile.business_type = payload.name, payload.business_type
    config.operation_mode, config.features = payload.operation_mode, ",".join(features)
    config.address, config.phone = payload.address.strip(), payload.phone.strip()
    config.logo_url, config.receipt_footer = payload.logo_url, payload.receipt_footer.strip()
    config.table_count, config.onboarding_complete = payload.table_count, True
    db.commit()
    return {"profile": get_profile(db), "added": added, "skipped": skipped}
