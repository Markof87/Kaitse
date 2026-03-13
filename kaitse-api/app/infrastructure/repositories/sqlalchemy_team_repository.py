from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.team import Team

class SQLAlchemyTeamRepository:
    def __init__(self, session: AsyncSession)-> None:
        self.session = session

    async def get_team_by_id(self, team_id: UUID) -> Team | None:
        return await self.session.get(Team, team_id)

    async def get_by_tm_id(self, tm_team_id: int) -> Team | None:
        stmt = select(Team).where(Team.tm_id == tm_team_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list(self, filters: dict) -> list[Team]:
        stmt = select(Team)
        if name:= filters.get("name"):
            stmt = stmt.where(Team.name.ilike(f"%{name}%"))
        if city:= filters.get("city"):
            stmt = stmt.where(Team.city.ilike(f"%{city}%"))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def save(self, team: Team) -> None:
        self.session.add(team)
        await self.session.flush()  # Ensure the team is saved and has an ID if it's new
        await self.session.refresh(team)  # Refresh the team instance to get any updated fields from the database
        return team

    async def delete(self, team_id: UUID) -> None:
        team = await self.get_team_by_id(team_id)
        if team:
            await self.session.delete(team)

    async def exists(self, team_id: UUID) -> bool:
        team = await self.get_team_by_id(team_id)
        return team is not None