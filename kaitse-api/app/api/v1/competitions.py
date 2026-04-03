from fastapi import APIRouter, Depends, Query, logger, status

from app.api.deps import get_competition_service
from app.application.dto.competition import CompetitionCreateDTO, CompetitionResponseDTO, CompetitionUpdateDTO
from app.application.services.competition_service import CompetitionService
from app.domain.exceptions import NotFoundError

router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.get("/", response_model=list[CompetitionResponseDTO])
async def list_competitions(country_code: str | None = Query(None), level: int | None = Query(None), service: CompetitionService = Depends(get_competition_service)) -> list[CompetitionResponseDTO]:
    filters = {}
    if country_code:
        filters["country_code"] = country_code
    if level:
        filters["level"] = level
    return await service.list(filters)

@router.get("/{competition_id}", response_model=CompetitionResponseDTO)
async def get_competition_by_id(competition_id: int, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    return await service.get_by_id(competition_id)

@router.get("/code/{code}", response_model=CompetitionResponseDTO)
async def get_competition_by_code(code: str, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    return await service.get_by_code(code)

@router.post("/", response_model=CompetitionResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_competition(dto: CompetitionCreateDTO, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    #If exists, update the existing competition with the same code, otherwise create a new one.
    try:
        existing = await service.get_by_code(dto.code)
    except NotFoundError:
        existing = None

    if existing:
        #Check if I need to update the existing competition with the new data, otherwise return the existing one.
        if existing.name != dto.name or existing.country_code != dto.country_code or existing.level != dto.level or existing.organizer != dto.organizer:
            logger.info(f"Updating existing competition: code={dto.code}")
            return await service.update(existing.id, dto)
        
        logger.info(f"Competition already exists with the same data: code={dto.code}")
        return existing
    
    logger.info(f"Creating new competition: code={dto.code}")
    return await service.create(dto)

@router.patch("/{competition_id}", response_model=CompetitionResponseDTO)
async def update_competition(competition_id: int, dto: CompetitionUpdateDTO, service: CompetitionService = Depends(get_competition_service)) -> CompetitionResponseDTO:
    return await service.update(competition_id, dto)

@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competition(competition_id: int, service: CompetitionService = Depends(get_competition_service)) -> None:
    await service.delete(competition_id)