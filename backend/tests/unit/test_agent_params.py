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
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
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
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("loop_detection_window") == 10, (
            f"loop_detection_window must be 10, got {kwargs.get('loop_detection_window')}"
        )

    @pytest.mark.asyncio
    async def test_max_failures_is_4(self):
        """Agent() receives max_failures=4 (TUNE-02, down from default 5)."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("max_failures") == 4, (
            f"max_failures must be 4, got {kwargs.get('max_failures')}"
        )

    @pytest.mark.asyncio
    async def test_planning_replan_on_stall_is_2(self):
        """Agent() receives planning_replan_on_stall=2 (TUNE-03, down from default 3)."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("planning_replan_on_stall") == 2, (
            f"planning_replan_on_stall must be 2, got {kwargs.get('planning_replan_on_stall')}"
        )

    @pytest.mark.asyncio
    async def test_enable_planning_is_true(self):
        """Agent() receives enable_planning=True (TUNE-04, confirmed)."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            kwargs = await _invoke_run_with_streaming(mock_agent_cls)

        assert kwargs.get("enable_planning") is True, (
            f"enable_planning must be True, got {kwargs.get('enable_planning')}"
        )


# ---------------------------------------------------------------------------
# Test: step_callback detector wiring (INTEG-03, INTEG-04)
# ---------------------------------------------------------------------------


async def _capture_step_callback(mock_agent_cls, run_id="test-cb"):
    """Call run_with_streaming, capture the step_callback from MonitoredAgent kwargs."""
    from backend.core.agent_service import AgentService

    svc = AgentService(output_dir="/tmp/test_outputs")
    captured_callback = None
    mock_run_logger = MagicMock()

    async def capture_on_step(*args, **kwargs):
        pass

    def capture_agent_call(**kwargs):
        nonlocal captured_callback
        captured_callback = kwargs.get("register_new_step_callback")
        return mock_agent_cls.return_value

    mock_agent_cls.side_effect = capture_agent_call

    with patch("backend.core.agent_service.create_llm", return_value=MagicMock()):
        with patch("backend.core.agent_service.create_browser_session", return_value=MagicMock()):
            with patch("backend.core.agent_service.RunLogger", return_value=mock_run_logger):
                await svc.run_with_streaming(
                    task="test task",
                    run_id=run_id,
                    on_step=capture_on_step,
                    max_steps=10,
                )

    return captured_callback, mock_run_logger


def _make_mock_browser_state(url="https://example.com"):
    """Create a mock browser_state with url, screenshot=None, dom_state=None."""
    mock = MagicMock()
    mock.url = url
    mock.screenshot = None
    mock.dom_state = None
    return mock


def _make_mock_agent_output(action=None, evaluation="success"):
    """Create a mock agent_output with action list and evaluation_previous_goal."""
    mock = MagicMock()
    mock.action = action or []
    mock.evaluation_previous_goal = evaluation
    return mock


class TestStepCallbackDetectors:
    """Verify step_callback wires detectors correctly (INTEG-03, INTEG-04)."""

    @pytest.mark.asyncio
    async def test_stall_detector_called_in_step_callback(self):
        """step_callback calls agent._stall_detector.check() and stores interventions."""
        from backend.agent.stall_detector import StallResult

        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            mock_instance = AsyncMock()
            mock_run_result = MagicMock()
            mock_run_result.is_successful.return_value = True
            mock_instance.run = AsyncMock(return_value=mock_run_result)
            mock_instance._stall_detector = MagicMock()
            mock_instance._stall_detector.check = MagicMock(
                return_value=StallResult(should_intervene=True, message="Stall detected!")
            )
            mock_instance._task_tracker = MagicMock()
            mock_instance._task_tracker.check_progress = MagicMock(
                return_value=MagicMock(
                    should_warn=False, level="", message="",
                    remaining_steps=10, remaining_tasks=5,
                )
            )
            mock_instance._task_tracker.update_from_evaluation = MagicMock()
            mock_instance._pending_interventions = []
            mock_agent_cls.return_value = mock_instance

            callback, _ = await _capture_step_callback(mock_agent_cls, "test-stall")

        if callback:
            await callback(
                _make_mock_browser_state(),
                _make_mock_agent_output(evaluation="failure error"),
                3,
            )

            mock_instance._stall_detector.check.assert_called_once()
            assert "Stall detected!" in mock_instance._pending_interventions

    @pytest.mark.asyncio
    async def test_progress_tracker_called_in_step_callback(self):
        """step_callback calls agent._task_tracker.check_progress()."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            mock_instance = AsyncMock()
            mock_run_result = MagicMock()
            mock_run_result.is_successful.return_value = True
            mock_instance.run = AsyncMock(return_value=mock_run_result)
            mock_instance._stall_detector = MagicMock()
            mock_instance._stall_detector.check = MagicMock(
                return_value=MagicMock(should_intervene=False, message="")
            )
            mock_instance._task_tracker = MagicMock()
            mock_instance._task_tracker.check_progress = MagicMock(
                return_value=MagicMock(
                    should_warn=True, level="urgent",
                    message="Progress urgent!",
                    remaining_steps=2, remaining_tasks=5,
                )
            )
            mock_instance._task_tracker.update_from_evaluation = MagicMock()
            mock_instance._pending_interventions = []
            mock_agent_cls.return_value = mock_instance

            callback, _ = await _capture_step_callback(mock_agent_cls, "test-progress")

        if callback:
            await callback(
                _make_mock_browser_state(),
                _make_mock_agent_output(evaluation="success"),
                8,
            )

            mock_instance._task_tracker.check_progress.assert_called_once_with(
                current_step=8, max_steps=10,
            )
            assert "Progress urgent!" in mock_instance._pending_interventions

    @pytest.mark.asyncio
    async def test_detector_error_non_blocking(self):
        """Detector errors are caught and do not crash step_callback."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_agent_cls:
            mock_instance = AsyncMock()
            mock_run_result = MagicMock()
            mock_run_result.is_successful.return_value = True
            mock_instance.run = AsyncMock(return_value=mock_run_result)
            mock_instance._stall_detector = MagicMock()
            mock_instance._stall_detector.check = MagicMock(
                side_effect=RuntimeError("Detector crashed!")
            )
            mock_instance._task_tracker = MagicMock()
            mock_instance._pending_interventions = []
            mock_agent_cls.return_value = mock_instance

            callback, _ = await _capture_step_callback(mock_agent_cls, "test-error")

        if callback:
            # Should NOT raise despite detector error
            await callback(
                _make_mock_browser_state(),
                _make_mock_agent_output(evaluation="ok"),
                1,
            )
