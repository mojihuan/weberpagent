# Phase 126: API Layer & Security Review - Findings

**Review Date:** 2026-05-03
**Scope:** 13 API layer files (~2,114 lines) + helpers.py + schemas/index.py
**Methodology:** Breadth-first scan + CONCERNS.md verification (per D-05)

## Tool Results

### ruff Scan

17 issues found (5 fixable):

```
E402 [x12] Module level import not at top of file  -- backend/api/main.py:21-34
F401 [*] `asyncio` imported but unused              -- backend/api/routes/run_pipeline.py:7
F401 [*] `fastapi.HTTPException` imported but unused -- backend/api/routes/run_pipeline.py:14
F401 [*] `backend.db.repository.TaskRepository` imported but unused -- backend/api/routes/run_pipeline.py:19
F401 [*] `backend.db.repository.StepRepository` imported but unused -- backend/api/routes/run_pipeline.py:19
F401 [*] `backend.db.schemas.TaskUpdate` imported but unused -- backend/api/routes/run_pipeline.py:29
```

**Notable:** The 12 E402 errors in main.py are caused by proxy environment variable cleanup (lines 18-19) that must execute before library imports. This is an intentional ordering constraint, not a code quality issue. The 5 unused imports in run_pipeline.py are leftovers from when pipeline code was part of the larger runs.py file (confirmed in Phase 125 findings).

### mypy Scan

58 errors in API layer files. Key categories:

- **response.py:** 3 errors -- implicit Optional on `meta`, `request_id`, `stack` parameters. These functions are unused by any route.
- **tasks.py:** 2 errors -- `create_task` and `update_task` return ORM `Task` instead of `TaskResponse` (return type mismatch).
- **run_pipeline.py:** 1 error -- `_build_description` receives `str | None` where `str` expected for `login_url`.
- **runs_routes.py:** 23 errors -- extensive None-safety issues on ORM relationships (`task.name`, `task.description`, `run.generated_code_path`), TaskUpdate missing required fields, return type mismatches.
- **batches.py:** 17 errors -- None-safety on `Task | None` and `Batch | None` from repository methods, attribute access without None guards.
- **reports.py:** 7 errors -- `dict[str, Any]` has no attribute errors in assertion result transformation (accessing `.id`, `.run_id` etc. on dict items).

**Notable:** The mypy errors reveal a systematic pattern: route handlers access ORM relationship attributes without None checks. For example, `run.task.name` where `task` could be None (lazy-loaded relationship). These are latent runtime AttributeError risks.

## Risk Priority Matrix

| Priority | File | Lines | Risk Justification |
|----------|------|-------|--------------------|
| P1 | main.py | 160 | CORS `*`, DEBUG stack traces always enabled, no auth middleware, global exception handler leaks stack traces |
| P1 | run_pipeline.py | 577 | 6-stage orchestrator API layer (business logic reviewed in Phase 125); 5 unused imports; SSE event publishing; context mutation at line 325 |
| P1 | runs_routes.py | 367 | subprocess.run for pytest execution; FileResponse without path validation on screenshots; SSE stream endpoint; code execution endpoint missing path re-validation |
| P1 | batches.py | 140 | Fire-and-forget asyncio.create_task without error callback; None-safety on ORM relationships (17 mypy errors) |
| P1 | external_assertions.py | 211 | Executes external assertion methods (code execution surface); user-controlled class_name/method_name flow to execution engine |
| P1 | external_data_methods.py | 101 | Executes external data methods (code execution surface); user-controlled class_name/method_name with params dict |
| P1 | external_operations.py | 88 | Generates precondition code from external modules; WEBSERP_PATH re-check after require_external_available() |
| P2 | tasks.py | 160 | File upload with validation; Excel import with atomic transaction; return type mismatches (2 mypy errors) |
| P2 | reports.py | 127 | Report retrieval with FileResponse; dict-to-object type confusion in assertion results (7 mypy errors) |
| P2 | runs.py | 14 | Backward-compat re-exports only (router + run_agent_background) |
| P3 | dashboard.py | 97 | Read-only aggregation queries; no user input; no file responses |
| P3 | response.py | 85 | Unused response helpers (success_response, error_response never called); ErrorCodes class never used; 3 mypy errors |
| P3 | routes/__init__.py | 5 | Minimal re-exports of tasks and runs only; main.py imports 8 modules directly |

## Security Check Matrix

| Check | main | run_pipeline | runs_routes | batches | external_assert | external_data | external_ops | tasks | reports | dashboard |
|-------|------|-------------|-------------|---------|----------------|--------------|-------------|-------|---------|-----------|
| **Param validation** | None (no params) | N/A (no HTTP endpoints) | `task_id: str` no format constraints; `run_id: str` no format constraints; `step_index: int` OK | `batch_id: str` no format constraints | `class_name: str` no format; `method_name: str` no format; `api_params: dict` no schema | `class_name: str` no format; `method_name: str` no format; `params: dict` no schema | `operation_codes: list[str]` no format | `task_id: str` no format; file upload validated (extension + size) | `report_id: str` no format; pagination validated via Query constraints | None (no params) |
| **Error handling** | Global handlers OK; print() in lifespan (lines 51,55,62,65) | try/except on agent execution; non_blocking_execute on code gen | try/except on code execution; silent_execute on cleanup; error on subprocess | **Fire-and-forget** (line 68); no done_callback; no error propagation | require_external_available raises 503; try/except delegated to execution engine | require_external_available raises 503; try/except delegated to execution engine | require_external_available raises 503; WEBSERP_PATH re-check | try/except on Excel parse; atomic transaction with rollback | HTTPException on missing report; nested import inside handler | None needed |
| **Path traversal** | N/A | N/A | **Screenshot FileResponse** (line 364) -- no path validation; Report FileResponse (line 263) -- derived from code_path, no validation; Code view (line 240) -- **has** `_validate_code_path()`; Code execute (line 302) -- **missing** `_validate_code_path()` | N/A | N/A | N/A | N/A | N/A | Report derived path (line 259) -- parent of validated code path, OK | N/A |
| **CORS/Auth gap** | `allow_origins=["*"]` | No auth | No auth | No auth | No auth | No auth | No auth | No auth | No auth | No auth |
| **Code execution surface** | N/A | Agent execution pipeline; code generation | **subprocess.run** for pytest (line 108); background task for code execution | asyncio.create_task for batch execution | External assertion method execution via execute_assertion_method | External data method execution via execute_data_method | Code generation from external modules | N/A | N/A | N/A |
| **SSRF risk** | N/A | `target_url` parameter flows to browser navigation | N/A | N/A | `api_params` dict passed to HTTP requests in external assertions | `params` dict passed to data methods | N/A | N/A | N/A | N/A |
| **Credential exposure** | N/A | `login_config` dict with plaintext account/password (line 556-560) | `_build_login_credentials()` returns plaintext dict (line 76-80); credentials written to conftest.py (line 85) | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **SSE stream errors** | N/A | event_manager.publish() -- no error handling on publish failure; None sentinel in finally (line 575) | **event_generator** (line 321-325) -- no try/except/finally; no cleanup on client disconnect | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## CONCERNS.md Verification

