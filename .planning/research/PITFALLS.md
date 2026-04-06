# Domain Pitfalls: DOM Patch Optimization for Table Interaction

**Domain:** Adding row identity injection, failure tracking, strategy prioritization, and failure recovery to an existing browser-use DOM serialization pipeline
**Researched:** 2026-04-06
**Context:** v0.8.4 milestone -- OPTIMIZE-01 through OPTIMIZE-04 (Phase 66 design, 16 code tasks)

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: `_failure_tracker` Module-Level State Leaking Across Runs

**What goes wrong:** The design specifies `_failure_tracker` as a module-level `dict` in `dom_patch.py` (T07, T08). Because `dom_patch.py` is imported once and the `_PATCHED` flag prevents re-patching, `_failure_tracker` is initialized once at module load time. If `apply_dom_patch()` resets it but the module is already loaded, stale data from a previous test run pollutes the next run. Worse, in the production deployment (Gunicorn 2 workers), each worker process has its own `_failure_tracker`, but within one worker, sequential runs share state.

**Why it happens:** Module-level mutable state (`_failure_tracker = {}`) survives across function calls within the same process. The design says "reset in `apply_dom_patch()`" but `apply_dom_patch()` is idempotent -- the `_PATCHED` guard means it returns immediately on the second call, so the reset never runs. The existing code at `agent_service.py:357` calls `apply_dom_patch()` once at the start of `run_with_streaming()`, but the `_PATCHED` check at line 234 means the reset code added inside `apply_dom_patch()` will only execute on the very first call in that worker's lifetime.

**Consequences:** Second run within same worker sees ghost failure annotations from first run. DOM dumps contain `<!-- 已尝试2次失败 -->` for elements that were never touched. Agent receives false failure signals and skips valid strategy-1 inputs, jumping straight to evaluate JS. Test isolation breaks.

**Prevention:**
1. Do NOT put the `_failure_tracker` reset inside `apply_dom_patch()`. The idempotent guard prevents it from running more than once.
2. Instead, expose a separate `reset_failure_tracker()` function that is called explicitly at the start of each run in `agent_service.py` (line 357 area), BEFORE the agent is created but AFTER the module is imported.
3. Unit tests MUST reset `_failure_tracker` in `setUp()` or `autouse` fixtures, not rely on `apply_dom_patch()` to do it.
4. Consider making `_failure_tracker` a dict that is passed in (dependency injection) rather than module-level global, so each `AgentService.run_with_streaming()` call creates a fresh instance.

**Detection:**
- Run two sequential E2E tests on same worker. Second test's DOM dump contains annotations from first test.
- Unit test order dependence: tests pass individually but fail when run together.
- `backend/tests/` already has known test isolation issues (PROJECT.md Backlog: "5 pre-existing test isolation issues").

**Confidence:** HIGH -- based on direct code analysis of `apply_dom_patch()` idempotent guard (dom_patch.py line 234-235) and Gunicorn 2-worker deployment (deployment-v0.5.0.md).

---

### Pitfall 2: DOM Dump Comment Injection Breaking the `serialize_tree` Parser

**What goes wrong:** The design injects HTML comments (`<!-- 行: I01784004409597 -->`, `<!-- 策略1: 原生 input -->`) into the DOM dump output. The injection point is described as "序列化输出阶段" but the actual `serialize_tree()` method in browser-use's `serializer.py` (line 883) is a recursive text builder that concatenates lines. Injecting comments requires intercepting this method or post-processing the output string. If the comment is injected at the wrong point (e.g., inside a tag's attribute string, or breaking the indentation structure), the LLM receives malformed DOM dump text.

