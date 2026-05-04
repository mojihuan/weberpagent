# Phase 133: 前端健壮性 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-04
**Phase:** 133-前端健壮性
**Areas discussed:** STATE-02 范围确认, MEM-03 优化策略, SSE 错误恢复边界, 前端测试策略

---

## STATE-02 范围确认

| Option | Description | Selected |
|--------|-------------|----------|
| 跳过，确认无问题 | 局部变量 .push() 不影响 React 渲染，不值得花时间重构 | ✓ |
| 重构为函数式写法 | 统一为 [...arr, item] 保持代码风格一致性 | |
| 全面消除所有 mutation 模式 | 搜索所有 .push()/.splice()/直接属性赋值，全部替换 | |

**User's choice:** 跳过，确认无问题
**Notes:** 代码侦察验证所有标记的 .push() 调用（DataMethodSelector:216,237, TaskForm:217, reasoningParser:26,28,30,33,38）均为函数局部变量，非 React state。STATE-02 确认为 no-op。

---

## MEM-03 ref-based 优化策略

| Option | Description | Selected |
|--------|-------------|----------|
| Ref + Version Counter | useRef 存可变数组，push 不拷贝。useRef<number> 计数器 + useMemo 触发重渲染 | ✓ |
| Ref + setState 触发 | useRef 存数组，每次变更后 setState 新对象引用。比当前好但仍创建新 run 对象 | |
| Claude 自行决定 | 只要消除 O(n^2) 并保持 API 兼容 | |

**User's choice:** Ref + Version Counter
**Notes:** 消费者只有 RunMonitor.tsx → StepTimeline/ScreenshotPanel/ReasoningLog，API 保持不变。

---

## SSE 错误恢复边界

| Option | Description | Selected |
|--------|-------------|----------|
| 无限容忍 | 每个 parse 错误 log + toast，连接不因 parse 错误断开 | ✓ |
| 最大错误计数断连 | 连续 N 次 parse 失败后自动断开 | |
| Claude 自行决定 | 自行决定边界策略 | |

**User's choice:** 无限容忍
**Notes:** SSE 连接本身有 onerror 处理断连场景。parse 错误仅影响单个事件，不应导致连接关闭。

---

## 前端测试策略

| Option | Description | Selected |
|--------|-------------|----------|
| 跳过，仅手动验证 | 修改范围小且集中在 1 个 hook 文件，无 Vitest 配置 | ✓ |
| 添加 Vitest 单元测试 | 覆盖 parse 错误、连接状态、ref-based 数组，但需配置基础设施 | |
| Claude 自行决定 | 自行决定测试策略 | |

**User's choice:** 跳过，仅手动验证
**Notes:** 项目当前无前端测试套件。Phase 130-132 的 TDD 策略用于后端 pytest。前端修改通过手动验证 + 现有 Playwright E2E 确认。

---

## Claude's Discretion

- useRef + version counter 的具体实现细节
- try/catch 中 console.error 的格式和内容
- isConnected 移到 onopen 后 onerror 中是否需显式 false
- sonner toast 的具体调用方式

## Deferred Ideas

None — discussion stayed within phase scope
