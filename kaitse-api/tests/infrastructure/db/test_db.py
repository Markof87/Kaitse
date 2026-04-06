import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

@pytest.mark.asyncio
async def test_async_session_creation():
    async with AsyncSessionLocal() as session:
        assert isinstance(session, AsyncSession)
        assert session is not None

@pytest.mark.asyncio
async def test_unit_of_work_creation():
    async with SqlAlchemyUnitOfWork(AsyncSessionLocal) as uow:
        assert uow is not None
        assert hasattr(uow, "players")  # Assuming you have a players repository in your unit of work
        assert hasattr(uow, "teams")
        assert hasattr(uow, "competitions")