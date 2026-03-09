"""DeepSeek LLM 实现

DeepSeek API 与 OpenAI 兼容，支持结构化输出。
"""

import os
from typing import Any

from openai import AsyncOpenAI
from pydantic import BaseModel

from browser_use.llm.base import BaseChatModel
from browser_use.llm.messages import BaseMessage
from browser_use.llm.views import ChatInvokeCompletion, ChatInvokeUsage


class DeepSeekChat(BaseChatModel):
    """DeepSeek 聊天模型

    使用 DeepSeek API（OpenAI 兼容）。
    支持结构化输出，适合 Browser-Use 集成。
    """

    _verified_api_keys: bool = True

    def __init__(
        self,
        model: str = "deepseek-chat",
        api_key: str | None = None,
        base_url: str = "https://api.deepseek.com/v1",
        temperature: float = 0.2,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url
        self.temperature = temperature

        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 未配置")

        self._client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    @property
    def provider(self) -> str:
        return "deepseek"

    @property
    def name(self) -> str:
        return self.model

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        output_format: type[BaseModel] | None = None,
        **kwargs: Any,
    ) -> ChatInvokeCompletion[Any]:
        """调用 DeepSeek API

        Args:
            messages: 消息列表
            output_format: 期望的输出格式（结构化输出）
            **kwargs: 其他参数

        Returns:
            ChatInvokeCompletion
        """
        # 转换消息格式
        openai_messages = self._convert_messages(messages)

        # 构建请求参数
        request_params = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
        }

        # 添加结构化输出（如果需要）
        if output_format is not None:
            # DeepSeek 支持 response_format
            request_params["response_format"] = {
                "type": "json_object"
            }

        # 调用 API
        response = await self._client.chat.completions.create(**request_params)

        # 提取响应
        choice = response.choices[0]
        content = choice.message.content or ""

        # 构建 usage
        usage = None
        if response.usage:
            usage = ChatInvokeUsage(
                prompt_tokens=response.usage.prompt_tokens,
                prompt_cached_tokens=0,
                prompt_cache_creation_tokens=0,
                prompt_image_tokens=0,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        # 处理输出
        if output_format is None:
            return ChatInvokeCompletion(
                completion=content,
                usage=usage,
                stop_reason=choice.finish_reason,
            )
        else:
            # 解析结构化输出
            import json
            try:
                json_content = json.loads(content)
                parsed = output_format.model_validate(json_content)
                return ChatInvokeCompletion(
                    completion=parsed,
                    usage=usage,
                    stop_reason=choice.finish_reason,
                )
            except json.JSONDecodeError as e:
                raise ValueError(f"无法解析 JSON 输出: {e}\n内容: {content[:500]}")

    def _convert_messages(self, messages: list[BaseMessage]) -> list[dict]:
        """转换消息格式为 OpenAI 格式

        Args:
            messages: Browser-Use 消息列表

        Returns:
            OpenAI 格式的消息列表
        """
        converted = []

        for msg in messages:
            role = getattr(msg, "role", "user")
            content = getattr(msg, "content", "")

            # 处理多模态内容
            if isinstance(content, str):
                converted.append({"role": role, "content": content})
            elif isinstance(content, list):
                # 构建多模态内容
                parts = []
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            parts.append({"type": "text", "text": part.get("text", "")})
                        elif part.get("type") == "image_url":
                            url_data = part.get("image_url", {})
                            if isinstance(url_data, dict):
                                url = url_data.get("url", "")
                            else:
                                url = str(url_data)
                            parts.append({
                                "type": "image_url",
                                "image_url": {"url": url}
                            })

                converted.append({"role": role, "content": parts})
            else:
                converted.append({"role": role, "content": str(content)})

        return converted
