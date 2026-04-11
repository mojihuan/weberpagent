# Project Research Summary

**Project:** aiDriveUITest v0.9.1 -- ERP Integration (CacheService, AccountService, TestFlowService)
**Domain:** AI-driven UI test automation -- run-scoped caching, multi-role login, test flow orchestration, Excel template extension
**Researched:** 2026-04-11
**Confidence:** HIGH

## Executive Summary

v0.9.1 adds a coordination layer to the existing aiDriveUITest platform, transforming it from "AI executes what you type" to "AI orchestrates a complete ERP test scenario with proper accounts, cached data references, and post-execution verification." The three new services (CacheService, AccountService, TestFlowService) are built entirely with Python stdlib and already-installed packages -- zero new dependencies. The implementation is an additive, backward-compatible branch: tasks without `login_role` continue using the existing execution path unchanged.

The recommended approach is to build bottom-up by dependency order: CacheService first (pure data primitive, everything depends on it), then AccountService (independent of cache, can be parallelized), then DB migration and Excel template updates (prerequisites for the integration layer), and finally TestFlowService as the orchestration layer that ties everything together. The critical risk is the two execution paths diverging in `run_agent_background()` -- the codebase already has a 340-line function, and adding a parallel path increases maintenance burden. Plan to unify into TestFlowService for all tasks after validation.

