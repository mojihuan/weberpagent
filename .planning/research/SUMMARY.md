# Project Research Summary

**Project:** aiDriveUITest v0.10.4 -- Playwright Code Verification and Task Management UI
**Domain:** AI-driven UI test automation -- Playwright code lifecycle (view, execute, verify)
**Researched:** 2026-04-23
**Confidence:** HIGH

## Executive Summary

This is an incremental feature release for an existing AI-driven UI test automation platform. The v0.10.4 milestone adds Playwright code visibility and manual re-execution to the task management workflow. The core challenge is not building new infrastructure -- it is correctly exposing what already exists (SelfHealingRunner subprocess execution, generated code files on disk, Run.healing_status tracking) through new API endpoints and frontend components.

The recommended approach is reuse-heavy: the backend adds two thin endpoints (GET code content, POST execute code) that delegate entirely to existing SelfHealingRunner and filesystem patterns. The frontend adds one new dependency (react-syntax-highlighter for read-only code display) and two new components (CodeViewerModal, RunCodeDialog) that follow established modal patterns. The Task.status extension to include "success" is the most architecturally sensitive change -- research strongly recommends deriving success from Run status rather than extending the Task status enum, to avoid conflating editorial state with execution outcome.

The primary risks are operational, not architectural. Orphaned Chrome processes from subprocess pytest execution can exhaust the 2GB deployment server's memory. Path traversal in the code-serving endpoint could expose secrets. Concurrent "Run Code" clicks without a semaphore gate could crash the server. All three have straightforward mitigations documented in the pitfalls research.

## Key Findings

### Recommended Stack

Only one new dependency is needed. The entire backend change reuses stdlib and existing infrastructure.

**Core technologies:**
- **react-syntax-highlighter 16.1.1 (Prism build):** Read-only Python code viewer component -- chosen over Monaco/CodeMirror (4MB+ overkill), Shiki (async complexity), and prism-react-renderer (more boilerplate). 40KB gzipped, zero-config line numbers and themes.
- **@types/react-syntax-highlighter 15.5.13:** TypeScript definitions for the above.
- **subprocess + asyncio.to_thread (stdlib, existing):** Code execution reuses the established SelfHealingRunner pattern -- no new subprocess code.
- **pathlib.Path (stdlib, existing):** File reading for code content serving, using `generated_code_path` from the Run model.

### Expected Features

**Must have (P1 -- table stakes):**
- UI-01: Task list "code" column -- icon/badge showing whether a task has generated Playwright code
- UI-02: View generated code modal -- read-only Python viewer with syntax highlighting and line numbers
- UI-03: Run code button -- triggers pytest execution via SelfHealingRunner, shows pass/fail result
- STATUS-01: Task status "success" -- marks task as verified after code execution passes

**Should have (P2 -- differentiators):**
- Code status badge on task row -- color-coded indicator (green/yellow/red/gray) for code health
- Inline execution feedback -- real-time pytest output in the code viewer

**Defer (v2+):**
- In-place code editing -- breaks AI-driven workflow; edits get overwritten on re-run
- Full IDE in browser -- scope creep beyond QA tester needs
- Automatic status promotion on healing pass -- hides uncertainty from flaky results

### Architecture Approach

The architecture follows a strict reuse pattern. Two new FastAPI endpoints wrap existing infrastructure: GET /runs/{id}/code reads from the filesystem (no database storage of code content), and POST /runs/{id}/run-code delegates to SelfHealingRunner with max_iterations=1 (disabling LLM retry). The frontend adds a CodeViewer/ component folder following the established feature-folder pattern. The TaskResponse gains a computed has_code field from a SQL subquery, avoiding denormalization.

**Major components:**
1. **CodeViewerModal** -- read-only Python display using react-syntax-highlighter, follows existing modal pattern (ConfirmModal, ImageViewer)
2. **RunCodeDialog** -- confirmation + execution result display, reuses ConfirmModal + loading state pattern from BatchExecuteDialog
3. **GET /runs/{id}/code endpoint** -- reads generated_code_path from DB, validates path within outputs/, serves file content as JSON
4. **POST /runs/{id}/run-code endpoint** -- instantiates SelfHealingRunner, executes pytest, updates Task.status on pass, uses asyncio.Semaphore(1) for concurrency control

