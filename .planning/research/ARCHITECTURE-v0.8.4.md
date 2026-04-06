# Architecture Patterns: DOM Patch Optimization Integration (v0.8.4)

**Domain:** AI-driven UI automation test platform -- ERP table interaction optimization
**Researched:** 2026-04-06
**Confidence:** HIGH (all conclusions drawn from direct source code analysis)

## Recommended Architecture

### System Context

The existing system has a layered architecture for browser-use DOM patching and agent monitoring. The v0.8.4 milestone adds four optimization strategies (OPTIMIZE-01 through OPTIMIZE-04) that integrate entirely within two existing files: `backend/agent/dom_patch.py` and `backend/agent/prompts.py`. No new modules are created.

```
                          +-------------------------------------+
                          |        agent_service.py             |
                          |  (orchestration entry point)        |
                          |                                     |
                          |  1. apply_dom_patch()               |
                          |  2. Create detectors                |
                          |  3. Create MonitoredAgent           |
                          |  4. step_callback() {               |
                          |       extract action/index/eval     |
                          |       stall_detector.check()        |
                          |       task_tracker.check()          |
                          |  >>> update_failure_tracker()       |  <-- NEW (OPTIMIZE-02)
                          |       on_step() callback            |
                          |     }                               |
                          +------------------+------------------+
                                             |
                      +----------------------+----------------------+
                      v                      v                      v
            +------------------+  +------------------+  +-------------------+
            | stall_           |  | pre_submit_      |  | task_progress_    |
            | detector.py      |  | guard.py         |  | tracker.py        |
            |                  |  |                  |  |                   |
            | check()          |  | check()          |  | check_progress()  |
            | >>> detect_      |  |                  |  |                   |
            |  failure_mode()  |  |                  |  |                   |  <-- NEW (OPTIMIZE-04)
            +------------------+  +------------------+  +-------------------+
                      |
                      | _pending_interventions
                      v
            +----------------------------------------------+
            |         monitored_agent.py                    |
            |                                              |
            |  _prepare_context()                          |
            |    inject pending interventions into LLM     |
            |  _execute_actions()                          |
            |    block submit if guard says so             |
            |  create_step_callback()                      |
            |    alternative callback path (unused         |
            |    by agent_service.py which defines         |
            |    its own inline step_callback)             |
            +----------------------------------------------+
                      |
                      | triggers DOM serialization each step
                      v
    +=============================================================+
    |       browser-use DOM Serialization Pipeline                 |
    |                                                              |
    |  serialize_accessible_elements()                             |
    |    Step 1: _create_simplified_tree(root_node)                |
    |    Step 2: PaintOrderRemover.calculate_paint_order()         |
    |    Step 3: _optimize_tree(simplified_tree)                   |
    |    Step 4: _apply_bounding_box_filtering(optimized_tree)     |
    |    Step 5: _assign_interactive_indices(filtered_tree)        |
    |    >>> Step 6: strategy annotation (within Step 5 wrapper)   |  <-- NEW (OPTIMIZE-03)
    |    >>> Step 7: dynamic annotation (in serialize_tree)        |  <-- NEW (OPTIMIZE-02/04)
    |                                                              |
    |    Returns: SerializedDOMState + DOM string via              |
    |             serialize_tree() static method                   |
    +=============================================================+
                      |
                      | monkey-patched by
                      v
    +=============================================================+
    |            dom_patch.py (all patches live here)              |
    |                                                              |
    |  EXISTING PATCHES (5):                                       |
    |  Patch 1: _patch_is_interactive()                            |
    |    -> ClickableElementDetector.is_interactive                |
    |    -> Marks ERP CSS classes + textual td cells               |
    |                                                              |
    |  Patch 2: _patch_paint_order_remover()                       |
    |    -> PaintOrderRemover.calculate_paint_order                |
    |    -> Restores paint order for ERP clickable nodes           |
    |                                                              |
    |  Patch 3: _patch_should_exclude_child()                     |
    |    -> DOMTreeSerializer._should_exclude_child                |
    |    -> Prevents bbox exclusion for ERP nodes                  |
    |                                                              |
    |  Patch 4: _patch_assign_interactive_indices()                |
    |    -> DOMTreeSerializer._assign_interactive_indices...       |
    |    -> Forces interactive for ERP table cell inputs           |
    |    >>> Enhanced: + row identity annotation                    |  <-- NEW (OPTIMIZE-01)
    |    >>> Enhanced: + strategy level annotation                  |  <-- NEW (OPTIMIZE-03)
    |                                                              |
    |  Patch 5: _is_textual_td_cell() helper (used by Patch 1)    |
    |                                                              |
    |  NEW MODULE-LEVEL STATE:                                     |
    |  _failure_tracker: dict[int, dict]                           |  <-- NEW (OPTIMIZE-02)
    |    {index: {count, last_error, mode}}                        |
    |    modes: repeated_fail / click_no_effect /                  |
    |           wrong_column / edit_not_active                     |
    |                                                              |
    |  NEW PATCHES:                                                |
    |  Patch 6: _patch_add_row_identity()                          |  <-- NEW (OPTIMIZE-01)
    |    -> Intercepts serialization to annotate <tr> with         |
    |       row identity (IMEI/product code) as HTML comments      |
    |                                                              |
    |  Patch 7: _patch_dynamic_annotation()                        |  <-- NEW (OPTIMIZE-02/04)
    |    -> Reads _failure_tracker during serialization             |
    |    -> Injects failure/warning annotations into DOM dump      |
    |                                                              |
    |  NEW HELPERS:                                                |
    |  _detect_row_identity(tr_node) -> str | None                 |  <-- NEW (OPTIMIZE-01)
    |  update_failure_tracker(index, evaluation, dom_hash)         |  <-- NEW (OPTIMIZE-02)
    |  reset_failure_tracker()                                     |  <-- NEW (OPTIMIZE-02)
    +=============================================================+
                      |
                      | annotations appear in
                      v
    +=============================================================+
    |                prompts.py Section 9                          |
    |                                                              |
    |  EXISTING (lines 52-83):                                     |
    |  - Click-to-edit workflow                                    |
    |  - Placeholder matching                                      |
    |  - Row location by product name/IMEI                         |
    |  - Prohibited behaviors                                      |
    |  - evaluate JS fallback                                      |
    |                                                              |
    |  APPENDED:                                                   |
    |  >>> Row identity usage rules (OPTIMIZE-01)                  |
    |  >>> Anti-repetition rules (OPTIMIZE-02)                     |
    |  >>> Strategy priority rules (OPTIMIZE-03)                   |
    |  >>> Failure recovery rules (OPTIMIZE-04)                    |
    +=============================================================+
```

