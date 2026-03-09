from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Database session management
# echo=True enables SQL query logging, 
# pool_pre_ping=True ensures connections are alive before using them
engine = create_engine(settings.database_url, echo=settings.debug, pool_pre_ping=True)

# sessionmaker factory for creating new database sessions, configured to not autocommit or autoflush, 
# and to not expire objects on commit
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a new database session for each request."""
    async with AsyncSessionLocal() as session:
        yield session