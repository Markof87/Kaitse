from datetime import datetime

from pydantic import BaseModel, Field

class CompetitionCreateDTO(BaseModel):
    code: str = Field(..., example="Unique code competition e.g. 'IT1'")
    name: str
    country_code: str | None = None
    level: int | None = None
    organizer: str | None = None

class CompetitionUpdateDTO(BaseModel):
    name: str | None = None
    country_code: str | None = None
    level: int | None = None
    organizer: str | None = None

class CompetitionResponseDTO(BaseModel):
    id: int
    code: str
    name: str
    country_code: str | None
    level: int | None
    organizer: str | None
    created_at: datetime

    model_config = {"from_attributes": True}