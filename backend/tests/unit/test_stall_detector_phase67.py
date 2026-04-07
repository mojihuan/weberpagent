"""Unit tests for StallDetector Phase 67 additions.

Tests cover FailureDetectionResult frozen dataclass and
detect_failure_mode() method for three ERP table interaction failure modes:
- click_no_effect: click with no DOM change
- wrong_column: evaluation indicates wrong column clicked
- edit_not_active: input action on non-editable element
"""

import dataclasses

import pytest

from backend.agent.stall_detector import FailureDetectionResult, StallDetector


class TestDetectFailureMode:
    """Tests for StallDetector.detect_failure_mode() method."""

    def test_click_no_effect(self):
        """Click with same dom_hash before and after should detect click_no_effect."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation="ok",
            dom_hash_before="abc",
            dom_hash_after="abc",
        )
        assert result.failure_mode == "click_no_effect"
        assert result.details["target_index"] == 5
        assert result.details["dom_hash"] == "abc"

    def test_click_no_effect_different_hash(self):
        """Click with different dom hashes should NOT detect click_no_effect."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation="ok",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode is None

    def test_wrong_column_chinese(self):
        """Evaluation with Chinese wrong-column keyword should detect wrong_column."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=10,
            evaluation="点了错误列的元素",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "wrong_column"
        assert "keywords_matched" in result.details
        assert len(result.details["keywords_matched"]) > 0

    def test_wrong_column_english(self):
        """Evaluation with English wrong-column keyword should detect wrong_column."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=10,
            evaluation="clicked wrong column",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "wrong_column"

    def test_wrong_column_non_target(self):
        """Evaluation with non-target-column keyword should detect wrong_column."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=10,
            evaluation="非目标列",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "wrong_column"

    def test_edit_not_active_chinese(self):
        """Input action with Chinese edit-not-active keyword should detect edit_not_active."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="input",
            target_index=20,
            evaluation="元素不可操作",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "edit_not_active"

    def test_edit_not_active_english(self):
        """Input action with English edit-not-active keyword should detect edit_not_active."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="input",
            target_index=20,
            evaluation="not editable element",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "edit_not_active"

    def test_edit_not_active_cannot_type(self):
        """Input action with cannot-type keyword should detect edit_not_active."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="input",
            target_index=20,
            evaluation="无法输入到目标字段",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "edit_not_active"

    def test_no_failure_normal_click(self):
        """Normal click with different hashes and no error keywords should return None."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation="成功",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode is None
        assert result.details == {}

    def test_no_failure_normal_input(self):
        """Normal input with no error keywords should return None."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="input",
            target_index=5,
            evaluation="成功输入",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode is None
        assert result.details == {}

    def test_frozen_dataclass(self):
        """FailureDetectionResult should be immutable (frozen dataclass)."""
        result = FailureDetectionResult(failure_mode="test", details={})
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.failure_mode = "other"  # type: ignore[misc]

    def test_wrong_column_priority_over_click_no_effect(self):
        """wrong_column should take priority over click_no_effect when both conditions met."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation="点了错误列",
            dom_hash_before="abc",
            dom_hash_after="abc",
        )
        assert result.failure_mode == "wrong_column"

    def test_details_contain_evaluation_snippet(self):
        """wrong_column details should contain evaluation_snippet truncated to 100 chars."""
        long_evaluation = "A" * 200 + "错误列" + "B" * 200
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation=long_evaluation,
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode == "wrong_column"
        assert len(result.details["evaluation_snippet"]) <= 100

    def test_edit_not_active_only_on_input_action(self):
        """edit_not_active keywords in evaluation should NOT trigger for non-input actions."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation="元素不可操作",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode is None

    def test_no_failure_empty_evaluation(self):
        """Empty evaluation string should return no failure."""
        detector = StallDetector()
        result = detector.detect_failure_mode(
            action_name="click",
            target_index=5,
            evaluation="",
            dom_hash_before="abc",
            dom_hash_after="def",
        )
        assert result.failure_mode is None
