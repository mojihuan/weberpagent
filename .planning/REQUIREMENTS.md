# Requirements: v0.6.0 Agent 行为优化

**Milestone:** v0.6.0
**Goal:** 优化 Agent 在复杂场景下的执行效率，减少无效循环，提高任务成功率
**Created:** 2026-03-24

## Research Summary

### browser-use 内置机制

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `loop_detection_window` | 20 | 滚动窗口大小 |
| `loop_detection_enabled` | True | 是否启用循环检测 |
| `max_failures` | 5 | 最大连续失败次数 |
| `step_timeout` | 180s | 每步超时 |
| `planning_replan_on_stall` | 3 | 停滞后重新规划 |

**阈值说明:**
- 5 次重复：轻微提醒
- 8 次重复：中度提醒
- 12 次重复：强烈提醒
- 5 次页面停滞：提醒

**核心问题:** 循环检测只提醒不干预，导致 stagnation=27 仍在循环

---

## Requirements

### LOOP - 循环干预优化

- [x] **LOOP-01**: 更早的循环干预
  - 降低 stagnation 阈值，在 5 次连续失败时就尝试跳过困难步骤
  - 实现方式: 自定义 hook 监控 stagnation，触发跳过逻辑
  - 验收标准: stagnation 达到 5 时自动尝试跳过当前步骤

- [ ] **LOOP-02**: 增强表格元素定位
  - 支持水平滚动表格内的输入字段定位
  - 实现方式: 创建自定义工具 `scroll_table_and_input`
  - 验收标准: 销售出库场景中能成功输入销售金额

- [ ] **LOOP-03**: 配置化循环检测参数
  - 允许用户自定义循环检测阈值
  - 实现方式: 扩展 AgentSettings 配置项，传递给 browser-use
  - 验收标准: 用户可在 TaskConfig 中配置 max_stagnation 等参数

- [x] **LOOP-04**: 智能跳过与继续
  - 当检测到无法完成的步骤时，跳过并继续后续步骤
  - 实现方式: 自定义 hook 检测长期停滞，注入 skip 指令
  - 验收标准: 困难步骤被跳过后，后续步骤能继续执行

### LOG - 日志与监控

- [x] **LOG-01**: 增强循环日志输出
  - 在循环检测触发时输出更详细的状态信息
  - 包含: 当前 stagnation 值、最近动作、页面变化
  - 验收标准: 日志中包含完整的循环诊断信息

- [ ] **LOG-02**: 步骤执行统计
  - 记录每步执行时间、动作次数、页面变化
  - 用于后续分析和优化
  - 验收标准: 报告中包含每步详细统计

---

## Future Requirements (Deferred)

- **UI-01**: 前端展示循环检测状态 - 需要更多后端支持
- **ML-01**: 基于历史数据的智能阈值调整 - 需要数据积累
- **CUSTOM-01**: 完全自定义循环检测算法 - 复杂度较高

---

## Out of Scope

| Item | Reason |
|------|--------|
| 修改 browser-use 核心库 | 维护成本高，升级困难 |
| 多 Agent 并行执行 | 当前场景不需要 |
| AI 模型微调 | 超出项目范围 |
| 用户认证系统 | 单用户使用 |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| LOOP-01 | Phase 39 | Complete |
| LOG-01 | Phase 39 | Complete |
| LOOP-02 | Phase 40 | Pending |
| LOOP-04 | Phase 40 | Complete |
| LOOP-03 | Phase 41 | Pending |
| LOG-02 | Phase 41 | Pending |

---
*Requirements defined: 2026-03-24*
