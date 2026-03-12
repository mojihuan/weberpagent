"""
LLM 模块

当前仅支持 OpenAI 官方 API。
历史适配器已归档到 _archived/llm/

注意：openai.py 将在后续任务中创建
"""

from .base import BaseLLM
from .config import LLMConfig, get_config
from .factory import LLMFactory, get_llm

__all__ = [
    "BaseLLM",
    "LLMConfig",
    "get_config",
    "LLMFactory",
    "get_llm",
]
