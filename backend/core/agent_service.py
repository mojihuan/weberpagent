"""Agent 服务 - 封装 browser-use Agent"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from browser_use import Agent

from backend.llm.factory import create_llm

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

    async def save_screenshot(
        self, screenshot_bytes: bytes, run_id: str, step_index: int
    ) -> str:
        """保存截图到本地文件

        Args:
            screenshot_bytes: 截图的二进制数据
            run_id: 执行 ID
            step_index: 步骤索引

        Returns:
            截图文件路径
        """
        filename = f"{run_id}_{step_index}.png"
        filepath = self.screenshots_dir / filename
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

        agent = Agent(
            task=task,
            llm=llm,
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
    ) -> Any:
        """带流式回调的执行

        Args:
            task: 自然语言任务描述
            run_id: 执行 ID（用于截图命名）
            on_step: 异步步骤回调函数 (step_index, action, reasoning, screenshot_path)
            max_steps: 最大执行步数
            llm_config: LLM 配置

        Returns:
            Agent 执行历史
        """
        logger.info(f"[{run_id}] 创建 LLM: config={llm_config}")
        llm = create_llm(llm_config)
        logger.info(f"[{run_id}] LLM 创建成功: type={type(llm).__name__}, model={getattr(llm, 'model_name', 'unknown')}")

        async def step_callback(browser_state, agent_output, step: int):
            logger.debug(f"[{run_id}] 步骤回调: step={step}")
            # 提取动作和推理
            action = ""
            reasoning = ""
            if agent_output and hasattr(agent_output, "action"):
                actions = agent_output.action
                if actions and len(actions) > 0:
                    first_action = actions[0]
                    action = getattr(first_action, "action", "")
                    reasoning = getattr(first_action, "reasoning", "")

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
            if asyncio.iscoroutinefunction(on_step):
                await on_step(step, action, reasoning, screenshot_path)
            else:
                on_step(step, action, reasoning, screenshot_path)

        logger.info(f"[{run_id}] 创建 Agent: task={task[:50]}..., max_steps={max_steps}")
        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
        )

        logger.info(f"[{run_id}] 开始执行 agent.run()...")
        result = await agent.run(max_steps=max_steps)
        logger.info(f"[{run_id}] agent.run() 完成")
        return result
