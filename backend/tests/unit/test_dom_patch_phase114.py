"""Unit tests for Phase 114: DOM Patch input detection refactoring.

Tests verify:
- DOM-01: _is_erp_table_cell_input detects ANY visible input[type=text/number] inside td
- DOM-02: _has_visible_input_child + _is_textual_td_cell guard prevent td interactive when input child exists
- DOM-03: Column header annotation for input nodes inside td (not just td elements)
- DOM-04: Diagnostic logging of discovered placeholder values
"""

from unittest.mock import MagicMock, patch

import pytest

from backend.agent.dom_patch import (
    _is_erp_table_cell_input,
    _is_textual_td_cell,
)


# ---------------------------------------------------------------------------
# Mock classes -- mirrors EnhancedDOMTreeNode / SimplifiedNode
# ---------------------------------------------------------------------------


class MockAccessibilityNode:
    """Mock AccessibilityNode for Phase 114 tests.

    Mirrors EnhancedDOMTreeNode with tag_name, attributes, snapshot_node,
    parent_node, children, backend_node_id, is_visible.
    """

    def __init__(
        self,
        tag_name: str = "",
        children_text: str = "",
        parent=None,
        children=None,
        backend_node_id: int = 0,
        snapshot_node: object = None,
        is_visible: bool = True,
        attributes: dict | None = None,
    ):
        self.tag_name = tag_name
        self._children_text = children_text
        self.parent_node = parent
        self.children = children or []
        self.backend_node_id = backend_node_id
        self.snapshot_node = snapshot_node
        self.is_visible = is_visible
        self.attributes = attributes or {}

    def get_all_children_text(self) -> str:
        return self._children_text


class MockSimplifiedNode:
    """Minimal mock for SimplifiedNode used in Phase 114 tests."""

    def __init__(
        self,
        original_node=None,
        is_interactive: bool = False,
        is_new: bool = False,
        children=None,
    ):
        self.original_node = original_node
        self.is_interactive = is_interactive
        self.is_new = is_new
        self.children = children or []


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_state():
    """Reset module-level state before/after each test."""
    import backend.agent.dom_patch as mod

    mod.reset_failure_tracker()
    mod._reset_node_annotations()
    yield
    mod.reset_failure_tracker()
    mod._reset_node_annotations()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_input_in_td(
    input_type: str = "text",
    placeholder: str = "请输入",
    snapshot_node: object = object(),
    backend_node_id: int = 100,
) -> MockSimplifiedNode:
    """Create a MockSimplifiedNode representing an input inside a td cell.

    Returns a SimplifiedNode whose original_node is an input with the given
    attributes, wrapped inside a td -> tr parent chain.
    """
    td_node = MockAccessibilityNode(
        tag_name="td",
        backend_node_id=backend_node_id - 1,
    )
    tr_node = MockAccessibilityNode(
        tag_name="tr",
        children=[td_node],
    )
    td_node.parent_node = tr_node

    input_node = MockAccessibilityNode(
        tag_name="input",
        backend_node_id=backend_node_id,
        snapshot_node=snapshot_node,
        attributes={"type": input_type, "placeholder": placeholder},
        parent=td_node,
    )

    return MockSimplifiedNode(original_node=input_node)


def _make_input_outside_td(
    input_type: str = "text",
    placeholder: str = "请输入",
    snapshot_node: object = object(),
    backend_node_id: int = 200,
) -> MockSimplifiedNode:
    """Create a MockSimplifiedNode representing an input NOT inside a td cell."""
    div_node = MockAccessibilityNode(
        tag_name="div",
        backend_node_id=backend_node_id - 1,
    )
    input_node = MockAccessibilityNode(
        tag_name="input",
        backend_node_id=backend_node_id,
        snapshot_node=snapshot_node,
        attributes={"type": input_type, "placeholder": placeholder},
        parent=div_node,
    )
    return MockSimplifiedNode(original_node=input_node)


# ---------------------------------------------------------------------------
# Tests: DOM-01 — _is_erp_table_cell_input refactored detection
# ---------------------------------------------------------------------------


