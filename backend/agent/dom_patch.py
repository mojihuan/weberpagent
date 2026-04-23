"""Monkey-patch for browser-use DOM serializer.

Patches PaintOrderRemover and DOMTreeSerializer to prevent ERP table
sub-elements (span.hand, .el-checkbox__inner) from being absorbed by
parent <tr> nodes during DOM serialization. Without this patch, these
elements lose their independent clickable index and the Agent cannot
use standard click(index=N) to interact with them.
"""

import logging
import re

logger = logging.getLogger(__name__)

_PATCHED = False

# CSS class substrings that identify ERP clickable sub-elements
_ERP_CLICKABLE_CLASSES = frozenset({"hand", "el-checkbox"})

# Tags inside <td> that should be protected from bbox flattening
_TD_CHILD_TAGS = frozenset({"div", "span"})

# Maximum depth from td to protect (depth 0 = direct child, depth 1 = grandchild)
_MAX_TD_CHILD_DEPTH = 2

# Placeholder substrings identifying ERP table cell input fields
# These inputs are inside <td> cells and may lack snapshot_node in AX tree
_ERP_TABLE_CELL_PLACEHOLDERS = frozenset({
    "销售金额",
    "物流费用",
    "备注",
    "单号",
    "数量",
})

# Numeric patterns for ERP table cell values that are editable (click-to-edit)
# These are displayed as text in <td> cells until clicked to enter edit mode
# Kept for reference; actual detection uses get_all_children_text() instead
_ERP_NUMERIC_CELL_PATTERNS = (
    r"^-?\d+(\.\d{1,2})?$",  # e.g. 0.00, 210, -210.00, 150.5
)

# IMEI / product number format: I + 15 digits
_ROW_IDENTITY_PATTERN = re.compile(r"I\d{15}")

# Failure tracking state: keyed by backend_node_id (str)
_failure_tracker: dict[str, dict] = {}

# Node annotations sidecar: keyed by backend_node_id (int)
# Populated by Patch 4 for ERP table cell inputs.
# Value: {"row_identity": str | None, "base_strategy": int, "is_erp_input": bool}
_node_annotations: dict[int, dict] = {}


def _is_textual_td_cell(node) -> bool:
    """Check if a SimplifiedNode is a <td> with meaningful text content.

    ERP Ant Design tables use click-to-edit cells: <td> shows a text value
    (e.g. "0.00", "210", "iPhone 16 Pro Max") and clicking it reveals an <input>.
    These <td> cells are currently NOT shown in the DOM dump (empty <td />) because
    they have should_display=False, which causes their children to be "flattened"
    and shown as bare text nodes at the <tr> level — making it impossible for the
    Agent to identify which column is which.

    By marking these cells as interactive, they appear in the dump with proper
    nesting: <td> [index]<td>...</td></td> with their text content indented inside.

    Returns True if the node is a <td> inside a <tr> that has meaningful text
    content (from its children).

    Args:
        node: A SimplifiedNode instance.

    Returns:
        True if the node is a <td> with text content.
    """
    original = getattr(node, "original_node", None)
    if original is None:
        return False

    tag_name = getattr(original, "tag_name", None)
    if not tag_name or tag_name.lower() != "td":
        return False

    # Must be inside a <tr>
    parent = getattr(original, "parent_node", None)
    if parent is None:
        return False
    parent_tag = getattr(parent, "tag_name", None)
    if not parent_tag or parent_tag.lower() != "tr":
        return False

    # Check if the cell has meaningful text content (from nested <span>/<div> children)
    # get_all_children_text() recursively collects all TEXT_NODE values from descendants
    text = original.get_all_children_text()
    if text and text.strip():
        return True

    return False


