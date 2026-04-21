"""Unit tests for Settings module."""
import os
from unittest.mock import patch

import pytest

from backend.config.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    """Clear get_settings cache before and after each test for isolation."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class TestSettings:
    """Tests for Settings class."""

    def test_settings_default_values(self):
        """Settings() returns defaults when no env vars set."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.llm_model == "qwen3.5-plus"
            assert settings.llm_temperature == 0.0
            assert settings.log_level == "INFO"

    def test_settings_from_env_vars(self):
        """Settings() loads from environment variables."""
        with patch.dict(
            os.environ,
            {
                "LLM_MODEL": "custom-model",
                "LLM_TEMPERATURE": "0.5",
                "LOG_LEVEL": "DEBUG",
            },
        ):
            settings = Settings()
            assert settings.llm_model == "custom-model"
            assert settings.llm_temperature == 0.5
            assert settings.log_level == "DEBUG"

    def test_get_settings_cached(self):
        """get_settings() returns cached singleton."""
        # Clear the cache first
        get_settings.cache_clear()

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2, "Should return same instance"

    def test_settings_missing_env_file(self):
        """Settings() works without .env file."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings is not None

    def test_settings_extra_fields_ignored(self):
        """Settings ignores unknown environment variables."""
        with patch.dict(os.environ, {"UNKNOWN_VAR": "some_value"}):
            settings = Settings()
            assert settings is not None
