# Feature Research: ERP Integration -- Caching, Multi-Account, Test Flow Orchestration (v0.9.1)

**Domain:** AI-driven UI test automation -- run-scoped caching, multi-role account management, test flow orchestration, Excel template extension
**Researched:** 2026-04-11
**Confidence:** HIGH (findings based on thorough codebase analysis + existing design docs + webseleniumerp integration patterns already validated in production)

## Executive Summary

This document covers the six feature areas for v0.9.1: (1) CacheService for run-scoped in-memory parameter caching, (2) AccountService for multi-role login credential resolution, (3) TestFlowService for orchestrating the full test lifecycle, (4) Excel template updates with login_role column, (5) DB migration for login_role field, and (6) frontend login_role dropdown. These features transform the platform from "AI executes what you type" to "AI executes a complete ERP test scenario with proper accounts, cached data references, and post-execution verification."

The core insight: the existing platform already has all the building blocks (PreconditionService with context variables, external assertion bridge, AgentService, SSE streaming). The new features add a coordination layer (TestFlowService) and two missing data-handling primitives (CacheService for cross-step data passing, AccountService for role-based login). The design is backward compatible -- tasks without login_role continue using the existing execution path.

## Feature Landscape

### Table Stakes (Users Expect These)

Features QA testers assume exist in an "ERP test automation" platform. Missing any of these = the ERP integration feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Run-scoped parameter cache** | ERP tests require cross-step data passing: query an item number in a precondition, then verify it appears in a sales list after execution. Without caching, QA must hardcode values or use fragile multi-step state sharing. webseleniumerp already uses `ParamCache` (JSON file-based); our platform must match this capability. | LOW | `CacheService` with `cache(key, value)`, `cached(key)`, `has(key)`, `all()`, `clear()`. In-memory dict scoped to a single Run. No disk I/O. Integrated into `ContextWrapper` so preconditions can call `context.cache('i', value)` and `context.cached('i')` directly. |
| **Multi-role account login** | Real ERP testing requires different accounts for different scenarios (admin for setup, warehouse for inventory, buyer for purchases). Currently only one account is configured via `ERP_USERNAME`/`ERP_PASSWORD` environment variables. QA cannot test multi-role workflows without this. | MEDIUM | `AccountService` reads from `webseleniumerp/config/user_info.py` (already validated, contains 8 roles). Resolves role name (e.g., "main") to `AccountInfo(account, password, role)`. Login URL from `settings.erp_login_url`, NOT from Excel. AI Agent receives login steps as a prefix in the task description. |
| **Login step injection** | When a task specifies a login role, the system must automatically add "open login URL, enter account, enter password, click login" steps before the user-defined steps. QA should not need to write login steps in every task. | MEDIUM | `TestFlowService.build_login_prefix()` generates login steps. Steps are injected as the first 5 lines of the task description. User step numbers are shifted by +5. The `{{cached:key}}` syntax and `{{variable}}` substitution happen after injection. |
| **Cache reference syntax in descriptions** | QA needs a way to reference cached values in task descriptions. The pattern `{{cached:i}}` should be replaced with the actual cached value before the AI Agent sees the description. This is the bridge between "precondition fetched data" and "AI uses that data during execution." | LOW | Regex-based replacement of `{{cached:key}}` patterns before Jinja2 variable substitution. Implemented in `TestFlowService._build_description()`. Uses `re.sub()` for cache patterns, then Jinja2 for context variables. Two-phase replacement avoids conflicts with Jinja2's `{{var}}` syntax. |
| **Cache-aware precondition execution** | Excel preconditions can now be JSON configs with `type: "cache"` instead of just Python code. A cache precondition calls a data method, extracts a field from the result, and stores it in the cache. Example: query inventory list, extract IMEI from first item, cache as key 'i'. | MEDIUM | New `execute_cache_precondition()` method on `PreconditionService`. Parses JSON config, calls `context.get_data()`, extracts `cache_field` from response, stores via `context.cache(cache_key, value)`. Falls back gracefully if external module is unavailable. |
| **Cache verification in assertions** | After execution, QA needs to verify that cached values appear in results. Example: cached IMEI number should appear in the sales item list. Without this, the cache precondition is useless for verification. | MEDIUM | New assertion type `cache_verify` in the assertion JSON config. Checks that `cache.cached(cache_key)` is found in the assertion result's `match_field`. Implemented in `TestFlowService._execute_assertions()`. Uses the same assertion bridge (`execute_assertion_method()`) but adds post-execution cache matching. |
| **Excel login_role column** | QA fills in a "login role" column in the Excel template. The template must support this new column with dropdown validation for valid roles. The parser must extract it and pass it through to Task creation. | LOW | Add `login_role` to `TEMPLATE_COLUMNS` as the second column (after task name). Add `DataValidation` dropdown with role names (main, special, vice, camera, platform, super, bot, idle). Parser maps it to `TaskCreate.login_role`. |
| **Task model login_role field** | The Task database model must store the login role. Runs must be able to read it from the task and pass it to the execution pipeline. | LOW | Add `login_role VARCHAR(20) NULL` to Task model. Add to Pydantic schemas (`TaskBase`, `TaskCreate`, `TaskUpdate`, `TaskResponse`). SQLite migration via `ALTER TABLE`. Nullable for backward compatibility -- old tasks without login_role continue to work. |
| **Frontend login_role dropdown** | The task creation/edit form must show a role selector dropdown. QA should see human-readable labels (not raw role IDs). | LOW | Add `<select>` dropdown to `TaskForm.tsx` with options mapped from role IDs to Chinese labels (main = "main account", special = "warehouse account", etc.). Update TypeScript types to include `login_role?: string | null`. |
| **Backward compatibility** | Tasks created before v0.9.1 (no login_role) must continue to work exactly as before. The existing execution path in `run_agent_background()` must remain unchanged for these tasks. | LOW | Detection pattern: `if task.login_role: use TestFlowService; else: existing flow`. No changes to AgentService, AssertionService, or batch execution. The new code path is additive. |

