# Requirements: v0.6.1 表格输入框定位优化

**Milestone:** v0.6.1
**Goal:** 解决 Agent 无法正确定位表格单元格内输入框的问题，减少类似步骤的无效循环
**Created:** 2026-03-25

---

## Problem Context

**问题表现:** Agent 从 Step 15 到 Step 24 反复点击同一索引，无法输入销售金额

**根本原因:**
- 输入框被标记为 `is_interactive=False` + `ignored_by_paint_order=True`
- 点击索引指向 td 而非内部 input 元素
- 10+ 步徒劳循环，stagnation 从 6 增加到 10+

**DOM 分析详情:**
```
销售价输入框属性:
- should_display=True ✓
- is_interactive=False ✗ (问题所在)
- ignored_by_paint_order=True ✗
- is_shadow_host=True
- 父元素 (td, div.cell, div.el-input-number) 全部 ignored_by_paint_order=True
```

**临时解决:** 通过 JavaScript `evaluate` 直接设置值

---

## In Scope (This Milestone)

### DOM - DOM 解析增强

- [x] **DOM-01**: DOM 解析器增强 - 表格内 input 元素不应仅依赖 paint_order 判断可交互性
  - **User Story**: 作为 Agent，当我遇到表格内的输入框时，应该能正确识别其为可交互元素
  - **Acceptance Criteria**:
    - 表格内的 input/textarea/select 元素应始终标记为 `is_interactive=True`
    - 不受父元素 `paint_order` 属性影响
  - **Complexity**: High（需要理解 browser-use DOM 解析机制）
  - **Implementation**: 通过项目层面扩展，不修改 browser-use 核心

- [x] **DOM-02**: 索引精确定位 - 点击 td 时自动定位到内部的 input 元素
  - **User Story**: 作为 Agent，当我点击表格单元格时，应该自动定位到内部的输入框
  - **Acceptance Criteria**:
    - 点击 td 元素时，自动查找内部 input/textarea/select
    - 如果找到输入元素，将焦点设置到该元素
  - **Complexity**: Medium
  - **Implementation**: AgentService 回调或自定义工具

### FALLBACK - 降级策略

- [x] **FALLBACK-01**: 自动降级策略 - 当普通点击失败时，自动切换到 JavaScript 方案
  - **User Story**: 作为 Agent，当我的点击操作没有产生预期效果时，应该自动尝试 JavaScript 方案
  - **Acceptance Criteria**:
    - 检测点击后输入框是否获得焦点
    - 如果焦点获取失败，自动使用 `page.evaluate()` 设置值
    - 降级行为应记录在执行日志中
  - **Complexity**: Medium
  - **Implementation**: 检测逻辑 + 自动降级

### LOG - 日志改进

- [ ] **LOG-03**: 执行日志改进 - 记录元素定位失败的具体原因
  - **User Story**: 作为开发者，当 Agent 定位元素失败时，我应该能看到详细的失败原因
  - **Acceptance Criteria**:
    - 记录 `is_interactive=False` 的元素信息
    - 记录 `ignored_by_paint_order=True` 的父元素链
    - 记录降级策略的触发和执行
  - **Complexity**: Low
  - **Implementation**: 增强 AgentService 日志输出

---

## Future Requirements (Deferred)

| Requirement | Reason | Future Milestone |
|-------------|--------|------------------|
| Shadow DOM 深度解析 | 复杂度高，当前问题非 Shadow DOM 导致 | v0.7+ |
| 自定义 DOM 过滤器配置 | 过度设计，当前需求明确 | v0.7+ |
| 可配置的交互元素白名单 | 灵活性需求不明确 | v0.7+ |

---

## Out of Scope

| Item | Reason |
|------|--------|
| 修改 browser-use 核心库 | 约束：通过项目层面扩展实现 |
| Shadow DOM 深度遍历 | 过度复杂，非当前问题根因 |
| 自定义 CSS 选择器引擎 | 不必要，Playwright 已有强大的选择器 |

---

## Constraints

1. **不修改 browser-use 核心库** - 通过项目层面扩展实现
2. **保持与现有 DOM 解析逻辑的兼容性** - 不能破坏现有功能
3. **最小侵入性** - 优先使用工具和回调机制

---

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| browser-use DOM 解析机制 | Technical | Need to understand |
| Phase 40 scroll_table_and_input 工具 | Code | ✅ Implemented |
| AgentService 回调机制 | Code | ✅ Available |
| JavaScript evaluate 能力 | Code | ✅ Available |

---

## Success Criteria

1. Agent 能够在 **3 步以内** 成功定位并输入表格单元格内的输入框
2. 无需手动介入即可完成表格输入操作
3. 执行日志清晰记录元素定位过程和失败原因
4. Stagnation **不再因输入框定位问题超过 5**

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| DOM-01 | Phase 42 | Complete |
| DOM-02 | Phase 43 | Complete |
| FALLBACK-01 | Phase 43 | Complete |
| LOG-03 | Phase 44 | Pending |

---

*Requirements for milestone v0.6.1*
*Created: 2026-03-25*
*Roadmap updated: 2026-03-25*
