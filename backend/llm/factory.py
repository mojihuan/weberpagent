"""LLM 实例工厂 - 创建 browser-use 兼容的 ChatOpenAI 实例"""

from __future__ import annotations

import logging
from typing import Optional

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logger = logging.getLogger(__name__)

RETRYABLE_ERRORS = (
    TimeoutError,
    ConnectionError,
)


def _should_retry_llm_error(exception: Exception) -> bool:
    """判断 LLM 错误是否可重试"""
    error_str = str(exception).lower()

    non_retryable = ["401", "403", "unauthorized", "invalid api key", "quota", "insufficient"]
    if any(pattern in error_str for pattern in non_retryable):
        return False

    retryable = ["429", "503", "timeout", "rate limit", "connection", "timed out", "connect"]
    return any(pattern in error_str for pattern in retryable)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(RETRYABLE_ERRORS),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def create_llm(llm_config: dict | None = None) -> "BaseLLM":
    """创建 browser-use 兼容的 ChatOpenAI 实例（带重试逻辑）

    Args:
        llm_config: 可选的 LLM 配置字典
            - model: 模型名称，默认 gpt-4o
            - api_key: API Key
            - base_url: API Base URL
            - temperature: 温度参数，默认 0.0

    Returns:
        ChatOpenAI 实例
    """
    from browser_use.llm.openai.chat import ChatOpenAI as BrowserUseChatOpenAI

    config = llm_config or {}
    model = config.get("model", "gpt-4o")
    api_key = config.get("api_key")
    base_url = config.get("base_url")
    temperature = config.get("temperature", 0.0)

    attempt_number = create_llm.retry.statistics.get("attempt_number", 0)
    if attempt_number > 0:
        logger.warning(f"LLM 调用重试，第 {attempt_number} 次")

    logger.info(f"create_llm: model={model}, base_url={base_url}, temperature={temperature}")
    logger.debug(f"create_llm: api_key={'*' * 8 if api_key else 'from env'}")

    try:
        llm = BrowserUseChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
        )
        logger.info(f"create_llm: 成功创建 ChatOpenAI, model={llm.model}, provider={llm.provider}")
        return llm
    except Exception as e:
        error_type = type(e).__name__
        logger.error(f"create_llm: 创建失败 - {error_type}: {e}")
        if not _should_retry_llm_error(e):
            logger.error("create_llm: 不可重试错误，放弃重试")
            raise
        raise


def get_llm(module_path: str):
    """便捷函数：获取指定模块的 LLM 实例（兼容旧接口，实际使用 create_llm）"""
    raise NotImplementedError("get_llm is deprecated, use create_llm() instead")


# Backward compatibility alias
LLMFactory = None
