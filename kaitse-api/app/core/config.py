from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Kaitse API"
    app_env: str ="development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    database_url: str
    database_url_sync: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    @field_validator('database_url_sync', mode='before')
    @classmethod
    def set_sync_url(cls, v, info):
        if v is None and 'database_url' in info.data:
            # convert asyncpg to psycopg2 for sync
            return info.data['database_url'].replace('asyncpg://', 'postgresql://')
        return v

settings = Settings()