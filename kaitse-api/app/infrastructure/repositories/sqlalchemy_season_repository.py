from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.season import Season

class SqlAlchemySeasonRepository:
    def __init__(self, session: AsyncSession)-> None:
        self.session = session

    async def get_by_code(self, code: str) -> Season | None:
        return await self.session.get(Season, code)

    async def list(self) -> list[Season]:
        stmt = select(Season).order_by(Season.code.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def save(self, season: Season) -> Season:
        self.session.add(season)
        await self.session.flush()  # Ensure the team is saved and has an ID if it's new
        await self.session.refresh(season)  # Refresh the team instance to get any updated fields from the database
        return season

    async def delete(self, code: str) -> None:
        season = await self.get_by_code(code)
        if season:
            await self.session.delete(season)
