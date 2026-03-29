from fastapi import APIRouter, Depends, status

from app.api.deps import get_season_service
from app.application.dto.season import SeasonCreateDTO, SeasonResponseDTO, SeasonUpdateDTO
from app.application.services.season_service import SeasonService

router = APIRouter(prefix="/seasons", tags=["seasons"])

@router.get("/", response_model=list[SeasonResponseDTO])
async def list_seasons(service: SeasonService = Depends(get_season_service)) -> list[SeasonResponseDTO]:
    return await service.list()

@router.get("/{code}", response_model=SeasonResponseDTO)
async def get_season(code: str, service: SeasonService = Depends(get_season_service)) -> SeasonResponseDTO:
    return await service.get_by_code(code)

@router.post("/", response_model=SeasonResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_season(dto: SeasonCreateDTO, service: SeasonService = Depends(get_season_service)) -> SeasonResponseDTO:
    return await service.create(dto)

@router.patch("/{code}", response_model=SeasonResponseDTO)
async def update_season(code: str, dto: SeasonUpdateDTO, service: SeasonService=Depends(get_season_service)) -> SeasonResponseDTO:
    return await service.update(code, dto)

@router.delete("/{code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_season(code: str, service: SeasonService = Depends(get_season_service)) -> None:
    await service.delete(code)