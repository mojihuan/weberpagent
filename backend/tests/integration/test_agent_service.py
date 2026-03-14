"""Integration tests for AgentService

Tests FND-04: LLM configuration through AgentService
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock


class TestAgentServiceIntegration:
    """Integration tests for AgentService LLM configuration"""

    @pytest.mark.asyncio
    async def test_agent_service_uses_llm_config(self):
        """AgentService.run_simple passes LLM config to create_llm"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        with patch('backend.core.agent_service.create_llm') as mock_create_llm:
            with patch('backend.core.agent_service.Agent') as mock_agent_class:
                mock_llm = MagicMock()
                mock_create_llm.return_value = mock_llm

                mock_agent = MagicMock()
                mock_agent.run = AsyncMock()
                mock_agent.run.return_value = MagicMock(is_successful=lambda: True)
                mock_agent_class.return_value = mock_agent

                llm_config = {
                    "model": "test-model",
                    "temperature": 0.0,
                    "api_key": "test-key",
                    "base_url": "https://test.api.com/v1"
                }

                await service.run_simple(
                    task="Test task",
                    max_steps=1,
                    llm_config=llm_config
                )

                # Verify create_llm was called with the config
                mock_create_llm.assert_called_once_with(llm_config)

    @pytest.mark.asyncio
    async def test_agent_service_default_temperature(self):
        """When no llm_config provided, AgentService uses create_llm defaults (temperature=0.0)"""
        from backend.core.agent_service import AgentService

        service = AgentService()

        with patch('backend.core.agent_service.create_llm') as mock_create_llm:
            with patch('backend.core.agent_service.Agent') as mock_agent_class:
                mock_llm = MagicMock()
                mock_create_llm.return_value = mock_llm

                mock_agent = MagicMock()
                mock_agent.run = AsyncMock()
                mock_agent.run.return_value = MagicMock(is_successful=lambda: True)
                mock_agent_class.return_value = mock_agent

                await service.run_simple(
                    task="Test task",
                    max_steps=1,
                    llm_config=None  # No config provided
                )

                # Verify create_llm was called with None (uses defaults)
                mock_create_llm.assert_called_once_with(None)
