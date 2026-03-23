from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.player_stats import PlayerStats

class SqlAlchemyPlayerStatsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, stats_id: UUID) -> PlayerStats | None:
        return await self.session.get(PlayerStats, stats_id)
    
    async def get_by_player(self, player_id: UUID, season_code: str | None = None, ) -> list[PlayerStats]:
        stmt = select(PlayerStats).where(PlayerStats.player_id == player_id)
        if season_code:
            stmt = stmt.where(PlayerStats.season_code == season_code)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_team(self, team_id: UUID, season_code: str | None = None, )-> list[PlayerStats]:
        stmt = select(PlayerStats).where(PlayerStats.team_id == team_id)
        if season_code:
            stmt = stmt.where(PlayerStats.season_code == season_code)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def upsert(self, stats: PlayerStats) -> PlayerStats:
        """
        Insert or update based on the unique constraint (player_id, team_id, season_code, source)
        If the record already exists, update the values, otherwise insert
        """

        stmt = (insert(PlayerStats).values(id = stats.id,
                                           player_id = stats.player_id,
                                           team_id = stats.team_id,
                                           season_code = stats.season_code,
                                           source = stats.source,
                                           minutes = stats.minutes,
                                           matches = stats.matches,
                                           goals = stats.goals,
                                           assists = stats.assists,
                                           metrics = stats.metrics,
                                           )
                                           .on_conflict_do_update(constraints = "uq_player_stats_logical",
                                                                  set_={
                                                                      "minutes" : stats.minutes,
                                                                      "matches" : stats.matches,
                                                                      "goals" : stats.goals,
                                                                      "assists" : stats.assists,
                                                                      "metrics" : stats.metrics,
                                                                      "updated_at" : stats.updated_at,
                                                                  },
                                            )
                                            .returning(PlayerStats)
                )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def bulk_upsert(self, stats_list: list[PlayerStats]) -> int:
        """
        Mass upsert, used from batch ETL
        Returns the number of processed rows
        """
        if not stats_list:
            return 0
        
        values =[{  
                    "id" = s.id,
                    "player_id" = s.player_id,
                    "team_id" = s.team_id,
                    "season_code" = s.season_code,
                    "source" = s.source,
                    "minutes" = s.minutes,
                    "matches" = s.matches,
                    "goals" = s.goals,
                    "assists" = s.assists,
                    "metrics" = s.metrics,
                }
                for s in stats_list
                ]
        stmt = (
            insert(PlayerStats)
            .values(values)
            .on_conflict_do_update(
                constraint="uq_player_stats_logical",
                set={
                    "minutes" : insert(PlayerStats).excluded.minutes,
                    "matches" : insert(PlayerStats).exluded.matches,
                    "goals" : insert(PlayerStats).excluded.goals,
                    "assists" : insert(PlayerStats).exluded.assists,
                    "metrics" : insert(PlayerStats).excluded.metrics,
                }
            )
        )

        await self.session.execute(stmt)
        await self.session.flush()
        return len(stats_list)
    
    async def delete(self, stats_id: UUID) -> None:
        stats = await self.get_by_id(stats_id)
        if stats:
            await self.session.delete(stats)