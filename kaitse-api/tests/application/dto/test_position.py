from app.application.dto.position import PositionCreateDTO, PositionUpdateDTO, PositionResponseDTO

# -------------------------
# PositionCreateDTO
# -------------------------

def test_position_create_dto():
    dto = PositionCreateDTO(code="FW", name="Forward", line="Attack")
    assert dto.code == "FW"
    assert dto.name == "Forward"
    assert dto.line == "Attack"

# -------------------------
# PositionUpdateDTO
# -------------------------

def test_position_update_allows_empty_payload():
    dto = PositionUpdateDTO()
    assert dto.model_dump(exclude_unset=True) == {}
    
def test_position_update_dto():
    dto = PositionUpdateDTO(name="Forward", line="Attack")
    assert dto.name == "Forward"
    assert dto.line == "Attack"

# -------------------------
# PositionResponseDTO
# -------------------------

def test_position_response_from_dict():
    data = {
        "code": "FW",
        "name": "Forward",
        "line": "Attack"
    }
    dto = PositionResponseDTO(**data)
    assert dto.code == "FW"
    assert dto.name == "Forward"
    assert dto.line == "Attack"