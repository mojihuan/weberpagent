"""OpenAI LLM 封装

提供 OpenAI API 封装，用于 browser-use 集成和内部 Agent 系统。
"""

import json
import os
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from .base import BaseLLM, LLMResponse, ActionResult


class OpenAIChat(BaseLLM):
    """OpenAI Chat 模型封装

    使用 langchain_openai 作为底层实现，支持:
    - 直接暴露 langchain 实例给 browser-use
    - 实现 BaseLLM 接口供内部 Agent 使用
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.1,
        **kwargs: Any,
    ):
        """初始化 OpenAI Chat

        Args:
            model: 模型名称，默认 gpt-4o
            api_key: API Key，默认从环境变量读取
            base_url: API Base URL，支持 OpenAI 兼容接口
            temperature: 温度参数
            **kwargs: 其他参数传递给 ChatOpenAI
        """
        self._model = model
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self._api_key:
            raise ValueError(
                "OPENAI_API_KEY not set. "
                "Please set OPENAI_API_KEY environment variable."
            )

        # 构建ChatOpenAI参数
        llm_kwargs = {
            "model": model,
            "temperature": temperature,
            "api_key": self._api_key,
        }

        # 支持自定义 base_url (OpenAI 兼容接口)
        if base_url:
            llm_kwargs["base_url"] = base_url

        # 合并其他参数
        llm_kwargs.update(kwargs)

        self._llm = ChatOpenAI(**llm_kwargs)

    @property
    def model_name(self) -> str:
        """返回模型名称，用于日志"""
        return self._model

    @property
    def llm(self) -> ChatOpenAI:
        """获取 langchain ChatOpenAI 实例

        可直接传递给 browser-use Agent

        Returns:
            ChatOpenAI 实例
        """
        return self._llm

    async def chat(self, messages: list[dict]) -> str:
        """聊天接口

        Args:
            messages: 消息列表，格式: [{"role": "user/assistant/system", "content": "..."}]

        Returns:
            模型响应文本
        """
        lc_messages = self._convert_messages(messages)
        response = await self._llm.ainvoke(lc_messages)
        return response.content

    def _convert_messages(self, messages: list[dict]) -> list:
        """转换消息格式为 langchain 消息对象

        Args:
            messages: OpenAI 格式消息列表

        Returns:
            langchain 消息对象列表
        """
        lc_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            else:
                lc_messages.append(HumanMessage(content=content))

        return lc_messages

    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],
    ) -> LLMResponse:
        """带图像理解的对话

        GPT-4o 原生支持多模态，将图像添加到消息内容中。

        Args:
            messages: OpenAI 格式的消息列表
            images: 图像列表（URL 或 base64 字符串）

        Returns:
            LLMResponse 包含响应内容和解析后的动作
        """
        # 构建带图像的消息
        vision_messages = self._build_vision_messages(messages, images)

        # 调用模型
        response = await self._llm.ainvoke(vision_messages)

        # 提取响应文本
        text = response.content

        # 解析动作
        action = self.parse_action(text)

        # 构建 token 使用统计
        usage = {}
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            usage = {
                "input_tokens": response.usage_metadata.get("input_tokens", 0),
                "output_tokens": response.usage_metadata.get("output_tokens", 0),
            }

        return LLMResponse(
            content=text,
            action=action,
            usage=usage,
        )

    def _build_vision_messages(
        self,
        messages: list[dict],
        images: list[str],
    ) -> list:
        """构建带图像的消息

        Args:
            messages: 原始消息列表
            images: 图像列表

        Returns:
            带 langchain 消息对象的列表
        """
        lc_messages = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            else:
                # 用户消息可能包含图像
                if images and role == "user":
                    # 构建多模态内容
                    multimodal_content = self._build_multimodal_content(
                        content, images
                    )
                    lc_messages.append(HumanMessage(content=multimodal_content))
                    # 图像只添加一次到第一条用户消息
                    images = []
                else:
                    lc_messages.append(HumanMessage(content=content))

        return lc_messages

    def _build_multimodal_content(
        self,
        text: str,
        images: list[str],
    ) -> list[dict]:
        """构建多模态消息内容

        Args:
            text: 文本内容
            images: 图像列表

        Returns:
            多模态内容列表
        """
        content = [{"type": "text", "text": text}]

        for img in images:
            if img.startswith("http"):
                # HTTP URL
                content.append({
                    "type": "image_url",
                    "image_url": {"url": img},
                })
            elif img.startswith("data:"):
                # Data URI (已经是 base64 格式)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": img},
                })
            else:
                # 本地文件路径 - 需要转换为 base64
                from .utils import encode_image_to_base64
                base64_data = encode_image_to_base64(img)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_data}"},
                })

        return content

    def parse_action(self, response: str) -> ActionResult | None:
        """解析模型输出为结构化动作

        支持 Browser-Use 格式的 JSON 动作输出。

        Args:
            response: 模型的原始文本输出

        Returns:
            ActionResult 或 None（如果无法解析）
        """
        try:
            # 尝试提取 JSON 块
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(response[json_start:json_end])
                return ActionResult(
                    action=data.get("action", ""),
                    selector=data.get("selector"),
                    value=data.get("value"),
                    reasoning=data.get("reasoning", ""),
                )
        except json.JSONDecodeError:
            pass

        return None