def _detect_row_identity(node) -> str | None:
    """Detect row identity (IMEI / product number) from an ERP table row.

    Walks the parent chain from node to find the nearest <tr>, then
    traverses all <td> children of that <tr>, applies the ``I\\d{15}``
    regex to each td's text, and returns the first match.

    Args:
        node: A SimplifiedNode instance.

    Returns:
        The matched IMEI string, or ``None``.
    """
    original = getattr(node, "original_node", None)
    if original is None:
        return None

    # Walk parent chain to find the nearest <tr>
    current = getattr(original, "parent_node", None)
    tr_node = None
    while current is not None:
        tag = getattr(current, "tag_name", None)
        if tag and tag.lower() == "tr":
            tr_node = current
            break
        current = getattr(current, "parent_node", None)

    if tr_node is None:
        return None

    tr_children = getattr(tr_node, "children", [])
    for child in tr_children:
        child_tag = getattr(child, "tag_name", "")
        if child_tag.lower() != "td":
            continue
        text = child.get_all_children_text()
        if not text:
            continue
        match = _ROW_IDENTITY_PATTERN.search(text)
        if match:
            return match.group()

    return None


def _detect_row_identity_from_tr(tr_original) -> str | None:
    """Extract IMEI row identity directly from a <tr> AccessibilityNode's td children.

    Unlike _detect_row_identity which walks the parent chain to find a <tr>,
    this function assumes the passed node IS the <tr> and scans its children.

    Args:
        tr_original: An AccessibilityNode with tag_name='tr'.

    Returns:
        The matched IMEI string, or None.
    """
    tr_children = getattr(tr_original, "children", [])
    for child in tr_children:
        child_tag = getattr(child, "tag_name", "")
        if child_tag.lower() != "td":
            continue
        text = child.get_all_children_text()
        if not text:
            continue
        match = _ROW_IDENTITY_PATTERN.search(text)
        if match:
            return match.group()

    return None


def update_failure_tracker(backend_node_id: str, error: str, mode: str) -> None:
    """Update failure tracking record.

    Args:
        backend_node_id: Target element's backend_node_id.
        error: Failure description.
        mode: Failure mode (click_no_effect / wrong_column / edit_not_active).
    """
    global _failure_tracker
    if backend_node_id in _failure_tracker:
        _failure_tracker[backend_node_id]["count"] += 1
        _failure_tracker[backend_node_id]["last_error"] = error
        _failure_tracker[backend_node_id]["mode"] = mode
    else:
        _failure_tracker[backend_node_id] = {
            "count": 1,
            "last_error": error,
            "mode": mode,
        }


def reset_failure_tracker() -> None:
    """Clear all failure tracking state. Called at the start of every run."""
    global _failure_tracker
    _failure_tracker = {}


def _reset_node_annotations() -> None:
    """Clear all node annotations. Called alongside reset_failure_tracker()."""
    global _node_annotations
    _node_annotations = {}


def _has_erp_clickable_class(node) -> bool:
    """Check if a SimplifiedNode has an ERP-specific clickable CSS class.

    Args:
        node: A SimplifiedNode instance with original_node attribute.

    Returns:
        True if the node's class attribute contains 'hand' or 'el-checkbox'.
    """
    original = getattr(node, "original_node", None)
    if original is None:
        return False

    attributes = getattr(original, "attributes", None)
    if not attributes:
        return False

    class_value = attributes.get("class", "")
    if not class_value:
        return False

    class_parts = class_value.split()
    for cls in class_parts:
        for erp_cls in _ERP_CLICKABLE_CLASSES:
            if erp_cls in cls:
                return True

    return False


def _is_inside_table_cell(node) -> bool:
    """Check if a SimplifiedNode is inside a table cell (<td> or <th>).

    Walks the original_node's parent chain looking for td/th tags.
    Uses original_node.parent_node (AccessibilityNode) not SimplifiedNode.parent.

    Args:
        node: A SimplifiedNode instance.

    Returns:
        True if the node is a descendant of <td> or <th>.
    """
    current = getattr(node.original_node, "parent_node", None)
    while current is not None:
        tag_name = getattr(current, "tag_name", None)
        if tag_name and tag_name.lower() in ("td", "th"):
            return True
        current = getattr(current, "parent_node", None)
    return False


