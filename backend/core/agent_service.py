"""Agent 服务 - 封装 browser-use Agent"""

from datetime import datetime
from pathlib import Path
from typing import Any, Callable

 Optional

from browser_use import Agent

from backend.llm.factory import create_llm


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
        llm = create_llm(llm_config)

        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
        )

        result = await agent.run(max_steps=max_steps)
        return result

