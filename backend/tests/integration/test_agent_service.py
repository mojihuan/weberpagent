"""Integration tests for AgentService

Tests FND-04: LLM configuration through AgentService
"""
import pytest


class TestAgentServiceIntegration:
    """Integration tests for AgentService - placeholders for Plan 01-04"""

    @pytest.mark.skip(reason="Implemented in Plan 01-04 Task 4")
    @pytest.mark.asyncio
    async def test_agent_service_uses_llm_config(self):
        """AgentService.run_with_streaming passes LLM config to create_llm"""
        pass

    @pytest.mark.skip(reason="Implemented in Plan 01-04 Task 4")
    @pytest.mark.asyncio
    async def test_agent_service_default_temperature(self):
        """When no llm_config provided, AgentService uses create_llm defaults"""
        pass