### Component Boundaries

| Component | Responsibility | Communicates With | File |
|-----------|---------------|-------------------|------|
| **AgentService** | Orchestrates agent creation, step callback, detector wiring | MonitoredAgent, all detectors, dom_patch | `backend/core/agent_service.py` |
| **MonitoredAgent** | Bridges detectors into browser-use Agent lifecycle | StallDetector, PreSubmitGuard, TaskProgressTracker, LLM context | `backend/agent/monitored_agent.py` |
| **StallDetector** | Detects consecutive failures, stagnant DOM | MonitoredAgent via check() return | `backend/agent/stall_detector.py` |
| **dom_patch** | Monkey-patches browser-use DOM serializer for ERP elements | browser-use internals, _failure_tracker read by patches | `backend/agent/dom_patch.py` |
| **prompts** | System message extending browser-use agent behavior | MonitoredAgent via extend_system_message parameter | `backend/agent/prompts.py` |
| **DOMTreeSerializer** | (browser-use internal) Serializes DOM tree to string | Patched by dom_patch.py | `.venv/.../browser_use/dom/serializer/serializer.py` |
| **PaintOrderRemover** | (browser-use internal) Removes hidden-by-overlap elements | Patched by dom_patch.py | `.venv/.../browser_use/dom/serializer/paint_order.py` |
| **ClickableElementDetector** | (browser-use internal) Determines element interactivity | Patched by dom_patch.py | `.venv/.../browser_use/dom/serializer/clickable_elements.py` |

### Data Flow

#### Current Data Flow (v0.8.3)

