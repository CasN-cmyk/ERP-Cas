from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.product import InventoryCache, InventoryMovement, InventoryMovementType, Product


async def recalc_inventory_cache(session: AsyncSession, product_id: int) -> InventoryCache:
    totals = await session.execute(
        select(
            InventoryMovement.type,
            func.sum(InventoryMovement.qty).label("qty"),
        ).where(InventoryMovement.product_id == product_id).group_by(InventoryMovement.type)
    )
    qty_map = {row.type: row.qty or 0 for row in totals}
    receipts = qty_map.get(InventoryMovementType.RECEIPT.value, 0) + qty_map.get(InventoryMovementType.RETURN.value, 0)
    shipments = qty_map.get(InventoryMovementType.SHIPMENT.value, 0)
    adjustments = qty_map.get(InventoryMovementType.ADJUST.value, 0)
    reserves = qty_map.get(InventoryMovementType.RESERVE.value, 0)

    on_hand = receipts - shipments + adjustments
    reserved = reserves
    available = on_hand - reserved

    cache = await session.get(InventoryCache, product_id)
    if cache is None:
        cache = InventoryCache(product_id=product_id)
        session.add(cache)

    cache.on_hand = int(on_hand)
    cache.reserved = int(reserved)
    cache.available = int(available)
    return cache


async def apply_inventory_movement(session: AsyncSession, *, product_id: int, movement_type: str, qty: int, ref_type: str | None = None, ref_id: str | None = None) -> InventoryMovement:
    movement = InventoryMovement(
        product_id=product_id,
        type=movement_type,
        qty=qty,
        ref_type=ref_type,
        ref_id=ref_id,
    )
    session.add(movement)
    await recalc_inventory_cache(session, product_id)
    return movement
