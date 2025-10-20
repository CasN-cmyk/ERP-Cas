from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderLineBase(BaseModel):
    product_id: Optional[int]
    sku: str
    name: str
    qty: int
    unit_price_ex: float
    tax_rate: float = 21
    discount_ex: float = 0


class OrderLineCreate(OrderLineBase):
    pass


class OrderLineRead(OrderLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    line_total_ex: float
    avg_cost_at_fulfill: Optional[float]


class PaymentBase(BaseModel):
    method: str
    amount: float
    currency: str = "EUR"
    paid_at: Optional[datetime] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class InvoiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    pdf_url: Optional[str]
    issued_at: Optional[datetime]
    due_at: Optional[datetime]
    totals_ex: float
    tax_total: float
    grand_total: float


class OrderBase(BaseModel):
    external_id: Optional[str] = None
    source: Optional[str] = None
    status: str = "new"
    customer_id: Optional[int] = None
    billing_id: Optional[int] = None
    shipping_id: Optional[int] = None
    currency: str = "EUR"
    subtotal_ex: float = 0
    discount_ex: float = 0
    tax_total: float = 0
    shipping_ex: float = 0
    grand_total: float = 0


class OrderCreate(OrderBase):
    lines: list[OrderLineCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    discount_ex: Optional[float] = None
    tax_total: Optional[float] = None
    shipping_ex: Optional[float] = None
    grand_total: Optional[float] = None


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    lines: list[OrderLineRead] = []
    payments: list[PaymentRead] = []
    invoice: Optional[InvoiceRead] = None