**Why it happens:** The `serialize_tree()` method builds output line-by-line with depth-based tab indentation. Comments must be inserted at the correct depth level and must not break the tree structure the LLM relies on. The design's proposed injection point is ambiguous -- it says "intercept serialization output stage" but the actual code path is: `serialize_accessible_elements()` -> `_create_simplified_tree()` -> `_optimize_tree()` -> `_assign_interactive_indices_and_mark_new_nodes()` -> `llm_representation()` -> `serialize_tree()`. Comment injection can only happen either: (a) during `_assign_interactive_indices` by storing metadata on nodes, or (b) by wrapping `serialize_tree()` to post-process the string output.

**Consequences:** DOM dump becomes garbled. LLM cannot parse element tree. Agent clicks wrong elements or fails entirely. Hard to debug because the issue is in the serialized text format, not in Python logic.

**Prevention:**
1. **Preferred approach:** Do NOT inject comments into the raw `serialize_tree()` output. Instead, store row-identity and strategy metadata as attributes on `SimplifiedNode` (e.g., `node._erp_row_identity = "I01784004409597"`, `node._erp_strategy = 1`). Then monkey-patch `serialize_tree()` to append these as comments at the correct depth level AFTER the element's own line is built, before processing children.
2. If post-processing the string: use regex replacement on the final `serialize_tree()` output, targeting lines that contain known element identifiers (placeholder text, backend_node_id).
3. Write explicit tests that verify the DOM dump output format is valid after comment injection. Test with a realistic mock tree structure.
4. Never inject comments inside XML/HTML tag angle brackets -- only between sibling elements or after closing tags.

**Detection:**
- DOM dump contains `<<` or `>>` or broken indentation.
- LLM output shows confusion about element hierarchy (e.g., treating a comment as a child element).
- `llm_representation()` returns a string with syntax errors visible in step logs.

**Confidence:** HIGH -- based on reading `serialize_tree()` implementation at serializer.py line 883-982 and understanding the recursive text builder pattern.

---

### Pitfall 3: Strategy Annotation Causing Agent to Always Choose Strategy 3 (evaluate JS)

**What goes wrong:** When strategy annotations appear in the DOM dump (`<!-- 策略1: 原生 input -->`, `<!-- 策略3: evaluate JS 兜底 -->`), the LLM agent (Qwen 3.5 Plus) may exhibit recency bias or "complexity preference" -- gravitating toward the last-mentioned or most-detailed strategy option. If the prompt describes all three strategies and the DOM dump shows `<!-- 策略3: evaluate JS 兜底 -->` alongside working strategy-1 inputs, the agent may skip the simpler `input(index=N)` action and jump to `evaluate("...")`, which is less reliable (does not trigger React state updates).

**Why it happens:** LLMs do not reliably follow priority ordering from annotations. The prompt says "优先使用策略1" but the DOM dump shows strategy annotations for every element, including the fallback. The agent sees strategy 3 as a viable option and may choose it because: (a) the evaluate JS path is more explicit (includes a full JS code snippet in the annotation), (b) the agent had previous failures with strategy 1 in its context window and generalizes those failures, or (c) the model's instruction-following for "prefer X" is weaker than its pattern-matching for "here is a concrete action you can take."

**Consequences:** Agent uses evaluate JS for inputs that would work with native `input()` action. evaluate JS does not trigger React's onChange handlers, so the ERP system does not register the value change. Form submission fails because values appear set in DOM but are not in React state. Worse, the agent thinks it succeeded because `input.value` shows the correct value.

**Prevention:**
1. **Only annotate strategy 3 when strategy 1 and 2 have actually failed.** Do NOT annotate all elements with their theoretical strategy level. If an input is visible and has an index, do not add any strategy annotation -- let the agent use it naturally.
2. For strategy annotations, ONLY show the strategy that applies to THIS element, not all three options. Use `<!-- 当前策略: 原生 input -->` rather than listing all three.
3. In the prompt, emphasize: "Do NOT use evaluate JS unless you see a `<!-- 策略降级: evaluate JS -->` annotation on the element. If no strategy annotation is present, use the standard input() action."
4. Include a worked example in the prompt showing the correct behavior: "If you see `<input placeholder='销售金额' /> [15]` with NO strategy annotation, use `input(index=15, value='150')`."
5. Monitor in E2E: track evaluate JS usage count. If it exceeds 20% of table cell inputs, the annotations are biasing the agent.

