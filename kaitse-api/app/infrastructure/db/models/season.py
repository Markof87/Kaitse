from datetime import date, datetime

from sqlalchemy import Date, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

# SQLAlchemy model for the "seasons" table
# This model represents a football season, with fields for the season code (e.g., "2025-2026"), 
# start date, and end date.

class Season(Base):
    __tablename__="seasons"

    code: Mapped[str] = mapped_column(Text, primary_key=True)
    start_date: Mapped[date|None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date|None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Season(code={self.code}, start_date={self.start_date}, end_date={self.end_date})"