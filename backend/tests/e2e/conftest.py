"""Shared E2E test fixtures for Phase 81 batch execution and compatibility verification."""

import os
import subprocess

import httpx
import pytest

from backend.config.settings import get_settings
from backend.core.auth_service import AuthService


@pytest.fixture
def erp_base_url() -> str:
    """Return ERP base URL from settings."""
    settings = get_settings()
    return settings.erp_base_url.rstrip("/")


@pytest.fixture
def auth_service() -> AuthService:
    """Return a fresh AuthService instance."""
    return AuthService()


@pytest.fixture
def skip_if_erp_unreachable(erp_base_url):
    """Skip test if ERP server is unreachable.

    Makes a lightweight HTTP GET to the ERP base URL.
    If connection fails or times out, skips the test instead of failing.
    """
    try:
        with httpx.Client(timeout=5.0) as client:
            client.get(erp_base_url)
    except (httpx.ConnectError, httpx.TimeoutException) as exc:
        pytest.skip(f"ERP server unreachable at {erp_base_url}: {exc}")


@pytest.fixture
def all_roles():
    """Return list of all 7 UI roles."""
    return ["main", "special", "vice", "camera", "platform", "super", "idle"]


@pytest.fixture(autouse=True, scope="session")
def cleanup_browser_processes():
    """Kill any orphaned chromium processes after test session."""
    yield
    try:
        subprocess.run(["pkill", "-f", "chromium"], capture_output=True, timeout=5)
    except Exception:
        pass
