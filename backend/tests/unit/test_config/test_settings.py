"""Unit tests for weberp_path configuration in Settings."""

import os

import pytest

from backend.config.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    """Clear get_settings cache before and after each test for isolation."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class TestWeberpPathSettings:
    """Tests for weberp_path field in Settings."""

    def test_weberp_path_default_none(self, monkeypatch):
        """weberp_path defaults to None when not configured."""
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        from backend.config import get_settings
        get_settings.cache_clear()  # Clear cached settings
        settings = Settings()
        # Empty string is treated as "not configured" (same as None)
        assert settings.weberp_path in (None, '')

    def test_weberp_path_from_env(self, monkeypatch):
        """weberp_path loads from WEBERP_PATH env var."""
        monkeypatch.setenv('WEBSERP_PATH', '/path/to/webseleniumerp')
        from backend.config import get_settings
        get_settings.cache_clear()  # Clear cached settings
        settings = Settings()
        assert settings.weberp_path == "/path/to/webseleniumerp"

    def test_weberp_path_optional_string(self, monkeypatch):
        """weberp_path accepts string or None."""
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        from backend.config import get_settings
        get_settings.cache_clear()  # Clear cached settings
        settings = Settings()
        # Empty string is treated as "not configured" (same as None)
        assert settings.weberp_path in (None, '')

        monkeypatch.setenv('WEBSERP_PATH', '/another/path')
        get_settings.cache_clear()  # Clear cached settings
        settings = Settings()
        assert isinstance(settings.weberp_path, str)
        assert settings.weberp_path == "/another/path"
