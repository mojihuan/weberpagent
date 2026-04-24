# Requirements: aiDriveUITest v0.10.4

**Defined:** 2026-04-23
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.10.4 Requirements

### 代码执行验证 (CODE)

- [x] **CODE-01**: GET /runs/{run_id}/code 返回已生成的 Playwright 代码文件内容（从 Run.generated_code_path 读取）
- [x] **CODE-02**: POST /runs/{run_id}/execute-code 触发 pytest 执行，复用 SelfHealingRunner 基础设施（storage_state 注入 + 超时保护）
- [x] **CODE-03**: 代码执行结果（成功/失败/错误信息/耗时）可通过 GET /runs/{run_id} 获取，包含 healing_status 和 healing_error 字段

### 任务管理 UI (UI)

- [ ] **UI-01**: 任务列表 TaskTable 新增"代码"列，通过 latest run 的 generated_code_path 判断是否显示代码可用标识
- [ ] **UI-02**: "查看代码"按钮 — 打开 CodeViewerModal 只读显示 Python 代码，使用 react-syntax-highlighter 语法高亮，显示行号
- [ ] **UI-03**: "运行代码"按钮 — 在 CodeViewerModal 内触发 Playwright 执行，异步反馈执行状态（等待/运行中/成功/失败），显示错误信息

### 任务状态 (STATUS)

- [x] **STATUS-01**: Task.status 扩展为 draft/ready/success 三种状态，success 由系统在 Playwright 代码执行成功后自动设置，前端 StatusBadge 显示"成功"标签（绿色）

## Future Requirements

### 代码管理

- **CODE-EDIT-01**: 在线编辑生成的 Playwright 代码（当前只读查看）
- **CODE-DIFF-01**: 查看 Agent 生成代码与 LLM 修复代码的 diff
- **CODE-CLEANUP-01**: 过期生成代码文件自动清理策略

### 高级执行

- **EXEC-CONCURRENT-01**: 多任务并发代码执行（Semaphore 控制）
- **EXEC-SCHEDULE-01**: 定时执行 Playwright 代码
- **EXEC-REPORT-01**: 代码执行结果生成独立报告

## Out of Scope

| Feature | Reason |
|---------|--------|
| 在线代码编辑器 (Monaco/CodeMirror) | 当前只需只读查看，4MB+ bundle 不值得 |
| 代码版本管理 | 过度设计，当前生成即最终版本 |
| 多用户并发执行保护 | 单用户本地使用，Semaphore(1) 足够 |
| 代码执行定时任务 | 非核心需求，推迟到有实际需求 |
| 批量代码执行 | 复杂度高，当前场景为单任务验证 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CODE-01 | Phase 97 | Complete |
| CODE-02 | Phase 97 | Complete |
| CODE-03 | Phase 97 | Complete |
| STATUS-01 | Phase 97 | Complete |
| UI-01 | Phase 98 | Pending |
| UI-02 | Phase 98 | Pending |
| UI-03 | Phase 98 | Pending |

**Coverage:**
- v0.10.4 requirements: 7 total
- Mapped to phases: 7
- Unmapped: 0

---
*Requirements defined: 2026-04-23*
*Last updated: 2026-04-23 after roadmap creation*
