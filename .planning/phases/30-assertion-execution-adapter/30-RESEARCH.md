# Phase 30: 断言执行适配层 - Research

**Researched:** 2026-03-22
**Domain:** 断言执行适配层实现（三层参数传递、"now"时间转换、结构化结果）
**Confidence:** HIGH

## Summary

Phase 30 需要重构 `execute_assertion_method()` 函数以支持三层参数结构（data、api_params、field_params），实现 "now" 时间转换适配层，并统一响应结构为 `fields/name` 格式。核心实现都在 `external_precondition_bridge.py` 中完成，需要扩展现有执行逻辑并保持向后兼容。

**Primary recommendation:** 扩展现有 `execute_assertion_method()` 函数签名，添加 `api_params` 和 `field_params` 参数，在调用断言方法前预处理 "now" 值，并修改 `_parse_assertion_error()` 返回字段名从 `field` 改为 `name`。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### 参数合并策略
- **D-01:** api_params 和 field_params **平级合并**为 kwargs，传给断言方法
  ```python
  kwargs = {**(api_params or {}), **(field_params or {})}
  method(headers=resolved_headers, data=data, **kwargs)
  ```

#### "now" 时间转换
- **D-02:** 转换格式 = **标准格式** `YYYY-MM-DD HH:mm:ss`（使用 `get_formatted_datetime()`）
- **D-03:** 转换时机 = **调用前预处理**（在适配层遍历 field_params 转换）
  ```python
  for key, value in kwargs.items():
      if value == 'now' and _is_time_field(key, default_node=None):
          kwargs[key] = get_formatted_datetime()
  ```

#### 响应结构统一
- **D-04:** 响应结构 = **统一为 `fields/name`**（符合 ROADMAP.md API Contract）
  - 修改 `_parse_assertion_error()` 返回 `name` 而非 `field`
  - 修改响应结构使用 `fields` 而非 `field_results`
  ```json
  {
    "success": true,
    "passed": false,
    "duration": 1.23,
    "fields": [
      {"name": "statusStr", "expected": "已完成", "actual": "进行中", "passed": false}
    ]
  }
  ```

#### API 端点设计
- **D-05:** API 端点设计 = **修改现有端点**
  - 保持 `POST /api/external-assertions/execute` 端点
  - 扩展请求体支持新结构
- **D-06:** 向后兼容性 = **完全兼容**
  - 顶层 `headers/data/params` 继续工作
  - 同时支持新的 `data/api_params/field_params`
  - 两种写法都有效

### Claude's Discretion
- **D-07:** 时间字段容差范围（建议 +/- 1 分钟）
- **D-08:** API 参数验证逻辑
- **D-09:** 单元测试 mock 数据结构

### Deferred Ideas (OUT OF SCOPE)
- E2E 测试 — Phase 31
- 断言结果持久化 — 未来需求
- 并行断言执行 — 未来优化

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| EXEC-01 | execute_assertion_method() 接收三层参数结构 | 现有函数签名需扩展，添加 api_params 和 field_params 参数 |
| EXEC-02 | 适配层将 field_params 中的 "now" 转换为实际时间 | 使用现有 _is_time_field() 判断 + datetime 模块生成时间字符串 |
| EXEC-03 | 捕获 AssertionError，解析为结构化字段结果 | 现有 _parse_assertion_error() 已实现，需修改字段名 field -> name |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python datetime | stdlib | 时间字符串生成 | 标准库，格式化时间 |
| asyncio | stdlib | 异步执行 | 已有模式 `run_in_executor` + `wait_for` |
| Pydantic | 2.x | 请求体验证 | 已有模式，扩展请求体模型 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| FastAPI | 0.135+ | API 路由 | 扩展现有 /execute 端点 |
| pytest | 8.x | 单元测试 | 已有测试框架 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| datetime.strftime | time.strftime | datetime 更直观 |
| 平级合并 | 嵌套结构 | 平级更简单，符合断言方法签名 |

**Installation:**
无新依赖，使用现有库。

## Architecture Patterns

### Recommended Project Structure (Changes)
```
backend/
├── core/
│   └── external_precondition_bridge.py  # 主要修改点
│       ├── execute_assertion_method()    # 扩展参数签名
│       ├── _convert_now_values()         # 新增："now" 转换
│       └── _parse_assertion_error()      # 修改：field -> name
└── api/routes/
    └── external_assertions.py            # 扩展请求体模型
```

