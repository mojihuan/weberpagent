# Requirements: aiDriveUITest v0.9.0

**Defined:** 2026-04-08
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告
**Milestone:** v0.9.0 Excel 批量导入功能开发

## v1 Requirements

### TMPL: 模版设计

- [x] **TMPL-01**: 用户可以下载预格式化的 Excel 模版 (.xlsx)，包含列头（任务名称、任务描述、目标URL、最大步数、前置条件、断言）+ 2 行示例数据 + README sheet 说明 — Phase 70
- [x] **TMPL-02**: Excel 模版中对 max_steps 字段配置下拉验证（1-100），防止输入错误 — Phase 70

### IMPT: 批量导入

- [x] **IMPT-01**: 用户可以上传 .xlsx 文件，系统逐行解析为 TaskCreate 格式并验证所有字段（必填检查、类型校验、前置条件可解析性、断言 JSON 格式）
- [x] **IMPT-02**: 用户可以在确认前预览解析结果，有效行显示绿色、无效行显示红色 + 具体错误信息（行号 + 字段 + 原因）
- [x] **IMPT-03**: 用户确认导入后，系统批量创建 Task（全部有效才提交，任一失败则全部回滚），导入的任务状态为 draft

### BATCH: 批量执行

- [x] **BATCH-01**: 用户可以在 TaskTable 勾选多个 Task，点击「批量执行」按钮启动并行执行
- [x] **BATCH-02**: 批量执行使用 asyncio.Semaphore 控制并发数，默认 2，用户可配置（上限 4），防止单服务器 OOM
- [ ] **BATCH-03**: 用户可以在批量进度页面查看每个任务的状态（等待/执行中/完成/失败），点击可跳转到该任务的执行监控详情

## v2 Requirements (Deferred)

### IMPT Enhancement

- **IMPT-04**: 导入失败时，用户可以下载错误标注的 Excel 文件，便于离线修复后重新上传
- **IMPT-05**: 支持简化断言格式（管道分隔 `method|headers|data|params`），替代 JSON 数组降低 QA 填写门槛

### BATCH Enhancement

- **BATCH-04**: 批量执行完成后显示汇总报告（通过/失败/错误数量），一键查看各任务报告
- **BATCH-05**: 批量执行支持取消操作，一键停止所有等待和执行中的任务
- **BATCH-06**: 批量执行失败任务一键重试

### 断言严格度分级

- **ASSERT-01**: 断言结果按严格度分级（严格/宽松/仅记录），减少因非关键字段断言失败导致的误判

### PreSubmitGuard DOM 值提取

- **GUARD-01**: PreSubmitGuard 读取 DOM 中的实际填写值，对比期望值后决定是否拦截提交

## Out of Scope

| Feature | Reason |
|---------|--------|
| CSV 导入 | CSV 编码/换行/类型问题多，XLSX 原生支持 Unicode 和数据验证 |
| 实时 SSE 批量进度 | 需 multiplexer 架构改造，轮询足够满足当前需求 |
| Task 导出为 Excel | 往返导入/导出需要 ID 保留和合并语义，v0.9.0 仅做导入 |
| Excel 公式支持 | openpyxl data_only 模式限制 + 公式跨单元格依赖脆弱 |
| 多行断言分组 | 行归属判断易被排序/筛选破坏，单行 JSON 更稳定 |
| 定时批量执行 | 需 cron 调度系统，超出当前里程碑范围 |
| 浏览器实例复用 | 跨任务 session 污染风险，每次新建更安全 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TMPL-01 | Phase 70 | Complete |
| TMPL-02 | Phase 70 | Complete |
| IMPT-01 | Phase 71 | Complete |
| IMPT-02 | Phase 71 | Complete |
| IMPT-03 | Phase 71 | Complete |
| BATCH-01 | Phase 72 | Complete |
| BATCH-02 | Phase 72 | Complete |
| BATCH-03 | Phase 73 | Pending |

**Coverage:**
- v1 requirements: 8 total
- Mapped to phases: 8
- Unmapped: 0

---
*Requirements defined: 2026-04-08*
*Last updated: 2026-04-08 — Traceability updated after roadmap creation*
