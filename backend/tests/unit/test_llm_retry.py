# backend/tests/unit/test_llm_retry.py
"""LLM 重试逻辑单元测试"""

import pytest
from unittest.mock import patch, MagicMock

from backend.llm.factory import create_llm, _should_retry_llm_error, RETRYABLE_ERRORS


class TestShouldRetryLlmError:
    """测试 _should_retry_llm_error 辅助函数"""

    def test_retry_on_timeout_error(self):
        """测试 TimeoutError 触发重试"""
        error = TimeoutError("Connection timed out")
        assert _should_retry_llm_error(error) is True

    def test_retry_on_connection_error(self):
        """测试 ConnectionError 触发重试"""
        error = ConnectionError("Failed to connect")
        assert _should_retry_llm_error(error) is True

    def test_retry_on_rate_limit_429(self):
        """测试 429 错误触发重试"""
        error = Exception("Error 429: Rate limit exceeded")
        assert _should_retry_llm_error(error) is True

    def test_retry_on_rate_limit_503(self):
        """测试 503 错误触发重试"""
        error = Exception("Error 503: Service unavailable")
        assert _should_retry_llm_error(error) is True

    def test_retry_on_timeout_in_message(self):
        """测试错误消息包含 'timeout' 触发重试"""
        error = Exception("Request timed out after 30s")
        assert _should_retry_llm_error(error) is True

    def test_retry_on_rate_limit_in_message(self):
        """测试错误消息包含 'rate limit' 触发重试"""
        error = Exception("API rate limit exceeded")
        assert _should_retry_llm_error(error) is True

    def test_no_retry_on_auth_401(self):
        """测试 401 认证错误不重试"""
        error = Exception("Error 401: Unauthorized")
        assert _should_retry_llm_error(error) is False

    def test_no_retry_on_auth_403(self):
        """测试 403 禁止访问错误不重试"""
        error = Exception("Error 403: Forbidden")
        assert _should_retry_llm_error(error) is False

    def test_no_retry_on_invalid_api_key(self):
        """测试无效 API Key 错误不重试"""
        error = Exception("Invalid API key provided")
        assert _should_retry_llm_error(error) is False

    def test_no_retry_on_quota_exceeded(self):
        """测试配额超限错误不重试"""
        error = Exception("Quota exceeded for this billing period")
        assert _should_retry_llm_error(error) is False

    def test_no_retry_on_unauthorized(self):
        """测试 'unauthorized' 错误不重试"""
        error = Exception("Unauthorized access")
        assert _should_retry_llm_error(error) is False

    def test_no_retry_on_insufficient_quota(self):
        """测试 'insufficient' 错误不重试"""
        error = Exception("Insufficient funds")
        assert _should_retry_llm_error(error) is False


class TestCreateLlmRetry:
    """测试 create_llm 重试逻辑"""

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_create_llm_success_no_retry(self, mock_chat_openai):
        """测试成功创建 LLM 不触发重试"""
        mock_instance = MagicMock()
        mock_instance.model = "gpt-4o"
        mock_instance.provider = "openai"
        mock_chat_openai.return_value = mock_instance

        result = create_llm({"model": "gpt-4o", "api_key": "test-key"})

        assert result == mock_instance
        assert mock_chat_openai.call_count == 1

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_retry_on_timeout(self, mock_chat_openai):
        """测试 TimeoutError 触发重试"""
        # 第一次调用失败，第二次成功
        mock_instance = MagicMock()
        mock_instance.model = "gpt-4o"
        mock_instance.provider = "openai"
        mock_chat_openai.side_effect = [
            TimeoutError("Connection timed out"),
            mock_instance,
        ]

        result = create_llm({"model": "gpt-4o", "api_key": "test-key"})

        assert result == mock_instance
        assert mock_chat_openai.call_count == 2

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_retry_on_connection_error(self, mock_chat_openai):
        """测试 ConnectionError 触发重试"""
        mock_instance = MagicMock()
        mock_instance.model = "gpt-4o"
        mock_instance.provider = "openai"
        mock_chat_openai.side_effect = [
            ConnectionError("Failed to connect"),
            mock_instance,
        ]

        result = create_llm({"model": "gpt-4o", "api_key": "test-key"})

        assert result == mock_instance
        assert mock_chat_openai.call_count == 2

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_no_retry_on_auth_error(self, mock_chat_openai):
        """测试认证错误不重试，直接抛出"""
        mock_chat_openai.side_effect = Exception("Error 401: Unauthorized")

        with pytest.raises(Exception, match="401"):
            create_llm({"model": "gpt-4o", "api_key": "invalid-key"})

        # 认证错误不应重试，只调用一次
        assert mock_chat_openai.call_count == 1

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_max_retries_exceeded(self, mock_chat_openai):
        """测试超过最大重试次数后抛出异常"""
        mock_chat_openai.side_effect = TimeoutError("Connection timed out")

        with pytest.raises(TimeoutError, match="timed out"):
            create_llm({"model": "gpt-4o", "api_key": "test-key"})

        # 初始调用 + 2 次重试 = 3 次（tenacity stop_after_attempt(3) 意味着总共最多 3 次尝试）
        assert mock_chat_openai.call_count == 3

    @patch("browser_use.llm.openai.chat.ChatOpenAI")
    def test_exponential_backoff(self, mock_chat_openai):
        """测试指数退避重试（1s, 2s, 4s）"""
        import time

        mock_instance = MagicMock()
        mock_instance.model = "gpt-4o"
        mock_instance.provider = "openai"

        call_times = []

        def track_time(*args, **kwargs):
            call_times.append(time.time())
            if len(call_times) < 3:
                raise TimeoutError("Connection timed out")
            return mock_instance

        mock_chat_openai.side_effect = track_time

        start = time.time()
        result = create_llm({"model": "gpt-4o", "api_key": "test-key"})
        elapsed = time.time() - start

        assert result == mock_instance
        assert mock_chat_openai.call_count == 3
        # 验证总时间大约为 1 + 2 = 3 秒（第一次失败后等待 1s，第二次失败后等待 2s）
        # 允许一定误差
        assert elapsed >= 2.5, f"Expected at least 2.5s for retries, got {elapsed}s"
