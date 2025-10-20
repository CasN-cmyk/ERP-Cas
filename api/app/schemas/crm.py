from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CRMLeadBase(BaseModel):
    source: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    status: str = "new"
    owner_id: Optional[int] = None
    notes: Optional[str] = None


class CRMLeadCreate(CRMLeadBase):
    pass


class CRMLeadRead(CRMLeadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CRMDealBase(BaseModel):
    customer_id: Optional[int] = None
    title: str
    value_ex: float
    stage: str = "prospect"
    expected_close: Optional[datetime] = None
    owner_id: Optional[int] = None


class CRMDealCreate(CRMDealBase):
    pass


class CRMDealRead(CRMDealBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CRMActivityBase(BaseModel):
    deal_id: int
    type: str
    subject: str
    due_at: Optional[datetime] = None
    done_at: Optional[datetime] = None
    notes: Optional[str] = None


class CRMActivityCreate(CRMActivityBase):
    pass


class CRMActivityRead(CRMActivityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