| CONCERNS.md Entry | Status | Current Impact (Single-User/Internal) | Public Internet Impact | Finding Reference |
|-------------------|--------|---------------------------------------|------------------------|-------------------|
| **CORS allows all origins** (main.py:77-83) | Confirmed | Low -- internal network only, no cross-origin attack vector | **Critical** -- any website can make API requests; combined with no auth = full API exposure; CSRF/XSS vector for browser-based attacks | API-SEC-01 |
| **No authentication/authorization** (all routes) | Confirmed | Low -- single user on internal network | **Critical** -- all 20+ endpoints fully exposed; anyone can create tasks, execute code (subprocess), read reports, trigger batch execution | API-SEC-02 |
| **Stack traces exposed in production** (main.py:132-149) | Confirmed | Low -- only visible to the single user hitting error endpoints | **High** -- stack traces reveal internal code structure, file paths, variable names; aids attackers in crafting targeted exploits; DEBUG level hardcoded at line 44 so stack traces are ALWAYS included | API-SEC-03 |
| **Credentials in generated test files** (code_generator.py) | Confirmed | Low -- generated files in outputs/ with path validation | **Medium** -- credentials stored on disk in plaintext; accessible via code viewer API endpoint; could be read if server file system is compromised | Phase 125 Ref: P1 code_generator.py:198-201 |
| **LLM API keys logged partially** (auth_service.py:85) | Noted | Low -- only in server logs | **Medium** -- first 20 chars of token logged; combined with knowledge of token format could aid reconstruction | Out of API layer scope |
| **exec() for user code** (precondition_service.py) | Noted | Low -- single user | **Critical** -- arbitrary code execution on server; file system access, network calls, process spawning | Out of API layer scope; Phase 125 Ref: P2 precondition_service.py:243 |

## Quick-Scan Findings (P3 Files)

### [P3] dashboard.py -- Read-only aggregation, no significant issues
- **Severity:** Low
- **Category:** Architecture
- **Description:** Dashboard endpoint performs 5 SQL queries (stats + 7-day trend + recent runs). No user-controlled input flows into queries. The `datetime.now()` usage means results are timezone-dependent (server local time). No pagination on recent_runs (hardcoded limit 5). All queries are read-only with no mutation.
- **Recommendation:** Consider using timezone-aware `datetime.utcnow()` or `datetime.now(timezone.utc)` for consistency. The hardcoded limit 5 is acceptable for dashboard context.

### [P3] response.py -- Unused response helpers and ErrorCodes
- **Severity:** Low
- **Category:** Architecture
- **Description:** `success_response()`, `error_response()`, and `ErrorCodes` are never used by any route file. Routes return Pydantic models directly (success) or rely on global exception handlers (errors). The documented API format `{"success": true, "data": {...}}` is only enforced on error responses. The 3 mypy errors are from implicit Optional on function parameters (meta=None, request_id=None, stack=None).
- **Recommendation:** Either remove the unused code or adopt the standard response wrapper across all routes. Current inconsistency means the frontend handles two different response structures.

### [P3] routes/__init__.py -- Incomplete exports
- **Severity:** Low
- **Category:** Architecture
- **Description:** `__init__.py` only imports `tasks` and `runs`, but `main.py` imports 8 route modules directly (tasks, runs, reports, dashboard, external_operations, external_data_methods, external_assertions, batches). The `__init__.py` is not used for route registration.
- **Recommendation:** Either update `__init__.py` to export all 8 route modules (for discoverability) or document that main.py is the sole registration point.

### [P3] runs.py -- Clean backward-compatible re-exports
- **Severity:** N/A
- **Category:** Architecture
- **Description:** 14-line file with clean re-exports of `router` from runs_routes.py and `run_agent_background` from run_pipeline.py. Uses `noqa: F401` appropriately. No issues.
- **Recommendation:** None needed.

## API-Layer Specific Findings

### [API-01] runs_routes.py:302 -- Code execution endpoint does not re-validate file path
- **Severity:** High
- **Category:** Security
- **Description:** The `execute_run_code` endpoint at line 299-305 passes `run.generated_code_path` directly to `_execute_code_background` which runs `subprocess.run(["uv", "run", "pytest", test_file_path, ...])` at line 108. Unlike the `get_run_code` endpoint (line 240) which calls `_validate_code_path()` before serving the file, the execution endpoint does NOT validate the path. If `generated_code_path` was tampered with in the database (via SQLite direct access or a SQL injection in a different context), arbitrary commands could be executed through pytest.
- **Current Impact:** Low -- requires database write access which is unlikely given internal single-user deployment.
- **Public Internet Impact:** Critical -- combined with no authentication, any user could modify the database to point to an arbitrary Python file.
- **Recommendation:** Add `_validate_code_path(run.generated_code_path)` in the execute_run_code endpoint before launching the background task. This is a one-line fix that provides defense-in-depth.
- **RESEARCH Reference:** Pitfall 6 (subprocess.run with user-influenced paths)

### [API-02] runs_routes.py:364 -- Screenshot FileResponse has no path validation
- **Severity:** Medium
- **Category:** Security
- **Description:** The `get_screenshot` endpoint at line 351-366 returns `FileResponse(step.screenshot_path)` where `screenshot_path` comes from the database. Unlike `get_run_code` which validates the path via `_validate_code_path()`, the screenshot endpoint performs no path validation. If an attacker could write arbitrary paths to the `screenshot_path` column, they could read any file on the server via this endpoint.
- **Current Impact:** Low -- screenshot paths are written by the agent service, not user-controlled.
- **Public Internet Impact:** High -- potential arbitrary file read if database can be manipulated.
- **Recommendation:** Add path validation: ensure `step.screenshot_path` resolves within the expected outputs/screenshots directory. Apply the same `resolve() + startswith()` pattern as `_validate_code_path()`.
- **RESEARCH Reference:** Pitfall 4 (File path exposure in screenshot/report endpoints)

