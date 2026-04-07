# Requirements: aiDriveUITest v0.8.4

**Defined:** 2026-04-06
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v1 Requirements

Requirements for v0.8.4 milestone. Each maps to roadmap phases.

### 行标识定位 (OPTIMIZE-01)

- [x] **ROW-01**: DOM Patch 能从 ERP 表格 `<tr>` 的子 `<td>` 文本中检测 IMEI/商品编号（正则 `I\d{15}`），提取为行标识
- [ ] **ROW-02**: DOM Patch 在 DOM dump 序列化输出中为含商品编号的行注入 `<!-- 行: {id} -->` 注释，Agent 可据此锁定目标行
- [ ] **ROW-03**: Patch 4 (`_assign_interactive_indices`) 为行内 input 添加行归属标注，Agent 可区分不同行的相同 placeholder input

### 反重复机制 (OPTIMIZE-02)

- [x] **ANTI-01**: 模块级 `_failure_tracker` 字典以 `backend_node_id` 为键（非 index）追踪失败历史，包含 count/last_error/mode 字段，并提供独立 `reset_failure_tracker()` 函数在每次 run 开始时重置
- [ ] **ANTI-02**: DOM Patch 在序列化时根据 `_failure_tracker` 为失败元素动态注入标注（已尝试N次失败、点击无响应、非目标列），且只在已失败元素上标注，避免全局策略偏差
- [ ] **ANTI-03**: step_callback 在 detector calls 区域调用 `update_failure_tracker()`，将 evaluation 失败关键词和 dom_hash 变化检测结果写入 tracker

### 策略优先级 (OPTIMIZE-03)

- [ ] **STRAT-01**: DOM Patch 基于 `snapshot_node` 存在性和 `is_visible` 状态判定三级策略——可见 input 为策略 1（原生 input），hidden input 为策略 2（click-to-edit），两次失败降级为策略 3（evaluate JS）
- [ ] **STRAT-02**: DOM Patch 在序列化后处理阶段通过包裹 `serialize_tree()` 输出注入策略注释，只在已失败元素上标注策略层级
- [ ] **STRAT-03**: 策略自动降级——`_failure_tracker` 记录同一元素策略 1 失败 2 次后标注降级为策略 2，策略 2 失败 2 次后降级为策略 3

### 失败恢复 (OPTIMIZE-04)

- [x] **RECOV-01**: StallDetector 新增三种失败模式检测——点击无 DOM 变化（`dom_hash_before == dom_hash_after`）、误点错误列（evaluation 关键词匹配）、编辑态未激活（input 操作失败）
- [ ] **RECOV-02**: step_callback 在 detector calls 区域添加新检测逻辑调用，将三种失败模式结果写入 `_failure_tracker` 对应 mode 字段
- [ ] **RECOV-03**: Section 9 追加 ERP 表格专用失败恢复规则——三种失败模式各自的检测→标注→切换操作流程

### Prompt 层集成

- [ ] **PROMPT-01**: Section 9 追加行标识使用规则——Agent 看到行标识注释后如何锁定目标行并在行内操作
- [ ] **PROMPT-02**: Section 9 追加反重复规则——Agent 看到失败标注后应切换策略，不在同一元素重复尝试
- [ ] **PROMPT-03**: Section 9 追加策略优先级规则——Agent 遇到策略标注时优先使用策略 1，失败后按标注降级

## v2 Requirements

Deferred to future release.

### 断言严格度分级

- **ASSERT-01**: 断言结果按严格度分级（严格/宽松/仅记录），减少因非关键字段断言失败导致的误判

### PreSubmitGuard DOM 值提取

- **GUARD-01**: PreSubmitGuard 读取 DOM 中的实际填写值，对比期望值后决定是否拦截提交

## Out of Scope

| Feature | Reason |
|---------|--------|
| 恢复 headed 模式 | 独立配置变更，不属于代码优化里程碑 |
| browser-use 版本升级 | 0.12.2 API 稳定，升级到 0.13+ 风险高，需单独评估 |
| 新增独立模块 | 设计决策：所有优化融入现有 dom_patch.py 和 prompts.py |
| 多表格类型通用化 | 当前只针对 ERP 销售出库表格，验证通过后再推广 |
| React 状态监听 | evaluate JS 绕过 React 状态管理是已知限制，v0.8.4 不解决 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| ROW-01 | Phase 67 | Complete |
| ROW-02 | Phase 68 | Pending |
| ROW-03 | Phase 68 | Pending |
| ANTI-01 | Phase 67 | Complete |
| ANTI-02 | Phase 68 | Pending |
| ANTI-03 | Phase 69 | Pending |
| STRAT-01 | Phase 68 | Pending |
| STRAT-02 | Phase 68 | Pending |
| STRAT-03 | Phase 68 | Pending |
| RECOV-01 | Phase 67 | Complete |
| RECOV-02 | Phase 69 | Pending |
| RECOV-03 | Phase 69 | Pending |
| PROMPT-01 | Phase 69 | Pending |
| PROMPT-02 | Phase 69 | Pending |
| PROMPT-03 | Phase 69 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-04-06*
*Last updated: 2026-04-06 — traceability updated after roadmap creation*
