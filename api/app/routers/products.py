from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.db import get_db
from ..core.security import get_current_active_user, require_roles
from ..models.product import InventoryMovementType, PricePerChannel, Product
from ..schemas.product import ProductCreate, ProductRead, ProductUpdate
from ..services.inventory import apply_inventory_movement
from ..services import audit

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
async def list_products(db: AsyncSession = Depends(get_db), limit: int = Query(100, le=200)) -> list[ProductRead]:
    result = await db.execute(select(Product).limit(limit))
    return result.scalars().unique().all()


@router.post("", response_model=ProductRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)) -> ProductRead:
    product = Product(
        name=payload.name,
        sku=payload.sku,
        ean=payload.ean,
        cost_price=payload.cost_price,
        default_tax_rate=payload.default_tax_rate,
        status=payload.status,
    )
    db.add(product)
    for price in payload.prices:
        db.add(
            PricePerChannel(
                product=product,
                channel=price.channel,
                price_ex=price.price_ex,
                currency=price.currency,
                active=price.active,
            )
        )
    await db.commit()
    await db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)) -> ProductRead:
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def update_product(product_id: int, payload: ProductUpdate, db: AsyncSession = Depends(get_db)) -> ProductRead:
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


@router.post("/{product_id}/adjust", response_model=ProductRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def adjust_inventory(product_id: int, qty: int, movement_type: InventoryMovementType, db: AsyncSession = Depends(get_db)) -> ProductRead:
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await apply_inventory_movement(db, product_id=product_id, movement_type=movement_type.value, qty=qty)
    await db.commit()
    await db.refresh(product)
    return product