class TestIsErpTableCellInput:
    """Tests for DOM-01: structural detection of inputs inside td cells."""

    def test_visible_text_input(self):
        """input inside td with type=text, snapshot_node present, arbitrary placeholder returns True."""
        node = _make_input_in_td(
            input_type="text",
            placeholder="请输入",
            snapshot_node=object(),
        )
        assert _is_erp_table_cell_input(node) is True

    def test_visible_number_input(self):
        """input inside td with type=number, snapshot_node present returns True."""
        node = _make_input_in_td(
            input_type="number",
            placeholder="数量",
            snapshot_node=object(),
        )
        assert _is_erp_table_cell_input(node) is True

    def test_hidden_input_no_snapshot(self):
        """input inside td without snapshot_node returns False."""
        node = _make_input_in_td(
            input_type="text",
            placeholder="请输入",
            snapshot_node=None,
        )
        assert _is_erp_table_cell_input(node) is False

    def test_input_outside_td(self):
        """input NOT inside td returns False."""
        node = _make_input_outside_td(
            input_type="text",
            placeholder="请输入",
            snapshot_node=object(),
        )
        assert _is_erp_table_cell_input(node) is False

    def test_input_type_checkbox(self):
        """input inside td with type=checkbox returns False."""
        node = _make_input_in_td(
            input_type="checkbox",
            placeholder="",
            snapshot_node=object(),
        )
        assert _is_erp_table_cell_input(node) is False

    def test_input_no_type_attribute(self):
        """input inside td with no type attribute (defaults to text) and snapshot_node returns True."""
        # Build mock manually with no type in attributes
        td_node = MockAccessibilityNode(tag_name="td", backend_node_id=98)
        tr_node = MockAccessibilityNode(tag_name="tr", children=[td_node])
        td_node.parent_node = tr_node
        input_node = MockAccessibilityNode(
            tag_name="input",
            backend_node_id=99,
            snapshot_node=object(),
            attributes={},  # no type key -> defaults to text
            parent=td_node,
        )
        node = MockSimplifiedNode(original_node=input_node)
        assert _is_erp_table_cell_input(node) is True


# ---------------------------------------------------------------------------
# Tests: DOM-02 — _has_visible_input_child helper
# ---------------------------------------------------------------------------


class TestHasVisibleInputChild:
    """Tests for DOM-02: _has_visible_input_child helper function."""

    @pytest.fixture(autouse=True)
    def _import_helper(self):
        """Import _has_visible_input_child (exists after Task 1 GREEN)."""
        try:
            from backend.agent.dom_patch import _has_visible_input_child
            self._has_visible_input_child = _has_visible_input_child
        except ImportError:
            pytest.skip("_has_visible_input_child not yet implemented")

    def test_td_with_visible_input(self):
        """td original with child input (type=text, snapshot_node present) returns True."""
        child_input = MockAccessibilityNode(
            tag_name="input",
            attributes={"type": "text"},
            snapshot_node=object(),
        )
        td_original = MockAccessibilityNode(
            tag_name="td",
            children=[child_input],
        )
        assert self._has_visible_input_child(td_original) is True

    def test_td_without_input(self):
        """td original with no input children returns False."""
        td_original = MockAccessibilityNode(
            tag_name="td",
            children=[MockAccessibilityNode(tag_name="span")],
        )
        assert self._has_visible_input_child(td_original) is False

    def test_td_with_hidden_input(self):
        """td original with child input but no snapshot_node returns False."""
        child_input = MockAccessibilityNode(
            tag_name="input",
            attributes={"type": "text"},
            snapshot_node=None,
        )
        td_original = MockAccessibilityNode(
            tag_name="td",
            children=[child_input],
        )
        assert self._has_visible_input_child(td_original) is False


# ---------------------------------------------------------------------------
# Tests: DOM-02 — _is_textual_td_cell guard
# ---------------------------------------------------------------------------


class TestIsTextualTdCell:
    """Tests for DOM-02: _is_textual_td_cell returns False when td has visible input child."""

    def test_td_with_visible_input_not_textual(self):
        """td that has text AND visible input child returns False from _is_textual_td_cell."""
        # Build: td with text "0.00" and a visible input child
        child_input = MockAccessibilityNode(
            tag_name="input",
            attributes={"type": "text"},
            snapshot_node=object(),
        )
        td_original = MockAccessibilityNode(
            tag_name="td",
            children_text="0.00",
            children=[child_input],
        )
        tr_original = MockAccessibilityNode(
            tag_name="tr",
            children=[td_original],
        )
        td_original.parent_node = tr_original

        node = MockSimplifiedNode(original_node=td_original)
        assert _is_textual_td_cell(node) is False

    def test_td_without_input_still_textual(self):
        """td that has text but NO visible input child still returns True."""
        td_original = MockAccessibilityNode(
            tag_name="td",
            children_text="0.00",
            children=[],
        )
        tr_original = MockAccessibilityNode(
            tag_name="tr",
            children=[td_original],
        )
        td_original.parent_node = tr_original

        node = MockSimplifiedNode(original_node=td_original)
        assert _is_textual_td_cell(node) is True


# ---------------------------------------------------------------------------
# Tests: DOM-03 — Column header annotation for input nodes inside td
# ---------------------------------------------------------------------------


