from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_player_stats_service
from app.application.dto.player_stats import PlayerStatsResponseDTO, PlayerStatsUpsertDTO
from app.application.services.player_stats_service import PlayerStatsService

router = APIRouter(prefix="/player-stats", tags=["player-stats"])

@router.get("/{stats_id}", response_model=PlayerStatsResponseDTO)
async def get_stats(
    stats_id: UUID,
    service: PlayerStatsService = Depends(get_player_stats_service)
) -> PlayerStatsResponseDTO:
    return await service.get_by_id(stats_id)

@router.get("/player/{player_id}", response_model=list[PlayerStatsResponseDTO])
async def get_stats_by_player(
    player_id: UUID,
    season_code: str | None = Query(None),
    service: PlayerStatsService = Depends(get_player_stats_service)
) -> list[PlayerStatsResponseDTO]:
    return await service.get_by_player(player_id, season_code)

@router.get("/team/{team_id}", response_model=list[PlayerStatsResponseDTO])
async def get_stats_by_team(
    team_id: UUID,
    season_code: str | None = Query(None),
    service: PlayerStatsService = Depends(get_player_stats_service)
) -> list[PlayerStatsResponseDTO]:
    return await service.get_by_team(team_id, season_code)

@router.post("/upsert", response_model=PlayerStatsResponseDTO)
async def upsert_stats(
    dto: PlayerStatsUpsertDTO,
    service: PlayerStatsService = Depends(get_player_stats_service)
) -> PlayerStatsResponseDTO:
    return await service.upsert(dto)

@router.post("/bulk-upsert", status_code=status.HTTP_200_OK)
async def bulk_upsert_stats(
    dtos: list[PlayerStatsUpsertDTO],
    service: PlayerStatsService = Depends(get_player_stats_service)
) -> dict[str, int]:
    count = await service.bulk_upsert(dtos)
    return {"processed": count}