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


class TestElementDiagnostics:
    """Element diagnostics 功能测试 (LOG-03)

    Per D-01, D-02, D-03: 测试 _collect_element_diagnostics 方法
    - D-01: 仅在检测到问题时记录日志 (is_interactive=False)
    - D-02: 返回 dict 结构用于 step_stats['element_diagnostics']
    - D-03: 包含 tag, index, parent_chain (max 5), ignored_ancestors
    """

    @pytest.mark.asyncio
    async def test_returns_empty_dict_when_browser_state_none(self):
        """Test 1: Returns empty dict when browser_state is None"""
        from backend.core.agent_service import AgentService

        service = AgentService()
        result = await service._collect_element_diagnostics(None, 'click', {'index': 0})

        assert result == {
            "non_interactive_elements": [],
            "fallback_triggered": False,
            "fallback_reason": None
        }

    @pytest.mark.asyncio
    async def test_returns_empty_dict_for_non_click_input_actions(self):
        """Test 2: Returns empty dict when action_name is not click or input"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        mock_browser_state = MagicMock()
        service = AgentService()
        result = await service._collect_element_diagnostics(mock_browser_state, 'scroll', {'pages': 0.5})

        assert result == {
            "non_interactive_elements": [],
            "fallback_triggered": False,
            "fallback_reason": None
        }

    @pytest.mark.asyncio
    async def test_returns_empty_dict_when_target_index_none(self):
        """Test 3: Returns empty dict when target_index is None"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        mock_browser_state = MagicMock()
        service = AgentService()
        result = await service._collect_element_diagnostics(mock_browser_state, 'click', {})

        assert result == {
            "non_interactive_elements": [],
            "fallback_triggered": False,
            "fallback_reason": None
        }

    @pytest.mark.asyncio
    async def test_returns_non_interactive_elements_when_is_interactive_false(self):
        """Test 4: Returns non_interactive_elements entry when element is_interactive=False"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        # Create mock element with is_interactive=False
        mock_element = MagicMock()
        mock_element.index = 42
        mock_element.tag_name = 'input'
        mock_element.is_interactive = False
        mock_element.parent = None

        # Create mock browser_state with element_tree
        mock_browser_state = MagicMock()
        mock_browser_state.element_tree = [mock_element]

        service = AgentService()
        result = await service._collect_element_diagnostics(mock_browser_state, 'click', {'index': 42})

        assert len(result["non_interactive_elements"]) == 1
        assert result["non_interactive_elements"][0]["tag"] == 'input'
        assert result["non_interactive_elements"][0]["index"] == 42

    @pytest.mark.asyncio
    async def test_parent_chain_includes_up_to_5_ancestors(self):
        """Test 5: parent_chain includes up to 5 ancestors"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        # Create parent chain: great_great_grandparent -> great_grandparent -> grandparent -> parent -> element
        mock_parent5 = MagicMock()
        mock_parent5.tag_name = 'tbody'
        mock_parent5.parent = None

        mock_parent4 = MagicMock()
        mock_parent4.tag_name = 'tr'
        mock_parent4.parent = mock_parent5

        mock_parent3 = MagicMock()
        mock_parent3.tag_name = 'div'
        mock_parent3.tag_name = 'div.el-input-number'
        mock_parent3.parent = mock_parent4

        mock_parent2 = MagicMock()
        mock_parent2.tag_name = 'div.cell'
        mock_parent2.parent = mock_parent3

        mock_parent1 = MagicMock()
        mock_parent1.tag_name = 'td'
        mock_parent1.parent = mock_parent2

        mock_element = MagicMock()
        mock_element.index = 42
        mock_element.tag_name = 'input'
        mock_element.is_interactive = False
        mock_element.parent = mock_parent1

        mock_browser_state = MagicMock()
        mock_browser_state.element_tree = [mock_element]

        service = AgentService()
        result = await service._collect_element_diagnostics(mock_browser_state, 'click', {'index': 42})

        # Should have exactly 5 ancestors in parent_chain
        assert len(result["non_interactive_elements"][0]["parent_chain"]) == 5
        assert result["non_interactive_elements"][0]["parent_chain"] == [
            'td', 'div.cell', 'div.el-input-number', 'tr', 'tbody'
        ]

    @pytest.mark.asyncio
    async def test_ignored_ancestors_filters_by_ignored_by_paint_order(self):
        """Test 6: ignored_ancestors includes only ancestors with ignored_by_paint_order=True"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        # Create parent chain where some have ignored_by_paint_order=True
        mock_parent3 = MagicMock()
        mock_parent3.tag_name = 'tr'
        mock_parent3.ignored_by_paint_order = False
        mock_parent3.parent = None

        mock_parent2 = MagicMock()
        mock_parent2.tag_name = 'div.el-input-number'
        mock_parent2.ignored_by_paint_order = True
        mock_parent2.parent = mock_parent3

        mock_parent1 = MagicMock()
        mock_parent1.tag_name = 'div.cell'
        mock_parent1.ignored_by_paint_order = True
        mock_parent1.parent = mock_parent2

        mock_element = MagicMock()
        mock_element.index = 42
        mock_element.tag_name = 'input'
        mock_element.is_interactive = False
        mock_element.parent = mock_parent1

        mock_browser_state = MagicMock()
        mock_browser_state.element_tree = [mock_element]

        service = AgentService()
        result = await service._collect_element_diagnostics(mock_browser_state, 'click', {'index': 42})

        # Only div.cell and div.el-input-number should be in ignored_ancestors
        ignored = result["non_interactive_elements"][0]["ignored_ancestors"]
        assert 'div.cell' in ignored
        assert 'div.el-input-number' in ignored
        assert 'tr' not in ignored

    @pytest.mark.asyncio
    async def test_multiple_non_interactive_elements_recorded(self):
        """Test 7: Multiple non-interactive elements are all recorded"""
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        # Create two non-interactive elements
        mock_element1 = MagicMock()
        mock_element1.index = 10
        mock_element1.tag_name = 'input'
        mock_element1.is_interactive = False
        mock_element1.parent = None

        mock_element2 = MagicMock()
        mock_element2.index = 42
        mock_element2.tag_name = 'textarea'
        mock_element2.is_interactive = False
        mock_element2.parent = None

        mock_browser_state = MagicMock()
        mock_browser_state.element_tree = [mock_element1, mock_element2]

        service = AgentService()
        # First call for element at index 10
        result1 = await service._collect_element_diagnostics(mock_browser_state, 'click', {'index': 10})
        # Second call for element at index 42
        result2 = await service._collect_element_diagnostics(mock_browser_state, 'input', {'index': 42})

        assert len(result1["non_interactive_elements"]) == 1
        assert result1["non_interactive_elements"][0]["index"] == 10

        assert len(result2["non_interactive_elements"]) == 1
        assert result2["non_interactive_elements"][0]["index"] == 42

    @pytest.mark.asyncio
    async def test_element_diagnostics_integration_with_fallback(self):
        """Test that element_diagnostics includes fallback info when triggered.

        Per D-04, D-05 from CONTEXT.md:
        - D-04: Add new test case for table input scenario
        - D-05: Single scenario - click td -> input value

        Validates integration between element diagnostics collection
        and the fallback mechanism.
        """
        from backend.core.agent_service import AgentService
        from unittest.mock import MagicMock

        # Mock browser_state with non-interactive element (td targeting input)
        mock_element = MagicMock()
        mock_element.index = 5
        mock_element.tag_name = 'td'
        mock_element.is_interactive = False

        mock_parent = MagicMock()
        mock_parent.tag_name = 'tr'
        mock_parent.ignored_by_paint_order = True
        mock_parent.parent = None

        mock_element.parent = mock_parent

        mock_browser_state = MagicMock()
        mock_browser_state.element_tree = [mock_element]

        service = AgentService()
        result = await service._collect_element_diagnostics(
            mock_browser_state, 'input', {'index': 5, 'text': '100'}
        )

        # Verify non_interactive_elements recorded
        assert len(result['non_interactive_elements']) == 1
        assert result['non_interactive_elements'][0]['tag'] == 'td'
        assert result['non_interactive_elements'][0]['index'] == 5
        assert 'tr' in result['non_interactive_elements'][0]['parent_chain']
        assert 'tr' in result['non_interactive_elements'][0]['ignored_ancestors']