```
1. agent_service.run_with_streaming()
   -> apply_dom_patch()           # One-time patch registration
   -> Create StallDetector, PreSubmitGuard, TaskProgressTracker
   -> Create MonitoredAgent(stall_detector, pre_submit_guard, task_progress_tracker)

2. Each step:
   agent._step()                  # browser-use internal
     -> browser_state = get_state()
       -> DOMTreeSerializer.serialize_accessible_elements()
         -> _create_simplified_tree()      [Patch 1 intercepts is_interactive]
         -> PaintOrderRemover()            [Patch 2 resets paint order for ERP]
         -> _optimize_tree()
         -> _apply_bounding_box_filtering() [Patch 3 prevents ERP exclusion]
         -> _assign_interactive_indices()  [Patch 4 forces ERP input indices]
         -> serialize_tree()               [generates DOM string for LLM]
     -> llm.decide(dom_state)     # LLM sees the serialized DOM

   -> step_callback(browser_state, agent_output, step)
     -> Extract: action_name, target_index, evaluation, dom_hash
     -> stall_detector.check(action_name, target_index, evaluation, dom_hash)
        -> If should_intervene: agent._pending_interventions.append(message)
     -> task_tracker.check_progress(step, max_steps)
        -> If should_warn: agent._pending_interventions.append(message)
     -> task_tracker.update_from_evaluation(evaluation)

3. Next step (after callback):
   agent._prepare_context()
     -> super()._prepare_context()   # clears context_messages
     -> Inject _pending_interventions as UserMessages
```

#### New Data Flow (v0.8.4 additions)

```
SAME AS ABOVE, PLUS:

2b. step_callback (extended):
     -> update_failure_tracker(target_index, evaluation, dom_hash)   # NEW
        -> Reads evaluation for failure keywords
        -> Compares dom_hash with previous step for click-no-effect detection
        -> Updates _failure_tracker module-level state
        -> Returns failure_mode if detected

     -> stall_detector.detect_failure_mode(action_name, target_index, ...)  # NEW
        -> Returns extended FailureDetectionResult with failure_mode field
        -> failure_mode: "click_no_effect" | "wrong_column" | "edit_not_active"

2c. DOM serialization (extended, triggered next step):
     DOMTreeSerializer.serialize_accessible_elements()
       -> ... existing pipeline ...
       -> _assign_interactive_indices()    [Patch 4 enhanced]
         -> For each ERP input: detect row identity via parent <tr>
         -> Determine strategy level:
              snapshot_node exists -> Strategy 1 (native input)
              snapshot_node missing -> Strategy 2 (click-to-edit)
              _failure_tracker has 2+ failures -> Strategy 3 (evaluate JS)
         -> Annotate node with strategy info

       -> _patch_add_row_identity()          [Patch 6 NEW]
         -> Traverse tree, find <tr> nodes with IMEI/product code in child <td>
         -> Inject <!-- ROW: {product_code} --> into DOM dump

       -> _patch_dynamic_annotation()        [Patch 7 NEW]
         -> Read _failure_tracker
         -> For each tracked failure index:
              Inject annotation into DOM dump:
              "repeated_fail": <!-- tried N times, switch strategy -->
              "click_no_effect": <!-- no response, try evaluate JS -->
              "wrong_column": <!-- not target column, ignore -->
              "edit_not_active": <!-- edit mode not activated, CLICK first -->
```

### Key Integration Points

#### Integration Point 1: Module-Level State Sharing (dom_patch.py <-> agent_service.py)

**Problem:** The step_callback runs in agent_service.py but DOM serialization runs in browser-use internals. The _failure_tracker state must be shared across these boundaries.

**Solution:** Module-level variable in dom_patch.py, same pattern as existing `_PATCHED`:

```python
# dom_patch.py (existing pattern)
_PATCHED = False

# dom_patch.py (new)
_failure_tracker: dict[int, dict] = {}
_previous_dom_hash: str = ""

def update_failure_tracker(index: int, evaluation: str, dom_hash: str) -> str | None:
    """Called from step_callback. Updates _failure_tracker. Returns failure_mode."""
    ...

def reset_failure_tracker() -> None:
    """Called at run start."""
    global _failure_tracker, _previous_dom_hash
    _failure_tracker = {}
    _previous_dom_hash = ""
```

**In agent_service.py step_callback:**
```python
from backend.agent.dom_patch import update_failure_tracker

# After existing detector calls (around line 335):
failure_mode = update_failure_tracker(target_index, evaluation, dom_hash)
if failure_mode:
    agent._pending_interventions.append(...)
```

**Confidence:** HIGH. This follows the exact pattern of the existing `_PATCHED` flag and is consistent with the project's "module-level state for cross-boundary sharing" approach.

#### Integration Point 2: DOM Serialization Pipeline Injection

