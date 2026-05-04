# Phase 126: API Layer & Security Review - Research

**Researched:** 2026-05-03
**Domain:** API route review, security audit, parameter validation, error handling
**Confidence:** HIGH

## Summary

This is a review-only phase that audits all 11 API route files, `main.py` (CORS/middleware/exception handlers), and `response.py` (error format) for parameter validation gaps, error handling omissions, and security risks. The phase must cover CORR-02 (API route correctness) and SEC-01 (security risks).

The codebase uses a standard FastAPI + Pydantic stack. Route files follow a consistent pattern: APIRouter with prefix, Depends-based DI, Pydantic schemas for request/response. Global exception handlers in `main.py` provide a safety net for unhandled exceptions. However, the review must identify gaps where this safety net is bypassed or where route-level error handling is inconsistent.

Phase 125 already reviewed `run_pipeline.py`'s business logic (32 findings). Phase 126 must supplement with API-layer concerns: HTTP status codes, parameter validation completeness, SSE stream error handling, and security risks -- without duplicating Phase 125's business logic findings.

**Primary recommendation:** Use a structured checklist per route covering 8 security/validation categories. Priority files are external_* routes (exec/code execution), batches (fire-and-forget), and run_pipeline (SSE stream handling). The `CONCERNS.md` security section provides 6 pre-identified issues to verify against the public-internet severity standard.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** run_pipeline.py -- supplement API-layer review only (parameter validation, HTTP status codes, SSE stream error handling); Phase 125 business logic findings not duplicated
- **D-02:** CONCERNS.md security issues (CORS `*`, no auth, stack traces, etc.) verified and confirmed; results referenced in FINDINGS.md, not rewritten
- **D-03:** All security issues evaluated against "public internet deployment" severity standard, with dual assessment: current impact + public impact
- **D-04:** Route files prioritized by risk: P1 (code execution/external module routes: batches, run_pipeline, runs_routes, external_*), P2 (CRUD routes: tasks, runs, reports), P3 (simple routes: dashboard)
- **D-05:** "Breadth-first + focused deep-dive" strategy matching Phase 125: quick scan all routes marking risk, then deep-dive high priority
- **D-06:** Review focus: (1) parameter validation gaps, (2) error handling omissions, (3) security risks (path traversal, CSRF, exec() safety, unsafe config, SSRF), (4) SSE stream error handling
- **D-07:** Findings output to `126-FINDINGS.md`, using Phase 125's 4-level severity (Critical/High/Medium/Low) and category labels (Correctness/Security/Architecture/Performance)
- **D-08:** Plan split into 3 plans matching Phase 125: Plan 1 breadth scan, Plan 2 P1 deep-dive, Plan 3 P2+P3+summary

### Claude's Discretion
- Specific risk scoring criteria for breadth scan
- P1/P2/P3 file assignment (breadth scan results inform final assignment)
- Specific security check item ordering and depth

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CORR-02 | Audit API route correctness: parameter validation, error handling, boundary conditions, error paths | Per-route analysis of Pydantic schema coverage, HTTP status code consistency, missing try/except, edge cases |
| SEC-01 | Audit security risks: path traversal, CSRF protection, exec() safety, unsafe config, SSRF | Security checklist per route: input sanitization, CORS gaps, authentication missing, credential exposure, code execution surface |
</phase_requirements>

## Standard Stack

### Core (Review Context -- Not Installation)
| Library | Version | Purpose | Relevance to Review |
|---------|---------|---------|---------------------|
| FastAPI | >=0.135.1 | API framework | Request validation auto-generation, dependency injection, exception handling |
| Pydantic | >=2.4.0 | Schema validation | Field constraints, validators, model_validate |
| SQLAlchemy | >=2.0 | Async ORM | Repository pattern, session management |
| uvicorn | >=0.34.0 | ASGI server | Lifespan events, middleware |

