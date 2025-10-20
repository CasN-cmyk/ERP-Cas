from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PricePerChannelBase(BaseModel):
    channel: str
    price_ex: float
    currency: str = "EUR"
    active: bool = True


class PricePerChannelCreate(PricePerChannelBase):
    pass


class PricePerChannelRead(PricePerChannelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductBase(BaseModel):
    name: str
    sku: str
    ean: Optional[str] = None
    cost_price: float = 0
    default_tax_rate: float = 21
    status: str = "active"


class ProductCreate(ProductBase):
    prices: list[PricePerChannelCreate] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    ean: Optional[str] = None
    cost_price: Optional[float] = None
    default_tax_rate: Optional[float] = None
    status: Optional[str] = None


class InventoryCacheRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    on_hand: int
    reserved: int
    available: int


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    prices: list[PricePerChannelRead] = []
    inventory_cache: InventoryCacheRead | None = None
