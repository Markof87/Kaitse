from uuid import uuid4

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.player_stats import PlayerStats
from app.infrastructure.repositories.sqlalchemy_player_stats_repository import SqlAlchemyPlayerStatsRepository

@pytest.mark.asyncio
async def test_get_by_id(test_db_session: AsyncSession):
    #Setup
    stats = PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    test_db_session.add(stats)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.get_by_id(stats.id)
    
    #Assert
    assert result is not None
    assert result.player_id == stats.player_id
    assert result.team_id == stats.team_id
    assert result.season_code == "2023/2024"
    assert result.source == "test_source"
    assert result.minutes == 1000
    assert result.matches == 10
    assert result.goals == 5
    assert result.assists == 3
    assert result.metrics == {"key": "value"}

@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_nonexistent_stats(test_db_session: AsyncSession):
    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.get_by_id(uuid4())

    #Assert
    assert result is None

@pytest.mark.asyncio
async def test_get_by_player(test_db_session: AsyncSession):
    #Setup
    stats = PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    test_db_session.add(stats)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.get_by_player(stats.player_id)
    
    #Assert
    assert result is not None
    for r in result:
        assert r.player_id == stats.player_id

@pytest.mark.asyncio
async def test_get_by_player_filters_by_season(test_db_session: AsyncSession):
    #Setup
    player_id = uuid4()
    stats1 = PlayerStats(player_id=player_id, team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    stats2 = PlayerStats(player_id=player_id, team_id=uuid4(), season_code="2022/2023", source="test_source", minutes=800, matches=8, goals=3, assists=2, metrics={"key": "value"})
    test_db_session.add_all([stats1, stats2])
    await test_db_session.flush()

@pytest.mark.asyncio
async def test_get_by_team(test_db_session: AsyncSession):
    #Setup
    stats = PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    test_db_session.add(stats)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.get_by_team(stats.team_id)
    #Assert
    assert result is not None
    for r in result:
        assert r.team_id == stats.team_id

@pytest.mark.asyncio
async def test_get_by_team_filters_by_season(test_db_session: AsyncSession):
    #Setup
    team_id = uuid4()
    stats1 = PlayerStats(player_id=uuid4(), team_id=team_id, season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    stats2 = PlayerStats(player_id=uuid4(), team_id=team_id, season_code="2022/2023", source="test_source", minutes=800, matches=8, goals=3, assists=2, metrics={"key": "value"})
    test_db_session.add_all([stats1, stats2])
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.get_by_team(team_id, season_code="2023/2024")

    #Assert
    assert result is not None
    for r in result:
        assert r.team_id == team_id
        assert r.season_code == "2023/2024"

@pytest.mark.asyncio
async def test_upsert_inserts_new_stats(test_db_session: AsyncSession):
    #Setup
    stats = PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.upsert(stats)

    #Assert
    assert result is not None
    assert result.player_id == stats.player_id
    assert result.team_id == stats.team_id
    assert result.season_code == "2023/2024"
    assert result.source == "test_source"
    assert result.minutes == 1000
    assert result.matches == 10
    assert result.goals == 5
    assert result.assists == 3
    assert result.metrics == {"key": "value"}

@pytest.mark.asyncio
async def test_upsert_updates_existing_stats(test_db_session: AsyncSession):
    #Setup
    stats = PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    test_db_session.add(stats)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    stats.minutes = 1200
    stats.goals = 7
    result = await repository.upsert(stats)

    #Assert
    assert result is not None
    assert result.minutes == 1200
    assert result.goals == 7
    assert result.assists == 3
    assert result.metrics == {"key": "value"}

@pytest.mark.asyncio
async def test_bulk_upsert(test_db_session: AsyncSession):
    #Setup
    stats_list = [
        PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"}),
        PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=800, matches=8, goals=3, assists=2, metrics={"key": "value"}),
    ]

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.bulk_upsert(stats_list)

    #Assert
    assert result == 2

@pytest.mark.asyncio
async def test_bulk_upsert_with_empty_list(test_db_session: AsyncSession):
    #Setup
    stats_list = []

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.bulk_upsert(stats_list)

    #Assert
    assert result == 0

@pytest.mark.asyncio
async def test_bulk_upsert_with_duplicates(test_db_session: AsyncSession):
    #Setup
    player_id = uuid4()
    team_id = uuid4()
    stats1 = PlayerStats(player_id=player_id, team_id=team_id, season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    stats2 = PlayerStats(player_id=player_id, team_id=team_id, season_code="2023/2024", source="test_source", minutes=1200, matches=12, goals=7, assists=4, metrics={"key": "updated_value"})
    test_db_session.add(stats1)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.bulk_upsert([stats2])

@pytest.mark.asyncio
async def test_bulk_upsert_with_conflicts(test_db_session: AsyncSession):
    #Setup
    player_id = uuid4()
    team_id = uuid4()
    stats1 = PlayerStats(player_id=player_id, team_id=team_id, season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    stats2 = PlayerStats(player_id=player_id, team_id=team_id, season_code="2023/2024", source="test_source", minutes=1200, matches=12, goals=7, assists=4, metrics={"key": "updated_value"})
    test_db_session.add(stats1)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    result = await repository.bulk_upsert([stats2])

@pytest.mark.asyncio
async def test_delete(test_db_session: AsyncSession):
    #Setup
    stats = PlayerStats(player_id=uuid4(), team_id=uuid4(), season_code="2023/2024", source="test_source", minutes=1000, matches=10, goals=5, assists=3, metrics={"key": "value"})
    test_db_session.add(stats)
    await test_db_session.flush()

    #Execute
    repository = SqlAlchemyPlayerStatsRepository(test_db_session)
    await repository.delete(stats.id)

    #Assert
    result = await repository.get_by_id(stats.id)
    assert result is None
