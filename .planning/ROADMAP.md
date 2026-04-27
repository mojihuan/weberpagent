# Roadmap: aiDriveUITest

## Milestones

- 🔄 **v0.10.7 生成测试代码行为优化** — Phases 105-107 (in progress)
- ✅ **v0.10.6 生成测试代码稳定可用** — Phases 102-104 (shipped 2026-04-25)
- ✅ **v0.10.5 生成测试代码修复与优化** — Phases 99-101 (shipped 2026-04-24)
- ✅ **v0.10.4 Playwright 代码验证与任务管理集成** — Phases 97-98 (shipped 2026-04-24)
- ✅ **v0.10.3 DOM 深度修复 - 表格单元格选择精确性** — Phases 94-96 (shipped 2026-04-23)
- ✅ **v0.10.2 测试验证与代码可用性修复** — Phases 90-93 (shipped 2026-04-23)
- ✅ **v0.10.1 代码登录及 Agent 复用登录的浏览器状态** — Phases 86-89 (shipped 2026-04-21)
- ✅ **v0.10.0 Agent 执行速度优化** — Phases 82-85 (shipped 2026-04-18)
- ✅ **v0.9.2 Cookie 预注入免登录** — Phases 79-81 (shipped 2026-04-17)
- ✅ **v0.9.1 ERP 全面集成重构** — Phases 74-78 (shipped 2026-04-12)
- ✅ **v0.9.0 Excel 批量导入功能开发** — Phases 70-73 (shipped 2026-04-09)
- ✅ **v0.8.4 基于 v0.8.3 的研究优化** — Phases 67-69 (shipped 2026-04-07)
- ✅ **v0.8.3 分析报告差距对表格填写影响** — Phases 65-66 (shipped 2026-04-06)
- ✅ **v0.8.2 浏览器模式差异调查** — Phases 63-64 (shipped 2026-04-06)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-04-03)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-04-03)

## Phases

<details open>
<summary>🔄 v0.10.7 生成测试代码行为优化 (Phases 105-107) — IN PROGRESS</summary>

- [x] Phase 105: 代码生成质量修复 — TRANSLATE + INDENT
  **Plans:** 2 plans (Wave 1 parallel)
  - [x] 105-01-PLAN.md — ActionTranslator 翻译质量修复：未知操作参数摘要 + 核心类型回归测试 (TRANSLATE-01, TRANSLATE-02)
  - [x] 105-02-PLAN.md — PlaywrightCodeGenerator 缩进修正 + validate_syntax 集成 (INDENT-01, INDENT-02, INDENT-03)
- [x] Phase 106: 定位器质量优化 — LOCATOR (2/2 plans) — completed 2026-04-26
  - [x] 106-01-PLAN.md — TDD: icon font 过滤 + exact 阈值 + 相对 XPath 实现 (LOCATOR-01, LOCATOR-02, LOCATOR-03, LOCATOR-04)
  - [x] 106-02-PLAN.md — 下游测试断言同步 + 全量回归验证 (LOCATOR-01, LOCATOR-02, LOCATOR-03, LOCATOR-04)
- [ ] Phase 107: 自愈修复增强 + E2E — HEAL + E2E
  **Plans:** 2 plans
  - [ ] 107-01-PLAN.md — 自愈修复核心: 内容匹配多行替换 + DOM 精准映射 + LLM prompt 结构化 (HEAL-01, HEAL-02, HEAL-03, HEAL-04)
  - [ ] 107-02-PLAN.md — E2E healing pipeline 测试 + 全量回归验证 (E2E-01, E2E-02)

</details>

<details>
<summary>✅ v0.10.6 生成测试代码稳定可用 (Phases 102-104) — SHIPPED 2026-04-25</summary>

- [x] Phase 102: 执行修复 (1/1 plans) — completed 2026-04-24
- [x] Phase 103: 自愈改进 (1/1 plans) — completed 2026-04-24
- [x] Phase 104: E2E 验证 (1/1 plans) — completed 2026-04-25

