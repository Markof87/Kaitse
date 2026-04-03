from typing import List

from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = Field("Kaitse API", alias="APP_NAME")
    app_env: str = Field("development", alias="APP_ENV")
    debug: bool = Field(True, alias="DEBUG")
    api_v1_prefix: str = Field("/api/v1", alias="API_V1_PREFIX")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    database_url: str = Field(..., alias="DATABASE_URL")
    database_url_sync: str | None = Field(None, alias="DATABASE_URL_SYNC")

    enable_docs: bool = Field(False, alias="ENABLE_DOCS")

    cors_allow_origins: List[str] = Field(default_factory=list, alias="CORS_ALLOW_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    @field_validator("database_url_sync", mode="before")
    @classmethod
    def set_sync_url(cls, v, info):
        if v is None and "database_url" in info.data:
            return info.data["database_url"].replace("postgresql+asyncpg://", "postgresql://")
        return v
    
    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def parse_cors_allow_origins(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        s = str(v).strip()
        if not s:
            return []
        if s == "*":
            return ["*"]
        # CSV
        return [item.strip() for item in s.split(",") if item.strip()]

settings = Settings()