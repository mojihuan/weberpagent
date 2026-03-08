"""通义千问视觉模型实现"""

import json
import os
from typing import Any

import dashscope
from dashscope import MultiModalConversation
from tenacity import retry, stop_after_attempt, wait_exponential

from .base import BaseLLM, LLMResponse, ActionResult
from .utils import encode_image_to_base64


class QwenChat(BaseLLM):
    """通义千问视觉模型实现"""

    def __init__(
        self,
        model: str = "qwen-vl-max",
        api_key: str | None = None,
        max_retries: int = 3,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.max_retries = max_retries

        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置")

        dashscope.api_key = self.api_key

    @property
    def model_name(self) -> str:
        return self.model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],
    ) -> LLMResponse:
        """调用通义千问视觉模型"""

        # 构建消息内容
        content = self._build_content(messages, images)

        response = MultiModalConversation.call(
            model=self.model,
            messages=[{"role": "user", "content": content}],
        )

        if response.status_code != 200:
            raise RuntimeError(f"API 调用失败: {response.message}")

        # 提取响应内容（可能是字符串或列表格式）
        raw_content = response.output.choices[0].message.content
        if isinstance(raw_content, list):
            # 列表格式: [{'text': '...'}]
            text = " ".join(
                item.get("text", "") for item in raw_content if isinstance(item, dict)
            )
        else:
            text = str(raw_content)

        return LLMResponse(
            content=text,
            action=self.parse_action(text),
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        )

    def _build_content(self, messages: list[dict], images: list[str]) -> list:
        """构建多模态消息内容"""
        content = []

        # 添加图像
        for img in images:
            if img.startswith("http"):
                content.append({"image": img})
            else:
                # 本地文件转 base64
                base64_data = encode_image_to_base64(img)
                content.append({"image": f"data:image/png;base64,{base64_data}"})

        # 添加文本消息
        text = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )
        content.append({"text": text})

        return content

    def parse_action(self, response: str) -> ActionResult | None:
        """解析 Browser-Use 格式的动作输出"""
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
