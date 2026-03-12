"""Agent 服务 - 封装 browser-use Agent"""

from typing import Any, Callable

from browser_use import Agent

from backend.llm.factory import create_llm


class AgentService:
    """browser-use Agent 服务封装"""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir

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

    async def run_with_streaming(
        self,
        task: str,
        on_step: Callable[[int, str, str, str | None], None],
        max_steps: int = 10,
        llm_config: dict | None = None,
    ) -> Any:
        """带流式回调的执行

        Args:
            task: 自然语言任务描述
            on_step: 步骤回调函数 (step, action, reasoning, screenshot_path)
            max_steps: 最大执行步数
            llm_config: LLM 配置

        Returns:
            Agent 执行历史
        """
        llm = create_llm(llm_config)

        def step_callback(browser_state, agent_output, step: int):
            # 提取动作和推理
            action = ""
            reasoning = ""
            if agent_output and hasattr(agent_output, "action"):
                actions = agent_output.action
                if actions and len(actions) > 0:
                    first_action = actions[0]
                    action = getattr(first_action, "action", "")
                    reasoning = getattr(first_action, "reasoning", "")

            on_step(step, action, reasoning, None)

        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=5,
            register_new_step_callback=step_callback,
        )

        result = await agent.run(max_steps=max_steps)
        return result
