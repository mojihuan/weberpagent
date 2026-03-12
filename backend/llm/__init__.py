"""LLM 模块 - 多模型适配层"""

from .base import BaseLLM, LLMResponse, ActionResult
from .qwen import QwenChat
from .deepseek import DeepSeekChat
from .azure_openai import AzureOpenAIChat
from .browser_use_adapter import BrowserUseAdapter
from .config import LLMConfig, get_config
from .factory import LLMFactory, get_llm

__all__ = [
    "BaseLLM",
    "LLMResponse",
    "ActionResult",
    "QwenChat",
    "DeepSeekChat",
    "AzureOpenAIChat",
    "BrowserUseAdapter",
    "LLMConfig",
    "get_config",
    "LLMFactory",
    "get_llm",
]


def get_default_llm() -> BaseLLM:
    """获取默认的 LLM 实例（使用工厂创建）"""
    return get_llm("decision")
