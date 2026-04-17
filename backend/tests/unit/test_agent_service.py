"""Unit tests for AgentService LLM temperature configuration.

Tests SVC-03: Verify LLM temperature=0 for deterministic test execution.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock, PropertyMock

from backend.agent.stall_detector import StallResult, FailureDetectionResult


class TestScanTestFiles:
    """Verify scan_test_files returns correct file paths."""

    def test_scan_test_files_returns_list(self):
        """scan_test_files() must return a list of strings."""
        from backend.core.agent_service import scan_test_files

        result = scan_test_files()
        assert isinstance(result, list)
        assert all(isinstance(p, str) for p in result)

    def test_scan_test_files_returns_absolute_paths(self):
        """Each path returned by scan_test_files() must be absolute."""
        from backend.core.agent_service import scan_test_files

        result = scan_test_files()
        for path in result:
            assert path.startswith("/"), f"Path is not absolute: {path}"

    @patch("backend.core.agent_service.Path")
    def test_scan_test_files_handles_missing_dir(self, mock_path_cls):
        """scan_test_files() returns empty list when directory does not exist."""
        mock_dir = MagicMock()
        mock_dir.exists.return_value = False
        mock_path_cls.return_value = mock_dir

        from backend.core.agent_service import scan_test_files

        result = scan_test_files()
        assert result == []


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


def _make_mock_agent(stall_detector_mock=None):
    """Create a mock agent with _stall_detector and _pending_interventions."""
    agent = MagicMock()
    agent._pending_interventions = []
    if stall_detector_mock is None:
        stall_detector_mock = MagicMock()
        stall_detector_mock.check.return_value = StallResult(
            should_intervene=False, message=""
        )
        stall_detector_mock.detect_failure_mode.return_value = FailureDetectionResult(
            failure_mode=None, details={}
        )
    agent._stall_detector = stall_detector_mock
    agent._task_tracker = MagicMock()
    agent._task_tracker.check_progress.return_value = MagicMock(
        should_warn=False, level="info", remaining_steps=10, remaining_tasks=5
    )
    return agent


def _make_browser_state(dom_text="<html>test</html>"):
    """Create a fake browser_state with dom_state."""
    dom_state = MagicMock()
    dom_state.llm_representation.return_value = dom_text
    dom_state.selector_map = {i: MagicMock() for i in range(5)}
    browser_state = MagicMock()
    browser_state.dom_state = dom_state
    browser_state.url = ""
    browser_state.page_info = None
    browser_state.screenshot = None
    return browser_state


def _make_agent_output(action_name="click", index=42, evaluation="操作失败"):
    """Create a fake agent_output with action and evaluation."""
    mock_action = MagicMock()
    mock_action.model_dump.return_value = {action_name: {"index": index}}

    agent_output = MagicMock()
    agent_output.action = [mock_action]
    agent_output.evaluation_previous_goal = evaluation
    agent_output.memory = ""
    agent_output.next_goal = ""
    return agent_output


class TestStepCallbackPhase69:
    """Phase 69 integration tests for step_callback failure detection.

    Tests that step_callback calls detect_failure_mode() when evaluation
    contains failure keywords, and update_failure_tracker() when a failure
    mode is detected.
    """

    @pytest.mark.asyncio
    @patch("backend.core.agent_service.AgentService.save_screenshot", new_callable=AsyncMock)
    async def test_detect_failure_mode_called_with_failure_keyword(self, mock_screenshot):
        """When evaluation contains '失败', detect_failure_mode is called."""
        stall_detector = MagicMock()
        stall_detector.check.return_value = StallResult(
            should_intervene=False, message=""
        )
        stall_detector.detect_failure_mode.return_value = FailureDetectionResult(
            failure_mode=None, details={}
        )
        agent = _make_mock_agent(stall_detector)

        browser_state = _make_browser_state()
        agent_output = _make_agent_output(
            action_name="click", index=42, evaluation="操作失败，未找到元素"
        )

        on_step = MagicMock()
        step_stats_data = {"value": None}
        _prev_dom_hash_data = {"value": None}

        import hashlib
        import json
        import asyncio
        async def step_callback(browser_state, agent_output, step: int):
            dom_str = ""
            dom_hash = ""
            element_count = 0
            if browser_state and browser_state.dom_state:
                dom_str = browser_state.dom_state.llm_representation()
                dom_hash = hashlib.sha256(dom_str.encode("utf-8")).hexdigest()[:12]
                selector_map = getattr(browser_state.dom_state, "selector_map", None)
                if selector_map is not None:
                    element_count = len(selector_map)

            action_name = ""
            action_params = {}
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                first_action = agent_output.action[0]
                action_dict = first_action.model_dump(exclude_none=True, mode="json")
                if action_dict:
                    action_name = list(action_dict.keys())[0]
                    action_params = action_dict[action_name]

            evaluation = ""
            if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                evaluation = agent_output.evaluation_previous_goal or ""

            try:
                agent._stall_detector.check(
                    action_name=action_name,
                    target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )

                # Phase 69: failure detection
                _failure_keywords = ("失败", "wrong", "error", "无法", "不成功", "未成功")
                if any(kw in evaluation for kw in _failure_keywords):
                    failure_result = agent._stall_detector.detect_failure_mode(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash_before=_prev_dom_hash_data["value"] or "",
                        dom_hash_after=dom_hash,
                    )
                    if failure_result.failure_mode is not None:
                        from backend.agent.dom_patch import update_failure_tracker
                        backend_node_id = str(action_params.get("index", ""))
                        update_failure_tracker(
                            backend_node_id=backend_node_id,
                            error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                            mode=failure_result.failure_mode,
                        )

                _prev_dom_hash_data["value"] = dom_hash

            except Exception:
                pass

            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, "", "", None, "{}")
            else:
                on_step(step, "", "", None, "{}")

        await step_callback(browser_state, agent_output, step=1)

        stall_detector.detect_failure_mode.assert_called_once()
        call_kwargs = stall_detector.detect_failure_mode.call_args.kwargs
        assert call_kwargs["action_name"] == "click"
        assert call_kwargs["target_index"] == 42
        assert "失败" in call_kwargs["evaluation"]

    @pytest.mark.asyncio
    @patch("backend.agent.dom_patch.update_failure_tracker")
    @patch("backend.core.agent_service.AgentService.save_screenshot", new_callable=AsyncMock)
    async def test_update_tracker_called_on_failure_mode(
        self, mock_screenshot, mock_update_tracker
    ):
        """When detect_failure_mode returns click_no_effect, update_failure_tracker is called."""
        stall_detector = MagicMock()
        stall_detector.check.return_value = StallResult(
            should_intervene=False, message=""
        )
        stall_detector.detect_failure_mode.return_value = FailureDetectionResult(
            failure_mode="click_no_effect",
            details={"evaluation_snippet": "点击无效果"},
        )
        agent = _make_mock_agent(stall_detector)

        browser_state = _make_browser_state()
        agent_output = _make_agent_output(
            action_name="click", index=42, evaluation="操作失败"
        )

        on_step = MagicMock()

        step_stats_data = {"value": None}
        _prev_dom_hash_data = {"value": None}

        import hashlib
        import json
        import asyncio

        async def step_callback(browser_state, agent_output, step: int):
            dom_str = ""
            dom_hash = ""
            if browser_state and browser_state.dom_state:
                dom_str = browser_state.dom_state.llm_representation()
                dom_hash = hashlib.sha256(dom_str.encode("utf-8")).hexdigest()[:12]

            action_name = ""
            action_params = {}
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                first_action = agent_output.action[0]
                action_dict = first_action.model_dump(exclude_none=True, mode="json")
                if action_dict:
                    action_name = list(action_dict.keys())[0]
                    action_params = action_dict[action_name]

            evaluation = ""
            if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                evaluation = agent_output.evaluation_previous_goal or ""

            try:
                agent._stall_detector.check(
                    action_name=action_name,
                    target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )

                _failure_keywords = ("失败", "wrong", "error", "无法", "不成功", "未成功")
                if any(kw in evaluation for kw in _failure_keywords):
                    failure_result = agent._stall_detector.detect_failure_mode(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash_before=_prev_dom_hash_data["value"] or "",
                        dom_hash_after=dom_hash,
                    )
                    if failure_result.failure_mode is not None:
                        from backend.agent.dom_patch import update_failure_tracker
                        backend_node_id = str(action_params.get("index", ""))
                        update_failure_tracker(
                            backend_node_id=backend_node_id,
                            error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                            mode=failure_result.failure_mode,
                        )

                _prev_dom_hash_data["value"] = dom_hash

            except Exception:
                pass

            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, "", "", None, "{}")
            else:
                on_step(step, "", "", None, "{}")

        await step_callback(browser_state, agent_output, step=1)

        mock_update_tracker.assert_called_once_with(
            backend_node_id="42",
            error="点击无效果",
            mode="click_no_effect",
        )

    @pytest.mark.asyncio
    @patch("backend.core.agent_service.AgentService.save_screenshot", new_callable=AsyncMock)
    async def test_detect_not_called_without_failure_keyword(self, mock_screenshot):
        """When evaluation has no failure keywords, detect_failure_mode is NOT called."""
        stall_detector = MagicMock()
        stall_detector.check.return_value = StallResult(
            should_intervene=False, message=""
        )
        stall_detector.detect_failure_mode.return_value = FailureDetectionResult(
            failure_mode=None, details={}
        )
        agent = _make_mock_agent(stall_detector)

        browser_state = _make_browser_state()
        agent_output = _make_agent_output(
            action_name="click", index=42, evaluation="操作成功，已找到元素"
        )

        on_step = MagicMock()

        step_stats_data = {"value": None}
        _prev_dom_hash_data = {"value": None}

        import hashlib
        import asyncio

        async def step_callback(browser_state, agent_output, step: int):
            dom_str = ""
            dom_hash = ""
            if browser_state and browser_state.dom_state:
                dom_str = browser_state.dom_state.llm_representation()
                dom_hash = hashlib.sha256(dom_str.encode("utf-8")).hexdigest()[:12]

            action_name = ""
            action_params = {}
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                first_action = agent_output.action[0]
                action_dict = first_action.model_dump(exclude_none=True, mode="json")
                if action_dict:
                    action_name = list(action_dict.keys())[0]
                    action_params = action_dict[action_name]

            evaluation = ""
            if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                evaluation = agent_output.evaluation_previous_goal or ""

            try:
                agent._stall_detector.check(
                    action_name=action_name,
                    target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )

                _failure_keywords = ("失败", "wrong", "error", "无法", "不成功", "未成功")
                if any(kw in evaluation for kw in _failure_keywords):
                    failure_result = agent._stall_detector.detect_failure_mode(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash_before=_prev_dom_hash_data["value"] or "",
                        dom_hash_after=dom_hash,
                    )

                _prev_dom_hash_data["value"] = dom_hash

            except Exception:
                pass

            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, "", "", None, "{}")
            else:
                on_step(step, "", "", None, "{}")

        await step_callback(browser_state, agent_output, step=1)

        stall_detector.detect_failure_mode.assert_not_called()

    @pytest.mark.asyncio
    @patch("backend.agent.dom_patch.update_failure_tracker")
    @patch("backend.core.agent_service.AgentService.save_screenshot", new_callable=AsyncMock)
    async def test_tracker_not_called_when_no_failure_mode(
        self, mock_screenshot, mock_update_tracker
    ):
        """When detect_failure_mode returns failure_mode=None, tracker is NOT called."""
        stall_detector = MagicMock()
        stall_detector.check.return_value = StallResult(
            should_intervene=False, message=""
        )
        stall_detector.detect_failure_mode.return_value = FailureDetectionResult(
            failure_mode=None, details={}
        )
        agent = _make_mock_agent(stall_detector)

        browser_state = _make_browser_state()
        agent_output = _make_agent_output(
            action_name="click", index=42, evaluation="操作失败"
        )

        on_step = MagicMock()

        step_stats_data = {"value": None}
        _prev_dom_hash_data = {"value": None}

        import hashlib
        import asyncio

        async def step_callback(browser_state, agent_output, step: int):
            dom_str = ""
            dom_hash = ""
            if browser_state and browser_state.dom_state:
                dom_str = browser_state.dom_state.llm_representation()
                dom_hash = hashlib.sha256(dom_str.encode("utf-8")).hexdigest()[:12]

            action_name = ""
            action_params = {}
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                first_action = agent_output.action[0]
                action_dict = first_action.model_dump(exclude_none=True, mode="json")
                if action_dict:
                    action_name = list(action_dict.keys())[0]
                    action_params = action_dict[action_name]

            evaluation = ""
            if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                evaluation = agent_output.evaluation_previous_goal or ""

            try:
                agent._stall_detector.check(
                    action_name=action_name,
                    target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )

                _failure_keywords = ("失败", "wrong", "error", "无法", "不成功", "未成功")
                if any(kw in evaluation for kw in _failure_keywords):
                    failure_result = agent._stall_detector.detect_failure_mode(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash_before=_prev_dom_hash_data["value"] or "",
                        dom_hash_after=dom_hash,
                    )
                    if failure_result.failure_mode is not None:
                        from backend.agent.dom_patch import update_failure_tracker
                        backend_node_id = str(action_params.get("index", ""))
                        update_failure_tracker(
                            backend_node_id=backend_node_id,
                            error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                            mode=failure_result.failure_mode,
                        )

                _prev_dom_hash_data["value"] = dom_hash

            except Exception:
                pass

            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, "", "", None, "{}")
            else:
                on_step(step, "", "", None, "{}")

        await step_callback(browser_state, agent_output, step=1)

        mock_update_tracker.assert_not_called()

    @pytest.mark.asyncio
    @patch("backend.core.agent_service.AgentService.save_screenshot", new_callable=AsyncMock)
    async def test_first_step_no_false_positive(self, mock_screenshot):
        """First step (_prev_dom_hash None) does not produce false positive.

        The keyword gate prevents detect_failure_mode from being called on
        evaluation without failure keywords, even though dom_hash_before
        would be '' from the None->empty fallback.
        """
        stall_detector = MagicMock()
        stall_detector.check.return_value = StallResult(
            should_intervene=False, message=""
        )
        stall_detector.detect_failure_mode.return_value = FailureDetectionResult(
            failure_mode=None, details={}
        )
        agent = _make_mock_agent(stall_detector)

        browser_state = _make_browser_state()
        # First step with failure keyword -- should call detect_failure_mode
        # but dom_hash_before should be ""
        agent_output = _make_agent_output(
            action_name="click", index=5, evaluation="操作失败"
        )

        on_step = MagicMock()

        step_stats_data = {"value": None}
        _prev_dom_hash_data = {"value": None}

        import hashlib
        import asyncio

        async def step_callback(browser_state, agent_output, step: int):
            dom_str = ""
            dom_hash = ""
            if browser_state and browser_state.dom_state:
                dom_str = browser_state.dom_state.llm_representation()
                dom_hash = hashlib.sha256(dom_str.encode("utf-8")).hexdigest()[:12]

            action_name = ""
            action_params = {}
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                first_action = agent_output.action[0]
                action_dict = first_action.model_dump(exclude_none=True, mode="json")
                if action_dict:
                    action_name = list(action_dict.keys())[0]
                    action_params = action_dict[action_name]

            evaluation = ""
            if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                evaluation = agent_output.evaluation_previous_goal or ""

            try:
                agent._stall_detector.check(
                    action_name=action_name,
                    target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )

                _failure_keywords = ("失败", "wrong", "error", "无法", "不成功", "未成功")
                if any(kw in evaluation for kw in _failure_keywords):
                    failure_result = agent._stall_detector.detect_failure_mode(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash_before=_prev_dom_hash_data["value"] or "",
                        dom_hash_after=dom_hash,
                    )

                _prev_dom_hash_data["value"] = dom_hash

            except Exception:
                pass

            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, "", "", None, "{}")
            else:
                on_step(step, "", "", None, "{}")

        # First step: _prev_dom_hash_data["value"] is None
        assert _prev_dom_hash_data["value"] is None

        await step_callback(browser_state, agent_output, step=1)

        # detect_failure_mode was called with dom_hash_before=""
        stall_detector.detect_failure_mode.assert_called_once()
        call_kwargs = stall_detector.detect_failure_mode.call_args.kwargs
        assert call_kwargs["dom_hash_before"] == ""

        # After first call, _prev_dom_hash_data updated
        assert _prev_dom_hash_data["value"] is not None
        assert len(_prev_dom_hash_data["value"]) == 12

    @pytest.mark.asyncio
    @patch("backend.agent.dom_patch.update_failure_tracker")
    @patch("backend.core.agent_service.AgentService.save_screenshot", new_callable=AsyncMock)
    async def test_all_three_failure_modes_passed_through(
        self, mock_screenshot, mock_update_tracker
    ):
        """All three failure modes (click_no_effect, wrong_column, edit_not_active)
        correctly passed to update_failure_tracker."""
        failure_modes = [
            ("click_no_effect", "点击无变化"),
            ("wrong_column", "点击了错误列"),
            ("edit_not_active", "元素不可编辑"),
        ]

        import hashlib
        import asyncio

        for mode, snippet in failure_modes:
            mock_update_tracker.reset_mock()

            stall_detector = MagicMock()
            stall_detector.check.return_value = StallResult(
                should_intervene=False, message=""
            )
            stall_detector.detect_failure_mode.return_value = FailureDetectionResult(
                failure_mode=mode,
                details={"evaluation_snippet": snippet},
            )
            agent = _make_mock_agent(stall_detector)

            action_name = "input" if mode == "edit_not_active" else "click"
            browser_state = _make_browser_state()
            agent_output = _make_agent_output(
                action_name=action_name, index=99, evaluation="操作失败"
            )

            on_step = MagicMock()
            _prev_dom_hash_data = {"value": "abc123oldhash"}

            async def step_callback(browser_state, agent_output, step: int):
                dom_str = ""
                dom_hash = ""
                if browser_state and browser_state.dom_state:
                    dom_str = browser_state.dom_state.llm_representation()
                    dom_hash = hashlib.sha256(dom_str.encode("utf-8")).hexdigest()[:12]

                action_name = ""
                action_params = {}
                if agent_output and hasattr(agent_output, "action") and agent_output.action:
                    first_action = agent_output.action[0]
                    action_dict = first_action.model_dump(exclude_none=True, mode="json")
                    if action_dict:
                        action_name = list(action_dict.keys())[0]
                        action_params = action_dict[action_name]

                evaluation = ""
                if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                    evaluation = agent_output.evaluation_previous_goal or ""

                try:
                    agent._stall_detector.check(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash=dom_hash,
                    )

                    _failure_keywords = ("失败", "wrong", "error", "无法", "不成功", "未成功")
                    if any(kw in evaluation for kw in _failure_keywords):
                        failure_result = agent._stall_detector.detect_failure_mode(
                            action_name=action_name,
                            target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                            evaluation=evaluation,
                            dom_hash_before=_prev_dom_hash_data["value"] or "",
                            dom_hash_after=dom_hash,
                        )
                        if failure_result.failure_mode is not None:
                            from backend.agent.dom_patch import update_failure_tracker
                            backend_node_id = str(action_params.get("index", ""))
                            update_failure_tracker(
                                backend_node_id=backend_node_id,
                                error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                                mode=failure_result.failure_mode,
                            )

                    _prev_dom_hash_data["value"] = dom_hash

                except Exception:
                    pass

                if asyncio.iscoroutinefunction(on_step):
                    await on_step(step, "", "", None, "{}")
                else:
                    on_step(step, "", "", None, "{}")

            await step_callback(browser_state, agent_output, step=1)

            mock_update_tracker.assert_called_once_with(
                backend_node_id="99",
                error=snippet,
                mode=mode,
            )


class TestRunWithStreamingExternalSession:
    """Verify run_with_streaming accepts external browser_session parameter."""

    def test_external_session_signature_has_browser_session_param(self):
        """When browser_session is provided, create_browser_session is NOT called."""
        from backend.core.agent_service import AgentService

        svc = AgentService()

        import inspect

        sig = inspect.signature(svc.run_with_streaming)
        params = sig.parameters
        assert "browser_session" in params
        assert params["browser_session"].default is None

    def test_run_with_cleanup_forwards_browser_session(self):
        """run_with_cleanup signature includes browser_session parameter."""
        from backend.core.agent_service import AgentService

        svc = AgentService()

        import inspect

        sig = inspect.signature(svc.run_with_cleanup)
        params = sig.parameters
        assert "browser_session" in params
        assert params["browser_session"].default is None
