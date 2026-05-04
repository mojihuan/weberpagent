# Codebase Concerns

**Analysis Date:** 2026-05-02

## Tech Debt

**exec() for user-provided code:**
- Issue: PreconditionService uses `exec()` to execute user-provided Python code in a thread pool. The execution environment includes `__builtins__` (full Python runtime), allowing arbitrary code execution including file system access, network calls, and process spawning.
- Files: `backend/core/precondition_service.py` (line 296)
- Impact: Any user who can create/modify tasks can execute arbitrary Python on the server. In a multi-user deployment this is a critical security hole. Currently acceptable only because the platform is single-user/internal.
- Fix approach: Sandboxed execution via RestrictedPython or a subprocess-based sandbox. At minimum, remove `__builtins__` and provide an explicit safe subset.

**Monkey-patching browser-use internals:**
- Issue: `dom_patch.py` monkey-patches 4 different browser-use internal classes (`ClickableElementDetector`, `PaintOrderRemover`, `DOMTreeSerializer`, `_assign_interactive_indices`). These patches will break silently when browser-use is upgraded and the internal API changes.
- Files: `backend/agent/dom_patch.py` (777 lines)
- Impact: browser-use version upgrades become high-risk. Patches are applied globally and once (`_PATCHED` flag), so stale patches from a prior run persist across the process lifetime.
- Fix approach: Wrap each patch in version-checking guards that log warnings or fail fast when the expected method signatures are absent. Consider contributing patches upstream to browser-use.

**Manual schema migrations in init_db():**
- Issue: Database schema evolution is handled by manual `ALTER TABLE` statements inside `init_db()`, each labeled with a Phase number. As phases accumulate, init_db grows linearly. There is no migration tracking -- every column check runs on every startup.
- Files: `backend/db/database.py` (lines 44-93)
- Impact: Schema changes are fragile, no rollback capability, and the startup cost increases over time.
- Fix approach: Introduce Alembic migrations or a simple migration table that tracks applied migrations and skips them on subsequent starts.

**Duplicated LLM configuration paths:**
- Issue: LLM configuration exists in two parallel systems: `backend/llm/config.py` (LLMConfig, reads from `config/llm_config.yaml`) and `backend/config/settings.py` (Settings, reads from `.env`). The `LLMFactory` uses LLMConfig while `run_pipeline.py` reads from Settings directly. This creates confusion about which config source is authoritative.
- Files: `backend/llm/config.py`, `backend/llm/factory.py`, `backend/config/settings.py`, `backend/api/routes/run_pipeline.py`
- Impact: Settings may diverge between LLMFactory and pipeline. New developers may not know which to modify.
- Fix approach: Consolidate into a single configuration source. Settings (pydantic-settings) is the right choice since it supports `.env` and is already used by the pipeline. Remove or archive `config/llm_config.yaml` and LLMConfig.

**Module-level mutable global state in external_module_loader:**
- Issue: `external_module_loader.py` uses 14 module-level global variables for caching (e.g., `_pre_front_class`, `_operations_cache`, `_path_configured`). These are mutated by `_lazy_load()` and `reset_cache()`. The globals are accessed via `globals()[var_name]` dynamic lookup which is fragile.
- Files: `backend/core/external_module_loader.py` (lines 17-43)
- Impact: Testing requires explicit `reset_cache()` calls. Thread safety is not guaranteed. The dynamic `globals()` lookup is error-prone if variable names are misspelled.
- Fix approach: Encapsulate in a class (e.g., `ExternalModuleRegistry`) with explicit attributes instead of dynamic globals lookup.

## Known Bugs

**8-character UUID collision risk:**
- Symptoms: All primary keys are 8 hex characters from `uuid.uuid4().hex[:8]`, giving only 4 billion possible values. While unlikely, collisions will cause silent data corruption (INSERT will fail on primary key conflict).
- Files: `backend/db/models.py` (line 14, `generate_id()`)
- Trigger: Creating many tasks/runs over time. At ~10,000 records, collision probability becomes non-negligible (birthday problem).
- Workaround: None. The error would surface as an unhandled IntegrityError.

**Batch fire-and-forget execution:**
- Symptoms: In `backend/api/routes/batches.py` line 68, `asyncio.create_task(service.start(run_configs))` is fire-and-forget. If the server restarts mid-batch, all progress is lost with no recovery mechanism.
- Files: `backend/api/routes/batches.py` (line 68)
- Trigger: Server restart or crash during batch execution.
- Workaround: None. Runs stuck in "running" status would need manual DB cleanup.

**Event manager memory leak:**
- Symptoms: `EventManager._events` stores all SSE events per run_id indefinitely. Only `cleanup()` removes them, but cleanup is never called anywhere in the codebase.
- Files: `backend/core/event_manager.py` (lines 27-28, `cleanup()` method never invoked)
- Trigger: Long-running server accumulates event history for every run ever executed.
- Workaround: Server restart clears memory. Not problematic for short-lived processes but becomes an issue for long uptime.

## Security Considerations

