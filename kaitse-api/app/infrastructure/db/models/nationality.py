from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base

class Nationality(Base):
    __tablename__ = "nationalities"

    code: Mapped[str] = mapped_column(Text, primary_key=True)
    fifa_name: Mapped[str|None] = mapped_column(Text, nullable=True)
    confederation: Mapped[str|None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Nationality(code={self.code}, fifa_name={self.fifa_name}, confederation={self.confederation})"