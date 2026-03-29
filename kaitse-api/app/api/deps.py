from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.services.competition_service import CompetitionService
from app.application.services.team_service import TeamService
from app.application.services.season_service import SeasonService
from app.application.services.player_service import PlayerService
from app.application.services.player_stats_service import PlayerStatsService

from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

def get_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(AsyncSessionLocal)

def get_player_service(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> PlayerService:
    return PlayerService(uow)

def get_team_service(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> TeamService:
    return TeamService(uow)

def get_competition_service(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> CompetitionService:
    return CompetitionService(uow)

def get_season_service(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> SeasonService:
    return SeasonService(uow)

def get_player_stats_service(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> PlayerStatsService:
    return PlayerStatsService(uow)