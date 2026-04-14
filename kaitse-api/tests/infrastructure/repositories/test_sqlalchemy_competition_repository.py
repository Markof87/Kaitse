import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.competition import Competition
from app.infrastructure.repositories.sqlalchemy_competition_repository import SqlAlchemyCompetitionRepository

@pytest.mark.asyncio
async def test_get_by_id_returns_competition(test_db_session: AsyncSession):
    #Setup
    competition = Competition(name="Test Competition", code="TEST123", country_code="US", level=1)
    test_db_session.add(competition)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    result = await repository.get_by_id(1)
    
    #Assert
    assert result is not None
    assert result.name == "Test Competition"
    assert result.code == "TEST123"

@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_nonexistent_competition(test_db_session: AsyncSession):

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    result = await repository.get_by_id(999)
    
    #Assert
    assert result is None

@pytest.mark.asyncio
async def test_get_by_code(test_db_session: AsyncSession):
    #Setup
    competition = Competition(name="Test Competition", code="TEST123", country_code="US", level=1)
    test_db_session.add(competition)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    result = await repository.get_by_code("TEST123")
    
    #Assert
    assert result is not None
    assert result.name == "Test Competition"
    assert result.code == "TEST123"

#First test of list is from the if clause "if country:= filters.get("country_code"):"
@pytest.mark.asyncio
async def test_list_with_country_filter(test_db_session: AsyncSession):
    #Setup
    competition1 = Competition(name="Competition 1", code="COMP1", country_code="US", level=1)
    competition2 = Competition(name="Competition 2", code="COMP2", country_code="CA", level=1)
    test_db_session.add_all([competition1, competition2])
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    result = await repository.list({"country_code": "US"})
    
    #Assert
    assert len(result) == 1
    assert result[0].name == "Competition 1"

#Second test of list is from the if clause "if level:= filters.get("level"):"
@pytest.mark.asyncio
async def test_list_with_level_filter(test_db_session: AsyncSession):
    #Setup
    competition1 = Competition(name="Competition 1", code="COMP1", country_code="US", level=1)
    competition2 = Competition(name="Competition 2", code="COMP2", country_code="US", level=2)
    test_db_session.add_all([competition1, competition2])
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    result = await repository.list({"level": 1})
    
    #Assert
    assert len(result) == 1
    assert result[0].name == "Competition 1"

@pytest.mark.asyncio
async def test_save_new_competition(test_db_session: AsyncSession):
    #Setup
    competition = Competition(name="New Competition", code="NEW123", country_code="US", level=1)

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    saved_competition = await repository.save(competition)
    
    #Assert
    assert saved_competition.id is not None
    assert saved_competition.name == "New Competition"
    assert saved_competition.code == "NEW123"

@pytest.mark.asyncio
async def test_delete_competition(test_db_session: AsyncSession):
    #Setup
    competition = Competition(name="Competition to Delete", code="DEL123", country_code="US", level=1)
    test_db_session.add(competition)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyCompetitionRepository(test_db_session)
    await repository.delete(competition.id)
    await test_db_session.flush()
    
    #Assert
    deleted_competition = await repository.get_by_id(competition.id)
    assert deleted_competition is None