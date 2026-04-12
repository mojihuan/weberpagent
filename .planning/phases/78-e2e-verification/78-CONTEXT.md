# Phase 78: E2E Verification - Context

**Gathered:** 2026-04-12
**Status:** Ready for planning

<domain>
## Phase Boundary

E2E 验证 — 验证 v0.9.1 完整集成链路：Excel导入 → 前置API(含缓存) → AI执行UI → 断言(含缓存验证)。通过 Mock 集成测试验证流程编排正确性，不依赖外部 LLM/API。

不涉及：CacheService/AccountService/TestFlowService 内部实现修改（Phases 74-77 已交付），新增功能代码。

</domain>

<decisions>
## Implementation Decisions

### 登录角色
- **D-01:** ROADMAP.md Success Criteria #1 中的 `login_role="admin"` 有误，实际使用 `login_role="main"`（7 种有效角色：main/special/vice/camera/platform/super/idle，无 admin）

### 验证方式
- **D-02:** 采用 **Mock 集成测试**而非真实 E2E — Mock AgentService/LLM 外部依赖，验证流程编排（登录注入 → 缓存传递 → 变量替换 → 断言验证）正确性
- **D-03:** 不依赖真实 ERP 环境，避免外部 API/网络不稳定导致测试失败
- **D-04:** Mock 粒度：Mock AgentService 的 run_with_cleanup() 返回成功结果，Mock AccountService.resolve() 返回预设 AccountInfo

### 销售出库场景设计
- **D-05:** 重点验证**缓存传递链路** — 前置条件通过 context.cache() 存储数据 → {{cached:key}} 变量替换 → Agent 收到完整描述 → 断言通过 context.cached() 读取缓存值
- **D-06:** 场景覆盖：login_role="main" → 自动登录注入 → 前置条件缓存 → 变量替换 → Agent 执行 → 断言验证

### 回归测试范围
- **D-07:** 78-02 核心回归覆盖两个场景：(1) 无 login_role 任务走现有路径无回归 (2) 报告生成包含完整步骤记录且登录/业务步骤顺序正确
- **D-08:** 批量执行传递和旧 Excel 模板兼容不在此 Phase 覆盖 — 推迟到 v2 或实际使用时验证

### ROADMAP 修正
- **D-09:** Success Criteria #1 修正为 `login_role="main"`，与 AccountService ROLE_MAP 一致

### Claude's Discretion
- Mock 的具体实现方式（unittest.mock vs pytest-mock）
- 测试文件组织结构
- 断言验证的具体检查点
- Mock AgentService 返回结果的数据结构

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心源码（测试目标）
- `backend/api/routes/runs.py` — `run_agent_background()` (lines 55-394)，login_role 分支逻辑
- `backend/api/routes/batches.py` — `run_configs` dict，login_role 传递
- `backend/core/test_flow_service.py` — TestFlowService 全部 API
- `backend/core/cache_service.py` — CacheService API
- `backend/core/account_service.py` — AccountService API

### 已有测试（参考模式）
- `backend/tests/unit/test_runs_login_role_integration.py` — 5 个集成测试覆盖 login_role 分支
- `backend/tests/unit/test_cache_service.py` — CacheService 单元测试
- `backend/tests/unit/test_account_service.py` — AccountService 单元测试
- `backend/tests/unit/test_test_flow_service.py` — TestFlowService 单元测试

### 数据模型
- `backend/models/task.py` — Task model login_role 字段
- `backend/schemas/task.py` — TaskCreate/TaskResponse schema

### 前置阶段参考
- `.planning/phases/77-testflowservice-runs-py-integration/77-CONTEXT.md` — TestFlowService 架构决策、数据流
- `.planning/phases/74-cacheservice-contextwrapper/74-CONTEXT.md` — CacheService API 决策
- `.planning/phases/75-accountservice-settings/75-CONTEXT.md` — AccountService 角色列表

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `test_runs_login_role_integration.py`: 已有 5 个集成测试使用 `unittest.mock.patch` Mock AgentService，可直接扩展
- `test_cache_service.py`: CacheService 完整测试，双向 deepcopy 验证
- `test_test_flow_service.py`: TestFlowService 单元测试，build_login_prefix + _build_description 覆盖

### Established Patterns
- 集成测试使用 `unittest.mock.patch` + `AsyncMock`
- 测试在 `backend/tests/unit/` 或 `backend/tests/integration/`
- `pytest-asyncio` 用于异步测试
- Mock AgentService: `patch("backend.api.routes.runs.AgentService")` 或 `patch("backend.api.routes.runs.agent_service")`

### Integration Points (Mock 验证点)
1. `run_agent_background()` login_role 分支 → AccountService.resolve() 调用
2. CacheService 创建 → 传入 PreconditionService 和断言 ContextWrapper
3. TestFlowService._build_description() → 登录前缀 + regex 替换 + Jinja2 替换
4. AgentService.run_with_cleanup() → 接收的 description 包含登录步骤
5. 断言阶段 ContextWrapper → 通过 cached() 读取前置缓存数据

### 关键数据流（Mock 验证路径）
```
run_agent_background(login_role="main")
  ├─ [verify] AccountService.resolve("main") called
  ├─ [verify] CacheService() created
  ├─ [verify] PreconditionService receives shared CacheService
  ├─ [verify] TestFlowService._build_description() output contains login prefix
  ├─ [verify] {{cached:key}} replaced with cached value
  ├─ [verify] AgentService.run_with_cleanup() called with full description
  └─ [verify] assertion ContextWrapper.cached() returns precondition cached data
```

</code_context>

<specifics>
## Specific Ideas

- 78-01 测试场景：模拟销售出库完整链路（前置缓存订单号 → 变量替换 → Agent 执行 → 断言读取缓存）
- 78-02 回归测试：login_role=None 任务走现有路径 + 报告步骤顺序验证
- ROADMAP Success Criteria #1 "admin" → "main" 需在 plan 中修正
- 测试不依赖外部服务，全部 Mock，可在 CI 中运行

</specifics>

<deferred>
## Deferred Ideas

- 真实 ERP 环境 E2E 测试 — 需要部署环境 + 真实账号，推迟到手动验证
- 批量执行 + login_role 传递验证 — 推迟到实际使用时或 v2
- 旧 Excel 模板（6 列无 login_role）导入兼容 — 推迟到实际使用时
- 性能/并发测试 — 超出 Phase 78 范围
- 多角色场景验证（special/vice/camera 等）— 核心链路验证 main 即可，其他角色结构相同

</deferred>

---
*Phase: 78-e2e-verification*
*Context gathered: 2026-04-12*
