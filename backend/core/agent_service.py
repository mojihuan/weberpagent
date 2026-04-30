"""Agent 服务 - 封装 browser-use Agent"""

import asyncio
import base64
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Callable, Union

from browser_use import BrowserSession, BrowserProfile

from backend.agent.monitored_agent import MonitoredAgent
from backend.agent.action_utils import extract_action_info
from backend.agent.stall_detector import StallDetector
from backend.agent.pre_submit_guard import PreSubmitGuard
from backend.agent.task_progress_tracker import TaskProgressTracker
from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE
from backend.agent.dom_patch import apply_dom_patch
from backend.llm.factory import create_llm
from backend.utils.run_logger import RunLogger


def scan_test_files() -> list[str]:
    """Scan data/test-files/ directory for uploadable test files.

    Returns absolute file paths for all files in data/test-files/.
    Returns empty list if directory does not exist.
    """
    test_dir = Path("data/test-files")
    if not test_dir.exists():
        return []
    return [str(f.resolve()) for f in sorted(test_dir.iterdir()) if f.is_file()]


# 服务器环境必需的 Chrome 参数
SERVER_BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
]


def create_browser_session() -> BrowserSession:
    """创建适用于服务器的 BrowserSession"""
    from browser_use.browser.profile import ViewportSize

    browser_profile = BrowserProfile(
        headless=True,
        args=SERVER_BROWSER_ARGS,
        viewport=ViewportSize(width=1920, height=1080),
    )
    return BrowserSession(browser_profile=browser_profile)

logger = logging.getLogger(__name__)


