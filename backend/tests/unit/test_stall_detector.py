"""Unit tests for StallDetector.

Tests cover MON-01 (consecutive same-target failures),
MON-02 (stagnant DOM fingerprint), and MON-03 (success resets counter).
"""

import dataclasses

import pytest

from backend.agent.stall_detector import StallDetector, StallResult


class TestStallDetectorCheck:
    """Tests for StallDetector.check() method."""

    def test_no_stall_on_first_failure(self):
        """Single failure on target 6246 with action 'click' should not trigger intervention."""
        detector = StallDetector(max_consecutive_failures=2)
        result = detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed to input text",
            dom_hash="abc123",
        )
        assert result.should_intervene is False
        assert result.message == ""

    def test_stall_on_two_consecutive_failures_same_target(self):
        """Two consecutive failures on same target with same action should trigger."""
        detector = StallDetector(max_consecutive_failures=2)
        # First failure
        detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed to input text",
            dom_hash="abc123",
        )
        # Second failure on same target with same action
        result = detector.check(
            action_name="click",
            target_index=6246,
            evaluation="error occurred",
            dom_hash="def456",
        )
        assert result.should_intervene is True
        assert "6246" in result.message

    def test_no_stall_on_different_target(self):
        """Failures on different targets should not trigger stall."""
        detector = StallDetector(max_consecutive_failures=2)
        # First failure on target 6246
        detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed to click",
            dom_hash="abc123",
        )
        # Second failure on different target 6250
        result = detector.check(
            action_name="click",
            target_index=6250,
            evaluation="Failed to click",
            dom_hash="def456",
        )
        assert result.should_intervene is False

    def test_no_stall_on_different_action(self):
        """Failures with different actions on same target should not trigger stall."""
        detector = StallDetector(max_consecutive_failures=2)
        # First failure with 'click'
        detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed to click",
            dom_hash="abc123",
        )
        # Second failure with 'input' on same target
        result = detector.check(
            action_name="input",
            target_index=6246,
            evaluation="Failed to input",
            dom_hash="def456",
        )
        assert result.should_intervene is False

    def test_stall_on_three_identical_dom_hashes(self):
        """Three consecutive steps with identical DOM hash should trigger stagnant DOM."""
        detector = StallDetector(max_stagnant_steps=3)
        # Three steps with same dom_hash, even with success evaluations
        detector.check(
            action_name="click",
            target_index=100,
            evaluation="Success",
            dom_hash="hash1",
        )
        detector.check(
            action_name="click",
            target_index=200,
            evaluation="Success",
            dom_hash="hash1",
        )
        result = detector.check(
            action_name="click",
            target_index=300,
            evaluation="Success",
            dom_hash="hash1",
        )
        assert result.should_intervene is True

    def test_reset_on_success(self):
        """Success step should reset the consecutive failure counter."""
        detector = StallDetector(max_consecutive_failures=2)
        # First failure
        detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed to click",
            dom_hash="abc123",
        )
        # Success resets counter
        detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Successfully clicked",
            dom_hash="def456",
        )
        # Another failure after reset -- should not trigger
        result = detector.check(
            action_name="click",
            target_index=6246,
            evaluation="Failed again",
            dom_hash="ghi789",
        )
        assert result.should_intervene is False

    def test_dom_hash_change_resets_stagnant_counter(self):
        """DOM hash change should break the stagnant DOM sequence."""
        detector = StallDetector(max_stagnant_steps=3)
        # Two steps with hash1
        detector.check(
            action_name="click",
            target_index=100,
            evaluation="Success",
            dom_hash="hash1",
        )
        detector.check(
            action_name="click",
            target_index=200,
            evaluation="Success",
            dom_hash="hash1",
        )
        # Different hash breaks the sequence
        detector.check(
            action_name="click",
            target_index=300,
            evaluation="Success",
            dom_hash="hash2",
        )
        # Only 1 step with hash2 so far -- not enough for stagnant
        result = detector.check(
            action_name="click",
            target_index=400,
            evaluation="Success",
            dom_hash="hash2",
        )
        assert result.should_intervene is False

    def test_boundary_exactly_max_failures(self):
        """Exactly max_consecutive_failures consecutive failures should trigger."""
        detector = StallDetector(max_consecutive_failures=2)
        # Exactly 2 failures
        detector.check(
            action_name="click",
            target_index=6246,
            evaluation="fail",
            dom_hash="abc",
        )
        result = detector.check(
            action_name="click",
            target_index=6246,
            evaluation="fail",
            dom_hash="def",
        )
        assert result.should_intervene is True

    def test_stall_result_is_frozen(self):
        """StallResult should be immutable (frozen dataclass)."""
        result = StallResult(should_intervene=True, message="test message")
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.should_intervene = False  # type: ignore[misc]
