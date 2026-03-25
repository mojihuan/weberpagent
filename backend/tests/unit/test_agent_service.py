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

    def test_diagnostic_info_includes_stagnation(self):
        """get_diagnostic_info() returns dict with stagnation value"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker()
        tracker.record_page_state("http://example.com", "hash123")
        tracker.record_page_state("http://example.com", "hash123")  # Same = stagnation

        diagnostic = tracker.get_diagnostic_info()

        assert "stagnation" in diagnostic
        assert diagnostic["stagnation"] == 2

    def test_diagnostic_info_includes_recent_actions(self):
        """get_diagnostic_info() returns dict with recent_actions list"""
        from backend.core.agent_service import LoopInterventionTracker

        tracker = LoopInterventionTracker()
        tracker.record_action("click", {"index": 1})
        tracker.record_action("input", {"index": 2, "text": "test"})

        diagnostic = tracker.get_diagnostic_info()

        assert "recent_actions" in diagnostic
        assert isinstance(diagnostic["recent_actions"], list)
        assert len(diagnostic["recent_actions"]) == 2
        assert diagnostic["recent_actions"][0]["action"] == "click"


class TestTDPostProcessing:
    """TD 后处理功能测试 (DOM-01)

    Per D-01, D-02, D-03, D-04: 测试 td 点击后焦点转移逻辑
    """

    @pytest.mark.asyncio
    async def test_not_td_element(self):
        """测试非 td 元素点击"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={'is_td': False})

        service = AgentService()
        result = await service._post_process_td_click(mock_page)

        assert result['is_td'] is False

    @pytest.mark.asyncio
    async def test_td_with_input(self):
        """测试 td 内有输入框"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'is_td': True,
            'input_found': True,
            'input_tag': 'input',
            'input_type': 'text',
            'focus_transferred': True
        })

        service = AgentService()
        result = await service._post_process_td_click(mock_page)

        assert result['is_td'] is True
        assert result['input_found'] is True
        assert result['focus_transferred'] is True

    @pytest.mark.asyncio
    async def test_td_without_input(self):
        """测试 td 内无输入框"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'is_td': True,
            'input_found': False
        })

        service = AgentService()
        result = await service._post_process_td_click(mock_page)

        assert result['is_td'] is True
        assert result['input_found'] is False

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """测试异常处理 - 返回 is_td: false 和 error 信息"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(side_effect=Exception("Browser error"))

        service = AgentService()
        result = await service._post_process_td_click(mock_page)

        assert result['is_td'] is False
        assert 'error' in result

    @pytest.mark.asyncio
    async def test_textarea_focus(self):
        """测试 td 内有 textarea - 正确识别并转移焦点"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'is_td': True,
            'input_found': True,
            'input_tag': 'textarea',
            'input_type': None,
            'focus_transferred': True
        })

        service = AgentService()
        result = await service._post_process_td_click(mock_page)

        assert result['is_td'] is True
        assert result['input_tag'] == 'textarea'

    @pytest.mark.asyncio
    async def test_select_focus(self):
        """测试 td 内有 select - 正确识别并转移焦点"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'is_td': True,
            'input_found': True,
            'input_tag': 'select',
            'input_type': None,
            'focus_transferred': True
        })

        service = AgentService()
        result = await service._post_process_td_click(mock_page)

        assert result['is_td'] is True
        assert result['input_tag'] == 'select'


class TestFallbackInput:
    """Fallback input 功能测试 (FALLBACK-01)

    Per D-01, D-02, D-03, D-07: 测试 JavaScript 降级输入逻辑
    """

    @pytest.mark.asyncio
    async def test_fallback_input_td_with_input(self):
        """测试 td 内有输入框 - 成功设置值"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'success': True,
            'target_tag': 'input',
            'target_type': 'text',
            'value_set': '100'
        })

        service = AgentService()
        result = await service._fallback_input(mock_page, {'index': 5, 'text': '100'})

        assert result['success'] is True
        assert result['target_tag'] == 'input'
        assert result['value_set'] == '100'

    @pytest.mark.asyncio
    async def test_fallback_input_td_not_found(self):
        """测试 td 索引无效"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'success': False,
            'error': 'td_not_found',
            'index': 999
        })

        service = AgentService()
        result = await service._fallback_input(mock_page, {'index': 999, 'text': '100'})

        assert result['success'] is False
        assert result['error'] == 'td_not_found'

    @pytest.mark.asyncio
    async def test_fallback_input_no_input_in_td(self):
        """测试 td 内无输入框"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value={
            'success': False,
            'error': 'no_input_in_td',
            'index': 5
        })

        service = AgentService()
        result = await service._fallback_input(mock_page, {'index': 5, 'text': '100'})

        assert result['success'] is False
        assert result['error'] == 'no_input_in_td'

    @pytest.mark.asyncio
    async def test_fallback_input_missing_index(self):
        """测试缺少 index 参数"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        mock_page = MagicMock()
        service = AgentService()
        result = await service._fallback_input(mock_page, {'text': '100'})

        assert result['success'] is False
        assert result['error'] == 'missing_index'

    @pytest.mark.asyncio
    async def test_fallback_input_exception_handling(self):
        """测试异常处理"""
        from backend.core.agent_service import AgentService
        from unittest.mock import AsyncMock, MagicMock

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(side_effect=Exception("Browser error"))

        service = AgentService()
        result = await service._fallback_input(mock_page, {'index': 5, 'text': '100'})

        assert result['success'] is False
        assert 'error' in result
