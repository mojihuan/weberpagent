# Phase 126: API 层与安全审查 - Context

**Gathered:** 2026-05-03
**Status:** Ready for planning

<domain>
## Phase Boundary

审查所有 API 路由文件的参数验证缺陷、错误处理遗漏和安全风险，输出具体发现清单。

**审查范围（11 个路由文件）：**
- API 路由 (`backend/api/routes/`): batches.py, dashboard.py, external_assertions.py, external_data_methods.py, external_operations.py, reports.py, run_pipeline.py, runs_routes.py, runs.py, tasks.py, __init__.py
- API 主入口 (`backend/api/main.py`): CORS 配置、异常处理、中间件
- API 响应格式 (`backend/api/response.py`): 错误码、响应结构

**不在范围内：** 后端核心业务逻辑（Phase 125 已完成）、前端（Phase 127）、代码质量/横切关注点（Phase 128）、测试规划（Phase 129）、任何代码修改。

**与 Phase 125 的关系：**
- run_pipeline.py 在 Phase 125 已做深度逻辑审查（32 条发现）
- Phase 126 对 run_pipeline.py 补充审查 API 层面（参数校验、HTTP 状态码、SSE 流异常处理），不重复业务逻辑发现
- CONCERNS.md 已记录的安全问题做验证确认，不重复记录

</domain>

<decisions>
## Implementation Decisions

### 审查范围
- **D-01:** run_pipeline.py — 补充审查 API 层面（参数校验、HTTP 状态码、SSE 流异常处理），Phase 125 的业务逻辑发现不重复
- **D-02:** CONCERNS.md 已记录的安全问题（CORS `*`、无认证、堆栈泄露等）做验证确认，验证结果在 FINDINGS.md 中引用而非重写

### 安全评估标准
- **D-03:** 所有安全问题按「公网部署」严格标准评估严重程度，即使当前是单用户内部工具。这样未来多用户部署时有现成清单。每个安全发现附带「当前影响」和「公网影响」双重评估

### 审查策略
- **D-04:** 路由文件按风险分 3 级：P1（涉及代码执行/外部模块的路由：batches, run_pipeline, runs_routes, external_*）、P2（一般 CRUD 路由：tasks, runs, reports）、P3（简单路由：dashboard）
- **D-05:** 采用「广度优先 + 聚焦深潜」策略，与 Phase 125 一致 — 先对所有路由文件快速扫描标记风险等级，然后对高优先级文件做深度逐行审查
- **D-06:** 审查重点：(1) 参数验证缺陷、(2) 错误处理遗漏、(3) 安全风险（路径遍历、CSRF、exec() 安全、不安全配置、SSRF）、(4) SSE 流异常处理

### 输出格式
- **D-07:** 审查发现输出到 `126-FINDINGS.md`，延续 Phase 125 的 4 级严重程度分级（Critical/High/Medium/Low）和类别标签（Correctness/Security/Architecture/Performance）
- **D-08:** 计划拆分为 3 个 plan，与 Phase 125 一致：Plan 1 广度扫描、Plan 2 P1 深潜、Plan 3 P2+P3+总结

### Claude's Discretion
- 广度扫描时每个路由文件的具体风险评分标准
- P1/P2/P3 的具体文件分配（建议由广度扫描结果决定最终分配）
- 具体安全检查项的执行顺序和深度

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目规划
- `.planning/PROJECT.md` — 项目愿景、技术栈、关键决策历史
- `.planning/ROADMAP.md` — Phase 126 定义和成功标准
- `.planning/STATE.md` — 当前项目状态

### Phase 125 产出（必须参考）
- `.planning/phases/125-backend-core-review/125-FINDINGS.md` — Phase 125 的 32 条发现，其中包含 run_pipeline.py 的业务逻辑发现和 CONCERNS.md 验证结果
- `.planning/phases/125-backend-core-review/125-CONTEXT.md` — Phase 125 审查策略和决策

### 代码库分析
- `.planning/codebase/CONCERNS.md` — 已知安全问题和风险（CORS、无认证、堆栈泄露、凭据嵌入、exec()、fire-and-forget）— Phase 126 需验证这些并补充新发现
- `.planning/codebase/ARCHITECTURE.md` — API Layer 架构、数据流、错误处理策略、横切关注点（认证、CORS、SSE）
- `.planning/codebase/STRUCTURE.md` — 目录结构和文件用途
- `.planning/codebase/CONVENTIONS.md` — 代码规范约定（API 响应格式、错误处理模式）
- `.planning/codebase/INTEGRATIONS.md` — 外部集成细节（external_* 路由相关）
- `.planning/codebase/STACK.md` — 技术栈依赖

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **125-FINDINGS.md 已有框架** — 严重程度分级、类别标签、风险矩阵格式可直接沿用
- **CONCERNS.md Security Considerations 段** — 已记录 6 个安全问题，作为 Phase 126 验证起点

### Established Patterns
- **API 响应格式**: `{"success": true, "data": {...}}` / `{"success": false, "error": {"code", "message"}}` — 审查时验证所有端点是否一致
- **全局异常处理**: `backend/api/main.py` 中 HTTPException、RequestValidationError、通用 Exception 处理器 — 审查是否有绕过全局处理器的情况
- **Repository Pattern**: Route -> Service -> Repository — 审查是否有路由直接访问数据库
- **Pydantic schemas**: `backend/db/schemas.py` + `backend/api/schemas/` — 审查参数验证是否完整

### Integration Points
- `run_pipeline.py` — API 层与 core 层的核心集成点，Phase 125 已审查逻辑正确性
- `batches.py` — 批量执行入口，fire-and-forget 模式
- `external_*` 路由 — 外部模块调用入口，涉及 exec() 和动态代码执行

</code_context>

<specifics>
## Specific Ideas

- 审查是 review-only：只输出发现和建议，不做代码修改
- 测试套件已删除（v0.11.0），项目当前无自测能力
- Phase 125 已验证的 CONCERNS.md 安全问题不重复记录，但需确认其严重程度评估是否需要更新（按公网标准重新评估）
- API 主入口 (`backend/api/main.py`) 的 CORS 配置和全局异常处理应纳入审查范围
- 外部集成路由（external_assertions, external_data_methods, external_operations）是最关键的安全审查对象，涉及 exec() 和外部代码执行
- SSE 流端点 (`GET /api/runs/{run_id}/stream`) 的异常处理和连接管理需要特别关注

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 126-api*
*Context gathered: 2026-05-03*
