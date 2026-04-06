# Technology Stack -- v0.8.4 DOM Patch Optimization

**Project:** aiDriveUITest -- Agent Table Interaction Optimization
**Researched:** 2026-04-06
**Scope:** Stack additions/changes for OPTIMIZE-01 through OPTIMIZE-04 only
**Confidence:** HIGH (verified against installed browser-use 0.12.2 source code)

## Executive Summary

The four optimizations (row identity injection, dynamic annotation, strategy prioritization, failure recovery) are implemented entirely within the existing monkey-patch architecture. No new external dependencies are needed. The work uses browser-use 0.12.2's internal APIs (`DOMTreeSerializer`, `ClickableElementDetector`, `PaintOrderRemover`, `SimplifiedNode`, `EnhancedDOMTreeNode`) which were verified by reading the installed source code.

The key architectural decision: all new patches follow the existing pattern -- save original method, wrap with additional logic, replace. State flows through module-level variables in `dom_patch.py`, updated by `step_callback`, and consumed during DOM serialization.

## Stack for v0.8.4

### Core (NO new dependencies)

| Technology | Version | Purpose | Why No Change Needed |
|------------|---------|---------|---------------------|
| **browser-use** | 0.12.2 | DOM serialization pipeline | All patch targets (`serialize_tree`, `_assign_interactive_indices`, `is_interactive`) are monkey-patchable static/instance methods. Verified in installed source at `.venv/lib/python3.11/site-packages/browser_use/dom/serializer/serializer.py` |
| **Python re** | stdlib | Pattern matching for IMEI/product codes | `re.compile(r"I\d{15}")` for row identity detection. stdlib is sufficient -- no regex library needed |
| **Python dataclasses** | stdlib | Frozen result types | Follows existing `StallResult(frozen=True)` pattern for new detection result types |
| **Python hashlib** | stdlib | DOM fingerprinting for click-no-effect detection | Already used in `agent_service.py` line 196 for `dom_hash`. Extend to track `dom_hash_before` vs `dom_hash_after` per step |

### Internal APIs Being Patched (browser-use 0.12.2)

These are the specific internal APIs that the new patches will monkey-patch. All verified against the installed source.

| API | Location | Current Use | New Use |
|-----|----------|-------------|---------|
| `DOMTreeSerializer.serialize_tree()` | `serializer.py` line 883 | Static method converting `SimplifiedNode` tree to string for LLM | **Post-process**: inject `<!-- row: ... -->` comments, strategy annotations, failure annotations after serialization |
| `DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes()` | `serializer.py` line 617 | Assigns `backend_node_id` based indices to interactive elements | **Extend**: add row归属 annotation + strategy level判定 during index assignment |
| `ClickableElementDetector.is_interactive()` | `clickable_elements.py` line 6 | Determines if a node is clickable | **No change** -- existing Patch 1 already wraps this correctly |
| `SimplifiedNode` | `views.py` line 218 | Tree node with `is_interactive`, `should_display`, `is_new` flags | **Read-only**: check `is_interactive` flag for strategy level判定; no new fields needed on this class |
| `EnhancedDOMTreeNode` | `views.py` line ~400 | Full DOM node with `attributes`, `tag_name`, `parent_node`, `snapshot_node` | **Read-only**: access `attributes.get("class")`, `tag_name`, walk `parent_node` chain, check `snapshot_node` existence for hidden state |

### Serialization Pipeline Integration Points

The browser-use serialization pipeline runs in this order (verified in `serializer.py` lines 100-148):

```
serialize_accessible_elements()
  1. _create_simplified_tree(root_node)       -- Patch 1 (is_interactive) affects this step
  2. PaintOrderRemover.calculate_paint_order() -- Patch 2 affects this step
  3. _optimize_tree(simplified_tree)           -- No patch needed
  4. _apply_bounding_box_filtering()           -- Patch 3 (_should_exclude_child) affects this step
  5. _assign_interactive_indices()             -- Patch 4 affects this step; EXTEND here for strategy
  --> Returns SerializedDOMState(_root, selector_map)

Then later, when LLM needs DOM text:
  llm_representation()
    -> DOMTreeSerializer.serialize_tree(root, include_attributes)  -- NEW Patch 6: inject annotations here
```

