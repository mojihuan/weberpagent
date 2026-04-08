# Phase 69: 服务集成与 Prompt 规则 - Research

**Researched:** 2026-04-07
**Domain:** step_callback 集成 + Prompt 规则追加
**Confidence:** HIGH

## Summary

Phase 69 的核心任务是激活 Phase 67/68 已实现但从未调用的两个函数（`detect_failure_mode()` 和 `update_failure_tracker()`），并在 Section 9 追加四组操作规则。研究确认了 step_callback 的现有结构、`selector_map` 的键类型映射、dom_hash 闭包变量的插入点，以及现有 Section 9 的精确行位置和格式风格。

所有被集成的函数已通过 Phase 67/68 的单元测试验证，函数签名和数据结构已锁定。集成工作本质上是"接线"——在 step_callback 的正确位置插入调用，并将 Phase 68 注释格式翻译为 Agent 可理解的 Prompt 指令。

**Primary recommendation:** 在 step_callback 的 detector calls 区域（line 302-337）内，stall_detector.check() 之后添加 detect_failure_mode + update_failure_tracker 调用链；Section 9 在 line 83 之后按 行标识 -> 反重复 -> 策略优先级 -> 失败恢复 顺序追加四个子节。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 调用顺序：先 `detect_failure_mode()` 检测失败，如果有失败结果（`failure_mode is not None`）则调用 `update_failure_tracker()` 写入 tracker
- **D-02:** dom_hash_before/after 通过闭包变量存储。step_callback 用 `_prev_dom_hash` 闭包变量存上一步 dom_hash，调用后更新为当前 dom_hash
- **D-03:** 仅在失败时调用 detect_failure_mode()。条件：evaluation 包含失败关键词（'失败'/'wrong'/'error'/'无法'/'不成功'/'未'）
- **D-04:** 只修改 agent_service.py 的 inline step_callback，不碰 monitored_agent.py 的死代码
- **D-05:** 简洁操作指令风格，每组规则 2-4 行，"看到 X -> 做 Y" 格式，不加解释性文字。与现有 Section 9 风格一致
- **D-06:** 规则追加顺序：行标识 -> 反重复 -> 策略优先级 -> 失败恢复（定位->操作->异常的逻辑链）
- **D-07:** 只追加新规则，不修改现有 Section 9 内容
- **D-08:** Mock 单元测试为主，mock step_callback 的输入，验证调用链路和数据正确性

### Claude's Discretion
- 具体的失败关键词列表确定
- detect_failure_mode() 调用的 dom_hash 前后对比的具体边界条件处理（如 _prev_dom_hash 为 None 的第一步）
- Section 9 每组规则的具体措辞

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ANTI-03 | step_callback 在 detector calls 区域调用 `update_failure_tracker()`，将 evaluation 失败关键词和 dom_hash 变化检测结果写入 tracker | D-01 确定调用顺序；D-02 确定闭包变量模式；`selector_map[index]` 映射 backend_node_id |
| RECOV-02 | step_callback 在 detector calls 区域添加新检测逻辑调用，将三种失败模式结果写入 `_failure_tracker` 对应 mode 字段 | detect_failure_mode() 已实现三种模式检测，返回 FailureDetectionResult |
| RECOV-03 | Section 9 追加 ERP 表格专用失败恢复规则——三种失败模式各自的检测->标注->切换操作流程 | D-05/D-06 确定格式和顺序；Phase 68 D-03 确定策略命名 |
| PROMPT-01 | Section 9 追加行标识使用规则——Agent 看到行标识注释后如何锁定目标行并在行内操作 | Phase 68 `<!-- 行: {id} -->` 格式已锁定 |
| PROMPT-02 | Section 9 追加反重复规则——Agent 看到失败标注后应切换策略，不在同一元素重复尝试 | Phase 68 `<!-- 行内 input [已尝试 N 次 ...] -->` 格式已锁定 |
| PROMPT-03 | Section 9 追加策略优先级规则——Agent 遇到策略标注时优先使用策略 1，失败后按标注降级 | Phase 68 D-03 策略 1/2/3 命名已锁定 |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11 | Runtime | Project standard (pyproject.toml) |
| pytest | 8.0+ | Testing | Project test framework (pyproject.toml) |
| pytest-asyncio | 0.24+ | Async test support | auto mode configured in pyproject.toml |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| unittest.mock | stdlib | Mocking for unit tests | All step_callback integration tests |
| dataclasses | stdlib | Frozen dataclass patterns | Verifying FailureDetectionResult immutability |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| unittest.mock | pytest-mock | stdlib sufficient for this scope; no external dependency needed |

