from collections.abc import AsyncGenerator
import ssl
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

CA_PATH = Path(__file__).with_name("certs") / "ca-certificate.crt"

ssl_context = ssl.create_default_context(cafile=str(CA_PATH))

# Database session management
# echo=True enables SQL query logging, 
# pool_pre_ping=True ensures connections are alive before using them
engine = create_async_engine(settings.database_url, echo=settings.debug, pool_pre_ping=True, connect_args={"ssl": ssl_context})

# sessionmaker factory for creating new database sessions, configured to not autocommit or autoflush, 
# and to not expire objects on commit
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a new database session for each request."""
    async with AsyncSessionLocal() as session:
        yield session

def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    Returns session factory, used to create SqlAlchemyUnitOfWork
    """
    return AsyncSessionLocal