class TestColumnHeaderForInput:
    """Tests for DOM-03: input nodes inside td get column header annotation."""

    def _make_table_with_input(self, th_texts, td_index, input_backend_id=600):
        """Build a mock input SimplifiedNode inside a td inside a table with thead."""
        # Build th nodes
        th_nodes = []
        for text in th_texts:
            th = MockAccessibilityNode(
                tag_name="th",
                children_text=text,
            )
            th_nodes.append(th)

        # Build thead > tr
        thead_tr = MockAccessibilityNode(tag_name="tr", children=th_nodes)
        thead = MockAccessibilityNode(tag_name="thead", children=[thead_tr])

        # Build td nodes with one containing an input
        td_nodes = []
        target_td = None
        for i in range(len(th_texts)):
            if i == td_index:
                input_node = MockAccessibilityNode(
                    tag_name="input",
                    backend_node_id=input_backend_id,
                    snapshot_node=object(),
                    attributes={"type": "text", "placeholder": "请输入"},
                )
                td = MockAccessibilityNode(
                    tag_name="td",
                    children=[input_node],
                    backend_node_id=input_backend_id + i + 1,
                )
                input_node.parent_node = td
                target_td = td
            else:
                td = MockAccessibilityNode(
                    tag_name="td",
                    backend_node_id=input_backend_id + i + 10,
                )
            td_nodes.append(td)

        # Build tbody > tr > table
        tbody_tr = MockAccessibilityNode(tag_name="tr", children=td_nodes)
        tbody = MockAccessibilityNode(tag_name="tbody", children=[tbody_tr])
        table = MockAccessibilityNode(tag_name="table", children=[thead, tbody])

        # Set parent chains
        for th in th_nodes:
            th.parent_node = thead_tr
        thead_tr.parent_node = thead
        for td in td_nodes:
            td.parent_node = tbody_tr
        tbody_tr.parent_node = tbody
        thead.parent_node = table
        tbody.parent_node = table

        # Return the input SimplifiedNode
        input_simplified = MockSimplifiedNode(original_node=input_node)
        return input_simplified

    def _apply_serialize_patch_and_call(self, node, include_attributes=None):
        """Apply serialize patch and call it with the given node."""
        import backend.agent.dom_patch as mod
        from browser_use.dom.serializer.serializer import DOMTreeSerializer

        original_serialize = DOMTreeSerializer.serialize_tree
        DOMTreeSerializer.serialize_tree = staticmethod(
            lambda n, attrs, depth=0: "<mock>output</mock>"
        )

        try:
            mod._patch_serialize_tree_annotations()
            result = DOMTreeSerializer.serialize_tree(node, include_attributes or [])
            return result
        finally:
            DOMTreeSerializer.serialize_tree = original_serialize

    def test_input_inside_td_gets_column_header(self):
        """input inside td gets column header comment annotation in serialized output."""
        input_node = self._make_table_with_input(
            th_texts=["物品编号", "销售金额", "利润"],
            td_index=1,
            input_backend_id=600,
        )
        result = self._apply_serialize_patch_and_call(input_node)
        assert "<!-- 列: 销售金额 -->" in result

    def test_input_outside_td_no_annotation(self):
        """input NOT inside td gets no column header annotation."""
        input_outside = _make_input_outside_td(
            snapshot_node=object(),
            backend_node_id=700,
        )
        result = self._apply_serialize_patch_and_call(input_outside)
        assert "<!-- 列:" not in result


# ---------------------------------------------------------------------------
# Tests: DOM-04 — Diagnostic logging
# ---------------------------------------------------------------------------


class TestDiagnosticLog:
    """Tests for DOM-04: placeholder values logged when ERP table cell inputs detected."""

    def test_placeholder_values_logged(self):
        """When ERP table cell inputs are detected, their placeholder values are logged via logger.info."""
        import backend.agent.dom_patch as mod
        from backend.agent.dom_patch import _patch_assign_interactive_indices
        from browser_use.dom.serializer.serializer import DOMTreeSerializer

        # Save original
        original_method = DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes

        # Build two input nodes inside td
        node1 = _make_input_in_td(
            input_type="text",
            placeholder="请输入数量",
            snapshot_node=object(),
            backend_node_id=300,
        )
        node2 = _make_input_in_td(
            input_type="text",
            placeholder="请输入金额",
            snapshot_node=object(),
            backend_node_id=400,
        )

        try:
            # Mock original method to be a no-op
            DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = (
                lambda self, node: None
            )

            # Apply patch
            _patch_assign_interactive_indices()

            # Call patched method for each node
            serializer = MagicMock()
            serializer._selector_map = {}
            serializer._interactive_counter = 0

            patched = DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes
            patched(serializer, node1)
            patched(serializer, node2)

            # Verify logging happened
            with patch.object(mod.logger, "info") as mock_info:
                # Re-invoke to capture log emission (the flag-based logic)
                # The flag is already set from the first call, so we need to reset
                mod._diagnostic_log_emitted = False
                mod._discovered_placeholders = ["请输入数量", "请输入金额"]

                # Trigger the log by calling patched_method again (it will check flag)
                node3 = _make_input_in_td(
                    input_type="text",
                    placeholder="请输入备注",
                    snapshot_node=object(),
                    backend_node_id=500,
                )
                patched(serializer, node3)

                # Check that logger.info was called with placeholder info
                mock_info.assert_called()
                logged_args = str(mock_info.call_args)
                assert "请输入数量" in logged_args or "请输入备注" in logged_args

        finally:
            DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = original_method
