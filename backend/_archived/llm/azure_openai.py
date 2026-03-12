"""Azure OpenAI LLM 实现

Azure OpenAI API 与 OpenAI 兼容，支持结构化输出。
适用于 Azure AI Foundry 部署的 OpenAI 模型。
"""

import os
from typing import Any

from openai import AsyncAzureOpenAI
from pydantic import BaseModel

from browser_use.llm.base import BaseChatModel
from browser_use.llm.messages import BaseMessage
from browser_use.llm.views import ChatInvokeCompletion, ChatInvokeUsage


class AzureOpenAIChat(BaseChatModel):
    """Azure OpenAI 聊天模型

    使用 Azure AI Foundry 部署的 OpenAI API。
    支持结构化输出和多模态输入，适合 Browser-Use 集成。
    """

    _verified_api_keys: bool = True  # 跳过 Browser-Use 的 API Key 验证

    def __init__(
        self,
        deployment: str | None = None,
        api_key: str | None = None,
        azure_endpoint: str | None = None,
        api_version: str = "2024-02-15-preview",
        temperature: float = 0.2,
    ):
        """初始化 Azure OpenAI 客户端

        Args:
            deployment: Azure 部署名称（模型）
            api_key: Azure OpenAI API 密钥
            azure_endpoint: Azure OpenAI 终端地址
            api_version: API 版本
            temperature: 生成温度
        """
        # 支持从环境变量读取 deployment
        self.deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
        self.model = self.deployment  # Browser-Use 期望 model 属性
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = api_version
        self.temperature = temperature

        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY 未配置")
        if not self.azure_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT 未配置")

        self._client = AsyncAzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.api_version,
        )

    @property
    def provider(self) -> str:
        return "azure-openai"

    @property
    def name(self) -> str:
        return self.deployment

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        output_format: type[BaseModel] | None = None,
        **kwargs: Any,
    ) -> ChatInvokeCompletion[Any]:
        """调用 Azure OpenAI API

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
            "model": self.deployment,  # Azure 使用 deployment name
            "messages": openai_messages,
            "temperature": self.temperature,
        }

        # 添加结构化输出（如果需要）
        if output_format is not None:
            request_params["response_format"] = {"type": "json_object"}

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
