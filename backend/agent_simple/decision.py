"""LLM 决策模块 - 调用模型生成动作"""

import json
import logging
import re
from backend.llm.base import BaseLLM
from backend.agent_simple.types import Action, PageState
from backend.agent_simple.prompts import build_messages

logger = logging.getLogger(__name__)


class Decision:
    """LLM 决策模块

    负责调用 LLM 并解析输出为结构化动作
    """

    def __init__(self, llm: BaseLLM):
        """初始化决策模块

        Args:
            llm: LLM 实例（支持 vision 的模型）
        """
        self.llm = llm

    async def decide(self, task: str, state: PageState) -> Action:
        """根据页面状态决定下一步动作

        Args:
            task: 任务描述
            state: 当前页面状态

        Returns:
            Action: 解析后的动作对象
        """
        # 1. 构建消息
        messages = build_messages(task, state)

        # 2. 构建图像 URL（data URI 格式）
        # 检查截图是否有效（非空且长度足够）
        if state.screenshot_base64 and len(state.screenshot_base64) > 100:
            image_url = f"data:image/png;base64,{state.screenshot_base64}"
            images = [image_url]
        else:
            # 截图无效时，不传图片，LLM 将依赖 DOM 信息
            logger.warning("截图无效，LLM 将仅基于 DOM 信息决策")
            images = []

        logger.info(f"调用 LLM 决策，模型: {self.llm.model_name}")

        # 3. 调用 LLM
        response = await self.llm.chat_with_vision(
            messages=messages,
            images=images,
        )

        logger.info(f"LLM 原始输出: {response.content[:200]}...")

        # 4. 解析输出
        action = self._parse_action(response.content)

        logger.info(f"解析后的动作: {action.action}, 目标: {action.target}")

        return action

    def _parse_action(self, response: str) -> Action:
        """解析 LLM 输出为 Action 对象

        Args:
            response: LLM 的原始文本输出

        Returns:
            Action: 解析后的动作对象
        """
        # 尝试提取 JSON 块
        json_str = self._extract_json(response)

        if json_str:
            try:
                data = json.loads(json_str)
                return Action(
                    thought=data.get("thought", ""),
                    action=data.get("action", "wait"),
                    target=data.get("target"),
                    value=data.get("value"),
                    done=data.get("done", False),
                    result=data.get("result"),
                )
            except json.JSONDecodeError as e:
                logger.warning(f"JSON 解析失败: {e}")

        # 解析失败，返回默认等待动作
        logger.warning(f"无法解析 LLM 输出，返回 wait 动作")
        return Action(
            thought=f"解析失败，原始输出: {response[:100]}",
            action="wait",
            done=False,
        )

    def _extract_json(self, text: str) -> str | None:
        """从文本中提取 JSON 字符串

        支持：
        1. 纯 JSON
        2. ```json ... ```
        3. ``` ... ```

        Args:
            text: 可能包含 JSON 的文本

        Returns:
            JSON 字符串或 None
        """
        # 尝试提取 ```json ... ``` 代码块
        json_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(json_block_pattern, text)
        if match:
            return match.group(1).strip()

        # 尝试提取 {...} 对象
        brace_start = text.find("{")
        brace_end = text.rfind("}")
        if brace_start >= 0 and brace_end > brace_start:
            return text[brace_start : brace_end + 1]

        return None
