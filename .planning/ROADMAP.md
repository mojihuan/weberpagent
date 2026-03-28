# Roadmap: aiDriveUITest

## Milestone: v0.6.3 Agent 可靠性优化

**Goal:** 通过子类化 Agent + 调优内置参数 + Prompt 优化，解决 Agent 循环重试、字段误填、步骤遗漏、提交未校验等核心问题
**Created:** 2026-03-27
---

## Phases

- [ ] **Phase 48: 监控模块与 Agent 子类** - 创建 MonitoredAgent 子类和 3 个检测器（StallDetector, PreSubmitGuard, TaskProgressTracker）
- [ ] **Phase 49: 提示词优化与参数调优** - 创建 ENHANCED_SYSTEM_MESSAGE，调优 browser-use 内置参数
- [ ] **Phase 50: AgentService 集成** - 将 MonitoredAgent 集成到 AgentService，接通 step_callback
- [ ] **Phase 51: 端到端验证** - 运行 ERP 测试验证 Agent 行为改善

---

## Phase Details

### Phase 48: 监控模块与 Agent 子类
**Goal:** MonitoredAgent 子类创建完成，3 个检测器（StallDetector, PreSubmitGuard, TaskProgressTracker）实现并通过单元测试
**Depends on:** Phase 47 (v0.6.2 已完成)
**Requirements:** SUB-01, SUB-02, SUB-03, MON-01, MON-02, MON-03, MON-04, MON-05, MON-06, MON-07, MON-08
**Success Criteria** (what must be TRUE):
1. `MonitoredAgent(Agent)` 子类存在于 `backend/agent/monitored_agent.py`，重写 `_prepare_context()` 和 `_execute_actions()`
2. StallDetector 在连续 2 次同目标失败时返回 `should_intervene=True`
3. StallDetector 在连续 3 步 DOM 指纹相同（element_count + url + dom_hash）时返回 `should_intervene=True`
4. StallDetector 成功操作后重置计数器
5. PreSubmitGuard 从 task 正则提取销售金额/物流费用/金额/付款状态的期望值
6. PreSubmitGuard 检测到提交意图且字段不匹配时返回 `should_block=True`
7. PreSubmitGuard 提取不到期望值时返回 `should_block=False`
8. TaskProgressTracker 正确解析 Step N / 第N步 / - [ ] / 数字编号格式
9. TaskProgressTracker 在 remaining_steps <= remaining_tasks 时返回 level="urgent"
10. 所有新增模块单元测试通过，覆盖率 >= 80%

**Key Design Decisions:**
- **消息注入**: 重写 `_prepare_context()`，在 `super()._prepare_context()` 之后注入 `_pending_interventions`，确保消息在 context_messages 清空之后、get_messages() 之前添加
- **Action 拦截**: 重写 `_execute_actions()`，在提交 action 执行前检查 PreSubmitGuard
- **DOM 指纹**: 使用 `(element_count, url, dom_hash[:12])` 元组，避免对完整 DOM 文本计算哈希
- **step_callback 职责**: 只检测并存储干预消息到 `_pending_interventions`，不直接调用 `_add_context_message()`

**Plans:**
2/4 plans executed
- [x] 48-02: Create PreSubmitGuard with unit tests (MON-04, MON-05, MON-06) - Wave 1
- [ ] 48-03: Create TaskProgressTracker with unit tests (MON-07, MON-08) - Wave 1
- [ ] 48-04: Create MonitoredAgent subclass (SUB-01, SUB-02, SUB-03) - Wave 2

### Phase 49: 提示词优化与参数调优
**Goal:** ENHANCED_SYSTEM_MESSAGE 创建完成并通过 extend_system_message 注入，browser-use 内置参数已调优
**Depends on:** None (可与 Phase 48 并行)
**Requirements:** PRM-01, PRM-02, PRM-03, PRM-04, PRM-05, TUNE-01, TUNE-02, TUNE-03, TUNE-04
**Success Criteria** (what must be TRUE):
1. ENHANCED_SYSTEM_MESSAGE 包含 click-to-edit 模式说明
2. ENHANCED_SYSTEM_MESSAGE 包含失败恢复强制规则（2 次失败后切换策略）
3. ENHANCED_SYSTEM_MESSAGE 包含字段填写后验证指导
4. ENHANCED_SYSTEM_MESSAGE 包含提交前校验规则
5. ENHANCED_SYSTEM_MESSAGE 通过 `extend_system_message` 参数注入（替换 CHINESE_ENHANCEMENT）
6. `loop_detection_window=10`, `max_failures=4`, `planning_replan_on_stall=2` 参数已配置
7. `enable_planning=True` 已确认开启

