from app.application.dto.competition import CompetitionCreateDTO, CompetitionResponseDTO, CompetitionUpdateDTO
from app.application.unit_of_work import UnitOfWork
from app.domain.exceptions import ConflictError, NotFoundError
from app.infrastructure.db.models.competition import Competition

class CompetitionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_by_id(self, competition_id: int) -> CompetitionResponseDTO:
        async with self.uow:
            competition = await self.uow.competitions.get_by_id(competition_id)
            if not competition:
                raise NotFoundError(f"Competition with id '{competition_id}' not found", competition_id)
            return CompetitionResponseDTO.model_validate(competition)
        
    async def get_by_code(self, code: str) -> CompetitionResponseDTO:
        async with self.uow:
            competition = await self.uow.competitions.get_by_code(code)
            if not competition:
                raise NotFoundError(f"Competition with code '{code}' not found", code)
            return CompetitionResponseDTO.model_validate(competition)
        
    async def list(self, filters: dict) -> list[CompetitionResponseDTO]:
        async with self.uow:
            competitions = await self.uow.competitions.list(filters)
            return [CompetitionResponseDTO.model_validate(comp) for comp in competitions]
        
    async def create(self, dto: CompetitionCreateDTO) -> CompetitionResponseDTO:
        async with self.uow:
            existing = await self.uow.competitions.get_by_code(dto.code)
            if existing:
                raise ConflictError(f"Competition with code '{dto.code}' already exists", dto.code)
            competition = Competition(code=dto.code, name=dto.name, country_code=dto.country_code, level=dto.level, organizer=dto.organizer)
            saved = await self.uow.competitions.save(competition)
            return CompetitionResponseDTO.model_validate(saved)

    async def update(self, competition_id: int, dto: CompetitionUpdateDTO) -> CompetitionResponseDTO:
        async with self.uow:
            competition = await self.uow.competitions.get_by_id(competition_id)
            if not competition:
                raise NotFoundError(f"Competition with id '{competition_id}' not found", competition_id)
            if dto.name is not None:
                competition.name = dto.name
            if dto.country_code is not None:
                competition.country_code = dto.country_code
            if dto.level is not None:
                competition.level = dto.level
            if dto.organizer is not None:
                competition.organizer = dto.organizer
            saved = await self.uow.competitions.save(competition)
            return CompetitionResponseDTO.model_validate(saved)
        
    async def delete(self, competition_id: int) -> None:
        async with self.uow:
            competition = await self.uow.competitions.get_by_id(competition_id)
            if not competition:
                raise NotFoundError(f"Competition with id '{competition_id}' not found", competition_id)
            await self.uow.competitions.delete(competition_id)
                