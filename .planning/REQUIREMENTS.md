# Requirements: aiDriveUITest v0.8.0

**Defined:** 2026-04-02
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.8.0 Requirements

### 执行步骤展示 (EXEC)

- [x] **EXEC-01**: 执行监控的 StepTimeline 中展示前置条件执行步骤（包含状态、耗时、代码摘要）
- [x] **EXEC-02**: 执行监控的 StepTimeline 中展示断言执行步骤（包含状态、耗时、断言名称）
- [x] **EXEC-03**: 前置条件和断言步骤与普通 UI 步骤按执行顺序交错显示在时间线中

### 报告详情 (RPT)

- [x] **RPT-01**: 报告详情页的步骤列表中展示前置条件步骤及其执行结果（成功/失败、耗时、变量输出）
- [x] **RPT-02**: 报告详情页的步骤列表中展示断言步骤及其执行结果（通过/失败、断言名称、失败信息）
- [x] **RPT-03**: 前置条件和断言步骤在报告步骤列表中按实际执行顺序与其他步骤交错展示

### AI 推理格式 (FMT)

- [ ] **FMT-01**: AI 推理过程中 Eval/Verdict/Memory/Goal 每项独占一行展示（替代当前的 `|` 分隔单行显示）
- [ ] **FMT-02**: 报告详情页 StepItem 中的推理文本按行解析并格式化展示（带标签高亮）
- [ ] **FMT-03**: 执行监控 ReasoningLog 中的推理文本同步格式化展示

### 任务表单优化 (FORM)

- [x] **FORM-01**: 任务表单中移除"接口断言"和"业务断言"的 tab 切换，仅保留业务断言配置区域
- [x] **FORM-02**: 移除表单中 api_assertions 相关的 textarea 列表（不再支持自由代码式接口断言）

## v2 Requirements

_(无推迟需求)_

## Out of Scope

| Feature | Reason |
|---------|--------|
| 接口断言功能保留 | 用户确认只使用业务断言，接口断言代码输入方式移除 |
| 推理过程编辑 | 仅展示格式优化，不需要编辑功能 |
| 前置条件/断言的步骤详情折叠 | 简化实现，直接展示关键信息 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EXEC-01 | Phase 58 | Complete |
| EXEC-02 | Phase 58 | Complete |
| EXEC-03 | Phase 58 | Complete |
| RPT-01 | Phase 59 | Complete |
| RPT-02 | Phase 59 | Complete |
| RPT-03 | Phase 59 | Complete |
| FMT-01 | Phase 57 | Pending |
| FMT-02 | Phase 57 | Pending |
| FMT-03 | Phase 57 | Pending |
| FORM-01 | Phase 60 | Complete |
| FORM-02 | Phase 60 | Complete |

**Coverage:**
- v0.8.0 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---
*Requirements defined: 2026-04-02*
*Last updated: 2026-04-02 after roadmap creation*
