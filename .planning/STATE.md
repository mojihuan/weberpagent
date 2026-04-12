---
gsd_state_version: 1.0
milestone: v0.9.1
milestone_name: ERP 全面集成重构
status: Phase complete — ready for verification
stopped_at: Completed 77-02-PLAN.md
last_updated: "2026-04-12T00:30:13.247Z"
progress:
  total_phases: 5
  completed_phases: 4
  total_plans: 7
  completed_plans: 7
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-11)

**Core value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告
**Current focus:** Phase 77 — testflowservice-runs-py-integration

## Last Shipped

**v0.9.0 Excel 批量导入功能开发** (2026-04-09)

- Phase 70: Excel 模版设计 — TEMPLATE_COLUMNS + generate_template() + ExcelParser
- Phase 71: 批量导入工作流 — ImportModal 三步状态机 + 原子批量创建
- Phase 72: 批量执行引擎 — Semaphore 并发控制 + BatchExecutionService
- Phase 73: 批量进度 UI — 2s 轮询 + 任务卡片 + 点击导航

**Server online**: 121.40.191.49

## Current Position

Phase: 77 (testflowservice-runs-py-integration) — EXECUTING
Plan: 2 of 2

## Performance Metrics

**Velocity:**

- Total plans completed: 0 (this milestone)
- Previous milestone (v0.9.0): 8 plans across 4 phases

*Updated after each plan completion*

## Accumulated Context

### Decisions

Key decisions moved to PROJECT.md Key Decisions table.
v0.9.0 decisions archived in milestones/v0.9.0-ROADMAP.md.

Recent decisions affecting current work:

- v0.9.1: CacheService 用 Python dict 而非 Redis — 单进程部署，内存足够
- v0.9.1: AccountInfo frozen dataclass — 不可变性保证，无需 Pydantic
- v0.9.1: login_role nullable 列 — 向后兼容，现有任务不受影响
- [Phase 74]: Bidirectional deepcopy: copy.deepcopy on both cache() store and cached() retrieve for full immutability isolation
- [Phase 74]: Keyword-only cache parameter prevents positional argument breakage across 15+ call sites
- [Phase 76]: login_role nullable VARCHAR(20) -- backward compatible, existing tasks unaffected
- [Phase 76]: login_role in from_orm_model() result dict -- prevents API silently omitting the field
- [Phase 77]: Regex phase before Jinja2 phase in _build_description -- prevents StrictUndefined crash on {{cached:xxx}}
- [Phase 77]: Missing cache keys produce empty string + warning log, not KeyError -- graceful degradation per D-05
- [Phase 77]: Jinja2 UndefinedError caught gracefully -- returns original text with warning log
- [Phase 77]: login_role=None default ensures zero regression for existing tasks
- [Phase 77]: Lazy imports inside if login_role block avoid circular dependencies, keep non-login path unchanged
- [Phase 77]: Shared CacheService created once at function top, threaded through PreconditionService and assertion ContextWrapper

### Pending Todos

None.

### Blockers/Concerns

- Jinja2 StrictUndefined 对 {{cached:key}} — 需在 regex 替换后再传 Jinja2，否则 UndefinedError
- ContextWrapper split-brain — 必须在 run_agent_background 顶部创建唯一 CacheService 实例
- Excel 模板列变更兼容性 — 新增 login_role 列可能影响旧模板导入

### Source-Verified Facts (2026-04-11)

- user_info.py: 7 种 UI 登录角色 (main/special/vice/camera/platform/super/idle)，bot 角色使用 phone+wechatId 登录不适用
- api_login.py: platform 角色密码字段为 INFO['password']（非 super_admin_password）
- base_params.py: PcImport.CtRBRcFNn2LnUPfJF5Yhu(i=2) 返回 list[dict]，包含 imei/articlesNo 字段
- base_url.py: 登录接口 CDQ3XEEfT = {ENV}/auth/login，测试环境 erptest.epbox.cn

## Session Continuity

Last session: 2026-04-12T00:30:13.245Z
Stopped at: Completed 77-02-PLAN.md
Resume file: None
