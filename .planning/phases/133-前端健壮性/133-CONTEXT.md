# Phase 133: 前端健壮性 - Context

**Gathered:** 2026-05-04
**Status:** Ready for planning

<domain>
## Phase Boundary

修复前端 SSE 连接的健壮性、性能和正确性：JSON.parse 无保护导致连接崩溃、长时间运行 O(n^2) 性能退化、isConnected 虚假显示已连接。

**Scope:**
- MEM-03: useRunStream steps/timeline 数组使用 ref-based 可变数组，消除 O(n^2) 拷贝
- ERR-02: useRunStream 所有 7 处 JSON.parse 添加 try/catch 保护
- ERR-04: isConnected 状态仅在 EventSource onopen 后设为 true
- STATE-02: 已验证无需修复（标记的 .push() 均为局部变量，非 React state）

**Out of scope:** 后端修复（已完成 Phase 130-132）、死代码清理（Phase 134）

</domain>

<decisions>
## Implementation Decisions

### MEM-03 ref-based 数组优化
- **D-01:** 使用 `useRef<Step[]>` 和 `useRef<TimelineItem[]>` 存储可变数组，每次 SSE 事件直接 push 不拷贝。使用 `useRef<number>` 版本计数器（每次变更 +1），消费者通过 `useMemo` + `[version]` 依赖读取最新数组。API 不变，消费者无需感知 ref 存在。

### ERR-02 JSON.parse 保护
- **D-02:** useRunStream.ts 中全部 7 处 JSON.parse（lines 44, 59, 83, 110, 126, 147, 163）包裹 try/catch。失败时 log raw data 到 console + 通过 sonner 显示 "数据解析错误" toast + skip 当前事件继续监听。
- **D-03:** SSE parse 错误采用无限容忍策略 — 无最大错误计数断连。连接仅因 EventSource.onerror 断开，不因 parse 错误主动关闭。

### ERR-04 连接状态修正
- **D-04:** 将 `setIsConnected(true)` 从 `connect()` 函数内（line 36，EventSource 构造前）移到 EventSource 的 `onopen` 回调中。确保 UI 仅在服务器确认连接后才显示"已连接"状态。

### STATE-02 范围确认
- **D-05:** 经代码侦察验证，REQUIREMENTS.md 标记的 STATE-02 所涉及 .push() 调用全部是函数局部变量（非 React state），不存在实际的 useState 直接 mutation。STATE-02 确认为 no-op，不进行任何代码修改。

### 测试策略
- **D-06:** 不添加前端单元测试（项目当前无 Vitest/Jest 配置）。通过手动验证 + 现有 Playwright E2E 测试确认修改正确。与 Phase 130-132 的 TDD 策略不同，前端修改范围小且集中在单一 hook 文件。

### Claude's Discretion
- useRef + version counter 的具体实现细节
- try/catch 中 console.error 的格式和内容
- isConnected 移到 onopen 后是否需要在 onerror 中显式设为 false
- sonner toast 的具体调用方式（项目已安装 sonner 2.0）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### SSE Hook (MEM-03, ERR-02, ERR-04)
- `frontend/src/hooks/useRunStream.ts` — 全部 216 行，SSE hook 主文件。7 处 JSON.parse (lines 44, 59, 83, 110, 126, 147, 163)、isConnected 过早设置 (line 36)、O(n^2) spread 模式 (lines 45, 60, 84, 111, 127, 148, 167)

### Hook 消费者（修改后需兼容）
- `frontend/src/pages/RunMonitor.tsx` — useRunStream 唯一消费者（133 行），解构 `{ run, disconnect }`
- `frontend/src/components/RunMonitor/StepTimeline.tsx` — 消费 `run.timeline`（286 行）
- `frontend/src/components/RunMonitor/ScreenshotPanel.tsx` — 消费 `run.steps`（131 行）
- `frontend/src/components/RunMonitor/ReasoningLog.tsx` — 消费 `run.steps`（65 行）
- `frontend/src/components/RunMonitor/RunHeader.tsx` — 消费 `status`、`timeline` 步骤计数（61 行）

### UI 设计合约
- `.planning/phases/133-前端健壮性/133-UI-SPEC.md` — SSE 错误交互合约、immutable 更新合约、MEM-03 性能合约

### 前置阶段上下文
- `.planning/phases/131-后端内存与错误处理/131-CONTEXT.md` — Phase 131 后端 SSE 修复（ERR-01 event_generator 异常保护），前端修复依赖后端事件格式正确

### 代码规范
- `.planning/codebase/CONVENTIONS.md` — 前端状态管理、SSE Streaming Pattern、Immutable State Updates 约定

### 已有依赖
- `sonner` 2.0 — toast 通知库，已在 `main.tsx` 中配置 `<Toaster />`

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `sonner` toast 库: 已安装配置，直接调用 `toast.error("数据解析错误")` 即可
- EventSource 标准 API: onopen/onerror/onmessage 回调机制，无需额外依赖
- useRef + useMemo: React 标准模式，项目已有使用（RunMonitor 中 useMemo 用于过滤 timeline）

### Established Patterns
- SSE streaming pattern: `new EventSource(url)` → event handlers → `close()` on cleanup
- Immutable state updates: `setRun(prev => ({ ...prev, steps: [...prev.steps, new] }))` — 当前正确但性能差
- Error handling: API 层用 sonner toast 通知（`client.ts` 中已有范例）
- 组件消费 pattern: RunMonitor 解构 hook 返回值，传递给子组件作为 props

### Integration Points
- `useRunStream` 返回值 `UseRunStreamReturn`: 包含 `run`, `isConnected`, `disconnect` 等 — 修改内部实现但保持 API 不变
- `run.steps` 和 `run.timeline`: 4 个子组件通过 props 消费 — ref-based 优化后这些仍需返回可消费的数组
- `RunMonitor.tsx` 的 useMemo: 依赖 `run.timeline` 做过滤排序 — ref-based 优化后需确保 useMemo 能感知变化

</code_context>

<specifics>
## Specific Ideas

- MEM-03 实现思路: 在 useRunStream 内部用 `stepsRef` 和 `timelineRef` 存储可变数组，每次事件处理器直接 push。用 `versionRef` 计数器跟踪变更次数。返回的 `run` 对象中 `steps` 和 `timeline` 通过 useMemo + version dependency 返回当前 ref 内容，消费者无需修改。
- ERR-04 实现: 移除 line 36 的 `setIsConnected(true)`，在 EventSource 构造后添加 `eventSource.onopen = () => setIsConnected(true)`。`onerror` 中已有 `setIsConnected(false)` 保持不变。
- 所有修改集中在单一文件 `useRunStream.ts`，消费者无需改动。

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---
*Phase: 133-前端健壮性*
*Context gathered: 2026-05-04*