### Security-Relevant Patterns
| Pattern | Implementation | Review Concern |
|---------|---------------|----------------|
| Global exception handlers | `main.py` lines 97-149 | Stack trace exposure at DEBUG level |
| CORS middleware | `main.py` lines 75-83 | `allow_origins=["*"]` |
| Pydantic validation | `api/schemas/index.py` | Field constraints (min_length, max_length, ge, le, pattern) |
| Path validation | `runs_routes.py` `_validate_code_path()` | Path traversal protection |
| 503 guard | `external_*` routes via `require_external_available()` | Service unavailable handling |

## Architecture Patterns

### Route File Pattern (All 11 Route Files)
```
route_file.py
  -> APIRouter(prefix="/resource", tags=["resource"])
  -> @router.get/post/put/delete with response_model
  -> Depends(get_db) for session injection
  -> Depends(get_*_repo) for repository injection
  -> raise_not_found() for 404s
  -> HTTPException for other errors
```

### Error Handling Flow
```
Route handler
  -> try/except (sometimes)
  -> raise HTTPException(status_code, detail)
  -> raise_not_found(entity_type, entity_id)
  -> Falls through to global handlers:
     -> StarletteHTTPException handler -> {"success": false, "error": {"code": "HTTP_xxx", ...}}
     -> RequestValidationError handler -> {"success": false, "error": {"code": "VALIDATION_ERROR", ...}}
     -> Exception handler (catch-all) -> {"success": false, "error": {"code": "INTERNAL_ERROR", ...}}
```

### Response Format Inconsistency
Two parallel patterns exist:
1. **Global exception handlers** return `{"success": false, "error": {...}}` format
2. **Route handlers** return Pydantic response models directly (e.g., `TaskResponse`, `RunResponse`) -- these do NOT include `{"success": true, "data": ...}` wrapper
3. Some routes return plain `dict` (dashboard, tasks import, delete)

The `success_response()` and `error_response()` helpers in `response.py` are NOT used by any route. The API response format documented in CLAUDE.md (`{"success": true, "data": {...}}`) is only enforced on error paths via global handlers.

### Anti-Patterns to Avoid (During Review)
- **Don't flag Pydantic auto-validation as a gap** -- FastAPI automatically validates request bodies via Pydantic schemas and returns 422 (caught by `RequestValidationError` handler returning 400)
- **Don't duplicate Phase 125 findings** -- run_pipeline.py business logic already reviewed; only supplement API-layer concerns
- **Don't flag missing authentication as a new finding** -- already in CONCERNS.md; verify and reference only

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Parameter validation | Custom validation in route body | Pydantic Field constraints + validators | FastAPI auto-validates and returns 400 on failure |
| 404 responses | Manual dict construction | `raise_not_found()` from helpers.py | Consistent format across all routes |
| Error response format | Manual dict construction | Global exception handlers | Consistent `{"success": false, "error": {...}}` format |
| CORS configuration | Per-route CORS headers | CORSMiddleware on app | Applied globally, consistently |

## Common Pitfalls

### Pitfall 1: Response Format Inconsistency
**What goes wrong:** Most routes return Pydantic models directly (not wrapped in `{"success": true, "data": ...}`). Only error responses use the standard format. The documented API response format is only half-implemented.
**Why it matters:** Frontend must handle two different response structures.
**Warning signs:** Routes using `response_model=list[TaskResponse]` instead of wrapped format.

### Pitfall 2: Missing Pydantic Field Constraints on Path Parameters
**What goes wrong:** Path parameters like `task_id: str`, `run_id: str`, `batch_id: str` have no length or format constraints. An attacker could pass extremely long strings, SQL-like content (not SQL injection risk with ORM, but unexpected behavior), or empty strings.
**Why it matters:** `task_id` is an 8-char hex string. No validation ensures this format.
**Warning signs:** `def get_task(task_id: str, ...)` without `Field(..., min_length=8, max_length=8, pattern="^[a-f0-9]+$")`.