**New Patch 6 (`_patch_inject_annotations`)** hooks into `serialize_tree()` as a post-processing step. This is the single injection point for all three annotation types:
- Row identity comments: `<!-- row: I01784004409597 -->`
- Strategy level comments: `<!-- strategy: native-input [index=15] -->`
- Failure tracking comments: `<!-- failed 2x, switch strategy -->`

### State Management Architecture

| State Variable | Location | Type | Lifecycle | Consumer |
|---------------|----------|------|-----------|----------|
| `_failure_tracker` | `dom_patch.py` (module-level) | `dict[int, FailureRecord]` | Reset in `apply_dom_patch()`, updated by `step_callback` via `update_failure_tracker()` | `_patch_inject_annotations()` reads during serialization |
| `_row_identity_map` | `dom_patch.py` (module-level) | `dict[int, str]` (backend_node_id -> row identity) | Built during `_assign_interactive_indices` patch, read during `serialize_tree` patch | `_patch_inject_annotations()` for row comments |
| `_dom_hash_before` | `dom_patch.py` (module-level) | `str` | Updated at start of `step_callback`, compared with new hash for click-no-effect detection | `update_failure_tracker()` |

**Why module-level state (not a class):** Follows the existing `_PATCHED` pattern in `dom_patch.py`. The module is imported once and state persists across calls within a single run. Reset happens in `apply_dom_patch()` which is called per-run in `agent_service.py` line 357.

### Data Structures (New)

```python
# In dom_patch.py -- follows existing frozen dataclass pattern

@dataclass(frozen=True)
class FailureRecord:
    """Immutable record of failure for a specific element index."""
    count: int
    last_error: str
    mode: str  # "repeated_fail" | "click_no_effect" | "wrong_column" | "edit_not_active"

@dataclass(frozen=True)
class FailureDetectionResult:
    """Immutable result from failure detection check."""
    failure_mode: str | None  # None means no failure detected
    target_index: int | None
    message: str
```

### Files Modified (NO new files)

| File | Changes | Lines of Impact |
|------|---------|----------------|
| `backend/agent/dom_patch.py` | Add `_failure_tracker`, `_row_identity_map`, `_dom_hash_before`; add `_detect_row_identity()`, `_patch_add_row_identity()`, `_patch_inject_annotations()`, `update_failure_tracker()`, `reset_tracker_state()`; enhance `_patch_assign_interactive_indices()` | ~200 new lines on top of existing 329 |
| `backend/agent/stall_detector.py` | Add `_check_click_no_effect()`, `_check_wrong_column()`, `_check_edit_not_active()` methods; extend `StallResult` or return `FailureDetectionResult` separately | ~80 new lines |
| `backend/agent/prompts.py` | Append 4 new rule blocks to Section 9: row identity usage, anti-repeat rules, strategy priority, failure recovery | ~40 new lines |
| `backend/core/agent_service.py` | Add `update_failure_tracker()` call in `step_callback` detector area (lines 302-337); add `_dom_hash_before` tracking | ~15 new lines |

## What NOT to Add

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **BeautifulSoup / lxml** | DOM parsing is done by browser-use's CDP-backed pipeline. Re-parsing serialized HTML would be slow and lossy | Walk `SimplifiedNode` tree and `EnhancedDOMTreeNode.parent_node` chains directly |
| **New CSS selector libraries** | browser-use already provides `selector_map` with `backend_node_id` indexing | Use existing `selector_map` and `backend_node_id` for element targeting |
| **State management framework (Redis, etc.)** | Failure tracking is per-run, ephemeral, single-process | Module-level `dict` in `dom_patch.py`, reset per run |
| **New Agent subclass** | `MonitoredAgent` already provides `_pending_interventions` injection and `_execute_actions` override | Add failure detection to existing `StallDetector.check()` flow, inject via existing `_pending_interventions` |
| **JavaScript injection frameworks** | browser-use `evaluate` action already handles JS execution for strategy 3 fallback | Direct `document.querySelector()` strings in prompt guidance |
| **Separate annotation module** | Design doc (66-OPTIMIZE-DESIGN.md D-05) explicitly says: "融入现有 dom_patch.py" | Keep all patches in single `dom_patch.py` file |
| **Schema validation library (marshmallow, etc.)** | `FailureRecord` is a simple 3-field dataclass | Python stdlib `dataclass(frozen=True)` following existing pattern |

