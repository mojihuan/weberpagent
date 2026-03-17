"""Unit tests for weberp_path configuration in Settings."""
import os
from unittest.mock import patch

import pytest

from backend.config.settings import Settings, get_settings


class TestWeberpPathSettings:
    """Tests for weberp_path field in Settings."""

    def test_weberp_path_default_none(self):
        """weberp_path defaults to None when not configured."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.weberp_path is None

    def test_weberp_path_from_env(self):
        """weberp_path loads from WEBERP_PATH env var."""
        with patch.dict(
            os.environ,
            {"WEBERP_PATH": "/path/to/webseleniumerp"},
            clear=True
        ):
            settings = Settings()
            assert settings.weberp_path == "/path/to/webseleniumerp"

    def test_weberp_path_optional_string(self):
        """weberp_path accepts string or None."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            # Should be None (type: str | None)
            assert settings.weberp_path is None

        with patch.dict(
            os.environ,
            {"WEBERP_PATH": "/another/path"},
            clear=True
        ):
            settings = Settings()
            assert isinstance(settings.weberp_path, str)
            assert settings.weberp_path == "/another/path"
