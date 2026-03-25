from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.repositories.sqlalchemy_player_repository import (SQLAlchemyPlayerRepository,)
from app.infrastructure.repositories.sqlalchemy_team_repository import (SQLAlchemyTeamRepository,)
from app.infrastructure.repositories.sqlalchemy_competition_repository import (SqlAlchemyCompetitionRepository,)
from app.infrastructure.repositories.sqlalchemy_season_repository import (SqlAlchemySeasonRepository,)
from app.infrastructure.repositories.sqlalchemy_player_stats_repository import (SqlAlchemyPlayerStatsRepository,)

class SqlAlchemyUnitOfWork:
    """
    Concrete implementation of Unit Of Work with SQLAlchemy
    Manage DB lifecycle:
    -open session at context manager input
    -do commit if everything is okay
    -do rollback in case of exception
    -close session on exit
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self.session_factory()

        self.players = SQLAlchemyPlayerRepository(self.session)
        self.teams = SQLAlchemyTeamRepository(self.session)
        self.competitions = SqlAlchemyCompetitionRepository(self.session)
        self.seasons = SqlAlchemySeasonRepository(self.session)
        self.player_stats = SqlAlchemyPlayerStatsRepository(self.session)

        return self
    
    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        if exc_type is not None:
            await self.rollback() #Exception -> undo all
        else:
            await self.commit() #Ok -> confirm all
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