**Detection:**
- Agent's first attempt on a new table cell uses evaluate JS instead of input().
- Agent uses evaluate JS on elements that have valid strategy-1 annotations.
- Evaluate JS usage rate is high in E2E logs despite most inputs being visible.

**Confidence:** HIGH -- based on established LLM behavior patterns (instruction following weakness, recency bias) and the specific risk of providing explicit JS code in annotations.

---

### Pitfall 4: Row Identity Regex `I\d{15}` False Positives

**What goes wrong:** The row identity detection uses regex `I\d{15}` to match IMEI-like product codes (e.g., `I01784004409597`). This pattern can match non-identity text in ERP table cells:
- Order numbers containing 15+ digits preceded by 'I' (e.g., "Invoice ID: I202604060000123")
- CSS class names or JavaScript variable references that happen to match
- URLs or paths containing the pattern
- The same product code appearing in header cells, footer totals, or adjacent table sections

**Why it happens:** The regex is applied broadly to all `<td>` text content within `<tr>` rows. The ERP system may display the product code in summary rows, filter fields, or search results outside the main editable table. The design (R01-4) says "only take the first match" but does not specify what "first" means when scanning all `<td>` children -- left-to-right DOM order may not correspond to the identity column.

**Consequences:** A non-data row (header, total, filter) gets assigned a row identity, causing the agent to target the wrong row. Multiple rows may get the same identity if the product code appears in a spanning header cell. The `<!-- 行: I... -->` comment appears on the wrong `<tr>`, and the agent fills values into the wrong product's row.

**Prevention:**
1. Restrict regex matching to `<td>` cells that are NOT in `<thead>`, `<tfoot>`, or rows with class "ant-table-header", "ant-table-footer", "ant-table-summary".
2. Only match `<td>` cells whose index position corresponds to the known identity column position (if known from ERP DOM structure). The ERP likely places the product code in a consistent column.
3. Use a stricter regex: `I\d{15}(?!\d)` (negative lookahead to prevent partial matches of longer numbers).
4. After detecting a match, verify the parent `<tr>` has the expected number of `<td>` children (matching the table structure) before assigning row identity.
5. Add a `max_row_identity_per_table` guard: if more than N rows in one table have row identities, the detection is likely too loose.

**Detection:**
- Row identity comment appears on `<thead>` or summary rows in DOM dump.
- Agent targets wrong row despite correct product code in prompt.
- Unit test with mock DOM containing header cells with I-prefix text.

**Confidence:** MEDIUM -- based on analysis of regex pattern and ERP table structure assumptions. The actual ERP DOM may or may not have these edge cases. Needs validation against real ERP HTML.

---

### Pitfall 5: Race Condition Between `step_callback` and DOM Serialization

**What goes wrong:** The design creates a data flow: `step_callback` (runs after each agent step) updates `_failure_tracker` -> DOM serialization (runs at next step) reads `_failure_tracker`. However, `step_callback` is called by browser-use AFTER the agent has already received the DOM dump for that step. The actual sequence in browser-use is: (1) get DOM state -> (2) LLM decides action -> (3) execute action -> (4) call `step_callback` -> (5) get DOM state for next step. The `_failure_tracker` update in step_callback happens in step (4), and the next DOM serialization happens in step (5), so the timing is actually correct for the NEXT step.

But there is a subtler issue: if `_failure_tracker` is updated in `step_callback` which runs in `agent_service.py`, and DOM serialization happens inside browser-use's internal `get_state()` call, the module-level `_failure_tracker` dict could be read while being written if any async interleaving occurs. Python's GIL protects dict operations, but the logical race is: the agent may trigger multiple DOM serializations in one step (e.g., `find_elements` action calls a separate DOM query).

