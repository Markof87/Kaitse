from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_team_service
from app.application.dto.team import TeamCreateDTO, TeamResponseDTO, TeamUpdateDTO
from app.application.services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[TeamResponseDTO])
async def list_teams(
    name: str | None = Query(None),
    city: str | None = Query(None),
    service: TeamService = Depends(get_team_service)
) -> list[TeamResponseDTO]:
    filters = {}
    if name:
        filters["name"] = name
    if city:
        filters["city"] = city
    return await service.list(filters)

@router.get("/{team_id}", response_model=TeamResponseDTO)
async def get_team(team_id: UUID, service: TeamService = Depends(get_team_service)) -> TeamResponseDTO:
    return await service.get_by_id(team_id)

@router.post("/", response_model=TeamResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_team(dto: TeamCreateDTO, service: TeamService = Depends(get_team_service)) -> TeamResponseDTO:
    return await service.create(dto)

@router.patch("/{team_id}", response_model=TeamResponseDTO)
async def update_team(team_id: UUID, dto: TeamUpdateDTO, service: TeamService = Depends(get_team_service)) -> TeamResponseDTO:
    return await service.update(team_id, dto)

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: UUID, service: TeamService = Depends(get_team_service)) -> None:
    await service.delete(team_id)