### [API-03] runs_routes.py:321-325 -- SSE stream endpoint has no try/except/finally
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `event_generator` async generator at lines 321-325 iterates `event_manager.subscribe(run_id)` with no error handling. If the subscribe generator raises an exception, the StreamingResponse may not properly close the connection. The EventManager.subscribe() method at lines 87-116 has its own try/finally that cleans up subscriber queues, but if the exception occurs in the yield statement (client disconnect during send), the finally block in EventManager handles it. However, if the exception occurs in event_generator itself (not in subscribe), there is no cleanup.
- **Current Impact:** Low -- SSE connections are short-lived in practice.
- **Public Internet Impact:** Medium -- malicious clients could trigger rapid connect/disconnect cycles, potentially leaking event queues if the finally block in EventManager doesn't execute.
- **Recommendation:** Wrap the event_generator body in try/except/finally:
  ```python
  async def event_generator() -> AsyncGenerator[str, None]:
      try:
          async for event in event_manager.subscribe(run_id):
              if event is None:
                  break
              yield event
      except Exception:
          pass  # Client disconnect or subscribe error
  ```
- **RESEARCH Reference:** Pitfall 3 (SSE stream error handling gaps)

### [API-04] batches.py:68 -- Fire-and-forget asyncio.create_task with no error callback
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Line 68 creates `asyncio.create_task(service.start(run_configs))` with no `add_done_callback()`. If `service.start()` raises immediately (before the first await), the exception is silently swallowed until the task is garbage collected, which triggers a "Task exception was never retrieved" warning. The batch appears "created" in the response but may have already failed internally. The BatchExecutionService internally uses `asyncio.gather(return_exceptions=True)` which catches per-task errors, but the outer `service.start()` itself could fail before reaching gather.
- **Current Impact:** Low -- batch creation rarely fails in practice.
- **Public Internet Impact:** Medium -- rapid batch creation with invalid configs could trigger silent failures with no user feedback.
- **Recommendation:** Add a done callback for error logging:
  ```python
  task = asyncio.create_task(service.start(run_configs))
  task.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)
  ```
- **RESEARCH Reference:** Pitfall 5 (fire-and-forget with no error propagation)

### [API-05] main.py:44 -- Hardcoded DEBUG logging enables stack traces in all error responses
- **Severity:** Medium
- **Category:** Security
- **Description:** The lifespan function at line 44 sets `logging.basicConfig(level=logging.DEBUG)`. The general exception handler at line 146 checks `logging.getLogger().level == logging.DEBUG` to decide whether to include stack traces. Since DEBUG is hardcoded, stack traces are ALWAYS included in 500 error responses. The LOG_LEVEL setting from `.env` is never used to control this behavior.
- **Current Impact:** Low -- only the single user sees error responses.
- **Public Internet Impact:** High -- stack traces reveal internal code structure, file paths, and variable names.
- **Recommendation:** Use the LOG_LEVEL from settings to control DEBUG level:
  ```python
  log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
  logging.basicConfig(level=log_level, format='...')
  ```
- **CONCERNS.md Reference:** Confirmed -- "Stack traces exposed in production"

### [API-06] Path parameter validation gaps across all route files
- **Severity:** Low
- **Category:** Correctness
- **Description:** All path parameters (`task_id`, `run_id`, `batch_id`, `report_id`, `step_index`) are bare `str` or `int` with no Pydantic Field constraints. IDs are expected to be 8-character hex strings (from `uuid4().hex[:8]`), but no validation enforces this format. Parameters accept arbitrary-length strings, SQL-like content (no SQL injection risk with ORM, but unexpected behavior), or empty strings.
- **Current Impact:** Low -- incorrect IDs result in 404 responses.
- **Public Internet Impact:** Medium -- lack of input validation allows malformed requests to reach the database layer; could be used for probing.
- **Recommendation:** Add Field constraints to path parameters where feasible:
  ```python
  async def get_task(task_id: str = Path(..., min_length=8, max_length=8, pattern="^[a-f0-9]+$"))
  ```
  Note: FastAPI path parameters require the `Path()` annotation for constraints.
- **RESEARCH Reference:** Pitfall 2 (Missing Pydantic Field Constraints on Path Parameters)

### [API-07] run_pipeline.py:325 -- Context mutation leaks external_assertion_summary into variable_map
- **Severity:** Medium
- **Category:** Correctness
- **Description:** At line 325, `_run_external_assertions` mutates the `context` dict by setting `context['external_assertion_summary'] = summary`. The variable_map filter at line 546 uses `not k.startswith("assertion")` which does NOT catch keys starting with "external_assertion" (they start with "external_", not "assertion"). The key `external_assertion_summary` would pass the filter as a dict value (filtered by `isinstance(v, (str, int, float))`), but if the summary format changes to a string, it would leak into generated test code as a variable substitution.
- **Current Impact:** Low -- summary is a dict, filtered by isinstance guard.
- **Public Internet Impact:** N/A (internal correctness issue).
- **Recommendation:** Change the filter at line 546 to `not k.startswith(("assertion", "external_assertion"))` for defense-in-depth. Also consider not mutating the shared context dict -- use a separate dict for external assertion metadata.
- **Phase 125 Reference:** Cross-4 and P1 finding for same issue

### [API-08] Response format inconsistency across routes
- **Severity:** Low
- **Category:** Architecture
- **Description:** Routes use three different response patterns: (1) Pydantic response_model (tasks, runs, batches, external_*), (2) plain dict (dashboard, import endpoints, delete endpoints), (3) FileResponse/StreamingResponse/PlainTextResponse (reports, screenshots, code, SSE). None of these wrap the response in the documented `{"success": true, "data": {...}}` format. Error responses DO use the standard format via global exception handlers. The `success_response()` and `error_response()` helpers in response.py are completely unused.
- **Current Impact:** Low -- frontend handles both formats.
- **Public Internet Impact:** Low -- API consumers must handle inconsistent response structures.
- **Recommendation:** Decide on one approach: either (a) use response_model consistently and document that success responses are unwrapped, or (b) adopt the standard wrapper. Current state is confusing for new developers.
- **RESEARCH Reference:** Open Question 1 (Response format standardization)

### [API-09] external_* routes -- User-controlled identifiers flow to execution engine
- **Severity:** Medium
- **Category:** Security
- **Description:** The `external_assertions.py` execute endpoint accepts `class_name` and `method_name` as bare strings (no format validation) and passes them to `execute_assertion_method()`. Similarly, `external_data_methods.py` accepts `class_name`, `method_name`, and `params` dict. These flow to the external execution engine which uses them to look up and call methods via `globals()[class_name]` and `getattr(class_instance, method_name)`. While the external module is loaded from a trusted path, the class_name and method_name are effectively used as `globals()` keys and attribute names without sanitization.
- **Current Impact:** Low -- external module methods are well-defined and lookup failure produces a safe error.
- **Public Internet Impact:** Medium -- combined with no auth, an attacker could probe for available classes/methods and call arbitrary methods on the external module.
- **Recommendation:** Validate class_name and method_name against the discovered method registry (which `require_external_available()` ensures is loaded). Reject unknown class/method combinations at the route level before reaching the execution engine.

