import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from app.infrastructure.db.session import get_async_session

#Fixture that returns asyncrone client HTTP for testing the API
@pytest.fixture
async def client():
    #Test client for making request to the API
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

#Fixture for testing database
@pytest.fixture
async def test_db_session():
    #Create a test database session
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_delete=False)

    async with test_engine.begin() as conn:
        #Create tables (skip this if you use Alembic for migrations)
        pass

    async with async_session() as session:
        yield session