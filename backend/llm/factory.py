"""LLM 实例工厂 - 根据模块名称创建对应的 LLM 实例

注意：当前 qwen.py 已归档到 _archived/llm/，需要创建 OpenAI 实现。
使用 set_llm_class() 方法设置具体的 LLM 实现。
"""

import logging
from typing import Type, Optional

from .base import BaseLLM
from .config import LLMConfig, get_config

logger = logging.getLogger(__name__)

# 尝试导入可用的 LLM 实现
_LLM_CLASS: Optional[Type[BaseLLM]] = None

# 尝试导入 QwenChat（已归档）
try:
    from backend._archived.llm.qwen import QwenChat

    _LLM_CLASS = QwenChat
    logger.info("使用已归档的 QwenChat 实现（建议迁移到 OpenAI）")
except ImportError:
    logger.debug("QwenChat 不可用，请使用 set_llm_class() 设置 LLM 实现")


class LLMFactory:
    """LLM 实例工厂

    根据模块名称从配置中获取对应的模型，创建 LLM 实例
    使用缓存避免重复创建

    使用前需要先调用 set_llm_class() 设置 LLM 实现类。
    """

    _instances: dict[str, BaseLLM] = {}
    _llm_class: Optional[Type[BaseLLM]] = _LLM_CLASS

    @classmethod
    def set_llm_class(cls, llm_class: Type[BaseLLM]) -> None:
        """设置 LLM 类（用于测试或切换实现）"""
        cls._llm_class = llm_class

    @classmethod
    def create(cls, module_path: str) -> BaseLLM:
        """创建或获取 LLM 实例

        Args:
            module_path: 模块路径，如 "simple_agent.reflect" 或 "decision"

        Returns:
            LLM 实例

        Raises:
            RuntimeError: 未设置 LLM 实现类
        """
        if cls._llm_class is None:
            raise RuntimeError(
                "LLM 实现类未设置。请先调用 LLMFactory.set_llm_class() "
                "设置 LLM 实现（如 OpenAI），或确保 QwenChat 可用。"
            )

        config = get_config()
        model = config.get_model(module_path)

        # 使用 model 作为缓存 key（同模型共享实例）
        cache_key = f"{cls._llm_class.__name__}:{model}"

        if cache_key not in cls._instances:
            logger.info(f"创建 LLM 实例: model={model}, module={module_path}")
            api_key = config.get_api_key()
            cls._instances[cache_key] = cls._llm_class(
                model=model,
                api_key=api_key,
            )
        else:
            logger.debug(f"复用 LLM 实例: model={model}")

        return cls._instances[cache_key]

    @classmethod
    def get_reflect_llm(cls) -> BaseLLM:
        """获取反思模块 LLM"""
        return cls.create("simple_agent.reflect")

    @classmethod
    def get_decision_llm(cls) -> BaseLLM:
        """获取决策模块 LLM"""
        return cls.create("decision")

    @classmethod
    def get_code_generator_llm(cls) -> BaseLLM:
        """获取代码生成模块 LLM"""
        return cls.create("form_filler.code_generator")

    @classmethod
    def get_code_optimizer_llm(cls) -> BaseLLM:
        """获取代码优化模块 LLM"""
        return cls.create("form_filler.code_optimizer")

    @classmethod
    def get_code_reviewer_llm(cls) -> BaseLLM:
        """获取代码审查模块 LLM"""
        return cls.create("form_filler.code_reviewer")

    @classmethod
    def clear_cache(cls) -> None:
        """清除缓存（用于测试）"""
        cls._instances.clear()


def get_llm(module_path: str) -> BaseLLM:
    """便捷函数：获取指定模块的 LLM 实例"""
    return LLMFactory.create(module_path)


def create_llm(llm_config: dict | None = None) -> "ChatOpenAI":
    """创建 browser-use 兼容的 ChatOpenAI 实例

    Args:
        llm_config: 可选的 LLM 配置字典
            - model: 模型名称，默认 gpt-4o
            - api_key: API Key，默认从环境变量读取
            - base_url: API Base URL，支持 OpenAI 兼容接口
            - temperature: 温度参数，默认 0.1

    Returns:
        ChatOpenAI 实例，可直接传递给 browser-use Agent
    """
    from .openai import OpenAIChat

    config = llm_config or {}
    model = config.get("model", "gpt-4o")
    api_key = config.get("api_key")
    base_url = config.get("base_url")
    temperature = config.get("temperature", 0.1)

    logger.info(f"create_llm: model={model}, base_url={base_url}, temperature={temperature}")
    logger.debug(f"create_llm: api_key={'*' * 8 if api_key else 'from env'}")

    try:
        openai_chat = OpenAIChat(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
        )
        llm = openai_chat.llm

        # 修复 browser-use 兼容性问题
        # browser-use 0.12.1 尝试访问 llm.provider 属性
        # 但 langchain_openai.ChatOpenAI 没有这个属性
        llm.provider = "openai"

        logger.info(f"create_llm: 成功创建 ChatOpenAI, model_name={getattr(llm, 'model_name', 'unknown')}, provider={getattr(llm, 'provider', 'unknown')}")
        return llm
    except Exception as e:
        logger.error(f"create_llm: 创建失败 - {e}")
        raise
