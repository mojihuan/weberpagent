# Phase 68: DOM Patch 增强 — 行标识注入与策略标注 - Research

**Researched:** 2026-04-07
**Domain:** browser-use DOM serialization monkey-patching, HTML comment injection, strategy annotation
**Confidence:** HIGH

## Summary

Phase 68 在 `dom_patch.py` 中新增三个能力：(1) Patch 4 增强 -- 在 index 分配阶段为 ERP 表格行内 input 判定行归属和策略层级；(2) Patch 6 -- 在 DOM dump 序列化输出中注入行标识注释 `<!-- 行: {id} -->`；(3) Patch 7 -- 在 DOM dump 中为已失败元素注入策略降级和失败模式标注。

核心发现是 **SimplifiedNode 使用 `@dataclass(slots=True)`，无法动态设置属性**（如 `node._row_identity = "I..."`）。这意味着 CONTEXT.md D-01 中"在 Patch 4 wrapper 中为 input 元素设置内部属性"的方案需要调整为使用模块级 sidecar 字典（如 `_node_annotations: dict[int, dict]`），以 backend_node_id 为键存储行归属和策略层级，Patch 6/7 在序列化时读取此字典。

DOM dump 文本的生成入口是 `DOMTreeSerializer.serialize_tree()` -- 一个 `@staticmethod`，被 `SerializedDOMState.llm_representation()` 调用。Patch 6 和 Patch 7 都需要 monkey-patch 这个静态方法，在输出文本中进行注释注入。

**Primary recommendation:** 使用模块级 sidecar 字典存储标注数据，Patch 4 增强填充此字典，Patch 6/7 包裹 `serialize_tree()` 在序列化输出中注入 HTML 注释。三个 patch 在 `apply_dom_patch()` 中按 Patch 4 -> Patch 6 -> Patch 7 的顺序注册。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 两阶段注入：(1) 树构建阶段在 Patch 4 wrapper 中为 input 元素设置内部属性（行归属、策略层级），(2) 新增 Patch 包裹序列化输出方法，在生成 DOM dump 文本时注入 HTML 注释
- **D-02:** 统一使用 HTML 注释格式 -- 行标识注释 `<!-- 行: {id} -->`、行归属+策略 `<!-- 行内 input [行: {id}] [策略: 2-需先 click] -->`、失败标注 `<!-- 已尝试 2 次 [模式: click_no_effect]，建议切换策略 -->`
- **D-03:** 描述性策略命名：策略1-原生 input / 策略2-需先 click / 策略3-evaluate JS
- **D-04:** 策略标注和失败标注只在已失败元素上显示。行标识注释对所有含商品编号的行都显示
- **D-05:** 假设 backend_node_id 跨 step 稳定，不做复合键回退

### Claude's Discretion
- Patch 4 wrapper 的具体扩展方式（如何存储行归属和策略层级）
- 序列化方法包裹的具体实现（哪个方法、注入位置）
- 策略判定的具体条件（snapshot_node 存在性检查的具体属性名）
- Patch 6 和 Patch 7 的注册顺序和依赖关系
- 单元测试的 mock 数据设计

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ROW-02 | DOM dump 序列化输出中为含商品编号的行注入 `<!-- 行: {id} -->` 注释 | Patch 6 包裹 `serialize_tree()`，检测含 IMEI 的 `<tr>` 节点并在其输出文本前插入注释 |
| ROW-03 | Patch 4 为行内 input 添加行归属标注 | Patch 4 增强调用 `_detect_row_identity()` 获取行标识，存入 sidecar 字典，Patch 7 在序列化时读取并注入 |
| STRAT-01 | 三级策略判定 -- 可见 input 为策略1，hidden input 为策略2，失败降级为策略3 | Patch 4 增强：`snapshot_node` 存在 + `is_visible` -> 策略1；`snapshot_node` 缺失 -> 策略2；`_failure_tracker` count >= 2 -> 策略3 |
| STRAT-02 | 序列化后处理阶段注入策略注释，只在已失败元素上标注 | Patch 7 包裹 `serialize_tree()`，检查 sidecar 字典和 `_failure_tracker`，仅为失败元素注入 |
| STRAT-03 | 策略自动降级 -- 策略1失败2次降级为策略2，策略2失败2次降级为策略3 | Patch 4 增强根据 `_failure_tracker` count 判定降级后的策略层级，存入 sidecar 字典 |
| ANTI-02 | DOM Patch 根据失败追踪器为失败元素动态注入标注，且只在已失败元素上标注 | Patch 7 读取 `_failure_tracker`，检查 `backend_node_id` 是否有记录，有则注入失败模式标注 |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11 | Runtime | Project standard |
| browser-use | 0.12.2 | DOM serialization pipeline being patched | Existing dependency |
| pytest | 8.0+ | Unit testing | Project standard |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| unittest.mock | stdlib | Mocking browser-use classes | All unit tests |
| re | stdlib | IMEI regex pattern | Row identity detection |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| sidecar dict | Monkey-patch SimplifiedNode to add __dict__ | sidecar dict is simpler and doesn't modify browser-use internals |
| Post-process serialize_tree output text | Intercept during tree traversal | Post-process is cleaner separation of concerns |

