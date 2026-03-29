from pydantic import BaseModel

class NationalityCreateDto(BaseModel):
    code: str
    fifa_name: str | None = None
    confederation: str | None = None

class NationalityUpdateDto(BaseModel):
    fifa_name: str | None = None
    confederation: str | None = None
    
class NationalityResponseDto(BaseModel):
    code: str
    fifa_name: str | None
    confederation: str | None

    model_config = {"from_attributes": True}