### Differentiators (Competitive Advantage)

Features that go beyond basic ERP test automation. Not expected by QA, but significantly improve test reliability and coverage.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Orchestration layer (TestFlowService)** | Coordinates the full lifecycle: resolve account -> create cache -> execute preconditions -> build description -> AI execute -> execute assertions -> cleanup. Without this, the `run_agent_background()` function in runs.py would become an unmaintainable 500-line monolith. | MEDIUM | `TestFlowService` is a pure coordinator. It does not implement any domain logic itself -- it delegates to AccountService, CacheService, PreconditionService, AgentService, and AssertionService. This keeps each service testable in isolation. |
| **Step number renumbering after login injection** | When login steps are injected (5 steps), the user's step numbering (step 1, step 2, ...) must be shifted to (step 6, step 7, ...) so the AI Agent sees a coherent numbered sequence. This prevents the Agent from getting confused by duplicate step numbers. | LOW | Regex-based renumbering in `_build_description()`. Pattern: `^步骤(\d+)` shifted by +5. If the user does not number their steps, no renumbering occurs -- the login prefix is simply prepended. |
| **Two-phase variable substitution** | Phase 1: replace `{{cached:key}}` patterns with cache values (regex). Phase 2: replace `{{variable}}` patterns with context variables (Jinja2). This ordering matters because cache values might contain Jinja2 syntax that should not be interpreted. | LOW | `re.sub()` for cache patterns, then Jinja2 `Environment(undefined=StrictUndefined)` for context variables. If a cache value contains `{{`, it will be treated as a literal string in phase 2 (since Jinja2 StrictUndefined would fail on unknown variables). This is the correct behavior. |
| **Cache precondition JSON schema** | Instead of forcing QA to write Python code for every data-fetching precondition, the JSON config format (`type: "cache", method: "PcImport.inventory_list", params: {...}, cache_key: "i", cache_field: "imei"`) provides a structured, declarative alternative. This is more maintainable and less error-prone than raw Python. | MEDIUM | The `parse_cache_config()` function validates required fields. The `execute_cache_precondition()` method handles the entire lifecycle. Error messages are specific ("missing required field: cache_key" rather than a Python traceback). |
| **Login URL separation from Excel** | The ERP login URL is a deployment detail, not a test parameter. It should come from `settings.py` (`ERP_LOGIN_URL`), not from the Excel template. This prevents QA from accidentally using the wrong URL (e.g., staging vs production). | LOW | Add `erp_login_url: str = ""` to `Settings`. AccountService reads it via `get_settings().erp_login_url`. Excel template removes the `target_url` column (replaced by login_role + settings-based URL). |

### Anti-Features (Features to Explicitly NOT Build)