**Installation:** No new packages required. All changes use existing dependencies.

**Version verification:** Existing project dependencies, no new installs needed.

## Architecture Patterns

### Recommended Project Structure
```
backend/agent/
├── dom_patch.py          # ALL Phase 68 changes go here (Patch 4 enhance + Patch 6 + Patch 7)
└── stall_detector.py     # No changes in Phase 68 (Phase 67 complete, Phase 69 integration)

backend/tests/unit/
├── test_dom_patch_phase67.py  # Existing Phase 67 tests (reference pattern)
└── test_dom_patch_phase68.py  # New Phase 68 tests
```

### Pattern 1: Sidecar Dictionary for Node Annotations (CRITICAL)
**What:** Since `SimplifiedNode` uses `@dataclass(slots=True)`, dynamic attributes like `node._row_identity` are impossible. Use a module-level dictionary keyed by `backend_node_id` to store annotations.
**When to use:** Whenever Phase 68 needs to attach metadata to SimplifiedNode instances during Patch 4 processing and read it during serialization.
**Example:**
```python
# Module-level sidecar dict
_node_annotations: dict[int, dict] = {}
# Key: backend_node_id, Value: {"row_identity": str|None, "strategy_level": int, ...}

def _reset_node_annotations() -> None:
    """Clear annotations. Called alongside reset_failure_tracker()."""
    global _node_annotations
    _node_annotations = {}
```

### Pattern 2: Monkey-patch serialize_tree for Text Injection
**What:** `DOMTreeSerializer.serialize_tree()` is a `@staticmethod` that generates the DOM dump text. Patch it to inject HTML comments at specific positions in the output.
**When to use:** Patch 6 (row identity comments) and Patch 7 (failure/strategy annotations) both need this.
**Example:**
```python
def _patch_serialize_tree_for_row_identity() -> None:
    """Patch 6: Wrap serialize_tree to inject <!-- 行: {id} --> comments."""
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    original_serialize = DOMTreeSerializer.serialize_tree

    @staticmethod
    def patched_serialize(node, include_attributes, depth=0) -> str:
        result = original_serialize(node, include_attributes, depth)
        if not result:
            return result
        # Check if node is a <tr> with row identity
        backend_node_id = getattr(getattr(node, 'original_node', None), 'backend_node_id', None)
        if backend_node_id and backend_node_id in _node_annotations:
            ann = _node_annotations[backend_node_id]
            if ann.get('row_identity'):
                depth_str = depth * '\t'
                return f'{depth_str}<!-- 行: {ann["row_identity"]} -->\n{result}'
        return result

    DOMTreeSerializer.serialize_tree = patched_serialize
```

### Pattern 3: Strategy Level Determination in Patch 4
**What:** During `_assign_interactive_indices_and_mark_new_nodes`, determine strategy level for ERP inputs based on visibility and failure history.
**When to use:** Patch 4 enhanced wrapper.
**Example:**
```python
# Inside patched_method, after forcing interactive for ERP input:
row_identity = _detect_row_identity(node)

# Strategy determination
snapshot_node = getattr(node.original_node, 'snapshot_node', None)
is_visible = getattr(node.original_node, 'is_visible', False)
backend_node_id = node.original_node.backend_node_id

if backend_node_id in _failure_tracker:
    count = _failure_tracker[backend_node_id]['count']
    if count >= 4:  # Total failures >= 4 means all strategies exhausted
        strategy_level = 3
    elif count >= 2:
        strategy_level = 3 if not snapshot_node else 2
    else:
        strategy_level = 2 if not snapshot_node else 1
else:
    strategy_level = 2 if not snapshot_node else 1

_node_annotations[backend_node_id] = {
    'row_identity': row_identity,
    'strategy_level': strategy_level,
}
```

### Pattern 4: Selective Annotation Injection (Patch 7)
**What:** Only inject strategy/failure annotations for elements that appear in `_failure_tracker`. This is D-04's core requirement.
**When to use:** Patch 7 wrapping of `serialize_tree()`.
**Example:**
```python
# Inside Patch 7's serialize_tree wrapper:
backend_node_id = getattr(getattr(node, 'original_node', None), 'backend_node_id', None)

# Only annotate elements in _failure_tracker (D-04)
if backend_node_id and backend_node_id in _failure_tracker:
    failure = _failure_tracker[backend_node_id]
    ann = _node_annotations.get(backend_node_id, {})
    row_identity = ann.get('row_identity')
    strategy_level = ann.get('strategy_level', 1)

    STRATEGY_NAMES = {1: "1-原生 input", 2: "2-需先 click", 3: "3-evaluate JS"}
    parts = []
    if row_identity:
        parts.append(f"[行: {row_identity}]")
    parts.append(f"[策略: {STRATEGY_NAMES.get(strategy_level, '?')}]")
    parts.append(f"[已尝试 {failure['count']} 次 模式: {failure['mode']}]")

    comment = f'<!-- 行内 input {" ".join(parts)} -->'
    result = result + '\n' + depth_str + comment
```

### Anti-Patterns to Avoid
- **Setting attributes on SimplifiedNode:** `node._row_identity = "I..."` will raise `AttributeError` due to `slots=True`. Use sidecar dict instead.
- **Multiple layers of serialize_tree wrapping:** Patch 6 and Patch 7 both wrap `serialize_tree`. If wrapped sequentially, each call goes through two wrappers. This is acceptable but the inner call must be to the *original* method, not to each other. Register Patch 7 first (outer wrapper), then Patch 6 (inner wrapper), so Patch 6's row identity comments are added before Patch 7's failure annotations in the output. Actually, the simplest approach is to combine both into a single wrapper to avoid multi-layer wrapping entirely.
- **Annotating all elements with strategy:** D-04 explicitly requires strategy/failure annotations ONLY on failed elements. Annotating every input would bias the Agent toward evaluate JS.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Row identity detection | New regex/traversal | `_detect_row_identity(node)` (Phase 67) | Already implemented and tested |
| Failure state management | New tracking dict | `_failure_tracker` + `update_failure_tracker()` (Phase 67) | Already implemented and tested |
| ERP input detection | New tag/placeholder check | `_is_erp_table_cell_input(node)` (existing) | Already handles td parent + input tag + placeholder matching |
| Table cell traversal | New parent chain walk | `_is_inside_table_cell(node)` (existing) | Already handles td/th parent chain walking |

**Key insight:** Phase 67 already built the foundation. Phase 68 is purely about *consuming* that foundation (reading `_failure_tracker`, calling `_detect_row_identity()`) and injecting annotations into the DOM dump text output.

## Common Pitfalls

### Pitfall 1: SimplifiedNode slots=True blocks dynamic attributes
**What goes wrong:** Attempting `node._row_identity = "I..."` raises `AttributeError: 'SimplifiedNode' object has no attribute '_row_identity' and has no __dict__ for setting new attributes`
**Why it happens:** `SimplifiedNode` is defined as `@dataclass(slots=True)` in browser_use/dom/views.py line 218. Slots prevent dynamic attribute creation.
**How to avoid:** Use module-level sidecar dictionary `_node_annotations: dict[int, dict]` keyed by `backend_node_id`. Reset alongside `_failure_tracker` in `reset_failure_tracker()`.
**Warning signs:** `AttributeError` at runtime when Patch 4 tries to set custom attributes.

### Pitfall 2: serialize_tree is a @staticmethod
**What goes wrong:** Treating `serialize_tree` as an instance method when wrapping it, or not preserving the `@staticmethod` decorator on the replacement.
**Why it happens:** `serialize_tree` is defined as `@staticmethod` on `DOMTreeSerializer` (line 883 of serializer.py). It's called as `DOMTreeSerializer.serialize_tree(...)` from `SerializedDOMState.llm_representation()`.
**How to avoid:** Ensure the patched version is also a `@staticmethod`. The wrapping pattern should be: save original static method, create new static method that calls original, assign back to class.
**Warning signs:** `TypeError` about missing self/cls argument.

### Pitfall 3: backend_node_id type mismatch (int vs str)
**What goes wrong:** `_failure_tracker` keys are strings (set by `update_failure_tracker(backend_node_id: str, ...)`), but `_selector_map` keys and `node.original_node.backend_node_id` are integers.
**Why it happens:** Phase 67 defined `update_failure_tracker(backend_node_id: str, ...)` with str type. The `backend_node_id` field on `EnhancedDOMTreeNode` is `int`.
**How to avoid:** When looking up `_failure_tracker` during Patch 4/7, convert `backend_node_id` to string: `_failure_tracker.get(str(node.original_node.backend_node_id))`. Similarly, `_node_annotations` should use consistent key type (recommend int to match `backend_node_id` field).
**Warning signs:** Annotations never appear in DOM dump because key type mismatch causes lookup to always return None.

### Pitfall 4: Multi-layer serialize_tree wrapping chain
**What goes wrong:** If Patch 6 wraps serialize_tree, then Patch 7 wraps the *already-wrapped* serialize_tree, you get a chain: Patch 7 -> Patch 6 -> original. Each call goes through two wrapper layers, and Patch 7 cannot see the annotations that Patch 6 added to the text.
**Why it happens:** Sequential monkey-patching of the same method creates a chain.
**How to avoid:** Combine Patch 6 and Patch 7 into a SINGLE `serialize_tree` wrapper that handles both row identity comments AND failure annotations. This is consistent with D-01's "不产生多层 wrapping 链" requirement. The single wrapper first calls original `serialize_tree`, then post-processes the text to inject both types of comments.
**Warning signs:** Row identity comments appear but failure annotations don't, or annotations are in wrong positions.

### Pitfall 5: Annotation injection position in multi-line output
**What goes wrong:** `serialize_tree` returns multi-line text for elements with children. Injecting a comment after the full text puts it AFTER all children, not after the opening tag.
**Why it happens:** A `<tr>` with children produces text like `<tr ...>\n\t<td>...</td>\n\t<td>...</td>`. Adding a comment at the end puts it after the last child, not after the `<tr>` tag itself.
**How to avoid:** Row identity comments (`<!-- 行: {id} -->`) should be prepended BEFORE the element's text (so they appear above the `<tr>` line). Strategy/failure annotations should be appended as a separate line after the element's line (for input elements which are self-closing `<input ... />`). Use `result.split('\n', 1)` to separate first line from children for precise injection.
**Warning signs:** Comments appear in wrong positions in DOM dump, confusing the Agent.

### Pitfall 6: Strategy level should reflect CURRENT state, not initial
**What goes wrong:** Computing strategy level once during Patch 4 and never updating it. If failure count increases between steps, strategy level should reflect the new count.
**Why it happens:** Patch 4 runs during `serialize_accessible_elements()`, but `_failure_tracker` is updated by `step_callback` (Phase 69). Between steps, the tracker may have new entries.
**How to avoid:** Strategy level is computed fresh each time `serialize_tree` runs (via Patch 7 reading `_failure_tracker` live), not stored statically from Patch 4. Patch 4 stores the base strategy (based on visibility) in sidecar dict; Patch 7 applies the failure-based override.
**Warning signs:** Strategy annotation shows "策略1" even after 2+ failures on that element.

## Code Examples

