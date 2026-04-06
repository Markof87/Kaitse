from datetime import datetime
from uuid import UUID

import pytest

from pydantic import ValidationError
from app.application.dto.team import TeamCreateDTO, TeamUpdateDTO, TeamResponseDTO

# -------------------------
# TeamCreateDTO
# -------------------------

def test_team_create_requires_name():
    with pytest.raises(ValidationError):
        TeamCreateDTO()

def test_team_create_accepts_only_tm_id():
    dto = TeamCreateDTO(tm_team_id=123, name="Team A")
    assert dto.tm_team_id == 123
    assert dto.name == "Team A"
    assert dto.city is None
    assert dto.image_path is None

def test_team_create_dto():
    dto = TeamCreateDTO(tm_team_id=123, name="Team A", city="City A", image_path="/path/to/image.png")
    assert dto.tm_team_id == 123
    assert dto.name == "Team A"
    assert dto.city == "City A"
    assert dto.image_path == "/path/to/image.png"

# -------------------------
# TeamUpdateDTO
# -------------------------

def test_team_update_allows_empty_payload():
    dto = TeamUpdateDTO()
    assert dto.model_dump(exclude_unset=True) == {}

# -------------------------
# TeamResponseDTO
# -------------------------

def test_team_response_from_dict():
    data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "tm_team_id": 123,
        "name": "Team A",
        "city": "City A",
        "image_path": "/path/to/image.png",
        "created_at": "2024-06-01T12:00:00Z"
    }
    dto = TeamResponseDTO(**data)
    assert dto.id == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert dto.tm_team_id == 123
    assert dto.name == "Team A"
    assert dto.city == "City A"
    assert dto.image_path == "/path/to/image.png"
    assert dto.created_at == datetime.fromisoformat("2024-06-01T12:00:00Z")