from pydantic import BaseModel, Field

class PositionCreateDTO(BaseModel):
    code: str = Field(..., description="Position Code, e.g GK, CB etc...")
    name: str
    line: str | None = None

class PositionUpdateDTO(BaseModel):
    name: str | None = None
    line: str | None = None

class PositionResponseDTO(BaseModel):
    code: str
    name: str
    line: str | None = None

    model_config = {"from_attributes": True}