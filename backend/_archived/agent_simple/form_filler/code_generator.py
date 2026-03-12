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
        # ========== 调试：打印传递给 LLM 的元素信息 ==========
        logger.info("=" * 60)
        logger.info("📋 传递给 LLM 的元素信息:")
        logger.info(f"   元素总数: {len(state.elements)}")
        for el in state.elements[:10]:  # 只打印前 10 个
            logger.info(f"   [{el.index}] <{el.tag}> text='{el.text[:30] if el.text else ''}' placeholder='{el.placeholder}' id='{el.id}' name='{el.name}'")
        if len(state.elements) > 10:
            logger.info(f"   ... 还有 {len(state.elements) - 10} 个元素")
        logger.info("=" * 60)

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
        logger.info(f"调用代码生成 LLM，模型: {self.llm.model_name}")
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
        # 1. 优先尝试从 ```json 代码块中提取
        json_code = self._extract_code_from_json_block(response)
        if json_code:
            logger.debug("从 JSON 代码块中提取代码成功")
            return json_code

        # 2. 提取 ```python 代码块
        code_block_pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
        match = re.search(code_block_pattern, response)
        if match:
            logger.debug("从 Python 代码块中提取代码成功")
            return match.group(1).strip()

        # 3. 尝试提取 async def fill_form
        func_start = response.find("async def fill_form")
        if func_start >= 0:
            logger.debug("直接提取 fill_form 函数")
            return response[func_start:].strip()

        logger.warning("无法提取代码，返回原始响应")
        return response.strip()

    def _extract_code_from_json_block(self, response: str) -> str | None:
        """从 JSON 格式中提取代码

        支持两种方式：
        1. 标准JSON 解析
        2. 正则表达式提取（处理非标准 JSON）
        """
        # 1. 尝试标准 JSON 解析
        # 1.1 查找 ```json ... ``` 块
        json_block_pattern = r"```json\s*([\s\S]*?)\s*```"
        match = re.search(json_block_pattern, response)
        if match:
            json_str = match.group(1)
            code = self._try_parse_json_for_code(json_str)
            if code:
                return code

        # 1.2 尝试找最大的 JSON 对象
        start = response.find("{")
        end = response.rfind("}")
        if start >= 0 and end > start:
            json_str = response[start:end+1]
            code = self._try_parse_json_for_code(json_str)
            if code:
                return code

        # 2. 使用手动解析提取 code 字段（处理非标准 JSON 和嵌套引号）
        # 查找 "code": " 字符串的起始位置
        code_start_match = re.search(r'"code"\s*:\s*"', response)
        if code_start_match:
            start_pos = code_start_match.end()
            # 从起始位置开始，找到匹配的结束引号
            code_chars = []
            i = start_pos
            while i < len(response):
                char = response[i]
                if char == '\\' and i + 1 < len(response):
                    # 处理转义字符
                    next_char = response[i + 1]
                    if next_char == 'n':
                        code_chars.append('\n')
                    elif next_char == 't':
                        code_chars.append('\t')
                    elif next_char == '"':
                        code_chars.append('"')
                    elif next_char == '\\':
                        code_chars.append('\\')
                    elif next_char == "'":
                        code_chars.append("'")
                    else:
                        code_chars.append(next_char)
                    i += 2
                elif char == '"':
                    # 找到结束引号
                    break
                else:
                    code_chars.append(char)
                    i += 1

            code = ''.join(code_chars)
            if code:
                logger.debug("通过手动解析提取 code 字段成功")
                return code

        return None

    def _try_parse_json_for_code(self, json_str: str) -> str | None:
        """尝试解析 JSON 并提取 code 字段"""
        try:
            data = json.loads(json_str)
            if "code" in data and isinstance(data["code"], str):
                return data["code"]
        except json.JSONDecodeError as e:
            logger.debug(f"JSON 解析失败: {e}")
        return None

    def _extract_field_values(self, response: str) -> dict:
        """从响应中提取字段值

        支持两种格式:
        1. JSON 格式中的 field_values
        2. 注释格式: # FIELD_VALUES: {"name": "value"}
        """
        # 1. 尝试标准 JSON 解析
        # 1.1 从 ```json 代码块中提取
        json_block_pattern = r"```json\s*([\s\S]*?)\s*```"
        match = re.search(json_block_pattern, response)
        if match:
            json_str = match.group(1)
            field_values = self._try_parse_json_for_field_values(json_str)
            if field_values:
                return field_values

        # 1.2 尝试找最大的 JSON 对象
        start = response.find("{")
        end = response.rfind("}")
        if start >= 0 and end > start:
            json_str = response[start:end+1]
            field_values = self._try_parse_json_for_field_values(json_str)
            if field_values:
                return field_values

        # 2. 使用正则表达式直接提取 field_values 字段
        field_pattern = r'"field_values"\s*:\s*(\{[^}]*\})'
        match = re.search(field_pattern, response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # 3. 尝试从注释格式提取
        pattern = r"#\s*FIELD_VALUES:\s*(\{.*?\})"
        match = re.search(pattern, response)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        return {}

    def _try_parse_json_for_field_values(self, json_str: str) -> dict | None:
        """尝试解析 JSON 并提取 field_values 字段"""
        try:
            data = json.loads(json_str)
            if "field_values" in data and isinstance(data["field_values"], dict):
                return data["field_values"]
        except json.JSONDecodeError:
            pass
        return None

    def _extract_description(self, code: str) -> str:
        """从代码中提取描述"""
        lines = code.split("\n")[:3]
        return " | ".join(line.strip() for line in lines if line.strip())