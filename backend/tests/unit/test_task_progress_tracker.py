"""Unit tests for TaskProgressTracker -- step progress tracking and budget warnings.

Covers MON-07 (step format parsing) and MON-08 (progress warning thresholds).
"""

from backend.agent.task_progress_tracker import ProgressResult, TaskProgressTracker


class TestTaskProgressTrackerParsing:
    """MON-07: Parse structured step list from task description."""

    def test_parse_step_n_format(self):
        """Parse 'Step N: ...' format into step descriptions."""
        tracker = TaskProgressTracker()
        tracker.parse_task("Step 1: Open page\nStep 2: Fill form\nStep 3: Submit")

        assert len(tracker._steps) == 3
        assert tracker._steps == ["Open page", "Fill form", "Submit"]

    def test_parse_chinese_format(self):
        """Parse Chinese numbered step format."""
        tracker = TaskProgressTracker()
        tracker.parse_task("第1步 打开页面\n第2步 填写表单")

        assert len(tracker._steps) == 2
        assert tracker._steps == ["打开页面", "填写表单"]

    def test_parse_checkbox_format(self):
        """Parse checkbox '- [ ] ...' format."""
        tracker = TaskProgressTracker()
        tracker.parse_task("- [ ] Open page\n- [ ] Fill form\n- [ ] Submit")

        assert len(tracker._steps) == 3
        assert tracker._steps == ["Open page", "Fill form", "Submit"]

    def test_parse_numbered_format(self):
        """Parse numbered '1. ...' format."""
        tracker = TaskProgressTracker()
        tracker.parse_task("1. Open page\n2. Fill form\n3. Submit")

        assert len(tracker._steps) == 3
        assert tracker._steps == ["Open page", "Fill form", "Submit"]

    def test_no_parseable_steps(self):
        """Unstructured task returns empty steps and no-warning result."""
        tracker = TaskProgressTracker()
        tracker.parse_task("Just do the thing")

        assert len(tracker._steps) == 0
        result = tracker.check_progress(current_step=5, max_steps=10)
        assert result.should_warn is False
        assert result.level == ""
        assert result.message == ""
        assert result.remaining_steps == 0
        assert result.remaining_tasks == 0


class TestTaskProgressTrackerProgress:
    """MON-08: Emit warning/urgent at correct thresholds."""

    @staticmethod
    def _make_tracker_with_steps(count: int) -> TaskProgressTracker:
        """Helper: create tracker with N numbered steps."""
        steps = "\n".join(f"Step {i + 1}: Task {i + 1}" for i in range(count))
        tracker = TaskProgressTracker()
        tracker.parse_task(steps)
        return tracker

    def test_urgent_when_remaining_steps_equal_tasks(self):
        """Remaining steps <= remaining tasks triggers 'urgent'."""
        tracker = self._make_tracker_with_steps(5)
        # 10 max, at step 8: remaining=2, remaining_tasks=5 -> 2 <= 5 -> urgent
        result = tracker.check_progress(current_step=8, max_steps=10)

        assert result.level == "urgent"
        assert result.should_warn is True
        assert result.remaining_steps == 2
        assert result.remaining_tasks == 5
        assert "紧迫" in result.message

    def test_warning_when_steps_tight(self):
        """Remaining steps < remaining_tasks * 1.5 triggers 'warning'."""
        tracker = self._make_tracker_with_steps(5)
        # 10 max, at step 4: remaining=6, remaining_tasks=5
        # 6 <= 5 is False, 6 < 7.5 is True -> warning
        result = tracker.check_progress(current_step=4, max_steps=10)

        assert result.level == "warning"
        assert result.should_warn is True
        assert result.remaining_steps == 6
        assert result.remaining_tasks == 5
        assert "预警" in result.message

    def test_no_warning_when_plenty_steps(self):
        """Plenty of remaining steps produces no warning."""
        tracker = self._make_tracker_with_steps(5)
        # 10 max, at step 2: remaining=8, remaining_tasks=5
        # 8 <= 5 is False, 8 < 7.5 is False -> no warning
        result = tracker.check_progress(current_step=2, max_steps=10)

        assert result.level == ""
        assert result.should_warn is False
        assert result.remaining_steps == 8
        assert result.remaining_tasks == 5

    def test_boundary_exactly_equal(self):
        """Boundary: remaining_steps == remaining_tasks triggers 'urgent'."""
        tracker = self._make_tracker_with_steps(5)
        # 10 max, at step 5: remaining=5, remaining_tasks=5 -> 5 <= 5 -> urgent
        result = tracker.check_progress(current_step=5, max_steps=10)

        assert result.level == "urgent"
        assert result.should_warn is True
        assert result.remaining_steps == 5
        assert result.remaining_tasks == 5

    def test_update_from_evaluation_marks_completed(self):
        """update_from_evaluation marks step as completed via keyword match."""
        tracker = TaskProgressTracker()
        tracker.parse_task("Step 1: Open page\nStep 2: Fill form")
        assert len(tracker._completed_steps) == 0

        tracker.update_from_evaluation("Successfully opened the page and loaded content")

        assert 0 in tracker._completed_steps
        assert 1 not in tracker._completed_steps