## Architecture Patterns

### Recommended Project Structure
```
backend/
  core/
    agent_service.py     # step_callback integration (modify)
  agent/
    prompts.py            # Section 9 prompt rules (modify)
    dom_patch.py          # update_failure_tracker / reset (reference only)
    stall_detector.py     # detect_failure_mode (reference only)
backend/tests/unit/
    test_agent_service.py # NEW: step_callback integration tests
    test_enhanced_prompt.py  # EXTEND: Section 9 content tests
```

### Pattern 1: step_callback Integration Point
**What:** Insert detect_failure_mode + update_failure_tracker calls in the detector calls region
**When to use:** Plan 69-01 implementation
**Example:**
```python
# agent_service.py step_callback, lines 302-337
# Insert AFTER stall_detector.check() block, BEFORE progress tracking
# Context: variables already available at this point:
#   - action_name (str)
#   - action_params (dict) with 'index' key = backend_node_id (int)
#   - evaluation (str)
#   - dom_hash (str, current step's hash)

# ... existing stall_detector.check() code ...

# --- Phase 69: Failure mode detection + tracker update (D-01/D-02/D-03) ---
try:
    failure_keywords = ('失败', 'wrong', 'error', '无法', '不成功', '未')
    if any(kw in evaluation.lower() for kw in failure_keywords):
        failure_result = agent._stall_detector.detect_failure_mode(
            action_name=action_name,
            target_index=action_params.get("index") if isinstance(action_params, dict) else None,
            evaluation=evaluation,
            dom_hash_before=_prev_dom_hash or "",
            dom_hash_after=dom_hash,
        )
        if failure_result.failure_mode is not None:
            from backend.agent.dom_patch import update_failure_tracker
            backend_node_id = str(action_params.get("index", ""))
            update_failure_tracker(
                backend_node_id=backend_node_id,
                error=failure_result.details.get("evaluation_snippet", evaluation[:100]),
                mode=failure_result.failure_mode,
            )
            run_logger.log("warning", "monitor", "Failure detected",
                           step=step, mode=failure_result.failure_mode)
except Exception as e:
    logger.error(f"[{run_id}][MONITOR] Failure detection error (non-blocking): {e}")

# Update previous dom_hash for next step (D-02)
_prev_dom_hash = dom_hash
```

### Pattern 2: Section 9 Rule Append
**What:** Append four subsections to Section 9 in prompts.py, after line 83
**When to use:** Plan 69-02 implementation
**Example:**
```python
# In prompts.py ENHANCED_SYSTEM_MESSAGE, after line 83 (the closing """)
# Each section follows D-05: "看到 X -> 做 Y" format, 2-4 lines per section
# Order per D-06: 行标识 -> 反重复 -> 策略优先级 -> 失败恢复

# Section 9.1: 行标识定位 (PROMPT-01)
# Maps to Phase 68 annotation: <!-- 行: I01784004409597 -->
# Tells Agent: see 行 comment -> lock target row -> operate within row

# Section 9.2: 反重复操作 (PROMPT-02)
# Maps to Phase 68 annotation: [已尝试 N 次 模式: click_no_effect]
# Tells Agent: see failure annotation -> switch strategy -> don't repeat

# Section 9.3: 策略优先级 (PROMPT-03)
# Maps to Phase 68 annotation: [策略: 1-原生 input] / [策略: 2-需先 click] / [策略: 3-evaluate JS]
# Tells Agent: use annotated strategy -> downgrade on failure

# Section 9.4: 失败恢复 (RECOV-03)
# Three failure modes: click_no_effect / wrong_column / edit_not_active
# Each with detection -> annotation -> switch operation flow
```

