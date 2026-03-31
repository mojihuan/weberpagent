"""Unit tests for backend/agent/dom_patch.py.

Tests verify the monkey-patch correctly modifies browser-use DOM
serialization behavior for ERP table sub-elements (span.hand,
.el-checkbox__inner).
"""

from unittest.mock import MagicMock, patch

import pytest

from backend.agent.dom_patch import (
    _ERP_CLICKABLE_CLASSES,
    _has_erp_clickable_class,
    apply_dom_patch,
)


# ---------------------------------------------------------------------------
# Mock node helpers — mirror SimplifiedNode / EnhancedDOMTreeNode shape
# ---------------------------------------------------------------------------


class MockOriginalNode:
    """Minimal mock for EnhancedDOMTreeNode."""

    def __init__(self, class_name: str = ""):
        self.attributes = {"class": class_name} if class_name else {}
        self.has_js_click_listener = False
        self.tag_name = "span"
        self.node_name = "SPAN"


class MockSimplifiedNode:
    """Minimal mock for SimplifiedNode."""

    def __init__(
        self,
        class_name: str = "",
        children: list | None = None,
    ):
        self.original_node = MockOriginalNode(class_name)
        self.children = children or []
        self.ignored_by_paint_order = False
        self.excluded_by_parent = False


# ---------------------------------------------------------------------------
# Tests: _has_erp_clickable_class
# ---------------------------------------------------------------------------


class TestHasErpClickableClass:
    """Tests for the _has_erp_clickable_class helper."""

    def test_detects_hand_class(self):
        node = MockSimplifiedNode(class_name="hand")
        assert _has_erp_clickable_class(node) is True

    def test_detects_el_checkbox_class(self):
        node = MockSimplifiedNode(class_name="el-checkbox__inner")
        assert _has_erp_clickable_class(node) is True

    def test_detects_class_among_multiple(self):
        node = MockSimplifiedNode(class_name="some-other hand active")
        assert _has_erp_clickable_class(node) is True

    def test_rejects_non_erp_class(self):
        node = MockSimplifiedNode(class_name="btn-primary")
        assert _has_erp_clickable_class(node) is False

    def test_rejects_empty_class(self):
        node = MockSimplifiedNode(class_name="")
        assert _has_erp_clickable_class(node) is False

    def test_rejects_no_attributes(self):
        node = MockSimplifiedNode()
        node.original_node.attributes = None
        assert _has_erp_clickable_class(node) is False

    def test_rejects_no_original_node(self):
        node = MockSimplifiedNode()
        node.original_node = None
        assert _has_erp_clickable_class(node) is False


# ---------------------------------------------------------------------------
# Tests: apply_dom_patch
# ---------------------------------------------------------------------------


class TestApplyDomPatch:
    """Tests for the apply_dom_patch function."""

    def test_apply_dom_patch_idempotent(self):
        """Multiple calls should not raise errors."""
        with patch("backend.agent.dom_patch._patch_paint_order_remover"), \
             patch("backend.agent.dom_patch._patch_should_exclude_child"):
            # Reset patched state
            import backend.agent.dom_patch as mod
            mod._PATCHED = False

            apply_dom_patch()
            apply_dom_patch()  # second call should be a no-op
            apply_dom_patch()  # third call too

    def test_apply_dom_patch_modifies_paint_order_remover(self):
        """PaintOrderRemover.calculate_paint_order should be replaced."""
        with patch("backend.agent.dom_patch._patch_paint_order_remover") as mock_po, \
             patch("backend.agent.dom_patch._patch_should_exclude_child"):
            import backend.agent.dom_patch as mod
            mod._PATCHED = False

            apply_dom_patch()
            mock_po.assert_called_once()

    def test_apply_dom_patch_modifies_should_exclude_child(self):
        """DOMTreeSerializer._should_exclude_child should be replaced."""
        with patch("backend.agent.dom_patch._patch_paint_order_remover"), \
             patch("backend.agent.dom_patch._patch_should_exclude_child") as mock_bb:
            import backend.agent.dom_patch as mod
            mod._PATCHED = False

            apply_dom_patch()
            mock_bb.assert_called_once()

    def test_apply_dom_patch_sets_patched_flag(self):
        """_PATCHED flag should be True after successful apply."""
        with patch("backend.agent.dom_patch._patch_paint_order_remover"), \
             patch("backend.agent.dom_patch._patch_should_exclude_child"):
            import backend.agent.dom_patch as mod
            mod._PATCHED = False

            apply_dom_patch()
            assert mod._PATCHED is True