### [API-10] tasks.py:123,149 -- Return type mismatches (mypy errors)
- **Severity:** Low
- **Category:** Correctness
- **Description:** `create_task` returns the result of `repo.create(data)` which is an ORM `Task` object, but the function signature declares return type `TaskResponse`. Similarly `update_task` returns `updated` which is `Task | None`. FastAPI's response_model parameter handles the conversion at runtime, but the type annotations are misleading for mypy and static analysis.
- **Current Impact:** None -- FastAPI's response_model serialization handles the conversion.
- **Public Internet Impact:** None.
- **Recommendation:** Either wrap the return in `TaskResponse.model_validate(result)` or change the return type annotation to `Task` (letting response_model handle serialization).

### [API-11] runs_routes.py:259 -- Report FileResponse path derived from generated_code_path without validation
- **Severity:** Low
- **Category:** Security
- **Description:** The `get_run_report` endpoint at line 259 computes `report_path = Path(run.generated_code_path).parent / "report.html"`. The `generated_code_path` is not validated with `_validate_code_path()` (unlike `get_run_code`). The `report_path.exists()` check at line 260 prevents serving non-existent files, but there is no validation that the path is within the outputs/ directory. However, since the path is derived from the parent of `generated_code_path` (which itself is set by the code generation function at run_pipeline.py:374), the risk is mitigated -- the path is always `outputs/{run_id}/generated/report.html`.
- **Current Impact:** None -- generated_code_path is set by internal code.
- **Public Internet Impact:** Low -- if generated_code_path is tampered, the parent directory traversal is limited.
- **Recommendation:** Add `_validate_code_path()` check for consistency with `get_run_code`.

### [API-12] main.py:51,55,62,65 -- print() statements in lifespan
- **Severity:** Low
- **Category:** Architecture
- **Description:** The lifespan function uses `print()` for startup messages instead of the project's structured logger. Four print statements at lines 51, 55, 62, and 65. These bypass the logging system and appear on stdout regardless of log level configuration.
- **Current Impact:** None -- startup messages are useful.
- **Public Internet Impact:** Low -- print output may not be captured by log aggregation systems.
- **Recommendation:** Replace `print()` with `logger.info()` using the structured logger. Use `logging.getLogger(__name__)` which is the project convention.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total files reviewed | 13 API files + 2 supporting files |
| Total lines scanned | ~2,114 (API files) + 155 (supporting) |
| ruff issues | 17 (5 fixable, 12 intentional E402) |
| mypy errors (API files) | 58 |
| P1 files (deep-dive needed) | 7 |
| P2 files (moderate concern) | 3 |
| P3 files (quick scan) | 3 |
| API-layer findings | 12 |
| Critical issues | 0 |
| High issues | 1 |
| Medium issues | 6 |
| Low issues | 5 |

## Files Requiring No Further Review

The following P3 files had no significant findings and do not need deep-dive:
- runs.py -- clean re-exports, no logic

## Top 5 API-Layer Findings (by severity + impact)

1. **[API-01] runs_routes.py:302 -- Code execution endpoint missing path validation.** The execute_run_code endpoint passes `run.generated_code_path` to subprocess.run without re-validating with `_validate_code_path()`. If the database path is tampered, arbitrary code execution is possible. (High/Security)

2. **[API-04] batches.py:68 -- Fire-and-forget asyncio.create_task with no error callback.** Batch execution is launched with no done callback, meaning startup failures are silently swallowed. (Medium/Correctness)

3. **[API-02] runs_routes.py:364 -- Screenshot FileResponse has no path validation.** Database-sourced path served as FileResponse without directory bounds checking. (Medium/Security)

4. **[API-05] main.py:44 -- Hardcoded DEBUG enables stack traces in all error responses.** The LOG_LEVEL setting is ignored; all 500 errors include full stack traces. (Medium/Security)

5. **[API-09] external_* routes -- User-controlled identifiers flow to execution engine without validation.** class_name and method_name are bare strings passed to globals() lookup and getattr() calls. (Medium/Security)

## Confirmed CONCERNS.md Issues

| CONCERNS.md Entry | Status | API-Layer Finding Reference |
|-------------------|--------|---------------------------|
| CORS allows all origins | Confirmed | API-SEC-01 (main.py:77-83) |
| No authentication/authorization | Confirmed | API-SEC-02 (all routes) |
| Stack traces exposed in production | Confirmed | API-SEC-03 + API-05 (main.py:44,132-149) |
| Credentials in generated test files | Referenced from Phase 125 | Phase 125 P1 code_generator.py:198-201 |
| LLM API keys logged partially | Noted (out of API scope) | auth_service.py:85 |
| exec() for user code | Noted (out of API scope) | precondition_service.py:243 |

## New Issues Not in CONCERNS.md

1. **Code execution path validation gap** (High) -- execute_run_code does not validate file path before subprocess.run
2. **Screenshot FileResponse path traversal** (Medium) -- no validation on database-sourced screenshot paths
3. **SSE stream error handling** (Medium) -- event_generator has no try/except/finally
4. **Fire-and-forget batch execution** (Medium) -- no error callback on asyncio.create_task
5. **External route identifier validation** (Medium) -- class_name/method_name flow to globals() lookup
6. **Response format inconsistency** (Low) -- three different response patterns across routes
7. **Path parameter validation gaps** (Low) -- all IDs are bare str with no format constraints
8. **print() in lifespan** (Low) -- uses print instead of structured logger

## Deep-Dive Findings (P1 Files)

*Deep-dive completed: 2026-05-03*
*Scope: main.py, runs_routes.py, run_pipeline.py (API layer only)*

### main.py (160 lines)

#### [DD-main-01] CORS `allow_origins=["*"]` combined with `allow_credentials=True` is a browser-blocked combination
- **Severity:** Medium
- **Category:** Security
- **Description:** main.py:77-83 configures `allow_origins=["*"]` with `allow_credentials=True`. Per CORS specification (RFC 6454 + Fetch spec), browsers reject credentialed requests (with cookies/Authorization header) when the origin is wildcard. The browser blocks the response, meaning the frontend cannot send cookies or auth headers. This combination is either (a) silently ignored by the browser (no credentials sent) or (b) causes CORS errors if the frontend tries to send credentials. Since the API has no authentication, `allow_credentials=True` is currently harmless but misleading -- it suggests the API supports cookie-based auth, which it does not.
- **Recommendation:** Either (a) set `allow_credentials=False` since no auth mechanism exists, or (b) restrict `allow_origins` to the actual frontend origin URL and keep `allow_credentials=True` for future auth support.
- **RESEARCH Reference:** Pitfall 1 (Response format inconsistency -- related CORS concern)
- **CONCERNS.md Reference:** Confirmed -- "CORS allows all origins"

