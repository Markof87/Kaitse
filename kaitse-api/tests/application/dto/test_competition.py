from pydantic import ValidationError

from app.application.dto.competition import CompetitionCreateDTO, CompetitionUpdateDTO, CompetitionResponseDTO

# -------------------------
# CompetitionCreateDTO
# -------------------------

def test_competition_create_dto():
    dto = CompetitionCreateDTO(code="IT1", name="International Tournament 1")
    assert dto.code == "IT1"
    assert dto.name == "International Tournament 1"

# -------------------------
# CompetitionUpdateDTO
# -------------------------

def test_competition_allows_empty_payload():
    dto = CompetitionUpdateDTO()
    assert dto.model_dump(exclude_unset=True) == {}

# -------------------------
# CompetitionResponseDTO
# -------------------------

def test_competition_response_dto_from_dict():
    data = {
        "id": 1,
        "code": "IT1",
        "name": "International Tournament 1",
        "country_code": "US",
        "level": 1,
        "organizer": "FIFA",
        "created_at": "2024-06-01T12:00:00Z"
    }
    dto = CompetitionResponseDTO(**data)
    assert dto.id == 1
    assert dto.code == "IT1"
    assert dto.name == "International Tournament 1"
    assert dto.country_code == "US"
    assert dto.level == 1
    assert dto.organizer == "FIFA"




