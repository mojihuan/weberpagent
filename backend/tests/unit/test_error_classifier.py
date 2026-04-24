"""Unit tests for error_classifier -- pure function pytest exit code classification.

覆盖全部 9 种分类路径 + frozen dataclass 验证.
"""

import dataclasses

import pytest

from backend.core.error_classifier import (
    ErrorCategory,
    ErrorCategoryResult,
    classify_pytest_error,
)


def test_exit_code_0_passed():
    """退出码 0 → PASSED, skip=False."""
    result = classify_pytest_error(0, "")
    assert result.category == ErrorCategory.PASSED
    assert result.skip_llm_healing is False
    assert "通过" in result.user_message


def test_exit_code_2_interrupt():
    """退出码 2 → ENV_INTERRUPT, skip=True."""
    result = classify_pytest_error(2, "KeyboardInterrupt")
    assert result.category == ErrorCategory.ENV_INTERRUPT
    assert result.skip_llm_healing is True
    assert "中断" in result.user_message


def test_exit_code_3_internal_error():
    """退出码 3 → ENV_PYTEST_ERROR (pytest INTERNALERROR), skip=True."""
    result = classify_pytest_error(3, "Internal Error")
    assert result.category == ErrorCategory.ENV_PYTEST_ERROR
    assert result.skip_llm_healing is True
    assert "内部错误" in result.user_message


def test_exit_code_4_pytest_error():
    """退出码 4 → ENV_PYTEST_ERROR (命令行错误), skip=True."""
    result = classify_pytest_error(4, "usage error")
    assert result.category == ErrorCategory.ENV_PYTEST_ERROR
    assert result.skip_llm_healing is True
    assert "命令行错误" in result.user_message


def test_exit_code_5_no_tests():
    """退出码 5 → ENV_NO_TESTS, skip=True."""
    result = classify_pytest_error(5, "no tests collected")
    assert result.category == ErrorCategory.ENV_NO_TESTS
    assert result.skip_llm_healing is True
    assert "未收集" in result.user_message


def test_exit_code_1_syntax_error():
    """退出码 1 + SyntaxError → CODE_ERROR, skip=False."""
    result = classify_pytest_error(1, "E   SyntaxError: invalid syntax")
    assert result.category == ErrorCategory.CODE_ERROR
    assert result.skip_llm_healing is False
    assert "语法错误" in result.user_message


def test_exit_code_1_import_error():
    """退出码 1 + ImportError → CODE_ERROR, skip=False."""
    result = classify_pytest_error(1, "E   ImportError: cannot import name 'foo'")
    assert result.category == ErrorCategory.CODE_ERROR
    assert result.skip_llm_healing is False
    assert "导入错误" in result.user_message


def test_exit_code_1_unknown_runtime():
    """退出码 1 + 无已知模式 → CODE_RUNTIME, skip=False."""
    result = classify_pytest_error(1, "E   AssertionError: assert False")
    assert result.category == ErrorCategory.CODE_RUNTIME
    assert result.skip_llm_healing is False
    assert "运行时错误" in result.user_message


def test_unknown_exit_code():
    """未知退出码 (99) → CODE_RUNTIME, skip=False, 含退出码."""
    result = classify_pytest_error(99, "something went wrong")
    assert result.category == ErrorCategory.CODE_RUNTIME
    assert result.skip_llm_healing is False
    assert "99" in result.user_message


def test_error_category_result_is_frozen():
    """ErrorCategoryResult 是 frozen dataclass (不可变)."""
    result = ErrorCategoryResult(
        category=ErrorCategory.PASSED,
        skip_llm_healing=False,
        user_message="测试通过",
    )
    assert dataclasses.is_dataclass(result)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.category = ErrorCategory.CODE_ERROR  # type: ignore[misc]
