"""Unit tests for Phase 68: _node_annotations sidecar dict and strategy logic.

Tests verify:
- ROW-03: _node_annotations populated with row_identity for ERP inputs
- STRAT-01: Strategy level 1 (visible input) and 2 (hidden input) assignment
- STRAT-03: Strategy level 3 (failure-based downgrade) when count >= 2
- Reset logic: _reset_node_annotations() clears sidecar dict
"""

from unittest.mock import MagicMock, patch

import pytest

from backend.agent.dom_patch import (
    _detect_row_identity,
    _failure_tracker,
    _node_annotations,
    apply_dom_patch,
    reset_failure_tracker,
    update_failure_tracker,
)


# ---------------------------------------------------------------------------
# Mock AccessibilityNode -- mirrors EnhancedDOMTreeNode
# ---------------------------------------------------------------------------


class MockAccessibilityNode:
    """Mock AccessibilityNode for Phase 68 tests.

    Mirrors EnhancedDOMTreeNode with additional fields: snapshot_node,
    is_visible, backend_node_id, attributes.
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
    """Minimal mock for SimplifiedNode used in Phase 68 tests."""

    def __init__(
        self,
        original_node=None,
        is_interactive: bool = False,
        is_new: bool = False,
    ):
        self.original_node = original_node
        self.is_interactive = is_interactive
        self.is_new = is_new


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_state():
    """Reset both _failure_tracker and _node_annotations before/after each test."""
    import backend.agent.dom_patch as mod

    reset_failure_tracker()
    mod._reset_node_annotations()
    yield
    reset_failure_tracker()
    mod._reset_node_annotations()


# ---------------------------------------------------------------------------
# Helper: Build an ERP table cell input node for testing
# ---------------------------------------------------------------------------


def _make_erp_input_node(
    backend_node_id: int = 100,
    snapshot_node: object | None = object(),  # Default: present (visible)
    placeholder: str = "销售金额",
    parent_tr_children: list | None = None,
) -> MockSimplifiedNode:
    """Create a MockSimplifiedNode representing an ERP table cell input.

    Args:
        backend_node_id: The backend_node_id for the input.
        snapshot_node: snapshot_node value (None = hidden, object = visible).
        placeholder: Input placeholder text.
        parent_tr_children: Children of the parent <tr> (for row identity).

    Returns:
        A MockSimplifiedNode with proper parent chain for ERP input detection.
    """
    # td node wrapping the input
    td_node = MockAccessibilityNode(
        tag_name="td",
        backend_node_id=backend_node_id - 1,
    )

    # tr parent
    tr_children = parent_tr_children or []
    td_node_in_tr = MockAccessibilityNode(
        tag_name="td",
        children_text="",
        backend_node_id=backend_node_id - 2,
    )
    tr_node = MockAccessibilityNode(
        tag_name="tr",
        children=[td_node_in_tr] + tr_children,
    )
    td_node.parent_node = tr_node

    # input node (the actual ERP input)
    input_node = MockAccessibilityNode(
        tag_name="input",
        backend_node_id=backend_node_id,
        snapshot_node=snapshot_node,
        attributes={"placeholder": placeholder},
        parent=td_node,
    )

    return MockSimplifiedNode(original_node=input_node)


def _make_imei_td(imei: str = "I352017041234567") -> MockAccessibilityNode:
    """Create a td node containing IMEI text for row identity detection."""
    return MockAccessibilityNode(
        tag_name="td",
        children_text=imei,
    )


def _call_patched_method(node, is_erp_input: bool = True):
    """Apply patch and call patched_method with the given node.

    Replaces the original DOMTreeSerializer method with a no-op so that
    only Phase 68 logic executes (no real serializer traversal).
    """
    import backend.agent.dom_patch as mod
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    # Step 1: Replace the serializer method with a no-op so
    # _patch_assign_interactive_indices captures a no-op as original_method.
    original = DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes
    DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = lambda self, node: None

    try:
        # Step 2: Mock _is_erp_table_cell_input to control ERP input detection
        with patch.object(mod, "_is_erp_table_cell_input", return_value=is_erp_input):
            mod._patch_assign_interactive_indices()

            # Step 3: Create a mock serializer and call the patched method
            serializer = MagicMock()
            serializer._selector_map = {}
            serializer._interactive_counter = 0

            patched = DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes
            patched(serializer, node)
    finally:
        # Restore original method to avoid side effects across tests
        DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = original


# ---------------------------------------------------------------------------
# Tests: Row belonging annotation
# ---------------------------------------------------------------------------


class TestRowBelongingAnnotation:
    """Tests for _node_annotations row identity and ERP input flag."""

    def test_erp_input_gets_row_identity_annotation(self):
        """Test 1: ERP input inside tr with IMEI gets row_identity in _node_annotations."""
        import backend.agent.dom_patch as mod

        imei_td = _make_imei_td("I352017041234567")
        node = _make_erp_input_node(
            backend_node_id=100,
            snapshot_node=object(),
            parent_tr_children=[imei_td],
        )

        _call_patched_method(node, is_erp_input=True)

        assert 100 in mod._node_annotations
        annotation = mod._node_annotations[100]
        assert annotation["row_identity"] == "I352017041234567"
        assert annotation["is_erp_input"] is True

    def test_non_erp_input_not_annotated(self):
        """Test 4: Non-ERP-input node gets no annotation."""
        import backend.agent.dom_patch as mod

        span_node = MockSimplifiedNode(
            original_node=MockAccessibilityNode(
                tag_name="span",
                backend_node_id=200,
            )
        )

        _call_patched_method(span_node, is_erp_input=False)

        assert 200 not in mod._node_annotations


# ---------------------------------------------------------------------------
# Tests: Strategy determination
# ---------------------------------------------------------------------------


class TestStrategyDetermination:
    """Tests for base_strategy assignment logic."""

    def test_strategy_1_for_visible_input(self):
        """Test 2: ERP input with snapshot_node gets base_strategy=1."""
        import backend.agent.dom_patch as mod

        imei_td = _make_imei_td("I352017041234567")
        node = _make_erp_input_node(
            backend_node_id=101,
            snapshot_node=object(),  # Present = visible
            parent_tr_children=[imei_td],
        )

        _call_patched_method(node, is_erp_input=True)

        assert 101 in mod._node_annotations
        assert mod._node_annotations[101]["base_strategy"] == 1

    def test_strategy_2_for_hidden_input(self):
        """Test 2b: ERP input with snapshot_node=None gets base_strategy=2."""
        import backend.agent.dom_patch as mod

        imei_td = _make_imei_td("I352017041234567")
        node = _make_erp_input_node(
            backend_node_id=102,
            snapshot_node=None,  # Hidden
            parent_tr_children=[imei_td],
        )

        _call_patched_method(node, is_erp_input=True)

        assert 102 in mod._node_annotations
        assert mod._node_annotations[102]["base_strategy"] == 2

    def test_strategy_3_when_failure_count_ge_2(self):
        """Test 3: ERP input with failure_count >= 2 gets base_strategy=3."""
        import backend.agent.dom_patch as mod

        # Seed failure tracker with count >= 2
        update_failure_tracker("103", "error1", "click_no_effect")
        update_failure_tracker("103", "error2", "click_no_effect")

        imei_td = _make_imei_td("I352017041234567")
        node = _make_erp_input_node(
            backend_node_id=103,
            snapshot_node=object(),  # Would normally be strategy 1
            parent_tr_children=[imei_td],
        )

        _call_patched_method(node, is_erp_input=True)

        assert 103 in mod._node_annotations
        assert mod._node_annotations[103]["base_strategy"] == 3

    def test_strategy_stays_at_visibility_level_when_count_1(self):
        """Test 7: Failure count=1 keeps visibility-based strategy."""
        import backend.agent.dom_patch as mod

        # Seed failure tracker with count=1 (below threshold)
        update_failure_tracker("104", "error1", "click_no_effect")

        imei_td = _make_imei_td("I352017041234567")
        node = _make_erp_input_node(
            backend_node_id=104,
            snapshot_node=object(),  # Would be strategy 1
            parent_tr_children=[imei_td],
        )

        _call_patched_method(node, is_erp_input=True)

        assert 104 in mod._node_annotations
        assert mod._node_annotations[104]["base_strategy"] == 1

    def test_strategy_3_when_failure_count_ge_4(self):
        """Test 8: Failure count >= 4 always results in strategy 3."""
        import backend.agent.dom_patch as mod

        # Seed failure tracker with count=4
        update_failure_tracker("105", "error1", "click_no_effect")
        update_failure_tracker("105", "error2", "click_no_effect")
        update_failure_tracker("105", "error3", "edit_not_active")
        update_failure_tracker("105", "error4", "click_no_effect")

        imei_td = _make_imei_td("I352017041234567")
        node = _make_erp_input_node(
            backend_node_id=105,
            snapshot_node=None,  # Would be strategy 2
            parent_tr_children=[imei_td],
        )

        _call_patched_method(node, is_erp_input=True)

        assert 105 in mod._node_annotations
        assert mod._node_annotations[105]["base_strategy"] == 3


# ---------------------------------------------------------------------------
# Tests: _reset_node_annotations
# ---------------------------------------------------------------------------


class TestResetNodeAnnotations:
    """Tests for _reset_node_annotations function."""

    def test_reset_clears_all_entries(self):
        """Test 5: _reset_node_annotations() clears all entries."""
        import backend.agent.dom_patch as mod

        # Manually populate annotations
        mod._node_annotations[100] = {
            "row_identity": "I123",
            "base_strategy": 1,
            "is_erp_input": True,
        }
        mod._node_annotations[200] = {
            "row_identity": None,
            "base_strategy": 2,
            "is_erp_input": True,
        }

        assert len(mod._node_annotations) == 2

        mod._reset_node_annotations()

        assert len(mod._node_annotations) == 0

    def test_reset_called_alongside_failure_tracker_in_apply(self):
        """Test 6: _reset_node_annotations() called in apply_dom_patch _PATCHED guard."""
        import backend.agent.dom_patch as mod

        with patch("backend.agent.dom_patch._patch_is_interactive"), \
             patch("backend.agent.dom_patch._patch_paint_order_remover"), \
             patch("backend.agent.dom_patch._patch_should_exclude_child"), \
             patch("backend.agent.dom_patch._patch_assign_interactive_indices"):
            mod._PATCHED = False

            # First call applies patches
            apply_dom_patch()

            # Populate both tracker and annotations
            update_failure_tracker("test_id", "test error", "test_mode")
            mod._node_annotations[300] = {
                "row_identity": "I999",
                "base_strategy": 1,
                "is_erp_input": True,
            }
            assert len(mod._failure_tracker) == 1
            assert len(mod._node_annotations) == 1

            # Second call: _PATCHED is True, should reset both
            apply_dom_patch()

            assert len(mod._failure_tracker) == 0
            assert len(mod._node_annotations) == 0
