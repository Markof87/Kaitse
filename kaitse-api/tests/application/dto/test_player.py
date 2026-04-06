from datetime import datetime

import pytest
from pydantic import ValidationError

from app.application.dto.player import PlayerCreateDTO, PlayerUpdateDTO, PlayerResponseDTO, PlayerPositionAddDTO, PlayerNationalityAddDTO

# -------------------------
# PlayerCreateDTO
# -------------------------

def test_player_create_dto_valid():
    dto = PlayerCreateDTO(
        full_name="John Doe",
        short_name="Doe",
        height=180,
        preferred_foot="right",
        slug="john-doe"
    )
    assert dto.full_name == "John Doe"
    assert dto.short_name == "Doe"
    assert dto.height == 180
    assert dto.preferred_foot == "right"
    assert dto.slug == "john-doe"

def test_player_create_dto_invalid_preferred_foot():
    with pytest.raises(ValidationError):
        PlayerCreateDTO(
            full_name="John Doe",
            slug="john-doe",
            preferred_foot="upside-down"
        )

def test_player_create_dto_invalid_slug():
    with pytest.raises(ValidationError):
        PlayerCreateDTO(
            full_name="John Doe",
            slug="john doe"
        )

# -------------------------
# PlayerUpdateDTO
# -------------------------

def test_player_update_dto_allows_empty_payload():
    dto = PlayerUpdateDTO()
    assert dto.model_dump(exclude_unset=True) == {}

# -------------------------
# PlayerResponseDTO
# -------------------------

def test_player_response_dto_from_dict():
    data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "full_name": "John Doe",
        "slug": "john-doe",
        "created_at": "2024-06-01T12:00:00Z",
        "updated_at": "2024-06-01T12:00:00Z"
    }
    dto = PlayerResponseDTO(**data)
    assert dto.full_name == "John Doe"
    assert isinstance(dto.created_at, datetime)
    assert isinstance(dto.updated_at, datetime)

# -------------------------
# PlayerPositionAddDTO
# -------------------------

def test_player_position_add_dto_valid():
    dto = PlayerPositionAddDTO(position_code="FW")
    assert dto.position_code == "FW"
    assert dto.is_primary is False

# -------------------------
# PlayerNationalityAddDTO
# -------------------------

def test_player_nationality_add_dto_valid():
    dto = PlayerNationalityAddDTO(code="ITA")
    assert dto.code == "ITA"
    assert dto.is_primary is False