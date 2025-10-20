from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    kind: str
    street: str
    zip: str
    city: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CustomerBase(BaseModel):
    external_id: Optional[str] = None
    source: str = "internal"
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    addresses: list[AddressCreate] = []


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    addresses: list[AddressRead] = []
