from datetime import date, datetime
from typing import Any, Iterable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Invoice, Order, OrderLine, Payment
from ..models.product import InventoryCache, Product


async def _date_filter(query, *, from_date: date | None = None, to_date: date | None = None, field=Order.created_at):
    if from_date:
        query = query.where(field >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.where(field <= datetime.combine(to_date, datetime.max.time()))
    return query


async def kpis(session: AsyncSession, *, from_date: date | None = None, to_date: date | None = None) -> dict[str, Any]:
    base_query = select(func.sum(Order.grand_total), func.sum(Order.tax_total), func.count(Order.id)).where(Order.status.in_(["paid", "fulfilled"]))
    base_query = await _date_filter(base_query, from_date=from_date, to_date=to_date)
    revenue, vat, order_count = (await session.execute(base_query)).one()

    cogs_query = select(func.sum(OrderLine.avg_cost_at_fulfill * OrderLine.qty)).join(Order, Order.id == OrderLine.order_id)
    cogs_query = await _date_filter(cogs_query, from_date=from_date, to_date=to_date, field=Order.updated_at)
    cogs = (await session.execute(cogs_query)).scalar() or 0

    customers_query = select(func.count(func.distinct(Order.customer_id))).where(Order.status.in_(["paid", "fulfilled"]))
    customers_query = await _date_filter(customers_query, from_date=from_date, to_date=to_date)
    customer_count = (await session.execute(customers_query)).scalar() or 0

    revenue = float(revenue or 0)
    vat = float(vat or 0)
    cogs = float(cogs or 0)
    margin = revenue - cogs
    margin_pct = (margin / revenue * 100) if revenue else 0
    avg_order_value = (revenue / order_count) if order_count else 0

    returns_query = select(func.count()).where(Order.status == "return")
    returns_query = await _date_filter(returns_query, from_date=from_date, to_date=to_date)
    returns_count = (await session.execute(returns_query)).scalar() or 0
    return_rate = (returns_count / order_count * 100) if order_count else 0

    open_payments_query = select(func.sum(Order.grand_total - func.coalesce(func.sum(Payment.amount), 0))).join(Payment, isouter=True).group_by(Order.id).where(Order.status.in_(["new", "paid"]))
    open_payments_query = await _date_filter(open_payments_query, from_date=from_date, to_date=to_date)
    open_payments_rows = await session.execute(open_payments_query)
    open_payments_total = sum(float(row[0] or 0) for row in open_payments_rows)

    inventory_value_query = select(func.sum(InventoryCache.on_hand * Product.cost_price)).join(Product, Product.id == InventoryCache.product_id)
    inventory_value = (await session.execute(inventory_value_query)).scalar() or 0

    return {
        "revenue_ex": revenue - vat,
        "vat_total": vat,
        "cogs": cogs,
        "margin": margin,
        "margin_pct": margin_pct,
        "avg_order_value": avg_order_value,
        "orders": order_count,
        "customers": customer_count,
        "return_rate": return_rate,
        "open_payments": open_payments_total,
        "inventory_value": float(inventory_value or 0),
    }


async def sales(session: AsyncSession, *, from_date: date | None = None, to_date: date | None = None, group_by: str = "day") -> list[dict[str, Any]]:
    trunc_func = {
        "day": func.strftime("%Y-%m-%d", Order.created_at),
        "month": func.strftime("%Y-%m", Order.created_at),
    }.get(group_by, func.strftime("%Y-%m-%d", Order.created_at))

    query = select(trunc_func.label("period"), func.sum(Order.grand_total).label("revenue"), func.sum(Order.tax_total).label("vat"), func.sum(Order.grand_total - Order.tax_total).label("net"))
    query = query.where(Order.status.in_(["paid", "fulfilled"]))
    query = query.group_by("period")
    query = await _date_filter(query, from_date=from_date, to_date=to_date)
    rows = await session.execute(query)
    return [
        {
            "period": row.period,
            "revenue": float(row.revenue or 0),
            "vat": float(row.vat or 0),
            "net": float(row.net or 0),
        }
        for row in rows
    ]


async def top_products(session: AsyncSession, limit: int = 10) -> list[dict[str, Any]]:
    query = (
        select(OrderLine.sku, OrderLine.name, func.sum(OrderLine.qty).label("qty"), func.sum(OrderLine.line_total_ex).label("revenue"))
        .group_by(OrderLine.sku, OrderLine.name)
        .order_by(func.sum(OrderLine.line_total_ex).desc())
        .limit(limit)
    )
    rows = await session.execute(query)
    return [
        {
            "sku": row.sku,
            "name": row.name,
            "qty": int(row.qty or 0),
            "revenue": float(row.revenue or 0),
        }
        for row in rows
    ]


async def top_customers(session: AsyncSession, limit: int = 10) -> list[dict[str, Any]]:
    query = (
        select(Order.customer_id, func.sum(Order.grand_total).label("revenue"), func.count(Order.id).label("orders"))
        .where(Order.customer_id.is_not(None))
        .group_by(Order.customer_id)
        .order_by(func.sum(Order.grand_total).desc())
        .limit(limit)
    )
    rows = await session.execute(query)
    results = []
    for customer_id, revenue, orders in rows:
        results.append({"customer_id": customer_id, "revenue": float(revenue or 0), "orders": int(orders or 0)})
    return results


async def vat_report(session: AsyncSession, *, from_date: date | None = None, to_date: date | None = None) -> list[dict[str, Any]]:
    query = select(OrderLine.tax_rate, func.sum(OrderLine.line_total_ex * (OrderLine.tax_rate / 100)).label("vat"))
    query = query.join(Order, Order.id == OrderLine.order_id)
    query = query.where(Order.status.in_(["paid", "fulfilled"]))
    query = query.group_by(OrderLine.tax_rate)
    query = await _date_filter(query, from_date=from_date, to_date=to_date)
    rows = await session.execute(query)
    return [{"tax_rate": float(row.tax_rate or 0), "vat": float(row.vat or 0)} for row in rows]


async def inventory_value(session: AsyncSession) -> dict[str, Any]:
    total_value = await session.execute(select(func.sum(InventoryCache.on_hand * Product.cost_price)))
    value = total_value.scalar() or 0
    return {"inventory_value": float(value)}


async def returns(session: AsyncSession, *, from_date: date | None = None, to_date: date | None = None) -> list[dict[str, Any]]:
    query = select(Order.id, Order.external_id, Order.grand_total, Order.updated_at).where(Order.status == "return")
    query = await _date_filter(query, from_date=from_date, to_date=to_date)
    rows = await session.execute(query)
    return [
        {
            "id": row.id,
            "external_id": row.external_id,
            "grand_total": float(row.grand_total or 0),
            "updated_at": row.updated_at,
        }
        for row in rows
    ]


async def stock_turn(session: AsyncSession, *, from_date: date | None = None, to_date: date | None = None) -> dict[str, Any]:
    cogs_query = select(func.sum(OrderLine.avg_cost_at_fulfill * OrderLine.qty)).join(Order, Order.id == OrderLine.order_id)
    cogs_query = await _date_filter(cogs_query, from_date=from_date, to_date=to_date, field=Order.updated_at)
    cogs = float((await session.execute(cogs_query)).scalar() or 0)

    inventory_value_query = select(func.avg(InventoryCache.on_hand * Product.cost_price))
    avg_inventory_value = float((await session.execute(inventory_value_query)).scalar() or 0)
    stock_turn_ratio = (cogs / avg_inventory_value) if avg_inventory_value else 0
    return {"stock_turn": stock_turn_ratio}


async def coverage(session: AsyncSession) -> dict[str, Any]:
    sales_velocity_query = (
        select(OrderLine.product_id, (func.sum(OrderLine.qty) / func.count(func.distinct(func.strftime("%Y-%m", Order.created_at))))).label("velocity")
        .join(Order, Order.id == OrderLine.order_id)
        .where(Order.status.in_(["paid", "fulfilled"]))
        .group_by(OrderLine.product_id)
    )
    velocity_rows = await session.execute(sales_velocity_query)
    coverage_map: dict[int, float] = {}
    for product_id, velocity in velocity_rows:
        cache = await session.get(InventoryCache, product_id)
        if cache:
            monthly_velocity = float(velocity or 0)
            daily_velocity = monthly_velocity / 30 if monthly_velocity else 0
            coverage_days = (cache.available / daily_velocity) if daily_velocity else None
            coverage_map[product_id] = coverage_days or 0
    return {"coverage_days": coverage_map}
