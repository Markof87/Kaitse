from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

class CompetitionSeason(Base):
    __tablename__ = "competition_season"

    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id", ondelete="CASCADE"), primary_key=True)
    season_code: Mapped[str] = mapped_column(ForeignKey("seasons.code", ondelete="CASCADE"), primary_key=True)

class CompetitionSeasonTeam(Base):
    __tablename__ = "competition_season_team"

    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id", ondelete="CASCADE"), primary_key=True)
    season_code: Mapped[str] = mapped_column(ForeignKey("seasons.code", ondelete="CASCADE"), primary_key=True)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)

class PlayerPosition(Base):
    __tablename__ = "player_position"

    player_id: Mapped[UUID] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), primary_key=True)
    position_code: Mapped[str] = mapped_column(ForeignKey("positions.id", ondelete="CASCADE"), primary_key=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

class PlayerNationality(Base):
    __tablename__ = "player_nationalities"
    player_id: Mapped[UUID] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), primary_key=True)
    nationality_code: Mapped[str] = mapped_column(ForeignKey("nationalities.code", ondelete="CASCADE"), primary_key=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())