def _td_child_depth(node) -> int | None:
    """Count parent_node chain distance from node to its nearest td/th ancestor.

    Returns the number of parent_node steps from node up to the nearest <td> or <th>.
    Returns None if the node is not inside a td/th, or if the node's tag is not div/span.

    Depth semantics (per D-02):
        depth=0: node is a direct child of td (layer 1)
        depth=1: node is a grandchild of td (layer 2)
        depth=2+: beyond the 2-layer protection limit

    Args:
        node: A SimplifiedNode instance.

    Returns:
        Number of steps to nearest td/th, or None.
    """
    original = getattr(node, "original_node", None)
    if original is None:
        return None

    tag_name = getattr(original, "tag_name", "")
    if tag_name.lower() not in _TD_CHILD_TAGS:
        return None

    depth = 0
    current = getattr(original, "parent_node", None)
    while current is not None:
        current_tag = getattr(current, "tag_name", "")
        if current_tag.lower() in ("td", "th"):
            return depth
        depth += 1
        current = getattr(current, "parent_node", None)
    return None


def _is_erp_table_cell_input(node) -> bool:
    """Check if a SimplifiedNode is an ERP table cell input with relevant placeholder.

    Conditions: (1) inside <td>/<th>, (2) input tag, (3) has placeholder matching ERP fields.

    Args:
        node: A SimplifiedNode instance.

    Returns:
        True if the node is an ERP table cell input.
    """
    if not _is_inside_table_cell(node):
        return False

    original = getattr(node, "original_node", None)
    if original is None:
        return False

    tag_name = getattr(original, "tag_name", None)
    if not tag_name or tag_name.lower() != "input":
        return False

    attributes = getattr(original, "attributes", None)
    if not attributes:
        return False

    placeholder = attributes.get("placeholder", "")
    for erp_placeholder in _ERP_TABLE_CELL_PLACEHOLDERS:
        if erp_placeholder in placeholder:
            return True
    return False


def _reset_paint_order_for_erp_nodes(node) -> None:
    """Recursively reset ignored_by_paint_order for ERP clickable nodes.

    Args:
        node: Root SimplifiedNode to traverse.
    """
    if _has_erp_clickable_class(node) and node.ignored_by_paint_order:
        node.ignored_by_paint_order = False
        logger.debug("dom_patch: restored paint order for node with class=%s",
                      node.original_node.attributes.get("class", ""))

    for child in node.children:
        _reset_paint_order_for_erp_nodes(child)


def _patch_is_interactive() -> None:
    """Patch ClickableElementDetector.is_interactive.

    Returns True for nodes with ERP clickable CSS classes AND for <td> cells
    with text content (click-to-edit entry points), ensuring they get assigned
    interactive indices during DOM serialization. Without this, those elements
    are skipped because they lack form controls, event handler attributes, ARIA
    roles, or interactive tag names.
    """
    from browser_use.dom.serializer.clickable_elements import ClickableElementDetector

    original_is_interactive = ClickableElementDetector.is_interactive

    def patched_is_interactive(node) -> bool:
        attributes = getattr(node, "attributes", None)
        if attributes:
            class_value = attributes.get("class", "")
            if class_value:
                for cls in class_value.split():
                    for erp_cls in _ERP_CLICKABLE_CLASSES:
                        if erp_cls in cls:
                            return True
        # Mark <td> cells with text content as interactive (click-to-edit entry point)
        if _is_textual_td_cell(node):
            return True
        return original_is_interactive(node)

    ClickableElementDetector.is_interactive = patched_is_interactive
    logger.debug("dom_patch: patched ClickableElementDetector.is_interactive")


