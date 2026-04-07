"""Unit tests for Phase 67: _detect_row_identity() and _failure_tracker.

Tests verify:
- ROW-01: _detect_row_identity extracts IMEI-format row identifiers from tr/td nodes
- ANTI-01: _failure_tracker state management with update/reset, independent of _PATCHED
"""

from unittest.mock import patch

import pytest

from backend.agent.dom_patch import (
    _detect_row_identity,
    _failure_tracker,
    apply_dom_patch,
    reset_failure_tracker,
    update_failure_tracker,
)


# ---------------------------------------------------------------------------
# Mock AccessibilityNode — mirrors EnhancedDOMTreeNode for _detect_row_identity
# ---------------------------------------------------------------------------


class MockAccessibilityNode:
    """Mock AccessibilityNode for _detect_row_identity tests."""

    def __init__(
        self,
        tag_name: str = "",
        children_text: str = "",
        parent=None,
        children=None,
    ):
        self.tag_name = tag_name
        self._children_text = children_text
        self.parent_node = parent
        self.children = children or []

    def get_all_children_text(self) -> str:
        return self._children_text


class MockSimplifiedNode:
    """Minimal mock for SimplifiedNode used in _detect_row_identity tests."""

    def __init__(self, original_node=None):
        self.original_node = original_node


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_tracker():
    """Reset _failure_tracker before each test to ensure isolation."""
    reset_failure_tracker()
    yield
    reset_failure_tracker()


# ---------------------------------------------------------------------------
# Tests: _detect_row_identity
# ---------------------------------------------------------------------------


class TestDetectRowIdentity:
    """Tests for _detect_row_identity function."""

    def test_extracts_imei_from_td_inside_tr(self):
        """Given a td node inside a tr with IMEI text, returns the IMEI string."""
        # Build: tr -> [td (IMEI text)]
        imei_td = MockAccessibilityNode(
            tag_name="td",
            children_text="I352017041234567",
        )
        tr_node = MockAccessibilityNode(
            tag_name="tr",
            children=[imei_td],
        )
        imei_td.parent_node = tr_node

        node = MockSimplifiedNode(original_node=imei_td)
        result = _detect_row_identity(node)

        assert result == "I352017041234567"

    def test_returns_none_for_non_imei_text(self):
        """Given a td node with plain text, returns None."""
        td = MockAccessibilityNode(
            tag_name="td",
            children_text="普通文本",
        )
        tr_node = MockAccessibilityNode(
            tag_name="tr",
            children=[td],
        )
        td.parent_node = tr_node

        node = MockSimplifiedNode(original_node=td)
        result = _detect_row_identity(node)

        assert result is None

    def test_returns_none_for_non_td_node(self):
        """Given a non-td node (e.g. span), returns None."""
        span = MockAccessibilityNode(
            tag_name="span",
            children_text="I352017041234567",
        )
        tr_node = MockAccessibilityNode(
            tag_name="tr",
            children=[span],
        )
        span.parent_node = tr_node

        node = MockSimplifiedNode(original_node=span)
        result = _detect_row_identity(node)

        assert result is None

    def test_returns_none_for_td_with_non_tr_parent(self):
        """Given a td node whose parent is not tr, returns None."""
        td = MockAccessibilityNode(
            tag_name="td",
            children_text="I352017041234567",
        )
        div_parent = MockAccessibilityNode(
            tag_name="div",
            children=[td],
        )
        td.parent_node = div_parent

        node = MockSimplifiedNode(original_node=td)
        result = _detect_row_identity(node)

        assert result is None

    def test_returns_none_for_none_original_node(self):
        """Given a node with original_node=None, returns None."""
        node = MockSimplifiedNode(original_node=None)
        result = _detect_row_identity(node)

        assert result is None

    def test_returns_none_for_none_parent_node(self):
        """Given a td node with no parent_node, returns None."""
        td = MockAccessibilityNode(
            tag_name="td",
            children_text="I352017041234567",
        )
        # parent_node defaults to None

        node = MockSimplifiedNode(original_node=td)
        result = _detect_row_identity(node)

        assert result is None

    def test_finds_imei_across_multiple_td_children(self):
        """Scans all td children of tr and finds IMEI in the second td."""
        td1 = MockAccessibilityNode(
            tag_name="td",
            children_text="iPhone 16 Pro Max",
        )
        td2 = MockAccessibilityNode(
            tag_name="td",
            children_text="I01784004409597",
        )
        tr_node = MockAccessibilityNode(
            tag_name="tr",
            children=[td1, td2],
        )
        td1.parent_node = tr_node
        td2.parent_node = tr_node

        # Pass any td in the row as entry point
        node = MockSimplifiedNode(original_node=td1)
        result = _detect_row_identity(node)

        assert result == "I01784004409597"

    def test_skips_non_td_children_in_tr(self):
        """Non-td children of tr are skipped during IMEI search."""
        th = MockAccessibilityNode(
            tag_name="th",
            children_text="I352017041234567",
        )
        td = MockAccessibilityNode(
            tag_name="td",
            children_text="regular value",
        )
        tr_node = MockAccessibilityNode(
            tag_name="tr",
            children=[th, td],
        )
        th.parent_node = tr_node
        td.parent_node = tr_node

        node = MockSimplifiedNode(original_node=td)
        result = _detect_row_identity(node)

        assert result is None

    def test_returns_first_imei_when_multiple_match(self):
        """Returns the first matched IMEI when multiple td cells contain IMEI."""
        td1 = MockAccessibilityNode(
            tag_name="td",
            children_text="I352017041234567",
        )
        td2 = MockAccessibilityNode(
            tag_name="td",
            children_text="I01784004409597",
        )
        tr_node = MockAccessibilityNode(
            tag_name="tr",
            children=[td1, td2],
        )
        td1.parent_node = tr_node
        td2.parent_node = tr_node

        node = MockSimplifiedNode(original_node=td1)
        result = _detect_row_identity(node)

        assert result == "I352017041234567"


