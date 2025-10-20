from typing import Any
from pydantic import BaseModel, ConfigDict, HttpUrl


class BrandSettings(BaseModel):
    primary: str = "#2563eb"
    secondary: str = "#1e293b"
    logo_url: HttpUrl | None = None


class CompanyAddress(BaseModel):
    street: str
    zip: str
    city: str
    country: str


class InvoiceSettings(BaseModel):
    number_pattern: str = "INV-{YYYY}-{SEQ5}"
    footer: str = "Bedankt voor uw bestelling!"
    default_tax_rate: int = 21


class CompanySettings(BaseModel):
    name: str
    kvk: str
    vat_id: str
    iban: str
    email: str
    phone: str
    address: CompanyAddress
    invoice: InvoiceSettings


class ShopifySettings(BaseModel):
    enabled: bool = False
    store: str | None = None
    api_key: str | None = None
    api_secret: str | None = None
    access_token: str | None = None
    webhook_secret: str | None = None


class BolSettings(BaseModel):
    enabled: bool = False
    client_id: str | None = None
    client_secret: str | None = None
    api_base: str = "https://api.bol.com/retailer"
    webhook_secret: str | None = None


class IntegrationsSettings(BaseModel):
    shopify: ShopifySettings
    bol: BolSettings


class SettingsPayload(BaseModel):
    brand: BrandSettings
    company: CompanySettings
    integrations: IntegrationsSettings


class SettingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: SettingsPayload | dict[str, Any]
