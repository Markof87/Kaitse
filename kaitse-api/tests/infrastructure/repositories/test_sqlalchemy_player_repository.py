from uuid import uuid4

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.player import Player
from app.infrastructure.repositories.sqlalchemy_player_repository import SQLAlchemyPlayerRepository

@pytest.mark.asyncio
async def test_get_by_id(test_db_session: AsyncSession):
    #Setup
    player = Player(full_name="Test Player", short_name="Test", slug="test-player", transfermarkt_id=12345, preferred_foot="right")
    test_db_session.add(player)
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.get_by_id(player.id)
    
    #Assert
    assert result is not None
    assert result.full_name == "Test Player"
    assert result.slug == "test-player"


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_nonexistent_player(test_db_session: AsyncSession):
    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    missing_uuid = uuid4()
    result = await repository.get_by_id(missing_uuid)
    
    #Assert
    assert result is None


@pytest.mark.asyncio
async def test_get_by_slug(test_db_session: AsyncSession):
    #Setup
    player = Player(full_name="Test Player", short_name="Test", slug="test-player", transfermarkt_id=12345, preferred_foot="right")
    test_db_session.add(player)
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.get_by_slug("test-player")

    #Assert
    assert result is not None
    assert result.full_name == "Test Player"
    assert result.slug == "test-player"

@pytest.mark.asyncio
async def test_get_by_slug_returns_none_for_nonexistent_player(test_db_session: AsyncSession):
    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.get_by_slug("nonexistent-player")

    #Assert
    assert result is None


@pytest.mark.asyncio
async def test_get_by_transfermarkt_id(test_db_session: AsyncSession):
    #Setup
    player = Player(full_name="Test Player", short_name="Test", slug="test-player", transfermarkt_id=12345, preferred_foot="right")
    test_db_session.add(player)
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.get_by_transfermarkt_id(12345)

    #Assert
    assert result is not None
    assert result.full_name == "Test Player"
    assert result.transfermarkt_id == 12345


@pytest.mark.asyncio
async def test_get_by_transfermarkt_id_returns_none_for_nonexistent_player(test_db_session: AsyncSession):
    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.get_by_transfermarkt_id(99999)

    #Assert
    assert result is None


@pytest.mark.asyncio
async def test_list_with_name_filter(test_db_session: AsyncSession):
    #Setup
    player1 = Player(full_name="Test Player 1", short_name="Test 1", slug="test-player-1", transfermarkt_id=12345, preferred_foot="right")
    player2 = Player(full_name="Another Player", short_name="Another", slug="another-player", transfermarkt_id=54321, preferred_foot="left")
    test_db_session.add_all([player1, player2])
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.list({"name": "Test"})

    #Assert
    assert len(result) == 1
    assert result[0].full_name == "Test Player 1"

@pytest.mark.asyncio
async def test_list_with_preferred_foot_filter(test_db_session: AsyncSession):
    #Setup
    player1 = Player(full_name="Test Player 1", short_name="Test 1", slug="test-player-1", transfermarkt_id=12345, preferred_foot="right")
    player2 = Player(full_name="Another Player", short_name="Another", slug="another-player", transfermarkt_id=54321, preferred_foot="left")
    test_db_session.add_all([player1, player2])
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    result = await repository.list({"preferred_foot": "right"})

    #Assert
    assert len(result) == 1
    assert result[0].full_name == "Test Player 1"

@pytest.mark.asyncio
async def test_save(test_db_session: AsyncSession):
    #Setup
    player = Player(full_name="New Player", short_name="New", slug="new-player", transfermarkt_id=67890, preferred_foot="right")

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    saved_player = await repository.save(player)

    #Assert
    assert saved_player.id is not None
    assert saved_player.full_name == "New Player"
    assert saved_player.slug == "new-player"

@pytest.mark.asyncio
async def test_delete(test_db_session: AsyncSession):
    #Setup
    player = Player(full_name="Player to Delete", short_name="Delete", slug="player-to-delete", transfermarkt_id=12345, preferred_foot="right")
    test_db_session.add(player)
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    await repository.delete(player.id)
    await test_db_session.flush()

    #Assert
    result = await repository.get_by_id(player.id)
    assert result is None

@pytest.mark.asyncio
async def test_exists(test_db_session: AsyncSession):
    #Setup
    player = Player(full_name="Existing Player", short_name="Existing", slug="existing-player", transfermarkt_id=12345, preferred_foot="right")
    test_db_session.add(player)
    await test_db_session.flush()

    #Execute
    repository = SQLAlchemyPlayerRepository(test_db_session)
    exists = await repository.exists(player.id)

    #Assert
    assert exists is True