### Pattern 1: 三层参数处理模式
**What:** 将 data、api_params、field_params 三层参数合并后传递给断言方法
**When to use:** 所有断言执行场景
**Example:**
```python
# Source: .planning/phases/30-assertion-execution-adapter/30-CONTEXT.md
async def execute_assertion_method(
    class_name: str,
    method_name: str,
    headers: str | None = 'main',
    data: str = 'main',
    api_params: dict | None = None,      # 新增
    field_params: dict | None = None,     # 新增
    params: dict | None = None,           # 保留向后兼容
    timeout: float = 30.0
) -> dict:
    # 向后兼容：如果传入 params，将其作为 field_params
    if params and not field_params:
        field_params = params

    # 平级合并参数
    kwargs = {**(api_params or {}), **(field_params or {})}
```

### Pattern 2: "now" 时间转换模式
**What:** 在调用断言方法前，遍历 kwargs 将 "now" 转换为实际时间字符串
**When to use:** 所有断言执行场景
**Example:**
```python
# Source: .planning/phases/30-assertion-execution-adapter/30-CONTEXT.md
from datetime import datetime

def _convert_now_values(kwargs: dict) -> dict:
    """Convert 'now' values to formatted datetime strings for time fields."""
    result = kwargs.copy()
    for key, value in result.items():
        if value == 'now' and _is_time_field(key, default_node=None):
            result[key] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return result
```

### Pattern 3: 响应结构统一模式
**What:** 将 field_results 改为 fields，field 改为 name
**When to use:** 所有断言执行响应
**Example:**
```python
# Source: ROADMAP.md API Contract
{
    "success": true,
    "passed": false,
    "duration": 1.23,
    "fields": [
        {"name": "statusStr", "expected": "已完成", "actual": "进行中", "passed": false}
    ],
    "error": null
}
```

### Anti-Patterns to Avoid
- **直接修改 base_assert.py:** 使用适配层模式，避免破坏现有功能
- **硬编码时间格式:** 使用 datetime 标准格式
- **破坏向后兼容:** 旧参数 params 必须继续工作

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 时间格式化 | 自定义格式化函数 | `datetime.now().strftime('%Y-%m-%d %H:%M:%S')` | 标准库，格式一致 |
| 时间字段判断 | 重复判断逻辑 | 现有 `_is_time_field()` | 已实现，经过测试 |
| 参数合并 | 复杂合并逻辑 | `{**dict1, **dict2}` 平级合并 | Python 原生语法 |

**Key insight:** 适配层模式意味着在现有函数上扩展，而非重写。保持向后兼容是关键。

## Common Pitfalls

### Pitfall 1: 向后兼容性破坏
**What goes wrong:** 修改函数签名后，旧的调用方式（使用 params）失败
**Why it happens:** 没有处理 params 作为 field_params 的 fallback
**How to avoid:** 在函数开头添加兼容性处理
```python
if params and not field_params:
    field_params = params
```
**Warning signs:** 现有测试失败，前端旧版本报错

### Pitfall 2: "now" 转换遗漏
**What goes wrong:** 时间字段传入 "now" 但未转换为实际时间
**Why it happens:** 忘记在调用断言方法前调用 _convert_now_values()
**How to avoid:** 在构建 call_kwargs 后、调用方法前调用转换函数
**Warning signs:** 断言失败消息显示 expected: "now"

### Pitfall 3: 响应结构不一致
**What goes wrong:** 部分响应使用 field_results，部分使用 fields
**Why it happens:** 只修改了 _parse_assertion_error() 但忘记修改其他返回点
**How to avoid:** 检查所有返回 result 的地方，确保使用统一字段名
**Warning signs:** 前端显示 undefined 或字段数据丢失

### Pitfall 4: 时间字段判断不准确
**What goes wrong:** 非时间字段被误判为时间字段，"now" 被错误转换
**Why it happens:** _is_time_field() 仅基于后缀匹配，可能有误判
**How to avoid:** 只有 value == 'now' 且 is_time_field() 为 True 时才转换
**Warning signs:** 非时间字段的字符串 "now" 被转换为时间

## Code Examples

Verified patterns from existing codebase:

### execute_assertion_method 现有实现 (需扩展)
```python
# Source: backend/core/external_precondition_bridge.py:846-956
async def execute_assertion_method(
    class_name: str,
    method_name: str,
    headers: str | None = 'main',
    data: str = 'main',
    params: dict | None = None,
    timeout: float = 30.0
) -> dict:
    # ... existing implementation ...
    call_kwargs = {
        'headers': resolved_headers,
        'data': data,
        **params
    }
    await asyncio.wait_for(
        loop.run_in_executor(None, lambda: method(**call_kwargs)),
        timeout=timeout
    )
```

