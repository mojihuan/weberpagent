# Phase 125: 后端核心逻辑审查 - Context

**Gathered:** 2026-05-03
**Status:** Ready for planning

<domain>
## Phase Boundary

审查后端核心业务逻辑（agent 层 / core services / pipeline 编排）的正确性和架构合理性，输出具体发现清单。

**审查范围（31 文件，~11.7K 行）：**
- agent 层 (7 文件): monitored_agent.py, stall_detector.py, pre_submit_guard.py, task_progress_tracker.py, action_utils.py, dom_patch.py, prompts.py
- core services (23 文件): agent_service.py, code_generator.py, action_translator.py, step_code_buffer.py, locator_chain_builder.py, precondition_service.py, assertion_service.py, report_service.py, test_flow_service.py, batch_execution.py, event_manager.py, account_service.py, auth_service.py, cache_service.py, error_utils.py, random_generators.py, time_utils.py, external_module_loader.py, external_method_discovery.py, external_execution_engine.py, external_precondition_bridge.py, 及其他
- pipeline 编排 (1 文件): run_pipeline.py

**不在范围内：** API 路由层（Phase 126）、前端（Phase 127）、代码质量/横切关注点（Phase 128）、测试规划（Phase 129）、任何代码修改。

</domain>

<decisions>
## Implementation Decisions

### 审查策略
- **D-01:** 采用「广度优先 + 聚焦深潜」策略 — 先对 31 个文件做快速扫描标记风险等级，然后对高优先级文件做深度逐行审查
- **D-02:** 审查重点向管道核心文件倾斜 — agent_service.py（执行核心）、run_pipeline.py（5 阶段编排）、code_generator.py（测试文件组装）优先深潜；工具类文件和简单服务只做快速扫描
- **D-03:** dom_patch.py (777行) 和 action_translator.py (718行) 虽然最复杂，但它们是 browser-use/ERP 特定的适配层，审查重点放在管道核心的逻辑正确性上

### 输出格式
- **D-04:** 审查发现输出到独立文件 `125-FINDINGS.md`，不修改现有 CONCERNS.md
- **D-05:** 发现按 4 级严重程度分级：Critical（数据丢失/安全漏洞）、High（逻辑错误/潜在 bug）、Medium（边界条件/异常路径）、Low（代码气味/小改进）
- **D-06:** 每条发现附带类别标签：正确性（Correctness）、架构（Architecture）、性能（Performance）、安全（Security）

### 审查方法
- **D-07:** 以人工阅读代码为主，ruff 和 mypy 作为辅助工具
- **D-08:** ruff 检查 style/lint 问题，mypy 检查类型不一致，但审查核心关注逻辑正确性、边界条件、异常路径、架构耦合

### Claude's Discretion
- 广度扫描时每个文件的具体风险评分标准
- 发现条目的具体格式模板（只要包含严重程度、类别、描述、位置、建议即可）
- 快速扫描与深潜的具体分界线（建议以扫描发现的问题数量和严重度为依据）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目规划
- `.planning/PROJECT.md` — 项目愿景、技术栈、关键决策历史
- `.planning/REQUIREMENTS.md` — v0.11.3 需求定义（CORR-01, ARCH-01, ARCH-02 对应本阶段）
- `.planning/ROADMAP.md` — Phase 125 定义和成功标准
- `.planning/STATE.md` — 当前项目状态

### 代码库分析
- `.planning/codebase/ARCHITECTURE.md` — 完整架构分析（层、数据流、关键抽象、横切关注点）
- `.planning/codebase/STRUCTURE.md` — 目录结构和文件用途
- `.planning/codebase/CONCERNS.md` — 已知问题（Tech Debt, Known Bugs, Security, Performance, Fragile Areas）— 审查时应验证这些已知问题并发现新问题
- `.planning/codebase/CONVENTIONS.md` — 代码规范约定
- `.planning/codebase/INTEGRATIONS.md` — 外部集成细节
- `.planning/codebase/STACK.md` — 技术栈依赖
- `.planning/codebase/TESTING.md` — 测试策略和覆盖缺口

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **CONCERNS.md 已记录大量已知问题** — 包括 exec() 安全、DOM monkey-patch、Event memory leak、UUID 碰撞、batch fire-and-forget 等。审查时应验证这些问题的准确性并补充新发现。
- **Architecture 数据流图** — ARCHITECTURE.md 已有完整的 Test Execution Flow 和 Code Generation Pipeline 数据流图，可作为审查的导航线索。

### Established Patterns
- **Repository Pattern** — `BaseRepository` + 专用子类，async session
- **Service Pattern** — Service 编排 Repository，Route 不直接访问 DB
- **Event Manager (Pub/Sub)** — 全局单例，SSE 推送
- **LLM Factory** — 工厂模式 + 缓存 + tenacity 重试
- **Code Generation Pipeline** — 4 级翻译管道（DOM → Locator → Action → Test file）
- **External Integration (Facade)** — 懒加载 + docstring 发现 + facade 模式

### Integration Points
- agent_service.py 是 agent 层和 core 层的核心集成点
- run_pipeline.py 编排所有服务的调用顺序
- external_precondition_bridge.py 是外部项目的 facade
- event_manager.py 是后端与前端的 SSE 桥梁

</code_context>

<specifics>
## Specific Ideas

- 审查是 review-only：只输出发现和建议，不做代码修改
- 测试套件已删除（v0.11.0），项目当前无自测能力
- v0.11.0 已完成代码清理（死代码删除、重复合并、类型标注、函数优化），代码质量基线已提升
- dom_patch.py 是最脆弱的文件（777 行，猴子补丁 4 个 browser-use 内部类），但审查重点放在管道核心
- PREVIOUS PHASES (120-124) 已处理了命名规范、类型标注、函数优化等表层问题，本阶段关注更深层逻辑问题

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 125-backend-core-review*
*Context gathered: 2026-05-03*