**The serialization pipeline is:**
```
serialize_accessible_elements()
  -> _create_simplified_tree()       [Step 1]
  -> PaintOrderRemover()             [Step 2]
  -> _optimize_tree()                [Step 3]
  -> _apply_bounding_box_filtering() [Step 4]
  -> _assign_interactive_indices()   [Step 5]
```

**New patches inject at these points:**

| New Patch | Injection Point | Method |
|-----------|----------------|--------|
| Patch 6 (row identity) | Wrap `_assign_interactive_indices` (Step 5) | After indices assigned, traverse tree to annotate `<tr>` nodes |
| Patch 7 (dynamic annotation) | Wrap `serialize_tree` (the static method that produces final text) | Post-process the string output to inject failure annotations |
| Patch 4 enhancement (strategy) | Wrap `_assign_interactive_indices` (Step 5) | During index assignment, detect strategy level and annotate |

**Important:** Patch 6 and Patch 4 enhancement both modify behavior at Step 5. They should be composed into a single enhanced wrapper around `_assign_interactive_indices_and_mark_new_nodes` to avoid double-patching the same method.

Patch 7 (dynamic annotation) should wrap `serialize_tree` (the static method), NOT the earlier pipeline steps, because it needs to modify the final text output. However, `serialize_tree` is a `@staticmethod`, so wrapping it requires replacing it on the class.

**Alternative approach for Patch 7:** Instead of wrapping `serialize_tree`, add annotations to `SimplifiedNode` attributes during Step 5, then let the existing `serialize_tree` logic render them. This is cleaner because it avoids string-level post-processing.

**Recommended approach for strategy annotation:** Add a custom attribute to `SimplifiedNode` (e.g., `_erp_strategy_annotation: str`) during the enhanced Patch 4, then patch `serialize_tree` to emit that annotation as an HTML comment. Since `SimplifiedNode` uses `@dataclass(slots=True)`, adding attributes dynamically requires `setattr` with `__dict__` or modifying the class. Better: store annotations in a module-level dict keyed by `backend_node_id`, read during `serialize_tree`.

**Confidence:** HIGH for the integration points. MEDIUM for the specific SimplifiedNode attribute approach -- needs verification that monkey-patching `serialize_tree` with annotation lookup works correctly.

#### Integration Point 3: StallDetector Extension

**Current StallDetector.check() signature:**
```python
def check(self, action_name, target_index, evaluation, dom_hash) -> StallResult
```

**Extension options for OPTIMIZE-04:**

Option A: Extend StallDetector with new methods:
```python
def detect_failure_mode(self, action_name, target_index, evaluation, dom_hash) -> FailureDetectionResult
```
This keeps the existing `check()` unchanged and adds a parallel detection path.

Option B: Extend the existing `check()` to return richer results by adding `failure_mode` to StallResult. But `StallResult` is `frozen=True`, so adding a field changes the interface.

**Recommendation:** Option A. Add a separate `detect_failure_mode()` method that returns a new `FailureDetectionResult` dataclass. This preserves the existing StallDetector interface and keeps the new detection orthogonal.

The three failure modes to detect:
1. `click_no_effect`: action_name == "click" AND dom_hash unchanged from previous step
2. `wrong_column`: evaluation contains keywords like "wrong column" / related Chinese terms
3. `edit_not_active`: action_name == "input" AND evaluation contains "not editable" / related Chinese terms

**Confidence:** HIGH. The detection logic is straightforward keyword matching and dom_hash comparison. StallDetector already has the _history list to track previous dom_hash values.

#### Integration Point 4: Prompt Section 9 Extension

**Current Section 9** (prompts.py lines 52-83) ends with the click-to-edit workflow rules.

**New content appends** after line 83, adding four blocks:
1. Row identity usage (how to read row identity comment markers)
2. Anti-repetition response (how to react to failure annotations)
3. Strategy priority (how to interpret strategy level annotations)
4. Failure recovery (specific recovery workflows for three failure modes)

**Integration note:** These are purely additive. No existing prompt content is modified. The ENHANCED_SYSTEM_MESSAGE is passed as `extend_system_message` to browser-use Agent, which appends it to the base system prompt.

**Confidence:** HIGH. Straightforward text addition with no code dependencies.

## Patterns to Follow

### Pattern 1: Monkey-Patch with Original Preservation

**What:** Every patch saves the original method, wraps it, and replaces it on the class.
**When:** All DOM patch modifications.
**Example** (from existing code, dom_patch.py):