## Integration Considerations

### serialize_tree() Patching Strategy

`DOMTreeSerializer.serialize_tree()` is a `@staticmethod` (serializer.py line 883). The new `_patch_inject_annotations()` will:

1. Save reference to original `serialize_tree`
2. Replace with wrapper that:
   - Calls original to get DOM string
   - Post-processes the string to inject annotations based on `_failure_tracker` and `_row_identity_map`
   - Returns annotated string

This approach avoids touching the tree-walking logic and works at the text level, which is simpler and less fragile than modifying the node tree.

### Why Text-Level Annotation (Not Node-Level)

Alternative considered: add annotation data to `SimplifiedNode` objects and modify `serialize_tree` to output them.

Rejected because:
1. `SimplifiedNode` is defined in browser-use's `views.py` -- adding fields would require monkey-patching the class definition
2. `serialize_tree` is a static method with complex branching -- wrapping the full output is safer than modifying internal logic
3. Text-level regex/substring injection on the final output is straightforward: find `[N]<tag` patterns and append `<!-- annotation -->`
4. Failure annotations are dynamic (change per step) while the tree is rebuilt each step anyway -- text post-processing is the natural layer

### Row Identity Detection Implementation

The `_detect_row_identity(tr_node)` function walks `<tr>` children looking for `<td>` cells containing IMEI-format text (`I\d{15}`):

```python
# Detection pattern (conceptual, not implementation)
def _detect_row_identity(simplified_node) -> str | None:
    """Walk <tr> children for <td> with IMEI text."""
    original = simplified_node.original_node
    if original.tag_name.lower() != "tr":
        return None
    for child in simplified_node.children:
        child_original = child.original_node
        if child_original.tag_name and child_original.tag_name.lower() == "td":
            text = child_original.get_all_children_text()
            match = IMEI_PATTERN.search(text or "")
            if match:
                return match.group(0)  # e.g. "I01784004409597"
    return None
```

This uses `get_all_children_text()` which is already used by `_is_textual_td_cell()` (dom_patch.py line 77). Consistent pattern.

### Failure Tracker State Flow

```
step_callback (agent_service.py)
    |
    v
1. Save _dom_hash_before = current dom_hash
2. ... agent executes action ...
3. Compute dom_hash_after from new browser_state
4. Call update_failure_tracker(index, evaluation, dom_hash_before, dom_hash_after)
    |
    v
dom_patch.py:update_failure_tracker()
    |
    v
5. Check failure conditions:
   a. FAILURE_KEYWORDS in evaluation -> increment count for index
   b. dom_hash_before == dom_hash_after + action_name == "click" -> mode="click_no_effect"
   c. WRONG_COLUMN_KEYWORDS in evaluation -> mode="wrong_column"
   d. NOT_EDITABLE_KEYWORDS in evaluation + action_name == "input" -> mode="edit_not_active"
6. Update _failure_tracker[index] = FailureRecord(...)
    |
    v
Next DOM serialization (agent's next step)
    |
    v
_patch_inject_annotations() reads _failure_tracker
    |
    v
DOM dump includes <!-- annotation --> for failed elements
```

### Strategy Level Determination Logic

Strategy assignment happens during `_assign_interactive_indices` (Patch 4 enhanced):