The highest-impact pitfalls involve substitution ordering (Jinja2 StrictUndefined will crash on `{{cached:key}}` if regex replacement does not run first), ContextWrapper lifecycle (separate CacheService instances for preconditions vs assertions causes split-brain state), and step numbering confusion (the AI agent's internal counter starts at 1 regardless of injected login step text). These must be addressed in the TestFlowService wiring phase, not patched later.

## Key Findings

### Recommended Stack

Zero new dependencies. All v0.9.1 capabilities use Python stdlib (dict for cache, dataclasses for DTOs, re for variable substitution, asyncio for concurrency) and already-installed packages (Jinja2 for template substitution, Pydantic for schema validation, SQLAlchemy for DB column addition, openpyxl for Excel template changes). This follows the project's explicit philosophy of minimal dependencies.

**Core technologies:**
- **Python `dict` (stdlib):** CacheService backing store -- single-process, run-scoped, O(1) lookup, GC cleanup, zero config
- **Python `@dataclass(frozen=True)` (stdlib):** AccountInfo DTO -- immutability enforced at class level, no Pydantic needed for internal DTOs
- **Python `re` + Jinja2 3.1.6:** Two-phase variable substitution -- regex replaces `{{cached:key}}` first, then Jinja2 handles `{{variable}}`, avoiding StrictUndefined crashes
- **SQLAlchemy 2.0 `mapped_column(String(20), nullable=True)`:** login_role column on Task model -- backward compatible, existing tasks get NULL
- **openpyxl 3.1.5:** Excel template update with login_role column and role dropdown validation

### Expected Features

**Must have (table stakes):**
- Run-scoped parameter cache (CacheService) -- ERP tests require cross-step data passing; without caching QA must hardcode values
- Multi-role account login (AccountService) -- real ERP testing requires different accounts for different scenarios (admin, warehouse, buyer)
- Login step injection -- when a task specifies a role, automatically prepend login steps before user-defined steps
- Cache reference syntax `{{cached:key}}` -- bridge between precondition-fetched data and AI execution
- Task model login_role field (DB migration) -- nullable for backward compatibility, existing tasks continue to work
- Excel template login_role column with dropdown -- parser extracts role, passes to Task creation
- Frontend login_role dropdown -- human-readable Chinese labels for role names

**Should have (competitive):**
- TestFlowService orchestration layer -- coordinates the full lifecycle without turning `run_agent_background()` into a 500-line monolith
- Cache precondition JSON schema -- declarative alternative to Python code for data-fetching preconditions
- Two-phase variable substitution -- explicit ordering prevents subtle template conflicts
- Cache verify assertion type -- verify cached values appear in post-execution results

**Defer (v0.9.x):**
- Step renumbering logic -- skip the regex complexity if AI Agent handles numbered steps well without it
- Login step optimization -- current 5-step injection is verbose but reliable
- Persistent cache across Runs -- stale data risk makes this a non-starter

**Explicitly exclude:**
- Account management UI (deployment concern, not test authoring)
- Multi-account concurrent login in a single Run (browser session limitation)
- Dynamic role resolution from ERP API (chicken-and-egg credential problem)
- Excel template auto-migration (subtle data loss risks)

### Architecture Approach

The architecture is a coordinator pattern: TestFlowService orchestrates AccountService (resolve credentials), CacheService (manage cross-step data), PreconditionService (execute setup with cache), AgentService (run AI execution), and AssertionService (verify results including cache values). The key integration point is a branch in `run_agent_background()`: if `task.login_role` is set, delegate to TestFlowService; otherwise, use the existing code path. Each service remains independently testable in isolation.

**Major components:**
1. **CacheService** (~30 lines) -- pure in-memory KV store scoped to a single Run, with `cache()`, `cached()`, `has()`, `all()`, `clear()` methods
2. **AccountService** (~60 lines) -- reads from `webseleniumerp/config/user_info.py`, maps role names to frozen AccountInfo dataclasses
3. **TestFlowService** (~80 lines) -- pure coordinator that delegates to all other services; handles login prefix generation, two-phase variable substitution, and assertion orchestration

### Critical Pitfalls

1. **Jinja2 StrictUndefined crashes on `{{cached:key}}` syntax** -- The existing `substitute_variables()` uses StrictUndefined. If `{{cached:key}}` reaches Jinja2 before regex replacement, the run fails with UndefinedError. Prevention: the `login_role` branch must skip the existing substitution call entirely and delegate all substitution to TestFlowService, which runs regex replacement before Jinja2.

2. **ContextWrapper split-brain (separate CacheService instances)** -- CacheService is created in multiple places: PreconditionService creates one, the assertion path may create another. Prevention: create ONE CacheService instance at the top of `run_agent_background()` and pass it to all services.

3. **Excel template column change breaks old imports** -- Inserting `login_role` at column 2 shifts all subsequent columns. Old templates fail header validation with cryptic messages. Prevention: either keep `target_url` and add `login_role` as a new column (backward compatible), or provide version-specific error messages explaining what changed.

4. **Precondition type crash (`dict.strip()`)** -- Cache-type preconditions are JSON dicts mixed with existing string preconditions. Calling `.strip()` on a dict raises AttributeError. Prevention: add isinstance dispatch before iterating preconditions.

5. **Account credentials leak into agent logs and database** -- Login step injection puts plain text credentials in the task description, which propagates to step actions, reasoning, and database records. Prevention: post-process step data to redact known credentials before saving.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: CacheService + ContextWrapper Integration
**Rationale:** CacheService is the foundation -- cache preconditions and cache assertions both depend on it. It is also the simplest component (pure data structure, ~30 lines, no external dependencies).
**Delivers:** In-memory KV cache scoped to a single Run, wired into existing ContextWrapper for precondition access.
**Addresses:** Table-stakes feature "run-scoped parameter cache"
**Avoids:** Pitfall 4 (ContextWrapper split-brain) by establishing the shared CacheService pattern from the start

### Phase 2: AccountService + Settings Update
**Rationale:** Account resolution is independent of caching -- it reads from `user_info.py` and returns frozen DTOs. Can be developed in parallel with Phase 1 results being validated.
**Delivers:** Multi-role account resolution, erp_login_url configuration field
**Addresses:** Table-stakes feature "multi-role account login"
**Uses:** Python dataclasses (frozen=True), existing sys.path lazy-loading pattern from external_precondition_bridge

### Phase 3: DB Migration + Excel Template + Frontend Dropdown
**Rationale:** The login_role field must exist in the database before the Excel parser or frontend form can use it. These three changes are tightly coupled and straightforward (LOW complexity each).
**Delivers:** Task model login_role column, updated Excel template with role dropdown, frontend role selector
**Addresses:** Table-stakes features "Task model login_role field", "Excel template login_role column", "Frontend login_role dropdown"
**Avoids:** Pitfall 3 (old template breakage) by deciding backward-compatibility strategy; Pitfall 6 (SQLite migration race) by following existing init_db() pattern with try/except

### Phase 4: TestFlowService + runs.py Integration
**Rationale:** The orchestration layer depends on all previous components. This is the highest-risk phase because it touches the existing execution pipeline and must handle substitution ordering, step numbering, credential masking, and backward compatibility.
**Delivers:** Full test flow orchestration with login injection, two-phase substitution, and cache-aware assertion execution
**Addresses:** Differentiator "TestFlowService orchestration layer", table-stakes "login step injection" and "cache reference syntax"
**Avoids:** Pitfall 1 (Jinja2 crash) by controlling substitution order; Pitfall 2 (step numbering) by NOT shifting numbers; Pitfall 5 (credential leak) by adding masking to on_step callback

### Phase 5: Cache Precondition Type + Cache Verify Assertions
**Rationale:** Advanced precondition/assertion patterns depend on CacheService working correctly. Deferred until the basic flow is validated end-to-end.
**Delivers:** JSON-config cache preconditions, cache_verify assertion type
**Addresses:** Differentiator "cache precondition JSON schema", deferred feature "cache verify assertion type"
**Avoids:** Pitfall 7 (precondition type crash) by implementing isinstance dispatch for mixed precondition arrays

### Phase Ordering Rationale

- Dependency chain: CacheService -> ContextWrapper -> PreconditionService -> TestFlowService. Building bottom-up ensures each phase has its dependencies ready.
- Phases 1 and 2 are independent (cache vs account) but Phase 4 needs both, so they must complete first.
- Phase 3 (DB + Excel + frontend) is a prerequisite for Phase 4 because TestFlowService branches on `task.login_role`, which must exist in the model.
- Phase 5 is deliberately last: it adds complexity (JSON precondition parsing, cache verify logic) that should only be built after the basic login_role flow works end-to-end.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 4:** Complex integration with the existing execution pipeline. The substitution ordering and step numbering strategies need validation with actual agent runs. Consider running a spike to verify the AI Agent's behavior with injected login steps before committing to the implementation.
- **Phase 5:** Cache precondition JSON schema design needs validation with real ERP API responses to confirm field extraction patterns work as expected.

Phases with standard patterns (skip research-phase):
- **Phase 1:** Pure data structure, well-documented Python dict patterns, no external dependencies
- **Phase 2:** Follows existing lazy-loading pattern from external_precondition_bridge.py
- **Phase 3:** Follows existing migration pattern from database.py init_db(), standard Excel template and Pydantic schema updates

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Verified against pyproject.toml and installed packages. Zero new dependencies confirmed. All version compatibility checked. |
| Features | HIGH | Based on thorough codebase analysis, existing design docs, and validated webseleniumerp integration patterns. Dependency graph is clear and well-documented. |
| Architecture | HIGH | Component boundaries and responsibilities are well-defined. Integration points with existing code identified at specific line numbers. The coordinator pattern is straightforward. |
| Pitfalls | HIGH | Based on direct code analysis of all affected files. Each pitfall references specific line numbers in the codebase. Recovery strategies are practical. |

**Overall confidence:** HIGH

### Gaps to Address

- **Login step injection AI reliability:** The design assumes the AI Agent reliably executes the 5-step login sequence. This needs end-to-end validation during Phase 4. If the agent struggles with login, the injection approach may need adjustment (e.g., Playwright API pre-navigation).
- **Batch execution + login_role interaction:** Batch execution with mixed login_role tasks (some with roles, some without) needs integration testing. The semaphore-based concurrency and per-task account resolution should work independently, but the combined path is untested.
- **Template migration UX:** The decision between keeping `target_url` for backward compatibility vs. removing it needs a definitive call during Phase 3 planning. The research recommends keeping it, but the design doc removes it.

## Sources

### Primary (HIGH confidence)
- Codebase analysis of all affected files (runs.py, precondition_service.py, external_precondition_bridge.py, models.py, database.py, excel_template.py, excel_parser.py)
- `pyproject.toml` -- verified dependency versions and zero-new-dependency confirmation
- `docs/plans/2026-04-11-erp-integration-design.md` -- design specifications
- `docs/plans/2026-04-11-erp-integration-impl.md` -- implementation plan
- `webseleniumerp/config/user_info.py` -- validated account configuration source

### Secondary (MEDIUM confidence)
- `webseleniumerp/common/file_cache_manager.py` -- JSON file cache being replaced by in-memory approach
- SQLite WAL mode documentation -- concurrency patterns for parallel browser writes
- Jinja2 StrictUndefined documentation -- variable substitution behavior under strict mode

### Tertiary (contextual)
- Previous milestone pitfalls (v0.9.0) -- SQLite concurrent writes, browser cleanup patterns inform v0.9.1 risk assessment
- PROJECT.md -- "zero new dependencies" decision record and scope boundaries

---
*Research completed: 2026-04-11*
*Ready for roadmap: yes*