```python
def _patch_assign_interactive_indices() -> None:
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    original_method = DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes

    def patched_method(self, node) -> None:
        original_method(self, node)  # Always call original first
        # ... ERP-specific enhancements ...

    DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes = patched_method
```

**New patches MUST follow this exact pattern.** Never replace a method without calling the original first. The idempotent `_PATCHED` flag prevents double-patching.

### Pattern 2: Module-Level State for Cross-Boundary Communication

**What:** When step_callback (in agent_service.py) needs to communicate state to DOM patches (in dom_patch.py), use module-level variables with accessor functions.
**When:** _failure_tracker, _previous_dom_hash.
**Example** (existing pattern with `_PATCHED`):

```python
# dom_patch.py
_PATCHED = False

def apply_dom_patch():
    global _PATCHED
    if _PATCHED:
        return
    ...
    _PATCHED = True
```

**New state:**
```python
# dom_patch.py
_failure_tracker: dict[int, dict] = {}

def update_failure_tracker(index, evaluation, dom_hash):
    global _failure_tracker
    # ... update logic ...

def reset_failure_tracker():
    global _failure_tracker
    _failure_tracker = {}
```

### Pattern 3: Frozen Dataclass for Detector Results

**What:** All detector return types use `@dataclass(frozen=True)` for immutability.
**When:** New FailureDetectionResult for OPTIMIZE-04.
**Example** (from stall_detector.py):

```python
@dataclass(frozen=True)
class StallResult:
    should_intervene: bool
    message: str
```

**New result type:**
```python
@dataclass(frozen=True)
class FailureDetectionResult:
    failure_mode: str | None  # None, "click_no_effect", "wrong_column", "edit_not_active"
    index: int | None
    message: str
```

### Pattern 4: Annotation Storage via Module-Level Dict

**What:** Since `SimplifiedNode` uses `@dataclass(slots=True)` and cannot have arbitrary attributes added, store annotations in a module-level dict keyed by `backend_node_id`.
**When:** Strategy annotations and row identity annotations that need to be emitted during `serialize_tree()`.
**Example:**

```python
# dom_patch.py
_strategy_annotations: dict[int, str] = {}  # backend_node_id -> annotation text
_row_identity_map: dict[int, str] = {}      # tr backend_node_id -> product code

# During _assign_interactive_indices (enhanced Patch 4):
_strategy_annotations[node.original_node.backend_node_id] = "strategy 1: native input"

# During serialize_tree (patched to emit annotations):
def patched_serialize_tree(node, include_attributes, depth):
    # ... original logic ...
    annotation = _strategy_annotations.get(node.original_node.backend_node_id)
    if annotation:
        line += f" {annotation}"
```

### Pattern 5: Detector Call Ordering in step_callback

**What:** Detectors are called in a specific order within try/except for fault tolerance.
**When:** Adding new failure tracking calls to step_callback.
**Example** (from agent_service.py lines 302-337):

```python
try:
    # Stall detection (existing)
    stall_result = agent._stall_detector.check(...)
    if stall_result.should_intervene:
        agent._pending_interventions.append(stall_result.message)

    # Progress tracking (existing)
    progress_result = agent._task_tracker.check_progress(...)
    ...

    # Failure tracking (NEW)
    failure_mode = update_failure_tracker(target_index, evaluation, dom_hash)
    if failure_mode:
        ...

except Exception as e:
    logger.error(f"[{run_id}][MONITOR] Detector error (non-blocking): {e}")
```

**Key constraint:** All new detector calls MUST be inside the existing try/except block and MUST NOT raise exceptions that break the agent loop.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Patching serialize_tree with String Post-Processing

**What:** Trying to modify the DOM dump string after it has been generated by `serialize_tree()`.
**Why bad:** The output string is a complex multi-line format with indentation, element nesting, and special characters. String-level post-processing is fragile and breaks when browser-use changes the format.
**Instead:** Store annotations as data during tree traversal (Step 5), then patch `serialize_tree` to emit them during rendering. This separates data from presentation.

### Anti-Pattern 2: Adding Attributes to SimplifiedNode Dynamically

**What:** Using `setattr()` or `__dict__` manipulation to add custom attributes to `SimplifiedNode`.
**Why bad:** `SimplifiedNode` uses `@dataclass(slots=True)` which prevents dynamic attribute creation. Any attempt to do `node._strategy = "..."` will raise `AttributeError`.
**Instead:** Use module-level dicts keyed by `backend_node_id` (Pattern 4 above).

