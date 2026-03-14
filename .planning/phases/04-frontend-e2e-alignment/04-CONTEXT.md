# Phase 4: Frontend + E2E Alignment - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

前后端类型对齐、UI 数据正确显示、SSE 实时更新、报告页断言结果展示、完整用户流程验证。

**包含：** TypeScript 类型同步、错误处理 UX、空状态设计、报告页布局、E2E 流程验证
**不包含：** 新功能开发、性能优化、多语言支持

</domain>

<decisions>
## Implementation Decisions

### 类型对齐策略
- **同步方式**: 手动同步（更新 types/index.ts 确保与后端 schemas 一致）
- **Run 状态值**: 使用后端值 (pending/running/completed/failed)
- **Step 字段名**: 统一使用 `step`（后端字段名）

### 错误处理 UX
- **错误展示方式**: Toast 通知
- **错误细节**: 显示完整错误详情（包括技术细节）
- **网络错误处理**: 自动重试 3 次 + toast 提示

### 空状态设计
- **任务列表空状态**: 显示"创建第一个任务" CTA
- **报告页空状态**: 显示"执行任务后查看报告" CTA
- **执行监控初始状态**: 显示"开始执行"按钮

### 报告页布局
- **断言结果展示**: 顶部摘要（通过率）+ 下方列表
- **断言失败详情**: 显示期望值 vs 实际值对比
- **截图展示**: 缩略图画廊（点击放大）

### E2E 测试范围
- **测试流程**: 仅测试正常流程（创建 → 执行 → 监控 → 报告）
- **测试级别**: 冒烟测试（smoke test），不测试边界情况
- **失败处理**: 测试失败时记录日志，不阻塞

### Claude's Discretion
- 具体组件实现细节
- 加载状态样式
- 过渡动画
- 响应式布局细节

</decisions>

<specifics>
## Specific Ideas

- 断言失败消息格式: "期望包含 'dashboard'，实际为 'login'"
- 报告通过率显示格式: "通过率: 75% (3/4)"
- Toast 使用 sonner 或 react-hot-toast 库
- 空状态使用现有 EmptyState 组件

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `frontend/src/types/index.ts`: 现有类型定义，需要更新以匹配后端
- `frontend/src/api/client.ts`: API 客户端，需要添加重试逻辑
- `frontend/src/hooks/useRunStream.ts`: SSE hook，已实现基础功能
- `frontend/src/components/shared/EmptyState.tsx`: 空状态组件，可复用
- `frontend/src/components/shared/LoadingSpinner.tsx`: 加载组件，可复用
- `frontend/src/components/Report/`: 报告组件目录，需要更新断言展示

### Established Patterns
- React + TypeScript + Vite
- Tailwind CSS for styling
- Custom hooks for data fetching (useTasks, useRunStream)
- apiClient for HTTP requests
- EventSource for SSE

### Integration Points
- 类型文件: `frontend/src/types/index.ts`
- API 客户端: `frontend/src/api/client.ts`
- 任务 API: `frontend/src/api/tasks.ts`
- 执行 API: `frontend/src/api/runs.ts`
- 报告 API: `frontend/src/api/reports.ts`
- SSE hook: `frontend/src/hooks/useRunStream.ts`

</code_context>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 范围内

</deferred>

---

*Phase: 04-frontend-e2e-alignment*
*Context gathered: 2026-03-14*
