"""LLM 实例工厂 - 根据模块名称创建对应的 LLM 实例"""

import logging
from typing import Type

from .base import BaseLLM
from .config import LLMConfig, get_config
from .qwen import QwenChat

logger = logging.getLogger(__name__)


class LLMFactory:
    """LLM 实例工厂

    根据模块名称从配置中获取对应的模型，创建 LLM 实例
    使用缓存避免重复创建
    """

    _instances: dict[str, BaseLLM] = {}
    _llm_class: Type[BaseLLM] = QwenChat

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
        """
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
