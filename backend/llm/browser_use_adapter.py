"""Browser-Use LLM 适配器"""

import logging
from typing import Any

from pydantic import BaseModel

from browser_use.llm.base import BaseChatModel
from browser_use.llm.messages import BaseMessage
from browser_use.llm.views import ChatInvokeCompletion

from .base import BaseLLM

logger = logging.getLogger(__name__)


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
    ) -> ChatInvokeCompletion[str]:
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

        # 3. 返回 Browser-Use 期望的格式
        return ChatInvokeCompletion(
            content=response.content,
            usage=response.usage,
        )

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
                            # 处理 image 类型
                            img_data = part.get("image", "")
                            if img_data:
                                image_urls.append(img_data)

            # 合并文本
            full_text = "\n".join(text_parts)
            converted.append({"role": role, "content": full_text})

            # 收集图像
            images.extend(image_urls)

        return converted, images
