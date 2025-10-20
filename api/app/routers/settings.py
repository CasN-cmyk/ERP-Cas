import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..models.settings import Setting
from ..schemas.settings import SettingsPayload

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/{key}")
async def get_setting(key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Setting).where(Setting.key == key))
    setting = result.scalar_one_or_none()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": key, "value": json.loads(setting.value)}


@router.post("/{key}", dependencies=[Depends(require_roles("admin"))])
async def upsert_setting(key: str, payload: SettingsPayload, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Setting).where(Setting.key == key))
    setting = result.scalar_one_or_none()
    if setting is None:
        setting = Setting(key=key, value=payload.json())
        db.add(setting)
    else:
        setting.value = payload.json()
    await db.commit()
    return {"key": key, "value": payload.dict()}