**Plans:**
- [ ] 49-01: Create ENHANCED_SYSTEM_MESSAGE (PRM-01~05) - Wave 1
- [ ] 49-02: Configure browser-use parameter tuning (TUNE-01~04) - Wave 1

### Phase 50: AgentService 集成
**Goal:** AgentService 使用 MonitoredAgent，step_callback 接通 3 个检测器，干预消息正确注入
**Depends on:** Phase 48, Phase 49
**Requirements:** INTEG-01, INTEG-02, INTEG-03, INTEG-04, INTEG-05
**Success Criteria** (what must be TRUE):
1. `run_with_streaming()` 创建 MonitoredAgent 实例替代原生 Agent
2. 3 个检测器实例在 Agent 创建前初始化，传入 MonitoredAgent
3. step_callback 调用 StallDetector.check() 和 TaskProgressTracker.check_progress()
4. 干预消息存储到 `_pending_interventions`（由 _prepare_context 注入）
5. 干预消息通过 run_logger.log(category="monitor") 记录
6. extend_system_message 传入 ENHANCED_SYSTEM_MESSAGE

**Plans:**
- [ ] 50-01: Integrate MonitoredAgent into AgentService (INTEG-01, INTEG-02, INTEG-05) - Wave 1
- [ ] 50-02: Wire step_callback with detectors and logging (INTEG-03, INTEG-04) - Wave 2

### Phase 51: 端到端验证
**Goal:** ERP 销售出库测试验证 Agent 行为改善，所有单元测试通过
**Depends on:** Phase 50
**Requirements:** VAL-01, VAL-02, VAL-03, VAL-04
**Success Criteria** (what must be TRUE):
1. 所有新增模块单元测试通过，覆盖率 >= 80%
2. ERP 销售出库测试中 Agent 不再对同一元素重复失败超过 2 次
3. per-run 日志中出现 category="monitor" 条目
4. 提交前有 PreSubmitGuard 拦截记录

**Plans:**
- [ ] 51-01: Run unit tests and verify coverage (VAL-01) - Wave 1
- [ ] 51-02: E2E verification with ERP test case (VAL-02, VAL-03, VAL-04) - Wave 2

## Progress
**Execution Order:**
Phase 48 + Phase 49 (parallel) → Phase 50 → Phase 51

| Phase | Milestone | Plans | Status |
|-------|-----------|-------|--------|
| 48. 监控模块与 Agent 子类 | 2/4 | In Progress|  |
| 49. 提示词优化与参数调优 | v0.6.3 | 0/2 | Pending |
| 50. AgentService 集成 | v0.6.3 | 0/2 | Pending |
| 51. 端到端验证 | v0.6.3 | 0/2 | Pending |

---

## Previous Milestone: v0.6.2 回归原生 browser-use (Complete)

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 45. 代码移除 | v0.6.2 | 5/5 | Complete | 2026-03-26 |
| 46. 代码简化与测试 | v0.6.2 | 2/2 | Complete | 2026-03-26 |
| 47. 验证 | v0.6.2 | 0/1 | Complete | 2026-03-26 |

---

## Coverage
| Requirement | Phase | Status |
|-------------|-------|--------|
| SUB-01 | Phase 48 | Pending |
| SUB-02 | Phase 48 | Pending |
| SUB-03 | Phase 48 | Pending |
| TUNE-01 | Phase 49 | Pending |
| TUNE-02 | Phase 49 | Pending |
| TUNE-03 | Phase 49 | Pending |
| TUNE-04 | Phase 49 | Pending |
| MON-01 | Phase 48 | Pending |
| MON-02 | Phase 48 | Pending |
| MON-03 | Phase 48 | Pending |
| MON-04 | Phase 48 | Pending |
| MON-05 | Phase 48 | Pending |
| MON-06 | Phase 48 | Pending |
| MON-07 | Phase 48 | Pending |
| MON-08 | Phase 48 | Pending |
| PRM-01 | Phase 49 | Pending |
| PRM-02 | Phase 49 | Pending |
| PRM-03 | Phase 49 | Pending |
| PRM-04 | Phase 49 | Pending |
| PRM-05 | Phase 49 | Pending |
| INTEG-01 | Phase 50 | Pending |
| INTEG-02 | Phase 50 | Pending |
| INTEG-03 | Phase 50 | Pending |
| INTEG-04 | Phase 50 | Pending |
| INTEG-05 | Phase 50 | Pending |
| VAL-01 | Phase 51 | Pending |
| VAL-02 | Phase 51 | Pending |
| VAL-03 | Phase 51 | Pending |
| VAL-04 | Phase 51 | Pending |
**Total v0.6.3:** 26/26 requirements mapped (100%)
---
*Roadmap updated: 2026-03-27 - Milestone v0.6.3 roadmap created*