| Condition | Strategy | Annotation |
|-----------|----------|------------|
| `snapshot_node exists` + `is_visible=True` + no failure history | 1 (native input) | `<!-- strategy: native-input -->` |
| `snapshot_node is None` OR `is_visible=False` (hidden by Ant Design) | 2 (click-to-edit) | `<!-- strategy: click-to-edit -->` |
| `_failure_tracker[index].count >= 2` | 3 (evaluate JS) | `<!-- strategy: evaluate-js fallback -->` |

The `snapshot_node` check is the key differentiator. In browser-use 0.12.2, `EnhancedDOMTreeNode.snapshot_node` is populated from CDP's `DOMSnapshot.captureSnapshot`. Ant Design's click-to-edit inputs that are `display:none` will have `snapshot_node=None` (or `is_visible=False`). This is how strategy 1 vs 2 is distinguished.

## Version Compatibility

| Package | Version | Compatibility Note |
|---------|---------|-------------------|
| browser-use | 0.12.2 | All internal APIs verified against installed source. Major version changes (0.13+) may restructure serializer pipeline |
| Python | 3.11 | `dataclass(frozen=True)`, `re`, `hashlib` all stdlib -- no version sensitivity |
| cdp-use | (bundled with browser-use) | CDP protocol is stable; `backend_node_id` indexing is fundamental to browser-use |

**Risk:** browser-use 0.13+ may rename or restructure `DOMTreeSerializer` methods. Mitigation: pin `browser-use>=0.12.2,<0.13` in `pyproject.toml` if upgrading becomes necessary.

## Performance Considerations

| Concern | Impact | Mitigation |
|---------|--------|------------|
| `_failure_tracker` dict lookup during serialization | Negligible -- `dict[int, FailureRecord]` lookup is O(1) | None needed |
| Text post-processing in `_patch_inject_annotations` | Low -- regex on serialized DOM string (~10-50KB typical) | Profile if DOM grows >100KB |
| `_row_identity_map` building during `_assign_interactive_indices` | Low -- one regex scan per `<tr>` node, typically <50 rows | None needed |
| `dom_hash_before` tracking | Already computed per step in `step_callback` | Reuse existing hash, just store before action |

## Sources

### Verified Against Installed Source (HIGH confidence)
- `.venv/lib/python3.11/site-packages/browser_use/dom/serializer/serializer.py` -- `DOMTreeSerializer.serialize_tree()` (line 883), `_assign_interactive_indices_and_mark_new_nodes()` (line 617), `serialize_accessible_elements()` (line 100)
- `.venv/lib/python3.11/site-packages/browser_use/dom/serializer/clickable_elements.py` -- `ClickableElementDetector.is_interactive()` (line 6)
- `.venv/lib/python3.11/site-packages/browser_use/dom/views.py` -- `SimplifiedNode` (line 218), `SerializedDOMState.llm_representation()` (line 937), `EnhancedDOMTreeNode.llm_representation()` (line 595)
- `.venv/lib/python3.11/site-packages/browser_use/dom/service.py` -- `DomService.get_serialized_dom_tree()` (line 1004) -- confirmed `llm_representation` calls `DOMTreeSerializer.serialize_tree()`

### Verified Against Project Source (HIGH confidence)
- `backend/agent/dom_patch.py` -- 5 existing patches, monkey-patch patterns, `_PATCHED` state management
- `backend/agent/stall_detector.py` -- `StallDetector.check()`, `StallResult(frozen=True)`, `_StepRecord`
- `backend/agent/monitored_agent.py` -- `_pending_interventions` injection, `_prepare_context()`, `_execute_actions()`
- `backend/core/agent_service.py` -- `step_callback` (line 175), detector calls area (line 302), `apply_dom_patch()` call (line 357)
- `backend/agent/prompts.py` -- `ENHANCED_SYSTEM_MESSAGE` Section 9 (line 52-83)
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` -- 16 task definitions, dependency chain, design rules

---
*Stack research for: aiDriveUITest v0.8.4 DOM Patch Optimization*
*Researched: 2026-04-06*
