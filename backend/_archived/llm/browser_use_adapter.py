"""
⚠️ 已归档 - 2026-03-12

原因：切换到官方 OpenAI API，不再需要国产模型适配器。
保留供历史参考。

替代方案：直接使用 langchain_openai.ChatOpenAI
"""

"""Browser-Use LLM 适配器"""

import json
import logging
import re
from typing import Any, TypeVar

from pydantic import BaseModel

from browser_use.llm.base import BaseChatModel
from browser_use.llm.messages import BaseMessage
from browser_use.llm.views import ChatInvokeCompletion, ChatInvokeUsage

from .base import BaseLLM

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class BrowserUseAdapter(BaseChatModel):
    """将国内模型适配到 Browser-Use 的 BaseChatModel Protocol

    这个适配器将我们的 QwenChat（或其他 BaseLLM 实现）
    转换为 Browser-Use 期望的接口格式。
    """

    _verified_api_keys: bool = True  # 跳过 Browser-Use 的 API Key 验证

    def __init__(self, llm: BaseLLM):
        """初始化适配器

        Args:
            llm: 底层 LLM 实例（如 QwenChat）
        """
        self._llm = llm
        self.model = llm.model_name

    @property
    def provider(self) -> str:
        """返回提供商名称"""
        return "chinese-domestic"

    @property
    def name(self) -> str:
        """返回模型名称"""
        return self.model

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        output_format: type[BaseModel] | None = None,
        **kwargs: Any,
    ) -> ChatInvokeCompletion[Any]:
        """调用底层 LLM 并返回结果

        Args:
            messages: Browser-Use 格式的消息列表
            output_format: 期望的输出格式（用于结构化输出）
            **kwargs: 其他参数

        Returns:
            ChatInvokeCompletion 包含响应内容
        """
        # 1. 转换消息格式
        converted_messages, images = self._convert_messages(messages)

        # 2. 调用底层 LLM
        response = await self._llm.chat_with_vision(
            messages=converted_messages,
            images=images,
        )

        # 3. 构建 usage 对象
        usage_data = response.usage or {}
        usage = ChatInvokeUsage(
            prompt_tokens=usage_data.get("input_tokens", 0),
            prompt_cached_tokens=0,
            prompt_cache_creation_tokens=0,
            prompt_image_tokens=0,
            completion_tokens=usage_data.get("output_tokens", 0),
            total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
        )

        # 4. 处理输出
        content = response.content

        if output_format is None:
            # 返回字符串响应
            return ChatInvokeCompletion(
                completion=content,
                usage=usage,
            )
        else:
            # 需要结构化输出 - 解析 JSON 并转换为 Pydantic 对象
            json_content = self._extract_json(content)

            try:
                # 使用 Pydantic 验证并解析
                parsed = output_format.model_validate(json_content)
                return ChatInvokeCompletion(
                    completion=parsed,
                    usage=usage,
                )
            except Exception as e:
                logger.error(f"解析结构化输出失败: {e}")
                logger.error(f"原始内容: {content[:500]}...")
                logger.error(f"提取的 JSON: {json.dumps(json_content, ensure_ascii=False)[:500]}...")
                raise

    def _extract_json(self, content: str) -> dict:
        """从 LLM 输出中提取 JSON

        支持以下格式：
        1. 纯 JSON 对象
        2. Markdown 代码块中的 JSON
        3. 嵌入在文本中的 JSON

        Args:
            content: LLM 返回的内容

        Returns:
            解析后的字典
        """
        # 尝试提取 markdown 代码块中的 JSON
        code_block_pattern = r"```(?:json)?\s*([\s\S]*?)```"
        matches = re.findall(code_block_pattern, content)

        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

        # 尝试找到最外层的 JSON 对象
        depth = 0
        start = -1
        for i, char in enumerate(content):
            if char == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        return json.loads(content[start : i + 1])
                    except json.JSONDecodeError:
                        start = -1
                        continue

        # 尝试直接解析
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # 返回空字典作为 fallback
        logger.warning(f"无法解析 JSON 输出: {content[:200]}...")
        return {}

    def _convert_messages(
        self, messages: list[BaseMessage]
    ) -> tuple[list[dict], list[str]]:
        """转换消息格式并提取图像

        Args:
            messages: Browser-Use 格式的消息列表

        Returns:
            (转换后的消息列表, 图像列表)
        """
        converted = []
        images = []

        for msg in messages:
            # 提取角色
            role = getattr(msg, "role", "user")

            # 处理内容（可能是字符串或列表）
            content = getattr(msg, "content", "")
            text_parts = []
            image_urls = []

            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text_parts.append(part.get("text", ""))
                        elif part.get("type") == "image_url":
                            url = part.get("image_url", {})
                            if isinstance(url, dict):
                                image_urls.append(url.get("url", ""))
                            elif isinstance(url, str):
                                image_urls.append(url)
                        elif part.get("type") == "image":
                            img_data = part.get("image", "")
                            if img_data:
                                image_urls.append(img_data)

            # 合并文本
            full_text = "\n".join(text_parts)
            converted.append({"role": role, "content": full_text})

            # 收集图像
            images.extend(image_urls)

        return converted, images
