"""Shared test fixtures for all backend tests.

Provides:
- db_session: In-memory async SQLite session for repository/service tests
- _reset_external_bridge_cache: Autouse fixture that clears module-level
  globals in external_precondition_bridge and settings cache between every
  test, preventing cross-test pollution.
"""

import pytest


@pytest.fixture
async def db_session():
    """Create an in-memory async SQLite session for testing."""
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
    from backend.db.database import Base

    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture(autouse=True)
def _reset_external_bridge_cache():
    """Reset bridge module caches and settings cache before and after each test.

    The external_precondition_bridge module stores 13+ module-level globals
    (_pre_front_class, _login_api_instance, _assertion_classes_cache, etc.)
    that persist across tests if not explicitly cleared. This autouse fixture
    ensures a clean state for every test in every subdirectory.
    """
    from backend.core import external_precondition_bridge
    from backend.config import get_settings

    external_precondition_bridge.reset_cache()
    get_settings.cache_clear()
    yield
    external_precondition_bridge.reset_cache()
    get_settings.cache_clear()
