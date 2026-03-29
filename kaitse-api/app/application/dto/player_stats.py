from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class PlayerStatsCreateDTO(BaseModel):
    player_id: UUID
    team_id: UUID
    season_code: str
    source: str = Field(..., description="Source of the stats, e.g., 'fbref', 'sofascore', etc.")
    minutes: int | None = Field(None, ge=0, description="Total minutes played in the season")
    matches: int | None = Field(None, ge=0, description="Total matches played in the season")
    goals: int = Field(..., ge=0)
    assists: int = Field(..., ge=0)
    metrics: dict | None = None

class PlayerStatsUpsertDTO(BaseModel):
    player_id: UUID
    team_id: UUID
    season_code: str
    source: str 
    minutes: int | None = Field(None, ge=0)
    matches: int | None = Field(None, ge=0)
    goals: int = Field(..., ge=0)
    assists: int = Field(..., ge=0)
    metrics: dict | None = None

class PlayerStatsResponseDTO(BaseModel):
    id: UUID
    player_id: UUID
    team_id: UUID
    season_code: str
    source: str
    minutes: int | None
    matches: int | None
    goals: int | None
    assists: int | None
    metrics: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class PlayerStatsFilterDTO(BaseModel):
    player_id: UUID | None = None
    team_id: UUID | None = None
    season_code: str | None = None
    source: str | None = None