from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SupplierBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PurchaseOrderLineBase(BaseModel):
    product_id: int
    qty: int
    unit_cost_ex: float


class PurchaseOrderLineCreate(PurchaseOrderLineBase):
    pass


class PurchaseOrderLineRead(PurchaseOrderLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PurchaseOrderBase(BaseModel):
    supplier_id: int
    status: str = "draft"
    currency: str = "EUR"
    expected_at: Optional[datetime] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    lines: list[PurchaseOrderLineCreate]


class PurchaseOrderRead(PurchaseOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lines: list[PurchaseOrderLineRead] = []
