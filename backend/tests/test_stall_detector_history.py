"""Tests for StallDetector _history cap at 1000 entries.

Tests MEM-04: StallDetector._history must be bounded to prevent unbounded memory
growth in long-running test sessions with many steps.
"""

import pytest

from backend.agent.stall_detector import StallDetector


class TestStallDetectorHistory:
    """Unit tests for StallDetector _history upper bound."""

    def test_history_capped_at_1000(self) -> None:
        """_history must not exceed 1000 entries — oldest entries truncated.

        After 1001 calls to check(), _history should contain exactly 1000 entries,
        with the oldest entry removed.
        """
        detector = StallDetector()

        for i in range(1001):
            detector.check(
                action_name="click",
                target_index=0,
                evaluation="ok",
                dom_hash=f"hash-{i}",
            )

        assert len(detector._history) == 1000, (
            f"_history should be capped at 1000, got {len(detector._history)}"
        )

    def test_history_cap_preserves_recent(self) -> None:
        """When _history is capped, the most recent entries must be preserved.

        The last entry in _history should be from the most recent call to check(),
        ensuring stall detection still works correctly on the latest data.
        """
        detector = StallDetector()

        for i in range(1001):
            detector.check(
                action_name="click",
                target_index=0,
                evaluation="ok",
                dom_hash=f"hash-{i}",
            )

        # The most recent entry (index 1000) should be preserved as the last item
        assert detector._history[-1].dom_hash == "hash-1000", (
            "Most recent entry must be preserved after cap truncation"
        )
