# Phase 58: 执行步骤展示 - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

在执行监控的 StepTimeline 中显示前置条件和断言的执行步骤，与普通 UI 步骤按实际执行顺序交错排列。只涉及实时监控页面（RunMonitor），不涉及报告详情页（Phase 59 的范围）。

</domain>

<decisions>
## Implementation Decisions

### 统一时间线数据结构
- **D-01:** 新建统一的 `TimelineItem` 联合类型（type: 'step' | 'precondition' | 'assertion' + 对应数据字段），不复用现有 Step 类型
- **D-02:** SSE 接收事件时实时将三种事件转换为 `TimelineItem` 并 append 到统一时间线数组
- **D-03:** StepTimeline 组件改为接收 `TimelineItem[]` 而非 `Step[]`

### 步骤外观与信息密度
- **D-04:** 前置条件步骤显示代码摘要（前 N 个字符 + "..."），断言步骤显示断言名称/索引标识
- **D-05:** 三类步骤用不同图标 + 不同颜色区分：前置条件（黄色/橙色 + 文件图标）、断言（绿色/紫色 + 盾牌图标）、UI 操作（保持现有蓝色）
- **D-06:** Claude 决定具体图标选择和 Tailwind 色值

### 交错排序策略
- **D-07:** 利用后端已有的按执行顺序发送事件的特性，前端 SSE 接收时直接 append 到统一时间线数组，不需要额外排序逻辑
- **D-08:** 不需要在渲染时合并排序——后端执行顺序就是展示顺序

### 点击交互与详情展示
- **D-09:** 点击前置条件步骤：展开显示完整代码 + 变量输出（variables）
- **D-10:** 点击断言步骤：展开显示断言代码 + 结果详情（field_results）
- **D-11:** 点击 UI 步骤保持现有行为（跳转截图面板）
- **D-12:** 前置条件/断言步骤不展示 AI 推理文本（reasoning）——它们是代码执行结果，无 AI 推理过程

### Claude's Discretion
- 具体图标选择（Lucide React 图标库）
- Tailwind 颜色值
- TimelineItem 类型的具体字段设计
- 代码摘要截取长度（N 个字符）
- 详情面板的展开/折叠动画

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心前端组件
- `frontend/src/components/RunMonitor/StepTimeline.tsx` — 当前步骤时间线组件，只渲染 Step[]，需改为渲染 TimelineItem[]
- `frontend/src/pages/RunMonitor.tsx` — 执行监控页面，需将统一时间线传给 StepTimeline
- `frontend/src/hooks/useRunStream.ts` — SSE hook，已接收三种事件类型到分别数组，需改为统一时间线数组
- `frontend/src/components/RunMonitor/ReasoningLog.tsx` — 推理日志组件，仅 UI 步骤需要

### 类型定义
- `frontend/src/types/index.ts` — Step/SSEPreconditionEvent/SSEApiAssertionEvent/Run 类型定义

### 后端参考（不改）
- `backend/api/routes/runs.py` (lines 56-384) — run_agent_background 函数，已按顺序发送 precondition → step → assertion SSE 事件
- `backend/db/schemas.py` — SSEPreconditionEvent/SSEApiAssertionEvent/SSEStepEvent Pydantic schema

### 后端服务（不改）
- `backend/core/precondition_service.py` — 前置条件执行服务
- `backend/core/api_assertion_service.py` — API 断言执行服务

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `StepTimeline.tsx` 的 timeline 布局结构（连接线、状态图标、duration 展示）可直接复用
- 现有状态图标映射：CheckCircle(成功) / XCircle(失败) / Loader2(运行中) / Circle(等待)
- Lucide React 图标库已引入，可直接使用 FileCode/ShieldCheck 等图标
- Tailwind CSS 用于所有样式，badge 样式已有先例（bg-blue-100 text-blue-700 等）

### Established Patterns
- SSE 事件处理在 `useRunStream.ts` hook 中集中管理
- React functional components + hooks 模式
- Tailwind CSS 样式
- 组件按功能域组织在 `frontend/src/components/RunMonitor/` 目录下

### Integration Points
- `useRunStream.ts` — SSE 事件接收处，需将事件转换为统一 TimelineItem
- `RunMonitor.tsx` — 页面组件，需将 `run.steps` 改为统一的 timeline 传给 StepTimeline
- `StepTimeline.tsx` — 核心改动点，需支持渲染三种类型的 timeline item

### 关键发现：后端不需要改动
后端 `run_agent_background` 已按执行顺序发送所有事件：
1. 前置条件循环 → SSE "precondition" 事件 (running → success/failed)
2. Agent 运行 → SSE "step" 事件 (每个浏览器操作)
3. API 断言循环 → SSE "api_assertion" 事件 (running → success/failed)
4. 外部断言 → SSE "external_assertions" 事件
5. 完成 → SSE "finished" 事件

前端 `useRunStream` 已正确接收所有三种事件到 `run.preconditions`、`run.steps`、`run.api_assertions`。纯前端改动。

</code_context>

<specifics>
## Specific Ideas

- 前置条件/断言没有截图，点击不应跳转到截图面板
- 前置条件变量输出（variables）是 dict 格式，需友好展示
- 断言的 field_results 包含各字段断言的通过/失败详情

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 58-exec-display*
*Context gathered: 2026-04-02*
