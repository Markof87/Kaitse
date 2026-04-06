from datetime import datetime

import pytest

from pydantic import ValidationError

from app.application.dto.player_stats import PlayerStatsCreateDTO, PlayerStatsUpsertDTO, PlayerStatsResponseDTO

# -------------------------
# PlayerStatsCreateDTO
# -------------------------

def test_player_stats_create_dto_valid():
    dto = PlayerStatsCreateDTO(
        player_id="123e4567-e89b-12d3-a456-426614174000",
        team_id="123e4567-e89b-12d3-a456-426614174001",
        season_code="2025-26",
        source="fbref",
        goals=5,
        assists=3
    )
    assert dto.goals == 5
    assert dto.assists == 3

def test_player_stats_create_dto_negative_goals():
    with pytest.raises(ValidationError):
        PlayerStatsCreateDTO(
            player_id="123e4567-e89b-12d3-a456-426614174000",
            team_id="123e4567-e89b-12d3-a456-426614174001",
            season_code="2025-26",
            source="fbref",
            goals=-1,
            assists=3
        )

def test_player_stats_create_dto_negative_assists():
    with pytest.raises(ValidationError):
        PlayerStatsCreateDTO(
            player_id="123e4567-e89b-12d3-a456-426614174000",
            team_id="123e4567-e89b-12d3-a456-426614174001",
            season_code="2025-26",
            source="fbref",
            goals=5,
            assists=-1
        )

# -------------------------
# PlayerStatsUpsertDTO
# -------------------------

def test_player_stats_upsert_dto_valid():
    dto = PlayerStatsUpsertDTO(
        player_id="123e4567-e89b-12d3-a456-426614174000",
        team_id="123e4567-e89b-12d3-a456-426614174001",
        season_code="2025-26",
        source="fbref",
        goals=5,
        assists=3
    )
    assert dto.goals == 5
    assert dto.assists == 3

# -------------------------
# PlayerStatsResponseDTO
# -------------------------

def test_player_stats_response_dto_from_dict():
    data = {
        "id": "123e4567-e89b-12d3-a456-426614174002",
        "player_id": "123e4567-e89b-12d3-a456-426614174000",
        "team_id": "123e4567-e89b-12d3-a456-426614174001",
        "season_code": "2025-26",
        "source": "fbref",
        "created_at": "2024-06-01T12:00:00Z",
        "updated_at": "2024-06-01T12:00:00Z"
    }
    dto = PlayerStatsResponseDTO(**data)
    assert dto.season_code == "2025-26"
    assert dto.source == "fbref"
    assert isinstance(dto.created_at, datetime)
    assert isinstance(dto.updated_at, datetime)