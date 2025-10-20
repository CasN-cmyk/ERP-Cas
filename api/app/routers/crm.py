from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..models.crm import CRMActivity, CRMDeal, CRMLead
from ..schemas.crm import CRMActivityCreate, CRMActivityRead, CRMDealCreate, CRMDealRead, CRMLeadCreate, CRMLeadRead

router = APIRouter(prefix="/crm", tags=["crm"], dependencies=[Depends(require_roles("admin", "support"))])


@router.get("/leads", response_model=list[CRMLeadRead])
async def list_leads(db: AsyncSession = Depends(get_db)) -> list[CRMLeadRead]:
    result = await db.execute(select(CRMLead))
    return result.scalars().all()


@router.post("/leads", response_model=CRMLeadRead)
async def create_lead(payload: CRMLeadCreate, db: AsyncSession = Depends(get_db)) -> CRMLeadRead:
    lead = CRMLead(**payload.dict())
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.get("/deals", response_model=list[CRMDealRead])
async def list_deals(db: AsyncSession = Depends(get_db)) -> list[CRMDealRead]:
    result = await db.execute(select(CRMDeal))
    return result.scalars().all()


@router.post("/deals", response_model=CRMDealRead)
async def create_deal(payload: CRMDealCreate, db: AsyncSession = Depends(get_db)) -> CRMDealRead:
    deal = CRMDeal(**payload.dict())
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    return deal


@router.get("/activities", response_model=list[CRMActivityRead])
async def list_activities(db: AsyncSession = Depends(get_db)) -> list[CRMActivityRead]:
    result = await db.execute(select(CRMActivity))
    return result.scalars().all()


@router.post("/activities", response_model=CRMActivityRead)
async def create_activity(payload: CRMActivityCreate, db: AsyncSession = Depends(get_db)) -> CRMActivityRead:
    activity = CRMActivity(**payload.dict())
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity
