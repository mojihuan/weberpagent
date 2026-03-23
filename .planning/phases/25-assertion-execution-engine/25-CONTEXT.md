# Phase 25: Assertion Execution Engine - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

执行已配置的断言方法（来自 Phase 24 的 AssertionConfig），解析 headers 标识符为实际 token，捕获断言结果并存入 context。此阶段专注于执行层实现，不包含断言方法的发现（Phase 23）或 UI 配置（Phase 24）。

**Scope:**
- 实现 `execute_assertion_method()` 函数，支持 30 秒超时保护
- 实现 headers 标识符解析（main/vice 等 → 实际 token 字典）
- 捕获 AssertionError 异常并提取字段级验证结果
- 断言结果存入 context 供后续步骤引用
- 断言失败不终止测试（非 fail-fast），收集所有结果
- 集成到 agent_service.py 的测试执行流程

**Out of Scope:**
- 断言方法发现 API（Phase 23 已完成）
- 断言配置 UI（Phase 24 已完成）
- 断言结果展示在测试报告中（Phase 26 E2E 验证）
- 断言结果持久化到数据库（未来需求）

</domain>

<decisions>
## Implementation Decisions

### Headers 解析策略
- **位置**: 扩展现有 `external_precondition_bridge.py` 模块
- **函数**: 新增 `resolve_headers(identifier: str) -> dict` 函数
- **实时解析**: 每次断言执行时调用 `ImportApi.headers()` 实时解析，不缓存
- **标识符列表**: main, idle, vice, special, platform, super, camera
- **调用链**: `execute_assertion_method()` → `resolve_headers()` → `ImportApi.headers()`

### AssertionError 捕获与结果提取
- **捕获策略**: 捕获 AssertionError 并解析消息提取字段级结果
- **解析方式**: 使用正则匹配已知格式（需研究 PcAssert 实际消息格式）
- **提取字段**: 字段名、期望值、实际值、是否通过
- **示例格式**: "字段 xxx 期望 xxx 实际 xxx" 或类似格式
- **降级处理**: 如果正则匹配失败，保留完整消息作为 description

### 断言执行时机与集成点
- **执行时机**: Agent 完成所有步骤后执行业务断言
- **集成位置**: 在 `agent_service.py` 的 run 方法末尾
- **触发方式**: 直接调用断言执行函数，不需要独立服务或事件机制
- **前置条件**: 确保 context 中已有 assertions 配置数据

### Context 存储结构
- **变量命名**: 使用数组索引命名：`assertion_result_0`, `assertion_result_1` 等
- **单条结果结构**:
  ```python
  {
      "passed": bool,           # 整体是否通过
      "method": str,            # 断言方法名
      "class_name": str,        # 断言类名 (PcAssert/MgAssert/McAssert)
      "field_results": [        # 字段级结果列表
          {
              "field": str,     # 字段名
              "expected": Any,  # 期望值
              "actual": Any,    # 实际值
              "passed": bool    # 该字段是否通过
          }
      ],
      "duration": float,        # 执行耗时（秒）
      "error": str | None       # 执行错误（如有）
  }
  ```
- **总结果变量**: `context['assertion_results']` 存储所有断言结果摘要
  ```python
  {
      "total": int,         # 断言总数
      "passed": int,        # 通过数
      "failed": int,        # 失败数
      "errors": int         # 执行错误数
  }
  ```

### 错误分类
- **执行错误**: TypeError, TimeoutError, ImportError 等 → `error_type` 字段
- **断言失败**: AssertionError → `passed: False` + `field_results`
- **API 错误**: 外部模块返回错误 → 记录到 `error` 字段

### Claude's Discretion
- AssertionError 消息的正则表达式具体实现
- ImportApi.headers() 的调用方式（需研究 webseleniumerp 源码）
- 超时错误的具体处理方式（是否重试）
- 执行错误时的日志级别和格式

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 架构设计参考
- `.planning/research/ARCHITECTURE.md` — ExternalPreconditionBridge 架构设计、Anti-Patterns、集成检查清单
- `.planning/research/PITFALLS.md` — 断言集成陷阱（Pitfall A1-A5）、Headers 解析、data 参数、i/j/k 分离
- `.planning/research/STACK.md` — 断言系统集成技术栈、方法签名模式、执行流程

