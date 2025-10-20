from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..models.customer import Address, Customer
from ..schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[CustomerRead])
async def list_customers(db: AsyncSession = Depends(get_db), limit: int = Query(100, le=500)) -> list[CustomerRead]:
    result = await db.execute(select(Customer).limit(limit).order_by(Customer.created_at.desc()))
    return result.scalars().unique().all()


@router.post("", response_model=CustomerRead, dependencies=[Depends(require_roles("admin", "support", "ops"))])
async def create_customer(payload: CustomerCreate, db: AsyncSession = Depends(get_db)) -> CustomerRead:
    customer = Customer(**payload.dict(exclude={"addresses"}))
    db.add(customer)
    for address in payload.addresses:
        db.add(Address(customer=customer, **address.dict()))
    await db.commit()
    await db.refresh(customer)
    return customer


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db)) -> CustomerRead:
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerRead, dependencies=[Depends(require_roles("admin", "support", "ops"))])
async def update_customer(customer_id: int, payload: CustomerUpdate, db: AsyncSession = Depends(get_db)) -> CustomerRead:
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    await db.commit()
    await db.refresh(customer)
    return customer
