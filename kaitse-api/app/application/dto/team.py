from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class TeamCreateDTO(BaseModel):
    tm_team_id: int | None = None
    name: str
    city: str | None = None
    image_path: str | None = None

class TeamUpdateDTO(BaseModel):
    id: UUID
    tm_team_id: int | None
    name: str
    city: str | None
    image_path: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

class TeamResponseDTO(BaseModel):
    id: UUID
    tm_team_id: int | None
    name: str
    city: str | None
    image_path: str | None
    created_at: datetime

    model_config = {"from_attributes": True}