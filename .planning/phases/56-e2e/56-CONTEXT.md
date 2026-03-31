# Phase 56: E2E 综合验证 - Context

**Gathered:** 2026-03-31
**Status:** Ready for planning

<domain>
## Phase Boundary

用全部 11 个 ERP 测试用例（9 个操作类 + 2 个断言类）端到端验证 Phase 52-54 的所有新操作能力（键盘、表格、文件上传）+ 断言功能协同工作。

**包含：**
- 键盘操作测试（KB-01/02/03）— 3 个用例
- 表格交互测试（TBL-01~04）— 4 个用例
- 文件导入测试（IMP-01/02）— 2 个用例
- 断言验证测试（AST-01/02）— 2 个用例
- 综合验证报告生成

**不包含：**
- 缓存断言功能（CAC-01/02 推迟）
- 修改 prompt 或代码（纯验证 Phase）
- 修复发现的 bug（仅记录分析）

</domain>

<decisions>
## Implementation Decisions

### 测试用例范围
- **D-01:** 全部 11 个测试用例。包含 Phase 52-54 的 9 个操作类用例 + 2 个断言用例（AST-01/02）。即使 Phase 55 跳过，也在 E2E 中验证断言功能

### 执行方式
- **D-02:** 通过平台 UI 手动执行。逐个创建/执行测试用例，人工观察 Agent 行为过程。与 Phase 51 验证模式一致（Phase 51 D-03）
- **D-03:** 本地开发机执行。方便查看日志和调试

### 通过标准与报告
- **D-04:** 逐场景判定。每个用例独立判定通过/失败，可以部分通过。与 Phase 52-54 验证模式一致
- **D-05:** 新建综合验证报告。在 `docs/test-steps/` 下创建 `采购-综合验证结果.md`，汇总全部 11 个场景结果
- **D-06:** 记录失败原因并分析，不做自动修复。保持验证 Phase 的纯洁性

### 断言验证
- **D-07:** 包含 AST-01/02 断言验证。验证 headers 参数传递和 i/j 参数组合的正确性
- **D-08:** 在 `docs/test-steps/` 下新建 `采购-断言验证测试步骤.md`，定义 AST-01/02 的具体测试步骤和验证条件

### Plan 结构
- **D-09:** 两个 Plan。Plan 56-01: 创建断言测试步骤文档 + 准备测试环境，Plan 56-02: 执行全部 11 个 E2E 测试用例并生成综合验证报告

### Claude's Discretion
- AST-01/02 测试步骤文档的具体内容
- 综合验证报告的具体格式
- 各用例执行的具体 ERP 操作流程
- 失败原因分析的具体深度

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — KB-01/02/03、TBL-01~04、IMP-01/02、AST-01/02 需求定义
- `.planning/ROADMAP.md` — Phase 56 成功标准和计划结构

### 测试步骤文档（执行目标）
- `docs/test-steps/采购-键盘操作测试步骤.md` — 3 个键盘操作测试用例
- `docs/test-steps/采购-表格交互测试步骤.md` — 4 个表格交互测试用例
- `docs/test-steps/采购-文件导入测试步骤.md` — 2 个文件导入测试用例
- `docs/test-steps/采购-断言验证测试步骤.md` — 2 个断言验证测试用例（Plan 56-01 创建）

### 已有验证结果（参考基线）
- `docs/test-steps/采购-键盘操作验证结果.md` — Phase 52 验证结果（1/3 通过，2 未独立验证）
- `docs/test-steps/采购-键盘操作验证结果-补充.md` — Phase 52 补充验证
- `docs/test-steps/采购-表格交互验证结果.md` — Phase 53 验证结果（4/4 通过）
- `docs/test-steps/采购-文件导入验证结果.md` — Phase 54 验证结果（2/2 通过）

### 代码参考（验证目标）
- `backend/agent/prompts.py` — ENHANCED_SYSTEM_MESSAGE（8 段，包含 Phase 52-54 新增的段落 6-8）
- `backend/core/agent_service.py` — AgentService + MonitoredAgent + available_file_paths
- `backend/agent/monitored_agent.py` — MonitoredAgent 子类
- `backend/core/external_precondition_bridge.py` — 断言执行引擎

### 先前阶段上下文
- `.planning/phases/52-prompt/52-CONTEXT.md` — Phase 52 键盘操作 Prompt 决策
- `.planning/phases/53-prompt/53-CONTEXT.md` — Phase 53 表格交互 Prompt 决策
- `.planning/phases/54-import/54-CONTEXT.md` — Phase 54 文件导入决策
- `.planning/phases/55-assertion-cache/55-CONTEXT.md` — Phase 55 跳过决策
- `.planning/phases/51-e2e-verification/51-CONTEXT.md` — Phase 51 E2E 验证模式参考

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/agent/prompts.py` ENHANCED_SYSTEM_MESSAGE：8 段完整 prompt，覆盖键盘/表格/文件上传操作指导
- `backend/core/agent_service.py`：MonitoredAgent + available_file_paths 注入，完整的 Agent 创建链路
- `backend/core/external_precondition_bridge.py`：断言执行引擎，已实现 headers/i/j 参数传递
- `data/test-files/`：测试文件目录，已有 .xlsx 和 .jpg 文件
- `backend/tests/unit/test_enhanced_prompt.py`：prompt 关键词测试（可运行确认 prompt 结构完整）

### Established Patterns
- E2E 验证通过平台 UI 手动执行（Phase 51 D-03）
- 逐场景判定通过/失败（Phase 52-54 验证模式）
- 验证结果文档记录格式：场景名 + 状态 + 说明 + 日志证据
- 测试用例通过平台 UI 创建，输入测试步骤描述
- per-run 日志存储在 `outputs/` 目录，用于检查 Agent 行为

### Integration Points
- 平台前端 → API → AgentService.run_with_streaming() → MonitoredAgent → browser-use
- `outputs/` 目录存储运行日志和截图
- 断言接口通过 external_precondition_bridge 调用 ERP API

### 关键注意事项
- Phase 52 的 Escape 和 Control+a 未独立验证，需要专门设计测试场景
- 断言测试需要确认 headers 参数和 i/j 参数是否正确传递
- 本地开发机需确认后端服务运行在 localhost:8080
- data/test-files/ 目录需确认存在且包含测试文件

</code_context>

<specifics>
## Specific Ideas

- 11 个测试用例执行顺序：先跑已独立验证的 7 个（确认回归），再跑未独立验证的 2 个键盘场景，最后跑断言场景
- 综合验证报告结构：按操作类型分组（键盘/表格/导入/断言），每组汇总通过率
- 断言测试场景可使用采购单列表 API 验证 headers 传递和 i/j 参数组合
- 失败分析模板：失败场景 + 日志证据 + 原因分类（prompt/环境/数据）

</specifics>

<deferred>
## Deferred Ideas

- CAC-01/02 缓存断言功能 — 推迟到有实际需求时实现（Phase 55 决策）
- 自动化回归测试框架 — 当前手动执行满足需求，未来可考虑自动化

</deferred>

---

*Phase: 56-e2e*
*Context gathered: 2026-03-31*
