"""
LLM 模块

当前支持 OpenAI 官方 API 和 OpenAI 兼容接口。
历史适配器已归档到 _archived/llm/
"""

from .base import BaseLLM, LLMResponse, ActionResult
from .config import LLMConfig, get_config
from .factory import LLMFactory, get_llm
from .openai import OpenAIChat

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "LLMConfig",
    "get_config",
    "LLMFactory",
    "get_llm",
    "OpenAIChat",
]
