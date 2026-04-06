from app.application.dto.nationality import NationalityCreateDto, NationalityUpdateDto, NationalityResponseDto

# -------------------------
# NationalityCreateDto
# -------------------------

def test_nationality_create_dto():
    dto = NationalityCreateDto(code="ENG", fifa_name="England", confederation="UEFA")
    assert dto.code == "ENG"
    assert dto.fifa_name == "England"
    assert dto.confederation == "UEFA"

# -------------------------
# NationalityUpdateDto
# -------------------------

def test_nationality_update_allows_empty_payload():
    dto = NationalityUpdateDto()
    assert dto.model_dump(exclude_unset=True) == {}
    
def test_nationality_update_dto():
    dto = NationalityUpdateDto(fifa_name="England", confederation="UEFA")
    assert dto.fifa_name == "England"
    assert dto.confederation == "UEFA"

# -------------------------
# NationalityResponseDto
# -------------------------

def test_nationality_response_from_dict():
    data = {
        "code": "ENG",
        "fifa_name": "England",
        "confederation": "UEFA"
    }
    dto = NationalityResponseDto(**data)
    assert dto.code == "ENG"
    assert dto.fifa_name == "England"
    assert dto.confederation == "UEFA"