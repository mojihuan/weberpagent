"""代码生成 Agent - 生成 Playwright 代码片段"""

import json
import logging
import re

from backend.llm.base import BaseLLM
from backend.agent_simple.types import PageState
from backend.agent_simple.form_filler.types import GeneratedCode
from backend.agent_simple.form_filler.prompts import build_code_generator_prompt

logger = logging.getLogger(__name__)


class CodeGenerator:
    """代码生成 Agent

    根据页面状态和任务描述，生成 Playwright 代码片段
    """

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def generate(self, state: PageState, task: str) -> GeneratedCode:
        """生成 Playwright 代码

        Args:
            state: 当前页面状态
            task: 任务描述

        Returns:
            GeneratedCode: 生成的代码和元数据
        """
        # 1. 构建 Prompt（返回消息列表）
        messages = build_code_generator_prompt(
            task=task,
            elements=state.elements,
            page_url=state.url,
        )

        # 2. 准备图像
        images = []
        if state.screenshot_base64 and len(state.screenshot_base64) > 100:
            images.append(f"data:image/png;base64,{state.screenshot_base64}")

        # 3. 调用 LLM
        response = await self.llm.chat_with_vision(messages=messages, images=images)

        # 4. 解析响应
        code = self._extract_code(response.content)
        field_values = self._extract_field_values(response.content)
        description = self._extract_description(code)

        return GeneratedCode(
            code=code,
            description=description,
            field_values=field_values,
        )

    def _extract_code(self, response: str) -> str:
        """从 LLM 响应中提取代码"""
        # 优先尝试从 JSON 中提取
        json_code = self._extract_code_from_json(response)
        if json_code:
            return json_code

        # 提取代码块
        code_block_pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
        match = re.search(code_block_pattern, response)
        if match:
            return match.group(1).strip()

        # 尝试提取 async def fill_form
        func_start = response.find("async def fill_form")
        if func_start >= 0:
            return response[func_start:].strip()

        return response.strip()

    def _extract_code_from_json(self, response: str) -> str | None:
        """尝试从 JSON 格式中提取代码"""
        # 查找 JSON 块
        json_pattern = r"\{[\s\S]*?\}"
        for match in re.finditer(json_pattern, response):
            try:
                data = json.loads(match.group())
                if "code" in data and isinstance(data["code"], str):
                    return data["code"]
            except json.JSONDecodeError:
                continue
        return None

    def _extract_field_values(self, response: str) -> dict:
        """从响应中提取字段值

        支持两种格式:
        1. JSON 格式中的 field_values
        2. 注释格式: # FIELD_VALUES: {"name": "value"}
        """
        # 尝试从 JSON 中提取
        json_pattern = r"\{[\s\S]*?\}"
        for match in re.finditer(json_pattern, response):
            try:
                data = json.loads(match.group())
                if "field_values" in data and isinstance(data["field_values"], dict):
                    return data["field_values"]
            except json.JSONDecodeError:
                continue

        # 尝试从注释格式提取
        pattern = r"#\s*FIELD_VALUES:\s*(\{.*?\})"
        match = re.search(pattern, response)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        return {}

    def _extract_description(self, code: str) -> str:
        """从代码中提取描述"""
        lines = code.split("\n")[:3]
        return " | ".join(line.strip() for line in lines if line.strip())