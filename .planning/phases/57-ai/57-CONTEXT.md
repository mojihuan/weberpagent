# Phase 57: AI 推理格式优化 - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

将 AI 推理过程中的 Eval/Verdict/Memory/Goal 文本从 `|` 分隔的单行纯文本改为分行展示，每项独占一行，带彩色 badge 标签高亮。涉及执行监控 ReasoningLog 和报告详情 StepItem 两个展示场景。

</domain>

<decisions>
## Implementation Decisions

### 解析策略
- **D-01:** 前端负责解析 reasoning 文本 — 不改后端数据格式，不改数据库存储
- **D-02:** 使用正则表达式匹配 `Eval:`, `Verdict:`, `Memory:`, `Goal:` 关键词（大小写不敏感）
- **D-03:** 按 `|` 分隔符拆分文本后逐段匹配标签 — 后端拼接格式为 `" | ".join(parts)`

### 视觉样式
- **D-04:** 每个标签用彩色 badge 展示，与现有 Action (蓝色) / Error (红色) 标签风格一致
- **D-05:** 建议配色: Eval-紫色、Verdict-绿色、Memory-橙色、Goal-蓝色（planner 可微调色值）
- **D-06:** 执行监控 (ReasoningLog) 和报告详情 (StepItem) 使用相同的标签样式和解析逻辑

### 兼容性处理
- **D-07:** 不匹配标准标签的推理文本原样展示为纯文本行
- **D-08:** 空 reasoning 或 null 值保持现有 "暂无推理记录" 展示不变
- **D-09:** 历史 data 无需 migration — 前端解析自动兼容

### Claude's Discretion
- badge 具体颜色值 (Tailwind class)
- 是否提取共享的 `ReasoningText` 解析组件
- 正则匹配的具体实现细节

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心文件
- `frontend/src/components/RunMonitor/ReasoningLog.tsx` — 执行监控推理日志组件，当前直接渲染 `step.reasoning` 纯文本
- `frontend/src/components/Report/StepItem.tsx` — 报告详情步骤组件，第 113-114 行渲染 reasoning
- `backend/core/agent_service.py` — 第 248-262 行生成 reasoning 文本 (`" | ".join(parts)`)

### 类型定义
- `frontend/src/types/index.ts` — Step 类型定义 (含 `reasoning: string | null`)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ReasoningLog.tsx` 的 Action/Error badge 模式 — 可复用 badge 样式结构（inline-flex + px-2 py-0.5 rounded text-xs font-medium）
- 两个展示场景 (ReasoningLog + StepItem) 都需要相同解析逻辑 — 适合提取共享工具函数

### Established Patterns
- Tailwind CSS 用于所有样式
- Lucide React 图标库
- React functional components + hooks

### Integration Points
- `ReasoningLog.tsx` — 需修改第 40-47 行的 reasoning 渲染区域
- `StepItem.tsx` — 需修改第 113-114 行的 reasoning 渲染区域
- 后端 `agent_service.py:262` — **不改**，仅参考其拼接格式

</code_context>

<specifics>
## Specific Ideas

- badge 配色参考现有 Action (bg-blue-100 text-blue-700) / Error (bg-red-100 text-red-700) 风格

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 57-ai*
*Context gathered: 2026-04-02*
