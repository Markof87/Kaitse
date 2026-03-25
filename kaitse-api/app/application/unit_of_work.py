from typing import Protocol

from app.domain.repositories.player_repository import PlayerRepository
from app.domain.repositories.team_repository import TeamRepository
from app.domain.repositories.competition_repository import CompetitionRepository
from app.domain.repositories.season_repository import SeasonRepository
from app.domain.repositories.player_stats_repository import PlayerStatsRepository

class UnitOfWork(Protocol):
    """
    Contract of Unit of Work: defines which repositories are available and how to manage transactions.
    """

    players: PlayerRepository
    teams: TeamRepository
    competitions: CompetitionRepository
    seasons: SeasonRepository
    player_stats: PlayerStatsRepository

    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(self, *args: object) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

    