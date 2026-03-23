# Phase 33: 人工验证断言执行 - Research

**Researched:** 2026-03-22
**Domain:** Manual verification of assertion execution flow (sales outbound test case)
**Confidence:** HIGH

## Summary

This phase is a **manual verification phase** focused on validating the end-to-end assertion execution flow using the sales outbound (`sell_sale_item_list_assert`) test case. The core assertion infrastructure (three-layer parameters, "now" time conversion, field-level result parsing) was implemented in Phases 28-32 and verified through unit tests. Phase 33's purpose is to validate this flow through actual UI execution with real ERP data.

**Primary recommendation:** Execute manual verification through the complete UI flow: create task -> configure assertion parameters -> run test -> verify report display. Document any issues found in ISSUES.md.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 验证方式 = **完整 UI 验证**
  - 在前端创建任务
  - 配置断言参数（salesOrder, articlesStateStr, saleTime）
  - 执行测试
  - 查看 ReportDetail 页面结果
- **D-02:** 断言参数 = **使用默认参数**
  - salesOrder='SA'
  - articlesStateStr='已销售'
  - saleTime='now'
- **D-03:** 数据准备 = **需要先创建数据**
  - 需要先执行完整测试流程创建销售出库记录
  - 然后执行断言验证
- **D-04:** 验证通过标准 = **全部四项**
  1. 断言被正确调用（返回结构包含 success/passed/fields）
  2. 'now' 时间转换正确（显示为实际时间字符串）
  3. 结果显示在报告中（断言结果卡片）
  4. 字段级结果清晰（name/expected/actual/passed）
- **D-05:** 失败处理 = **需要分析原因**
  - 如果 passed=false，需要分析是参数错误还是系统 bug
- **D-06:** Bug 记录位置 = **ISSUES.md 文件**
  - 在 `.planning/phases/33-人工验证断言执行/` 目录下创建
- **D-07:** Bug 记录内容 = **四项**
  - 问题描述
  - 复现步骤
  - 错误信息/证据
  - 优先级 (P0-P3)

### Claude's Discretion
- 具体验证用例的选择
- 测试执行的超时设置
- 报告截图的命名规则

### Deferred Ideas (OUT OF SCOPE)
- 自动化 E2E 测试 — Phase 34 或后续版本
- 断言参数智能推荐 — 未来需求
- 断言结果对比分析 — 未来需求
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ASSERT-01 | `sell_sale_item_list_assert` 断言方法能正确执行并返回结果 | `execute_assertion_method()` in external_precondition_bridge.py handles assertion execution with timeout protection |
| ASSERT-02 | 断言参数（salesOrder、articlesStateStr、saleTime）正确传递到断言方法 | Three-layer params (api_params, field_params, params) flow through `execute_all_assertions()` -> `execute_assertion_method()` |
| ASSERT-03 | `saleTime='now'` 能正确转换为当前时间 | `_convert_now_values()` converts 'now' to `YYYY-MM-DD HH:mm:ss` format using `datetime.now()` |
| ASSERT-04 | 断言结果正确存储到 context 并在报告中展示 | Results stored via `context.store_assertion_result()`, displayed in `ReportDetail.tsx` via `assertion_results` prop |
</phase_requirements>

## Standard Stack

### Core Infrastructure (Already Implemented)
| Component | File | Purpose | Status |
|-----------|------|---------|--------|
| `execute_all_assertions()` | backend/core/external_precondition_bridge.py | Execute multiple assertions, extract three-layer params | VERIFIED (Phase 32) |
| `execute_assertion_method()` | backend/core/external_precondition_bridge.py | Execute single assertion with timeout, "now" conversion | VERIFIED (Phase 30) |
| `_convert_now_values()` | backend/core/external_precondition_bridge.py | Convert 'now' to datetime string | VERIFIED (Phase 30) |
| `_parse_assertion_error()` | backend/core/external_precondition_bridge.py | Parse AssertionError to field-level results | VERIFIED |
| `FieldParamsEditor` | frontend/src/components/TaskModal/FieldParamsEditor.tsx | Field parameter configuration UI | VERIFIED (Phase 29) |
| `ReportDetail` | frontend/src/pages/ReportDetail.tsx | Display assertion results in report | VERIFIED |
| `AssertionResults` | frontend/src/components/Report/AssertionResults.tsx | Assertion result card component | VERIFIED |

