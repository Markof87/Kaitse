from app.infrastructure.db.base import Base
from app.infrastructure.db.models import player_stats

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

@pytest.fixture
def app():
    from main import app as fastapi_app
    return fastapi_app

#Fixture that returns asyncrone client HTTP for testing the API
@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

#Fixture for testing database
@pytest.fixture
async def test_db_session():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    # Remove PlayerStats from metadata
    tables_to_drop = [t for t in Base.metadata.tables.values() if t.name == 'player_stats']
    for table in tables_to_drop:
        Base.metadata.remove(table)
    
    # Create all tables except player_stats
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(test_engine, class_=AsyncSession)
    
    async with async_session() as session:
        yield session
        
    await test_engine.dispose()