Features that seem related but would create significant complexity or violate the project's design principles.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Persistent cache across Runs** | "Cache should survive between runs so I don't need to re-query data." Persistent cache creates stale data risk (cached IMEI from yesterday's inventory query applied to today's sales test). The webseleniumerp `ParamCache` uses JSON files and has exactly this problem -- QA frequently forgets to clear cache and gets wrong verification results. | Keep cache Run-scoped (in-memory, destroyed when Run ends). Each Run starts fresh. If QA needs to share data between Runs, use the existing precondition system with explicit queries. |
| **Account management UI** | "Let QA add/edit accounts in the frontend instead of editing user_info.py." Account management is a deployment concern, not a test authoring concern. Adding CRUD UI for accounts introduces authentication, authorization, and secret management requirements that are explicitly out of scope (single-user local tool, per PROJECT.md "Out of Scope: user authentication"). | Read accounts from `webseleniumerp/config/user_info.py` (the source of truth that the QA team already maintains). If accounts change, update the file and restart the server. |
| **Dynamic role resolution from ERP API** | "Instead of hardcoding roles, query the ERP system for available roles at runtime." This requires authenticated API calls before the test starts, creating a chicken-and-egg problem (you need credentials to discover credentials). It also couples the platform to ERP API version changes. | Static `ROLE_MAP` in `AccountService` mapping role names to `user_info.py` field names. If new roles are needed, update the map and redeploy. The 8 current roles cover all documented ERP testing scenarios. |
| **Multi-account concurrent login in a single Run** | "Test with main account AND warehouse account in the same Run." The AI Agent uses a single browser session with one logged-in user. Multi-account testing requires separate browser sessions or complex session-switching, which browser-use does not support natively. | One account per Run. Multi-account scenarios are tested as separate tasks in a batch (Task A with role=main, Task B with role=special, assert Task A's data appears in Task B's view). This is the pattern webseleniumerp already uses. |
| **Excel template auto-migration** | "If I upload an old template (without login_role column), automatically add the column." Auto-migration of uploaded Excel files creates subtle data loss risks (column reordering, format stripping). It also couples the parser to template versioning, which is fragile. | Validate template headers strictly. If headers don't match the current `TEMPLATE_COLUMNS`, reject with a clear error message: "Please download the latest template." This is the same approach used by TestRail and qTest for template versioning. |
| **Cache key validation against schema** | "Validate that cache keys match a predefined schema so QA doesn't typo key names." This would require a cache schema definition system (which keys are valid, what types they hold). Over-engineering for the current use case where QA writes both the precondition (which sets the key) and the assertion (which reads it). | Let QA use any string as a cache key. If they typo a key name, the `cached()` call raises `KeyError` with a clear message ("cache key 'typo' does not exist"). This is sufficient for debugging. |
| **Login step customization** | "Let QA customize the login steps (e.g., add CAPTCHA handling, SSO redirect)." Customizable login steps require a template language or scriptable login flow. This is a separate feature entirely (not part of this milestone). The current login step injection is deliberately simple: open URL, type account, type password, click login. | Fixed login step template in `build_login_prefix()`. If the ERP login flow changes (e.g., adds CAPTCHA), update the template function and redeploy. The AI Agent is capable of handling minor variations (element positioning, label changes) without customization. |

## Feature Dependencies

```
CACHE-01: CacheService (in-memory KV cache)
    |
    +--integrates with--> CONTEXT-01: ContextWrapper cache methods
    |                       (preconditions can cache/cached via context)
    |
    +--used by--> PRECOND-01: Cache-type precondition execution
    |               (JSON config: fetch data -> extract field -> cache)
    |
    +--used by--> VERIFY-01: Cache verify in assertions
                    (check cached value appears in assertion result)

ACCOUNT-01: AccountService (multi-role account resolution)
    |
    +--reads from--> user_info.py (webseleniumerp/config/user_info.py)
    |
    +--provides--> LOGIN-01: Login step injection
    |               (build_login_prefix with account + URL)
    |
    +--requires--> SETTINGS-01: erp_login_url config
                    (new field in Settings)

DB-01: Task model login_role field
    |
    +--required by--> EXCEL-01: Excel template login_role column
    |                   (TEMPLATE_COLUMNS update + parser)
    |
    +--required by--> FRONTEND-01: login_role dropdown
    |                   (TaskForm.tsx select element)
    |
    +--required by--> FLOW-01: TestFlowService branching
                      (if login_role: new flow; else: existing flow)

FLOW-01: TestFlowService (orchestration)
    |
    +--coordinates--> ACCOUNT-01, CACHE-01, CONTEXT-01,
                      PRECOND-01, LOGIN-01, VERIFY-01
    |
    +--integrates with--> runs.py: run_agent_background()
                          (branching point: login_role present?)
```