### Example 1: Patch 4 Enhancement -- Row Identity + Base Strategy
```python
# Inside the existing _patch_assign_interactive_indices() wrapper
# After the existing "Force interactive assignment" block:

# --- Phase 68: Row identity + strategy base ---
row_identity = _detect_row_identity(node)
backend_node_id = node.original_node.backend_node_id
snapshot_node = getattr(node.original_node, 'snapshot_node', None)

# Base strategy from visibility (failure override applied in Patch 7)
base_strategy = 1 if snapshot_node else 2

_node_annotations[backend_node_id] = {
    'row_identity': row_identity,
    'base_strategy': base_strategy,
    'is_erp_input': True,
}
```

### Example 2: Combined Patch 6+7 -- serialize_tree Wrapper
```python
def _patch_serialize_tree_annotations() -> None:
    """Patch 6+7: Inject row identity comments and failure annotations."""
    from browser_use.dom.serializer.serializer import DOMTreeSerializer

    original_serialize = DOMTreeSerializer.serialize_tree

    @staticmethod
    def patched_serialize(node, include_attributes, depth=0) -> str:
        result = original_serialize(node, include_attributes, depth)
        if not result:
            return result

        orig = getattr(node, 'original_node', None)
        if orig is None:
            return result

        backend_id = getattr(orig, 'backend_node_id', None)
        if backend_id is None:
            return result

        ann = _node_annotations.get(backend_id, {})
        depth_str = depth * '\t'
        lines = []

        # Patch 6: Row identity comment (for <tr> with IMEI)
        row_id = ann.get('row_identity')
        if row_id:
            tag = getattr(orig, 'tag_name', '').lower()
            if tag == 'tr':
                lines.append(f'{depth_str}<!-- 行: {row_id} -->')

        lines.append(result)

        # Patch 7: Failure + strategy annotation (only for failed ERP inputs)
        if ann.get('is_erp_input') and str(backend_id) in _failure_tracker:
            failure = _failure_tracker[str(backend_id)]
            base_strategy = ann.get('base_strategy', 1)
            # Apply failure-based downgrade
            count = failure['count']
            if base_strategy == 1 and count >= 2:
                current_strategy = 2
            elif base_strategy == 2 and count >= 2:
                current_strategy = 3
            else:
                current_strategy = base_strategy

            STRATEGY_NAMES = {1: "1-原生 input", 2: "2-需先 click", 3: "3-evaluate JS"}
            parts = []
            if row_id:
                parts.append(f"[行: {row_id}]")
            parts.append(f"[策略: {STRATEGY_NAMES[current_strategy]}]")
            parts.append(f"[已尝试 {count} 次 模式: {failure['mode']}]")
            lines.append(f'{depth_str}<!-- 行内 input {" ".join(parts)} -->')

        return '\n'.join(lines)

    DOMTreeSerializer.serialize_tree = patched_serialize
```

### Example 3: Registration in apply_dom_patch()
```python
def apply_dom_patch() -> None:
    global _PATCHED
    if _PATCHED:
        reset_failure_tracker()
        _reset_node_annotations()  # NEW: reset annotations too
        logger.debug("dom_patch: already applied, skipping")
        return

    try:
        _patch_is_interactive()
        _patch_paint_order_remover()
        _patch_should_exclude_child()
        _patch_assign_interactive_indices()  # Enhanced by Phase 68
        _patch_serialize_tree_annotations()  # NEW: Patch 6+7 combined
        _PATCHED = True
        logger.info("dom_patch: successfully applied all patches (including Phase 68)")
    except Exception as exc:
        logger.error("dom_patch: failed to apply: %s", exc)
        raise
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Separate Patch 6 + Patch 7 wrappers | Single combined wrapper for serialize_tree | Phase 68 design | Avoids multi-layer wrapping chain (D-01 constraint) |
| Setting node attributes for annotations | Sidecar dictionary keyed by backend_node_id | Phase 68 research | Required because SimplifiedNode uses slots=True |

**Deprecated/outdated:**
- CONTEXT.md D-01 mentions "设置 node._row_identity 和 node._strategy_level 等临时属性" -- this is NOT possible due to `slots=True`. Must use sidecar dict instead.

## Open Questions

1. **Row identity for non-input nodes**
   - What we know: `_detect_row_identity()` works from any node inside a `<tr>`. Patch 4 only processes ERP inputs. For Patch 6's row identity comments on `<tr>` elements, we need a separate mechanism.
   - What's unclear: Should Patch 6 detect row identity independently during `serialize_tree`, or should we also populate `_node_annotations` for `<tr>` nodes during an earlier phase?
   - Recommendation: The simplest approach is to have Patch 6 call `_detect_row_identity()` directly during `serialize_tree` for `<tr>` elements, without depending on `_node_annotations`. The sidecar dict is only needed for ERP inputs processed in Patch 4.

2. **`serialize_tree` recursion depth impact**
   - What we know: `serialize_tree` is called recursively for every node in the tree. Adding annotation lookups at every node adds overhead.
   - What's unclear: Whether the performance impact is negligible or noticeable.
   - Recommendation: Early-return for non-relevant nodes (no original_node, backend_node_id not in annotations/tracker). The lookup cost is O(1) dict access.

3. **`<tr>` row identity detection in serialize_tree**
   - What we know: In `serialize_tree`, the `SimplifiedNode` for a `<tr>` has `original_node` which is an `EnhancedDOMTreeNode` with `tag_name`, `children`, etc. We can call `_detect_row_identity()` on these nodes.
   - What's unclear: Whether `serialize_tree` is called for `<tr>` nodes or if they're collapsed/optimized out.
   - Recommendation: Test this -- `<tr>` elements may be visible in the tree depending on whether they pass the visibility filter. If `<tr>` is in the tree, `_detect_row_identity()` can be called directly.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies identified -- Phase 68 is pure Python code changes to existing files with existing test infrastructure).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py -v -x` |
