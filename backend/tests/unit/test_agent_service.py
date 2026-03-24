"""Unit tests for AgentService LLM temperature configuration.

Tests SVC-03: Verify LLM temperature=0 for deterministic test execution.
Tests LOOP-01: LoopInterventionTracker for early loop intervention.
"""
import pytest
from unittest.mock import patch, MagicMock


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


class TestLoopInterventionTracker:
    """Test LoopInterventionTracker for early loop intervention (LOOP-01)

    Per D-01:
    - Trigger: stagnation >= 5 (5 consecutive page states without change)
    - Intervention: Return prompt message suggesting different approaches
    """

    def test_loop_intervention_trigger(self):
        """stagnation >= 5 returns should_intervene() == True"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker(stagnation_threshold=5)

        # Record 5 stagnant page states with SAME url and dom_hash
        for _ in range(5):
            tracker.record_page_state("http://example.com", "hash123")

        assert tracker.should_intervene() is True

    def test_intervention_message(self):
        """get_intervention_message() contains expected Chinese text"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker(stagnation_threshold=5)

        # Record 5 stagnant page states
        for _ in range(5):
            tracker.record_page_state("http://example.com", "hash123")

        message = tracker.get_intervention_message()

        # Assert message contains stagnation count and suggestion keywords
        assert "5" in message
        assert ("滚动页面" in message or "选择器" in message)

    def test_record_action_updates_hashes(self):
        """record_action() adds to recent_actions"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker()

        tracker.record_action("click", {"index": 1})

        assert len(tracker.recent_actions) == 1
        assert tracker.recent_actions[0]["action"] == "click"

    def test_record_page_state_increments_stagnation(self):
        """same fingerprint increments consecutive_stagnant_pages"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker()

        # Call twice with SAME values - stagnation should be 2
        tracker.record_page_state("http://example.com", "hash123")
        assert tracker.consecutive_stagnant_pages == 1  # First occurrence

        tracker.record_page_state("http://example.com", "hash123")
        assert tracker.consecutive_stagnant_pages == 2  # Second consecutive

    def test_diagnostic_info_structure(self):
        """get_diagnostic_info() returns dict with stagnation, recent_actions keys"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker()
        tracker.record_action("click", {"index": 1})
        tracker.record_action("input", {"index": 2, "text": "test"})

        info = tracker.get_diagnostic_info()

        # Assert required keys exist
        assert "stagnation" in info
        assert "max_repetition_count" in info
        assert "recent_actions" in info
        assert "intervention_triggered" in info

    def test_different_page_resets_stagnation(self):
        """Different page state resets consecutive_stagnant_pages"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker(stagnation_threshold=5)

        # Record 3 stagnant states
        for _ in range(3):
            tracker.record_page_state("http://example.com", "hash123")
        assert tracker.consecutive_stagnant_pages == 3  # 3 consecutive same states

        # Record different page state - resets to 1 (first occurrence of new state)
        tracker.record_page_state("http://example.com", "hash456")
        assert tracker.consecutive_stagnant_pages == 1  # First occurrence of new state

    def test_should_not_intervene_below_threshold(self):
        """should_intervene() returns False when stagnation < threshold"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker(stagnation_threshold=5)

        # Record only 3 stagnant states (below threshold of 5)
        for _ in range(3):
            tracker.record_page_state("http://example.com", "hash123")

        assert tracker.should_intervene() is False
