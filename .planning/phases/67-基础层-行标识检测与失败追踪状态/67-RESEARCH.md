# Phase 67 Research: 基础层 — 行标识检测与失败追踪状态

**Researched:** 2026-04-07
**Status:** Complete

## Research Summary

Phase 67 需要在 `dom_patch.py` 和 `stall_detector.py` 中建立三项基础能力。研究结论：现有代码模式成熟，可直接复用，实施风险低。

---

## 1. _detect_row_identity() 实现

### 现有可复用模式

- `_is_textual_td_cell()` (dom_patch.py:37-81) — 已实现 td 文本检测：通过 `original_node.get_all_children_text()` 获取子节点文本，通过 `original_node.parent_node` 遍历父级
- `_is_inside_table_cell()` (dom_patch.py:114-132) — 已实现 td/th 父级遍历模式

### 实现策略

新函数 `_detect_row_identity(node)` 应：
1. 接收 SimplifiedNode（与 `_is_textual_td_cell` 参数一致）
2. 获取 `original_node.parent_node` 找到 `<tr>` 父级
3. 遍历 `<tr>` 的子节点（而非 parent_node 链），收集所有 `<td>` 的 `get_all_children_text()`
4. 对文本应用正则 `I\d{15}` 匹配，返回第一个匹配的字符串
5. 返回 `str | None`

### 关键发现

- `get_all_children_text()` 是 AccessibilityNode 的方法，返回所有 TEXT_NODE 后代的递归文本拼接
- `<tr>` 的子 `<td>` 遍历需要通过 AccessibilityNode 的子节点 API — 需确认 AccessibilityNode 是否有 `children` 属性或需通过其他方式获取子节点
- 正则 `I\d{15}` 对应 IMEI 格式（如 `I352017041234567`），从 CONTEXT.md specifics 确认

### 风险点

- AccessibilityNode 子节点遍历 API 可能不同于 SimplifiedNode — 需在实现时确认具体 API
- 解决方案：参考 `_is_textual_td_cell` 已成功使用 `original_node.parent_node` 的模式，`<tr>` 的子节点遍历同理使用 AccessibilityNode 的 `children` 属性

## 2. _failure_tracker 状态管理

### 现有模式参考

- `_PATCHED` (dom_patch.py:14) — 模块级布尔变量，通过 `global` 声明在函数内修改
- `apply_dom_patch()` 使用 `global _PATCHED` 修改模块状态

### 实现策略

```python
# 模块级状态
_failure_tracker: dict[str, dict] = {}

def update_failure_tracker(backend_node_id: str, error: str, mode: str) -> None:
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
    global _failure_tracker
    _failure_tracker = {}
```

### 关键决策点

- **键策略** (D-01): 使用 `backend_node_id`（字符串），与 browser-use `_selector_map` 一致
- **reset 时机**: `reset_failure_tracker()` 在 `apply_dom_patch()` 中被调用，但独立于 `_PATCHED` 幂等保护 — 即每次 run 都重置，即使 patch 已应用
- **实现方式**: 在 `apply_dom_patch()` 中 `if _PATCHED:` 分支后添加 `reset_failure_tracker()` 调用

### 集成点

agent_service.py:357 处 `apply_dom_patch()` 调用点 — 每次 run 开始时调用。reset_failure_tracker 应在此函数内部被调用，确保 tracker 每次 run 清空。

## 3. FailureDetectionResult + detect_failure_mode()

### 现有模式参考

- `StallResult` (stall_detector.py:20-23) — `frozen=True` dataclass，包含 `should_intervene: bool` 和 `message: str`
- `_StepRecord` (stall_detector.py:28-34) — 内部状态 dataclass（非 frozen）
- `StallDetector` (stall_detector.py:38-51) — 主检测器 dataclass，包含 `check()` 方法

### 实现策略

新增 frozen dataclass：
```python
@dataclass(frozen=True)
class FailureDetectionResult:
    failure_mode: str | None  # None = 无失败
    details: dict             # 诊断信息
```

新增方法到 StallDetector：
```python
def detect_failure_mode(
    self,
    action_name: str,
    target_index: int | None,
    evaluation: str,
    dom_hash_before: str,
    dom_hash_after: str,
) -> FailureDetectionResult:
```

### 三种失败模式检测逻辑

| 模式 | 检测条件 | details 内容 |
|------|---------|-------------|
| `click_no_effect` | `action_name == "click"` 且 `dom_hash_before == dom_hash_after` | `{"target_index": N, "dom_hash": "..."}` |
| `wrong_column` | evaluation 包含 `"wrong column"` / `"错误列"` / `"误点"` / `"非目标列"` | `{"keywords_matched": [...], "evaluation_snippet": "..."}` |
| `edit_not_active` | `action_name == "input"` 且 evaluation 包含 `"not editable"` / `"无法输入"` / `"元素不可操作"` | `{"target_index": N, "evaluation_snippet": "..."}` |

### 关键词列表设计

