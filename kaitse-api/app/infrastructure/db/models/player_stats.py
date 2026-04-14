from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Integer, DateTime, Text, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

class PlayerStats(Base):
    __tablename__ = "player_stats"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    player_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    team_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    season_code: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)

    #fixed metrics
    minutes: Mapped[int|None] = mapped_column(Integer, nullable=True)
    matches: Mapped[int|None] = mapped_column(Integer, nullable=True)
    goals: Mapped[int|None] = mapped_column(Integer, nullable=True)
    assists: Mapped[int|None] = mapped_column(Integer, nullable=True)

    #extendible metrics
    metrics: Mapped[dict|None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    #Unique constraint resolves the issue of multiple entries for the same player-season-source combination
    __table_args__ = (UniqueConstraint('player_id', 'team_id', 'season_code', 'source', name='uq_player_season_source'),)

    def __repr__(self) -> str:
        return f"<PlayerStats(id={self.id}, player_id='{self.player_id}', season='{self.season_code}', source='{self.source}')>"