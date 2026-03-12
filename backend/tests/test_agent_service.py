"""测试 Agent 服务"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.core.agent_service import AgentService


@pytest.fixture
def agent_service():
    return AgentService()


def test_agent_service_creation(agent_service):
    """测试服务创建"""
    assert agent_service is not None


@pytest.mark.asyncio
async def test_run_simple_mock(agent_service):
    """测试简单执行（Mock）"""
    with (
        patch("backend.core.agent_service.Agent") as MockAgent,
        patch("backend.core.agent_service.create_llm") as mock_create_llm,
    ):
        # Mock LLM
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm

        # Mock Agent
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock()
        mock_agent.run.return_value = MagicMock(is_done=True)
        MockAgent.return_value = mock_agent

        result = await agent_service.run_simple(task="打开网页")

        assert result is not None
        mock_agent.run.assert_called_once()
        mock_create_llm.assert_called_once_with(None)


@pytest.mark.asyncio
async def test_run_with_callback(agent_service):
    """测试带回调的执行"""
    with (
        patch("backend.core.agent_service.Agent") as MockAgent,
        patch("backend.core.agent_service.create_llm") as mock_create_llm,
    ):
        # Mock LLM
        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm

        # Mock Agent
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock()
        mock_agent.run.return_value = MagicMock(is_done=True)
        MockAgent.return_value = mock_agent

        steps = []

        def on_step(step, action, reasoning, screenshot):
            steps.append({"step": step, "action": action})

        result = await agent_service.run_with_streaming(
            task="打开网页", on_step=on_step
        )

        assert result is not None
        mock_create_llm.assert_called_once_with(None)
