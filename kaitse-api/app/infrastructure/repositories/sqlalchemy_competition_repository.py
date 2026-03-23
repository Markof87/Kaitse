from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.competition import Competition

class SqlAlchemyCompetitionRepository:
    def __init__(self, session: AsyncSession)-> None:
        self.session = session

    async def get_competition_by_id(self, competition_id: int) -> Competition | None:
        return await self.session.get(Competition, competition_id)

    async def get_by_code(self, code: str) -> Competition | None:
        stmt = select(Competition).where(Competition.code == code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list(self, filters: dict) -> list[Competition]:
        stmt = select(Competition)
        if country:= filters.get("country_code"):
            stmt = stmt.where(Competition.country_code == country)
        if level:= filters.get("level"):
            stmt = stmt.where(Competition.level == level)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def save(self, competition: Competition) -> Competition:
        self.session.add(competition)
        await self.session.flush()  # Ensure the team is saved and has an ID if it's new
        await self.session.refresh(competition)  # Refresh the team instance to get any updated fields from the database
        return competition

    async def delete(self, competition_id: int) -> None:
        competition = await self.get_competition_by_id(competition_id)
        if competition:
            await self.session.delete(competition)
