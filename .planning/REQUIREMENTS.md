# Requirements: v0.6.3 Agent 可靠性优化

**Milestone:** v0.6.3
**Goal:** 通过子类化 Agent + 调优内置参数 + Prompt 优化，解决 Agent 循环重试、字段误填、步骤遗漏、提交未校验等核心问题
**Created:** 2026-03-27

---

## Problem Context

**背景:** 运行记录 `outputs/7fcea593` 暴露了 5 个核心问题

**问题:**
1. 表格 click-to-edit 单元格不可见 — Ant Design 表格 `<td>` 在 DOM 快照中为空
2. 循环重试同一失败操作 — Agent 对同一 index 连续失败 12 步
3. 值被误填到其他字段 — 150 被填入物流费用字段
4. 步骤遗漏 — 30 步限制中前面浪费太多步数
5. 提交前校验形同虚设 — 多个字段未正确填写就点了确认

**源码分析关键发现:**
- browser-use `_add_context_message()` 存在，但 step_callback 中注入的消息会在下一步被 `prepare_step_state()` 清空
- browser-use 已有内置循环检测（阈值 5/8/12），但偏弱
- browser-use 有内置 Planning 系统（`enable_planning=True`），可利用重规划能力
- step_callback 无法阻止 action 执行

**决策:** 子类化 Agent + 调优内置参数 + Prompt 优化，不侵入 browser-use 源码

---

## In Scope (This Milestone)

### SUBCLASS — Agent 子类化

- [ ] **SUB-01**: 创建 `MonitoredAgent(Agent)` 子类，重写 `_prepare_context()` 在内置 nudge 之后注入自定义干预消息
- [ ] **SUB-02**: step_callback 只负责检测和存储干预消息到 `_pending_interventions`，不直接调用 `_add_context_message`
- [ ] **SUB-03**: 重写 `_execute_actions()` 实现 PreSubmitGuard 的 action 拦截（阻止提交 click 执行）

### TUNE — 内置参数调优

- [ ] **TUNE-01**: 将 `loop_detection_window` 从默认 20 降到 10，加速循环检测
- [ ] **TUNE-02**: 将 `max_failures` 从默认 5 降到 4，更早触发失败处理
- [ ] **TUNE-03**: 将 `planning_replan_on_stall` 从默认 3 降到 2，更激进触发重规划
- [ ] **TUNE-04**: 验证 `enable_planning=True`（默认）已开启，利用内置 Planning 系统的重规划能力

### MONITOR — 监控模块

- [x] **MON-01**: StallDetector 检测连续 2 次对同一 target_index 执行相同 action 且 evaluation 含失败关键词
- [x] **MON-02**: StallDetector 检测连续 3 步 DOM 指纹完全相同（页面无变化），使用轻量指纹（element_count + url + dom_hash 前 12 位）
- [x] **MON-03**: StallDetector 成功操作后重置连续失败计数器
- [x] **MON-04**: PreSubmitGuard 从 task 描述正则提取期望值（销售金额、物流费用、金额、付款状态）
- [x] **MON-05**: PreSubmitGuard 在 step_callback 中检测提交意图（click + 确认/提交/保存），通过 `_execute_actions()` 拦截并注入校验报告
- [x] **MON-06**: PreSubmitGuard 正则提取不到期望值时跳过校验，不阻塞流程
- [x] **MON-07**: TaskProgressTracker 从 task 描述解析结构化步骤列表（支持 Step N、第N步、- [ ]、数字编号格式）
- [x] **MON-08**: TaskProgressTracker 剩余步数 < 剩余任务 * 1.5 时发出 warning，<= 剩余任务时发出 urgent

### PROMPT — 提示词优化

- [ ] **PRM-01**: ENHANCED_SYSTEM_MESSAGE 包含 click-to-edit 模式说明（click td → 等待 input → input 值）
- [ ] **PRM-02**: ENHANCED_SYSTEM_MESSAGE 包含失败恢复强制规则（2 次失败后禁止重试，强制使用 evaluate/find_elements/滚动）
- [ ] **PRM-03**: ENHANCED_SYSTEM_MESSAGE 包含字段填写后立即验证指导（截图确认值已正确填入）
- [ ] **PRM-04**: ENHANCED_SYSTEM_MESSAGE 包含提交前完整校验规则
- [ ] **PRM-05**: 通过 `extend_system_message` 参数注入（替换现有 `CHINESE_ENHANCEMENT`）

### INTEG — 集成

- [ ] **INTEG-01**: AgentService.run_with_streaming() 使用 MonitoredAgent 替代原生 Agent
- [ ] **INTEG-02**: 创建 3 个检测器实例（StallDetector, PreSubmitGuard, TaskProgressTracker），传入 MonitoredAgent
- [ ] **INTEG-03**: step_callback 中调用 StallDetector.check() 和 TaskProgressTracker.check_progress()，结果存入 `_pending_interventions`
- [ ] **INTEG-04**: 干预消息通过结构化日志记录（category="monitor"），便于排查
- [ ] **INTEG-05**: extend_system_message 传入 ENHANCED_SYSTEM_MESSAGE

### VALID — 验证

- [ ] **VAL-01**: 所有新增模块的单元测试覆盖率 >= 80%
- [ ] **VAL-02**: 端到端验证：运行 ERP 销售出库测试，确认 Agent 不再对同一元素重复失败超过 2 次
- [ ] **VAL-03**: 端到端验证：日志中出现 "monitor" 类别条目，干预消息被正确注入
- [ ] **VAL-04**: 端到端验证：提交前有字段校验拦截

---

## Out of Scope

| Item | Reason |
|------|--------|
| 侵入修改 browser-use 源码 | 通过子类化和公开 API 实现 |
| 更换 LLM 模型 | 保持 Qwen 3.5 Plus，通过工程手段弥补 |
| 通用 ERP 适配 | JS 校验脚本针对当前目标 ERP 适配 |

---

## Success Criteria

1. MonitoredAgent 子类正确注入干预消息到 LLM 上下文
2. StallDetector 在 2 次连续失败后生成干预消息
3. PreSubmitGuard 在提交前拦截并校验关键字段
4. TaskProgressTracker 在步数紧张时发出预警
5. ENHANCED_SYSTEM_MESSAGE 通过 extend_system_message 注入
6. 端到端测试验证 Agent 行为改善

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| SUB-01 | Phase 48 | Pending |
| SUB-02 | Phase 48 | Pending |
| SUB-03 | Phase 48 | Pending |
| TUNE-01 | Phase 49 | Pending |
| TUNE-02 | Phase 49 | Pending |
| TUNE-03 | Phase 49 | Pending |
| TUNE-04 | Phase 49 | Pending |
| MON-01 | Phase 48 | Complete |
| MON-02 | Phase 48 | Complete |
| MON-03 | Phase 48 | Complete |
| MON-04 | Phase 48 | Complete |
| MON-05 | Phase 48 | Complete |
| MON-06 | Phase 48 | Complete |
| MON-07 | Phase 48 | Complete |
| MON-08 | Phase 48 | Complete |
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

---

*Requirements for milestone v0.6.3*
*Created: 2026-03-27*
