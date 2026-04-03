# Phase 62: 销售出库表格填写修复 - Research

**Researched:** 2026-04-03
**Domain:** browser-use DOM serialization + ERP table DOM visibility
**Confidence:** HIGH

## Summary

The AI agent fails to fill the sales amount field (`销售金额`) in the sales outbound page. Root cause: `<input>` elements inside `<td>` cells are often invisible in browser-use's DOM snapshot because Chromium's accessibility tree doesn't properly expose nested inputs within table cells. Without `snapshot_node`, these inputs are skipped during `_assign_interactive_indices_and_mark_new_nodes`, so they don't receive clickable indices. The agent cannot target specific row inputs.

**Fix approach:** Extend DOM Patch with a 4th patch targeting `_assign_interactive_indices_and_mark_new_nodes` to force visibility for ERP table cell inputs (inputs inside `<td>` with sales-related placeholders). Add 8th prompt section for ERP table cell filling guidance.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DOM-PATCH-01 | Extend DOM Patch — table cell input visibility | Patching `_assign_interactive_indices_and_mark_new_nodes` line 704 |
| PROMPT-01 | Add Section 9 — ERP 表格单元格填写指导 | Adding guidance to ENHANCED_SYSTEM_MESSAGE |
| E2E-01 | E2E 验证 — 销售出库场景测试 | Full ERP sales outbound E2E test |
</phase_requirements>

## Root Cause Analysis

### How browser-use serializes DOM

The `DOMTreeSerializer.serialize_accessible_elements()` pipeline:

```
Step 1: _create_simplified_tree()
  → Creates SimplifiedNode for each accessible DOM node
  → Visibility: node.is_visible (from AX tree)
  → INPUTS inside table cells: is_visible=False if no snapshot_node

Step 2: PaintOrderRemover.calculate_paint_order()
  → Sets ignored_by_paint_order for certain nodes

Step 3: _optimize_tree()
  → Removes invisible nodes with no children
  → INPUTS with children stay (rare for inputs)

Step 4: _apply_bounding_box_filtering()
  → Excludes nodes outside viewport

Step 5: _assign_interactive_indices_and_mark_new_nodes()
  → Assigns clickable indices to interactive+visible elements
  → Line 626: is_visible = node.original_node.snapshot_node and node.original_node.is_visible
  → Line 704: should_make_interactive = is_visible OR is_file_input OR is_shadow_dom_element
  → TABLE CELL INPUTS without snapshot_node → SKIPPED → no index
```

### Why table cell inputs lose snapshot_node

Chromium's `AccessibilityTree.getSnapshot()` (CDP `DOMSnapshot.captureSnapshot`) doesn't always include nested `<input>` elements inside `<td>` cells. The `<td>` cell might be visible but the nested `<input>` (especially those with `opacity:0` or custom-styled) may not be captured in the AX tree.

This is similar to why file inputs (`opacity:0`) need special handling — they're in the DOM but invisible to the AX tree.

### Existing Exception Pattern

From serializer.py lines 653-670:
- File inputs: `is_file_input` → always visible
- Shadow DOM elements: `is_shadow_dom_element` → always visible

Both patterns patch `_assign_interactive_indices_and_mark_new_nodes` line 704.

### Proposed Fix: `is_table_cell_input`

```python
# In _assign_interactive_indices_and_mark_new_nodes, line 704:
elif is_interactive_assign and (is_visible or is_file_input or is_shadow_dom_element or is_table_cell_input):
    should_make_interactive = True
```

Where `is_table_cell_input` detects:
1. Input element inside `<td>` cell (walking parent chain)
2. Has placeholder matching ERP table fields:
   - `销售金额` (sales amount) — PRIMARY TARGET
   - `物流费用` (logistics fee) — secondary
   - `备注` (remark) — tertiary

### Alternative Approaches Considered

1. **Patch `_create_simplified_tree`** to force visibility for table cell inputs
   - Rejected: Too early in pipeline, would affect tree structure

2. **Patch `_optimize_tree`** to not remove inputs inside table cells
   - Rejected: Complex traversal needed, less targeted

3. **JS evaluate to set values directly**
   - Not reliable: Doesn't update React state

4. **Prompt enhancement only**
   - Rejected: Doesn't fix the fundamental DOM visibility issue

**Chosen: Patch `_assign_interactive_indices_and_mark_new_nodes`** — same pattern as existing exceptions (file inputs, shadow DOM), targeted to specific input types.

## DOM Patch Enhancement Plan

### New 4th Patch: `_patch_assign_interactive_indices`

Location: `backend/agent/dom_patch.py`

Add:
1. `ERP_TABLE_CELL_PLACEHOLDERS` — frozenset of placeholder substrings
2. `_is_inside_table_cell(node)` — walks parent chain for `<td>`/`<th>`
3. `_is_erp_table_cell_input(node)` — checks both conditions
4. `_patch_assign_interactive_indices()` — patches line 704 condition

### Existing Patches (unchanged)

1. `_patch_is_interactive()` — marks `span.hand`, `.el-checkbox` as interactive
2. `_patch_paint_order_remover()` — restores paint order for ERP nodes
3. `_patch_should_exclude_child()` — prevents bounding box exclusion for ERP nodes

## Prompt Enhancement Plan

### New Section 9: ERP 表格单元格填写

Add to ENHANCED_SYSTEM_MESSAGE (after Section 8):
- **销售出库表格填写规则**: When filling table cell input fields (销售金额, 物流费用), use the exact placeholder text to locate the correct input in the DOM: `placeholder="销售金额"` for sales amount, `placeholder="物流费用"` for logistics fee
- **Row targeting**: After adding a product to the table, the row's input fields appear in the DOM with placeholder text. Target the specific placeholder to avoid index ambiguity
- **Negative examples**: Don't click `<td>` elements (not interactive). Don't use generic input indices (may hit wrong field). Don't confuse "物流费用" with "销售金额"
- **evaluate JS as fallback**: If standard input fails, use `document.querySelector('input[placeholder="销售金额"]').value = '150'` but verify with `input.value` check

## Implementation Files

| File | Change |
|------|--------|
| `backend/agent/dom_patch.py` | Add 4th patch + 3 helper functions |
| `backend/agent/prompts.py` | Add Section 9 to ENHANCED_SYSTEM_MESSAGE |
| `docs/test-steps/v0.8.1-销售出库填写修复验证.md` | E2E test steps |

## Testing Strategy

1. **Unit test**: Patch applies without error, helper functions work
2. **E2E**: Full sales outbound ERP scenario — add product, fill sales amount, verify value = 150
