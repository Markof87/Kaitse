from datetime import date, datetime
import pytest

from pydantic import ValidationError
from app.application.dto.season import SeasonCreateDTO, SeasonUpdateDTO, SeasonResponseDTO

# -------------------------
# SeasonCreateDTO
# -------------------------

def test_season_create_accepts_only_code():
    dto = SeasonCreateDTO(code="2025-26")
    assert dto.code == "2025-26"
    assert dto.start_date is None
    assert dto.end_date is None

def test_season_create_parsers_dates_from_strings():
    dto = SeasonCreateDTO(code="2025-26", start_date="2025-08-01", end_date="2026-05-31")
    assert dto.start_date == date(2025, 8, 1)
    assert dto.end_date == date(2026, 5, 31)

def test_season_create_rejects_invalid_dates():
    with pytest.raises(ValidationError):
        SeasonCreateDTO(code="2025-26", start_date="invalid-date")

# -------------------------
# SeasonUpdateDTO
# -------------------------

def test_season_update_allows_empty_payload():
    dto = SeasonUpdateDTO()
    assert dto.model_dump(exclude_unset=True) == {}

def test_season_update_parsers_dates():
    dto = SeasonUpdateDTO(start_date="2025-08-01", end_date="2026-05-31")
    assert dto.start_date == date(2025, 8, 1)
    assert dto.end_date == date(2026, 5, 31)

def test_season_update_rejects_invalid_dates():
    with pytest.raises(ValidationError):
        SeasonUpdateDTO(start_date="28/02/2026")

# -------------------------
# SeasonResponseDTO
# -------------------------

def test_season_response_from_dict():
    data = {
        "code": "2025-26",
        "start_date": "2025-08-01",
        "end_date": None,
        "created_at": "2024-06-01T12:00:00Z"
    }
    dto = SeasonResponseDTO(**data)
    assert dto.code == "2025-26"
    assert dto.start_date == date(2025, 8, 1)
    assert dto.end_date is None
    assert isinstance(dto.created_at, datetime)

def test_season_requires_created_at():
    with pytest.raises(ValidationError):
        SeasonResponseDTO(code="2025-26", start_date=None, end_date=None)

def test_season_response_supports_from_attributes():
    class SeasonORM:
        def __init__(self):
            self.code = "2025-26"
            self.start_date = date(2025, 8, 1)
            self.end_date = None
            self.created_at = datetime(2024, 6, 1, 12, 0, 0)
            
    orm_obj = SeasonORM()
    dto = SeasonResponseDTO.model_validate(orm_obj)
    assert dto.code == "2025-26"
    assert dto.start_date == date(2025, 8, 1)
    assert dto.end_date is None
    assert dto.created_at == datetime(2024, 6, 1, 12, 0, 0)