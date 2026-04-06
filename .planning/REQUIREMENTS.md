# Requirements: aiDriveUITest v0.8.3

**Defined:** 2026-04-06
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.8.3 Requirements

### 差距关联分析 (ANALYSIS)

- [ ] **ANALYSIS-01**: 分析 v0.8.2 报告中 headless/headed 差异与 Agent 表格定位不准的因果关联 — headless 下 DOM 序列化是否导致 index 偏移、元素不可见等
- [ ] **ANALYSIS-02**: 评估 headed 模式恢复后 DOM Patch (5 patches) 的有效性 — 补丁在 headed 下是否有冗余或冲突
- [ ] **ANALYSIS-03**: 评估 headed 模式恢复后 Section 9 Prompt (click-to-edit 指导) 的有效性 — prompt 指导是否仍需保留

### 优化方案设计 (OPTIMIZE)

- [x] **OPTIMIZE-01**: 设计"按行定位 + 直接找 input"的表格输入策略 — 先锁定目标行（如含 I01784004409597），再在行内找销售金额 input
- [x] **OPTIMIZE-02**: 设计反重复机制 — 同一 index 连续失败 2 次自动切换策略，误点错误列 1 次立即重新识别
- [x] **OPTIMIZE-03**: 设计策略优先级 — 原生 input 操作 → DOM 查询定位 → evaluate JS 兜底
- [x] **OPTIMIZE-04**: 设计失败恢复策略 — 点击无 DOM 变化、误点错误列、编辑态判断失误时的快速切换规则

## Future Requirements

### 断言严格度 (deferred)

- **ASSERT-01**: 评估 saleTime 比较规则是否为严格相等
- **ASSERT-02**: 评估 salesOrder='SA' 是否只是前缀匹配
- **ASSERT-03**: 设计断言严格度分级（宽松/标准/严格）

## Out of Scope

| Feature | Reason |
|---------|--------|
| 实际代码修改 | 本 milestone 只做分析和方案设计，不写代码 |
| 断言系统修改 | 推迟到有实际需求时处理 |
| headed 模式恢复实施 | 恢复 headed 属于独立修复，不在本分析范围内 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ANALYSIS-01 | Phase 65 | Pending |
| ANALYSIS-02 | Phase 65 | Pending |
| ANALYSIS-03 | Phase 65 | Pending |
| OPTIMIZE-01 | Phase 66 | Complete |
| OPTIMIZE-02 | Phase 66 | Complete |
| OPTIMIZE-03 | Phase 66 | Complete |
| OPTIMIZE-04 | Phase 66 | Complete |

**Coverage:**
- v0.8.3 requirements: 7 total
- Mapped to phases: 7/7 (100%)

---
*Requirements defined: 2026-04-06*
*Last updated: 2026-04-06 after roadmap creation*