### _is_time_field 现有实现 (可复用)
```python
# Source: backend/core/external_precondition_bridge.py:1366-1383
def _is_time_field(field_name: str, default_node) -> bool:
    """Check if field is a time field based on name suffix or default value."""
    # Primary: Check AST for get_formatted_datetime call
    if isinstance(default_node, ast.Call):
        if isinstance(default_node.func, ast.Attribute):
            if default_node.func.attr == 'get_formatted_datetime':
                return True
    # Fallback: Suffix matching
    return field_name.endswith(('Time', 'time', 'Date', 'date'))
```

### _parse_assertion_error 现有实现 (需修改 field -> name)
```python
# Source: backend/core/external_precondition_bridge.py:806-843
def _parse_assertion_error(error_message: str) -> list[dict]:
    """Parse AssertionError message to extract field-level results."""
    field_results = []
    pattern = r"字段\s+['\"]([^'\"]+)['\"]\s+(预期值|预期包含):\s*['\"]([^'\"]*)['\"]\s*,\s*实际值:\s*['\"]([^'\"]*)['\"]"

    for match in re.finditer(pattern, error_message):
        field_name = match.group(1)
        # ... parse logic ...
        field_results.append({
            'field': field_name,  # 需改为 'name'
            'expected': expected,
            'actual': actual,
            'passed': False,
            'comparison_type': 'equals' if comparison_type == '预期值' else 'contains'
        })
    return field_results
```

### 新增 _convert_now_values 实现
```python
# Source: Phase 30 设计
from datetime import datetime

def _convert_now_values(kwargs: dict) -> dict:
    """Convert 'now' string values to formatted datetime for time fields.

    Args:
        kwargs: Parameter dictionary to process

    Returns:
        New dict with 'now' values converted to datetime strings
    """
    result = {}
    for key, value in kwargs.items():
        if value == 'now' and _is_time_field(key, default_node=None):
            result[key] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            result[key] = value
    return result
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 单层 params | 三层 data/api_params/field_params | Phase 30 | 更清晰的参数分类 |
| field_results 响应 | fields 响应 | Phase 30 | 符合 ROADMAP API Contract |
| 无 "now" 转换 | 预处理 "now" 为时间字符串 | Phase 30 | 前端可直接传 "now" |

**Deprecated/outdated:**
- 顶层 params 参数：保留但推荐使用 field_params

## Open Questions

1. **时间字段容差范围**
   - What we know: CONTEXT.md 建议容差 +/- 1 分钟
   - What's unclear: 容差在断言方法内部处理，适配层是否需要额外逻辑
   - Recommendation: 适配层不做容差处理，"now" 精确转换为当前时间，容差由断言方法内部 assert_time() 处理

2. **headers 参数位置**
   - What we know: D-01 决定 api_params 平级合并，headers 可能在 api_params 中
   - What's unclear: 如果 api_params.headers 和顶层 headers 同时存在，如何处理
   - Recommendation: 顶层 headers 优先，api_params.headers 作为 fallback

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x |
| Config file | pyproject.toml |
| Quick run command | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EXEC-01 | execute_assertion_method() 接收三层参数 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::TestExecuteAssertionMethod -v` | Yes - 需扩展 |
| EXEC-02 | "now" 转换为实际时间 | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::TestConvertNowValues -v` | No - Wave 0 新增 |
| EXEC-03 | AssertionError 解析为结构化结果 | unit | `uv run pytest backend/tests/core/test_external_precondition_bridge_assertion.py::TestParseAssertionError -v` | Yes - 需修改 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_external_assertion_bridge.py` — 需新增 TestConvertNowValues 测试类
- [ ] 需扩展 TestExecuteAssertionMethod 测试用例覆盖三层参数
- [ ] 需修改 TestParseAssertionError 测试用例验证 name 字段

*(If no gaps: "None - existing test infrastructure covers all phase requirements")*

## Sources

### Primary (HIGH confidence)
- `.planning/phases/30-assertion-execution-adapter/30-CONTEXT.md` - 用户决策和设计规范
- `backend/core/external_precondition_bridge.py` - 现有实现代码
- `.planning/ROADMAP.md` - API Contract 定义

### Secondary (MEDIUM confidence)
- `.planning/research/STACK.md` - 断言系统集成技术栈
- `.planning/research/PITFALLS.md` - 断言集成陷阱
- `.planning/phases/25-assertion-execution-engine/25-CONTEXT.md` - Phase 25 决策（执行模式参考）

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 无新依赖，复用现有库
- Architecture: HIGH - 模式已确立，代码已存在
- Pitfalls: HIGH - 基于现有代码分析和 CONTEXT.md 决策

**Research date:** 2026-03-22
**Valid until:** 30 days (stable implementation)