### Critical Pitfalls

1. **Orphaned Chrome processes from subprocess pytest** -- Use `start_new_session=True` + `os.killpg()` for process group kill on timeout. Add `_active_code_runs` tracking dict. Register FastAPI shutdown handler.
2. **Path traversal in code file serving** -- Never accept raw file paths as API parameters. Resolve from DB, validate with `Path.is_relative_to(OUTPUTS_DIR)`. Only serve .py files.
3. **Task status "success" conflating editorial state with execution outcome** -- Strongly consider deriving success from latest Run.healing_status instead of extending Task.status. If extending, update ALL validation layers (schema regex, TypeScript type, StatusBadge).
4. **Concurrent code execution exhausting server memory** -- Use `asyncio.Semaphore(1)`. Return HTTP 409 Conflict for concurrent requests. Debounce frontend button.
5. **XSS via generated code content** -- Use react-syntax-highlighter (renders text nodes, not raw HTML). Never use dangerouslySetInnerHTML. Set Content-Type to text/plain.

## Implications for Roadmap

### Phase 1: Backend Data Layer and API Endpoints

**Rationale:** Backend changes have zero frontend dependencies and establish the API contract. Building this first allows frontend work to proceed against real endpoints.
**Delivers:** Two new endpoints, schema extensions, SelfHealingRunner parameterization.
**Addresses:** UI-02 (code serving), UI-03 (code execution), STATUS-01 (status extension), UI-01 (has_code field).
**Avoids:** Pitfalls 1 (process group kill), 2 (path validation), 4 (semaphore gate), 9 (SQLite contention), 10 (output truncation).

Key changes:
- Add `max_iterations` parameter to SelfHealingRunner.run()
- Add GET /runs/{run_id}/code with path traversal protection
- Add POST /runs/{run_id}/run-code with Semaphore(1) and process group tracking
- Extend TaskResponse with computed `has_code` field (SQL subquery)
- Extend Task.status validation to include "success" (or implement derived approach)
- Add `asyncio.Semaphore(1)` + `_active_code_runs` tracking module

### Phase 2: Frontend Infrastructure and API Integration

**Rationale:** Depends on Phase 1 endpoints being available. Installs the single new dependency and wires up API functions.
**Delivers:** react-syntax-highlighter installed, TypeScript types updated, API functions ready.
**Uses:** react-syntax-highlighter, existing lucide-react icons.
**Implements:** Frontend data layer for code viewing/execution.

Key changes:
- Install react-syntax-highlighter + @types/react-syntax-highlighter
- Add `getCode()` and `runCode()` to frontend/src/api/runs.ts
- Update Task type: add `'success'` to status union, add `has_code?: boolean`
- Update StatusBadge config for "success" status

### Phase 3: Frontend UI Components

**Rationale:** Depends on Phase 2 for API wiring. Builds the user-facing components.
**Delivers:** CodeViewerModal, RunCodeDialog, task list "code" column.
**Addresses:** UI-01, UI-02, UI-03 frontend implementation.
**Avoids:** Pitfall 5 (XSS via react-syntax-highlighter), Pitfall 6 (large file rendering with line cap), Pitfall 8 (race condition with healing_status gate).

Key changes:
- Build CodeViewerModal with react-syntax-highlighter Prism build
- Build RunCodeDialog with confirmation, loading state, result display
- Add "code" column to TaskTable
- Add code indicator and view/run buttons to TaskRow
- Wire Tasks page to host new modals

### Phase 4: Integration and Security Testing

**Rationale:** Validates the full flow end-to-end and catches the "looks done but isn't" items from pitfalls research.
**Delivers:** E2E tests, security tests, concurrency tests.
**Addresses:** All pitfalls from the "Looks Done But Isn't" checklist.

Key tests:
- E2E: task with code -> view code -> verify display
- E2E: task with code -> run code -> verify status update to "success"
- Security: path traversal payloads return 404
- Security: XSS payloads in code content do not execute
- Concurrency: two simultaneous run-code requests -> one 409
- Edge case: file not found -> 404 with clear message
- Edge case: code generation in progress -> button disabled

### Phase Ordering Rationale