**CORS allows all origins:**
- Risk: `allow_origins=["*"]` in `backend/api/main.py` (line 79) permits any website to make requests to the API. Combined with no authentication, this exposes the full API to cross-origin attacks.
- Files: `backend/api/main.py` (lines 76-83)
- Current mitigation: Platform is internal/single-user. No deployment to public internet documented.
- Recommendations: Restrict to the frontend origin in production. Add at minimum API key authentication.

**No authentication or authorization:**
- Risk: All API endpoints are unauthenticated. Anyone with network access can create tasks, execute runs, read reports, and trigger code execution. The `subprocess.run` in `runs_routes.py` (line 108) allows arbitrary pytest execution.
- Files: `backend/api/routes/runs_routes.py` (line 108), all route files
- Current mitigation: Internal network deployment assumption.
- Recommendations: Add authentication middleware. At minimum, an API key header check for non-GET endpoints.

**Stack traces exposed in production:**
- Risk: The general exception handler in `backend/api/main.py` (line 146) includes `traceback.format_exc()` in the response when DEBUG logging is enabled. Since the lifespan sets `logging.DEBUG` globally (line 44), stack traces are always included in error responses.
- Files: `backend/api/main.py` (lines 132-149)
- Current mitigation: None. DEBUG level is hardcoded.
- Recommendations: Use the actual LOG_LEVEL from settings to control this behavior. Never include stack traces in non-debug mode.

**Credentials in generated test files:**
- Risk: `PlaywrightCodeGenerator` embeds login credentials (account/password) directly into generated test files as string literals (line 201: `_form_login(page, "{origin}", "{account}", "{password}")`). These files are stored on disk and served via the code viewer API.
- Files: `backend/core/code_generator.py` (lines 197-201), `backend/api/routes/runs_routes.py` (code viewer endpoint)
- Current mitigation: Generated code is within `outputs/` directory with path validation.
- Recommendations: Consider storing credentials separately and injecting at test execution time rather than embedding in generated files.

**LLM API keys logged partially:**
- Risk: `backend/core/auth_service.py` (line 85) logs the first 20 characters of the access token. While not the full token, this leaks enough to potentially identify the token.
- Files: `backend/core/auth_service.py` (line 85)
- Current mitigation: Only visible in server logs.
- Recommendations: Redact token logging entirely or use `***REDACTED***`.

## Performance Bottlenecks

**SQLite with connection pool for concurrent writes:**
- Problem: SQLite is single-writer. The connection pool is set to `pool_size=5` but `max_overflow=0`. During batch execution with concurrency=2-4, writes from parallel runs will contend on the SQLite lock. The `connect_args={"timeout": 30}` only makes them wait longer, not faster.
- Files: `backend/db/database.py` (lines 19-27)
- Cause: SQLite is not designed for concurrent write workloads.
- Improvement path: For production, migrate to PostgreSQL. For current scale (internal tool, single user), the 30s timeout is a reasonable mitigation but will degrade with more concurrent users.

**selectinload N+1 on task list:**
- Problem: `TaskRepository.list()` eagerly loads `Task.assertions` and `Task.runs` via `selectinload()` for every task. For large task lists, this generates 2 additional queries per list call regardless of whether the caller needs assertions/runs data.
- Files: `backend/db/repository.py` (lines 64-70)
- Cause: Eager loading is convenient but unnecessary for list endpoints.
- Improvement path: Use lazy loading for list endpoints and only `selectinload` for detail views. Or use `load_only()` to limit columns.

**DOM serialization and hashing on every step:**
- Problem: `_extract_browser_state()` calls `dom_state.llm_representation()` and then `hashlib.sha256()` on the full DOM string on every agent step. For complex ERP pages, the DOM representation can be very large (tens of KB), and this happens synchronously in the step callback.
- Files: `backend/core/agent_service.py` (lines 386-414)
- Cause: Stall detection requires DOM hashing, but the full DOM string is computed even when not needed.
- Improvement path: Cache or skip DOM hashing when the previous step had no stall indicators. Consider using a faster hash or sampling.

**screenshot base64 decode on every step:**
- Problem: Every agent step triggers `save_screenshot()` which base64-decodes the screenshot and writes it to disk. Screenshots can be 100KB-1MB+ in base64. This is I/O-bound work happening in the async event loop context.
- Files: `backend/core/agent_service.py` (lines 98-128)
- Cause: Screenshots are always captured and saved.
- Improvement path: Offload file writing to a thread pool via `run_in_executor`. Or make screenshot capture optional for faster execution.

## Fragile Areas

**DOM patching for ERP-specific behavior:**
- Files: `backend/agent/dom_patch.py` (777 lines, largest file in the codebase)
- Why fragile: Deeply coupled to browser-use internal class structure. Patches 4 different classes and 7 different methods. The hardcoded ERP-specific class names (`hand`, `el-checkbox`), placeholder text (`"sales amount"`, `"logistics fee"`), and IMEI regex (`I\d{15}`) are all specific to one ERP application.
- Safe modification: Changes to patch logic require understanding browser-use internals. When upgrading browser-use, re-test all patches.
- Test coverage: No unit tests for dom_patch logic. Only verified through manual E2E runs.