def apply_dom_patch() -> None:
    """Apply monkey-patches to browser-use DOM serializer.

    Patches 6 mechanisms:
    1. ClickableElementDetector.is_interactive - marks ERP elements (ERP CSS
       classes and <td> cells with text) as interactive so they receive
       clickable indices.
    2. PaintOrderRemover.calculate_paint_order - resets ignored_by_paint_order
       for ERP nodes after the original method runs.
    3. DOMTreeSerializer._should_exclude_child - returns False for ERP nodes
       and div/span inside td (up to 2 layers) so they are never excluded
       by bounding box filtering.
    4. DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes -
       forces interactive assignment for ERP table cell inputs.
    5. ClickableElementDetector.is_interactive (extended) - marks <td> cells
       with text content as interactive so they appear with proper nesting
       in DOM dump (fixes click-to-edit cell visibility).
    6. DOMTreeSerializer.serialize_tree - inject row identity comments (Patch 6)
       and failure/strategy annotations (Patch 7) into DOM dump output.

    Idempotent: multiple calls are safe and only patch once.
    """
    global _PATCHED
    if _PATCHED:
        reset_failure_tracker()  # reset tracker every run, independent of _PATCHED
        _reset_node_annotations()  # clear annotations alongside tracker
        logger.debug("dom_patch: already applied, skipping")
        return

    try:
        _patch_is_interactive()
        _patch_paint_order_remover()
        _patch_should_exclude_child()
        _patch_assign_interactive_indices()
        _patch_serialize_tree_annotations()
        _PATCHED = True
        logger.info("dom_patch: successfully applied all patches (including Phase 68)")
    except Exception as exc:
        logger.error("dom_patch: failed to apply: %s", exc)
        raise


def _patch_paint_order_remover() -> None:
    """Patch PaintOrderRemover.calculate_paint_order.

    After the original method sets ignored_by_paint_order flags, this
    patch traverses the tree and resets the flag for any node with an
    ERP clickable CSS class.
    """
    from browser_use.dom.serializer.paint_order import PaintOrderRemover

    original_calculate = PaintOrderRemover.calculate_paint_order

    def patched_calculate_paint_order(self) -> None:
        original_calculate(self)
        _reset_paint_order_for_erp_nodes(self.root)

    PaintOrderRemover.calculate_paint_order = patched_calculate_paint_order
    logger.debug("dom_patch: patched PaintOrderRemover.calculate_paint_order")


def _patch_should_exclude_child() -> None:
    """Patch DOMTreeSerializer._should_exclude_child.

    Returns False for nodes with ERP clickable CSS classes, preventing
    them from being excluded by bounding box filtering. Other nodes
    use the original logic.
    """
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    original_should_exclude = DOMTreeSerializer._should_exclude_child

    def patched_should_exclude_child(self, node, active_bounds) -> bool:
        # Existing: protect ERP clickable elements (hand, el-checkbox)
        if _has_erp_clickable_class(node):
            return False
        # D-01: protect div/span inside td up to 2 layers (depth < _MAX_TD_CHILD_DEPTH)
        td_depth = _td_child_depth(node)
        if td_depth is not None and td_depth < _MAX_TD_CHILD_DEPTH:
            return False
        return original_should_exclude(self, node, active_bounds)

    DOMTreeSerializer._should_exclude_child = patched_should_exclude_child
    logger.debug("dom_patch: patched DOMTreeSerializer._should_exclude_child")


