from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..models.product import Product
from ..models.purchase import PurchaseOrder, PurchaseOrderLine, Supplier
from ..schemas.purchase import PurchaseOrderCreate, PurchaseOrderRead, SupplierCreate, SupplierRead
from ..services.inventory import apply_inventory_movement

router = APIRouter(prefix="/purchase-orders", tags=["purchase"])


@router.get("/suppliers", response_model=list[SupplierRead])
async def list_suppliers(db: AsyncSession = Depends(get_db)) -> list[SupplierRead]:
    result = await db.execute(select(Supplier))
    return result.scalars().all()


@router.post("/suppliers", response_model=SupplierRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def create_supplier(payload: SupplierCreate, db: AsyncSession = Depends(get_db)) -> SupplierRead:
    supplier = Supplier(**payload.dict())
    db.add(supplier)
    await db.commit()
    await db.refresh(supplier)
    return supplier


@router.get("", response_model=list[PurchaseOrderRead])
async def list_purchase_orders(db: AsyncSession = Depends(get_db)) -> list[PurchaseOrderRead]:
    result = await db.execute(select(PurchaseOrder))
    return result.scalars().unique().all()


@router.post("", response_model=PurchaseOrderRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def create_purchase_order(payload: PurchaseOrderCreate, db: AsyncSession = Depends(get_db)) -> PurchaseOrderRead:
    purchase_order = PurchaseOrder(**payload.dict(exclude={"lines"}))
    db.add(purchase_order)
    for line in payload.lines:
        db.add(PurchaseOrderLine(purchase_order=purchase_order, **line.dict()))
    await db.commit()
    await db.refresh(purchase_order)
    return purchase_order


@router.post("/{po_id}/receive", response_model=PurchaseOrderRead, dependencies=[Depends(require_roles("admin", "ops"))])
async def receive_purchase_order(po_id: int, db: AsyncSession = Depends(get_db)) -> PurchaseOrderRead:
    purchase_order = await db.get(PurchaseOrder, po_id)
    if not purchase_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    purchase_order.status = "received"
    for line in purchase_order.lines:
        await apply_inventory_movement(db, product_id=line.product_id, movement_type="receipt", qty=line.qty, ref_type="purchase_order", ref_id=str(po_id))
    await db.commit()
    await db.refresh(purchase_order)
    return purchase_order
