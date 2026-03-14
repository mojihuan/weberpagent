"""Unit tests for LLM configuration

Tests FND-04: LLM deterministic configuration
"""
import pytest
from unittest.mock import patch, MagicMock


class TestCreateLLM:
    """Tests for create_llm() in backend/llm/factory.py"""

    def test_create_llm_temperature_default(self):
        """create_llm() returns temperature=0.0 by default"""
        import backend.llm.factory as factory_module

        mock_instance = MagicMock()
        mock_instance.model = "test-model"
        mock_instance.provider = "test"

        # Mock the ChatOpenAI that gets imported inside the function
        mock_chat_class = MagicMock(return_value=mock_instance)

        # Patch where the function looks up BrowserUseChatOpenAI at runtime
        original_code = factory_module.create_llm.__code__

        # Since BrowserUseChatOpenAI is imported inside the function,
        # we need to patch at the browser_use module level
        with patch('browser_use.llm.openai.chat.ChatOpenAI', mock_chat_class):
            from backend.llm.factory import create_llm
            create_llm()

            # Verify temperature=0.0 was passed
            call_kwargs = mock_chat_class.call_args[1]
            assert call_kwargs["temperature"] == 0.0, "Default temperature should be 0.0"

    def test_create_llm_temperature_from_config(self):
        """create_llm() respects provided temperature in config"""
        mock_instance = MagicMock()
        mock_instance.model = "test-model"
        mock_instance.provider = "test"

        mock_chat_class = MagicMock(return_value=mock_instance)

        with patch('browser_use.llm.openai.chat.ChatOpenAI', mock_chat_class):
            from backend.llm.factory import create_llm
            create_llm({"temperature": 0.5})

            call_kwargs = mock_chat_class.call_args[1]
            assert call_kwargs["temperature"] == 0.5, "Should use provided temperature"


class TestGetLLMConfig:
    """Tests for get_llm_config() in backend/api/routes/runs.py"""

    def test_get_llm_config_uses_settings(self):
        """get_llm_config() uses centralized Settings"""
        from backend.api.routes.runs import get_llm_config

        with patch('backend.api.routes.runs.get_settings') as mock_get_settings:
            mock_settings = MagicMock()
            mock_settings.llm_model = "test-model"
            mock_settings.llm_base_url = "https://test.api.com/v1"
            mock_settings.llm_temperature = 0.0
            mock_settings.dashscope_api_key = "test-key"
            mock_settings.openai_api_key = ""
            mock_get_settings.return_value = mock_settings

            config = get_llm_config()

            assert config["model"] == "test-model"
            assert config["base_url"] == "https://test.api.com/v1"
            assert config["temperature"] == 0.0
            assert config["api_key"] == "test-key"

    def test_get_llm_config_temperature_zero(self):
        """get_llm_config() returns temperature=0.0"""
        from backend.api.routes.runs import get_llm_config

        with patch('backend.api.routes.runs.get_settings') as mock_get_settings:
            mock_settings = MagicMock()
            mock_settings.llm_model = "qwen3.5-plus"
            mock_settings.llm_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            mock_settings.llm_temperature = 0.0
            mock_settings.dashscope_api_key = ""
            mock_settings.openai_api_key = "openai-key"
            mock_get_settings.return_value = mock_settings

            config = get_llm_config()

            assert config["temperature"] == 0.0, "Temperature must be 0.0 for determinism"

    def test_get_llm_config_prefers_dashscope_key(self):
        """get_llm_config() prefers dashscope_api_key over openai_api_key"""
        from backend.api.routes.runs import get_llm_config

        with patch('backend.api.routes.runs.get_settings') as mock_get_settings:
            mock_settings = MagicMock()
            mock_settings.llm_model = "qwen3.5-plus"
            mock_settings.llm_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            mock_settings.llm_temperature = 0.0
            mock_settings.dashscope_api_key = "dashscope-key"
            mock_settings.openai_api_key = "openai-key"
            mock_get_settings.return_value = mock_settings

            config = get_llm_config()

            assert config["api_key"] == "dashscope-key", "Should prefer DashScope key"
