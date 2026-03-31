"""Unit tests for AgentService LLM temperature configuration.

Tests SVC-03: Verify LLM temperature=0 for deterministic test execution.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestScanTestFiles:
    """Verify scan_test_files returns correct file paths."""

    def test_scan_test_files_returns_list(self):
        """scan_test_files() must return a list of strings."""
        from backend.core.agent_service import scan_test_files

        result = scan_test_files()
        assert isinstance(result, list)
        assert all(isinstance(p, str) for p in result)

    def test_scan_test_files_returns_absolute_paths(self):
        """Each path returned by scan_test_files() must be absolute."""
        from backend.core.agent_service import scan_test_files

        result = scan_test_files()
        for path in result:
            assert path.startswith("/"), f"Path is not absolute: {path}"

    @patch("backend.core.agent_service.Path")
    def test_scan_test_files_handles_missing_dir(self, mock_path_cls):
        """scan_test_files() returns empty list when directory does not exist."""
        mock_dir = MagicMock()
        mock_dir.exists.return_value = False
        mock_path_cls.return_value = mock_dir

        from backend.core.agent_service import scan_test_files

        result = scan_test_files()
        assert result == []


class TestLLMTemperature:
    """Verify LLM temperature configuration (SVC-03)"""

    def test_default_temperature_is_zero(self):
        """Settings.llm_temperature defaults to 0.0 for deterministic output"""
        from backend.config import Settings

        # Create settings without explicit temperature
        settings = Settings()

        assert settings.llm_temperature == 0.0

    @patch("backend.api.routes.runs.get_settings")
    def test_llm_temperature_uses_settings(self, mock_get_settings):
        """get_llm_config() returns temperature from Settings"""
        from backend.api.routes.runs import get_llm_config
        from backend.config import Settings

        # Mock settings with custom temperature
        mock_settings = Settings(llm_temperature=0.0)
        mock_get_settings.return_value = mock_settings

        config = get_llm_config()

        assert config["temperature"] == 0.0

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_llm_config_passed_to_create_llm(self, mock_chat_openai):
        """Temperature from config is passed to ChatOpenAI constructor"""
        from backend.llm.factory import create_llm

        mock_instance = MagicMock()
        mock_instance.model = "test-model"
        mock_instance.provider = "test"
        mock_chat_openai.return_value = mock_instance

        llm_config = {
            "model": "gpt-4o",
            "api_key": "test-key",
            "base_url": "https://api.example.com",
            "temperature": 0.0,
        }

        create_llm(llm_config)

        # Verify ChatOpenAI was called with temperature=0.0
        mock_chat_openai.assert_called_once()
        call_kwargs = mock_chat_openai.call_args.kwargs
        assert call_kwargs["temperature"] == 0.0