#### [DD-main-02] Global DEBUG logging hardcoded at lifespan, ignoring LOG_LEVEL setting
- **Severity:** Medium
- **Category:** Security
- **Description:** main.py:44 calls `logging.basicConfig(level=logging.DEBUG)` unconditionally. The `LOG_LEVEL` setting from `settings.py` (default "INFO") is never consulted for the root logger. This causes: (1) all loggers output at DEBUG level including verbose httpx, SQLAlchemy, and browser_use internals; (2) the general exception handler at line 146 checks `logging.getLogger().level == logging.DEBUG` to decide whether to include stack traces -- since DEBUG is always active, stack traces are ALWAYS included in 500 responses. The `settings.log_level` field exists but is unused by the root logger configuration.
- **Recommendation:** Use settings to control log level: `logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))`. Add a separate boolean `DEBUG` or `INCLUDE_STACK_TRACES` setting for controlling stack trace inclusion, independent of log verbosity.
- **RESEARCH Reference:** Pitfall 7 (Global DEBUG Logging Exposes Stack Traces)

#### [DD-main-03] browser_use and cdp_use DEBUG logging forces verbose output regardless of root level
- **Severity:** Low
- **Category:** Performance
- **Description:** main.py:49-50 sets `logging.getLogger('browser_use').setLevel(logging.DEBUG)` and `logging.getLogger('cdp_use').setLevel(logging.DEBUG)` independently. Even if the root logger level is fixed (finding DD-main-02), these two loggers will always output DEBUG messages. During agent execution, these loggers produce extensive output (CDP protocol messages, DOM serialization details, browser navigation events), which can reach several MB per run. This slows I/O and fills disk if log output is redirected to files.
- **Recommendation:** Make browser_use/cdp_use log levels configurable via settings. Default to INFO or WARNING in production.

#### [DD-main-04] RequestValidationError handler returns 400 instead of FastAPI default 422
- **Severity:** Low
- **Category:** Architecture
- **Description:** main.py:119 returns `status_code=400` for validation errors instead of FastAPI's default 422. While 400 is arguably more correct (the request is malformed), this deviates from FastAPI convention. Existing API consumers that check for 422 validation errors will not catch these. The response format does include the Pydantic error details in `error.details` which is helpful for debugging.
- **Recommendation:** Document this deviation from FastAPI convention. If frontend code checks for 422 status for validation errors, update to check 400 instead. Current state is consistent within the codebase.

#### [DD-main-05] General exception handler includes full stack trace via traceback.format_exc() at DEBUG
- **Severity:** Medium
- **Category:** Security
- **Description:** main.py:146 calls `traceback.format_exc()` which returns the full stack trace as a string. Combined with DD-main-02 (DEBUG always active), every 500 error response includes the complete stack trace including: Python file paths on the server, local variable names, line numbers, and the full exception chain. The `request_id` field is a UUID that provides no traceability back to server logs (there is no request ID middleware to correlate). The stack trace is returned in the JSON response body, visible to any API consumer.
- **Current Impact:** Low -- only the single internal user sees error responses.
- **Public Internet Impact:** High -- stack traces reveal internal code structure, absolute file paths (including username in path), and variable names. This aids attackers in understanding the codebase and crafting targeted attacks.
- **Recommendation:** Never include stack traces in API responses in production. Add a `DEBUG` boolean setting that controls this behavior. Log the stack trace server-side (already done at line 137 with `exc_info=True`) and return only the `request_id` for correlation.
- **RESEARCH Reference:** Pitfall 7 (Global DEBUG Logging Exposes Stack Traces)

#### [DD-main-06] print() statements in lifespan bypass structured logging
- **Severity:** Low
- **Category:** Architecture
- **Description:** main.py:51,55,60,62,65 uses `print()` for startup messages instead of the project's structured logger. These bypass the logging system: they are not captured by log handlers, not filtered by log level, and appear on stdout regardless of configuration. The print at line 60 leaks the WEBSERP_PATH value (`f"Validating WEBSERP_PATH: {settings.weberp_path}"`) to stdout -- this is a file system path that could reveal server directory structure.
- **Recommendation:** Replace all `print()` calls with `logger.info()` using `logging.getLogger(__name__)`. This is the project convention per CLAUDE.md.
- **RESEARCH Reference:** Already noted in breadth scan as API-12.

#### [DD-main-07] lifespan does not handle database initialization failure gracefully
- **Severity:** Medium
- **Category:** Correctness
- **Description:** main.py:54 calls `await init_db()` without try/except. If init_db fails (e.g., SQLite file is corrupted, permissions error, disk full), the exception propagates up to the ASGI server which logs a generic startup error and the application fails to start. The user sees a raw exception traceback, not a helpful message. The `init_db()` function performs ALTER TABLE operations that can fail if the database schema is in an inconsistent state.
- **Recommendation:** Wrap `await init_db()` in try/except with a clear error message: "Database initialization failed: {e}. Check database file permissions and integrity."
- **RESEARCH Reference:** None (not in RESEARCH pitfalls)

#### [DD-main-08] No authentication or authorization middleware on any endpoint
- **Severity:** Medium (current) / Critical (public internet)
- **Category:** Security
- **Description:** main.py registers 8 route modules (lines 85-92) with no authentication middleware. All 20+ endpoints are unauthenticated. Combined with CORS `allow_origins=["*"]` (DD-main-01), the full API surface is accessible from any origin. Sensitive endpoints include: `POST /api/runs` (triggers agent execution), `POST /api/runs/{run_id}/execute-code` (runs subprocess), `POST /api/batches` (triggers batch execution), and all external_* routes (execute external code).
- **Current Impact:** Low -- internal single-user deployment, network access is trusted.
- **Public Internet Impact:** Critical -- anyone can trigger code execution, read reports with credentials, delete tasks, and execute arbitrary external assertion methods.
- **Recommendation:** Add at minimum an API key middleware: `X-API-Key` header check for all non-GET endpoints. For production, use session-based or JWT authentication.
- **CONCERNS.md Reference:** Confirmed -- "No authentication or authorization"

### runs_routes.py (367 lines)