### Pitfall 3: SSE Stream Error Handling Gaps
**What goes wrong:** The SSE endpoint (`GET /api/runs/{run_id}/stream`) uses an async generator that yields from `event_manager.subscribe()`. If the generator raises an exception, the StreamingResponse may not properly close the connection, leaving orphaned event queues.
**Why it matters:** Multiple reconnection attempts could leak memory via uncleaned EventManager state.
**Warning signs:** No try/except/finally in `event_generator()`.

### Pitfall 4: File Path Exposure in Screenshot/Report Endpoints
**What goes wrong:** `get_screenshot()` returns `FileResponse(step.screenshot_path)` where `screenshot_path` comes from the database. If an attacker could write arbitrary paths to the database (via a compromised route), they could read any file on the server.
**Why it matters:** `FileResponse` does not validate the path is within expected directory bounds.
**Warning signs:** `FileResponse(step.screenshot_path)` without path validation like `_validate_code_path()`.

### Pitfall 5: Fire-and-Forget Task with No Error Propagation
**What goes wrong:** `asyncio.create_task(service.start(run_configs))` in batches.py creates a background task. If `service.start()` raises immediately (before the first await), the exception is silently swallowed until the task is garbage collected.
**Why it matters:** The batch appears "created" in the response but may have already failed internally.
**Warning signs:** `asyncio.create_task()` without `task.add_done_callback()` for error logging.

### Pitfall 6: subprocess.run with User-Influenced Paths
**What goes wrong:** `runs_routes.py:108` runs `subprocess.run(["uv", "run", "pytest", test_file_path, ...])`. While `test_file_path` comes from `run.generated_code_path` (database), and `_validate_code_path()` is called before execution in the code viewer, the `execute_run_code` endpoint at line 299 passes `run.generated_code_path` directly to `_execute_code_background` WITHOUT re-validating the path.
**Why it matters:** If `generated_code_path` was tampered with in the database, arbitrary commands could be executed.
**Warning signs:** `test_file_path=run.generated_code_path` at line 302 without `_validate_code_path()` call.

### Pitfall 7: Global DEBUG Logging Exposes Stack Traces
**What goes wrong:** `main.py` line 44 sets `logging.basicConfig(level=logging.DEBUG)`. The exception handler at line 146 checks `logging.getLogger().level == logging.DEBUG` to decide whether to include stack traces. Since DEBUG is hardcoded, stack traces are ALWAYS included in error responses.
**Why it matters:** Stack traces reveal internal code structure, file paths, and variable names to anyone hitting an error endpoint.
**Warning signs:** `"stack": traceback.format_exc()` in API responses.

### Pitfall 8: Credentials in API Responses
**What goes wrong:** The `_build_login_credentials()` function in `runs_routes.py` constructs a dict with plaintext account/password. While this is used internally for background task execution, the credentials flow through multiple function calls and could potentially leak into logs or error responses.
**Why it matters:** Credentials appear in `_login_config` dict passed to code generation, which embeds them in generated test files stored on disk.

## Code Examples

### Path Traversal Protection (runs_routes.py -- Good Pattern)
```python
def _validate_code_path(code_path: str) -> Path:
    """Validate code path exists and is within outputs/ directory (per D-03)."""
    resolved = Path(code_path).resolve()
    outputs_root = Path("outputs").resolve()
    if not str(resolved).startswith(str(outputs_root)):
        raise HTTPException(status_code=403, detail="illegal file path")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="code file not found")
    return resolved
```

### Missing Path Validation (runs_routes.py -- Gap)
```python
@router.get("/{run_id}/screenshots/{step_index}")
async def get_screenshot(run_id: str, step_index: int, ...) -> FileResponse:
    step = await step_repo.get_by_index(run_id, step_index)
    if not step or not step.screenshot_path:
        raise_not_found("Screenshot")
    return FileResponse(step.screenshot_path, media_type="image/png")
    # NOTE: No path validation on step.screenshot_path!
```

