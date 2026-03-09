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

settings = Settings()