```python
_WRONG_COLUMN_KEYWORDS = re.compile(
    r"wrong.?column|错误列|误点|非目标列|clicked.*wrong",
    re.IGNORECASE,
)

_EDIT_NOT_ACTIVE_KEYWORDS = re.compile(
    r"not.?editable|无法输入|元素不可操作|cannot.?type|not.?interactable",
    re.IGNORECASE,
)
```

### 与现有 StallDetector 的关系

- `check()` 保持不变 — 检测停滞（连续失败 + DOM 停滞）
- `detect_failure_mode()` 新增独立方法 — 检测失败模式（三种具体 ERP 表格失败）
- 两个方法平级，step_callback 先调 `check()` 再调 `detect_failure_mode()`
- `detect_failure_mode()` 可以复用 `_history` 中的 `_StepRecord`（已存储 action_name, target_index, evaluation, dom_hash）

### 简化方案

CONTEXT.md D-03 指定签名包含 `dom_hash_before` 和 `dom_hash_after` 参数。但 StallDetector 的 `check()` 已在 `_history` 中记录 dom_hash，可通过 `_history[-2].dom_hash` 和 `_history[-1].dom_hash` 获取前后两步的 hash，减少参数传递。

**建议**: 保持 CONTEXT.md 签名（显式传参更清晰），同时也可以从 `_history` 获取作为 fallback。

## 4. 测试策略

### 测试文件位置

- `backend/tests/test_dom_patch_phase67.py` — 测试 _detect_row_identity, _failure_tracker
- `backend/tests/test_stall_detector_phase67.py` — 测试 detect_failure_mode, FailureDetectionResult

### Mock 策略 (D-04)

- Mock SimplifiedNode 和 AccessibilityNode 测试 `_detect_row_identity`
  - 创建 mock AccessibilityNode 设置 `tag_name`, `get_all_children_text()`, `parent_node`, `children`
  - 测试：包含 IMEI → 返回字符串；不包含 → 返回 None；非 td → 返回 None
- Mock step 参数测试 `detect_failure_mode`
  - 测试三种模式各自触发条件
  - 测试不匹配任何模式返回 `FailureDetectionResult(failure_mode=None, details={})`
- Dict 操作测试 `_failure_tracker`
  - 测试 `update_failure_tracker()` 新建记录
  - 测试累加 count
  - 测试 `reset_failure_tracker()` 清空

### 覆盖率目标

>= 80% (per D-04)

## 5. Validation Architecture

### Testable Behaviors

| ID | Behavior | How to Verify |
|----|----------|---------------|
| V1 | `_detect_row_identity()` 正确提取 IMEI | Unit test: mock tr with td containing "I352017041234567", assert returns "I352017041234567" |
| V2 | `_detect_row_identity()` 对无 IMEI 的 tr 返回 None | Unit test: mock tr with td containing "普通文本", assert returns None |
| V3 | `_failure_tracker` 新建记录 | Unit test: call update_failure_tracker("id1", "err", "mode"), assert tracker["id1"]["count"] == 1 |
| V4 | `_failure_tracker` 累加 | Unit test: call update 3 times, assert count == 3 |
| V5 | `reset_failure_tracker()` 清空 | Unit test: add entries, call reset, assert len(tracker) == 0 |
| V6 | `detect_failure_mode` 识别 click_no_effect | Unit test: action="click", same hashes, assert failure_mode == "click_no_effect" |
| V7 | `detect_failure_mode` 识别 wrong_column | Unit test: evaluation with "错误列", assert failure_mode == "wrong_column" |
| V8 | `detect_failure_mode` 识别 edit_not_active | Unit test: action="input", evaluation with "无法输入", assert failure_mode == "edit_not_active" |
| V9 | `detect_failure_mode` 无失败返回 None | Unit test: normal case, assert failure_mode is None |
| V10 | `FailureDetectionResult` frozen | Unit test: attempt to set attribute, raises FrozenInstanceError |
| V11 | `reset_failure_tracker` 独立于 `_PATCHED` | Integration test: apply_dom_patch() twice, second call resets tracker but skips patches |

### Dimension Coverage

| Dimension | Coverage | Notes |
|-----------|----------|-------|
| 1. Happy path | V1, V3, V6-V8 | Core detection and tracking |
| 2. Edge cases | V2, V9 | No match returns None |
| 3. Error handling | Missing — add test for invalid inputs | |
| 4. State transitions | V4, V5 | Counter increment + reset |
| 5. Immutability | V10 | frozen dataclass |
| 6. Integration | V11 | reset vs _PATCHED independence |
| 7. Performance | N/A — simple dict/regex operations | |
| 8. Validation | V1-V11 | Full coverage |

---

## RESEARCH COMPLETE

**Key findings:**
1. 现有 `_is_textual_td_cell()` 模式可直接复用实现 `_detect_row_identity()`
2. `_PATCHED` 模块级变量模式可直接复用实现 `_failure_tracker`
3. `StallResult` frozen dataclass 模式可直接复用实现 `FailureDetectionResult`
4. 三种失败模式检测逻辑清晰，关键词匹配 + dom_hash 比对
5. 纯单元测试策略可行，所有组件可通过 mock 测试

**Risk assessment:** LOW — 所有实现基于成熟模式，无架构变更