### 现有代码参考
- `backend/core/external_precondition_bridge.py` — 需扩展支持断言执行
  - `load_base_assertions_class()` — 断言类加载（已实现）
  - `execute_data_method()` — 执行模式参考（30s 超时、错误处理）
  - 需新增 `resolve_headers()` 和 `execute_assertion_method()`
- `backend/core/agent_service.py` — 需集成断言执行
  - `run()` 方法末尾添加断言执行逻辑
- `backend/core/precondition_service.py` — 前置条件服务参考
  - `ContextWrapper` — context 存储接口

### 前置阶段参考
- `.planning/phases/23-backend-assertion-discovery/23-CONTEXT.md` — Phase 23 决策（API 响应结构、headers_options、data_options）
- `.planning/phases/24-frontend-assertion-ui/24-CONTEXT.md` — Phase 24 决策（AssertionConfig 结构、UI 集成）
- `.planning/phases/17-后端数据获取桥接/17-CONTEXT.md` — Phase 17 决策（execute_data_method 模式）
- `.planning/phases/14-后端桥接模块/14-CONTEXT.md` — Phase 14 决策（桥接模块模式、错误处理）

### 外部项目结构
- `webseleniumerp/common/base_assertions.py` — PcAssert/MgAssert/McAssert 断言类
- `webseleniumerp/common/base_assert.py` — BaseAssert 基类
- `webseleniumerp/common/import_api.py` — ImportApi.headers() 方法（需确认实际位置）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `load_base_assertions_class()` — 已加载 PcAssert/MgAssert/McAssert
  - `execute_data_method()` — 执行模式：30s 超时、asyncio.wait_for、错误分类
  - `configure_external_path()` — 路径配置可复用
  - 单例缓存模式可复用
- `backend/core/agent_service.py`:
  - `run()` 方法 — 断言执行集成点
  - SSE 事件推送模式可复用
- `backend/core/precondition_service.py`:
  - `ContextWrapper` — context 字典接口，`context['var']` 语法

### Established Patterns
- **执行模式**: `asyncio.wait_for(loop.run_in_executor(...), timeout=30)`
- **错误分类**: success, error_type (TimeoutError, ParameterError, ExecutionError)
- **Context 存储**: ContextWrapper 字典接口
- **日志记录**: logger.error() with exc_info=True

### Integration Points
- `backend/core/external_precondition_bridge.py` — 需新增:
  - `resolve_headers(identifier: str) -> dict`
  - `execute_assertion_method(config: AssertionConfig, context: dict) -> dict`
- `backend/core/agent_service.py`:
  - `run()` 方法末尾 — 调用断言执行
- `backend/api/routes/runs.py`:
  - 可能需要更新 SSE 事件格式（断言进度）

### 需要新增的代码
| 组件 | 目的 | 参考模式 |
|------|------|----------|
| `resolve_headers()` | 解析标识符为 token 字典 | 调用 ImportApi.headers() |
| `execute_assertion_method()` | 执行断言方法 + 超时保护 | 复制 `execute_data_method()` |
| `_parse_assertion_error()` | 解析 AssertionError 消息 | 正则匹配 |
| Agent 集成逻辑 | 在 run() 末尾调用断言执行 | 直接调用 |

</code_context>

<specifics>
## Specific Ideas

- Headers 解析应优雅处理无效标识符（返回错误而非崩溃）
- 断言执行结果通过 SSE 推送进度（如 "执行断言 1/3..."）
- AssertionError 消息格式需在实现时研究 PcAssert 源码确认
- 断言执行失败时记录完整堆栈到日志，但只返回摘要给前端
- 支持断言执行结果的 Jinja2 变量引用（如 `{{assertion_result_0.passed}}`）

</specifics>

<deferred>
## Deferred Ideas

- 断言结果展示在测试报告中 — Phase 26 E2E 验证
- 断言结果持久化到数据库 — 未来需求
- 并行断言执行 — v1 先实现串行执行
- 断言执行预览（在配置时测试断言）— 未来优化
- 断言结果缓存（避免重复执行）— 未来优化

</deferred>

---
*Phase: 25-assertion-execution-engine*
*Context gathered: 2026-03-20*