</details>

<details>
<summary>✅ v0.10.5 生成测试代码修复与优化 (Phases 99-101) — SHIPPED 2026-04-24</summary>

- [x] Phase 99: 核心键名修复 (2/2 plans) — completed 2026-04-24
- [x] Phase 100: 操作翻译扩展 (2/2 plans) — completed 2026-04-24
- [x] Phase 101: 测试验证 (2/2 plans) — completed 2026-04-24

</details>

<details>
<summary>✅ v0.10.4 Playwright 代码验证与任务管理集成 (Phases 97-98) — SHIPPED 2026-04-24</summary>

- [x] Phase 97: 后端 API (2/2 plans) — completed 2026-04-23
- [x] Phase 98: 前端 UI (2/2 plans) — completed 2026-04-24

</details>

<details>
<summary>✅ v0.10.3 DOM 深度修复 - 表格单元格选择精确性 (Phases 94-96) — SHIPPED 2026-04-23</summary>

- [x] Phase 94: DOM Patch 增强 (2/2 plans) — completed 2026-04-23
- [x] Phase 95: Prompt 更新 (1/1 plans) — completed 2026-04-23
- [x] Phase 96: E2E 验证 (1/1 plans) — completed 2026-04-23

</details>

<details>
<summary>✅ v0.10.2 测试验证与代码可用性修复 (Phases 90-93) — SHIPPED 2026-04-23</summary>

- [x] Phase 90: 过时测试清理 (2/2 plans) — completed 2026-04-21
- [x] Phase 91: 测试代码修复 (2/2 plans) — completed 2026-04-21
- [x] Phase 92: DataMethodError 修复 (2/2 plans) — completed 2026-04-21
- [x] Phase 93: 端到端可用性验证 (1/1 plan) — completed 2026-04-22

</details>

<details>
<summary>✅ v0.10.1 代码登录及 Agent 复用登录的浏览器状态 (Phases 86-89) — SHIPPED 2026-04-21</summary>

- [x] Phase 86: 登录机制研究 (2/2 plans) — completed 2026-04-20
- [x] Phase 87: 代码登录修复与集成 (1/1 plans) — completed 2026-04-21
- [x] Phase 88: 认证代码清理 (2/2 plans) — completed 2026-04-21
- [x] Phase 89: 测试覆盖 (1/1 plans) — completed 2026-04-21

</details>

<details>
<summary>✅ Older milestones (v0.9.0 — v0.6.2)</summary>

- ✅ **v0.9.2 Cookie 预注入免登录** — Phases 79-81 (shipped 2026-04-17)
- ✅ **v0.10.0 Agent 执行速度优化** — Phases 82-85 (shipped 2026-04-18)
- ✅ **v0.9.1 ERP 全面集成重构** — Phases 74-78 (shipped 2026-04-12)
- ✅ **v0.9.0 Excel 批量导入功能开发** — Phases 70-73 (shipped 2026-04-09)
- ✅ **v0.8.4 基于 v0.8.3 的研究优化** — Phases 67-69 (shipped 2026-04-07)
- ✅ **v0.8.3 分析报告差距对表格填写影响** — Phases 65-66 (shipped 2026-04-06)
- ✅ **v0.8.2 浏览器模式差异调查** — Phases 63-64 (shipped 2026-04-06)
- ✅ **v0.8.1 修复销售出库表格填写问题** — Phase 62 (shipped 2026-04-06)
- ✅ **v0.8.0 报告完善与 UI 优化** — Phases 57-61 (shipped 2026-04-03)
- ✅ **v0.7.0 更多操作边界测试** — Phases 52-56 (shipped 2026-04-01)
- ✅ **v0.6.3 Agent 可靠性优化** — Phases 48-51 (shipped 2026-04-03)
- ✅ **v0.6.2 回归原生 browser-use** — Phases 45-47 (shipped 2026-04-03)

</details>

---
*Roadmap updated: 2026-04-27 — Phase 107 plans created*
