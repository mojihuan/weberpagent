"""HealerError 单元测试 -- 自定义异常类验证。

验证 HealerError 包含结构化字段：action_type, locators, original_error。
遵循 TokenFetchError 模式 (auth_service.py)。
"""

import pytest

from backend.core.healer_error import HealerError


class TestHealerErrorFields:
    """HealerError 字段验证。"""

    def test_fields_stored(self) -> None:
        """HealerError 包含 action_type, locators, original_error 字段。"""
        err = HealerError(
            action_type="click_element",
            locators=("page.locator('xpath=/html/body/div')", "page.locator('#btn')"),
            original_error="Timeout: 5000ms exceeded",
        )

        assert err.action_type == "click_element"
        assert err.locators == ("page.locator('xpath=/html/body/div')", "page.locator('#btn')")
        assert err.original_error == "Timeout: 5000ms exceeded"

    def test_is_exception_subclass(self) -> None:
        """HealerError 是 Exception 子类。"""
        assert issubclass(HealerError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        """HealerError 可以被 raise 和 except 捕获。"""
        with pytest.raises(HealerError) as exc_info:
            raise HealerError(
                action_type="input_text",
                locators=("page.locator('xpath=/input')",),
                original_error="Element not found",
            )

        assert exc_info.value.action_type == "input_text"


class TestHealerErrorStr:
    """HealerError.__str__() 格式验证。"""

    def test_str_contains_action_type(self) -> None:
        """__str__() 包含操作类型。"""
        err = HealerError(
            action_type="click_element",
            locators=("page.locator('xpath=/btn')",),
            original_error="timeout",
        )
        text = str(err)

        assert "click_element" in text

    def test_str_contains_locators(self) -> None:
        """__str__() 包含尝试过的定位器列表。"""
        err = HealerError(
            action_type="click_element",
            locators=("loc_a", "loc_b", "loc_c"),
            original_error="timeout",
        )
        text = str(err)

        assert "loc_a" in text
        assert "loc_b" in text
        assert "loc_c" in text

    def test_str_contains_original_error(self) -> None:
        """__str__() 包含原始错误信息。"""
        err = HealerError(
            action_type="input_text",
            locators=("loc1",),
            original_error="Connection refused",
        )
        text = str(err)

        assert "Connection refused" in text
