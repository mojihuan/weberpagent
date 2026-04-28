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

    async def _programmatic_login(
        self,
        run_id: str,
        page: Any,
        account: str,
        password: str,
    ) -> bool:
        """Login to ERP SPA via mouse click + JS value injection.

        Strategy:
          - page.evaluate() to find elements (JSON.stringify return)
          - (await page.mouse).click() for physical clicks (isTrusted)
          - JS nativeInputValueSetter for form filling (v-model)

        browser-use CDP page limitations:
          - page.evaluate() returns strings for objects → JSON.stringify
          - page.mouse is async (await), page.keyboard does NOT exist
          - page.locator() does NOT work

        Reference: webseleniumerp/pages/pages_login.py login flow.
        """
        try:
            mouse = await page.mouse
            # Escape values for safe JS embedding
            acc_js = json.dumps(account)
            pwd_js = json.dumps(password)

            # Step 1: Switch to 密码登录 tab (mouse click = isTrusted)
            tab_raw = await page.evaluate("""() => {
                var divs = document.querySelectorAll('div');
                for (var i = 0; i < divs.length; i++) {
                    if (divs[i].textContent.trim() === '密码登录'
                        && divs[i].offsetParent !== null) {
                        var r = divs[i].getBoundingClientRect();
                        return JSON.stringify({
                            x: r.x + r.width/2,
                            y: r.y + r.height/2
                        });
                    }
                }
                return null;
            }""")
            if tab_raw:
                tab_pos = json.loads(tab_raw)
                await mouse.click(tab_pos['x'], tab_pos['y'])
                logger.info(
                    f"[{run_id}][LOGIN] Clicked 密码登录 tab at "
                    f"({tab_pos['x']:.0f}, {tab_pos['y']:.0f})"
                )
                await asyncio.sleep(1)
            else:
                logger.warning(
                    f"[{run_id}][LOGIN] Could not find 密码登录 tab"
                )

            # Step 2: Fill account (nativeInputValueSetter → v-model)
            acc_raw = await page.evaluate(f"""() => {{
                var inp = document.querySelector(
                    'input[placeholder="请输入账号"]'
                );
                if (!inp) {{
                    var all = document.querySelectorAll('input');
                    for (var i = 0; i < all.length; i++) {{
                        if (all[i].placeholder
                            && all[i].placeholder.indexOf('账号') >= 0) {{
                            inp = all[i]; break;
                        }}
                    }}
                }}
                if (!inp) return null;
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                setter.call(inp, {acc_js});
                inp.dispatchEvent(new Event('input', {{bubbles: true}}));
                inp.dispatchEvent(new Event('change', {{bubbles: true}}));
                return 'ok';
            }}""")
            if not acc_raw:
                logger.error(
                    f"[{run_id}][LOGIN] Could not find account input"
                )
                return False
            logger.info(f"[{run_id}][LOGIN] Filled account: {account}")
            await asyncio.sleep(0.3)

            # Step 3: Fill password (nativeInputValueSetter → v-model)
            pwd_raw = await page.evaluate(f"""() => {{
                var inp = document.querySelector(
                    'input[placeholder="请输入密码"]'
                );
                if (!inp) inp = document.querySelector(
                    'input[type="password"]'
                );
                if (!inp) return null;
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                setter.call(inp, {pwd_js});
                inp.dispatchEvent(new Event('input', {{bubbles: true}}));
                inp.dispatchEvent(new Event('change', {{bubbles: true}}));
                return 'ok';
            }}""")
            if not pwd_raw:
                logger.error(
                    f"[{run_id}][LOGIN] Could not find password input"
                )
                return False
            logger.info(f"[{run_id}][LOGIN] Filled password")
            await asyncio.sleep(0.3)

            # Step 4: Click 登 录 button (mouse click = isTrusted)
            btn_raw = await page.evaluate("""() => {
                var btns = document.querySelectorAll('button');
                for (var i = 0; i < btns.length; i++) {
                    var t = btns[i].textContent.trim();
                    if (t === '登 录' || t === '登录' || t === 'Login') {
                        var r = btns[i].getBoundingClientRect();
                        return JSON.stringify({
                            x: r.x + r.width/2,
                            y: r.y + r.height/2,
                            text: t
                        });
                    }
                }
                return null;
            }""")
            if not btn_raw:
                logger.error(
                    f"[{run_id}][LOGIN] Could not find login button"
                )
                return False
            btn_pos = json.loads(btn_raw)
            await mouse.click(btn_pos['x'], btn_pos['y'])
            logger.info(
                f"[{run_id}][LOGIN] Clicked login button "
                f"'{btn_pos['text']}' at "
                f"({btn_pos['x']:.0f}, {btn_pos['y']:.0f})"
            )

            # Step 5: Wait for redirect away from /login
            for wait_sec in [2, 3, 5]:
                await asyncio.sleep(wait_sec)
                current_url = await page.evaluate(
                    "() => window.location.href"
                )
                if "/login" not in current_url:
                    logger.info(
                        f"[{run_id}][LOGIN] Login succeeded, "
                        f"redirected to: {current_url}"
                    )
                    return True
                logger.debug(
                    f"[{run_id}][LOGIN] Still on login page after "
                    f"{wait_sec}s"
                )

            logger.error(
                f"[{run_id}][LOGIN] Login did not redirect from /login"
            )
            return False

        except Exception as e:
            logger.error(
                f"[{run_id}][LOGIN] Programmatic login failed: {e}"
            )
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
        """带流式回调的执行

        Args:
            task: 自然语言任务描述
            run_id: 执行 ID（用于截图命名）
            on_step: 异步步骤回调函数 (step_index, action, reasoning, screenshot_path)
            max_steps: 最大执行步数
            llm_config: LLM 配置
            target_url: 目标 URL（执行前先导航到此页面）
            browser_session: Optional pre-authenticated BrowserSession

        Returns:
            Agent 执行历史
        """
        logger.info(f"[{run_id}] 创建 LLM: config={llm_config}")
        llm = create_llm(llm_config)
        logger.info(f"[{run_id}] LLM 创建成功: type={type(llm).__name__}, model={getattr(llm, 'model_name', 'unknown')}")

        # Use provided session or create default
        if browser_session is None:
            browser_session = create_browser_session()

        # 存储引用供 step_callback 访问 (Phase 42, D-01)
        self._browser_session = browser_session

        # Pre-navigate to target URL when authenticated session is available.
        # If runs.py already called pre_navigate successfully (marked by
        # _pre_navigated), skip redundant pre-navigation here.
        pre_navigated = False
        if target_url and not getattr(browser_session, '_pre_navigated', False):
            await self.pre_navigate(run_id, target_url, browser_session)
            pre_navigated = True
        elif target_url:
            pre_navigated = True

        # 创建 per-run 结构化日志记录器
        run_logger = RunLogger(run_id, str(self.output_dir))
        run_logger.log("info", "system", "Run started", max_steps=max_steps)

        step_stats_data = {"value": None}  # Mutable container for step stats (Phase 41, LOG-02)
        _prev_dom_hash_data = {"value": None}  # Mutable container for previous step dom_hash (Phase 69, D-02)

        async def step_callback(browser_state, agent_output, step: int):
            logger.debug(f"[{run_id}] 步骤回调: step={step}")

            # ===== 详细日志: browser_state =====
            if browser_state:
                url = getattr(browser_state, "url", "") or ""
                logger.info(f"[{run_id}][BROWSER] URL: {url}")

                # 记录 DOM 状态
                dom_state = getattr(browser_state, "dom_state", None)
                dom_str = ""
                element_count = 0
                if dom_state:
                    # 使用 llm_representation() 获取 DOM 文本
                    try:
                        dom_str = dom_state.llm_representation()
                    except Exception:
                        dom_str = str(dom_state)
                    logger.info(f"[{run_id}][BROWSER] DOM 长度: {len(dom_str)} 字符")

                    # 计算 DOM 哈希用于停滞检测
                    dom_hash = hashlib.sha256(dom_str.encode('utf-8')).hexdigest()[:12]

                    # 使用 selector_map 计算元素数量
                    selector_map = getattr(dom_state, "selector_map", None)
                    if selector_map is not None:
                        element_count = len(selector_map) if hasattr(selector_map, '__len__') else 0
                    logger.info(f"[{run_id}][BROWSER] 元素数量: {element_count}")
                else:
                    dom_hash = ""
                    logger.warning(f"[{run_id}][BROWSER] dom_state 为空")

                # 记录页面信息
                page_info = getattr(browser_state, "page_info", None)
                if page_info:
                    logger.debug(f"[{run_id}][BROWSER] page_info: {page_info}")

                # 结构化日志: 保存 DOM 到 per-run 目录
                run_logger.log_browser(
                    url=url,
                    dom_content=dom_str,
                    step=step,
                    element_count=element_count,
                )

            else:
                logger.warning(f"[{run_id}][BROWSER] browser_state 为空!")
                dom_hash = ""

            # ===== 详细日志: agent_output =====
            # 提取动作和推理 - 从 agent_output 顶层获取
            action = ""
            action_name = ""
            action_params = {}
            reasoning = ""
            if agent_output:
                # 记录完整的 agent_output 结构
                logger.info(f"[{run_id}][AGENT] agent_output 类型: {type(agent_output).__name__}")

                # 获取动作名称（第一个动作的类型）
                if hasattr(agent_output, "action") and agent_output.action:
                    first_action = agent_output.action[0]
                    # ActionModel 是动态模型，获取第一个非 None 的动作类型
                    action_dict = first_action.model_dump(exclude_none=True, mode='json')
                    if action_dict:
                        action_name = list(action_dict.keys())[0]
                        action_params = action_dict[action_name]
                        # 格式化为可读字符串
                        action = f"{action_name}: {action_params}" if action_params else action_name

                        logger.info(f"[{run_id}][AGENT] 动作: {action_name}, 参数: {action_params}")

                        # 记录动作中的 index 信息（用于调试定位问题）
                        if 'index' in action_params:
                            logger.info(f"[{run_id}][AGENT] 目标元素 index: {action_params['index']}")

                # 获取推理信息（evaluation + memory + next_goal）
                parts = []
                if hasattr(agent_output, "evaluation_previous_goal") and agent_output.evaluation_previous_goal:
                    parts.append(f"Eval: {agent_output.evaluation_previous_goal}")
                    logger.info(f"[{run_id}][AGENT] 评估: {agent_output.evaluation_previous_goal}")
                if hasattr(agent_output, "memory") and agent_output.memory:
                    parts.append(f"Memory: {agent_output.memory}")
                    logger.debug(f"[{run_id}][AGENT] 记忆: {agent_output.memory[:100]}...")
                if hasattr(agent_output, "next_goal") and agent_output.next_goal:
                    parts.append(f"Goal: {agent_output.next_goal}")
                    logger.info(f"[{run_id}][AGENT] 下一步: {agent_output.next_goal}")
                reasoning = " | ".join(parts) if parts else ""
            else:
                logger.warning(f"[{run_id}][AGENT] agent_output 为空!")

            # Collect step statistics (Phase 41, LOG-02, per D-02)
            # element_count 已在上方从 dom_state.selector_map 计算

            # Action count: how many actions agent decided to take this step
            action_count = 1  # Default to 1 action
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                action_count = len(agent_output.action)

            # Build step_stats dict (per D-02)
            step_stats = {
                "action_count": action_count,
                "duration_ms": 0,  # Will be updated if timing wrapper exists
                "element_count": element_count,
            }
            step_stats_data["value"] = json.dumps(step_stats, ensure_ascii=False)

            # 结构化日志: 记录 agent 动作
            if action_name:
                run_logger.log_agent(
                    action_name=action_name,
                    action_params=action_params,
                    reasoning=reasoning,
                    step=step,
                )

            # 提取截图
            screenshot_path = None
            if browser_state and hasattr(browser_state, "screenshot"):
                screenshot_bytes = browser_state.screenshot
                if screenshot_bytes:
                    screenshot_path = await self.save_screenshot(
                        screenshot_bytes, run_id, step
                    )
                    logger.debug(f"[{run_id}] 截图已保存: {screenshot_path}")
                    run_logger.log("info", "step", f"Screenshot saved", step=step, path=screenshot_path)

            # ===== Detector calls (Phase 50, D-02/D-03, INTEG-03/INTEG-04) =====
            try:
                # Extract evaluation for detector use
                evaluation = ""
                if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
                    evaluation = agent_output.evaluation_previous_goal or ""

                # Stall detection -- reuse already-extracted action_name, action_params, dom_hash
                stall_result = agent._stall_detector.check(
                    action_name=action_name,
                    target_index=action_params.get("index") if isinstance(action_params, dict) else None,
                    evaluation=evaluation,
                    dom_hash=dom_hash,
                )
                if stall_result.should_intervene:
                    agent._pending_interventions.append(stall_result.message)
                    run_logger.log("warning", "monitor", "Stall detected",
                                   step=step, detail=stall_result.message[:100])

                # --- Phase 69: Failure mode detection + tracker update (D-01/D-02/D-03) ---
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
                            backend_node_id = str(action_params.get("index", ""))
                            update_failure_tracker(
                                backend_node_id=backend_node_id,
                                error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                                mode=failure_result.failure_mode,
                            )
                            run_logger.log("warning", "monitor", "Failure detected",
                                           step=step, mode=failure_result.failure_mode)
                    except Exception as fe:
                        logger.error(f"[{run_id}][MONITOR] Failure detection error (non-blocking): {fe}")

                # Update previous dom_hash for next step (D-02)
                _prev_dom_hash_data["value"] = dom_hash

                # Progress tracking
                progress_result = agent._task_tracker.check_progress(
                    current_step=step,
                    max_steps=max_steps,
                )
                if progress_result.should_warn:
                    agent._pending_interventions.append(progress_result.message)
                    run_logger.log(progress_result.level, "monitor", "Progress warning",
                                   step=step,
                                   remaining_steps=progress_result.remaining_steps,
                                   remaining_tasks=progress_result.remaining_tasks)

                # Update completed steps from evaluation
                agent._task_tracker.update_from_evaluation(evaluation)

            except Exception as e:
                logger.error(f"[{run_id}][MONITOR] Detector error (non-blocking): {e}")
                run_logger.log("error", "monitor", f"Detector error: {e}", step=step)

            # 调用异步回调
            step_stats_json = step_stats_data["value"]
            # Phase 112: Pass action_dict to on_step for incremental code translation (INTEG-01)
            _action_dict_data = action_dict if 'action_dict' in locals() else None
            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, action, reasoning, screenshot_path, step_stats_json,
                              action_dict=_action_dict_data)
            else:
                on_step(step, action, reasoning, screenshot_path, step_stats_json,
                        action_dict=_action_dict_data)

        # 如果有目标 URL 且未预导航，拼接到任务描述前面
        actual_task = task
        if target_url and not pre_navigated:
            actual_task = f"目标URL: {target_url}\n\n任务:\n{task}"
            logger.info(f"[{run_id}] 已将目标 URL 拼接到任务描述中")
        elif pre_navigated:
            logger.info(f"[{run_id}] 已预导航到目标页面，跳过 URL 拼接")

        logger.info(f"[{run_id}] Creating MonitoredAgent: task={actual_task[:80]}..., max_steps={max_steps}")

        # Apply DOM serializer monkey-patch for ERP table elements (checkbox, links)
        apply_dom_patch()

        # Initialize detectors (D-07)
        stall_detector = StallDetector()
        pre_submit_guard = PreSubmitGuard()
        task_progress_tracker = TaskProgressTracker()

        # Scan test files for upload_file whitelist
        file_paths = scan_test_files()
        logger.info(f"[{run_id}] Available upload files: {len(file_paths)} files")

        agent = MonitoredAgent(
            task=actual_task,
            llm=llm,
            browser_session=browser_session,
            available_file_paths=file_paths,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
            extend_system_message=ENHANCED_SYSTEM_MESSAGE,
            loop_detection_window=10,
            max_failures=4,
            planning_replan_on_stall=2,
            enable_planning=True,
            stall_detector=stall_detector,
            pre_submit_guard=pre_submit_guard,
            task_progress_tracker=task_progress_tracker,
            run_logger=run_logger,
        )

        logger.info(f"[{run_id}] 开始执行 agent.run()...")
        try:
            result = await agent.run(max_steps=max_steps)
            logger.info(f"[{run_id}] agent.run() 完成")
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