**Why it happens:** The `_failure_tracker` is shared mutable state accessed from two different call sites: written by `step_callback` (in `agent_service.py` / `monitored_agent.py`), read by `_patch_dynamic_annotation()` (called during `DOMTreeSerializer.serialize_accessible_elements()`). Both run on the same async event loop but at different points in the agent loop.

**Consequences:** Inconsistent failure annotations. Rarely, `_failure_tracker` may be read mid-update, showing partial data. More likely: `find_elements` or similar browser-use internal calls trigger DOM serialization without going through the patched path, producing un-annotated DOM dumps.

**Prevention:**
1. Accept that `_failure_tracker` writes are eventually consistent -- the annotations apply to the NEXT step, not the current one. Document this explicitly.
2. Use a `dict.copy()` when reading `_failure_tracker` in `_patch_dynamic_annotation()` to avoid reading partially-updated state.
3. Verify that ALL DOM serialization paths go through `serialize_accessible_elements()` (the patched method), not just the main `llm_representation()` path. Check if `find_elements` or other browser-use actions use a separate code path.
4. Add logging when `_failure_tracker` is read vs written, with step numbers, to verify ordering in E2E tests.

**Detection:**
- Failure annotations appear one step late (expected, document it).
- Failure annotations appear on wrong elements (index mismatch).
- Intermittent test failures that correlate with fast agent steps.

**Confidence:** MEDIUM -- the GIL makes Python dict reads/writes atomic at the bytecode level, but the logical ordering of annotations vs steps requires careful verification. The actual risk depends on browser-use internals that may have changed since training.

---

### Pitfall 6: Monkey-Patch Ordering When Multiple New Patches Modify `_assign_interactive_indices`

**What goes wrong:** The design adds TWO enhancements to Patch 4 (`_patch_assign_interactive_indices`): row identity annotation (T04) and strategy level annotation (T05). Both wrap the same `original_method` from `DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes`. If implemented as separate monkey-patches that each save and wrap the "original" method, the second patch wraps the first patch's wrapper, creating a chain. If the order is wrong, row identity may not be available when strategy annotation runs.

**Why it happens:** The current `_patch_assign_interactive_indices()` (dom_patch.py line 289-328) already wraps the original browser-use method. Adding T04 and T05 on top means there will be 3 layers of wrapping: original browser-use method -> current Patch 4 (force interactive for ERP inputs) -> T04 (row identity) -> T05 (strategy level). If T04 and T05 are registered as separate patches, they must be applied in the correct order. If T04 runs AFTER T05, the row identity is not yet set when strategy annotation checks it.

**Consequences:** Strategy annotations always show "strategy 2" or "strategy 3" because the row identity context is missing, causing the agent to skip strategy 1. Or, row identity annotations appear but strategy annotations do not, because T05's wrapper was applied first and its `original_method` call skips T04's wrapper.

**Prevention:**
1. **Do NOT create separate patch functions for T04 and T05.** Instead, extend the EXISTING `_patch_assign_interactive_indices()` function to include both row identity and strategy logic in a single wrapper. This avoids multi-layer wrapping entirely.
2. If separate functions are unavoidable, document the wrapping order explicitly and enforce it in `apply_dom_patch()`: T05 wraps T04 wraps original Patch 4 wraps browser-use original.
3. Add an assertion in tests that `_assign_interactive_indices_and_mark_new_nodes` has the expected number of wrapper layers.
4. Consider consolidating all "post-assignment" logic (row identity, strategy level, dynamic annotation) into a single `_post_assignment_enhancements()` function called from within the patched method.

**Detection:**
- DOM dump shows row identity comments but no strategy comments (or vice versa).
- Strategy annotations reference wrong row identity.
- Unit test specifically checking wrapper layer count fails.

