"""Application settings for AssetFlow.

The settings layer uses pydantic-settings so values can be sourced from the
environment and optionally from a local .env file during development.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed runtime settings for the AssetFlow backend."""

    project_name: str = Field(default="AssetFlow", alias="PROJECT_NAME")
    version: str = Field(default="0.1.0", alias="VERSION")
    database_url: str = Field(
        default="postgresql://postgres:password@localhost:5432/assetflow",
        alias="DATABASE_URL",
    )
    secret_key: str = Field(default="change-me-in-production", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    backend_cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="BACKEND_CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        """Convert environment input into a list of allowed CORS origins."""

        if value is None or value == "":
            return ["http://localhost:5173", "http://127.0.0.1:5173"]

        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        if isinstance(value, str):
            value = value.strip()
            if not value:
                return ["http://localhost:5173", "http://127.0.0.1:5173"]

            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                parsed = [item.strip() for item in value.split(",")]

            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]

        raise ValueError("BACKEND_CORS_ORIGINS must be a list or comma-separated string")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()
