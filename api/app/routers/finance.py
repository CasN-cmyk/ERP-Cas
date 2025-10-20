from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..services import finance

router = APIRouter(prefix="/reports", tags=["finance"], dependencies=[Depends(require_roles("admin", "ops"))])


def parse_date(value: str | None) -> date | None:
    if value:
        return date.fromisoformat(value)
    return None


@router.get("/kpis")
async def get_kpis(from_date: str | None = Query(None), to_date: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await finance.kpis(db, from_date=parse_date(from_date), to_date=parse_date(to_date))


@router.get("/sales")
async def get_sales(
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    group_by: str = Query("day", pattern="^(day|month)$"),
    db: AsyncSession = Depends(get_db),
):
    return await finance.sales(db, from_date=parse_date(from_date), to_date=parse_date(to_date), group_by=group_by)


@router.get("/margin")
async def get_margin(from_date: str | None = Query(None), to_date: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    kpi = await finance.kpis(db, from_date=parse_date(from_date), to_date=parse_date(to_date))
    return {"margin": kpi["margin"], "margin_pct": kpi["margin_pct"]}


@router.get("/vat")
async def get_vat(from_date: str | None = Query(None), to_date: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await finance.vat_report(db, from_date=parse_date(from_date), to_date=parse_date(to_date))


@router.get("/inventory/value")
async def inventory_value(db: AsyncSession = Depends(get_db)):
    return await finance.inventory_value(db)


@router.get("/top-products")
async def top_products(db: AsyncSession = Depends(get_db)):
    return await finance.top_products(db)


@router.get("/top-customers")
async def top_customers(db: AsyncSession = Depends(get_db)):
    return await finance.top_customers(db)


@router.get("/returns")
async def returns(from_date: str | None = Query(None), to_date: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await finance.returns(db, from_date=parse_date(from_date), to_date=parse_date(to_date))


@router.get("/stock-turn")
async def stock_turn(from_date: str | None = Query(None), to_date: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await finance.stock_turn(db, from_date=parse_date(from_date), to_date=parse_date(to_date))


@router.get("/coverage")
async def coverage(db: AsyncSession = Depends(get_db)):
    return await finance.coverage(db)
