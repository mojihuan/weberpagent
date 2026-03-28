"""Unit tests for MonitoredAgent -- Agent subclass wiring 3 detectors.

Tests use mocked browser-use internals (no real browser/LLM needed).
Covers SUB-01 (_prepare_context injection), SUB-02 (step_callback),
and SUB-03 (_execute_actions blocking).
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.agent.pre_submit_guard import GuardResult, PreSubmitGuard
from backend.agent.stall_detector import StallDetector, StallResult
from backend.agent.task_progress_tracker import (
    ProgressResult,
    TaskProgressTracker,
)


# ---------------------------------------------------------------------------
# Helper: create MonitoredAgent with mocked internals
# ---------------------------------------------------------------------------


def _make_monitored_agent(
    task: str = "Test task",
    stall_detector: StallDetector | None = None,
    pre_submit_guard: PreSubmitGuard | None = None,
    task_tracker: TaskProgressTracker | None = None,
) -> "MonitoredAgent":
    """Create MonitoredAgent with mocked Agent.__init__ internals."""
    with patch("backend.agent.monitored_agent.Agent.__init__", return_value=None):
        from backend.agent.monitored_agent import MonitoredAgent

        agent = MonitoredAgent(
            stall_detector=stall_detector,
            pre_submit_guard=pre_submit_guard,
            task_progress_tracker=task_tracker,
        )
        # Manually set attributes that Agent.__init__ would set
        agent.task = task
        agent._message_manager = MagicMock()
        agent._message_manager._add_context_message = MagicMock()
        agent.state = MagicMock()
        agent.state.n_steps = 0
        agent.state.last_model_output = None
        agent.state.last_result = None
        return agent


# ---------------------------------------------------------------------------
# SUB-01: _prepare_context() injects pending interventions
# ---------------------------------------------------------------------------


class TestPrepareContextInjectsInterventions:
    """_prepare_context() must inject _pending_interventions after super() call."""

    @pytest.mark.asyncio
    async def test_injects_single_intervention(self) -> None:
        """_prepare_context injects pending interventions via _add_context_message."""
        agent = _make_monitored_agent()
        agent._pending_interventions = ["test intervention"]

        # Mock super()._prepare_context
        with patch(
            "backend.agent.monitored_agent.Agent._prepare_context",
            new_callable=AsyncMock,
            return_value=MagicMock(),
        ):
            await agent._prepare_context()

        # Verify _add_context_message was called with UserMessage
        assert agent._message_manager._add_context_message.call_count == 1
        call_args = agent._message_manager._add_context_message.call_args[0][0]
        assert hasattr(call_args, "content")
        assert call_args.content == "test intervention"

        # Verify _pending_interventions is cleared
        assert agent._pending_interventions == []

    @pytest.mark.asyncio
    async def test_clears_after_injection(self) -> None:
        """_prepare_context clears _pending_interventions after injecting all messages."""
        agent = _make_monitored_agent()
        agent._pending_interventions = ["msg1", "msg2"]

        with patch(
            "backend.agent.monitored_agent.Agent._prepare_context",
            new_callable=AsyncMock,
            return_value=MagicMock(),
        ):
            await agent._prepare_context()

        assert agent._message_manager._add_context_message.call_count == 2
        assert agent._pending_interventions == []

    @pytest.mark.asyncio
    async def test_empty_interventions_noop(self) -> None:
        """_prepare_context does not call _add_context_message when no interventions."""
        agent = _make_monitored_agent()
        agent._pending_interventions = []

        with patch(
            "backend.agent.monitored_agent.Agent._prepare_context",
            new_callable=AsyncMock,
            return_value=MagicMock(),
        ):
            await agent._prepare_context()

        agent._message_manager._add_context_message.assert_not_called()
        assert agent._pending_interventions == []


# ---------------------------------------------------------------------------
# SUB-02: step_callback stores interventions in _pending_interventions
# ---------------------------------------------------------------------------


class TestStepCallback:
    """step_callback stores detector results in _pending_interventions, not _add_context_message."""

    @pytest.mark.asyncio
    async def test_stores_stall_intervention(self) -> None:
        """step_callback appends stall message to _pending_interventions."""
        # Create a stall detector that will trigger on consecutive failures
        detector = StallDetector(max_consecutive_failures=2)
        agent = _make_monitored_agent(
            task="Test task",
            stall_detector=detector,
        )

        # Build mock browser_state with dom_state
        mock_dom_state = MagicMock()
        mock_dom_state.llm_representation.return_value = "test dom content"
        mock_browser_state = MagicMock()
        mock_browser_state.dom_state = mock_dom_state

        # Build mock agent_output with click action and failure evaluation
        mock_action = MagicMock()
        mock_action.model_dump.return_value = {"click": {"index": 5}}
        mock_output = MagicMock()
        mock_output.action = [mock_action]
        mock_output.evaluation_previous_goal = "Failed to click element"

        callback = agent.create_step_callback()

        # First failure
        await callback(mock_browser_state, mock_output, 1)
        # Second failure -- should trigger stall
        await callback(mock_browser_state, mock_output, 2)

        assert len(agent._pending_interventions) > 0

    @pytest.mark.asyncio
    async def test_does_not_call_add_context_message(self) -> None:
        """step_callback modifies _pending_interventions, not _add_context_message."""
        agent = _make_monitored_agent()

        mock_dom_state = MagicMock()
        mock_dom_state.llm_representation.return_value = "dom"
        mock_browser_state = MagicMock()
        mock_browser_state.dom_state = mock_dom_state

        mock_action = MagicMock()
        mock_action.model_dump.return_value = {"click": {"index": 1}}
        mock_output = MagicMock()
        mock_output.action = [mock_action]
        mock_output.evaluation_previous_goal = "Success"

        # Reset the mock to clear any constructor calls
        agent._message_manager._add_context_message.reset_mock()

        callback = agent.create_step_callback()
        await callback(mock_browser_state, mock_output, 1)

        agent._message_manager._add_context_message.assert_not_called()


# ---------------------------------------------------------------------------
# SUB-03: _execute_actions() blocks submit when guard triggers
# ---------------------------------------------------------------------------


class TestExecuteActionsBlocking:
    """_execute_actions() blocks submit click when PreSubmitGuard returns should_block=True."""

    @pytest.mark.asyncio
    async def test_blocks_submit_click(self) -> None:
        """_execute_actions blocks and sets ActionResult.error when guard triggers."""
        guard = PreSubmitGuard()
        agent = _make_monitored_agent(
            task="销售金额：150元",
            pre_submit_guard=guard,
        )

        # Mock last_model_output with a click action
        mock_action = MagicMock()
        mock_action.model_dump.return_value = {"click": {"index": 3}}
        agent.state.last_model_output = MagicMock()
        agent.state.last_model_output.action = [mock_action]

        # Patch guard.check to return should_block=True
        with patch.object(
            guard,
            "check",
            return_value=GuardResult(
                should_block=True, message="【提交拦截】字段不匹配"
            ),
        ):
            with patch(
                "backend.agent.monitored_agent.Agent._execute_actions",
                new_callable=AsyncMock,
            ) as mock_super:
                await agent._execute_actions()

                # super()._execute_actions should NOT be called
                mock_super.assert_not_called()

        # last_result should have ActionResult with error
        assert agent.state.last_result is not None
        assert len(agent.state.last_result) == 1
        assert agent.state.last_result[0].error == "【提交拦截】字段不匹配"

    @pytest.mark.asyncio
    async def test_allows_non_click_action(self) -> None:
        """_execute_actions delegates to super() for non-click actions."""
        agent = _make_monitored_agent()

        # Mock last_model_output with an input action (not click)
        mock_action = MagicMock()
        mock_action.model_dump.return_value = {"input": {"text": "hello", "index": 1}}
        agent.state.last_model_output = MagicMock()
        agent.state.last_model_output.action = [mock_action]

        with patch(
            "backend.agent.monitored_agent.Agent._execute_actions",
            new_callable=AsyncMock,
        ) as mock_super:
            await agent._execute_actions()
            mock_super.assert_called_once()

    @pytest.mark.asyncio
    async def test_delegates_on_none_output(self) -> None:
        """_execute_actions delegates to super() when last_model_output is None."""
        agent = _make_monitored_agent()
        agent.state.last_model_output = None

        with patch(
            "backend.agent.monitored_agent.Agent._execute_actions",
            new_callable=AsyncMock,
        ) as mock_super:
            await agent._execute_actions()
            mock_super.assert_called_once()


# ---------------------------------------------------------------------------
# D-07/D-08: Fault tolerance -- detector exceptions do not crash agent
# ---------------------------------------------------------------------------


class TestDetectorFaultTolerance:
    """Detector exceptions are caught and logged, not propagated."""

    @pytest.mark.asyncio
    async def test_step_callback_catches_detector_exception(self) -> None:
        """step_callback catches exceptions from detectors and does not crash."""
        detector = StallDetector()
        agent = _make_monitored_agent(stall_detector=detector)

        mock_browser_state = MagicMock()
        mock_browser_state.dom_state = None

        mock_output = MagicMock()
        mock_output.action = []
        mock_output.evaluation_previous_goal = ""

        callback = agent.create_step_callback()

        # Patch stall_detector.check to raise
        with patch.object(
            detector, "check", side_effect=Exception("detector crash")
        ):
            # Should NOT raise
            await callback(mock_browser_state, mock_output, 1)

        # Agent should still be functional
        assert agent._pending_interventions is not None
