# Phase 127: 前端审查 - Context

**Gathered:** 2026-05-03
**Status:** Ready for planning

<domain>
## Phase Boundary

审查前端 React 组件逻辑正确性和渲染性能，输出具体发现清单。

**审查范围（~60 文件，~8,900 行）：**
- 页面层 (8 文件): Dashboard.tsx, Tasks.tsx, TaskDetail.tsx, RunList.tsx, RunMonitor.tsx, BatchProgress.tsx, Reports.tsx, ReportDetail.tsx
- 组件层 (~30 文件): BatchProgress/, Dashboard/, ImportModal/, Report/, RunMonitor/, TaskDetail/, TaskList/, TaskModal/, shared/
- Hooks 层 (5 文件): useRunStream.ts, useTasks.ts, useReports.ts, useDashboard.ts, useBatchProgress.ts
- API 层 (9 文件): client.ts, tasks.ts, runs.ts, reports.ts, batches.ts, dashboard.ts, externalOperations.ts, externalDataMethods.ts, externalAssertions.ts
- 类型/工具: types/index.ts, utils/reasoningParser.ts, utils/retry.ts, constants/roleLabels.ts

**不在范围内：** 后端核心逻辑（Phase 125 已完成）、API 路由层（Phase 126 已完成）、代码质量/横切关注点（Phase 128）、测试规划（Phase 129）、任何代码修改。

**与 Phase 125/126 的关系：**
- Phase 125 审查了 event_manager.py（SSE 推送端），Phase 127 审查 useRunStream.ts（SSE 消费端），两者交叉验证
- CONCERNS.md 已记录的前端问题做验证确认，不重复记录

</domain>

<decisions>
## Implementation Decisions

