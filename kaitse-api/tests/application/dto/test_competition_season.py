from app.application.dto.competition_season import CompetitionSeasonCreateDTO, CompetitionSeasonResponseDTO

# -------------------------
# CompetitionSeasonCreateDTO
# -------------------------

def test_competition_season_create_dto():
    dto = CompetitionSeasonCreateDTO(competition_id=1, season_code="2025-26")
    assert dto.competition_id == 1
    assert dto.season_code == "2025-26"

# -------------------------
# CompetitionSeasonResponseDTO
# -------------------------

def test_competition_season_response_dto():
    dto = CompetitionSeasonResponseDTO(competition_id=1, season_code="2025-26", is_current=True)
    assert dto.competition_id == 1
    assert dto.season_code == "2025-26"
    assert dto.is_current is True

def test_competition_season_response_dto_from_dict():
    data = {
        "competition_id": 1,
        "season_code": "2025-26",
        "is_current": True
    }
    dto = CompetitionSeasonResponseDTO(**data)
    assert dto.competition_id == 1
    assert dto.season_code == "2025-26"
    assert dto.is_current is True