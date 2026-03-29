from uuid import UUID

from app.application.dto.team import TeamCreateDTO, TeamResponseDTO, TeamUpdateDTO
from app.application.unit_of_work import UnitOfWork
from app.domain.exceptions import ConflictError, NotFoundError
from app.infrastructure.db.models.team import Team

class TeamService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_by_id(self, team_id: UUID) -> TeamResponseDTO:
        async with self.uow:
            team = await self.uow.teams.get_by_id(team_id)
            if not team:
                raise NotFoundError(f"Team with id '{team_id}' not found", team_id)
            return TeamResponseDTO.model_validate(team)
        
    async def list(self, filters: dict) -> list[TeamResponseDTO]:
        async with self.uow:
            teams = await self.uow.teams.list(filters)
            return [TeamResponseDTO.model_validate(team) for team in teams]
        
    async def create(self, dto: TeamCreateDTO) -> TeamResponseDTO:
        async with self.uow:
            if dto.tm_team_id is not None:
                existing = await self.uow.teams.get_by_tm_team_id(dto.tm_team_id)
                if existing:
                    raise ConflictError(f"Team with tm_team_id '{dto.tm_team_id}' already exists", dto.tm_team_id)
            team = Team(name=dto.name, tm_team_id=dto.tm_team_id, city=dto.city, image_path=dto.image_path)
            saved = await self.uow.teams.save(team)
            return TeamResponseDTO.model_validate(saved)

    async def update(self, team_id: UUID, dto: TeamUpdateDTO) -> TeamResponseDTO:
        async with self.uow:
            team = await self.uow.teams.get_by_id(team_id)
            if not team:
                raise NotFoundError(f"Team with id '{team_id}' not found", team_id)
            if dto.name is not None:
                team.name = dto.name
            if dto.tm_team_id is not None:
                team.tm_team_id = dto.tm_team_id
            if dto.city is not None:
                team.city = dto.city
            if dto.image_path is not None:
                team.image_path = dto.image_path
            saved = await self.uow.teams.save(team)
            return TeamResponseDTO.model_validate(saved)
        
    async def delete(self, team_id: UUID) -> None:
        async with self.uow:
            team = await self.uow.teams.get_by_id(team_id)
            if not team:
                raise NotFoundError(f"Team with id '{team_id}' not found", team_id)
            await self.uow.teams.delete(team_id)