# Phase 39: 循环干预优化 (基础) - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

实现更早的循环干预机制和增强的日志输出，当 Agent 执行过程中检测到循环行为（stagnation >= 5）时：
1. 通过 step callback 注入提示信息，让 Agent 尝试不同方法
2. 记录完整的诊断信息（循环状态值、动作序列、页面快照）
3. 在报告中展示循环干预记录

**不包含：**
- 修改 browser-use 核心库
- 表格元素定位增强（Phase 40）
- 配置化参数（Phase 41）

</domain>

<decisions>
## Implementation Decisions

### D-01: 干预策略
- **触发条件**: stagnation >= 5（连续 5 次页面无变化）
- **干预方式**: 通过 `register_new_step_callback` 检测循环，返回提示信息注入到 Agent 上下文
- **提示内容**: 建议尝试不同方法、检查页面元素、考虑跳过当前步骤
- **重试限制**: 最多重试 2 次，超过后跳过当前困难步骤

### D-02: 诊断日志内容
循环检测触发时记录以下信息：
1. **循环状态值**
   - `stagnation`: 当前连续停滞次数
   - `max_repetition_count`: 最高动作重复次数
   - `most_repeated_hash`: 最常重复的动作 hash
2. **最近动作序列**（最近 5-10 次）
   - 动作类型（click/input/navigate/scroll 等）
   - 动作参数摘要
3. **页面状态快照**
   - 当前 URL
   - 页面标题
   - DOM 结构 hash
   - 可点击元素数量

### D-03: 报告展示方式
- 在 `steps` 表中添加 `loop_intervention` 字段（JSON 类型）
- 存储完整的诊断信息 JSON
- 前端在步骤详情中展示循环干预标记和诊断信息
- 需要数据库迁移

### D-04: 实现位置
- 在 `backend/core/agent_service.py` 的 `run_with_streaming` 方法中实现
- 通过 `step_callback` 检测 `browser_state` 中的循环状态
- 使用现有的日志系统记录诊断信息

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### browser-use 循环检测机制
- `.venv/lib/python3.11/site-packages/browser_use/agent/views.py` — `ActionLoopDetector` 类实现，包含 `stagnation` 追踪和 `get_nudge_message()` 方法

### 项目现有代码
- `backend/core/agent_service.py` — AgentService 封装，包含 `run_with_streaming` 和 `step_callback` 实现
- `backend/agent/browser_agent.py` — UIBrowserAgent 封装，包含 `_on_step` 回调示例
- `backend/db/models.py` — Step 模型定义，需要添加 `loop_intervention` 字段

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ActionLoopDetector` (browser-use): 已有完整的循环检测逻辑，包括 `consecutive_stagnant_pages` 和 `max_repetition_count` 追踪
- `step_callback` (agent_service.py): 已有回调机制，可访问 `browser_state` 和 `agent_output`
- `StepRepository`: 已有数据库操作封装，可扩展支持新字段

### Established Patterns
- 数据库迁移使用 Alembic
- 日志使用 Python logging 模块
- 异步回调使用 `asyncio.iscoroutinefunction()` 检测

### Integration Points
- `run_with_streaming()` 方法中的 `step_callback` 是主要集成点
- Step 模型需要添加字段并更新 repository
- 前端报告页面需要展示新字段

</code_context>

<specifics>
## Specific Ideas

- 提示信息示例: "检测到连续 5 次相同页面状态。请尝试：1) 滚动页面查看更多元素 2) 使用不同的选择器 3) 如果当前步骤非关键，考虑跳过"
- 重试 2 次后仍未成功时，自动标记为 `loop_intervention_failed` 并继续执行后续步骤

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 39-loop-intervention-basics*
*Context gathered: 2026-03-24*