### Anti-Patterns to Avoid
- **Mutating _failure_tracker directly from step_callback:** Use `update_failure_tracker()` function, not direct dict manipulation
- **Importing update_failure_tracker at module level:** Import inside the try block or at function top — dom_patch may not be loaded yet at import time
- **Modifying monitored_agent.py create_step_callback():** Dead code per D-04, all work in agent_service.py inline callback
- **Adding verbose explanations in Section 9 rules:** D-05 mandates concise "看到 X -> 做 Y" style

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Failure mode detection | Custom keyword matching in step_callback | `StallDetector.detect_failure_mode()` | Already implemented in Phase 67, tested, returns structured FailureDetectionResult |
| Tracker state update | Direct dict manipulation | `update_failure_tracker()` | Handles count increment, last_error/mode update correctly |
| Tracker reset timing | Custom reset logic | `reset_failure_tracker()` in `apply_dom_patch()` | Already called on every run, independent of _PATCHED |
| Failure keyword regex | Custom string matching | `FAILURE_KEYWORDS` in stall_detector.py | Already compiled regex with Chinese/English keywords |

**Key insight:** Phase 69 is purely an integration phase. All detection and tracking logic is implemented and tested. The work is wiring calls and writing prompt text.

## Common Pitfalls

### Pitfall 1: index vs backend_node_id Confusion
**What goes wrong:** `action_params.get("index")` might be mistaken for a 0-based array index instead of the browser-use backend_node_id
**Why it happens:** Variable name "index" is misleading
**How to avoid:** browser-use v0.12.2 uses `backend_node_id` as the "index" parameter. The selector_map is keyed by `backend_node_id`. The value from `action_params.get("index")` IS the `backend_node_id` (int type).
**Warning signs:** `update_failure_tracker()` expects `str` type for backend_node_id, but `action_params.get("index")` returns `int`. Must convert: `str(action_params["index"])`.

### Pitfall 2: _prev_dom_hash Closure Variable Scope
**What goes wrong:** `_prev_dom_hash` defined inside step_callback resets on every callback invocation
**Why it happens:** step_callback is an inner function that closes over variables in `run_with_streaming()`
**How to avoid:** Define `_prev_dom_hash` as a mutable container (e.g., `{"value": None}`) in the outer scope (`run_with_streaming()` body, before step_callback definition), similar to `step_stats_data`. Update `_prev_dom_hash["value"]` at end of each step_callback invocation.
**Warning signs:** If `_prev_dom_hash` is defined as a simple variable inside step_callback, it will always be `None`.

### Pitfall 3: First-Step dom_hash_before Is Empty
**What goes wrong:** On step 1, `_prev_dom_hash` is None, causing detect_failure_mode to compare "" with actual hash
**Why it happens:** No previous step exists before the first step
**How to avoid:** D-03 gate (only call on failure keywords) plus early return when `_prev_dom_hash is None` ensures first step never triggers false click_no_effect detection. Alternatively, pass `_prev_dom_hash or ""` and rely on the keyword gate.
**Warning signs:** First step producing click_no_effect detection when evaluation contains a failure keyword.

### Pitfall 4: Prompt Rule Length Budget
**What goes wrong:** Section 9 grows too large, consuming LLM context window
**Why it happens:** Each section adds lines, and Section 9 is already 31 lines (lines 52-83)
**How to avoid:** D-05 mandates 2-4 lines per rule group, so 4 groups = 8-16 new lines. Total Section 9 stays under 50 lines. Test with `test_line_count_under_80` (existing test checks total prompt under 80 lines).
**Warning signs:** Total ENHANCED_SYSTEM_MESSAGE exceeds 80 lines after append.

### Pitfall 5: Import Cycle Risk
**What goes wrong:** Importing `update_failure_tracker` at module level in agent_service.py causes circular import
**Why it happens:** agent_service.py already imports from dom_patch (`apply_dom_patch`), but adding another import at module level could trigger initialization order issues
**How to avoid:** Use local import inside the try block: `from backend.agent.dom_patch import update_failure_tracker`. The existing `apply_dom_patch` import at module level is fine because it's a function reference, not a data dependency.
**Warning signs:** ImportError or ModuleNotFoundError at startup.

