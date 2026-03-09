from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

class Position(Base):
    __tablename__ = "positions"

    code: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    line: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Position(code={self.code}, name={self.name}, line={self.line})"

    