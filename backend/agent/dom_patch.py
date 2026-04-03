"""Monkey-patch for browser-use DOM serializer.

Patches PaintOrderRemover and DOMTreeSerializer to prevent ERP table
sub-elements (span.hand, .el-checkbox__inner) from being absorbed by
parent <tr> nodes during DOM serialization. Without this patch, these
elements lose their independent clickable index and the Agent cannot
use standard click(index=N) to interact with them.
"""

import logging

logger = logging.getLogger(__name__)

_PATCHED = False

# CSS class substrings that identify ERP clickable sub-elements
_ERP_CLICKABLE_CLASSES = frozenset({"hand", "el-checkbox"})

# Placeholder substrings identifying ERP table cell input fields
# These inputs are inside <td> cells and may lack snapshot_node in AX tree
_ERP_TABLE_CELL_PLACEHOLDERS = frozenset({
    "销售金额",
    "物流费用",
    "备注",
    "单号",
    "数量",
})


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

    Returns True for nodes with ERP clickable CSS classes, ensuring they
    get assigned interactive indices during DOM serialization. Without this,
    <span class="hand"> and <span class="el-checkbox__inner"> are skipped
    because they lack form controls, event handler attributes, ARIA roles,
    or interactive tag names.
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
        return original_is_interactive(node)

    ClickableElementDetector.is_interactive = patched_is_interactive
    logger.debug("dom_patch: patched ClickableElementDetector.is_interactive")


def apply_dom_patch() -> None:
    """Apply monkey-patches to browser-use DOM serializer.

    Patches three mechanisms:
    1. ClickableElementDetector.is_interactive - marks ERP elements as
       interactive so they receive clickable indices.
    2. PaintOrderRemover.calculate_paint_order - resets ignored_by_paint_order
       for ERP nodes after the original method runs.
    3. DOMTreeSerializer._should_exclude_child - returns False for ERP nodes
       so they are never excluded by bounding box filtering.

    Idempotent: multiple calls are safe and only patch once.
    """
    global _PATCHED
    if _PATCHED:
        logger.debug("dom_patch: already applied, skipping")
        return

    try:
        _patch_is_interactive()
        _patch_paint_order_remover()
        _patch_should_exclude_child()
        _patch_assign_interactive_indices()
        _PATCHED = True
        logger.info("dom_patch: successfully applied all 4 patches")
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
        if _has_erp_clickable_class(node):
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

    DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = patched_method
    logger.debug("dom_patch: patched _assign_interactive_indices_and_mark_new_nodes")