**Action translator with hardcoded ERP knowledge:**
- Files: `backend/core/action_translator.py` (718 lines)
- Why fragile: The translator contains ERP-specific heuristics for locator generation, including table row/column strategies and specific DOM patterns. Changing the ERP frontend would require updating these heuristics.
- Safe modification: New action types can be added safely. Existing type handlers should not be changed without E2E verification.
- Test coverage: No dedicated unit tests found for the translator.

**External module loading with sys.path manipulation:**
- Files: `backend/core/external_module_loader.py`, `backend/core/precondition_service.py`
- Why fragile: Both files independently add paths to `sys.path`. The order of path insertion matters for import resolution. `reset_cache()` also manipulates `sys.modules` to force re-imports, which can break other imports in the same process.
- Safe modification: Changes to the external module path configuration require restarting the server to take full effect.
- Test coverage: No unit tests for module loading edge cases.

## Scaling Limits

**SQLite single-database file:**
- Current capacity: Suitable for single-user, dozens of concurrent runs.
- Limit: SQLite's single-writer lock means batch execution with concurrency > 2 will see lock contention. Database file growth is unbounded (no cleanup strategy).
- Scaling path: Migrate to PostgreSQL for multi-user deployment. Add periodic cleanup of old runs/reports.

**No pagination on task and run lists:**
- Current capacity: Returns all tasks/runs without pagination limits.
- Limit: `TaskRepository.list()` and `RunRepository.list_with_details()` load all records with eager-loaded relationships. Performance degrades linearly with data volume.
- Scaling path: Add pagination parameters (page, page_size) to list endpoints. `ReportRepository` already has pagination; apply the same pattern to Task and Run repositories.

**In-memory event storage:**
- Current capacity: All SSE events stored in memory (dict of lists). Reasonable for tens of concurrent runs.
- Limit: Never cleaned up. After hundreds of runs, memory grows indefinitely.
- Scaling path: Add TTL-based cleanup or cap events per run. Call `event_manager.cleanup()` when a run finishes.

## Dependencies at Risk

**browser-use (>=0.12.2):**
- Risk: Core browser automation dependency. The project deeply monkey-patches its internals (dom_patch.py). Major version upgrades will likely break patches.
- Impact: Agent execution, DOM serialization, locator generation all depend on browser-use internals.
- Migration plan: Pin exact version in production. Create integration test suite that validates patches after upgrades.

**nest_asyncio (>=1.5.0):**
- Risk: Used as a workaround for running async code from within async contexts. This is a known antipattern and can cause subtle event loop issues. The library has limited maintenance activity.
- Impact: Used in `precondition_service.py` for `execute_data_method_sync()` and in generated test code.
- Migration plan: Refactor to avoid nested event loops. Use `asyncio.run_in_executor` consistently or restructure to keep everything async.

## Missing Critical Features

**No authentication/authorization system:**
- Problem: No user management, login, or API key verification. All endpoints are open.
- Blocks: Multi-user deployment, public internet deployment.

**No rate limiting:**
- Problem: No protection against rapid task creation or concurrent run execution limits beyond batch concurrency.
- Blocks: Protection against accidental or intentional resource exhaustion.

**No run cleanup/archival:**
- Problem: Runs, steps, screenshots, and generated code accumulate indefinitely. No mechanism to archive or delete old data.
- Blocks: Long-term production deployment without disk space concerns.

## Test Coverage Gaps

**No backend unit tests:**
- What's not tested: No Python unit test files exist under `backend/`. Zero backend code coverage.
- Files: All `backend/core/*.py`, `backend/agent/*.py`, `backend/api/routes/*.py`
- Risk: Refactoring or feature changes can break critical paths (agent execution, code generation, precondition execution) without detection.
- Priority: High -- core logic like `action_translator.py`, `step_code_buffer.py`, and `dom_patch.py` contain complex translation and detection logic that would benefit greatly from unit tests.

**No API integration tests:**
- What's not tested: API endpoint behavior (create task, run agent, get report) is not tested in isolation.
- Files: `backend/api/routes/*.py`
- Risk: API contract changes or regressions are only caught by E2E tests.
- Priority: Medium -- FastAPI's TestClient makes integration tests straightforward to add.

**E2E tests depend on live server:**
- What's not tested: E2E tests (7 spec files, 2596 lines) require a running backend server with browser-use configured. They are not self-contained and cannot run in CI without full environment setup.
- Files: `e2e/tests/*.spec.ts`
- Risk: E2E tests are likely run manually, not in CI. Regressions may go undetected.
- Priority: Medium -- add mock-based E2E tests or CI pipeline with full environment.

**Frontend has no tests:**
- What's not tested: No unit or component tests for React frontend components.
- Files: `frontend/src/**/*.tsx`, `frontend/src/**/*.ts`
- Risk: UI regressions in complex components like `DataMethodSelector.tsx` (829 lines), `TaskForm.tsx` (560 lines), `AssertionSelector.tsx` (546 lines).
- Priority: Low -- UI is relatively stable and can be verified visually.

---

*Concerns audit: 2026-05-02*
