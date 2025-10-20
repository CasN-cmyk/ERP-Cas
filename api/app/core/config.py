from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    app_name: str = "Cas Commerce ERP"
    database_url: str = Field("sqlite+aiosqlite:///./erp.db")
    secret_key: str = Field("super-secret-key")
    access_token_expire_minutes: int = Field(60 * 24)
    algorithm: str = "HS256"
    environment: str = Field("development")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    log_level: str = Field("INFO")
    default_locale: str = Field("nl")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