## Code Examples

### Example 1: Closure Variable Pattern (from existing code)
```python
# agent_service.py line 173 -- existing pattern for mutable closure state
step_stats_data = {"value": None}  # Mutable container for step stats (Phase 41, LOG-02)

# Phase 69 should follow this pattern:
_prev_dom_hash_data = {"value": None}  # Mutable container for previous step dom_hash
```

### Example 2: detect_failure_mode Return Structure
```python
# From stall_detector.py lines 162-221 -- already implemented, never called
# Returns FailureDetectionResult(frozen=True):
#   failure_mode: str | None  -- "click_no_effect" | "wrong_column" | "edit_not_active" | None
#   details: dict  -- {"keywords_matched": [...], "evaluation_snippet": ..., "target_index": ..., "dom_hash": ...}
```

### Example 3: update_failure_tracker Signature
```python
# From dom_patch.py lines 168-186 -- already implemented, never called
def update_failure_tracker(backend_node_id: str, error: str, mode: str) -> None:
    # _failure_tracker uses str keys (line 41: dict[str, dict] = {})
    # action_params["index"] returns int -- MUST convert to str
```

### Example 4: Existing Section 9 Format (lines 52-83)
```python
# prompts.py -- current Section 9 structure for reference
"""## 9. ERP 表格单元格填写
销售出库等页面的表格中，每个商品行有多个可编辑单元格（销售金额、物流费用等）。
...
**单元格定位：**
- 用 placeholder 精确匹配目标输入框：...
...
**禁止行为：**
- 不要点击 `<td>` 本身（td 元素不是交互元素，会误命中）
...
**evaluate JS fallback：**
- 如果标准 input action 失败，可用 ...
...
**点击编辑工作流（关键）：**
...
"""
# New rules append AFTER line 83, BEFORE the closing triple-quote
```

