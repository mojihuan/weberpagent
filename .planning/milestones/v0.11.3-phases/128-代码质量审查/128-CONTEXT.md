# Phase 128: 代码质量审查 - Context

**Gathered:** 2026-05-03
**Status:** Ready for planning

<domain>
## Phase Boundary

审查代码可维护性、横切关注点一致性和异步性能，跨前后端全栈审查，输出具体发现清单。

**审查范围：**

### 后端 (backend/)
- **可维护性**: DRY/SOLID 违反、代码重复、单一职责违反 (MAINT-01)
- **结构复杂度**: 函数长度超标、文件过大、圈复杂度过高 (MAINT-02)
- **命名规范**: 误导性命名、不一致抽象层级 (MAINT-03)
- **横切关注点**: 错误处理策略一致性、配置管理、日志策略 (ARCH-03)
- **异步性能**: 阻塞操作混入 async 代码、资源竞争、内存泄漏、SSE 连接管理 (PERF-01)

### 前端 (frontend/src/)
- **可维护性**: DRY/SOLID 违反、代码重复 (MAINT-01)
- **结构复杂度**: 组件过大、函数复杂度 (MAINT-02)
- **命名规范**: 误导性命名 (MAINT-03)
- **横切关注点**: 错误处理一致性、状态管理策略 (ARCH-03)
- **异步性能**: 不必要重渲染、资源泄漏 (PERF-01)

**不在范围内：** 正确性审查（Phase 125/127 已完成）、安全审查（Phase 126 已完成）、测试规划（Phase 129）、任何代码修改。

**与 Phase 125/126/127 的关系：**
- Phase 125 已发现 run_pipeline.py god-module、event_manager memory leak 等架构/性能问题
- Phase 126 已发现 SSE stream 无 try/except/finally、API 错误处理不一致等横切关注点问题
- Phase 127 已发现 React Query 安装但未使用、3 个超大组件 (829/560/546 行) 等可维护性问题
- 以上已有发现直接引用，不重复分析

</domain>

<decisions>
## Implementation Decisions

### 与前面阶段的重叠处理
- **D-01:** 直接引用 — 128-FINDINGS.md 只记录新发现，对 Phase 125/126/127 已发现的 MAINT/ARCH-03/PERF-01 范畴问题标注 "See {phase}-FINDINGS.md #N" 引用来源，不重复分析

### 审查工具
- **D-02:** 轻度工具辅助 — 引入 radon (Python 圈复杂度/MI 指标) + ESLint complexity rule 生成量化报告。radon 不需安装为项目依赖（`uv run radon` 即可），ESLint complexity 在广度扫描时配置。量化报告作为广度扫描的一部分识别高复杂度热点，再人工深潜

### Plan 结构
- **D-03:** 3-plan 结构按层组织：
  - **Plan 1 (128-01):** 全栈广度扫描 — radon + ESLint complexity 量化报告 + 所有文件快速扫描 + 风险矩阵
  - **Plan 2 (128-02):** 后端 P1 深潜 — 对广度扫描识别的后端高复杂度/高风险文件做 MAINT/ARCH-03/PERF-01 深度审查
  - **Plan 3 (128-03):** 前端 P1 深潜 + 总结 — 前端深度审查 + 跨阶段关联分析 + 最终统计

### 命名规范审查范围
- **D-04:** MAINT-03 补充审查 — Phase 123 已完成 snake_case 规范化。Phase 128 聚焦于 Phase 123 未覆盖的：误导性命名（函数名与行为不符）、不一致的抽象层级命名、过度缩写或含义不清的变量名

### 异步性能审查深度
- **D-05:** PERF-01 静态分析明确反模式 — 识别明确的异步反模式：sync I/O 在 async 函数中、未 await 的 coroutine、无限增长的集合、缺少 cleanup 的资源（如 event_manager）。不做运行时性能测试或调用链分析

### 审查策略
- **D-06:** 延续「广度优先 + 聚焦深潜」策略，与 Phase 125/126/127 一致
- **D-07:** 审查关注点向横切一致性倾斜 — 本阶段重点是跨文件的系统性问题（DRY 违反、错误处理策略不一致、日志策略不一致），而非单文件内的逻辑正确性
- **D-08:** 横切关注点 (ARCH-03) 的三个维度：
  - 错误处理策略：try-except 模式是否一致、error_utils 使用是否统一、全局异常处理是否有绕过
  - 配置管理：双重配置源（settings.py vs llm_config.yaml）的影响、环境变量的使用一致性
  - 日志策略：logger 选择（getLogger vs StructuredLogger vs RunLogger）是否一致、日志级别使用是否恰当

### 输出格式
- **D-09:** 审查发现输出到 `128-FINDINGS.md`，延续 Phase 125/126/127 的 4 级严重程度分级（Critical/High/Medium/Low）和类别标签（Maintainability/Architecture/Performance）
- **D-10:** 最终总结应包含跨阶段关联分析 — 将 128 发现与 125/126/127 发现进行交叉对比，识别系统性问题模式