| Full suite command | `uv run pytest backend/tests/unit/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ROW-02 | Row identity comment injected for `<tr>` with IMEI | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestRowIdentityComment -v` | Wave 0 |
| ROW-03 | ERP input annotated with row identity | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestRowBelongingAnnotation -v` | Wave 0 |
| STRAT-01 | Strategy level 1 for visible input, 2 for hidden, 3 after failures | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestStrategyDetermination -v` | Wave 0 |
| STRAT-02 | Strategy annotation only on failed elements in serialize output | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestStrategyAnnotation -v` | Wave 0 |
| STRAT-03 | Strategy auto-downgrade on failure count >= 2 | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestStrategyDowngrade -v` | Wave 0 |
| ANTI-02 | Failure mode annotation injected for tracked elements only | unit | `uv run pytest backend/tests/unit/test_dom_patch_phase68.py::TestFailureAnnotation -v` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_dom_patch_phase68.py -v -x`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** `uv run pytest backend/tests/ -v` full suite green before verify

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_dom_patch_phase68.py` -- covers ROW-02, ROW-03, STRAT-01, STRAT-02, STRAT-03, ANTI-02
- [ ] Test mock for `serialize_tree` output -- need to mock the original static method and verify annotation injection in the text output

## Sources

### Primary (HIGH confidence)
- `browser_use/dom/serializer/serializer.py` -- DOMTreeSerializer.serialize_tree (line 883-1085), _assign_interactive_indices_and_mark_new_nodes (line 617-727)
- `browser_use/dom/views.py` -- SimplifiedNode definition (line 218, slots=True confirmed), SerializedDOMState.llm_representation (line 936-949)
- `backend/agent/dom_patch.py` -- Full current implementation with Phase 67 additions
- `.planning/phases/68-dom-patch/68-CONTEXT.md` -- User decisions D-01 through D-05

### Secondary (MEDIUM confidence)
- `backend/tests/unit/test_dom_patch_phase67.py` -- Test pattern reference (mock patterns for MockAccessibilityNode, MockSimplifiedNode)
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` -- Original design document for all four optimizations
- `.planning/phases/67-基础层-行标识检测与失败追踪状态/67-CONTEXT.md` -- Phase 67 design decisions and integration points

### Tertiary (LOW confidence)
- None -- all findings verified against source code

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new dependencies, verified against existing code
- Architecture: HIGH - sidecar dict pattern verified against SimplifiedNode(slots=True) constraint
- Pitfalls: HIGH - SimplifiedNode slots=True confirmed by source code inspection and runtime test
- Annotation injection: HIGH - serialize_tree @staticmethod verified, patching pattern established by existing patches

**Research date:** 2026-04-07
**Valid until:** 2026-05-07 (stable - no dependency changes expected)