def _patch_assign_interactive_indices() -> None:
    """Patch _assign_interactive_indices_and_mark_new_nodes.

    Adds 'is_erp_table_cell_input' as a visibility exception in the
    should_make_interactive condition. Without this, inputs inside <td> cells
    with sales/logistics placeholders are skipped because they lack snapshot_node
    in the Chromium accessibility tree.

    Pattern follows existing exceptions for file inputs (is_file_input) and
    shadow DOM elements (is_shadow_dom_element) in serializer.py.
    """
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    original_method = DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes

    def patched_method(self, node) -> None:
        # Call original first to handle all standard cases
        original_method(self, node)

        # Skip if already marked interactive by original method
        if getattr(node, "is_interactive", False):
            return

        # Skip if not an ERP table cell input
        if not _is_erp_table_cell_input(node):
            return

        # Force interactive assignment for ERP table cell inputs
        node.is_interactive = True
        self._selector_map[node.original_node.backend_node_id] = node.original_node
        counter = getattr(self, "_interactive_counter", 0)
        self._interactive_counter = counter + 1
        node.is_new = True
        logger.debug(
            "dom_patch: forced interactive for ERP table cell input placeholder=%s",
            getattr(node.original_node, "attributes", {}).get("placeholder", "")
        )

        # --- Phase 68: Row identity + strategy annotation ---
        row_identity = _detect_row_identity(node)
        backend_node_id = node.original_node.backend_node_id
        snapshot_node = getattr(node.original_node, 'snapshot_node', None)

        # Base strategy from visibility
        if snapshot_node:
            base_strategy = 1  # Visible input: direct input operation
        else:
            base_strategy = 2  # Hidden/click-to-edit: need click first

        # Apply failure-based downgrade per STRAT-03
        tracker_key = str(backend_node_id)  # _failure_tracker uses str keys
        if tracker_key in _failure_tracker:
            failure_count = _failure_tracker[tracker_key]['count']
            if base_strategy == 1 and failure_count >= 2:
                base_strategy = 2  # Downgrade to click-to-edit
            if base_strategy == 2 and failure_count >= 2:
                base_strategy = 3  # Downgrade to evaluate JS

        _node_annotations[backend_node_id] = {
            'row_identity': row_identity,
            'base_strategy': base_strategy,
            'is_erp_input': True,
        }

    DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = patched_method
    logger.debug("dom_patch: patched _assign_interactive_indices_and_mark_new_nodes")


# Strategy names for DOM dump annotation (D-03)
_STRATEGY_NAMES = {
    1: "1-原生 input",
    2: "2-需先 click",
    3: "3-evaluate JS",
}


def _patch_serialize_tree_annotations() -> None:
    """Patch 6+7: Inject row identity comments and failure annotations into DOM dump.

    Combines two concerns into a single serialize_tree wrapper to avoid
    multi-layer wrapping chains (per D-01):

    - Patch 6: Prepend ``<!-- 行: {id} -->`` above ``<tr>`` elements with IMEI row identity
    - Patch 7: Append strategy + failure annotation for ERP inputs in ``_failure_tracker``
    """
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    original_serialize = DOMTreeSerializer.serialize_tree

    @staticmethod
    def patched_serialize(node, include_attributes, depth=0):
        result = original_serialize(node, include_attributes, depth)
        if not result or not node:
            return result

        orig = getattr(node, 'original_node', None)
        if orig is None:
            return result

        backend_id = getattr(orig, 'backend_node_id', None)
        if backend_id is None:
            return result

        depth_str = depth * '\t'
        lines = []

        # --- Patch 6: Row identity comment ---
        # For <tr> elements: scan td children directly for IMEI (not from sidecar dict,
        # since <tr> nodes are not processed by Patch 4)
        tag = getattr(orig, 'tag_name', '').lower()
        if tag == 'tr':
            row_id = _detect_row_identity_from_tr(orig)
            if row_id:
                lines.append(f'{depth_str}<!-- 行: {row_id} -->')

        lines.append(result)

        # --- Patch 7: Failure + strategy annotation ---
        # Only for ERP inputs that appear in _failure_tracker (D-04)
        ann = _node_annotations.get(backend_id, {})
        if ann.get('is_erp_input') and str(backend_id) in _failure_tracker:
            failure = _failure_tracker[str(backend_id)]
            base_strategy = ann.get('base_strategy', 1)

            # Re-apply failure-based downgrade (tracker may have updated since Patch 4)
            count = failure['count']
            if base_strategy == 1 and count >= 2:
                current_strategy = 2
            elif base_strategy == 2 and count >= 2:
                current_strategy = 3
            else:
                current_strategy = base_strategy

            parts = []
            row_id = ann.get('row_identity')
            if row_id:
                parts.append(f"[行: {row_id}]")
            parts.append(f"[策略: {_STRATEGY_NAMES.get(current_strategy, '?')}]")
            parts.append(f"[已尝试 {count} 次 模式: {failure['mode']}]")

            lines.append(f'{depth_str}<!-- 行内 input {" ".join(parts)} -->')

        return '\n'.join(lines)

    DOMTreeSerializer.serialize_tree = patched_serialize
    logger.debug("dom_patch: patched serialize_tree for row identity and failure annotations")