### Test Data Structure
| Parameter | Type | Value | Purpose |
|-----------|------|-------|---------|
| salesOrder | string | 'SA' | Sales order type filter |
| articlesStateStr | string | '已销售' | Article state filter |
| saleTime | string | 'now' | Time field - will be converted to actual timestamp |

### Expected Response Structure
```json
{
  "success": true,
  "passed": false,
  "duration": 1.23,
  "fields": [
    {"name": "statusStr", "expected": "已完成", "actual": "进行中", "passed": false},
    {"name": "saleTime", "expected": "now", "actual": "2026-03-22 10:30:00", "passed": true}
  ],
  "error": null
}
```

## Architecture Patterns

### Verification Flow
```
┌─────────────────────────────────────────────────────────────────┐
│                     Manual Verification Flow                     │
├─────────────────────────────────────────────────────────────────┤
│ 1. Start Services                                               │
│    - Backend: uv run uvicorn backend.api.main:app --port 8080   │
│    - Frontend: cd frontend && npm run dev                       │
├─────────────────────────────────────────────────────────────────┤
│ 2. Create/Configure Task (UI)                                   │
│    - Navigate to Task creation page                             │
│    - Configure assertion:                                       │
│      - className: "PcAssert"                                    │
│      - methodName: "sell_sale_item_list_assert"                 │
│      - field_params: {salesOrder: 'SA', articlesStateStr: '已销售', saleTime: 'now'} │
├─────────────────────────────────────────────────────────────────┤
│ 3. Execute Test                                                 │
│    - Run test (may need precondition data first)                │
│    - Wait for completion                                        │
├─────────────────────────────────────────────────────────────────┤
│ 4. Verify Report (ReportDetail page)                            │
│    - Check assertion_results section exists                     │
│    - Verify fields array contains field-level results           │
│    - Check saleTime shows actual time, not "now"                │
│    - Verify passed/failed status is correct                     │
└─────────────────────────────────────────────────────────────────┘
```

### Three-Layer Parameter Flow
```
Frontend (AssertionConfig)          Backend (execute_all_assertions)
─────────────────────────          ─────────────────────────────────
{
  className: "PcAssert",
  methodName: "sell_sale_item_list_assert",
  headers: "main",
  data: "main",
  api_params: {},                   →  api_params = assertion_config.get('api_params', {})
  field_params: {                   →  field_params = assertion_config.get('field_params', {})
    salesOrder: 'SA',
    articlesStateStr: '已销售',
    saleTime: 'now'
  }
}
                                           ↓
                                   execute_assertion_method()
                                           ↓
                                   _convert_now_values()  // 'now' -> '2026-03-22 10:30:00'
                                           ↓
                                   merged_kwargs = {**api_params, **field_params}
                                           ↓
                                   method(headers=resolved_headers, data=data, **merged_kwargs)
```

### Key Code References

#### Assertion Execution (external_precondition_bridge.py:847-970)
```python
async def execute_assertion_method(
    class_name: str,
    method_name: str,
    headers: str | None = 'main',
    data: str = 'main',
    api_params: dict | None = None,
    field_params: dict | None = None,
    params: dict | None = None,
    timeout: float = 30.0
) -> dict:
    # Backward compatibility: params acts as field_params fallback
    if params and not field_params:
        field_params = params

    # ... load assertion class, resolve headers ...

    # Merge api_params and field_params (D-01)
    merged_kwargs = {**(api_params or {}), **(field_params or {})}

    # Convert "now" values to datetime strings (D-02, D-03)
    call_kwargs = _convert_now_values(merged_kwargs)
```

