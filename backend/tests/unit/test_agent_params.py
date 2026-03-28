"""Unit tests for Agent constructor parameter injection in agent_service.py.

Tests TUNE-01~04: Verify ENHANCED_SYSTEM_MESSAGE import and tuned browser-use
parameters are passed to the Agent() constructor.

TDD RED phase: These tests should FAIL until agent_service.py is updated.
"""

from __future__ import annotations

import inspect
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE


# ---------------------------------------------------------------------------
# Helper: invoke run_with_streaming and capture Agent() kwargs
# ---------------------------------------------------------------------------


async def _invoke_run_with_streaming(mock_agent_cls):
    """Call AgentService.run_with_streaming with mocked deps, return Agent kwargs."""
    from backend.core.agent_service import AgentService

    svc = AgentService(output_dir="/tmp/test_outputs")

    mock_instance = AsyncMock()
    mock_run_result = MagicMock()
    mock_run_result.is_successful.return_value = True
    mock_instance.run = AsyncMock(return_value=mock_run_result)
    mock_agent_cls.return_value = mock_instance

    async def noop_on_step(*args, **kwargs):
        pass

    with patch("backend.core.agent_service.create_llm", return_value=MagicMock()):
        with patch("backend.core.agent_service.create_browser_session", return_value=MagicMock()):
            await svc.run_with_streaming(
                task="test task",
                run_id="test-run",
                on_step=noop_on_step,
                max_steps=1,
            )

    return mock_agent_cls.call_args.kwargs


# ---------------------------------------------------------------------------
# Test 1: ENHANCED_SYSTEM_MESSAGE import exists in agent_service module
# ---------------------------------------------------------------------------


class TestAgentParams:
    """Verify Agent() receives correct parameters from agent_service.py."""

    def test_imports_enhanced_system_message(self):
        """agent_service.py imports ENHANCED_SYSTEM_MESSAGE from backend.agent.prompts."""
        from backend.core import agent_service

        assert hasattr(agent_service, "ENHANCED_SYSTEM_MESSAGE"), (
            "agent_service module must import ENHANCED_SYSTEM_MESSAGE"
        )
        assert agent_service.ENHANCED_SYSTEM_MESSAGE is ENHANCED_SYSTEM_MESSAGE, (
            "agent_service.ENHANCED_SYSTEM_MESSAGE must reference the same object"
        )

    @pytest.mark.asyncio
    async def test_extend_system_message_passed(self):
        """Agent() receives extend_system_message=ENHANCED_SYSTEM_MESSAGE."""
        with patch("backend.core.agent_service.Agent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert "extend_system_message" in kwargs, (
            "Agent() must receive extend_system_message kwarg"
        )
        assert kwargs["extend_system_message"] == ENHANCED_SYSTEM_MESSAGE, (
            "extend_system_message must equal ENHANCED_SYSTEM_MESSAGE"
        )
        assert len(kwargs["extend_system_message"].strip()) > 0, (
            "extend_system_message must not be empty"
        )

    @pytest.mark.asyncio
    async def test_loop_detection_window_is_10(self):
        """Agent() receives loop_detection_window=10 (TUNE-01, down from default 20)."""
        with patch("backend.core.agent_service.Agent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("loop_detection_window") == 10, (
            f"loop_detection_window must be 10, got {kwargs.get('loop_detection_window')}"
        )

    @pytest.mark.asyncio
    async def test_max_failures_is_4(self):
        """Agent() receives max_failures=4 (TUNE-02, down from default 5)."""
        with patch("backend.core.agent_service.Agent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("max_failures") == 4, (
            f"max_failures must be 4, got {kwargs.get('max_failures')}"
        )

    @pytest.mark.asyncio
    async def test_planning_replan_on_stall_is_2(self):
        """Agent() receives planning_replan_on_stall=2 (TUNE-03, down from default 3)."""
        with patch("backend.core.agent_service.Agent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("planning_replan_on_stall") == 2, (
            f"planning_replan_on_stall must be 2, got {kwargs.get('planning_replan_on_stall')}"
        )

    @pytest.mark.asyncio
    async def test_enable_planning_is_true(self):
        """Agent() receives enable_planning=True (TUNE-04, confirmed)."""
        with patch("backend.core.agent_service.Agent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("enable_planning") is True, (
            f"enable_planning must be True, got {kwargs.get('enable_planning')}"
        )
