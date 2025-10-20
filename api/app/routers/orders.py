from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..models.order import Invoice, Order, OrderLine, Payment
from ..schemas.order import OrderCreate, OrderRead, OrderUpdate, PaymentCreate
from ..services.inventory import apply_inventory_movement, recalc_inventory_cache

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
async def list_orders(db: AsyncSession = Depends(get_db), limit: int = Query(100, le=200)) -> list[OrderRead]:
    result = await db.execute(select(Order).limit(limit).order_by(Order.created_at.desc()))
    return result.scalars().unique().all()


@router.post("", response_model=OrderRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def create_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)) -> OrderRead:
    order = Order(**payload.dict(exclude={"lines"}))
    db.add(order)
    for line in payload.lines:
        db.add(
            OrderLine(
                order=order,
                product_id=line.product_id,
                sku=line.sku,
                name=line.name,
                qty=line.qty,
                unit_price_ex=line.unit_price_ex,
                tax_rate=line.tax_rate,
                discount_ex=line.discount_ex,
                line_total_ex=(line.unit_price_ex * line.qty) - line.discount_ex,
            )
        )
        if line.product_id:
            await apply_inventory_movement(db, product_id=line.product_id, movement_type="reserve", qty=line.qty, ref_type="order", ref_id=str(order.id))
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)) -> OrderRead:
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}", response_model=OrderRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def update_order(order_id: int, payload: OrderUpdate, db: AsyncSession = Depends(get_db)) -> OrderRead:
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(order, field, value)
    await db.commit()
    await db.refresh(order)
    return order


@router.post("/{order_id}/payment", response_model=OrderRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def register_payment(order_id: int, payload: PaymentCreate, db: AsyncSession = Depends(get_db)) -> OrderRead:
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    payment = Payment(order=order, **payload.dict())
    db.add(payment)
    await db.commit()
    await db.refresh(order)
    return order


@router.post("/{order_id}/fulfill", response_model=OrderRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def fulfill_order(order_id: int, db: AsyncSession = Depends(get_db)) -> OrderRead:
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "fulfilled"
    for line in order.lines:
        if line.product_id:
            await apply_inventory_movement(db, product_id=line.product_id, movement_type="shipment", qty=line.qty, ref_type="order", ref_id=str(order.id))
            await recalc_inventory_cache(db, line.product_id)
    await db.commit()
    await db.refresh(order)
    return order