### Claude's Discretion
- 广度扫描时每个文件的风险评分标准
- P1/P2 文件的具体分配（由广度扫描结果决定）
- radon 复杂度阈值（建议 A 级以上才标记为关注点）
- ESLint complexity 配置的具体阈值
- 前端组件复杂度的人工评估标准

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目规划
- `.planning/PROJECT.md` — 项目愿景、技术栈、关键决策历史
- `.planning/REQUIREMENTS.md` — v0.11.3 需求定义（MAINT-01, MAINT-02, MAINT-03, ARCH-03, PERF-01 对应本阶段）
- `.planning/ROADMAP.md` — Phase 128 定义和成功标准
- `.planning/STATE.md` — 当前项目状态

### Phase 125/126/127 产出（必须参考，引用已有发现）
- `.planning/phases/125-backend-core-review/125-FINDINGS.md` — 32 条发现，含 run_pipeline god-module、event_manager leak、dual stall detection
- `.planning/phases/125-backend-core-review/125-CONTEXT.md` — Phase 125 审查策略
- `.planning/phases/126-api/126-FINDINGS.md` — 78 条发现，含 SSE stream 异常处理、错误处理不一致
- `.planning/phases/126-api/126-CONTEXT.md` — Phase 126 审查策略
- `.planning/phases/127-frontend-review/127-FINDINGS.md` — 95 条发现，含 React Query 未使用、超大组件、JSON.parse gap
- `.planning/phases/127-frontend-review/127-CONTEXT.md` — Phase 127 审查策略

### 代码库分析
- `.planning/codebase/ARCHITECTURE.md` — 完整架构分析，含错误处理策略和横切关注点
- `.planning/codebase/STRUCTURE.md` — 全栈目录结构
- `.planning/codebase/CONCERNS.md` — 已知问题（Tech Debt、Performance、Security）— Phase 128 需验证并补充可维护性问题
- `.planning/codebase/CONVENTIONS.md` — 代码规范约定（错误处理模式、日志策略、不可变性模式）
- `.planning/codebase/INTEGRATIONS.md` — 外部集成细节
- `.planning/codebase/STACK.md` — 技术栈依赖
- `.planning/codebase/TESTING.md` — 测试策略和覆盖缺口

### 审查工具参考
- `pyproject.toml` — ruff/mypy 配置（已有工具链）
- `frontend/eslint.config.js` — ESLint 配置（需添加 complexity rule）
- `frontend/tsconfig.json` — TypeScript strict 配置

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **125/126/127-FINDINGS.md 框架** — 严重程度分级、类别标签、风险矩阵格式可直接沿用
- **已有发现引用库** — Phase 125 (32 条) + Phase 126 (78 条) + Phase 127 (95 条) = 205 条已有发现，其中部分属 MAINT/ARCH-03/PERF-01 范畴可直接引用
- **CONCERNS.md 结构化问题清单** — 已记录 Tech Debt (5 项)、Known Bugs (3 项)、Performance Bottlenecks (4 项)、Fragile Areas (3 项)

### Established Patterns
- **错误处理**: 全局异常处理器 (main.py) + error_utils (non_blocking_execute/silent_execute) + route-level HTTPException — 审查一致性
- **日志策略**: logging.getLogger(__name__) + StructuredLogger + RunLogger — 三套日志系统需审查使用一致性
- **配置管理**: Settings (.env) vs LLMConfig (YAML) 双重源 — 审查配置使用的一致性
- **Repository Pattern**: BaseRepository + _persist() — 审查是否有绕过 repository 的直接 DB 访问
- **前端状态管理**: React Query (已安装) vs manual useState+useEffect (实际使用) — 审查策略一致性

### Integration Points
- `backend/core/error_utils.py` — 横切错误处理的统一入口
- `backend/utils/logger.py` — StructuredLogger，横切日志的统一入口
- `backend/config/settings.py` — 全局配置的权威来源（但 LLM 配置有双重源）
- `frontend/src/api/client.ts` — 前端错误处理的统一入口
- `frontend/src/main.tsx` — QueryClientProvider 配置

### 已知的高复杂度文件（来自 CONCERNS.md 和 prior phases）
- `backend/agent/dom_patch.py` — 777 行，最脆弱文件
- `backend/core/action_translator.py` — 718 行，ERP 特定翻译
- `frontend/src/components/TaskModal/DataMethodSelector.tsx` — 829 行，最大组件
- `frontend/src/components/TaskModal/TaskForm.tsx` — 560 行
- `frontend/src/components/TaskModal/AssertionSelector.tsx` — 546 行
- `backend/api/routes/run_pipeline.py` — 管道编排，god-module (13+ deps)

</code_context>

<specifics>
## Specific Ideas

- 审查是 review-only：只输出发现和建议，不做代码修改
- 测试套件已删除（v0.11.0），项目当前无自测能力
- Phase 123 已完成 snake_case 命名规范化 — MAINT-03 不重复此工作
- 前端 hooks 全部使用 manual useState+useEffect+fetch 模式而非 React Query — 这是一个已知的 DRY/架构问题（Phase 127 已发现）
- 后端有 3 套日志系统（getLogger / StructuredLogger / RunLogger），使用一致性需要审查
- 双重配置源（settings.py vs llm_config.yaml）的影响需要评估 — 这是横切关注点一致性的典型案例
- event_manager memory leak (Phase 125 已发现) 和 useRunStream 无限增长数组 (Phase 127 已发现) 是跨层同类问题的典型

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 128-代码质量审查*
*Context gathered: 2026-05-03*
