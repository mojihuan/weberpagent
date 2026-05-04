"""Tests for MonitoredAgent dead code removal (CORR-01/CORR-03).

Verifies that create_step_callback() has been removed and that existing
functionality (_prepare_context, _execute_actions, constructors) is intact.
"""

from unittest.mock import patch

from backend.agent import __all__ as agent_exports
from backend.agent.monitored_agent import MonitoredAgent


class TestDeadCodeRemoval:
    """Verify create_step_callback dead code is removed."""

    def test_no_create_step_callback(self) -> None:
        """create_step_callback should not exist on MonitoredAgent (CORR-01/CORR-03)."""
        assert not hasattr(MonitoredAgent, "create_step_callback"), (
            "create_step_callback should be removed (CORR-01/CORR-03: dead code)"
        )


class TestMonitoredAgentIntegrity:
    """Verify MonitoredAgent still functions correctly after dead code removal."""

    def test_monitored_agent_instantiates(self) -> None:
        """MonitoredAgent can be instantiated (constructor unaffected)."""
        with patch.object(MonitoredAgent.__mro__[1], "__init__", return_value=None):
            agent = MonitoredAgent(
                stall_detector=None,
                pre_submit_guard=None,
                task_progress_tracker=None,
                task="test task",
            )
            assert hasattr(agent, "_stall_detector")
            assert hasattr(agent, "_pre_submit_guard")
            assert hasattr(agent, "_task_tracker")
            assert hasattr(agent, "_pending_interventions")
            assert agent._pending_interventions == []

    def test_monitored_agent_has_expected_methods(self) -> None:
        """MonitoredAgent retains _prepare_context and _execute_actions."""
        assert hasattr(MonitoredAgent, "_prepare_context")
        assert hasattr(MonitoredAgent, "_execute_actions")

    def test_agent_init_exports(self) -> None:
        """backend.agent.__init__ still exports MonitoredAgent."""
        from backend.agent import MonitoredAgent as ImportedAgent

        assert ImportedAgent is MonitoredAgent
        assert "MonitoredAgent" in agent_exports
