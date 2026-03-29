from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

class PlayerCreateDTO(BaseModel):
    full_name: str
    short_name: str | None = None
    birth_date: date | None = None
    height: int | None = Field(None, ge=100, le=250, description="Height in centimeters")
    weight: int | None = Field(None, ge=40, le=150, description="Weight in kilograms")
    preferred_foot: str | None = Field(None, pattern="^(left|right|both)$")
    slug: str
    image_path: str | None = None
    fbref_id: str | None = None
    sofascore_id: int | None = None
    fotmob_id: int | None = None
    transfermarkt_id: int | None = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        if not value.replace("-", "").isalnum():
            raise ValueError("Slug must contain only alphanumeric characters and hyphens")
        return value.lower()
    
class PlayerUpdateDTO(BaseModel):
    full_name: str | None = None
    short_name: str | None = None
    birth_date: date | None = None
    height: int | None = Field(None, ge=100, le=250)
    weight: int | None = Field(None, ge=40, le=150)
    preferred_foot: str | None = Field(None, pattern="^(left|right|both)$")
    image_path: str | None = None
    fbref_id: str | None = None
    sofascore_id: int | None = None
    fotmob_id: int | None = None
    transfermarkt_id: int | None = None

class PlayerResponseDTO(BaseModel):
    id: UUID
    full_name: str
    short_name: str | None
    birth_date: date | None
    height: int | None
    weight: int | None
    preferred_foot: str | None
    slug: str
    image_path: str | None
    fbref_id: str | None
    sofascore_id: int | None
    fotmob_id: int | None
    transfermarkt_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class PlayerFiltersDTO(BaseModel):
    name: str | None = None
    preferred_foot: str | None = None

#DTO for associations
class PlayerPositionAddDTO(BaseModel):
    position_code: str
    is_primary: bool = False

class PlayerNationalityAddDTO(BaseModel):
    national_code: str
    is_primary: bool = False
