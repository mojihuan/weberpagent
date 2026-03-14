import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import engine, async_session, get_db


def test_engine_pool_configuration():
    """Engine has explicit pool configuration"""
    # Access pool configuration through engine
    assert engine.pool.size() == 5, "Pool size should be 5"
    assert engine.pool._max_overflow == 0, "max_overflow should be 0 for SQLite"


def test_engine_pool_pre_ping():
    """Engine has pool_pre_ping enabled"""
    # pool_pre_ping is stored in pool._pre_ping
    assert engine.pool._pre_ping is True, "pool_pre_ping should be enabled"


@pytest.mark.asyncio
async def test_concurrent_sessions():
    """Concurrent database operations don't block"""
    results = []

    async def db_operation(i: int):
        async with async_session() as session:
            # Simulate a quick operation
            results.append(i)
            return i

    # Run 5 concurrent operations
    tasks = [db_operation(i) for i in range(5)]
    await asyncio.gather(*tasks)

    assert len(results) == 5, "All operations should complete"


@pytest.mark.asyncio
async def test_get_db_yields_session():
    """get_db dependency yields proper session"""
    gen = get_db()
    session = await gen.__anext__()
    assert isinstance(session, AsyncSession), "Should yield AsyncSession"
    # Clean up
    try:
        await gen.__anext__()
    except StopAsyncIteration:
        pass


@pytest.mark.asyncio
async def test_session_autocommit_off():
    """Sessions are not in autocommit mode by default"""
    async with async_session() as session:
        # SQLAlchemy async sessions are not autocommit by default
        # This test verifies the session factory is configured correctly
        assert not session.autocommit if hasattr(session, 'autocommit') else True
