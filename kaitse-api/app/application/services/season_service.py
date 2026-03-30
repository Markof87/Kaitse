from app.application.dto.season import SeasonCreateDTO, SeasonResponseDTO, SeasonUpdateDTO
from app.application.unit_of_work import UnitOfWork
from app.domain.exceptions import ConflictError, NotFoundError
from app.infrastructure.db.models.season import Season

class SeasonService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_by_code(self, code: str) -> SeasonResponseDTO:
        async with self.uow:
            season = await self.uow.seasons.get_by_code(code)
            if not season:
                raise NotFoundError(f"Season with code '{code}' not found", code)
            return SeasonResponseDTO.model_validate(season)
    
    async def list(self) -> list[SeasonResponseDTO]:
        async with self.uow:
            seasons = await self.uow.seasons.list()
            return [SeasonResponseDTO.model_validate(season) for season in seasons]
        
    async def create(self, dto: SeasonCreateDTO) -> SeasonResponseDTO:
        async with self.uow:
            existing = await self.uow.seasons.get_by_code(dto.code)
            if existing:
                raise ConflictError(f"Season with code '{dto.code}' already exists", dto.code)
            season = Season(code=dto.code, start_date=dto.start_date, end_date=dto.end_date)
            saved = await self.uow.seasons.save(season)
            return SeasonResponseDTO.model_validate(saved)
    
    async def update(self, code: str, dto: SeasonUpdateDTO) -> SeasonResponseDTO:
        async with self.uow:
            season = await self.uow.seasons.get_by_code(code)
            if not season:
                raise NotFoundError(f"Season with code '{code}' not found", code)
            if dto.start_date is not None:
                season.start_date = dto.start_date
            if dto.end_date is not None:
                season.end_date = dto.end_date
            saved = await self.uow.seasons.save(season)
            return SeasonResponseDTO.model_validate(saved)
        
    async def delete(self, code: str) -> None:
        async with self.uow:
            season = await self.uow.seasons.get_by_code(code)
            if not season:
                raise NotFoundError(f"Season with code '{code}' not found", code)
            await self.uow.seasons.delete(code)