**Confidence:** HIGH -- based on direct analysis of existing `_patch_assign_interactive_indices()` pattern (dom_patch.py line 289-328) and the design's specification that both T04 and T05 enhance the same method.

---

## Moderate Pitfalls

### Pitfall 7: DOM Hash Unchanged Does Not Mean Click Failed

**What goes wrong:** OPTIMIZE-04 Rule 1 detects "click no effect" by checking `dom_hash_before == dom_hash_after`. But DOM hash staying the same is NORMAL in many scenarios: clicking a table cell that is already in edit mode, clicking an element that triggers a React state update without DOM change, clicking during an animation that hasn't completed, or clicking an element whose only effect is setting a JavaScript variable. The design triggers "click no effect" after just ONE occurrence (R02-3), which means false positives are likely.

**Why it happens:** The DOM hash is a SHA-256 truncation of `llm_representation()` output. If the click activates an input that was already in the DOM (but hidden), the serialized DOM may not change because the input was already indexed by Patch 4. Similarly, if the click scrolls the table slightly but the visible elements don't change, the hash stays the same.

**Prevention:**
1. Increase the threshold from 1 to 2 for "click no DOM change" detection, matching the 2-failure threshold for repeated failures.
2. Only trigger "click no effect" if the action was `click` AND the evaluation contains a failure keyword. Require BOTH signals, not just DOM hash.
3. Exclude "click no effect" detection for elements that are known click-to-edit cells (they may legitimately produce no DOM change if the input was already visible via Patch 4).
4. Add a small delay (200-500ms) before computing the "after" DOM hash, to allow React state updates to render.

**Detection:**
- Agent receives `<!-- 点击无效 -->` annotations on elements that were actually clicked successfully.
- Agent switches to evaluate JS unnecessarily for click-to-edit cells.
- "Click no effect" count is high in E2E logs but final test results are correct.

---

### Pitfall 8: Section 9 Prompt Bloat Overwhelming the Agent

**What goes wrong:** The design adds FOUR new rule blocks to Section 9 of `ENHANCED_SYSTEM_MESSAGE` (T13-T16): row identity usage, anti-repeat rules, strategy priority, failure recovery. Section 9 is already 31 lines (prompts.py line 52-83). Adding 4 more blocks could push it to 60+ lines. Combined with Sections 1-8 (83 lines total), the system prompt becomes very long. Qwen 3.5 Plus has limited context window, and long system prompts reduce instruction-following quality.

**Why it happens:** Each optimization adds rules that the agent "needs to know." But the agent only encounters ERP table interactions in specific test scenarios. For non-table tasks (login, navigation, file upload), all the table-specific rules are noise that dilutes the agent's attention.

**Prevention:**
1. Keep each new Section 9 addition to 3-5 lines maximum. Use terse format, not explanatory prose.
2. Consider conditionally including Section 9 table rules only when the task description mentions table operations (检测 "表格"/"出库"/"入库" keywords in task text).
3. Remove existing redundant rules: Section 2 (line 16-21) "失败恢复强制规则" overlaps with the new OPTIMIZE-04 failure recovery rules. Consolidate.
4. Prioritize rules by impact: row identity (most impactful) > failure recovery > strategy priority > anti-repeat. If prompt length is a concern, drop anti-repeat rules (the DOM annotations handle this).

**Detection:**
- Agent starts ignoring earlier system prompt rules (Sections 1-8) after Section 9 grows.
- Agent takes more steps to complete tasks that do NOT involve table interactions.
- Token usage per step increases significantly.

---

### Pitfall 9: `_pending_interventions` Flooding the Agent's Context Window

**What goes wrong:** Each detector can append messages to `_pending_interventions`. The existing code clears the list after injection (monitored_agent.py line 81: `self._pending_interventions = []`). But with 3 new failure mode detections added to StallDetector, plus the existing stall and progress trackers, a single step could generate 4-5 intervention messages. Each message is injected as a `UserMessage` into the LLM context via `_message_manager._add_context_message()`. These messages accumulate across steps if not properly cleared.

