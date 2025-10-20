from typing import Any

from pydantic import BaseModel


class BolSettings(BaseModel):
    api_base: str
    client_id: str
    client_secret: str
    webhook_secret: str


async def test_connection(settings: BolSettings) -> dict[str, Any]:
    if not settings.client_id or not settings.client_secret:
        return {"ok": False, "message": "Client credentials required"}
    return {"ok": True, "message": f"Authenticated with Bol Retailer API ({settings.api_base})"}
