"""
LLM 模块

当前支持 OpenAI 官方 API 和 OpenAI 兼容接口。
历史适配器已归档到 _archived/llm/
"""

from .base import BaseLLM, LLMResponse, ActionResult
from .factory import LLMFactory, get_llm, create_llm
from .openai import OpenAIChat

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "LLMFactory",
    "get_llm",
    "create_llm",
    "OpenAIChat",
]
