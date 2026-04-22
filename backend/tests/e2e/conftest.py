"""E2E test fixtures.

Provides:
- api_client: httpx.AsyncClient for in-process FastAPI testing
- _reset_external_bridge_cache: Override that preserves bridge state (E2E needs real modules)
"""

import os
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient


def _load_dotenv():
    """Load .env file from project root if python-dotenv is available."""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:
        pass


def _has_api_key() -> bool:
    """Check if DASHSCOPE_API_KEY is configured."""
    _load_dotenv()
    return bool(os.environ.get("DASHSCOPE_API_KEY", "").strip())


def _has_weberp_path() -> bool:
    """Check if WEBSERP_PATH is configured and points to an existing directory."""
    _load_dotenv()
    weberp_path = os.environ.get("WEBSERP_PATH", "").strip()
    if not weberp_path:
        return False
    return Path(weberp_path).is_dir()


@pytest.fixture
async def api_client():
    """Create an httpx.AsyncClient for in-process FastAPI testing.

    Uses ASGITransport which triggers the app's lifespan (init_db, etc.)
    without starting a real server.
    """
    from backend.api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def _reset_external_bridge_cache():
    """Override parent's autouse fixture -- E2E tests need real bridge modules.

    The parent conftest resets all external_precondition_bridge caches between
    tests. E2E tests require the real bridge modules to stay loaded so that
    precondition and assertion execution can work end-to-end.
    """
    yield
