"""Browser Agent 封装类"""

import logging
import time
import uuid
from typing import Any

from browser_use import Agent, BrowserProfile

from backend.llm.base import BaseLLM
from backend.llm.browser_use_adapter import BrowserUseAdapter
from backend.utils.logger import StructuredLogger
from backend.utils.screenshot import ScreenshotManager
from backend.agent.prompts import CHINESE_ENHANCEMENT

logger = logging.getLogger(__name__)


class UIBrowserAgent:
    """封装 Browser-Use Agent，集成国内模型

    提供简化的接口来执行 UI 自动化任务：
    - 自动集成国内 LLM（通义千问）
    - 自动保存截图和日志
    - 支持回调函数监控执行过程
    """

    def __init__(
        self,
        task: str,
        llm: BaseLLM,
        output_dir: str = "outputs",
        task_id: str | None = None,
        max_failures: int = 3,
        use_vision: bool = True,
    ):
        """初始化 Agent

        Args:
            task: 任务描述（自然语言）
            llm: LLM 实例（如 QwenChat）
            output_dir: 输出目录
            task_id: 任务 ID（可选，自动生成）
            max_failures: 最大失败次数
            use_vision: 是否使用视觉能力
        """
        self.task = task
        self.llm = llm
        self.output_dir = output_dir
        self.task_id = task_id or str(uuid.uuid4())[:8]
        self.max_failures = max_failures
        self.use_vision = use_vision

        # 创建适配器
        self.adapter = BrowserUseAdapter(llm)

        # 初始化工具
        self.screenshot_manager = ScreenshotManager(output_dir, self.task_id)
        self.logger = StructuredLogger(output_dir, self.task_id)

        # 执行状态
        self._step_count = 0
        self._start_time: float | None = None

    async def run(self) -> dict:
        """执行任务

        Returns:
            执行结果字典，包含：
            - success: 是否成功
            - steps: 执行步数
            - duration_seconds: 执行时长
            - screenshot_dir: 截图目录
            - log_file: 日志文件
        """
        self._start_time = time.time()
        self._step_count = 0

        logger.info(f"开始执行任务: {self.task[:50]}...")
        logger.info(f"任务 ID: {self.task_id}")

        try:
            # 创建 Browser-Use Agent
            agent = Agent(
                task=self.task,
                llm=self.adapter,
                extend_system_message=CHINESE_ENHANCEMENT,
                max_failures=self.max_failures,
                use_vision=self.use_vision,
                register_new_step_callback=self._on_step,
                browser_profile=BrowserProfile(wait_between_actions=0.5),
            )

            # 执行
            result = await agent.run()

            # 记录摘要
            duration = time.time() - self._start_time
            self.logger.log_summary(
                total_steps=self._step_count,
                success=result.is_done,
                duration_seconds=duration,
            )

            logger.info(f"任务完成: 成功={result.is_done}, 步数={self._step_count}")

            return {
                "success": result.is_done,
                "steps": self._step_count,
                "duration_seconds": duration,
                "screenshot_dir": self.screenshot_manager.get_dir(),
                "log_file": self.logger.get_log_file(),
            }

        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            self.logger.log_error(self._step_count, str(e))

            duration = time.time() - self._start_time if self._start_time else 0
            return {
                "success": False,
                "steps": self._step_count,
                "duration_seconds": duration,
                "error": str(e),
                "screenshot_dir": self.screenshot_manager.get_dir(),
                "log_file": self.logger.get_log_file(),
            }

    async def _on_step(self, browser_state, agent_output, step: int) -> None:
        """每步回调函数

        Args:
            browser_state: 浏览器状态
            agent_output: Agent 输出
            step: 步骤编号
        """
        self._step_count = step

        # 提取动作信息
        action = ""
        selector = None
        reasoning = ""

        if agent_output and hasattr(agent_output, "action"):
            actions = agent_output.action
            if actions and len(actions) > 0:
                first_action = actions[0]
                action = getattr(first_action, "action", "")
                selector = getattr(first_action, "selector", None)
                reasoning = getattr(first_action, "reasoning", "")

        # 获取截图
        screenshot_path = None
        try:
            if browser_state and hasattr(browser_state, "page"):
                screenshot_path = self.screenshot_manager.get_path(step)
                await browser_state.page.screenshot(path=screenshot_path)
        except Exception as e:
            logger.warning(f"截图失败: {e}")

        # 记录日志
        self.logger.log_step(
            step=step,
            action=action,
            selector=selector,
            reasoning=reasoning,
            success=True,
            screenshot_path=screenshot_path,
        )

        logger.info(f"步骤 {step}: {action} - {reasoning[:50] if reasoning else ''}")