class AgentService:
    """browser-use Agent 服务封装"""

    def __init__(
        self,
        output_dir: str = "outputs",
        screenshots_dir: str = "data/screenshots",
    ):
        self.output_dir = Path(output_dir)
        self.screenshots_dir = Path(screenshots_dir)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._browser_session = None  # 存储浏览器会话引用供 step_callback 访问

    async def save_screenshot(
        self, screenshot_data: Union[bytes, str], run_id: str, step_index: int
    ) -> str:
        """保存截图到本地文件

        Args:
            screenshot_data: 截图数据（可以是 bytes 或 base64 编码的字符串）
            run_id: 执行 ID
            step_index: 步骤索引

        Returns:
            截图文件路径
        """
        filename = f"step_{step_index}.png"
        run_screenshots_dir = Path(self.output_dir, run_id, "screenshots")
        run_screenshots_dir.mkdir(parents=True, exist_ok=True)
        filepath = run_screenshots_dir / filename

        # 处理不同类型的输入
        if isinstance(screenshot_data, str):
            # 如果是字符串，尝试 base64 解码
            try:
                screenshot_bytes = base64.b64decode(screenshot_data)
            except Exception as e:
                logger.warning(f"[{run_id}] base64 解码失败，尝试直接编码: {e}")
                screenshot_bytes = screenshot_data.encode('utf-8')
        else:
            screenshot_bytes = screenshot_data

        filepath.write_bytes(screenshot_bytes)
        return str(filepath)

    async def _click_password_login_tab(self, run_id: str, page: Any) -> bool:
        """Switch to password login tab via mouse click."""
        mouse = await page.mouse
        tab_raw = await page.evaluate("""() => {
            var divs = document.querySelectorAll('div');
            for (var i = 0; i < divs.length; i++) {
                if (divs[i].textContent.trim() === '密码登录'
                    && divs[i].offsetParent !== null) {
                    var r = divs[i].getBoundingClientRect();
                    return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
                }
            }
            return null;
        }""")
        if tab_raw:
            tab_pos = json.loads(tab_raw)
            await mouse.click(tab_pos['x'], tab_pos['y'])
            logger.info(f"[{run_id}][LOGIN] Clicked 密码登录 tab at ({tab_pos['x']:.0f}, {tab_pos['y']:.0f})")
            await asyncio.sleep(1)
            return True
        logger.warning(f"[{run_id}][LOGIN] Could not find 密码登录 tab")
        return True  # Continue even without tab click

    async def _fill_login_form(
        self, run_id: str, page: Any, account: str, password: str,
    ) -> bool:
        """Fill account and password inputs using nativeInputValueSetter."""
        acc_js = json.dumps(account)
        pwd_js = json.dumps(password)

        # Fill account
        acc_raw = await page.evaluate(f"""() => {{
            var inp = document.querySelector('input[placeholder="请输入账号"]');
            if (!inp) {{
                var all = document.querySelectorAll('input');
                for (var i = 0; i < all.length; i++) {{
                    if (all[i].placeholder && all[i].placeholder.indexOf('账号') >= 0) {{ inp = all[i]; break; }}
                }}
            }}
            if (!inp) return null;
            var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(inp, {acc_js});
            inp.dispatchEvent(new Event('input', {{bubbles: true}}));
            inp.dispatchEvent(new Event('change', {{bubbles: true}}));
            return 'ok';
        }}""")
        if not acc_raw:
            logger.error(f"[{run_id}][LOGIN] Could not find account input")
            return False
        logger.info(f"[{run_id}][LOGIN] Filled account: {account}")
        await asyncio.sleep(0.3)

        # Fill password
        pwd_raw = await page.evaluate(f"""() => {{
            var inp = document.querySelector('input[placeholder="请输入密码"]');
            if (!inp) inp = document.querySelector('input[type="password"]');
            if (!inp) return null;
            var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(inp, {pwd_js});
            inp.dispatchEvent(new Event('input', {{bubbles: true}}));
            inp.dispatchEvent(new Event('change', {{bubbles: true}}));
            return 'ok';
        }}""")
        if not pwd_raw:
            logger.error(f"[{run_id}][LOGIN] Could not find password input")
            return False
        logger.info(f"[{run_id}][LOGIN] Filled password")
        await asyncio.sleep(0.3)

        # Click login button
        mouse = await page.mouse
        btn_raw = await page.evaluate("""() => {
            var btns = document.querySelectorAll('button');
            for (var i = 0; i < btns.length; i++) {
                var t = btns[i].textContent.trim();
                if (t === '登 录' || t === '登录' || t === 'Login') {
                    var r = btns[i].getBoundingClientRect();
                    return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2, text: t});
                }
            }
            return null;
        }""")
        if not btn_raw:
            logger.error(f"[{run_id}][LOGIN] Could not find login button")
            return False
        btn_pos = json.loads(btn_raw)
        await mouse.click(btn_pos['x'], btn_pos['y'])
        logger.info(f"[{run_id}][LOGIN] Clicked login button '{btn_pos['text']}' at ({btn_pos['x']:.0f}, {btn_pos['y']:.0f})")
        return True

    async def _verify_login_success(self, run_id: str, page: Any) -> bool:
        """Wait for redirect away from /login page."""
        for wait_sec in [2, 3, 5]:
            await asyncio.sleep(wait_sec)
            current_url = await page.evaluate("() => window.location.href")
            if "/login" not in current_url:
                logger.info(f"[{run_id}][LOGIN] Login succeeded, redirected to: {current_url}")
                return True
            logger.debug(f"[{run_id}][LOGIN] Still on login page after {wait_sec}s")
        logger.error(f"[{run_id}][LOGIN] Login did not redirect from /login")
        return False

    async def _programmatic_login(
        self,
        run_id: str,
        page: Any,
        account: str,
        password: str,
    ) -> bool:
        """Login to ERP SPA via mouse click + JS value injection.

        Orchestrates: click tab -> fill form -> verify redirect.
        """
        try:
            await self._click_password_login_tab(run_id, page)
            if not await self._fill_login_form(run_id, page, account, password):
                return False
            return await self._verify_login_success(run_id, page)
        except Exception as e:
            logger.error(f"[{run_id}][LOGIN] Programmatic login failed: {e}")
            return False

    async def pre_navigate(
        self,
        run_id: str,
        target_url: str,
        browser_session: BrowserSession,
        login_account: str | None = None,
        login_password: str | None = None,
    ) -> bool:
        """Pre-navigate to target URL, performing login if needed.

        Strategy:
        1. Start browser and navigate to the SPA
        2. If login credentials are provided, perform programmatic login
           (fill form + click login) so the SPA handles all internal state
        3. Verify the SPA left the /login page

        Args:
            run_id: Execution ID for logging.
            target_url: URL to navigate to.
            browser_session: BrowserSession to use.
            login_account: Account for programmatic login (optional).
            login_password: Password for programmatic login (optional).

        Returns:
            True if the SPA successfully loaded a non-login page.
        """
        try:
            await browser_session.start()
            await browser_session.navigate_to(target_url)
            await asyncio.sleep(2)

            page = await browser_session.get_current_page()
            if not page:
                logger.error(f"[{run_id}] No page after initial navigation")
                return False

            current_url = await page.evaluate("() => window.location.href")
            logger.info(f"[{run_id}] After initial nav: {current_url}")

            # If we're NOT on /login, we're already authenticated
            if "/login" not in current_url:
                logger.info(f"[{run_id}] Already on main page: {current_url}")
                browser_session._pre_navigated = True
                return True

            # We're on /login — try programmatic login if credentials provided
            if login_account and login_password:
                logger.info(
                    f"[{run_id}] On login page, performing programmatic login "
                    f"with account={login_account}"
                )
                success = await self._programmatic_login(
                    run_id, page, login_account, login_password,
                )
                if success:
                    browser_session._pre_navigated = True
                    return True
                logger.warning(f"[{run_id}] Programmatic login failed")
                return False

            # No credentials — can't do anything
            logger.warning(f"[{run_id}] On login page but no credentials provided")
            return False

        except Exception as e:
            logger.warning(f"[{run_id}] Pre-navigation failed: {e}")
            return False

    async def _run_detectors(
        self,
        agent_ref: dict,
        run_id: str,
        run_logger: RunLogger,
        action_name: str,
        action_params: dict,
        evaluation: str,
        dom_hash: str,
        _prev_dom_hash_data: dict,
        step: int,
        max_steps: int,
    ) -> None:
        """Run stall detection, failure mode detection, and progress tracking."""
        agent = agent_ref["value"]
        if agent is None:
            return

        try:
            # Stall detection
            stall_result = agent._stall_detector.check(
                action_name=action_name,
                target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                evaluation=evaluation, dom_hash=dom_hash,
            )
            if stall_result.should_intervene:
                agent._pending_interventions.append(stall_result.message)
                run_logger.log("warning", "monitor", "Stall detected", step=step, detail=stall_result.message[:100])

            # Failure mode detection (Phase 69)
            _failure_keywords = ('失败', 'wrong', 'error', '无法', '不成功', '未成功')
            if any(kw in evaluation for kw in _failure_keywords):
                try:
                    failure_result = agent._stall_detector.detect_failure_mode(
                        action_name=action_name,
                        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                        evaluation=evaluation,
                        dom_hash_before=_prev_dom_hash_data["value"] or "",
                        dom_hash_after=dom_hash,
                    )
                    if failure_result.failure_mode is not None:
                        from backend.agent.dom_patch import update_failure_tracker
                        update_failure_tracker(
                            backend_node_id=str(action_params.get("index", "")),
                            error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                            mode=failure_result.failure_mode,
                        )
                        run_logger.log("warning", "monitor", "Failure detected", step=step, mode=failure_result.failure_mode)
                except Exception as fe:
                    logger.error(f"[{run_id}][MONITOR] Failure detection error (non-blocking): {fe}")

            _prev_dom_hash_data["value"] = dom_hash

            # Progress tracking
            progress_result = agent._task_tracker.check_progress(current_step=step, max_steps=max_steps)
            if progress_result.should_warn:
                agent._pending_interventions.append(progress_result.message)
                run_logger.log(progress_result.level, "monitor", "Progress warning",
                               step=step, remaining_steps=progress_result.remaining_steps,
                               remaining_tasks=progress_result.remaining_tasks)
            agent._task_tracker.update_from_evaluation(evaluation)

        except Exception as e:
            logger.error(f"[{run_id}][MONITOR] Detector error (non-blocking): {e}")
            run_logger.log("error", "monitor", f"Detector error: {e}", step=step)

    def _extract_browser_state(
        self, run_id: str, browser_state: Any, run_logger: RunLogger, step: int,
    ) -> tuple[str, int]:
        """Extract dom_hash and element_count from browser state, logging to run_logger."""
        dom_hash = ""
        element_count = 0
        if not browser_state:
            logger.warning(f"[{run_id}][BROWSER] browser_state 为空!")
            return dom_hash, element_count

        url = getattr(browser_state, "url", "") or ""
        logger.info(f"[{run_id}][BROWSER] URL: {url}")
        dom_state = getattr(browser_state, "dom_state", None)
        dom_str = ""
        if dom_state:
            try:
                dom_str = dom_state.llm_representation()
            except Exception:
                dom_str = str(dom_state)
            logger.info(f"[{run_id}][BROWSER] DOM 长度: {len(dom_str)} 字符")
            dom_hash = hashlib.sha256(dom_str.encode('utf-8')).hexdigest()[:12]
            selector_map = getattr(dom_state, "selector_map", None)
            if selector_map is not None:
                element_count = len(selector_map) if hasattr(selector_map, '__len__') else 0
            logger.info(f"[{run_id}][BROWSER] 元素数量: {element_count}")
        else:
            logger.warning(f"[{run_id}][BROWSER] dom_state 为空")
        run_logger.log_browser(url=url, dom_content=dom_str, step=step, element_count=element_count)
        return dom_hash, element_count

    @staticmethod
    def _extract_agent_output(run_id: str, agent_output: Any) -> tuple[str, str, dict, dict, str]:
        """Extract action info and reasoning from agent output.

        Returns (action, action_name, action_params, action_dict, reasoning).
        """
        action = ""
        action_name = ""
        action_params: dict = {}
        action_dict: dict = {}
        reasoning = ""
        if not agent_output:
            logger.warning(f"[{run_id}][AGENT] agent_output 为空!")
            return action, action_name, action_params, action_dict, reasoning

        action_name, action_params = extract_action_info(agent_output)
        if action_name != "unknown":
            action_dict = {action_name: action_params}
            action = f"{action_name}: {action_params}" if action_params else action_name
            logger.info(f"[{run_id}][AGENT] 动作: {action_name}, 参数: {action_params}")
            if 'index' in action_params:
                logger.info(f"[{run_id}][AGENT] 目标元素 index: {action_params['index']}")

        parts = []
        if hasattr(agent_output, "evaluation_previous_goal") and agent_output.evaluation_previous_goal:
            parts.append(f"Eval: {agent_output.evaluation_previous_goal}")
        if hasattr(agent_output, "memory") and agent_output.memory:
            parts.append(f"Memory: {agent_output.memory}")
        if hasattr(agent_output, "next_goal") and agent_output.next_goal:
            parts.append(f"Goal: {agent_output.next_goal}")
        reasoning = " | ".join(parts) if parts else ""
        return action, action_name, action_params, action_dict, reasoning

    def _create_step_callback(
        self,
        run_id: str,
        run_logger: RunLogger,
        step_stats_data: dict,
        _prev_dom_hash_data: dict,
        on_step: Callable,
        max_steps: int,
        agent_ref: dict,
    ) -> Callable:
        """Create step callback closure for MonitoredAgent.

        Uses agent_ref mutable dict to defer agent binding.
        """
        svc = self  # Capture self for use in closure

        async def step_callback(browser_state: Any, agent_output: Any, step: int) -> None:
            logger.debug(f"[{run_id}] 步骤回调: step={step}")
            dom_hash, element_count = svc._extract_browser_state(run_id, browser_state, run_logger, step)
            action, action_name, action_params, action_dict, reasoning = svc._extract_agent_output(run_id, agent_output)

            # 从 browser_state 提取 interacted_element 并注入 action_dict
            if action_dict and browser_state and hasattr(browser_state, 'dom_state'):
                try:
                    from browser_use.dom.views import DOMInteractedElement
                    selector_map = browser_state.dom_state.selector_map
                    first_action = agent_output.action[0]
                    index = first_action.get_index()
                    if index is not None and index in selector_map:
                        action_dict["interacted_element"] = DOMInteractedElement.load_from_enhanced_dom_tree(
                            selector_map[index]
                        )
                    else:
                        action_dict["interacted_element"] = None
                except Exception as e:
                    logger.warning(f"[{run_id}] 提取 interacted_element 失败: {e}")
                    action_dict["interacted_element"] = None

            # Step statistics
            action_count = 1
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                action_count = len(agent_output.action)
            step_stats_data["value"] = json.dumps(
                {"action_count": action_count, "duration_ms": 0, "element_count": element_count}, ensure_ascii=False,
            )
            if action_name:
                run_logger.log_agent(action_name=action_name, action_params=action_params, reasoning=reasoning, step=step)

            # Screenshot
            screenshot_path = None
            if browser_state and hasattr(browser_state, "screenshot") and browser_state.screenshot:
                screenshot_path = await svc.save_screenshot(browser_state.screenshot, run_id, step)
                run_logger.log("info", "step", "Screenshot saved", step=step, path=screenshot_path)

            # Detectors
            evaluation = ""
            if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                evaluation = agent_output.evaluation_previous_goal or ""
            await svc._run_detectors(
                agent_ref, run_id, run_logger, action_name, action_params,
                evaluation, dom_hash, _prev_dom_hash_data, step, max_steps,
            )

            # Call external on_step callback
            step_stats_json = step_stats_data["value"]
            _action_dict_data = action_dict if action_dict else None
            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, action, reasoning, screenshot_path, step_stats_json, action_dict=_action_dict_data)
            else:
                on_step(step, action, reasoning, screenshot_path, step_stats_json, action_dict=_action_dict_data)

        return step_callback

    async def run_with_streaming(
        self,
        task: str,
        run_id: str,
        on_step: Callable[[int, str, str, str | None], Any],
        max_steps: int = 10,
        llm_config: dict | None = None,
        target_url: str | None = None,
        browser_session: BrowserSession | None = None,
    ) -> Any:
        """带流式回调的执行"""
        logger.info(f"[{run_id}] 创建 LLM: config={llm_config}")
        llm = create_llm(llm_config)

        if browser_session is None:
            browser_session = create_browser_session()
        self._browser_session = browser_session

        pre_navigated = False
        if target_url and not getattr(browser_session, '_pre_navigated', False):
            await self.pre_navigate(run_id, target_url, browser_session)
            pre_navigated = True
        elif target_url:
            pre_navigated = True

        run_logger = RunLogger(run_id, str(self.output_dir))
        run_logger.log("info", "system", "Run started", max_steps=max_steps)

        step_stats_data: dict[str, Any] = {"value": None}
        _prev_dom_hash_data: dict[str, Any] = {"value": None}
        agent_ref: dict[str, Any] = {"value": None}

        step_callback = self._create_step_callback(
            run_id, run_logger, step_stats_data, _prev_dom_hash_data, on_step, max_steps, agent_ref,
        )

        actual_task = task
        if target_url and not pre_navigated:
            actual_task = f"目标URL: {target_url}\n\n任务:\n{task}"
        elif pre_navigated:
            logger.info(f"[{run_id}] 已预导航到目标页面，跳过 URL 拼接")

        apply_dom_patch()

        stall_detector = StallDetector()
        pre_submit_guard = PreSubmitGuard()
        task_progress_tracker = TaskProgressTracker()
        file_paths = scan_test_files()

        agent = MonitoredAgent(
            task=actual_task, llm=llm, browser_session=browser_session,
            available_file_paths=file_paths, max_actions_per_step=5,
            register_new_step_callback=step_callback,
            extend_system_message=ENHANCED_SYSTEM_MESSAGE,
            loop_detection_window=10, max_failures=4,
            planning_replan_on_stall=2, enable_planning=True,
            stall_detector=stall_detector, pre_submit_guard=pre_submit_guard,
            task_progress_tracker=task_progress_tracker, run_logger=run_logger,
        )
        agent_ref["value"] = agent

        try:
            result = await agent.run(max_steps=max_steps)
            run_logger.log("info", "system", "Run completed", success=result.is_successful())
            return result
        except Exception:
            run_logger.log("error", "system", "Run failed with exception")
            raise
        finally:
            run_logger.close()

    async def run_with_cleanup(
        self,
        task: str,
        run_id: str,
        on_step: Callable[[int, str, str, str | None], Any],
        max_steps: int = 10,
        llm_config: dict | None = None,
        target_url: str | None = None,
        browser_session: BrowserSession | None = None,
    ) -> Any:
        """Execute task with guaranteed cleanup logging

        Wraps run_with_streaming with try/finally to ensure
        cleanup logging happens even on errors.

        Note: browser-use Agent handles browser lifecycle internally.
        This method ensures we log completion status for debugging.

        Args:
            task: Natural language task description
            run_id: Execution ID for logging
            on_step: Async callback for step updates
            max_steps: Maximum execution steps
            llm_config: LLM configuration
            target_url: Target URL to navigate to before execution
            browser_session: Optional pre-authenticated BrowserSession

        Returns:
            Agent execution history

        Raises:
            Exception: Re-raises any execution errors
        """
        try:
            logger.info(f"[{run_id}] Starting execution with cleanup tracking")
            result = await self.run_with_streaming(
                task=task,
                run_id=run_id,
                on_step=on_step,
                max_steps=max_steps,
                llm_config=llm_config,
                target_url=target_url,
                browser_session=browser_session,
            )
            logger.info(f"[{run_id}] Execution completed successfully")
            return result
        except Exception as e:
            logger.error(f"[{run_id}] Execution failed with error: {e}")
            logger.debug(f"[{run_id}] Error type: {type(e).__name__}")
            raise
        finally:
            logger.info(f"[{run_id}] Execution cleanup complete - resources released")
