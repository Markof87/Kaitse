from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Integer, Date, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

class Player(Base):
    __tablename__ = "players"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    short_name: Mapped[str|None] = mapped_column(Text, nullable=False)
    birth_date: Mapped[date|None] = mapped_column(Date, nullable=True)
    height: Mapped[int|None] = mapped_column(Integer, nullable=True)
    weight: Mapped[int|None] = mapped_column(Integer, nullable=True)
    preferred_foot: Mapped[str|None] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    image_path: Mapped[str|None] = mapped_column(Text, nullable=True)

    #External identifiers
    fbref_id: Mapped[int|None] = mapped_column(Text, unique=True, nullable=True)
    sofascore_id: Mapped[int|None] = mapped_column(Integer, unique=True, nullable=True)
    fotmob_id: Mapped[int|None] = mapped_column(Integer, unique=True, nullable=True)
    transfermarkt_id: Mapped[int|None] = mapped_column(Integer, unique=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Player(id={self.id}, full_name='{self.full_name}', slug='{self.slug}')>"