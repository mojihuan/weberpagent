"""测试断言服务"""

import pytest
from backend.core.assertion_service import AssertionService
from backend.api.schemas.index import Assertion


@pytest.fixture
def service():
    return AssertionService()


def test_check_url_contains_success(service):
    """测试 URL 包含检查 - 成功"""
    class MockHistory:
        final_result = type("Result", (), {"url": "https://example.com/dashboard"})()

    result = service.check_url_contains(MockHistory(), "/dashboard")
    assert result is True


def test_check_url_contains_failure(service):
    """测试 URL 包含检查 - 失败"""
    class MockHistory:
        final_result = type("Result", (), {"url": "https://example.com/login"})()

    result = service.check_url_contains(MockHistory(), "/dashboard")
    assert result is False


def test_check_text_exists_success(service):
    """测试文本存在检查 - 成功"""
    class MockHistory:
        final_result = type("Result", (), {"extracted_content": "欢迎回来，用户"})()

    result = service.check_text_exists(MockHistory(), "欢迎")
    assert result is True


def test_check_no_errors_success(service):
    """测试无错误检查 - 成功"""
    class MockHistory:
        is_done = True

    result = service.check_no_errors(MockHistory())
    assert result is True


def test_run_all_assertions(service):
    """测试运行所有断言"""
    class MockHistory:
        is_done = True
        final_result = type(
            "Result", (), {"url": "https://example.com/dashboard"}
        )()

    assertions = [
        Assertion(name="URL检查", type="url_contains", expected="/dashboard"),
        Assertion(name="无错误", type="no_errors", expected=True),
    ]

    results = service.run_all_assertions(MockHistory(), assertions)
    assert results["URL检查"] is True
    assert results["无错误"] is True