### Pydantic Validation (api/schemas/index.py -- Good Pattern)
```python
class BatchCreateRequest(BaseModel):
    task_ids: List[str] = Field(..., min_length=1, max_length=50)
    concurrency: int = Field(default=2, ge=1, le=4)
```

### Missing Parameter Validation (runs_routes.py -- Gap)
```python
@router.post("", response_model=RunResponse)
async def create_run(task_id: str, ...):  # task_id has no length/format constraint
    task = await task_repo.get(task_id)
    if not task:
        raise_not_found("Task", task_id)
```

### File Upload Validation (tasks.py -- Good Pattern)
```python
async def _validate_upload_file(file: UploadFile) -> bytes:
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files supported")
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    return content
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Global `Optional[str]` | `str | None` union syntax | Python 3.10+ | api/schemas still uses `Optional` in some places |
| `from_attributes=True` per model | `ConfigDict(from_attributes=True)` | Pydantic v2 | All response models use this correctly |
| Manual response wrapping | Global exception handlers | FastAPI pattern | Most routes return raw models, not wrapped |

**Deprecated/outdated:**
- `backend/db/schemas.py`: Uses old-style `Optional[str]` and `Literal` for status fields. These schemas are NOT used by routes (routes use `api/schemas/index.py`), but they exist as legacy models.

## Route File Inventory

### Complete File List with Line Counts and Priority

| File | Lines | Priority | Key Concerns |
|------|-------|----------|-------------|
| `main.py` | 160 | P1 | CORS `*`, DEBUG stack traces, no auth middleware |
| `response.py` | 85 | P3 | Unused helpers (`success_response`, `error_response`), `ErrorCodes` unused |
| `__init__.py` | 96 | P3 | Only imports `tasks` and `runs`, but 8 routers registered in main.py |
| `run_pipeline.py` | 577 | P1 | SSE events, pipeline orchestration API layer (business logic already reviewed in Phase 125) |
| `runs_routes.py` | 367 | P1 | subprocess.run, FileResponse without path validation, SSE stream, code execution |
| `batches.py` | 140 | P1 | Fire-and-forget asyncio.create_task, no error callback |
| `external_assertions.py` | 211 | P1 | Executes external assertion methods (code execution surface) |
| `external_data_methods.py` | 101 | P1 | Executes external data methods (code execution surface) |
| `external_operations.py` | 88 | P1 | Generates precondition code from external modules |
| `tasks.py` | 160 | P2 | File upload, Excel import, Task CRUD |
| `reports.py` | 127 | P2 | Report retrieval, FileResponse |
| `runs.py` | 14 | P2 | Backward-compat re-exports only |
| `dashboard.py` | 97 | P3 | Read-only aggregation queries |

### Security Check Matrix (Per Route)

| Check | batches | run_pipeline | runs_routes | external_assert | external_data | external_ops | tasks | reports | dashboard |
|-------|---------|-------------|-------------|----------------|--------------|-------------|-------|---------|-----------|
| Param validation gaps | task_ids format | N/A (no HTTP) | task_id, run_id format | class_name, method_name format | class_name, method_name format | operation_codes format | file upload OK | report_id format | N/A |
| Error handling omissions | fire-and-forget | SSE None handling | subprocess error propagation | execution error format | execution error format | WEBSERP_PATH check | import rollback | DB query errors | N/A |
| Path traversal risk | N/A | N/A | screenshot FileResponse, code FileResponse | N/A | N/A | N/A | N/A | report FileResponse | N/A |
| CORS/Auth gap | ALL routes | ALL routes | ALL routes | ALL routes | ALL routes | ALL routes | ALL routes | ALL routes | ALL routes |
| Code execution surface | batch spawns tasks | pipeline exec | subprocess.run | execute_assertion_method | execute_data_method | N/A | N/A | N/A | N/A |
| SSRF risk | N/A | target_url param | N/A | api_params dict | params dict | N/A | N/A | N/A | N/A |
| Credential exposure | N/A | login_config | _build_login_credentials | N/A | N/A | N/A | N/A | N/A | N/A |
| SSE stream errors | N/A | event publishing | event_generator cleanup | N/A | N/A | N/A | N/A | N/A | N/A |

## CONCERNS.md Security Issues to Verify

The following 6 security issues are pre-identified in CONCERNS.md. Phase 126 must verify each and provide updated severity assessment per D-03 (public internet standard).

| CONCERNS.md Entry | Location | Phase 126 Action |
|-------------------|----------|------------------|
| CORS allows all origins | main.py:77-83 | Verify + assess public internet severity |
| No authentication/authorization | All routes | Verify + assess public internet severity |
| Stack traces in production | main.py:132-149 | Verify DEBUG level always active + assess |
| Credentials in generated files | code_generator.py:197-201 | Already confirmed in Phase 125; reference only |
| LLM API keys logged partially | auth_service.py:85 | Out of API layer scope but note for completeness |
| exec() for user code | precondition_service.py | Out of API layer scope but note for completeness |

## Environment Availability

Step 2.6: SKIPPED (review-only phase with no external dependencies -- all analysis is code reading)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None -- test suite deleted in v0.11.0 |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

**Note:** This is a review-only phase that produces findings, not code. No automated tests are needed. The validation is human review of findings quality and completeness.

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CORR-02 | API route parameter validation audit | Manual review | N/A | N/A |
| SEC-01 | Security risk assessment | Manual review | N/A | N/A |

### Wave 0 Gaps
None -- review-only phase requires no test infrastructure.

## Open Questions

1. **Response format standardization**
   - What we know: Most routes return raw Pydantic models. Error responses use the standard format. `success_response()` and `error_response()` exist but are unused.
   - What's unclear: Whether the documented format (`{"success": true, "data": ...}`) was ever fully implemented or was always aspirational.
   - Recommendation: Flag as an architecture finding, not a bug. The frontend handles both formats.

2. **`__init__.py` incomplete exports**
   - What we know: `routes/__init__.py` only imports `tasks` and `runs`, but `main.py` imports 8 route modules directly.
   - What's unclear: Whether `__init__.py` is intentionally minimal or a maintenance gap.
   - Recommendation: Flag as Low/Architecture. No functional impact since main.py imports directly.

3. **External module route validation depth**
   - What we know: `require_external_available()` raises 503 if external module not loaded. But what about partial module states (loaded but some classes missing)?
   - What's unclear: Whether `execute_assertion_method()` and `execute_data_method()` handle partial module states gracefully.
   - Recommendation: Check during deep-dive of external_* routes.

## Sources

### Primary (HIGH confidence)
- Direct code reading of all 13 files in scope (main.py, response.py, 11 route files)
- `api/schemas/index.py` -- Pydantic schema definitions with field constraints
- `api/helpers.py` -- Shared error handling helpers
- Phase 125 FINDINGS.md -- 32 findings providing context for what was already reviewed

### Secondary (MEDIUM confidence)
- `codebase/ARCHITECTURE.md` -- API Layer architecture and data flow
- `codebase/CONVENTIONS.md` -- Error handling patterns and response format
- `codebase/CONCERNS.md` -- Pre-identified security issues (6 items)
- `codebase/INTEGRATIONS.md` -- External module integration details

### Tertiary (LOW confidence)
- Web search not performed -- all findings based on direct code reading (highest confidence source)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- directly verified from source code and pyproject.toml
- Architecture patterns: HIGH -- all 13 files read and analyzed
- Pitfalls: HIGH -- derived from concrete code patterns found during analysis
- Security issues: HIGH -- verified against CONCERNS.md and source code

**Research date:** 2026-05-03
**Valid until:** 2026-06-03 (stable -- code is not changing during review phases)