### Anti-Pattern 3: Modifying StallDetector.check() Signature

**What:** Adding `failure_mode` to the existing `check()` method's return type.
**Why bad:** `StallResult` is frozen and used by `monitored_agent.py` as well. Changing it forces changes in two files and risks breaking the existing stall detection flow.
**Instead:** Add a new `detect_failure_mode()` method with a new `FailureDetectionResult` return type.

### Anti-Pattern 4: Creating New Python Modules for Optimizations

**What:** Creating files like `backend/agent/failure_tracker.py` or `backend/agent/strategy_annotation.py`.
**Why bad:** The project decision (D-04/D-05) explicitly states all DOM Patch work stays in `dom_patch.py` and all prompt work stays in `prompts.py`. Adding modules increases coupling and violates the project's architectural convention.
**Instead:** Keep all new code in `dom_patch.py` using the existing helper function + patch function organization.

### Anti-Pattern 5: Forgetting to Reset Module-Level State Between Runs

**What:** Leaving `_failure_tracker` populated from a previous run.
**Why bad:** Stale failure data from a previous task would incorrectly annotate elements in a new task, causing the agent to avoid elements that have never failed.
**Instead:** Call `reset_failure_tracker()` inside `apply_dom_patch()` (which is called at the start of each `run_with_streaming()` call). The existing `_PATCHED` guard means `apply_dom_patch()` won't re-apply patches, but the reset must happen unconditionally.