### 审查范围与优先级
- **D-01:** 文件按风险分 3 级：
  - **P1（深度逐行审查）**: useRunStream.ts, DataMethodSelector.tsx, TaskForm.tsx, AssertionSelector.tsx, client.ts — SSE核心 / 最大组件(829+560+546行) / API基础设施
  - **P2（快速扫描）**: pages/*.tsx, types/index.ts, StepTimeline.tsx, TaskRow.tsx, ImportModal/*.tsx, 其他 TaskModal/*.tsx, Report/*.tsx, RunMonitor/*.tsx — 页面组件 / 中等复杂度
  - **P3（仅 lint/类型检查）**: shared/*.tsx, Dashboard/*.tsx, constants/*, utils/*, 简单 API 模块 (dashboard.ts, batches.ts 等) — 低复杂度，风险低

### SSE 边界审查深度
- **D-02:** useRunStream.ts (215行) 做深度逐行审查，覆盖所有边界场景：JSON.parse 无 try/catch、事件乱序（step 先于 started）、重复事件（step 无去重）、连接断开重连（isConnectedRef 状态不同步）、timeline 数组无限增长
- **D-03:** 与后端 event_manager.py 交叉验证 — 确认前端期望的事件格式与后端推送格式一致，验证事件类型和数据结构匹配

### 性能审查方式
- **D-04:** 采用静态代码分析，不做运行时性能测试。识别明显的性能问题：缺少 React.memo/useMemo/useCallback、大列表无虚拟化、React Query 配置不当、state 更新粒度过粗、不必要的重渲染等
- **D-05:** 重点审查 3 个超大组件（DataMethodSelector 829行、TaskForm 560行、AssertionSelector 546行）的内部状态管理和组件拆分合理性

### 审查策略
- **D-06:** 沿用 Phase 125/126 的「广度优先 + 聚焦深潜」策略 — Plan 1 广度扫描全部文件 + ESLint/TypeScript 检查，Plan 2 P1 文件深度审查，Plan 3 P2/P3 审查 + 总结

### 输出格式
- **D-07:** 审查发现输出到 `127-FINDINGS.md`，延续 Phase 125/126 的 4 级严重程度分级（Critical/High/Medium/Low）和类别标签（Correctness/Architecture/Performance/Security）

### Claude's Discretion
- 广度扫描时每个文件的具体风险评分标准
- P2 文件中发现问题时的审查深度（快速扫描转深度审查的阈值）
- ESLint/TypeScript 检查的具体命令和配置

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目规划
- `.planning/PROJECT.md` — 项目愿景、技术栈、关键决策历史
- `.planning/REQUIREMENTS.md` — v0.11.3 需求定义（CORR-03, PERF-02 对应本阶段）
- `.planning/ROADMAP.md` — Phase 127 定义和成功标准
- `.planning/STATE.md` — 当前项目状态

### Phase 125/126 产出（必须参考）
- `.planning/phases/125-backend-core-review/125-FINDINGS.md` — Phase 125 的 32 条发现，包含 event_manager.py 相关发现（SSE 推送端）
- `.planning/phases/125-backend-core-review/125-CONTEXT.md` — Phase 125 审查策略和决策
- `.planning/phases/126-api/126-FINDINGS.md` — Phase 126 的 78 条发现，包含 SSE 流端点相关发现
- `.planning/phases/126-api/126-CONTEXT.md` — Phase 126 审查策略和决策

### 代码库分析
- `.planning/codebase/ARCHITECTURE.md` — 前端架构、数据流、SSE 模式、React Query 配置
- `.planning/codebase/STRUCTURE.md` — 前端目录结构和文件用途
- `.planning/codebase/CONCERNS.md` — 已知前端问题（无前端测试、DataMethodSelector 829行等）
- `.planning/codebase/CONVENTIONS.md` — 前端代码规范（组件模式、状态管理、不可变性模式、路由约定）
- `.planning/codebase/STACK.md` — 前端技术栈依赖
- `.planning/codebase/TESTING.md` — 测试策略和前端覆盖缺口

### 前端关键文件（审查对象）
- `frontend/src/hooks/useRunStream.ts` — SSE 实时数据流 hook (215行)
- `frontend/src/components/TaskModal/DataMethodSelector.tsx` — 最大组件 (829行)
- `frontend/src/components/TaskModal/TaskForm.tsx` — 任务表单 (560行)
- `frontend/src/components/TaskModal/AssertionSelector.tsx` — 断言选择器 (546行)
- `frontend/src/api/client.ts` — HTTP 客户端 + 重试 + 错误处理
- `frontend/src/types/index.ts` — 全部 TypeScript 类型定义 (456行)
- `frontend/src/main.tsx` — React 入口（需验证 QueryClientProvider 配置）

### 后端交叉验证文件
- `backend/core/event_manager.py` — SSE 推送端（Phase 125 已审查，交叉验证用）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **125-FINDINGS.md 和 126-FINDINGS.md 框架** — 严重程度分级、类别标签、风险矩阵格式可直接沿用
- **event_manager.py 审查发现** — Phase 125 已识别 event_manager 无 cleanup 调用、内存无限增长等问题，前端审查可验证这些后端问题在前端的表现

### Established Patterns
- **SSE Streaming Pattern**: EventSource + addEventListener per event type + immutable state updates — 审查时验证所有事件类型处理的完整性和一致性
- **Custom Hook Pattern**: useState + useCallback + useEffect + useMemo — 审查时验证 hooks 的依赖数组和 cleanup 函数
- **Component Pattern**: Named function export + Tailwind CSS utility classes + TypeScript props — 审查时验证 props 类型和事件处理
- **API Client Pattern**: apiClient<T> + retry + error toast — 审查时验证错误处理的完整性和类型安全

### Integration Points
- `useRunStream.ts` ← `event_manager.py` — SSE 事件格式和数据结构必须匹配
- `api/client.ts` → 所有 API 路由 — 请求格式和错误处理必须一致
- `types/index.ts` ← `backend/db/schemas.py` — TypeScript 类型必须与后端 Pydantic schemas 匹配
- `hooks/*.ts` → `api/*.ts` — React Query hooks 的数据获取策略

</code_context>

<specifics>
## Specific Ideas

- 审查是 review-only：只输出发现和建议，不做代码修改
- 前端无测试（CONCERNS.md Priority: Low），审查无法通过测试验证发现，纯静态分析
- useRunStream.ts 的 SSE 连接管理是已知风险点 — 无自动重连、onerror 处理简单、JSON.parse 无 try/catch
- 3 个超大组件 (800+/500+ 行) 的内部状态管理复杂度需要重点关注
- main.tsx 需验证 React Query Provider 配置 — CONVENTIONS.md 提到使用 React Query，但 main.tsx 代码未见 QueryClientProvider

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 127-frontend-review*
*Context gathered: 2026-05-03*
