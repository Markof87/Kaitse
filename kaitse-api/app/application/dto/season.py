from datetime import date, datetime

from pydantic import BaseModel, Field

class SeasonCreateDTO(BaseModel):
    code: str = Field(..., description="Season Code, eg 2025-26")
    start_date: date | None=None
    end_date: date | None=None

class SeasonUpdateDTO(BaseModel):
    start_date: date | None=None
    end_date: date | None=None

class SeasonResponseDTO(BaseModel):
    code: str
    start_date: date | None
    end_date: date | None
    created_at: datetime

    #from_attributes = True is fundamental - says Pydantic to read values from attributes of an object (our ORM) instead of a dictionary
    model_config = {"from_attributes": True}