from uuid import UUID

from app.application.dto.player_stats import PlayerStatsCreateDTO, PlayerStatsFilterDTO, PlayerStatsUpsertDTO, PlayerStatsResponseDTO
from app.application.unit_of_work import UnitOfWork
from app.domain.exceptions import NotFoundError
from app.infrastructure.db.models.player_stats import PlayerStats

class PlayerStatsService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_by_id(self, stats_id: UUID) -> PlayerStatsResponseDTO:
        async with self.uow:
            stats = await self.uow.player_stats.get_by_id(stats_id)
            if not stats:
                raise NotFoundError(f"PlayerStats with id '{stats_id}' not found", stats_id)
            return PlayerStatsResponseDTO.model_validate(stats)
    
    async def get_by_player(self, player_id: UUID, season_code: str | None=None) -> list[PlayerStatsResponseDTO]:
        async with self.uow:
            stats = await self.uow.player_stats.get_by_player_and_season(player_id, season_code)
            if not stats:
                raise NotFoundError(f"PlayerStats for player_id '{player_id}' and season '{season_code}' not found", {"player_id": player_id, "season": season_code})
            return [PlayerStatsResponseDTO.model_validate(stat) for stat in stats]
        
    async def get_by_team(self, team_id: UUID, season_code: str | None=None) -> list[PlayerStatsResponseDTO]:
        async with self.uow:
            stats = await self.uow.player_stats.get_by_team(team_id, season_code)
            if not stats:
                raise NotFoundError(f"PlayerStats for team '{team_id}' and season '{season_code}' not found", {"team": team_id, "season": season_code})
            return [PlayerStatsResponseDTO.model_validate(stat) for stat in stats]

    async def upsert(self, dto: PlayerStatsUpsertDTO) -> PlayerStatsResponseDTO:
        async with self.uow:
            stats = PlayerStats(player_id=dto.player_id, 
                                team_id=dto.team_id, 
                                season_code=dto.season_code, 
                                source=dto.source,
                                minutes=dto.minutes, 
                                matches=dto.matches,
                                goals=dto.goals, 
                                assists=dto.assists,
                                metrics=dto.metrics
                            )
            saved = await self.uow.player_stats.upsert(stats)
            return PlayerStatsResponseDTO.model_validate(saved)
        
    async def bulk_upsert(self, dtos: list[PlayerStatsUpsertDTO]) -> int:
        async with self.uow:
            stats_list = [PlayerStats(player_id=dto.player_id, 
                                        team_id=dto.team_id, 
                                        season_code=dto.season_code, 
                                        source=dto.source,
                                        minutes=dto.minutes, 
                                        matches=dto.matches,
                                        goals=dto.goals, 
                                        assists=dto.assists,
                                        metrics=dto.metrics
                                    ) for dto in dtos]
            return await self.uow.player_stats.bulk_upsert(stats_list)