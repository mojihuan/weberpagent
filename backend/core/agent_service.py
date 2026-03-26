"""Agent 服务 - 封装 browser-use Agent"""

import base64
import hashlib
import json
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, Union

from browser_use import Agent, BrowserSession, BrowserProfile

from backend.llm.factory import create_llm


# 服务器环境必需的 Chrome 参数
SERVER_BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
]


class LoopInterventionTracker:
    """Tracks action repetition and page stagnation for early intervention.

    Per D-01: Triggers intervention when stagnation >= 5.
    Maintains independent tracking parallel to browser-use's internal ActionLoopDetector.
    """

    def __init__(self, window_size: int = 20, stagnation_threshold: int = 5):
        self.window_size = window_size
        self.stagnation_threshold = stagnation_threshold
        self.recent_action_hashes: list[str] = []
        self.recent_page_fingerprints: list[str] = []
        self.consecutive_stagnant_pages: int = 0
        self.max_repetition_count: int = 0
        self.recent_actions: list[dict] = []

    def _compute_action_hash(self, action_name: str, params: dict) -> str:
        """Compute hash for action similarity detection."""
        if action_name in ('click', 'input'):
            index = params.get('index')
            if action_name == 'input':
                text = str(params.get('text', '')).strip().lower()
                normalized = f'input|{index}|{text}'
            else:
                normalized = f'click|{index}'
        elif action_name == 'navigate':
            url = str(params.get('url', ''))
            normalized = f'navigate|{url}'
        else:
            filtered = {k: v for k, v in sorted(params.items()) if v is not None}
            normalized = f'{action_name}|{json.dumps(filtered, sort_keys=True, default=str)}'
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:12]

    def record_action(self, action_name: str, params: dict) -> None:
        """Record action and update repetition stats."""
        h = self._compute_action_hash(action_name, params)
        self.recent_action_hashes.append(h)
        self.recent_actions.append({"action": action_name, "params": params})
        if len(self.recent_action_hashes) > self.window_size:
            self.recent_action_hashes = self.recent_action_hashes[-self.window_size:]
            self.recent_actions = self.recent_actions[-self.window_size:]
        self._update_repetition_stats()

    def _update_repetition_stats(self) -> None:
        """Update max_repetition_count from recent action hashes."""
        if not self.recent_action_hashes:
            self.max_repetition_count = 0
            return
        counts = Counter(self.recent_action_hashes)
        self.max_repetition_count = max(counts.values()) if counts else 0

    def record_page_state(self, url: str, dom_hash: str) -> None:
        """Record page fingerprint and update stagnation count.

        Semantics: consecutive_stagnant_pages counts how many times we've seen
        the same page state consecutively. First occurrence = 1, second = 2, etc.
        """
        fp = f"{url}:{dom_hash}"
        if self.recent_page_fingerprints and self.recent_page_fingerprints[-1] == fp:
            # Same as previous - increment count
            self.consecutive_stagnant_pages += 1
        else:
            # Different from previous (or first ever) - start count at 1
            self.consecutive_stagnant_pages = 1
        self.recent_page_fingerprints.append(fp)
        if len(self.recent_page_fingerprints) > self.window_size:
            self.recent_page_fingerprints = self.recent_page_fingerprints[-self.window_size:]

    def should_intervene(self) -> bool:
        """Check if intervention threshold is reached (D-01: stagnation >= 5)."""
        return self.consecutive_stagnant_pages >= self.stagnation_threshold

    def get_intervention_message(self) -> str:
        """Generate intervention prompt for the agent (per D-01).

        Provides context-specific suggestions based on recent action patterns.
        """
        base_msg = f"⚠️ 循环干预: 连续 {self.consecutive_stagnant_pages} 次相同页面状态。"

        # Analyze recent action patterns for targeted suggestions
        recent_action_types = [a.get('action', '') for a in self.recent_actions[-5:]]
        action_counts = {}
        for action_type in recent_action_types:
            action_counts[action_type] = action_counts.get(action_type, 0) + 1

        suggestions = []

        # Check for repeated input failures
        if action_counts.get('input', 0) >= 3:
            suggestions.extend([
                "输入操作可能失败: 1) 确认点击的是 INPUT 元素而非 TD 单元格",
                "2) 使用 scroll_table_and_input_action 工具处理表格输入",
                "3) 先用 find_elements 查找所有输入框再选择正确的 index"
            ])

        # Check for repeated click failures
        elif action_counts.get('click', 0) >= 3:
            suggestions.extend([
                "点击可能无效: 1) 尝试双击 (doubleClick: true)",
                "2) 滚动页面后重试 (scroll -> pages: 0.5)",
                "3) 使用不同的元素选择器或 index"
            ])

        # Check for scroll_table_and_input failures
        elif action_counts.get('scroll_table_and_input_action', 0) >= 2:
            suggestions.extend([
                "表格工具失败: 1) 检查列标题是否正确 (使用 find_elements 查看表头)",
                "2) 尝试更通用的列名 (如 '金额' 而非 '销售金额（元）')",
                "3) 手动定位: find_elements -> click -> input"
            ])

        # Default suggestions
        else:
            suggestions.extend([
                "1) 滚动页面查看更多元素 (scroll -> down: true)",
                "2) 使用 find_elements 查找目标元素",
                "3) 如果当前步骤非关键，考虑跳过"
            ])

        return base_msg + "\n建议: " + " | ".join(suggestions)

    def get_diagnostic_info(self) -> dict:
        """Get diagnostic information for logging/storage (per D-02)."""
        return {
            "stagnation": self.consecutive_stagnant_pages,
            "max_repetition_count": self.max_repetition_count,
            "recent_actions": self.recent_actions[-10:],
            "intervention_triggered": self.should_intervene(),
        }