**Why it happens:** The current code clears `_pending_interventions` in `_prepare_context()` (line 81), which runs at the START of each step. But if multiple detectors trigger in the same step_callback, all messages are injected at once. With failure recovery messages containing JS code snippets (`document.querySelector('...').value = '...'`), each message can be 200+ characters. Over 10 steps, this adds 2-3KB of intervention text to the context.

**Prevention:**
1. Cap `_pending_interventions` at 3 messages per step. If more detectors trigger, keep only the highest-priority ones.
2. Implement priority ordering: failure recovery (OPTIMIZE-04) > anti-repeat (OPTIMIZE-02) > stall detection > progress warning.
3. Merge related messages: if stall detection and failure recovery both trigger for the same element, send one combined message.
4. Truncate long messages to 150 characters. JS code snippets should be shortened to just the selector, not the full evaluate expression.

**Detection:**
- Context window fills faster than expected.
- Agent output quality degrades in later steps (step 15+).
- `_pending_interventions` list has 4+ items in step logs.

---

### Pitfall 10: `snapshot_node` Check is Unreliable for Strategy Level Determination

**What goes wrong:** OPTIMIZE-03 strategy level determination relies on `snapshot_node` presence to distinguish strategy 1 (visible input, `snapshot_node` exists) from strategy 2 (hidden input, `snapshot_node` missing). But `snapshot_node` availability depends on Chromium's accessibility tree, which is affected by: headless vs headed mode, React rendering timing, Ant Design's dynamic visibility toggling, and whether the element is within the viewport. The same input may have `snapshot_node` in one step and not in the next.

**Why it happens:** Chromium's `DOMSnapshot.captureSnapshot` is called once per step by browser-use. Between steps, React may re-render the component, Ant Design may toggle the input's visibility based on user interaction, and the element may scroll in/out of the viewport. The `snapshot_node` availability is not stable across steps.

**Consequences:** Strategy level oscillates between 1 and 2 for the same input across steps. The agent sees `<!-- 策略1: 原生 input -->` in step N, then `<!-- 策略2: click-to-edit -->` in step N+1 for the same element. This confuses the agent and may cause it to re-try the click-to-edit workflow on an already-visible input.

**Prevention:**
1. Cache the strategy level per element (by backend_node_id or placeholder text) across steps. Once strategy 1 is detected for an element, do not downgrade to strategy 2 unless `_failure_tracker` records a failure.
2. Use a more robust visibility check: combine `snapshot_node` with `is_visible` attribute AND bounding box dimensions. An input with `snapshot_node=None` but positive bounding box should still be strategy 1.
3. Default to strategy 1 for inputs that already have interactive indices (assigned by Patch 4). Only assign strategy 2 to newly discovered inputs without indices.

**Detection:**
- DOM dump shows different strategy annotations for the same input across consecutive steps.
- Agent re-clicks a cell that is already in edit mode.

---

### Pitfall 11: `update_failure_tracker()` Index Mismatch After DOM Re-serialization

**What goes wrong:** `step_callback` captures `target_index` from the agent's action (e.g., `click(index=15)`). This index is from the PREVIOUS step's DOM serialization. The `_failure_tracker` stores `{15: {"count": 1, ...}}`. But in the NEXT step, DOM re-serialization may assign different indices (element count changes, page structure changes, or elements become visible/hidden). The annotation `_patch_dynamic_annotation()` applies to index 15 in the NEW serialization, which may now point to a completely different element.

**Why it happens:** browser-use re-serializes the DOM at every step. Interactive indices are assigned sequentially starting from 1 based on the current tree structure. If the page changes between steps (new elements appear, elements are removed, scrolling reveals new elements), all indices shift. The failure tracker's `target_index` from step N is meaningless in step N+1's DOM.

