import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..core.security import require_roles
from ..models.integration import IntegrationEvent
from ..models.settings import Setting
from ..schemas.settings import SettingsPayload
from ..services.integrations.bol import BolSettings as BolServiceSettings, test_connection as bol_test_connection
from ..services.integrations.shopify import ShopifySettings as ShopifyServiceSettings, test_connection as shopify_test_connection

router = APIRouter(prefix="/integrations", tags=["integrations"], dependencies=[Depends(require_roles("admin", "ops"))])


async def _load_settings(db: AsyncSession) -> SettingsPayload:
    result = await db.execute(select(Setting).where(Setting.key == "core"))
    setting = result.scalar_one_or_none()
    if not setting:
        raise HTTPException(status_code=404, detail="Core settings missing")
    return SettingsPayload.model_validate_json(setting.value)


@router.post("/shopify/test")
async def shopify_test(db: AsyncSession = Depends(get_db)):
    settings = await _load_settings(db)
    shopify = settings.integrations.shopify
    return await shopify_test_connection(
        ShopifyServiceSettings(
            store=shopify.store or "",
            api_key=shopify.api_key or "",
            api_secret=shopify.api_secret or "",
            access_token=shopify.access_token or "",
            webhook_secret=shopify.webhook_secret or "",
        )
    )


@router.post("/bol/test")
async def bol_test(db: AsyncSession = Depends(get_db)):
    settings = await _load_settings(db)
    bol = settings.integrations.bol
    return await bol_test_connection(
        BolServiceSettings(
            api_base=bol.api_base,
            client_id=bol.client_id or "",
            client_secret=bol.client_secret or "",
            webhook_secret=bol.webhook_secret or "",
        )
    )


@router.get("/events")
async def integration_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(IntegrationEvent).order_by(IntegrationEvent.created_at.desc()).limit(200))
    events = result.scalars().all()
    return [
        {
            "id": event.id,
            "source": event.source,
            "topic": event.topic,
            "status": event.status,
            "attempts": event.attempts,
            "error_message": event.error_message,
            "created_at": event.created_at,
        }
        for event in events
    ]
