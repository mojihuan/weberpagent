"""LLM 模块 - 国内模型适配层"""

from .base import BaseLLM, LLMResponse, ActionResult
from .qwen import QwenChat
from .browser_use_adapter import BrowserUseAdapter

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "QwenChat",
    "BrowserUseAdapter",
]


def get_default_llm() -> BaseLLM:
    """获取默认的 LLM 实例（通义千问）"""
    return QwenChat()