#### [DD-runs-01] POST /api/runs -- create_run endpoint has no parameter validation on task_id
- **Severity:** Low
- **Category:** Correctness
- **Description:** runs_routes.py:183 accepts `task_id: str` as a bare string with no Field constraints. Expected format is 8-char hex (from `uuid4().hex[:8]`), but any string is accepted. If an empty string is passed, `task_repo.get("")` returns None and `raise_not_found("Task", "")` is called, producing a confusing "Task  not found" message (double space). If an extremely long string is passed, it flows directly into the database query. While SQLAlchemy parameterizes queries (no SQL injection risk), the unbounded string could cause unexpected behavior in log messages and SSE events.
- **Recommendation:** Add `task_id: str = Path(..., min_length=1, max_length=32, pattern="^[a-f0-9]+$")` or validate format in the handler before the DB lookup.
- **RESEARCH Reference:** Pitfall 2 (Missing Pydantic Field Constraints on Path Parameters)

#### [DD-runs-02] POST /api/runs -- create_run returns raw ORM Run object, not RunResponse
- **Severity:** Low
- **Category:** Architecture
- **Description:** runs_routes.py:212 returns `run` which is an ORM `Run` object from `run_repo.create()`. The endpoint declares `response_model=RunResponse`, so FastAPI serializes the ORM object using `RunResponse.model_validate(run)`. However, the `Run` ORM model may not populate all `RunResponse` fields (e.g., `task_name`, `steps_count` are computed fields). The ORM `run` has `task_id` set but no eager-loaded `task` relationship, so `task_name` will be None in the response. This means the created run response lacks the task name, requiring a separate GET to populate it.
- **Recommendation:** Either (a) return `RunResponse` explicitly constructed with the needed fields, or (b) call `run_repo.get_with_task(run.id)` to eagerly load the relationship. Current behavior is correct but the response is incomplete.
- **RESEARCH Reference:** Pitfall 1 (Response format inconsistency)

#### [DD-runs-03] POST /api/runs -- create_run triggers agent execution via BackgroundTasks with no error propagation
- **Severity:** Medium
- **Category:** Correctness
- **Description:** runs_routes.py:199 uses `background_tasks.add_task(run_agent_background, ...)` which is FastAPI's BackgroundTasks mechanism. If `run_agent_background` raises an exception, FastAPI catches it and logs a warning, but the HTTP response (201 Created) has already been sent. The run is in "pending" status and will remain so if the background task fails before reaching `update_status(run_id, "running")` at run_pipeline.py:510. The user sees a "created" response but the run never starts.
- **Current Impact:** Low -- background task failures are rare.
- **Public Internet Impact:** Medium -- concurrent task creation could overwhelm resources, causing background tasks to fail silently.
- **Recommendation:** Consider updating run status to "queued" immediately in the handler, and let the background task set "running" when it starts. Add a health check endpoint that detects "pending" runs older than a threshold (stuck runs).
- **RESEARCH Reference:** Pitfall 5 (fire-and-forget with no error propagation)

#### [DD-runs-04] GET /api/runs/{run_id}/stream -- SSE event_generator has no try/except/finally
- **Severity:** Medium
- **Category:** Correctness
- **Description:** runs_routes.py:321-325 defines `event_generator()` as an async generator with no error handling. The generator iterates `event_manager.subscribe(run_id)` and yields events. Three failure modes exist:
  1. **Client disconnect during yield:** The `yield` raises `asyncio.CancelledError` or a broken pipe. Without a try/except, this propagates to `event_manager.subscribe()`'s finally block (which does handle cleanup at event_manager.py:102-116).
  2. **Exception in subscribe generator:** If `event_manager.subscribe()` raises, the generator exits without cleanup.
  3. **None sentinel:** The `if event is None: break` correctly handles the termination signal.
  The EventManager.subscribe() method at event_manager.py:87-116 does have its own try/finally that cleans up subscriber queues and heartbeat tasks. So the primary concern is client disconnect during yield -- which Starlette's StreamingResponse handles by cancelling the async generator, triggering cleanup in EventManager.subscribe's finally block. This is actually correct behavior but is fragile -- it depends on EventManager's implementation details.
- **Recommendation:** Add a defensive try/except/finally wrapper for robustness:
  ```python
  async def event_generator() -> AsyncGenerator[str, None]:
      try:
          async for event in event_manager.subscribe(run_id):
              if event is None:
                  break
              yield event
      except (asyncio.CancelledError, GeneratorExit):
          pass  # Client disconnect, EventManager cleans up
      except Exception:
          pass  # Subscribe error, don't crash the response handler
  ```
- **RESEARCH Reference:** Pitfall 3 (SSE Stream Error Handling Gaps)

#### [DD-runs-05] GET /api/runs/{run_id}/screenshots/{step_index} -- FileResponse with unvalidated database path
- **Severity:** Medium
- **Category:** Security
- **Description:** runs_routes.py:363-364 returns `FileResponse(step.screenshot_path)` where `step.screenshot_path` comes from the `steps` table in SQLite. There is no path validation -- `_validate_code_path()` (the good pattern at line 44-52) is NOT called. If the `screenshot_path` column contained an arbitrary path (via direct DB manipulation or a future bug), this endpoint would serve any file on the server filesystem. The path is set by `agent_service.save_screenshot()` which constructs it safely (`outputs/{run_id}/screenshots/step_N.png`), but the route does not verify this.
- **Current Impact:** Low -- screenshot paths are written by internal code only.
- **Public Internet Impact:** High -- if combined with a separate vulnerability that allows DB writes, this becomes an arbitrary file read.
- **Recommendation:** Add path validation before FileResponse:
  ```python
  screenshot_root = Path("outputs").resolve()
  resolved = Path(step.screenshot_path).resolve()
  if not str(resolved).startswith(str(screenshot_root)):
      raise HTTPException(status_code=403, detail="illegal file path")
  ```
- **RESEARCH Reference:** Pitfall 4 (File path exposure in screenshot/report endpoints)

#### [DD-runs-06] POST /api/runs/{run_id}/execute-code -- Missing _validate_code_path before subprocess.run
- **Severity:** High
- **Category:** Security
- **Description:** runs_routes.py:299-305 passes `run.generated_code_path` directly to `_execute_code_background` via `background_tasks.add_task()`. Inside `_execute_code_background` at line 108, `subprocess.run(["uv", "run", "pytest", test_file_path, ...])` executes the file. The `test_file_path` is never validated with `_validate_code_path()`. The `get_run_code` endpoint at line 240 correctly calls `_validate_code_path()` before serving the file, but the execute endpoint skips this validation. If `generated_code_path` is tampered in the database (via direct SQLite access), arbitrary Python files can be executed as pytest tests.
- **Current Impact:** Low -- requires direct database write access.
- **Public Internet Impact:** Critical -- combined with no authentication, any API consumer could manipulate the runs table to point to arbitrary Python files. The subprocess runs with the server's full process permissions.
- **Recommendation:** Add `_validate_code_path(run.generated_code_path)` at line 298 (after the pre-checks, before launching the background task):
  ```python
  _validate_code_path(run.generated_code_path)  # Add this line
  background_tasks.add_task(...)
  ```
