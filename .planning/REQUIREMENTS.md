# Requirements: aiDriveUITest v0.11.4

**Defined:** 2026-05-04
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.11.4 Requirements

修复 v0.11.3 审查发现的 5 个系统性跨层模式 (CP-1~CP-5) 及 Top 5 High 优先问题。

### Memory (MEM) — 内存泄漏修复

- [x] **MEM-01**: EventManager._events dict 在 run 完成后自动清理，防止无界增长 (CP-1, High)
  - 来源: 125-FINDINGS P2-event_manager:27, 128-FINDINGS QS-07
  - 当前 cleanup() 方法存在但从未被调用
- [x] **MEM-02**: EventManager heartbeat task 在 re-subscribe 时正确取消旧 task，防止 task 泄漏 (CP-1, Medium)
  - 来源: 125-FINDINGS P2-event_manager:84-85
- [ ] **MEM-03**: useRunStream steps/timeline 数组使用 ref-based 可变数组，消除 O(n^2) 拷贝开销 (CP-1, High)
  - 来源: 127-FINDINGS SSE-4, DD-USE-04, 128-FINDINGS QS-07
- [x] **MEM-04**: StallDetector._history 添加 1000 条目上限作为防御性保护 (CP-1, Low)
  - 来源: 128-FINDINGS QS-07

### Error Handling (ERR) — 错误处理补全

- [ ] **ERR-01**: SSE event_generator 添加 try/except 防止 publish 失败中断 pipeline (CP-2, High)
  - 来源: 128-FINDINGS QS-06, 125-FINDINGS P2-event_manager:27
- [ ] **ERR-02**: useRunStream 所有 JSON.parse 调用添加 try/catch 保护 (CP-2, High)
  - 来源: 127-FINDINGS DD-USE-01 (7 处 unprotected JSON.parse)
- [ ] **ERR-03**: assertion_service.check_element_exists 实现真实 DOM 元素检测逻辑，替换 stub (High)
  - 来源: 125-FINDINGS P2-assertion_service:88-110, 128-FINDINGS QS-09
  - 当前硬编码返回 True，名称暗示 DOM 检查但实际是完成检查
- [ ] **ERR-04**: useRunStream isConnected 状态在 EventSource onopen 后才设为 true (CP-2, Medium)
  - 来源: 127-FINDINGS DD-USE-02
  - 当前在 EventSource 构造后立即设为 true

### Async Safety (ASYNC) — 阻塞操作迁移

- [ ] **ASYNC-01**: agent_service.save_screenshot 中 write_bytes 迁移为 run_in_executor 避免阻塞事件循环 (CP-4, Medium)
  - 来源: 125-FINDINGS P1-agent_service:127, 128-FINDINGS QS-08
- [ ] **ASYNC-02**: runs_routes._execute_code_background 中 subprocess.run 迁移为 asyncio.create_subprocess_exec (CP-4, Medium)
  - 来源: 126-FINDINGS DD-runs-11, 128-FINDINGS QS-08
  - 当前最大阻塞 180 秒

### State (STATE) — 可变状态解耦

- [ ] **STATE-01**: external_execution_engine 中 context mutation 改用独立 dict 存储 external_assertion_summary，防止泄漏到 variable_map (CP-5, Medium)
  - 来源: 125-FINDINGS P3-external_execution_engine:325
  - 当前 filter 无法捕获 "external_assertion_summary" key
- [ ] **STATE-02**: 前端组件中 useState 直接修改对象属性的 pattern 改为 immutable 更新模式 (CP-5, Low)
  - 来源: 127-FINDINGS 多处 useState mutation

### Correctness (CORR) — 正确性 bug 修复

- [x] **CORR-01**: 修复 dual stall detection bug — 同一 StallDetector 在 MonitoredAgent 和 agent_service 中各调用一次，阈值被意外减半 (High)
  - 来源: 125-FINDINGS Cross-2, 128-FINDINGS MAINT-01
  - 修复方案: 统一到单一调用点
- [x] **CORR-02**: execute_run_code 添加路径验证，防止路径遍历攻击 (High, SEC)
  - 来源: 126-FINDINGS 安全发现
- [x] **CORR-03**: dual progress tracking bug — 同一 TaskProgressTracker 在两处被调用 (Medium)
  - 来源: 125-FINDINGS P1-agent_service:374-380

### Dead Code (DEAD) — 未使用代码清理

- [ ] **DEAD-01**: 删除 response.py 85 行完全未使用的代码 (CP-3, Medium)
  - 来源: 126-FINDINGS P3-resp-01, 128-FINDINGS QS-09
- [ ] **DEAD-02**: 4 个前端 hooks 迁移到 React Query useQuery，消除 ~200 行重复 boilerplate (CP-3, High)
  - 来源: 128-FINDINGS QS-03, 127-FINDINGS App.tsx-React-Query
  - useTasks, useReports, useDashboard, useBatchProgress
- [ ] **DEAD-03**: PreSubmitGuard 标记为已知限制或删除死代码路径 (CP-3, Medium)
  - 来源: 125-FINDINGS P3-pre_submit_guard:109-114, 128-FINDINGS QS-09
  - actual_values/submit_button_text 始终为 None，核心逻辑不可达
- [ ] **DEAD-04**: 统一后端错误处理策略 — 可选操作统一使用 non_blocking_execute (Medium)
  - 来源: 128-FINDINGS QS-06
  - 当前 3+ 种错误处理模式混合使用

## Out of Scope

| Feature | Reason |
|---------|--------|
| 67 个测试场景重建 | 独立里程碑，测试依赖代码修复完成 |
| F-grade generate() 函数拆分 | 复杂度高但功能正确，风险大于收益 |
| 前端高复杂度组件重构 (JsonTreeViewer, TaskForm) | UI 功能正确，重构风险高 |
| 配置双源统一 (.env vs YAML) | 影响 LLM 层，范围超出当前优化 |
| mypy 类型错误修复 (136 errors) | 不影响运行时行为，优先级低于 bug 修复 |
| run_pipeline.py god-module 拆分 | 架构重构风险高，独立评估 |
| 后端命名一致性统一 (QS-04) | 纯代码风格，不影响正确性 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| MEM-01 | Phase 131 | Complete |
| MEM-02 | Phase 131 | Complete |
| MEM-03 | Phase 133 | Pending |
| MEM-04 | Phase 131 | Complete |
| ERR-01 | Phase 131 | Pending |
| ERR-02 | Phase 133 | Pending |
| ERR-03 | Phase 131 | Pending |
| ERR-04 | Phase 133 | Pending |
| ASYNC-01 | Phase 132 | Pending |
| ASYNC-02 | Phase 132 | Pending |
| STATE-01 | Phase 132 | Pending |
| STATE-02 | Phase 133 | Pending |
| CORR-01 | Phase 130 | Complete |
| CORR-02 | Phase 130 | Complete |
| CORR-03 | Phase 130 | Complete |
| DEAD-01 | Phase 134 | Pending |
| DEAD-02 | Phase 134 | Pending |
| DEAD-03 | Phase 134 | Pending |
| DEAD-04 | Phase 134 | Pending |

**Coverage:**
- v0.11.4 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-05-04*
*Last updated: 2026-05-04 — traceability updated after roadmap creation*