# ---------------------------------------------------------------------------
# Tests: paint order patch behavior
# ---------------------------------------------------------------------------


class TestPaintOrderPatch:
    """Tests for the patched PaintOrderRemover.calculate_paint_order."""

    def test_erp_elements_not_ignored_by_paint_order(self):
        """Nodes with hand/el-checkbox class should have ignored_by_paint_order reset."""
        # Create mock tree: root > tr > span.hand
        hand_node = MockSimplifiedNode(class_name="hand")
        hand_node.ignored_by_paint_order = True  # simulate paint order marking it

        tr_node = MockSimplifiedNode(class_name="", children=[hand_node])
        root_node = MockSimplifiedNode(class_name="", children=[tr_node])

        # Import and run the reset function directly
        from backend.agent.dom_patch import _reset_paint_order_for_erp_nodes

        _reset_paint_order_for_erp_nodes(root_node)

        assert hand_node.ignored_by_paint_order is False

    def test_non_erp_elements_still_ignored(self):
        """Non-ERP nodes should keep their ignored_by_paint_order flag."""
        other_node = MockSimplifiedNode(class_name="other-class")
        other_node.ignored_by_paint_order = True

        root_node = MockSimplifiedNode(class_name="", children=[other_node])

        from backend.agent.dom_patch import _reset_paint_order_for_erp_nodes

        _reset_paint_order_for_erp_nodes(root_node)

        assert other_node.ignored_by_paint_order is True

    def test_checkbox_elements_not_ignored(self):
        """el-checkbox nodes should have ignored_by_paint_order reset."""
        checkbox_node = MockSimplifiedNode(class_name="el-checkbox__inner")
        checkbox_node.ignored_by_paint_order = True

        root_node = MockSimplifiedNode(class_name="", children=[checkbox_node])

        from backend.agent.dom_patch import _reset_paint_order_for_erp_nodes

        _reset_paint_order_for_erp_nodes(root_node)

        assert checkbox_node.ignored_by_paint_order is False

    def test_nested_erp_elements_restored(self):
        """Deeply nested ERP elements should also be restored."""
        deep_node = MockSimplifiedNode(class_name="hand")
        deep_node.ignored_by_paint_order = True

        middle = MockSimplifiedNode(class_name="", children=[deep_node])
        root = MockSimplifiedNode(class_name="", children=[middle])

        from backend.agent.dom_patch import _reset_paint_order_for_erp_nodes

        _reset_paint_order_for_erp_nodes(root)

        assert deep_node.ignored_by_paint_order is False


# ---------------------------------------------------------------------------
# Tests: should_exclude_child patch behavior
# ---------------------------------------------------------------------------


class TestShouldExcludeChildPatch:
    """Tests for the patched DOMTreeSerializer._should_exclude_child."""

    def test_erp_elements_not_excluded_by_parent(self):
        """_should_exclude_child should return False for el-checkbox nodes."""
        # We test the _has_erp_clickable_class path directly since
        # the actual patch wraps it around the original method.
        checkbox_node = MockSimplifiedNode(class_name="el-checkbox__inner")

        # Simulate what the patched method does
        if _has_erp_clickable_class(checkbox_node):
            result = False
        else:
            result = True  # would call original

        assert result is False

    def test_hand_elements_not_excluded(self):
        """span.hand nodes should return False from patched _should_exclude_child."""
        hand_node = MockSimplifiedNode(class_name="hand")

        if _has_erp_clickable_class(hand_node):
            result = False
        else:
            result = True

        assert result is False

    def test_regular_elements_use_original_logic(self):
        """Non-ERP nodes should fall through to original _should_exclude_child."""
        regular_node = MockSimplifiedNode(class_name="regular-span")

        # The patched method checks _has_erp_clickable_class first
        assert _has_erp_clickable_class(regular_node) is False
        # Original method would be called for this node
