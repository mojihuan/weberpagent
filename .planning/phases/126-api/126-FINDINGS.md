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

---

*Findings documented: 2026-05-03*
*Breadth scan completed: 2026-05-03*