- **RESEARCH Reference:** Pitfall 6 (subprocess.run with user-influenced paths)

#### [DD-runs-07] GET /api/runs/{run_id}/report -- Report FileResponse derived from generated_code_path without validation
- **Severity:** Low
- **Category:** Security
- **Description:** runs_routes.py:259 computes `report_path = Path(run.generated_code_path).parent / "report.html"`. The `generated_code_path` is not validated with `_validate_code_path()`. However, the derived path is always `report.html` in the parent directory of the code path. Since the code path is set by `_run_code_generation` at run_pipeline.py:370-374 (which constructs it as `outputs/{run_id}/generated/test_{run_id}.py`), the report path is always `outputs/{run_id}/generated/report.html`. The `report_path.exists()` check at line 260 prevents serving non-existent files. The risk is mitigated by the path derivation pattern, but for consistency with `get_run_code`, validation should be added.
- **Recommendation:** Add `_validate_code_path(run.generated_code_path)` before computing the report path, consistent with `get_run_code`.
- **RESEARCH Reference:** Pitfall 4 (File path exposure in screenshot/report endpoints)

#### [DD-runs-08] GET /api/runs -- list_runs returns all runs with no pagination
- **Severity:** Low
- **Category:** Performance
- **Description:** runs_routes.py:160-178 calls `run_repo.list_with_details()` which loads all runs with eager-loaded task and step relationships. There is no pagination (no page/page_size parameters). As the number of runs grows, this endpoint becomes increasingly slow. The response also iterates all runs to construct RunResponse objects with computed fields (task_name, steps_count).
- **Recommendation:** Add pagination parameters with reasonable defaults (e.g., `page: int = 1, page_size: int = 20`). ReportRepository already implements pagination; apply the same pattern.
- **RESEARCH Reference:** None (not in RESEARCH pitfalls)

#### [DD-runs-09] _build_login_credentials returns plaintext credentials dict that flows to conftest.py on disk
- **Severity:** Medium
- **Category:** Security
- **Description:** runs_routes.py:67-80 constructs a dict with `{"origin": ..., "account": ..., "password": ...}` where password is the actual ERP password in plaintext. This dict is used at line 104-105 to write `_write_test_support_files()` which creates a `conftest.py` on disk. The credentials are written as string literals into generated test code via code_generator.py (referenced in Phase 125 finding P1 code_generator.py:198-201). The credentials flow through: account_service -> _build_login_credentials -> _write_test_support_files -> conftest.py on disk. Additionally, `_build_login_credentials` is called at line 104 inside `_execute_code_background` which runs in a background task -- any exception during credential resolution would be caught by the outer try/except and logged, potentially including the credentials in log output.
- **Current Impact:** Low -- credentials are for the ERP system under test, not the platform itself. Generated files are in outputs/ with path validation.
- **Public Internet Impact:** Medium -- credentials stored in plaintext on disk in generated test files; accessible via code viewer API.
- **Recommendation:** Consider injecting credentials at test execution time via environment variables rather than embedding in generated files. At minimum, ensure the log output at line 128 does not include the credentials dict.
- **RESEARCH Reference:** Pitfall 8 (Credentials in API Responses)

#### [DD-runs-10] POST /api/runs/{run_id}/stop -- stop_run updates status but does not cancel the running agent
- **Severity:** Medium
- **Category:** Correctness
- **Description:** runs_routes.py:334-348 sets run status to "stopped" via `run_repo.update_status(run_id, "stopped")` but does NOT signal the running agent to actually stop. The background task (`run_agent_background` in run_pipeline.py) continues executing until the agent completes or times out. The status change in the database has no effect on the running agent -- there is no cancellation mechanism. The user sees "stopped" in the UI but the agent continues consuming resources (browser, LLM API calls) until it finishes naturally.
- **Recommendation:** Implement agent cancellation: store the asyncio.Task reference for each run_id and call `task.cancel()` when stop is requested. Alternatively, add a polling check in the agent loop that reads run status and stops when it sees "stopped".
- **RESEARCH Reference:** None (not in RESEARCH pitfalls)

#### [DD-runs-11] _execute_code_background uses subprocess.run synchronously in async context
- **Severity:** Medium
- **Category:** Performance
- **Description:** runs_routes.py:108 calls `subprocess.run()` which is a synchronous blocking call. This runs inside a FastAPI BackgroundTasks handler which executes in the main event loop. During the subprocess execution (up to 180 seconds timeout at line 111), the event loop is blocked. All other async handlers (SSE events, API requests, concurrent runs) are stalled. For a tool that supports batch execution, this means code execution of one run blocks the entire server.
- **Recommendation:** Use `asyncio.create_subprocess_exec()` instead of `subprocess.run()`:
  ```python
  proc = await asyncio.create_subprocess_exec(
      "uv", "run", "pytest", test_file_path, ...
      stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
  )
  stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=180)
  ```
- **RESEARCH Reference:** None (not in RESEARCH pitfalls)

#### [DD-runs-12] _validate_code_path uses startswith for path containment -- bypass possible with similar-named directories
- **Severity:** Low
- **Category:** Security
- **Description:** runs_routes.py:48 uses `str(resolved).startswith(str(outputs_root))` for path containment. This is a classic path traversal weakness: if `outputs_root` is `/app/outputs`, a path like `/app/outputs_secret/evil.py` would pass the check. The `resolve()` call eliminates `..` traversal, but the startswith check does not ensure the outputs_root is a complete path segment. In practice, the `outputs` directory name is unlikely to be a prefix of another real directory, so the risk is theoretical.
- **Recommendation:** Use path segment comparison: `resolved.parent == outputs_root or any(p == outputs_root for p in resolved.parents)`. Or check `resolved.relative_to(outputs_root)` which raises ValueError if not contained.
- **RESEARCH Reference:** None (not in RESEARCH pitfalls)

### run_pipeline.py (API Layer, 577 lines)

*Note: Per D-01, this section covers API-layer concerns only. Business logic findings from Phase 125 are not duplicated.*

#### [DD-pipe-01] SSE event publishing has no error handling -- publish failure silently drops events
- **Severity:** Low
- **Category:** Correctness
- **Description:** run_pipeline.py publishes SSE events via `await event_manager.publish(run_id, event_string)` at 12 different locations (lines 99, 109, 123, 219, 258, 267, 334, 420, 467, 512, 573, 575). None of these calls have try/except. If `event_manager.publish()` raises (e.g., queue full, memory error), the exception propagates up and could abort the entire pipeline. The `publish` method itself (event_manager.py:42-50) appends to a deque and iterates subscriber queues, which could raise if a subscriber's queue is in an unexpected state.
- **Recommendation:** Wrap critical publish calls in try/except so that event publishing failure does not abort the pipeline. Log the failure and continue execution:
  ```python
  try:
      await event_manager.publish(run_id, event_string)
  except Exception as e:
      logger.warning(f"[{run_id}] SSE publish failed: {e}")
  ```
