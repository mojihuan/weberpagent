"""LLM 抽象基类和数据模型"""

from abc import ABC, abstractmethod
from pydantic import BaseModel


class ActionResult(BaseModel):
    """解析后的动作结果"""

    action: str  # 动作类型: click, fill, goto, etc.
    selector: str | None = None  # 目标元素选择器
    value: str | None = None  # 输入值（fill 时使用）
    reasoning: str = ""  # AI 的推理说明


class LLMResponse(BaseModel):
    """LLM 响应封装"""

    content: str  # 原始文本响应
    action: ActionResult | None = None  # 解析后的动作（如果适用）
    usage: dict = {}  # token 使用统计


class BaseLLM(ABC):
    """国内模型统一接口"""

    @abstractmethod
    async def chat_with_vision(
        self,
        messages: list[dict],
        images: list[str],  # 支持 URL 或 base64
    ) -> LLMResponse:
        """带图像理解的对话

        Args:
            messages: OpenAI 格式的消息列表
            images: 图像列表（URL 或 base64 字符串）

        Returns:
            LLMResponse 包含响应内容和解析后的动作
        """
        pass

    @abstractmethod
    def parse_action(self, response: str) -> ActionResult | None:
        """解析模型输出为结构化动作

        Args:
            response: 模型的原始文本输出

        Returns:
            ActionResult 或 None（如果无法解析）
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """返回模型名称，用于日志"""
        pass
