from pydantic import BaseModel

class CompetitionSeasonCreateDTO(BaseModel):
    season_code: str
    competition_id: int
    is_current: bool

class CompetitionSeasonResponseDTO(BaseModel):
    season_code: str
    competition_id: int
    is_current: bool

    model_config = {"from_attributes": True}