- Phase 1 before Phase 2-3: Backend API contract must exist before frontend can integrate. No mock server needed.
- Phase 2 before Phase 3: API functions and types must be ready before components consume them.
- Phase 4 last: Integration testing requires both backend and frontend complete.
- STATUS-01 in Phase 1: The status extension is a prerequisite for the "mark as success" flow in UI-03.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1 (Task status decision):** The choice between deriving success from Run.status vs. extending Task.status is an architectural decision that should be finalized during requirements. Both research files recommend deriving, but the milestone description says "extend status."
- **Phase 1 (SelfHealingRunner parameterization):** Adding `max_iterations` to an existing class needs careful testing to ensure it doesn't break the self-healing pipeline (which uses max_iterations=3).

Phases with standard patterns (skip research-phase):
- **Phase 2:** Standard npm install + TypeScript type updates. Well-documented patterns.
- **Phase 3:** Standard React component development following existing project conventions (modal pattern, TaskRow pattern).
- **Phase 4:** Standard Playwright E2E + security testing patterns.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Only one new dependency (react-syntax-highlighter). All alternatives evaluated against specific requirements. Backend uses 100% existing infrastructure. |
| Features | HIGH | Feature specifications derived from direct codebase analysis. Dependencies mapped with existing code references. Priority matrix based on user value vs. cost. |
| Architecture | HIGH | Architecture is primarily reuse of existing patterns (SelfHealingRunner, modal components, subprocess execution). All component boundaries mapped to existing files. |
| Pitfalls | HIGH | Critical pitfalls identified with CVE references, GitHub issues, and direct codebase analysis. Recovery strategies documented. "Looks Done But Isn't" checklist provided. |

**Overall confidence:** HIGH

### Gaps to Address

- **Task "success" status semantics:** Research recommends deriving from Run.status (Option A), but the milestone says "extend Task.status" (Option C). This decision must be finalized during requirements definition. Option A is cleaner architecturally; Option C is simpler to query.
- **SelfHealingRunner.run() thread safety:** Adding `max_iterations` parameter and potentially calling run() from a new endpoint context needs verification that the class is stateless between calls or properly resets.
- **Deployment server memory headroom:** The 2GB server constraint (121.40.191.49) means the Semaphore(1) gate is critical. Verify current memory usage during normal operation to confirm one additional Chrome process (~300MB) fits within available headroom.

## Sources

### Primary (HIGH confidence)
- Codebase analysis: `backend/core/self_healing_runner.py`, `backend/core/code_generator.py`, `backend/api/routes/runs.py`, `backend/db/models.py`, `backend/db/schemas.py`, `backend/db/repository.py`, `frontend/src/types/index.ts`, `frontend/src/components/TaskList/`
- [react-syntax-highlighter NPM](https://www.npmjs.com/package/react-syntax-highlighter) -- version 16.1.1, Python support confirmed
- [pytest-timeout subprocess leak](https://github.com/pytest-dev/pytest-timeout/issues/159) -- orphaned process behavior documented
- [Playwright Python zombie threads](https://github.com/microsoft/playwright-python/issues/2397) -- server environment issue
- [FastAPI path traversal CVE-2025-55526](https://www.sentinelone.com/vulnerability-database/cve-2025-55526/) -- exact vulnerability pattern

### Secondary (MEDIUM confidence)
- [Shiki vs Prism vs highlight.js comparison](https://www.pkgpulse.com/blog/shiki-vs-prismjs-vs-highlightjs-syntax-highlighting-javascript-2026) -- feature comparison
- [react-syntax-highlighter large file issue](https://github.com/react-syntax-highlighter/react-syntax-highlighter/issues/545) -- DOM bloat for 500+ lines
- [Playwright in production memory issues](https://medium.com/@onurmaciit/8gb-was-a-lie-playwright-in-production-c2bdbe4429d6) -- production memory analysis
- [TestRail Code-first workflow](https://support.testrail.com/hc/en-us/articles/12609674354068-Code-first-workflow) -- competitor reference
- [FastAPI Background Tasks docs](https://fastapi.tiangolo.com/tutorial/background-tasks/) -- existing async pattern

---
*Research completed: 2026-04-23*
*Ready for roadmap: yes*