**Consequences:** Failure annotations appear on the wrong element. The agent sees `<!-- 已尝试2次失败 -->` on an element it has never interacted with. The real failed element gets no annotation and the agent repeats the same mistake.

**Prevention:**
1. **Do NOT use index as the key for `_failure_tracker`.** Instead, use a stable element identifier: a combination of `backend_node_id` (Chromium's stable node ID within a page load) and element characteristics (tag name + placeholder + row identity).
2. When annotating in the next serialization, match tracker entries to elements by `backend_node_id`, not by interactive index.
3. Add a "stale tracker" cleanup: if a tracker entry's `backend_node_id` no longer exists in the current DOM, remove it.
4. Fallback: if `backend_node_id` is not available, use `(tag_name, placeholder, row_identity)` tuple as a composite key.

**Detection:**
- Failure annotation appears on element with different placeholder text than what the agent actually targeted.
- `backend_node_id` in tracker does not match any element in current DOM.

**Confidence:** HIGH -- this is a fundamental issue with using mutable indices as identifiers across re-serializations. browser-use indices are per-serialization, not stable.

---

## Minor Pitfalls

### Pitfall 12: IMEI Regex Missing Variants

**What goes wrong:** The regex `I\d{15}` assumes all product codes are exactly "I" followed by 15 digits. Real IMEI codes can vary: 14 digits (check digit omitted), alphanumeric product codes (e.g., "SKU-12345"), or codes with hyphens/dots. The ERP system may display product codes in different formats across pages.

**Prevention:** Make the regex configurable. Start with `I\d{14,15}` to handle both 14 and 15 digit variants. Log unmatched `<td>` text in cells adjacent to known identity columns for analysis.

---

### Pitfall 13: `data-row-identity` HTML Attribute Not Reaching DOM Dump

**What goes wrong:** The design says to add `data-row-identity` attribute to `<tr>` elements. But browser-use's `serialize_tree()` only outputs attributes that are in the `include_attributes` list (serializer.py line 948). Custom `data-*` attributes are not in the default include list. The attribute will exist on the DOM element but will never appear in the LLM's DOM dump.

**Prevention:** Do not rely on `data-*` attributes for communication with the agent. Use the comment injection approach exclusively. If `data-row-identity` is needed for internal tracking, it should NOT be the primary mechanism for the agent to see row identity.

---

### Pitfall 14: `_PATCHED` Flag Prevents Re-initialization of New Sub-patches

**What goes wrong:** When new patches are added to `apply_dom_patch()` (T03), the existing `_PATCHED = True` guard means that after the first call, subsequent calls skip all patch registration -- including the new patches. If the code is deployed incrementally (e.g., first OPTIMIZE-01, then OPTIMIZE-02 in a later release), the new patches will not be applied if the worker process was started with the old code and hot-reloaded.

**Prevention:** This is unlikely in practice because uvicorn/gunicorn restart workers on code changes. But if in doubt, change the guard to track which patches are applied individually (set of patch names) rather than a single boolean flag.

---

### Pitfall 15: `evaluate` JS Not Triggering React State Updates

**What goes wrong:** Strategy 3 uses `evaluate("document.querySelector('input[placeholder=\"销售金额\"]').value = '150'")`. Setting `input.value` via JavaScript does NOT trigger React's synthetic onChange event. The ERP's Ant Design form will not register the value change. When the form is submitted, the field appears empty from React's perspective.

**Prevention:**
1. In the evaluate JS fallback, dispatch input and change events after setting value:
   ```javascript
   const input = document.querySelector('input[placeholder="销售金额"]');
   input.value = '150';
   input.dispatchEvent(new Event('input', { bubbles: true }));
   input.dispatchEvent(new Event('change', { bubbles: true }));
   ```
2. Document this in the prompt so the agent includes the event dispatch.
3. Verify in E2E that evaluate JS strategy actually submits correctly by checking the API request payload.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation | Priority |
|-------------|---------------|------------|----------|
| T01-T03: Row identity mechanism | IMEI regex false positives (Pitfall 4) | Restrict to data rows, use stricter regex, verify column position | HIGH |
| T04: Patch 4 row identity enhancement | Patch ordering confusion (Pitfall 6) | Merge into single wrapper, do not create separate patches | HIGH |
| T05: Patch 4 strategy level | `snapshot_node` unreliability (Pitfall 10) | Cache strategy level, use composite visibility check | MEDIUM |
| T06: Strategy annotation injection | Comment breaking parser (Pitfall 2) | Patch `serialize_tree()`, test output format, never inject inside tags | HIGH |
| T07-T08: Failure tracker state | State leaking across runs (Pitfall 1) | Separate reset function, call per-run, DI instead of module global | CRITICAL |
| T09: Dynamic annotation patch | Index mismatch (Pitfall 11) | Use backend_node_id as key, not interactive index | HIGH |
| T10: Strategy downgrade linkage | Agent bias toward strategy 3 (Pitfall 3) | Only annotate failed strategies, do not show all options | HIGH |
| T11: StallDetector extension | DOM hash false positive (Pitfall 7) | Require both hash match AND failure keywords, increase threshold | MEDIUM |
| T12: step_callback integration | Race condition (Pitfall 5) | dict.copy() on read, document eventual consistency | MEDIUM |
| T13-T16: Prompt additions | Section 9 bloat (Pitfall 8) | Cap at 3-5 lines each, consider conditional inclusion | MEDIUM |
| E2E validation | React state not updated by evaluate JS (Pitfall 15) | Include event dispatch in JS snippet, verify form submission | HIGH |

## Implementation Phase Risk Assessment

### Phase 1: Foundation (T01-T03, T07-T08) -- HIGH RISK
The failure tracker state management (Pitfall 1) is the single highest-risk item. If implemented wrong, it poisons all subsequent optimizations. Must be correct before anything else is built on top of it.

### Phase 2: Enhancement (T04-T06) -- MEDIUM-HIGH RISK
Patch ordering (Pitfall 6) and comment injection (Pitfall 2) can cause silent failures that are hard to debug. Recommend writing the DOM dump output format test FIRST (TDD).

### Phase 3: Dynamic (T09-T11) -- HIGH RISK
Index mismatch (Pitfall 11) and DOM hash false positives (Pitfall 7) directly affect the agent's decision-making. Wrong annotations are worse than no annotations.

### Phase 4: Integration (T12-T16) -- MEDIUM RISK
Prompt additions and callback wiring are relatively straightforward but prompt bloat (Pitfall 8) and intervention flooding (Pitfall 9) can degrade overall agent performance.

## Sources

### Primary (HIGH confidence)
- Direct code analysis: `backend/agent/dom_patch.py` (329 lines, 5 existing patches)
- Direct code analysis: `backend/agent/monitored_agent.py` (240 lines, step_callback + interventions)
- Direct code analysis: `backend/agent/stall_detector.py` (138 lines, stall + stagnant DOM detection)
- Direct code analysis: `backend/core/agent_service.py` (447 lines, step_callback with detector calls)
- Direct code analysis: `backend/agent/prompts.py` (97 lines, Section 1-9 system message)
- Direct code analysis: `browser_use/dom/serializer/serializer.py` (serializer pipeline, `serialize_tree()` method)
- Design document: `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` (540 lines, T01-T16)

### Secondary (MEDIUM confidence)
- LLM instruction-following patterns for strategy annotation bias (training data, not verified with Qwen 3.5 Plus specifically)
- React synthetic event behavior for evaluate JS pitfall (well-established React behavior)

---
*Pitfalls research for: DOM Patch Optimization (v0.8.4, OPTIMIZE-01~04)*
*Researched: 2026-04-06*
