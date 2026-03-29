from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_competition_service
from app.application.dto.competition import CompetitionCreateDTO, CompetitionResponseDTO, CompetitionUpdateDTO
from app.application.services.competition_service import CompetitionService

router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.get("/", response_model=list[CompetitionResponseDTO])
async def list_competitions(
    country_code: str | None = Query(None),
    level: int | None = Query(None),
    service: CompetitionService = Depends(get_competition_service)
) -> list[CompetitionResponseDTO]:
    filters = {}
    if country_code:
        filters["country_code"] = country_code
    if level:
        filters["level"] = level
    return await service.list(filters)

@router.get("/{competition_id}", response_model=CompetitionResponseDTO)
async def get_competition(competition_id: int, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    return await service.get_by_id(competition_id)

@router.post("/", response_model=CompetitionResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_competition(dto: CompetitionCreateDTO, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    return await service.create(dto)

@router.patch("/{competition_id}", response_model=CompetitionResponseDTO)
async def update_competition(competition_id: int, dto: CompetitionUpdateDTO, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    return await service.update(competition_id, dto)

@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competition(competition_id: int, service: CompetitionService = Depends(get_competition_service)) -> None:
    await service.delete(competition_id)