### Example 5: Phase 68 Annotation Formats (what Agent sees in DOM dump)
```html
<!-- Row identity: -->
<!-- 行: I01784004409597 -->

<!-- Failure + strategy annotation (only on failed ERP inputs): -->
<!-- 行内 input [行: I01784004409597] [策略: 2-需先 click] [已尝试 2 次 模式: click_no_effect] -->
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| No failure tracking | _failure_tracker dict keyed by backend_node_id | Phase 67 | Tracking state exists but inert |
| No failure mode detection | detect_failure_mode() with 3 modes | Phase 67 | Detection logic exists but inert |
| No DOM annotations | serialize_tree patches for row identity + failure | Phase 68 | Annotations exist but tracker never populated |
| Manual retry in prompt only | Prompt rules + automated detection/annotation | Phase 69 | Full detection->tracking->annotation->prompt loop |

**Deprecated/outdated:**
- monitored_agent.py create_step_callback(): dead code, not used by agent_service.py which has its own inline callback

## Open Questions

1. **backend_node_id Stability Across Steps**
   - What we know: STATE.md flags this as a blocker concern. Phase 67/68 assumed stable. browser-use's EnhancedDOMTreeNode has `compute_stable_hash()` suggesting awareness of potential instability.
   - What's unclear: Whether backend_node_id changes for the same visible element across DOM rebuilds.
   - Recommendation: Implement with backend_node_id as planned. If instability surfaces in testing, Phase 69 integration tests will catch it (tracker won't match). Fallback: use `compute_stable_hash()` or `(tag_name, placeholder, row_identity)` composite key.

2. **Evaluation Keyword Gate Precision**
   - What we know: D-03 specifies keywords '失败'/'wrong'/'error'/'无法'/'不成功'/'未'. StallDetector already has `FAILURE_KEYWORDS` regex with broader set.
   - What's unclear: Whether '未' alone causes false positives (e.g., "已完成" = completed, not failed).
   - Recommendation: Use '未成功' instead of bare '未' to avoid false positives. This is Claude's discretion per CONTEXT.md.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.11 | Runtime | True | 3.11.x | -- |
| pytest | Testing | True | 8.0+ | -- |
| pytest-asyncio | Testing | True | 0.24+ | -- |
| browser-use 0.12.2 | Runtime | True | 0.12.2 | -- |

**Missing dependencies with no fallback:**
- None

**Missing dependencies with fallback:**
- None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ with pytest-asyncio 0.24+ |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/unit/test_agent_service.py -x -q` |
| Full suite command | `uv run pytest backend/tests/unit/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ANTI-03 | update_failure_tracker called with correct args on failure | unit | `uv run pytest backend/tests/unit/test_agent_service.py::test_step_callback_updates_failure_tracker -x` | No -- Wave 0 |
| ANTI-03 | update_failure_tracker NOT called when no failure detected | unit | `uv run pytest backend/tests/unit/test_agent_service.py::test_step_callback_no_update_on_success -x` | No -- Wave 0 |
| RECOV-02 | detect_failure_mode called with correct dom_hash before/after | unit | `uv run pytest backend/tests/unit/test_agent_service.py::test_step_callback_calls_detect_failure_mode -x` | No -- Wave 0 |
| RECOV-02 | All three failure modes (click_no_effect/wrong_column/edit_not_active) correctly written | unit | `uv run pytest backend/tests/unit/test_agent_service.py::test_three_failure_modes -x` | No -- Wave 0 |
| PROMPT-01 | Section 9 contains row identity usage rules | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::test_contains_row_identity_rules -x` | No -- Wave 0 |
| PROMPT-02 | Section 9 contains anti-repeat rules | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::test_contains_anti_repeat_rules -x` | No -- Wave 0 |
| PROMPT-03 | Section 9 contains strategy priority rules | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::test_contains_strategy_priority_rules -x` | No -- Wave 0 |
| RECOV-03 | Section 9 contains failure recovery rules for 3 modes | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::test_contains_failure_recovery_rules -x` | No -- Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_agent_service.py backend/tests/unit/test_enhanced_prompt.py -x -q`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** Full unit test suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_agent_service.py` -- covers ANTI-03, RECOV-02 step_callback integration tests (file exists but needs Phase 69 specific test class)
- [ ] `backend/tests/unit/test_enhanced_prompt.py` -- extend with PROMPT-01/02/03, RECOV-03 keyword assertions (file exists with existing tests, needs new test methods)
- [ ] No new framework install needed -- existing pytest infrastructure sufficient

## Sources

### Primary (HIGH confidence)
- `backend/core/agent_service.py` -- step_callback inline definition (lines 175-346), detector calls region (lines 302-337)
- `backend/agent/prompts.py` -- ENHANCED_SYSTEM_MESSAGE (lines 9-83), Section 9 (lines 52-83)
- `backend/agent/dom_patch.py` -- update_failure_tracker (lines 168-186), _failure_tracker (line 41), _node_annotations (line 46), serialize_tree patches (lines 487-556)
- `backend/agent/stall_detector.py` -- detect_failure_mode (lines 162-221), FailureDetectionResult (lines 39-49), FAILURE_KEYWORDS (line 14)
- `browser_use/dom/views.py` -- DOMSelectorMap type alias (line 913), EnhancedDOMTreeNode.backend_node_id field

### Secondary (MEDIUM confidence)
- `browser_use/agent/views.py` -- get_interacted_element confirms selector_map keyed by index=backend_node_id (lines 499-508)
- `browser_use/dom/serializer/serializer.py` -- _selector_map uses backend_node_id as key (line 713)
- Phase 68 CONTEXT.md -- annotation format decisions D-02/D-03/D-04

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Python standard library + existing project deps, verified in pyproject.toml
- Architecture: HIGH -- step_callback structure, selector_map mapping, and prompt format all verified from source code
- Pitfalls: HIGH -- index/backend_node_id type mapping verified from browser-use source; closure variable pattern verified from existing agent_service.py code

**Research date:** 2026-04-07
**Valid until:** 2026-05-07 (stable codebase, no external deps)