### Dependency Notes

- **CACHE-01 is the foundation**: CacheService must be implemented first because both preconditions (cache-type) and assertions (cache_verify) depend on it. It is also the simplest component (pure in-memory dict with 5 methods).
- **ACCOUNT-01 is independent of CACHE-01**: Account resolution and caching are orthogonal concerns. They only meet in TestFlowService. These can be developed in parallel.
- **DB-01 is a prerequisite for EXCEL-01 and FRONTEND-01**: The Task model must have the `login_role` field before the Excel parser or frontend form can use it. This is a blocking dependency.
- **FLOW-01 is the integration point**: TestFlowService depends on all other components. It must be implemented last. Its tests should mock the other services.
- **EXCEL-01 and FRONTEND-01 are independent**: The Excel template update and frontend dropdown can be developed in parallel after DB-01 is complete.

## MVP Recommendation

### Build First (v0.9.1 Core)

These features form the minimum viable "ERP test with caching and multi-account" flow.

1. **CacheService** -- Pure data primitive, no external dependencies, 5 methods. Everything else depends on it.
2. **ContextWrapper integration** -- Wire cache into the existing precondition execution context. `context.cache('i', value)` and `context.cached('i')` become available in precondition code.
3. **AccountService** -- Read from `user_info.py`, resolve role to credentials. Independent of caching, can be developed in parallel.
4. **DB migration (login_role)** -- Add field to Task model. Fast SQLite ALTER TABLE. Required before Excel/frontend changes.
5. **Excel template update** -- Add login_role column with dropdown. Update parser.
6. **TestFlowService** -- Orchestration layer. Ties everything together. The `if login_role` branch in `run_agent_background()`.
7. **Frontend login_role dropdown** -- Select element in TaskForm. Quick win after backend is done.

### Defer (v0.9.x)

- **Cache verify assertion type** -- Start with manual cache verification in precondition code. The structured `cache_verify` JSON config can be added once the basic flow works.
- **Step renumbering logic** -- If AI Agent handles numbered steps well without renumbering, skip the regex complexity.
- **Login step optimization** -- Current 5-step login injection is verbose. If Agent handles it reliably, leave as-is. If not, explore shorter prompts.

### Explicitly Exclude

- Persistent cache (stale data risk)
- Account management UI (out of scope per PROJECT.md)
- Multi-account per Run (browser session limitation)
- Dynamic role resolution (unnecessary complexity)

## Interaction with Existing Features

| Existing Feature | How New Features Affect It | Risk | Mitigation |
|------------------|---------------------------|------|------------|
| **PreconditionService** | ContextWrapper gains `cache()`/`cached()` methods. Optional `CacheService` parameter in constructor. | LOW | Backward compatible: `cache=None` defaults to fresh CacheService. Existing tests that don't use cache are unaffected. |
| **run_agent_background()** | New `login_role` parameter. Branching logic: if login_role, use TestFlowService; else, existing code path. | MEDIUM | The branching must not break the existing path. Test with and without login_role. The function is already 340 lines -- adding a branch increases complexity. Consider extracting the new path to TestFlowService entirely. |
| **Excel template** | `TEMPLATE_COLUMNS` gains `login_role` column. `target_url` column is replaced. | MEDIUM | Existing templates without login_role will fail header validation. Provide clear error message. Consider a one-time migration guide for QA. |
| **TaskForm.tsx** | New dropdown field. `FormData` interface gains `login_role`. | LOW | Additive change. Existing form data without login_role continues to work (nullable field). |
| **Batch execution** | Batch tasks with different login_roles execute independently. Each Run resolves its own account. | LOW | No changes to batch execution code. The branching in `run_agent_background()` handles it per-Run. |
| **SSE streaming** | Login injection steps are visible in the step stream (steps 1-5 are login). | LOW | No SSE changes needed. Login steps appear as regular Agent steps. |
| **External precondition bridge** | `execute_data_method()` is called by cache-type preconditions. Already supports timeout protection and error handling. | LOW | No changes to the bridge. Cache preconditions use the same `context.get_data()` path that existing preconditions use. |

## Complexity Assessment