# ---------------------------------------------------------------------------
# Tests: _failure_tracker state management
# ---------------------------------------------------------------------------


class TestFailureTracker:
    """Tests for update_failure_tracker and reset_failure_tracker."""

    def test_create_new_entry(self):
        """First call creates a new tracker entry with count=1."""
        update_failure_tracker("id1", "error message", "click_no_effect")

        import backend.agent.dom_patch as mod

        assert "id1" in mod._failure_tracker
        assert mod._failure_tracker["id1"]["count"] == 1
        assert mod._failure_tracker["id1"]["last_error"] == "error message"
        assert mod._failure_tracker["id1"]["mode"] == "click_no_effect"

    def test_accumulate_count_on_repeated_calls(self):
        """Three calls with the same id accumulate count to 3."""
        update_failure_tracker("id1", "error1", "click_no_effect")
        update_failure_tracker("id1", "error2", "wrong_column")
        update_failure_tracker("id1", "error3", "edit_not_active")

        import backend.agent.dom_patch as mod

        assert mod._failure_tracker["id1"]["count"] == 3
        assert mod._failure_tracker["id1"]["last_error"] == "error3"
        assert mod._failure_tracker["id1"]["mode"] == "edit_not_active"

    def test_independent_tracking_across_ids(self):
        """Different ids are tracked independently."""
        update_failure_tracker("id1", "err1", "mode1")
        update_failure_tracker("id2", "err2", "mode2")
        update_failure_tracker("id1", "err1b", "mode1b")

        import backend.agent.dom_patch as mod

        assert mod._failure_tracker["id1"]["count"] == 2
        assert mod._failure_tracker["id2"]["count"] == 1

    def test_reset_clears_all_entries(self):
        """reset_failure_tracker clears all tracker entries."""
        update_failure_tracker("id1", "err", "mode")
        update_failure_tracker("id2", "err", "mode")

        reset_failure_tracker()

        import backend.agent.dom_patch as mod

        assert len(mod._failure_tracker) == 0


# ---------------------------------------------------------------------------
# Tests: reset_failure_tracker independent of _PATCHED
# ---------------------------------------------------------------------------


class TestResetIndependentOfPatched:
    """Tests that reset_failure_tracker runs even when _PATCHED is True."""

    def test_reset_called_on_second_apply_dom_patch(self):
        """After apply_dom_patch sets _PATCHED, second call still resets tracker."""
        with patch("backend.agent.dom_patch._patch_is_interactive"), \
             patch("backend.agent.dom_patch._patch_paint_order_remover"), \
             patch("backend.agent.dom_patch._patch_should_exclude_child"), \
             patch("backend.agent.dom_patch._patch_assign_interactive_indices"):
            import backend.agent.dom_patch as mod

            mod._PATCHED = False

            # First call — applies patches, sets _PATCHED=True
            apply_dom_patch()

            # Add a tracker entry
            update_failure_tracker("test_id", "test error", "test_mode")
            assert len(mod._failure_tracker) == 1

            # Second call — _PATCHED is True, but should still reset tracker
            apply_dom_patch()

            assert len(mod._failure_tracker) == 0