**Implementation note:** Since `apply_dom_patch()` has an early return when `_PATCHED` is True, the reset call should be either:
- Before the `_PATCHED` check (reset every call but don't re-patch), or
- In a separate `reset_dom_patch_state()` function called from agent_service.py before each run.

The second option is cleaner because it separates "register patches once" from "reset state per run."

## Build Order

Based on dependency analysis, the following build order minimizes rework and allows incremental testing:

### Phase 1: Foundation (no dependencies, can be tested independently)

| Task | File | Description |
|------|------|-------------|
| T01 | dom_patch.py | `_detect_row_identity(tr_node)` -- extract IMEI/product code from `<tr>` children |
| T07 | dom_patch.py | `_failure_tracker` module-level state + `reset_failure_tracker()` |
| T08 | dom_patch.py | `update_failure_tracker(index, evaluation, dom_hash)` function |
| T11 | stall_detector.py | `detect_failure_mode()` new method + `FailureDetectionResult` dataclass |

**Rationale:** These are leaf tasks with no dependencies. T01 is a pure helper function. T07/T08 establish the state management that later tasks read. T11 extends StallDetector independently.

**Testing:** Unit test `_detect_row_identity()` with mock `AccessibilityNode` objects. Unit test `update_failure_tracker()` with various evaluation strings. Unit test `detect_failure_mode()` with simulated step histories.

### Phase 2: DOM Patch Enhancements (depends on Phase 1)

| Task | File | Description |
|------|------|-------------|
| T02 | dom_patch.py | `_patch_add_row_identity()` -- Patch 6, uses T01 |
| T03 | dom_patch.py | Register new patch in `apply_dom_patch()` |
| T04 | dom_patch.py | Enhance Patch 4 with row identity annotation (uses T01) |
| T05 | dom_patch.py | Enhance Patch 4 with strategy level detection (uses T04) |
| T06 | dom_patch.py | `_inject_strategy_annotation()` -- reads `_failure_tracker` (T07) + strategy from T05 |
| T09 | dom_patch.py | `_patch_dynamic_annotation()` -- Patch 7, reads `_failure_tracker` (T07) |
| T10 | dom_patch.py | Strategy downgrade integration (T05 + T07) |

**Rationale:** These tasks modify the DOM serialization pipeline. T02 creates Patch 6 (row identity). T04-T05-T06 progressively enhance Patch 4. T09 creates Patch 7 (dynamic annotation). T10 connects failure tracking to strategy downgrade.

**Testing:** Integration test with a mock DOM tree containing ERP table rows. Verify that annotations appear correctly in the serialized output.

**Critical note:** T02, T04, T05, T09, and T10 all modify `_assign_interactive_indices_and_mark_new_nodes`. They should be composed into a single enhanced wrapper rather than stacking multiple patches on the same method. The design should plan for this composition from the start.

### Phase 3: Service Wiring (depends on Phase 1 + Phase 2)

| Task | File | Description |
|------|------|-------------|
| T12 | agent_service.py | Call `update_failure_tracker()` and `detect_failure_mode()` in step_callback |
| Reset | agent_service.py | Call `reset_failure_tracker()` before agent.run() |

**Rationale:** Connects the monitoring layer to the DOM patch state. This is the integration point that makes everything work together.

**Testing:** Integration test running a simulated agent step sequence. Verify that `_failure_tracker` accumulates correctly and annotations appear in subsequent DOM serializations.

### Phase 4: Prompt Layer (depends on Phase 2 + Phase 3)

| Task | File | Description |
|------|------|-------------|
| T13 | prompts.py | Section 9 append: row identity usage rules |
| T14 | prompts.py | Section 9 append: anti-repetition rules |
| T15 | prompts.py | Section 9 append: strategy priority rules |
| T16 | prompts.py | Section 9 append: ERP failure recovery rules |

**Rationale:** Prompts are documentation for the agent. They must reference the actual annotation formats produced by Phase 2, so they come last. They can be written in parallel with Phase 3 since they don't depend on the wiring code.

**Testing:** Manual E2E test with the full sales outbound scenario. Compare step counts and error rates against the baseline.

## Scalability Considerations

| Concern | At 10 elements | At 100 elements | At 1000 elements |
|---------|---------------|-----------------|------------------|
| Row identity detection | Negligible | Negligible | Linear scan of all `<tr>` nodes, but ERP tables rarely exceed 50 rows |
| Failure tracker lookup | O(1) dict lookup | O(1) dict lookup | O(1) dict lookup |
| Strategy annotation injection | O(n) tree traversal | O(n) tree traversal | O(n) tree traversal, n = interactive elements |
| Dynamic annotation injection | O(n) tree traversal | O(n) tree traversal | O(n) tree traversal |
| Module-level dict size | < 1 KB | < 10 KB | < 50 KB, cleared per run |

No performance concerns. All operations are O(n) at worst, where n is the number of interactive elements (typically 20-80 in ERP pages).

## Component Modification Summary

### Files Modified (existing)

| File | Nature of Change | Risk |
|------|-----------------|------|
| `backend/agent/dom_patch.py` | Add 6+ functions, 2 module-level dicts, enhance 1 existing patch, add 2 new patches | MEDIUM -- central file, but changes are additive |
| `backend/agent/stall_detector.py` | Add 1 dataclass, 1 method | LOW -- additive, no existing code changed |
| `backend/core/agent_service.py` | Add approximately 15 lines in step_callback, add 1 import, add reset call | LOW -- additions to existing try/except block |
| `backend/agent/prompts.py` | Append approximately 40 lines to Section 9 string | LOW -- pure text addition |

### Files NOT Modified

| File | Reason |
|------|--------|
| `monitored_agent.py` | The step_callback is defined inline in agent_service.py, not using MonitoredAgent.create_step_callback(). No changes needed. |
| `pre_submit_guard.py` | No relationship to the new optimizations. |
| `task_progress_tracker.py` | No relationship to the new optimizations. |
| `browser_agent.py` | Uses a simpler Agent (not MonitoredAgent), not the target for these optimizations. |
| `proxy_agent.py` | Not involved in the DOM patch pipeline. |

### New Files

None. All code is added to existing files per project decision D-04.

## Sources

- `backend/agent/dom_patch.py` -- Existing 5 patches, module-level `_PATCHED` pattern
- `backend/agent/stall_detector.py` -- StallDetector.check(), frozen StallResult pattern
- `backend/agent/monitored_agent.py` -- _pending_interventions bridge pattern, step_callback structure
- `backend/core/agent_service.py` -- step_callback detector calls (lines 302-337), apply_dom_patch() call (line 357)
- `backend/agent/prompts.py` -- ENHANCED_SYSTEM_MESSAGE Section 9 (lines 52-83)
- `.venv/.../browser_use/dom/serializer/serializer.py` -- DOMTreeSerializer serialization pipeline (1276 lines)
- `.venv/.../browser_use/dom/serializer/paint_order.py` -- PaintOrderRemover (197 lines)
- `.venv/.../browser_use/dom/views.py` -- SimplifiedNode dataclass with slots=True (lines 218-258)
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` -- Design document with 16 code tasks (T01-T16)
