from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_player_service
from app.application.dto.player import PlayerCreateDTO, PlayerFiltersDTO, PlayerNationalityAddDTO, PlayerPositionAddDTO, PlayerResponseDTO, PlayerUpdateDTO
from app.application.services.player_service import PlayerService

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=list[PlayerResponseDTO])
async def list_players(name: str | None = Query(None), preferred_foot: str | None = Query(None), service: PlayerService = Depends(get_player_service)) -> list[PlayerResponseDTO]:
    filters = PlayerFiltersDTO(name=name, preferred_foot=preferred_foot)
    return await service.list(filters)

@router.get("/{player_id}", response_model=PlayerResponseDTO)
async def get_player(player_id: UUID, service: PlayerService = Depends(get_player_service)) -> PlayerResponseDTO:
    return await service.get_by_id(player_id)

@router.get("/slug/{slug}", response_model=PlayerResponseDTO)
async def get_player_by_slug(slug: str, service: PlayerService = Depends(get_player_service)) -> PlayerResponseDTO:
    return await service.get_by_slug(slug)

@router.post("/", response_model=PlayerResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_player(dto: PlayerCreateDTO, service: PlayerService = Depends(get_player_service)) -> PlayerResponseDTO:
    return await service.create(dto)

@router.patch("/{player_id}", response_model=PlayerResponseDTO)
async def update_player(player_id: UUID, dto: PlayerUpdateDTO, service: PlayerService = Depends(get_player_service)) -> PlayerResponseDTO:
    return await service.update(player_id, dto)

@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: UUID, service: PlayerService = Depends(get_player_service)) -> None:
    await service.delete(player_id)

#Positions
@router.post("/{player_id}/positions", status_code=status.HTTP_204_NO_CONTENT, tags=["player-associations"])
async def add_player_position(player_id: UUID, dto: PlayerPositionAddDTO, service: PlayerService = Depends(get_player_service)) -> None:
    await service.add_position(player_id, dto)

@router.delete("/{player_id}/positions/{position_code}", status_code=status.HTTP_204_NO_CONTENT, tags=["player-associations"])
async def remove_position(player_id: UUID, position_code: str, service: PlayerService = Depends(get_player_service)) -> None:
    await service.remove_position(player_id, position_code)

#Nationalities
@router.post("/{player_id}/nationalities", status_code=status.HTTP_204_NO_CONTENT, tags=["player-associations"])
async def add_player_nationality(player_id: UUID, dto: PlayerNationalityAddDTO, service: PlayerService = Depends(get_player_service)) -> None:
    await service.add_nationality(player_id, dto)