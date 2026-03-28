"""Unit tests for PreSubmitGuard -- validates form fields before submit clicks.

Covers:
- MON-04: Extract expected values from task description via regex
- MON-05: Block submit when click targets submit button and values mismatch
- MON-06: Skip blocking when no expectations can be extracted
"""

from __future__ import annotations

import pytest

from backend.agent.pre_submit_guard import EXPECTATION_PATTERNS, GuardResult, PreSubmitGuard


# ---------------------------------------------------------------------------
# MON-04: Expectation extraction
# ---------------------------------------------------------------------------


class TestPreSubmitGuardExtraction:
    """Tests for _extract_expectations() -- MON-04."""

    def setup_method(self) -> None:
        self.guard = PreSubmitGuard()

    def test_extract_sales_amount(self) -> None:
        """Extract '150' from task containing '销售金额150元'."""
        result = self.guard._extract_expectations("销售金额150元")
        assert result.get("销售金额") == "150"

    def test_extract_logistics_fee(self) -> None:
        """Extract '30' from task containing '物流费用30元'."""
        result = self.guard._extract_expectations("物流费用30元")
        assert result.get("物流费用") == "30"

    def test_extract_payment_status(self) -> None:
        """Extract '已付款' from task containing '付款状态：已付款'."""
        result = self.guard._extract_expectations("付款状态：已付款")
        assert result.get("付款状态") == "已付款"

    def test_no_extraction_without_amounts(self) -> None:
        """No expectations extracted from task without amounts or status."""
        result = self.guard._extract_expectations("点击确认按钮")
        assert result == {}


# ---------------------------------------------------------------------------
# MON-05: Block submit on mismatch, MON-06: Skip when no expectations
# ---------------------------------------------------------------------------


class TestPreSubmitGuardCheck:
    """Tests for check() method -- MON-05, MON-06."""

    def setup_method(self) -> None:
        self.guard = PreSubmitGuard()

    def test_blocks_submit_on_mismatch(self) -> None:
        """Click on submit button with mismatched actual_values -> should_block=True."""
        result = self.guard.check(
            action_name="click",
            target_index=0,
            task="销售金额150元",
            actual_values={"销售金额": "200"},
            submit_button_text="确认",
        )
        assert result.should_block is True
        assert "提交拦截" in result.message
        assert "销售金额" in result.message

    def test_allows_submit_on_match(self) -> None:
        """Click on submit button with matching actual_values -> should_block=False."""
        result = self.guard.check(
            action_name="click",
            target_index=0,
            task="销售金额150元",
            actual_values={"销售金额": "150"},
            submit_button_text="确认",
        )
        assert result.should_block is False
        assert result.message == ""

    def test_skips_when_no_expectations(self) -> None:
        """Click on submit button but no amounts in task -> should_block=False (MON-06)."""
        result = self.guard.check(
            action_name="click",
            target_index=0,
            task="点击确认按钮",
            actual_values={},
            submit_button_text="确认",
        )
        assert result.should_block is False

    def test_non_click_action_passes(self) -> None:
        """Non-click action always passes regardless of values."""
        result = self.guard.check(
            action_name="input",
            target_index=5,
            task="销售金额150元",
            actual_values={"销售金额": "200"},
            submit_button_text=None,
        )
        assert result.should_block is False

    def test_non_submit_button_passes(self) -> None:
        """Click action on non-submit button passes."""
        result = self.guard.check(
            action_name="click",
            target_index=0,
            task="销售金额150元",
            actual_values={"销售金额": "200"},
            submit_button_text="取消",
        )
        assert result.should_block is False

    def test_no_actual_values_skips_blocking(self) -> None:
        """Click on submit button but actual_values=None -> should_block=False."""
        result = self.guard.check(
            action_name="click",
            target_index=0,
            task="销售金额150元",
            actual_values=None,
            submit_button_text="确认",
        )
        assert result.should_block is False


# ---------------------------------------------------------------------------
# GuardResult immutability
# ---------------------------------------------------------------------------


class TestGuardResultImmutability:
    """GuardResult must be frozen (immutable)."""

    def test_guard_result_is_frozen(self) -> None:
        """GuardResult should raise FrozenInstanceError on mutation attempt."""
        result = GuardResult(should_block=True, message="test")
        with pytest.raises(AttributeError):
            result.should_block = False  # type: ignore[misc]

    def test_guard_result_stores_values(self) -> None:
        """GuardResult should store values correctly."""
        result = GuardResult(should_block=True, message="blocked")
        assert result.should_block is True
        assert result.message == "blocked"
