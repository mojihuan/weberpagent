# Phase 129: 测试规划 - Context

**Gathered:** 2026-05-03
**Status:** Ready for planning

<domain>
## Phase Boundary

基于 Phase 125-128 审查发现，识别缺失测试场景和边界覆盖不足，输出按 ROI 排序的测试优先级清单。

**范围：**
- 从 Phase 125-128 的 ~390 条审查发现中推导可测试验证的场景
- 按 Critical/High/Medium/Low 严重程度驱动优先级排序
- 后端测试场景优先（单元测试 > 集成测试），前端和 E2E 补充
- 输出测试场景清单，不写测试代码

**不在范围内：** 编写测试代码、创建测试基础设施（conftest.py/fixtures）、配置测试框架 — 这些属于后续里程碑的实施工作。

**与 Phase 125-128 的关系：**
- Phase 125 (后端核心): 32 条发现，含 run_pipeline god-module、dual stall detection、event_manager leak
- Phase 126 (API 层): 78 条发现，含 SSE stream 异常处理、execute_run_code path validation、错误处理不一致
- Phase 127 (前端): 95 条发现，含 React Query 未使用、JSON.parse gap、TaskForm stale data
- Phase 128 (代码质量): 81+ 条发现，含 5 个系统性模式（memory leak、error handling gap、dead code、blocking ops、mutable state）

</domain>

<decisions>
## Implementation Decisions

### 优先级策略
- **D-01:** 严重程度驱动排序 — 按 Phase 125-128 发现的严重程度 (Critical > High > Medium > Low) 排序测试场景优先级。直接保护最高风险区域
- **D-02:** 从审查发现推导 — 不是独立做边界分析，而是从 390 条审查发现中筛选「写测试能防回归」的部分。不需要覆盖全部发现，只识别有回归保护价值的场景

### 测试分层
- **D-03:** 后端优先 — 按后端单元测试 → 后端集成测试 → 前端组件测试 → E2E 补充的顺序组织。后端无测试保护、风险最高，优先建立基线
- **D-04:** E2E 现有覆盖补充 — 已有 7 个 E2E spec 文件，识别缺失的 E2E 场景但不作为重点

### 输出格式
- **D-05:** 仅输出清单 — Phase 129 是 review-only，不写测试代码、不设计 fixtures/mocks、不创建测试基础设施
- **D-06:** 延续 FINDINGS 格式 — 输出到 `129-FINDINGS.md`，与 Phase 125-128 保持格式一致。按严重程度分级、分层组织
- **D-07:** 每个测试场景包含：场景名称、描述、对应审查发现引用（如 "See 125-FINDINGS.md #BD-08"）、推荐测试类型（unit/integration/e2e）、优先级

### Plan 结构
- **D-08:** 建议延续 3-plan 结构：
  - **Plan 1 (129-01):** 汇总分析 — 读取 125-128 FINDINGS，筛选可测试验证的发现，按严重程度排序
  - **Plan 2 (129-02):** 后端测试场景详列 — 对后端 Critical/High 发现推导具体测试场景（单元 + 集成）
  - **Plan 3 (129-03):** 前端 + E2E 测试场景 + 总结 — 前端和 E2E 补充场景 + 最终统计

### Claude's Discretion
- 每条发现是否「适合写测试」的判断标准
- 后端单元测试与集成测试的边界划分
- E2E 缺失场景的具体优先级排序
- 最终统计数据和分组方式

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目规划
- `.planning/PROJECT.md` — 项目愿景、技术栈、关键决策历史
- `.planning/REQUIREMENTS.md` — v0.11.3 需求定义（TEST-01, TEST-02 对应本阶段）
- `.planning/ROADMAP.md` — Phase 129 定义和成功标准
- `.planning/STATE.md` — 当前项目状态

### Phase 125-128 产出（核心输入）
- `.planning/phases/125-backend-core-review/125-FINDINGS.md` — 32 条发现（后端核心逻辑）
- `.planning/phases/125-backend-core-review/125-CONTEXT.md` — Phase 125 审查策略
- `.planning/phases/126-api/126-FINDINGS.md` — 78 条发现（API 层 + 安全）
- `.planning/phases/126-api/126-CONTEXT.md` — Phase 126 审查策略
- `.planning/phases/127-frontend-review/127-FINDINGS.md` — 95 条发现（前端）
- `.planning/phases/127-frontend-review/127-CONTEXT.md` — Phase 127 审查策略
- `.planning/phases/128-代码质量审查/128-FINDINGS.md` — 81+ 条发现（代码质量）— 含 5 个系统性模式总结
- `.planning/phases/128-代码质量审查/128-CONTEXT.md` — Phase 128 审查策略

### 代码库分析
- `.planning/codebase/TESTING.md` — 测试策略、覆盖缺口、推荐测试添加清单、E2E 现有结构
- `.planning/codebase/ARCHITECTURE.md` — 完整架构分析（测试场景推导需理解数据流和模块关系）
- `.planning/codebase/CONCERNS.md` — 已知问题清单（需验证哪些有测试保护价值）
- `.planning/codebase/STRUCTURE.md` — 目录结构（确定测试文件组织位置）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **TESTING.md 推荐清单** — 已有按文件建议的测试添加清单（repository CRUD、schemas validation、error_utils、excel_parser 等），但未按 ROI 排序。可作为基础输入
- **125-128 FINDINGS 的严重程度标签** — 已分级为 Critical/High/Medium/Low，可直接用于排序
- **5 个系统性模式 (CP-1~CP-5)** — Phase 128 识别的跨层系统性问题，适合推导跨模块集成测试场景
- **E2E 测试结构** — 已有 7 个 spec 文件和清晰的测试模式（conditional skip、bilingual locator、timeout 策略），可作为 E2E 补充的参考基线

### Established Patterns
- **FINDINGS 格式** — 4 级严重程度 + 类别标签 + 位置 + 描述 + 建议，Phase 129 延续此格式
- **Review-only 策略** — Phase 125-128 均为只输出发现不改代码，Phase 129 保持一致
- **3-plan 结构** — 广度扫描 → 深度分析 → 总结，已被验证有效

### Integration Points
- 129-FINDINGS.md 中的测试场景将作为后续测试实施里程碑的输入需求
- TESTING.md 中的 fixture/工具建议与 129 场景清单需保持一致
- 后续里程碑需创建 `backend/tests/` 目录和 `conftest.py` 基础设施

</code_context>

<specifics>
## Specific Ideas

- 测试套件已删除（v0.11.0 Phase 120），项目当前无自测能力
- 后端 pytest + pytest-asyncio 依赖已在 pyproject.toml 中，但无 conftest.py、无 tests/ 目录
- 前端无测试框架（无 vitest/jest/testing-library）
- E2E 有 Playwright 配置和 7 个 spec 文件，但使用 conditional skip（外部依赖不可用时跳过）
- Phase 128 识别的 5 个系统性模式（CP-1~CP-5）是高 ROI 的集成测试候选
- TESTING.md 建议的 mock 策略：LLM calls 和 Browser session 应 mock，DB operations 用 in-memory SQLite

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 129-测试规划*
*Context gathered: 2026-05-03*
