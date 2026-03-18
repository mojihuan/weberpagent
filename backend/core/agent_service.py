"""Agent 服务 - 封装 browser-use Agent"""

import base64
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, Union

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

        async def step_callback(browser_state, agent_output, step: int):
            logger.debug(f"[{run_id}] 步骤回调: step={step}")
            # 提取动作和推理 - 从 agent_output 顶层获取
            action = ""
            reasoning = ""
            if agent_output:
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

                # 获取推理信息（evaluation + memory + next_goal）
                parts = []
                if hasattr(agent_output, "evaluation_previous_goal") and agent_output.evaluation_previous_goal:
                    parts.append(f"Eval: {agent_output.evaluation_previous_goal}")
                if hasattr(agent_output, "memory") and agent_output.memory:
                    parts.append(f"Memory: {agent_output.memory}")
                if hasattr(agent_output, "next_goal") and agent_output.next_goal:
                    parts.append(f"Goal: {agent_output.next_goal}")
                reasoning = " | ".join(parts) if parts else ""

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

        # 如果有目标 URL，拼接到任务描述前面
        actual_task = task
        if target_url:
            actual_task = f"目标URL: {target_url}\n\n任务:\n{task}"
            logger.info(f"[{run_id}] 已将目标 URL 拼接到任务描述中")

        logger.info(f"[{run_id}] 创建 Agent: task={actual_task[:80]}..., max_steps={max_steps}")
        agent = Agent(
            task=actual_task,
            llm=llm,
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
