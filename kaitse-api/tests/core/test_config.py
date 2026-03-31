import os
import pytest
from app.core.config import Settings

def test_settings_load_from_env():
    # Set environment variables for testing
    os.environ["APP_ENV"] = "test"
    os.environ["APP_NAME"] = "Kaitse API Test"
    os.environ["DEBUG"] = "False"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://test:test@localhost/test"
    os.environ["DATABASE_URL_SYNC"] = "postgresql://test:test@localhost/test"

    # Reload settings to pick up new environment variables
    settings = Settings()

    assert settings.app_env == "test"
    assert settings.app_name == "Kaitse API Test"
    assert settings.debug is False
    assert settings.database_url == "postgresql+asyncpg://test:test@localhost/test"
    assert settings.database_url_sync == "postgresql://test:test@localhost/test"

def test_settings_have_required_fields():
    settings = Settings()

    assert hasattr(settings, "app_env")
    assert hasattr(settings, "app_name")
    assert hasattr(settings, "debug")
    assert hasattr(settings, "database_url")
    assert hasattr(settings, "database_url_sync")