#### "now" Time Conversion (external_precondition_bridge.py:1404-1419)
```python
def _convert_now_values(kwargs: dict) -> dict:
    """Convert 'now' values to formatted datetime strings for time fields."""
    result = {}
    for key, value in kwargs.items():
        if value == 'now' and _is_time_field(key, default_node=None):
            result[key] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            result[key] = value
    return result
```

#### Field Result Parsing (external_precondition_bridge.py:807-844)
```python
def _parse_assertion_error(error_message: str) -> list[dict]:
    """Parse AssertionError message to extract field-level results."""
    # Pattern for: 字段 'fieldName' 预期值: 'expected', 实际值: 'actual'
    pattern = r"字段\s+['\"]([^'\"]+)['\"]\s+(预期值|预期包含):\s*['\"]([^'\"]*)['\"]\s*,\s*实际值:\s*['\"]([^'\"]*)['\"]"

    for match in re.finditer(pattern, error_message):
        field_results.append({
            'name': field_name,
            'expected': expected,
            'actual': actual,
            'passed': False,
            'comparison_type': 'equals' if comparison_type == '预期值' else 'contains'
        })
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Time conversion | Custom date formatting | `_convert_now_values()` | Already handles time field detection and YYYY-MM-DD HH:mm:ss format |
| Assertion execution | Custom assertion runner | `execute_assertion_method()` | Includes timeout protection, error handling, field parsing |
| Parameter passing | Manual param extraction | `execute_all_assertions()` | Already extracts api_params, field_params, params correctly |
| Bug tracking | Ad-hoc notes | ISSUES.md template | Standardized format for P0-P3 prioritization |

## Common Pitfalls

### Pitfall 1: Missing Precondition Data
**What goes wrong:** Assertion fails because no sales outbound record exists to validate against.
**Why it happens:** The assertion validates existing data; without it, there's nothing to check.
**How to avoid:** Execute full test flow (preconditions + steps) before running assertion verification.
**Warning signs:** AssertionError with "no data found" or empty results.

### Pitfall 2: "now" Not Converting
**What goes wrong:** `saleTime` shows literal "now" string in report instead of actual timestamp.
**Why it happens:** `_is_time_field()` returns false for the field name, or conversion not triggered.
**How to avoid:** Verify field name ends with 'Time'/'time'/'Date'/'date' suffix.
**Warning signs:** Report shows `expected: "now"` instead of `expected: "2026-03-22 10:30:00"`.

### Pitfall 3: Field Results Not Displayed
**What goes wrong:** Assertion fails but no field-level details shown in report.
**Why it happens:** `_parse_assertion_error()` couldn't parse the error message format.
**How to avoid:** Check assertion method uses standard error format: `字段 'name' 预期值: 'x', 实际值: 'y'`.
**Warning signs:** Report shows only generic "Assertion failed" message.

### Pitfall 4: Three-Layer Params Not Passed
**What goes wrong:** `field_params` not reaching assertion method.
**Why it happens:** Frontend config not properly structured or backend extraction failing.
**How to avoid:** Verify `AssertionConfig` includes `field_params` key; check backend logs for extracted values.
**Warning signs:** Backend logs show empty `field_params={}`.

## Code Examples

### Verify Assertion Configuration (Frontend)
```typescript
// Expected structure in Task assertions array
const assertion: AssertionConfig = {
  className: 'PcAssert',
  methodName: 'sell_sale_item_list_assert',
  headers: 'main',
  data: 'main',
  params: {},
  field_params: {
    salesOrder: 'SA',
    articlesStateStr: '已销售',
    saleTime: 'now'
  }
}
```

### Check Backend Logs
```bash
# Look for these log patterns during execution:
# "Executing assertion 1/1: PcAssert.sell_sale_item_list_assert"
# "Assertion 0 passed" or "Assertion 0 failed: <error message>"
# "Assertion execution complete: X/Y passed"
```

### Verify Report Structure
```typescript
// In ReportDetail, check assertion_results contains:
interface ExpectedAssertionResult {
  id: string
  run_id: string
  assertion_id: string
  status: 'pass' | 'fail'
  message: string | null
  actual_value: string | null
}

