# Phase 30: 断言执行适配层 - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary

适配层模式处理三层参数传递（data、api_params、field_params），将 field_params 中的 "now" 转换为实际时间字符串，返回结构化字段结果（fields/name 格式）。此阶段专注于适配层实现，不包含字段发现（Phase 28 已完成）或前端 UI（Phase 29 已完成）。

**Scope:**
- 重构 `execute_assertion_method()` 接收三层参数结构
- 实现适配层将 field_params 中的 "now" 转换为实际时间
- 修改响应结构为 `fields/name` 格式（符合 ROADMAP.md API Contract）
- 保持向后兼容（顶层 headers/data/params 继续工作）

**Out of Scope:**
- 字段发现 API（Phase 28 已完成）
- 前端字段配置 UI（Phase 29 已完成）
- E2E 测试（Phase 31）
- 修改 base_assert.py

</domain>

<decisions>
## Implementation Decisions

### 参数合并策略
- **D-01:** api_params 和 field_params **平级合并**为 kwargs，传给断言方法
  ```python
  kwargs = {**(api_params or {}), **(field_params or {})}
  method(headers=resolved_headers, data=data, **kwargs)
  ```

### "now" 时间转换
- **D-02:** 转换格式 = **标准格式** `YYYY-MM-DD HH:mm:ss`（使用 `get_formatted_datetime()`）
- **D-03:** 转换时机 = **调用前预处理**（在适配层遍历 field_params 转换）
  ```python
  for key, value in kwargs.items():
      if value == 'now' and _is_time_field(key, default_node=None):
          kwargs[key] = get_formatted_datetime()
  ```

### 响应结构统一
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

### API 端点设计
- **D-05:** API 端点设计 = **修改现有端点**
  - 保持 `POST /api/external-assertions/execute` 端点
  - 扩展请求体支持新结构
- **D-06:** 向后兼容性 = **完全兼容**
  - 顶层 `headers/data/params` 继续工作
  - 同时支持新的 `data/api_params/field_params`
  - 两种写法都有效

### Claude's Discretion
- **D-07:** 时间字段容差范围（建议 ±1 分钟）
- **D-08:** API 参数验证逻辑
- **D-09:** 单元测试 mock 数据结构

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 架构设计参考
- `.planning/ROADMAP.md` — Phase 30 定义、API Contract（Request Body/Response 结构）
- `.planning/research/STACK.md` — 断言系统集成技术栈
- `.planning/research/PITFALLS.md` — 断言集成陷阱

### 前置阶段参考
- `.planning/phases/25-assertion-execution-engine/25-CONTEXT.md` — Phase 25 决策（execute_assertion_method 模式、超时保护、AssertionError 解析）
- `.planning/phases/28-backend-field-discovery/28-CONTEXT.md` — Phase 28 决策（_is_time_field 函数、字段发现逻辑）
- `.planning/phases/29-frontend-field-config-ui/29-CONTEXT.md` — Phase 29 决策（field_params 结构、AssertionConfig 类型）

### 现有代码参考
- `backend/core/external_precondition_bridge.py`:
  - `execute_assertion_method()` — 需重构支持三层参数
  - `_parse_assertion_error()` — 需修改返回 `name` 而非 `field`
  - `_is_time_field()` — 用于判断时间字段
  - `resolve_headers()` — headers 解析（已有）
- `backend/api/routes/external_assertions.py`:
  - `/execute` 端点 — 需扩展请求体结构

### 外部项目结构
- `webseleniumerp/common/base_assertions_field.py` — 包含 param 字典的字段定义
- `webseleniumerp/common/base_api.py` — `get_formatted_datetime()` 方法

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `execute_assertion_method()` — 已有执行框架，需扩展参数处理
  - `_parse_assertion_error()` — 已有解析逻辑，需修改字段名
  - `_is_time_field()` — 已有时间字段判断，可直接使用
  - `resolve_headers()` — headers 解析已完成
  - 30 秒超时保护 — 已实现
- `backend/api/routes/external_assertions.py`:
  - Pydantic 请求/响应模型 — 可扩展

### Established Patterns
- **执行模式**: `asyncio.wait_for(loop.run_in_executor(...), timeout=30)`
- **参数合并**: `{**dict1, **dict2}` 平级合并
- **错误分类**: success, error_type (TimeoutError, ParameterError, ExecutionError)
- **向后兼容**: 保留旧参数，同时支持新参数

### Integration Points
- `backend/core/external_precondition_bridge.py` — 需修改:
  - `execute_assertion_method()` — 扩展参数签名，添加 api_params/field_params
  - `_parse_assertion_error()` — 修改返回字段名 field → name
  - 新增 `_convert_now_values()` — 预处理 "now" 值
- `backend/api/routes/external_assertions.py`:
  - `/execute` 端点 — 扩展请求体模型，支持三层参数

### 需要新增/修改的代码
| 组件 | 目的 | 参考模式 |
|------|------|----------|
| `_convert_now_values()` | 预处理 "now" 为时间字符串 | 遍历 kwargs，调用 _is_time_field |
| `execute_assertion_method()` 扩展 | 接收 api_params/field_params | 参数合并 + 预处理 |
| `_parse_assertion_error()` 修改 | 返回 name 而非 field | 字段名修改 |
| 请求体模型扩展 | 支持 data/api_params/field_params | Pydantic 模型 |

### API Contract (from ROADMAP.md)

**Request Body:**
```json
{
  "class_name": "PcAssert",
  "method_name": "attachment_inventory_list_assert",
  "data": "main",
  "api_params": {
    "i": 1,
    "j": null,
    "headers": "main"
  },
  "field_params": {
    "statusStr": "已完成",
    "createTime": "now"
  }
}
```

**Response:**
```json
{
  "success": true,
  "passed": false,
  "duration": 1.23,
  "fields": [
    {"name": "statusStr", "expected": "已完成", "actual": "进行中", "passed": false},
    {"name": "createTime", "expected": "now", "actual": "2026-03-21 10:30:00", "passed": true}
  ],
  "error": null
}
```

</code_context>

<specifics>
## Specific Ideas

- "now" 转换使用 `get_formatted_datetime()` 保持与 webseleniumerp 一致
- 时间字段容差范围建议 ±1 分钟（需在断言方法内部处理）
- 向后兼容：顶层 headers 保留，同时支持 api_params.headers

</specifics>

<deferred>
## Deferred Ideas

- E2E 测试 — Phase 31
- 断言结果持久化 — 未来需求
- 并行断言执行 — 未来优化

</deferred>

---
*Phase: 30-assertion-execution-adapter*
*Context gathered: 2026-03-22*