| Component | Backend LOC (est.) | Frontend LOC (est.) | Files Modified/Created | Testing Difficulty |
|-----------|---------------------|----------------------|------------------------|--------------------|
| CacheService | 30-40 | 0 | 1 new file (`cache_service.py`) | LOW -- pure data structure, deterministic |
| ContextWrapper integration | 15-20 | 0 | 1 modified file (`precondition_service.py`) | LOW -- add cache/cached methods, test delegation |
| AccountService | 50-70 | 0 | 1 new file (`account_service.py`) | LOW -- frozen dataclass + dict lookup |
| Settings update | 3-5 | 0 | 1 modified file (`settings.py`) | LOW -- add one field |
| DB migration | 10-15 | 0 | 2 modified files (models.py, schemas.py) + migration script | LOW -- nullable field, no data loss risk |
| Excel template update | 20-30 | 0 | 2 modified files (template.py, parser.py) | LOW -- add column to shared TEMPLATE_COLUMNS |
| TestFlowService | 80-120 | 0 | 1 new file (`test_flow_service.py`) | MEDIUM -- integration testing, mock dependencies |
| runs.py integration | 30-40 | 0 | 1 modified file (`runs.py`) | MEDIUM -- branching logic, backward compatibility |
| Frontend login_role | 0 | 30-50 | 3 modified files (types, form, types) | LOW -- select dropdown |
| **Total** | **240-340** | **30-50** | **7 modified, 3 new** | |

## Key Design Decisions

### 1. In-memory cache vs. JSON file cache

The webseleniumerp project uses `ParamCache` which writes JSON files to disk. This creates:
- Stale data between test runs (cache not cleared)
- File I/O overhead
- Concurrency issues (two tests writing same file)

Our CacheService uses a plain Python dict, scoped to a single Run. Advantages:
- Zero disk I/O
- Automatic cleanup (Python GC when Run ends)
- No concurrency issues (each Run has its own CacheService instance)
- Simpler implementation (30 lines vs 140 lines)

Tradeoff: cache does not survive server restart. This is acceptable because each Run should be self-contained.

### 2. Login injection via description prefix vs. separate browser navigation

Two approaches were considered:
- (A) Inject login steps as text prefix in the task description
- (B) Navigate to login URL and fill credentials via Playwright API before Agent starts

Approach (A) was chosen because:
- No changes to AgentService or browser session management
- The AI Agent already handles form filling reliably (validated in v0.6.3-v0.8.4)
- Login failures are visible as regular Agent steps (better debugging)
- Approach (B) would require a new Playwright automation layer before Agent starts, adding complexity without benefit

### 3. Cache variable syntax: `{{cached:key}}` vs `{{cache.key}}`

The `{{cached:key}}` syntax was chosen over `{{cache.key}}` because:
- Jinja2's `StrictUndefined` would fail on `cache.i` if `cache` is not in the context
- The regex approach (`re.sub(r'\{\{cached:(\w+)\}\}', ...)`) is explicit and unambiguous
- QA can distinguish cache references (`{{cached:i}}`) from precondition variables (`{{sf_no}}`) at a glance
- No risk of namespace collision between cache keys and context variables

## Sources

- Existing PreconditionService with ContextWrapper: `backend/core/precondition_service.py`
- Existing external_precondition_bridge with LoginApi integration: `backend/core/external_precondition_bridge.py`
- Existing run execution pipeline: `backend/api/routes/runs.py`
- Existing Task model: `backend/db/models.py`
- Existing Pydantic schemas: `backend/db/schemas.py`
- Existing Excel template: `backend/utils/excel_template.py`
- Existing TaskForm component: `frontend/src/components/TaskModal/TaskForm.tsx`
- Existing TypeScript types: `frontend/src/types/index.ts`
- webseleniumerp user_info.py (account configuration): `webseleniumerp/config/user_info.py`
- webseleniumerp file_cache_manager.py (JSON file cache being replaced): `webseleniumerp/common/file_cache_manager.py`
- webseleniumerp settings.py: `webseleniumerp/config/settings.py`
- ERP integration design document: `docs/plans/2026-04-11-erp-integration-design.md`
- ERP integration implementation plan: `docs/plans/2026-04-11-erp-integration-impl.md`
- Project context: `.planning/PROJECT.md`

---
*Feature research for: ERP integration -- caching, multi-account, test flow orchestration (v0.9.1)*
*Researched: 2026-04-11*
