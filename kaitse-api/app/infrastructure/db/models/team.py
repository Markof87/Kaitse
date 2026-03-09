from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tm_team_id: Mapped[int|None] = mapped_column(BigInteger, nullable=True, unique=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str|None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str|None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Team(id={self.id}, name={self.name})"