def create_browser_session() -> BrowserSession:
    """创建适用于服务器的 BrowserSession"""
    browser_profile = BrowserProfile(
        headless=True,
        args=SERVER_BROWSER_ARGS,
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
        filename = f"{run_id}_{step_index}.png"
        filepath = self.screenshots_dir / filename

        # 处理不同类型的输入
        if isinstance(screenshot_data, str):
            # 如果是字符串，尝试 base64 解码
            try:
                screenshot_bytes = base64.b64decode(screenshot_data)
            except Exception as e:
                logger.warning(f"[{run_id}] base64 解码失败，尝试直接编码: {e}")
                # 如果不是 base64，可能是普通的字符串路径或其他格式
                screenshot_bytes = screenshot_data.encode('utf-8')
        else:
            screenshot_bytes = screenshot_data

        filepath.write_bytes(screenshot_bytes)
        return str(filepath)

    async def run_simple(
        self,
        task: str,
        max_steps: int = 10,
        llm_config: dict | None = None,
    ) -> Any:
        """简单执行任务

        Args:
            task: 自然语言任务描述
            max_steps: 最大执行步数
            llm_config: LLM 配置

        Returns:
            Agent 执行历史
        """
        logger.info(f"创建 LLM: config={llm_config}")
        llm = create_llm(llm_config)
        logger.info(f"LLM 创建成功: type={type(llm).__name__}")

        # 创建本地浏览器会话
        browser_session = create_browser_session()

        agent = Agent(
            task=task,
            llm=llm,
            browser_session=browser_session,
            max_actions_per_step=5,
        )

        result = await agent.run(max_steps=max_steps)
        return result

    async def run_with_streaming(
        self,
        task: str,
        run_id: str,
        on_step: Callable[[int, str, str, str | None], Any],
        max_steps: int = 10,
        llm_config: dict | None = None,
        target_url: str | None = None,
    ) -> Any:
        """带流式回调的执行

        Args:
            task: 自然语言任务描述
            run_id: 执行 ID（用于截图命名）
            on_step: 异步步骤回调函数 (step_index, action, reasoning, screenshot_path)
            max_steps: 最大执行步数
            llm_config: LLM 配置
            target_url: 目标 URL（执行前先导航到此页面）

        Returns:
            Agent 执行历史
        """
        logger.info(f"[{run_id}] 创建 LLM: config={llm_config}")
        llm = create_llm(llm_config)
        logger.info(f"[{run_id}] LLM 创建成功: type={type(llm).__name__}, model={getattr(llm, 'model_name', 'unknown')}")

        # 创建本地浏览器会话
        browser_session = create_browser_session()

        # 存储引用供 step_callback 访问 (Phase 42, D-01)
        self._browser_session = browser_session

        # Create loop intervention tracker (per D-01)
        tracker = LoopInterventionTracker(window_size=20, stagnation_threshold=5)
        loop_intervention_data = {"value": None}  # Mutable container for closure (Phase 39, LOG-01)
        step_stats_data = {"value": None}  # Mutable container for step stats (Phase 41, LOG-02)

        async def step_callback(browser_state, agent_output, step: int):
            logger.debug(f"[{run_id}] 步骤回调: step={step}")

            # ===== 详细日志: browser_state =====
            if browser_state:
                url = getattr(browser_state, "url", "") or ""
                logger.info(f"[{run_id}][BROWSER] URL: {url}")

                # 记录 DOM 状态（使用正确的属性名 dom_state）
                dom_state = getattr(browser_state, "dom_state", None)
                if dom_state:
                    # dom_state 可能是字符串或对象
                    dom_str = str(dom_state)
                    logger.info(f"[{run_id}][BROWSER] DOM 状态长度: {len(dom_str)} 字符")

                    # 将 DOM 内容写入文件（便于调试）
                    dom_file = self.output_dir / f"dom_{run_id}_step{step}.txt"
                    dom_file.parent.mkdir(parents=True, exist_ok=True)
                    dom_file.write_text(dom_str, encoding='utf-8')
                    logger.info(f"[{run_id}][BROWSER] DOM 已保存到: {dom_file}")

                    # 计算 DOM 哈希用于停滞检测
                    dom_hash = hashlib.sha256(dom_str.encode('utf-8')).hexdigest()[:12]
                else:
                    dom_hash = ""
                    logger.warning(f"[{run_id}][BROWSER] dom_state 为空")

                # 记录元素树信息（如果存在）
                element_tree = getattr(browser_state, "element_tree", None)
                if element_tree is not None:
                    element_count = len(element_tree) if hasattr(element_tree, '__len__') else 0
                    logger.info(f"[{run_id}][BROWSER] 元素数量: {element_count}")

                    # 记录前 5 个元素的关键信息
                    for i, elem in enumerate(list(element_tree)[:5]):
                        if hasattr(elem, '__dict__'):
                            elem_dict = {k: v for k, v in elem.__dict__.items()
                                        if k in ('index', 'tag_name', 'role', 'text', 'aria_label')}
                            logger.info(f"[{run_id}][BROWSER] 元素[{i}]: {elem_dict}")
                        elif isinstance(elem, dict):
                            logger.info(f"[{run_id}][BROWSER] 元素[{i}]: {elem}")

                # 记录页面信息
                page_info = getattr(browser_state, "page_info", None)
                if page_info:
                    logger.debug(f"[{run_id}][BROWSER] page_info: {page_info}")

            else:
                logger.warning(f"[{run_id}][BROWSER] browser_state 为空!")
                dom_hash = ""

            # ===== 详细日志: agent_output =====
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

                        # Record action for loop detection (D-01)
                        if not isinstance(action_params, dict):
                            action_params = {}
                        tracker.record_action(action_name, action_params)

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

            # Record page state for stagnation detection (D-01)
            if browser_state:
                url = getattr(browser_state, "url", "") or ""
                dom_content = getattr(browser_state, "dom", "") or ""
                dom_hash = hashlib.sha256(dom_content.encode('utf-8')).hexdigest()[:12] if dom_content else ""
                tracker.record_page_state(url, dom_hash)
                logger.debug(f"[{run_id}][STAGNATION] 页面指纹: {dom_hash}, 连续停滞: {tracker.consecutive_stagnant_pages}")

            # Collect step statistics (Phase 41, LOG-02, per D-02)
            # Get element count (number of interactive elements on page)
            element_count = 0
            if browser_state:
                element_tree = getattr(browser_state, "element_tree", None)
                if element_tree is not None:
                    # element_tree is a list-like structure
                    element_count = len(element_tree) if hasattr(element_tree, '__len__') else 0

            # Action count: how many actions agent decided to take this step
            action_count = 1  # Default to 1 action
            if agent_output and hasattr(agent_output, "action") and agent_output.action:
                action_count = len(agent_output.action)

            # Build step_stats dict (per D-02)
            step_stats = {
                "action_count": action_count,
                "stagnation": tracker.consecutive_stagnant_pages,
                "duration_ms": 0,  # Will be updated if timing wrapper exists
                "element_count": element_count,
            }
            step_stats_data["value"] = json.dumps(step_stats, ensure_ascii=False)

            # Check for loop intervention (D-01, D-02)
            if tracker.should_intervene():
                intervention_msg = tracker.get_intervention_message()
                diagnostic = tracker.get_diagnostic_info()
                # Store diagnostic for future Step storage integration (Phase 39, LOG-01)
                loop_intervention_data["value"] = json.dumps(diagnostic, ensure_ascii=False)
                # Log full diagnostic info (D-02: 包含 stagnation 值、最近动作、页面变化)
                logger.warning(
                    f"[{run_id}] Loop intervention triggered: "
                    f"stagnation={diagnostic['stagnation']}, "
                    f"max_repetition={diagnostic['max_repetition_count']}, "
                    f"recent_actions_count={len(diagnostic['recent_actions'])}"
                )
                # Log recent actions for debugging
                for i, act in enumerate(diagnostic['recent_actions'][-5:]):
                    logger.info(f"[{run_id}] Recent action {i}: {act['action']} -> {act.get('params', {})}")

            # 提取截图
            screenshot_path = None
            if browser_state and hasattr(browser_state, "screenshot"):
                screenshot_bytes = browser_state.screenshot
                if screenshot_bytes:
                    screenshot_path = await self.save_screenshot(
                        screenshot_bytes, run_id, step
                    )
                    logger.debug(f"[{run_id}] 截图已保存: {screenshot_path}")

            # 调用异步回调
            import asyncio
            step_stats_json = step_stats_data["value"]
            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, action, reasoning, screenshot_path, step_stats_json)
            else:
                on_step(step, action, reasoning, screenshot_path, step_stats_json)

        # 如果有目标 URL，拼接到任务描述前面
        actual_task = task
        if target_url:
            actual_task = f"目标URL: {target_url}\n\n任务:\n{task}"
            logger.info(f"[{run_id}] 已将目标 URL 拼接到任务描述中")

        logger.info(f"[{run_id}] 创建 Agent: task={actual_task[:80]}..., max_steps={max_steps}")
        agent = Agent(
            task=actual_task,
            llm=llm,
            browser_session=browser_session,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
        )

        logger.info(f"[{run_id}] 开始执行 agent.run()...")
        result = await agent.run(max_steps=max_steps)
        logger.info(f"[{run_id}] agent.run() 完成")
        return result

    async def run_with_cleanup(
        self,
        task: str,
        run_id: str,
        on_step: Callable[[int, str, str, str | None], Any],
        max_steps: int = 10,
        llm_config: dict | None = None,
        target_url: str | None = None,
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
            )
            logger.info(f"[{run_id}] Execution completed successfully")
            return result
        except Exception as e:
            logger.error(f"[{run_id}] Execution failed with error: {e}")
            logger.debug(f"[{run_id}] Error type: {type(e).__name__}")
            raise
        finally:
            logger.info(f"[{run_id}] Execution cleanup complete - resources released")
