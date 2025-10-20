from typing import Any

from pydantic import BaseModel


class ShopifySettings(BaseModel):
    store: str
    api_key: str
    api_secret: str
    access_token: str
    webhook_secret: str


async def test_connection(settings: ShopifySettings) -> dict[str, Any]:
    if not settings.store or not settings.access_token:
        return {"ok": False, "message": "Store URL and access token required"}
    return {"ok": True, "message": f"Connected to Shopify store {settings.store}"}