- **RESEARCH Reference:** Pitfall 3 (SSE stream error handling)

#### [DD-pipe-02] None sentinel published in finally block always fires, even on successful completion
- **Severity:** Low
- **Category:** Correctness
- **Description:** run_pipeline.py:575 publishes `None` in the `finally` block. The EventManager.subscribe() generator breaks on `None` (runs_routes.py:323). This means the SSE stream always terminates when the pipeline finishes, regardless of success or failure. This is correct behavior for normal flows. However, if the client disconnects before the `finally` block executes, `event_manager.publish(run_id, None)` appends to subscriber queues that may no longer be consumed -- the None sentinel sits in the queue until the subscriber is cleaned up (by EventManager.subscribe's finally block). This is not a leak but a minor inconsistency.
- **Recommendation:** No action needed. The behavior is correct. Document that the None sentinel serves as the stream termination signal.
- **RESEARCH Reference:** Pitfall 3 (SSE stream error handling)

#### [DD-pipe-03] Precondition failure early return skips "started" SSE event -- frontend may miss the run start
- **Severity:** Medium
- **Category:** Correctness
- **Description:** run_pipeline.py:499-500 returns early when `_run_preconditions()` returns None. At this point, the "started" SSE event (published at line 512) has NOT been sent. The frontend receives "precondition" events followed directly by a "finished" event with status="failed", but never receives "started". The frontend RunMonitor component likely expects a "started" event to initialize the run display. Missing "started" could cause the UI to show the run in an incorrect state (still showing "pending" or not rendering the step timeline).
- **Recommendation:** Move the "started" event publication to before preconditions, or publish it immediately after creating the run:
  ```python
  # After line 486 (async with async_session()...)
  started = SSEStartedEvent(run_id=run_id, task_id=task_id, task_name=task_name)
  await event_manager.publish(run_id, f"event: started\ndata: {started.model_dump_json()}\n\n")
  ```
  Then move `await run_repo.update_status(run_id, "running")` to before preconditions as well.
- **RESEARCH Reference:** None (not in RESEARCH pitfalls; related to Phase 125 finding P1 run_pipeline.py:499-500)

#### [DD-pipe-04] Context mutation at line 325 leaks external_assertion_summary into variable_map
- **Severity:** Low
- **Category:** Correctness
- **Description:** run_pipeline.py:325 sets `context['external_assertion_summary'] = summary`. At line 543-547, context is used to build `_variable_map` for code generation. The filter `not k.startswith("assertion")` does NOT match keys starting with "external_assertion" (they start with "external_"). However, the `isinstance(v, (str, int, float))` guard at line 546 filters out dict values, so the summary (which is a dict) does not leak as a variable substitution. This is a latent gap that could surface if the summary format changes to a string.
- **Recommendation:** Change the filter to `not k.startswith(("assertion", "external_assertion"))` for defense-in-depth. This is already documented in breadth scan as API-07 and Phase 125 as Cross-4.
- **RESEARCH Reference:** Pitfall 2 (context mutation between pipeline stages)

#### [DD-pipe-05] 5 unused imports in pipeline orchestrator file
- **Severity:** Low
- **Category:** Architecture
- **Description:** run_pipeline.py:7 imports `asyncio`, line 14 imports `HTTPException`, line 19 imports `TaskRepository` and `StepRepository`, line 29 imports `TaskUpdate`. None of these are used in the file. These are leftovers from when pipeline code was part of the larger runs.py file (split per D-06). The unused imports clutter the import section and confuse readers about what the pipeline depends on.
- **Recommendation:** Remove all 5 unused imports. Verified by ruff F401 checks.
- **RESEARCH Reference:** Already noted in breadth scan ruff results and Phase 125.

#### [DD-pipe-06] _run_auth_and_session fallback writes plaintext credentials into task_description
- **Severity:** Medium
- **Category:** Security
- **Description:** run_pipeline.py:182-188 calls `flow._build_description()` with `account=account_info.account` and `password=account_info.password`. This embeds the ERP credentials directly into the task description string that is passed to the LLM agent. The credentials appear as text in the task description, which means: (1) the LLM receives plaintext credentials in its prompt, (2) the credentials may be logged at line 188 (`task_description[:150]...`), (3) the credentials flow through the agent's reasoning which may appear in SSE step events. This is the "text login fallback" path when programmatic login fails.
- **Current Impact:** Low -- the credentials are for the ERP under test, handled internally.
- **Public Internet Impact:** Medium -- credentials appear in LLM prompts (logged by DashScope?), in SSE events (visible to frontend), and in step reasoning text.
- **Recommendation:** Log the task description with credentials redacted at line 188: replace `task_description[:150]` with a redacted version. Consider whether the LLM provider logs prompt content.
- **RESEARCH Reference:** Pitfall 8 (Credentials in API Responses)

#### [DD-pipe-07] Login credentials logged at line 484
- **Severity:** Low
- **Category:** Security
- **Description:** run_pipeline.py:484 logs `f"[{run_id}] 登录角色: {login_role}, 账号: {account_info.account}"`. While the password is not logged, the account name is. Combined with the log level being DEBUG (DD-main-02), this information is always written to logs. For internal use this is acceptable but for production deployment, account names should not appear in logs.
- **Recommendation:** Redact or remove the account name from the log message: `f"[{run_id}] 登录角色: {login_role}"`.
- **RESEARCH Reference:** None

#### [DD-pipe-08] _run_code_generation uses non_blocking_execute but write_text is synchronous
- **Severity:** Low
- **Category:** Performance
- **Description:** run_pipeline.py:373 calls `_output_path.write_text(_content, encoding="utf-8")` synchronously inside `_generate()` which is passed to `non_blocking_execute`. The `non_blocking_execute` function runs the callable in a thread pool executor, so the synchronous write does not block the event loop. However, if the generated content is large (complex test with many steps), the write could take time. The non_blocking_execute wrapper correctly handles this.
- **Recommendation:** No action needed. The `non_blocking_execute` wrapper at error_utils.py handles the async bridge correctly.
- **RESEARCH Reference:** None

---

*Findings documented: 2026-05-03*
*Breadth scan completed: 2026-05-03*
*Deep-dive (P1 main.py, runs_routes.py, run_pipeline.py) completed: 2026-05-03*