// For field-level results, check api_assertion_results:
interface ExpectedApiAssertionResult {
  index: number
  code: string
  status: 'success' | 'failed'
  field_results?: Array<{
    field_name: string
    expected: any
    actual: any
    passed: boolean
  }>
}
```

## State of the Art

| Previous Approach | Current Approach | When Changed | Impact |
|-------------------|------------------|--------------|--------|
| Manual Python code for assertions | Structured AssertionConfig JSON | Phase 29 | Easier UI configuration |
| Single-layer params | Three-layer params (api_params, field_params, params) | Phase 32 | Cleaner separation of concerns |
| "now" as literal string | Auto-converted to datetime | Phase 30 | Accurate time comparisons |

**Deprecated/outdated:**
- `field_results` key in response: Use `fields` instead (per ROADMAP API Contract)
- `field` key in field result: Use `name` instead

## Open Questions

1. **Precondition Data Availability**
   - What we know: Sales outbound test case requires existing sales records
   - What's unclear: Whether test environment has pre-existing data or needs fresh creation
   - Recommendation: Assume data creation needed; execute full test flow first

2. **Assertion Pass/Fail Criteria**
   - What we know: Assertion validates salesOrder, articlesStateStr, saleTime
   - What's unclear: What values are expected in the actual ERP data
   - Recommendation: If assertion fails, analyze if it's data mismatch vs system bug

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/core/test_external_precondition_bridge_assertion.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ASSERT-01 | Assertion executes and returns result | unit | `uv run pytest backend/tests/core/test_external_precondition_bridge_assertion.py::TestExecuteAssertionMethod -v` | YES |
| ASSERT-02 | Parameters correctly passed | unit | `uv run pytest backend/tests/core/test_external_precondition_bridge_assertion.py::TestExecuteAllAssertionsThreeLayerParams -v` | YES |
| ASSERT-03 | "now" time conversion | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -v -k "now"` | Check needed |
| ASSERT-04 | Results stored in context | unit | `uv run pytest backend/tests/core/test_external_precondition_bridge_assertion.py::TestExecuteAllAssertions::test_stores_results_in_context_via_store_assertion_result -v` | YES |

### Sampling Rate
- **Per task commit:** Manual verification (this phase is manual by design)
- **Per wave merge:** N/A (single verification phase)
- **Phase gate:** All four ASSERT requirements verified through UI

### Wave 0 Gaps
- [ ] Manual verification checklist document
- [ ] ISSUES.md template for bug recording

*(Note: This phase is intentionally manual verification - automated tests exist for the underlying code but the phase goal is UI verification)*

## Sources

### Primary (HIGH confidence)
- `.planning/phases/33-人工验证断言执行/33-CONTEXT.md` - User decisions and scope
- `backend/core/external_precondition_bridge.py` - Assertion execution implementation
- `backend/tests/core/test_external_precondition_bridge_assertion.py` - Unit test coverage

### Secondary (MEDIUM confidence)
- `.planning/phases/30-assertion-execution-adapter/30-CONTEXT.md` - Three-layer params decisions
- `.planning/phases/32-three-layer-params-gap-closure/32-VERIFICATION.md` - Phase 32 verification results

### Tertiary (LOW confidence)
- N/A - All core patterns verified through code inspection

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All components implemented and unit tested in Phases 28-32
- Architecture: HIGH - Code inspection confirms three-layer param flow
- Pitfalls: MEDIUM - Based on code analysis; actual runtime may reveal edge cases

**Research date:** 2026-03-22
**Valid until:** 30 days (stable assertion infrastructure)
