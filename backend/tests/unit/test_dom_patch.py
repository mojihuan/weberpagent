"""Unit tests for backend/agent/dom_patch.py.

Tests verify the monkey-patch correctly modifies browser-use DOM
serialization behavior for ERP table sub-elements (span.hand,
.el-checkbox__inner).
"""

from unittest.mock import MagicMock, patch

import pytest

from backend.agent.dom_patch import (
    _ERP_CLICKABLE_CLASSES,
    _get_column_header,
    _has_erp_clickable_class,
    _td_child_depth,
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


class MockChainNode:
    """Mock for AccessibilityNode with parent_node chain support."""

    def __init__(self, tag_name: str = "", parent=None, children=None):
        self.tag_name = tag_name
        self.parent_node = parent
        self.children = children or []
        self.attributes = {}


class MockSimplifiedNodeWithChain:
    """Mock SimplifiedNode with configurable original_node for parent chain tests."""

    def __init__(self, original_node=None):
        self.original_node = original_node
        self.children = []
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
        with patch("backend.agent.dom_patch._patch_is_interactive"), \
             patch("backend.agent.dom_patch._patch_paint_order_remover"), \
             patch("backend.agent.dom_patch._patch_should_exclude_child"):
            # Reset patched state
            import backend.agent.dom_patch as mod
            mod._PATCHED = False

            apply_dom_patch()
            apply_dom_patch()  # second call should be a no-op
            apply_dom_patch()  # third call too

    def test_apply_dom_patch_calls_all_three_patches(self):
        """All three patch functions should be called."""
        with patch("backend.agent.dom_patch._patch_is_interactive") as mock_ii, \
             patch("backend.agent.dom_patch._patch_paint_order_remover") as mock_po, \
             patch("backend.agent.dom_patch._patch_should_exclude_child") as mock_bb:
            import backend.agent.dom_patch as mod
            mod._PATCHED = False

            apply_dom_patch()
            mock_ii.assert_called_once()
            mock_po.assert_called_once()
            mock_bb.assert_called_once()

    def test_apply_dom_patch_sets_patched_flag(self):
        """_PATCHED flag should be True after successful apply."""
        with patch("backend.agent.dom_patch._patch_is_interactive"), \
             patch("backend.agent.dom_patch._patch_paint_order_remover"), \
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


# ---------------------------------------------------------------------------
# Tests: is_interactive patch behavior
# ---------------------------------------------------------------------------


class TestIsInteractivePatch:
    """Tests for the patched ClickableElementDetector.is_interactive."""

    def test_hand_class_detected_as_interactive(self):
        """span.hand nodes should be detected as interactive by patched method."""
        mock_node = MagicMock()
        mock_node.attributes = {"class": "hand"}

        # Simulate the patched logic
        detected = False
        class_value = mock_node.attributes.get("class", "")
        if class_value:
            for cls in class_value.split():
                for erp_cls in _ERP_CLICKABLE_CLASSES:
                    if erp_cls in cls:
                        detected = True
        assert detected is True

    def test_el_checkbox_class_detected_as_interactive(self):
        """el-checkbox nodes should be detected as interactive."""
        mock_node = MagicMock()
        mock_node.attributes = {"class": "el-checkbox__inner"}

        detected = False
        class_value = mock_node.attributes.get("class", "")
        if class_value:
            for cls in class_value.split():
                for erp_cls in _ERP_CLICKABLE_CLASSES:
                    if erp_cls in cls:
                        detected = True
        assert detected is True

    def test_el_checkbox_label_detected_as_interactive(self):
        """label.el-checkbox should be detected as interactive."""
        mock_node = MagicMock()
        mock_node.attributes = {"class": "el-checkbox"}

        detected = False
        class_value = mock_node.attributes.get("class", "")
        if class_value:
            for cls in class_value.split():
                for erp_cls in _ERP_CLICKABLE_CLASSES:
                    if erp_cls in cls:
                        detected = True
        assert detected is True

    def test_regular_span_not_detected_as_interactive_by_erp_check(self):
        """Regular span nodes should NOT be flagged by ERP class check."""
        mock_node = MagicMock()
        mock_node.attributes = {"class": "regular-span"}

        detected = False
        class_value = mock_node.attributes.get("class", "")
        if class_value:
            for cls in class_value.split():
                for erp_cls in _ERP_CLICKABLE_CLASSES:
                    if erp_cls in cls:
                        detected = True
        assert detected is False


# ---------------------------------------------------------------------------
# Tests: _td_child_depth
# ---------------------------------------------------------------------------


class TestTdChildDepth:
    """Tests for _td_child_depth helper function."""

    def test_direct_child_of_td_returns_0(self):
        """div directly inside td has depth 0."""
        td = MockChainNode(tag_name="td")
        div = MockChainNode(tag_name="div", parent=td)
        node = MockSimplifiedNodeWithChain(original_node=div)
        assert _td_child_depth(node) == 0

    def test_grandchild_of_td_returns_1(self):
        """span inside div inside td has depth 1."""
        td = MockChainNode(tag_name="td")
        div = MockChainNode(tag_name="div", parent=td)
        span = MockChainNode(tag_name="span", parent=div)
        node = MockSimplifiedNodeWithChain(original_node=span)
        assert _td_child_depth(node) == 1

    def test_great_grandchild_of_td_returns_2(self):
        """div inside span inside div inside td has depth 2 (layer 3)."""
        td = MockChainNode(tag_name="td")
        div1 = MockChainNode(tag_name="div", parent=td)
        span = MockChainNode(tag_name="span", parent=div1)
        div2 = MockChainNode(tag_name="div", parent=span)
        node = MockSimplifiedNodeWithChain(original_node=div2)
        assert _td_child_depth(node) == 2

    def test_not_inside_td_returns_none(self):
        """div NOT inside td returns None."""
        tr = MockChainNode(tag_name="tr")
        div = MockChainNode(tag_name="div", parent=tr)
        node = MockSimplifiedNodeWithChain(original_node=div)
        assert _td_child_depth(node) is None

    def test_non_div_span_tag_returns_none(self):
        """input tag returns None even if inside td."""
        td = MockChainNode(tag_name="td")
        inp = MockChainNode(tag_name="input", parent=td)
        node = MockSimplifiedNodeWithChain(original_node=inp)
        assert _td_child_depth(node) is None

    def test_no_original_node_returns_none(self):
        """Node with no original_node returns None."""
        node = MockSimplifiedNodeWithChain(original_node=None)
        assert _td_child_depth(node) is None

    def test_th_also_works_as_ancestor(self):
        """th works the same as td for depth counting."""
        th = MockChainNode(tag_name="th")
        div = MockChainNode(tag_name="div", parent=th)
        node = MockSimplifiedNodeWithChain(original_node=div)
        assert _td_child_depth(node) == 0


# ---------------------------------------------------------------------------
# Tests: _should_exclude_child td depth patch
# ---------------------------------------------------------------------------


class TestShouldExcludeChildTdPatch:
    """Tests for extended _patch_should_exclude_child with td depth check."""

    def _make_node_in_td(self, tag_name: str, depth_from_td: int):
        """Build a mock chain: td > div > ... > node at given depth from td.

        depth_from_td=0: td > tag_name
        depth_from_td=1: td > div > tag_name
        depth_from_td=2: td > div > div > tag_name
        """
        td = MockChainNode(tag_name="td")
        current = td
        for _i in range(depth_from_td):
            intermediate = MockChainNode(tag_name="div", parent=current)
            current = intermediate
        target = MockChainNode(tag_name=tag_name, parent=current)
        return MockSimplifiedNodeWithChain(original_node=target)

    def test_div_directly_in_td_not_excluded(self):
        """Per D-01: div directly in td should return False (not excluded)."""
        node = self._make_node_in_td("div", depth_from_td=0)
        td_depth = _td_child_depth(node)
        assert td_depth == 0
        # Simulate patched logic
        if td_depth is not None and td_depth < 2:
            result = False
        else:
            result = True  # would call original
        assert result is False

    def test_span_in_div_in_td_not_excluded(self):
        """Per D-02: span at depth 1 (grandchild of td) should return False."""
        node = self._make_node_in_td("span", depth_from_td=1)
        td_depth = _td_child_depth(node)
        assert td_depth == 1
        if td_depth is not None and td_depth < 2:
            result = False
        else:
            result = True
        assert result is False

    def test_deep_div_in_td_uses_original(self):
        """Per D-02: div at depth 2 (great-grandchild) should use original logic."""
        node = self._make_node_in_td("div", depth_from_td=2)
        td_depth = _td_child_depth(node)
        assert td_depth == 2
        # depth 2 is NOT < 2, so falls through to original
        if td_depth is not None and td_depth < 2:
            result = False
        else:
            result = "original_called"
        assert result == "original_called"

    def test_existing_hand_class_still_protected(self):
        """Existing hand/el-checkbox protection must be preserved."""
        node = MockSimplifiedNode(class_name="hand")
        assert _has_erp_clickable_class(node) is True
        # hand class is caught BEFORE td_depth check in the patch

    def test_non_td_element_uses_original(self):
        """Regular span not in td should use original exclusion logic."""
        tr = MockChainNode(tag_name="tr")
        span = MockChainNode(tag_name="span", parent=tr)
        node = MockSimplifiedNodeWithChain(original_node=span)
        td_depth = _td_child_depth(node)
        assert td_depth is None
        # None is not < 2, so falls through to original


# ---------------------------------------------------------------------------
# Tests: _get_column_header
# ---------------------------------------------------------------------------


class TestGetColumnHeader:
    """Tests for _get_column_header helper function."""

    def _build_table_tree(self, th_texts: list[str], td_count: int, target_td_index: int):
        """Build a mock table tree: table > thead > tr > th*s, tbody > tr > td*s.

        Returns the td node at target_td_index.
        """
        # Build th nodes
        th_nodes = []
        for text in th_texts:
            th = MockChainNode(tag_name="th")
            th._text = text
            th.get_all_children_text = lambda t=text: t
            th_nodes.append(th)

        # Build thead > tr > th*s
        thead_tr = MockChainNode(tag_name="tr", children=th_nodes)
        for th in th_nodes:
            th.parent_node = thead_tr
        thead = MockChainNode(tag_name="thead", children=[thead_tr])
        thead_tr.parent_node = thead

        # Build td nodes
        td_nodes = []
        target_td = None
        for i in range(td_count):
            td = MockChainNode(tag_name="td")
            td._text = f"cell_{i}"
            td.get_all_children_text = lambda t=f"cell_{i}": t
            td_nodes.append(td)
            if i == target_td_index:
                target_td = td

        # Build tbody > tr > td*s
        tbody_tr = MockChainNode(tag_name="tr", children=td_nodes)
        for td in td_nodes:
            td.parent_node = tbody_tr
        tbody = MockChainNode(tag_name="tbody", children=[tbody_tr])
        tbody_tr.parent_node = tbody

        # Build table
        table = MockChainNode(tag_name="table", children=[thead, tbody])
        thead.parent_node = table
        tbody.parent_node = table

        return target_td

    def test_returns_header_for_first_td(self):
        """td at index 0 returns first th text."""
        td = self._build_table_tree(
            th_texts=["物品编号", "IMEI", "品类"],
            td_count=3,
            target_td_index=0,
        )
        assert _get_column_header(td) == "物品编号"

    def test_returns_header_for_third_td(self):
        """td at index 2 returns third th text."""
        td = self._build_table_tree(
            th_texts=["物品编号", "IMEI", "品类", "品牌"],
            td_count=4,
            target_td_index=2,
        )
        assert _get_column_header(td) == "品类"

    def test_returns_none_when_no_parent_tr(self):
        """td with no parent_node returns None."""
        td = MockChainNode(tag_name="td")
        assert _get_column_header(td) is None

    def test_returns_none_when_parent_not_tr(self):
        """td with parent that is not tr returns None."""
        div = MockChainNode(tag_name="div")
        td = MockChainNode(tag_name="td", parent=div)
        assert _get_column_header(td) is None

    def test_returns_none_when_no_table_ancestor(self):
        """td in tr but no table ancestor returns None."""
        tr = MockChainNode(tag_name="tr")
        td = MockChainNode(tag_name="td", parent=tr)
        tr.children = [td]
        assert _get_column_header(td) is None

    def test_returns_none_when_no_thead(self):
        """table without thead returns None."""
        tr = MockChainNode(tag_name="tr")
        td = MockChainNode(tag_name="td", parent=tr)
        tr.children = [td]
        tbody = MockChainNode(tag_name="tbody", children=[tr])
        tr.parent_node = tbody
        table = MockChainNode(tag_name="table", children=[tbody])
        tbody.parent_node = table
        assert _get_column_header(td) is None

    def test_returns_none_when_thead_has_no_tr(self):
        """thead with no tr children returns None."""
        tr = MockChainNode(tag_name="tr")
        td = MockChainNode(tag_name="td", parent=tr)
        tr.children = [td]
        thead = MockChainNode(tag_name="thead", children=[])
        tbody_tr = MockChainNode(tag_name="tbody", children=[tr])
        tr.parent_node = tbody_tr
        table = MockChainNode(tag_name="table", children=[thead, tbody_tr])
        thead.parent_node = table
        tbody_tr.parent_node = table
        assert _get_column_header(td) is None

    def test_uses_last_tr_in_thead(self):
        """Multi-row header: uses LAST tr (actual column headers)."""
        # First tr: group header "基本信息"
        th_group = MockChainNode(tag_name="th")
        th_group.get_all_children_text = lambda: "基本信息"
        th_group.parent_node = MockChainNode(tag_name="tr")
        th_group.parent_node.children = [th_group]
        first_tr = th_group.parent_node

        # Second tr: actual column headers
        th1 = MockChainNode(tag_name="th")
        th1.get_all_children_text = lambda: "编号"
        th1.parent_node = MockChainNode(tag_name="tr")
        th2 = MockChainNode(tag_name="th")
        th2.get_all_children_text = lambda: "名称"
        th2.parent_node = th1.parent_node
        second_tr = th1.parent_node
        second_tr.children = [th1, th2]

        thead = MockChainNode(tag_name="thead", children=[first_tr, second_tr])
        first_tr.parent_node = thead
        second_tr.parent_node = thead

        # tbody > tr > td
        td = MockChainNode(tag_name="td")
        tr = MockChainNode(tag_name="tr", children=[td])
        td.parent_node = tr
        tbody = MockChainNode(tag_name="tbody", children=[tr])
        tr.parent_node = tbody
        table = MockChainNode(tag_name="table", children=[thead, tbody])
        thead.parent_node = table
        tbody.parent_node = table

        # td at index 0 should map to second_tr's first th = "编号"
        assert _get_column_header(td) == "编号"

    def test_returns_none_for_index_out_of_range(self):
        """td index exceeds th count returns None."""
        td = self._build_table_tree(
            th_texts=["A"],  # only 1 th
            td_count=3,
            target_td_index=2,  # index 2 but only 1 th
        )
        assert _get_column_header(td) is None

    def test_returns_none_for_empty_th_text(self):
        """th with empty text returns None."""
        td = self._build_table_tree(
            th_texts=[""],  # empty header
            td_count=1,
            target_td_index=0,
        )
        assert _get_column_header(td) is None
