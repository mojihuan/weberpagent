"""代码优化 Agent - 根据审查意见或执行错误优化代码"""

import logging
import re

from backend.llm.base import BaseLLM
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewIssue
from backend.agent_simple.form_filler.prompts import build_code_optimizer_prompt

logger = logging.getLogger(__name__)


class CodeOptimizer:
    """代码优化 Agent - 根据审查意见或执行错误优化代码"""

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def optimize(
        self,
        code: str,
        elements: list[InteractiveElement],
        issues: list[ReviewIssue] | None = None,
        execution_error: str | None = None,
    ) -> str:
        """优化代码

        Args:
            code: 原始代码
            elements: 页面元素列表
            issues: 审查问题列表（可选）
            execution_error: 执行错误信息（可选）

        Returns:
            优化后的代码
        """
        if not issues and not execution_error:
            logger.info("无需优化，返回原代码")
            return code

        # 构建 Prompt
        issues_dict = [
            {"severity": i.severity, "line": i.line, "message": i.message}
            for i in (issues or [])
        ]

        prompt = build_code_optimizer_prompt(
            code=code,
            issues=issues_dict,
            elements=elements,
            execution_error=execution_error,
        )

        # 调用 LLM
        logger.info(f"调用代码优化 LLM，模型: {self.llm.model_name}")
        response = await self.llm.chat_with_vision(messages=prompt, images=[])

        # 提取代码
        optimized_code = self._extract_code(response.content)
        logger.info(f"代码优化完成，原长度: {len(code)}，新长度: {len(optimized_code)}")

        return optimized_code

    def _extract_code(self, response: str) -> str:
        """从响应中提取代码"""
        import json

        # 1. 优先从 ```json 代码块中提取 JSON，然后提取 code 字段
        json_block_pattern = r"```json\s*([\s\S]*?)\s*```"
        match = re.search(json_block_pattern, response)
        if match:
            try:
                data = json.loads(match.group(1))
                if isinstance(data, dict) and "code" in data:
                    return data["code"].strip()
            except json.JSONDecodeError:
                pass

        # 2. 从 ```python 代码块提取
        code_block_pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
        match = re.search(code_block_pattern, response)
        if match:
            content = match.group(1).strip()
            # 如果内容是 JSON，尝试解析
            try:
                data = json.loads(content)
                if isinstance(data, dict) and "code" in data:
                    return data["code"].strip()
            except json.JSONDecodeError:
                pass
            # 否则直接返回代码
            return content

        # 3. 尝试直接解析整个响应为 JSON
        try:
            data = json.loads(response)
            if isinstance(data, dict) and "code" in data:
                return data["code"].strip()
        except json.JSONDecodeError:
            pass

        # 4. 尝试找到函数定义开始
        func_start = response.find("async def fill_form")
        if func_start >= 0:
            return response[func_start:].strip()

        return response.strip()