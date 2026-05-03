# Phase 128: Code Quality Review - Findings

**Review Date:** 2026-05-03
**Scope:** Full-stack codebase (backend: ~12,527 lines Python, frontend: ~8,898 lines TypeScript/TSX)
**Methodology:** Tool-assisted breadth scan (radon cc/mi + ESLint complexity) + cross-reference mapping + quick-scan for MAINT/ARCH-03/PERF-01 quality dimensions
**Reference:** Cross-references Phase 125 (backend core), Phase 126 (API layer), Phase 127 (frontend) findings

## Tool Results

### radon Cyclomatic Complexity (cc)

548 blocks (classes, functions, methods) analyzed. Average complexity: A (3.31).

**Grade C or worse (MAINT-02 concern threshold):**

| File | Block | Grade | Complexity |
|------|-------|-------|------------|
| backend/core/code_generator.py | `PlaywrightCodeGenerator.generate` | **F** | >10 |
| backend/core/action_translator.py | `ActionTranslator.translate` | C | 11-20 |
| backend/core/action_translator.py | `ActionTranslator.translate_with_llm` | C | 11-20 |
| backend/core/external_execution_engine.py | `execute_data_method` | C | 11-20 |
| backend/core/external_execution_engine.py | `_resolve_assertion_instance` | C | 11-20 |
| backend/core/external_execution_engine.py | `_parse_operations_from_source` | C | 11-20 |
| backend/core/agent_service.py | `AgentService._run_detectors` | C | 11-20 |
| backend/core/agent_service.py | `AgentService._extract_agent_output` | C | 11-20 |
| backend/core/report_service.py | `ReportService.generate_report` | C | 11-20 |
| backend/core/locator_chain_builder.py | `LocatorChainBuilder.extract` | D | 21-30 |
| backend/core/locator_chain_builder.py | `LocatorChainBuilder` (class) | C | class avg |
| backend/core/external_method_discovery.py | `extract_method_info` | C | 11-20 |
| backend/core/external_method_discovery.py | `_build_docstring_method_map` | C | 11-20 |
| backend/core/external_method_discovery.py | `_patch_import_api_aliases` | C | 11-20 |
| backend/core/external_method_discovery.py | `_remap_stale_module_map_classes` | C | 11-20 |
| backend/utils/excel_parser.py | `_coerce_column_value` | C | 11-20 |
| backend/utils/excel_parser.py | `_validate_headers` | C | 11-20 |
| backend/agent/pre_submit_guard.py | `PreSubmitGuard.check` | C | 11-20 |
| backend/agent/dom_patch.py | `_annotate_erp_input_node` | C | 11-20 |
| backend/db/database.py | `init_db` | C | 11-20 |
| backend/api/routes/dashboard.py | `get_dashboard` | C | 11-20 |
| backend/api/routes/run_pipeline.py | `run_agent_background` | C | 11-20 |
| backend/api/routes/run_pipeline.py | `_run_preconditions` | C | 11-20 |
| backend/api/routes/run_pipeline.py | `_publish_external_assertion_results` | C | 11-20 |

**Key takeaway:** Only 1 function at grade F (`PlaywrightCodeGenerator.generate` in code_generator.py). 23 functions at grade C. Average complexity A (3.31) is healthy. The F-grade function is the primary MAINT-02 concern.

### radon Maintainability Index (mi)

All files scored grade A (20-100 range) except:

| File | MI Grade |
|------|----------|
| backend/core/external_execution_engine.py | **B** (partial, 700 lines) |
| backend/core/external_method_discovery.py | **B** (partial, 669 lines) |

No files scored below MI grade B. The B grades for external_execution_engine.py and external_method_discovery.py correlate with their large file sizes (700 and 669 lines respectively) and higher cyclomatic complexity.

### ESLint Complexity (frontend)

28 errors + 3 warnings across 87 files. **12 functions exceed complexity threshold of 10:**

| File | Function | Complexity |
|------|----------|------------|
| frontend/src/components/TaskModal/JsonTreeViewer.tsx | `JsonNode` | **26** |
| frontend/src/components/TaskModal/TaskForm.tsx | `TaskForm` | **24** |
| frontend/src/components/TaskModal/AssertionSelector.tsx | `AssertionSelector` | **16** |
| frontend/src/components/RunMonitor/StepTimeline.tsx | Arrow function (line 69) | **14** |
| frontend/src/components/TaskModal/DataMethodSelector.tsx | `DataMethodSelector` | **14** |
| frontend/src/components/TaskModal/DataMethodSelector.tsx | Arrow function (line 500) | **14** |
| frontend/src/components/TaskModal/TaskForm.tsx | Arrow function (line 368) | **14** |
| frontend/src/components/TaskModal/DataMethodSelector.tsx | Arrow function (line 361) | **13** |
| frontend/src/api/client.ts | `apiClient` | **11** |
| frontend/src/components/Report/TimelineItemCard.tsx | `StepExpandedContent` | **11** |
| frontend/src/components/RunMonitor/ScreenshotPanel.tsx | `ScreenshotPanel` | **11** |
| frontend/src/components/TaskModal/FieldParamsEditor.tsx | `FieldParamsEditor` | **11** |
| frontend/src/components/TaskModal/OperationCodeSelector.tsx | `OperationCodeSelector` | **11** |

**Key takeaway:** JsonTreeViewer.tsx:JsonNode (complexity 26) and TaskForm.tsx:TaskForm (complexity 24) are the highest complexity functions. DataMethodSelector.tsx has 3 functions exceeding the threshold (14, 14, 13), totaling the worst complexity density. 5 of 12 high-complexity functions are in TaskModal components, confirming the task form area as the most complex frontend region.

## Risk Priority Matrix

### Backend Files

| Priority | File | Lines | CC Grade | MAINT-01 | MAINT-02 | MAINT-03 | ARCH-03 | PERF-01 | Risk Justification |
|----------|------|-------|----------|----------|----------|----------|---------|---------|-------------------|
| P1 | backend/api/routes/run_pipeline.py | 576 | C | High | High | Low | High | Medium | God-module (13+ deps), 3 C-grade functions, dual config access, sync I/O in non_blocking_execute |
| P1 | backend/core/agent_service.py | 658 | C | High | High | Medium | Medium | High | 2 C-grade functions, dual stall/progress tracking (DRY), sync write_bytes, DOM serialization |
| P1 | backend/core/code_generator.py | 553 | **F** | Medium | **Critical** | Low | Low | Low | Only F-grade function (generate), credential embedding, unescaped assertion values |
| P1 | backend/core/external_execution_engine.py | 700 | C | Medium | High | Low | Medium | Low | 3 C-grade functions, context mutation, getattr() with user input |
| P1 | backend/core/action_translator.py | 718 | C | Low | High | Medium | Low | Low | 2 C-grade functions, ambiguous variable `l` (MAINT-03), ERP-specific heuristics |
| P1 | backend/agent/dom_patch.py | 777 | C | Low | Medium | Low | Low | Low | Largest file, monkey-patch fragility, 1 C-grade function, 9 mypy errors |
| P1 | backend/core/step_code_buffer.py | 414 | A | Medium | Medium | Low | Low | High | Duplicated wait logic, private method cross-class call, corrective detection gap |
| P1 | backend/agent/monitored_agent.py | 227 | A | High | Low | Medium | Low | Medium | Dead code (PreSubmitGuard None params), async sleep, duplicate DOM hash computation |
| P2 | backend/core/external_method_discovery.py | 669 | C | Low | High | Low | Low | Low | 4 C-grade functions, unused import, complex alias patching |
| P2 | backend/core/precondition_service.py | 378 | A | Low | Low | Low | High | Low | exec() with full builtins (ARCH-03: cross-cutting error handling), nest_asyncio global patch |
| P2 | backend/core/event_manager.py | 156 | A | Low | Low | Low | Medium | High | Memory leak (cleanup never called), heartbeat task leak on re-subscribe |
| P2 | backend/core/batch_execution.py | 107 | A | Medium | Low | Low | Medium | Medium | Semaphore private access, fire-and-forget, upward dependency to API layer |
| P2 | backend/core/assertion_service.py | 157 | A | Low | Low | **High** | Low | Low | check_element_exists stub (MAINT-03: misleading name vs behavior) |
| P2 | backend/agent/stall_detector.py | 221 | A | Low | Low | Low | Low | Low | Unbounded _history, but short-lived instances; dual detection in P1 agent_service |
| P2 | backend/agent/pre_submit_guard.py | 149 | C | Low | Medium | **High** | Low | Low | C-grade check() function, dead core logic (MAINT-03: name implies active, behavior is no-op) |
| P2 | backend/api/routes/runs_routes.py | 366 | A | Low | Low | Low | High | High | Missing path validation on subprocess.run, sync subprocess in async, SSE no try/except |
| P2 | backend/api/routes/batches.py | 139 | A | Low | Low | Low | Medium | Medium | Fire-and-forget asyncio.create_task, partial run creation |
| P2 | backend/api/main.py | 159 | A | Low | Low | Low | **Critical** | Low | Dual config concern: hardcoded DEBUG, CORS *, no auth, print() instead of logger |
| P2 | backend/core/test_flow_service.py | 193 | A | Low | Low | Low | Low | Low | Chinese-only step pattern, silent empty string substitution |
| P2 | backend/utils/excel_parser.py | 262 | C | Low | Medium | Low | Low | Low | 2 C-grade functions |
| P2 | backend/db/repository.py | 402 | A | Medium | Low | Low | Low | Medium | selectinload N+1 on list, no pagination |
| P2 | backend/db/database.py | N/A | C | Low | Medium | Low | Low | Low | init_db C-grade, manual ALTER TABLE, no migration tracking |
| P3 | backend/core/report_service.py | 197 | C | Low | Medium | Low | Low | Low | 1 C-grade function, Optional vs str\|None |
| P3 | backend/core/locator_chain_builder.py | 233 | D | Low | High | Low | Low | Low | D-grade class, but well-structured |
| P3 | backend/api/routes/tasks.py | 159 | A | Low | Low | Low | Low | Low | No pagination, return type mismatch |
| P3 | backend/api/routes/reports.py | 126 | A | Low | Low | Low | Low | Low | Type annotation wrong, lazy import |
| P3 | backend/api/routes/dashboard.py | 97 | C | Low | Medium | Low | Low | Low | 1 C-grade function, 14 sequential queries |
| P3 | backend/api/response.py | 85 | A | Medium | Low | Low | Medium | Low | 85 lines completely unused (dead code) |
| P3 | backend/api/routes/external_assertions.py | 210 | A | Low | Low | Low | High | Low | User-controlled identifiers to getattr, SSRF risk |
| P3 | backend/api/routes/external_data_methods.py | 100 | A | Low | Low | Low | High | Low | Same pattern as external_assertions |
| P3 | backend/api/routes/external_operations.py | 88 | A | Low | Low | Low | Medium | Low | Redundant WEBSERP_PATH check |
| P3 | backend/core/external_module_loader.py | 218 | A | High | Low | Low | Low | Low | 14 module-level globals, globals() dynamic lookup |
| P3 | backend/core/auth_service.py | 116 | A | Low | Low | Low | Low | Low | Token prefix logged, response scope in except |
| P3 | backend/core/account_service.py | 108 | A | Low | Low | Low | Low | Low | Lazy loading, sys.path manipulation |
| P3 | backend/agent/task_progress_tracker.py | 152 | A | Low | Low | Low | Low | Low | Loose keyword matching |
| P3 | backend/utils/logger.py | 96 | A | Low | Low | Low | Low | Low | StructuredLogger, one of 3 logging systems |
| P3 | backend/utils/run_logger.py | 151 | A | Low | Low | Low | Low | Low | RunLogger, one of 3 logging systems |
| P3 | backend/core/cache_service.py | 56 | A | Low | Low | Low | Low | Low | Clean immutable pattern |
| P3 | backend/core/error_utils.py | 69 | A | Low | Low | Low | Medium | Low | Unused asyncio import, cross-cutting error utility |
| P3 | backend/llm/config.py | 272 | A | Low | Low | Low | High | Low | Dual config source (YAML), overlaps with settings.py |
| P3 | backend/config/settings.py | N/A | A | Low | Low | Low | High | Low | Dual config source (.env), LOG_LEVEL unused |

### Frontend Files

| Priority | File | Lines | ESLint Complexity | MAINT-01 | MAINT-02 | MAINT-03 | ARCH-03 | PERF-01 | Risk Justification |
|----------|------|-------|-------------------|----------|----------|----------|---------|---------|-------------------|
| P1 | frontend/src/components/TaskModal/JsonTreeViewer.tsx | 221 | **26** | Low | **Critical** | Low | Low | Low | Highest complexity in codebase (26) |
| P1 | frontend/src/components/TaskModal/TaskForm.tsx | 560 | **24** | Medium | **Critical** | Low | Low | Low | 2nd highest complexity (24), child modal coordination |
| P1 | frontend/src/components/TaskModal/AssertionSelector.tsx | 546 | **16** | Low | High | Low | Low | Low | Complexity 16, exhaustive-deps warning |
| P1 | frontend/src/components/TaskModal/DataMethodSelector.tsx | 829 | **14** | Medium | High | Low | Low | Low | Largest component, 3 high-complexity functions, 5 ESLint errors |
| P1 | frontend/src/hooks/useRunStream.ts | 215 | A | Medium | Low | Low | Low | **Critical** | Unbounded arrays (O(n^2) copy), JSON.parse no try/catch |
| P1 | frontend/src/api/client.ts | 61 | **11** | Low | Medium | Low | Medium | Low | Retry logic linear not exponential, toast accumulation |
| P2 | frontend/src/components/RunMonitor/StepTimeline.tsx | 285 | **14** | Low | High | Low | Low | Low | Complexity 14, array index as key |
| P2 | frontend/src/components/Report/TimelineItemCard.tsx | 247 | **11** | Low | Medium | Low | Low | Low | Complexity 11 |
| P2 | frontend/src/components/RunMonitor/ScreenshotPanel.tsx | 130 | **11** | Low | Medium | Low | Low | Low | Complexity 11 |
| P2 | frontend/src/components/TaskModal/FieldParamsEditor.tsx | 236 | **11** | Low | Medium | Low | Low | Low | Complexity 11 |
| P2 | frontend/src/components/TaskModal/OperationCodeSelector.tsx | 226 | **11** | Low | Medium | Low | Low | Low | Complexity 11 |
| P2 | frontend/src/types/index.ts | 456 | A | Low | Low | Low | Medium | Low | 4x `any` type, must match backend schemas |
| P2 | frontend/src/hooks/useTasks.ts | 135 | A | **High** | Low | Low | Medium | Low | Manual fetch pattern (DRY violation), prefer-const error |
| P2 | frontend/src/hooks/useReports.ts | 93 | A | **High** | Low | Low | Medium | Low | Manual fetch pattern (DRY violation) |
| P2 | frontend/src/hooks/useDashboard.ts | 43 | A | **High** | Low | Low | Medium | Low | Manual fetch pattern (DRY violation) |
| P2 | frontend/src/hooks/useBatchProgress.ts | 68 | A | **High** | Low | Low | Medium | Low | Manual fetch pattern (DRY violation), 2s polling |
| P2 | frontend/src/pages/RunMonitor.tsx | 132 | A | Low | Low | Low | Low | Low | set-state-in-effect ESLint error |
| P2 | frontend/src/pages/ReportDetail.tsx | 114 | A | Low | Low | Low | Low | Low | set-state-in-effect ESLint error |
| P2 | frontend/src/pages/Tasks.tsx | 211 | A | Low | Low | Low | Low | Low | Client-side pagination |
| P2 | frontend/src/pages/TaskDetail.tsx | 174 | A | Low | Low | Low | Low | Low | Multi-panel layout |
| P2 | frontend/src/components/TaskDetail/CodeViewerModal.tsx | 175 | A | Low | Low | Low | Low | Low | set-state-in-effect ESLint error |
| P2 | frontend/src/api/reports.ts | 172 | A | Low | Low | Low | Low | Low | Largest API module |
| P2 | frontend/src/components/TaskList/TaskRow.tsx | 140 | A | Low | Low | Low | Low | Low | Interactive element with selection state |
| P3 | frontend/src/components/shared/StatusBadge.tsx | 35 | A | Low | Low | Low | Low | Low | react-refresh error, mixed exports |
| P3 | frontend/src/App.tsx | 42 | A | High | Low | Low | Low | Low | React Query installed but completely unused by any hook |
| P3 | All other P3 files (20+ files) | ~2,800 | A | Low | Low | Low | Low | Low | Clean, no significant findings |

## Cross-Reference Map

The following maps findings from Phase 125, 126, and 127 to Phase 128 requirement categories (MAINT-01, MAINT-02, MAINT-03, ARCH-03, PERF-01). Per D-01, existing findings are referenced, not duplicated.

### MAINT-01 (DRY/SOLID Violations) Cross-References

| Finding ID | Phase | Category | Description |
|------------|-------|----------|-------------|
| Cross-2 | 125 | Correctness | Dual stall detection: same StallDetector called twice per step in MonitoredAgent and agent_service |
| P1 agent_service:374-380 | 125 | Correctness | Dual progress tracking: same TaskProgressTracker called in both locations |
| P1 agent_service:294,307 | 125 | Architecture | Fragile attribute setting on BrowserSession -- external object modification |
| P1 step_code_buffer:131-133 | 125 | Performance | Duplicated wait logic between _derive_wait and assemble (6.5s total per click) |
| ARCH-01 run_pipeline | 125 | Architecture | God-module pattern: 13+ module dependencies, orchestrator coupling |
| ARCH-01 batch_execution | 125 | Architecture | Upward dependency: core layer imports from API layer |
| ARCH-01 agent_service<->monitored_agent | 125 | Architecture | Bidirectional knowledge: both files know detector interfaces |
| P2-runs-08 | 126 | Performance | list_runs returns all runs with no pagination |
| P2-tasks-02 | 126 | Performance | list_tasks returns all tasks with no pagination |
| DD-runs-11 | 126 | Performance | subprocess.run synchronous blocking in async context |
| SSE-1 | 127 | Architecture | Backend event fields silently ignored by frontend (wasted computation) |
| App.tsx React Query | 127 | Architecture | React Query installed and configured but completely unused by all 4 hooks |
| useTasks/useReports/useDashboard/useBatchProgress | 127 | Architecture | All 4 hooks use identical manual useState+useEffect+fetch pattern instead of React Query |
| QS-01 | 128 | Maintainability | Error handling: 3+ distinct patterns across backend files (non_blocking_execute, raw try/except, bare operations) |
| QS-02 | 128 | Maintainability | Logging: 3 different logging systems (getLogger, StructuredLogger, RunLogger) used across backend |
| QS-03 | 128 | Maintainability | Frontend hooks: 4 hooks with copy-paste fetch pattern (useState + useEffect + fetch + error toast) |

### MAINT-02 (Structural Complexity) Cross-References

| Finding ID | Phase | Category | Description |
|------------|-------|----------|-------------|
| P1 code_generator.py | 125 | Security | PlaywrightCodeGenerator.generate -- only F-grade (radon cc), most complex backend function |
| P1 run_pipeline:510 | 125 | Correctness | run_pipeline.py -- 3 C-grade functions, 576-line orchestrator |
| P3 action_translator:378 | 125 | Architecture | action_translator.py -- 2 C-grade functions, 718 lines, ambiguous `l` variable |
| P1 agent_service:400-413 | 125 | Performance | agent_service.py -- 2 C-grade functions, synchronous DOM serialization |
| P2 precondition_service:243 | 125 | Security | precondition_service.py -- 378 lines, exec() with full builtins |
| P3 external_execution_engine:325 | 125 | Correctness | external_execution_engine.py -- 3 C-grade functions, 700 lines |
| DD-USE-04 | 127 | Performance | useRunStream.ts steps/timeline O(n^2) copy cost per step |
| ESLint JsonTreeViewer | 128 | Maintainability | JsonNode function complexity 26 (highest in frontend) |
| ESLint TaskForm | 128 | Maintainability | TaskForm function complexity 24 (2nd highest) |
| ESLint DataMethodSelector | 128 | Maintainability | DataMethodSelector 3 functions at 13-14 complexity |
| radon external_method_discovery | 128 | Maintainability | 4 C-grade functions in 669-line file |

### MAINT-03 (Misleading Names) Cross-References

| Finding ID | Phase | Category | Description |
|------------|-------|----------|-------------|
| P2 assertion_service:88-110 | 125 | Correctness | check_element_exists always returns True -- name implies DOM check, behavior is completion check (stub) |
| P3 pre_submit_guard:109-114 | 125 | Correctness | PreSubmitGuard.check() -- name implies active guard, behavior is unconditional pass-through (dead code) |
| P1 monitored_agent:113-114 | 125 | Correctness | _execute_actions -- name implies action execution only, also runs detectors and trackers |
| P3 action_translator:378 | 125 | Architecture | Variable `l` -- ambiguous, confusable with `1` |
| P3 report_service:6 | 125 | Architecture | Uses `Optional[Report]` instead of `Report \| None` (project convention) |
| DD-ext-data-03 | 126 | Architecture | external_data_methods.py uses `Optional[str]` instead of `str \| None` |
| P1 step_code_buffer:63 | 125 | Architecture | Calls `ActionTranslator._identify_action_type` -- private method from different class |
| DD-USE-07 | 127 | Architecture | started handler ignores task_name -- handler name suggests using all started fields |
| QS-04 | 128 | Maintainability | Inconsistent naming: mix of get_/fetch_/load_ for same operation type across files |

### ARCH-03 (Cross-Cutting Consistency) Cross-References

| Finding ID | Phase | Category | Description |
|------------|-------|----------|-------------|
| P2 precondition_service:243 | 125 | Security | exec() with __builtins__ -- error handling strategy varies (exec vs non_blocking_execute vs raw try) |
| P2 precondition_service:59 | 125 | Architecture | nest_asyncio.apply() modifies global event loop policy |
| P2 event_manager:27 | 125 | Performance | EventManager._events never cleaned up -- cleanup() exists but never called |
| P2 event_manager:84-85 | 125 | Correctness | Heartbeat task overwritten on re-subscribe -- old task leaks |
| DD-main-02 | 126 | Security | Hardcoded DEBUG logging ignores LOG_LEVEL setting -- dual config impact |
| DD-main-06 | 126 | Architecture | print() in lifespan bypasses structured logging |
| API-08 | 126 | Architecture | Response format inconsistency: 3 different patterns across routes |
| DD-pipe-05 | 126 | Architecture | 5 unused imports in pipeline orchestrator |
| P3-resp-01 | 126 | Architecture | response.py: 85 lines of completely unused code (success_response, error_response, ErrorCodes) |
| DD-USE-01 | 127 | Correctness | All 7 JSON.parse in useRunStream lack try/catch -- error handling gap |
| DD-USE-02 | 127 | Correctness | isConnected state set true before EventSource confirms connection |
| QS-05 | 128 | Architecture | Configuration dual source: Settings (.env) vs LLMConfig (YAML), 2 files read different sources |
| QS-06 | 128 | Architecture | Error handling: non_blocking_execute used in 4 files, raw try/except in 20+ files, no consistent pattern |

### PERF-01 (Async Performance) Cross-References

| Finding ID | Phase | Category | Description |
|------------|-------|----------|-------------|
| P1 agent_service:127 | 125 | Performance | save_screenshot: synchronous write_bytes in async method blocks event loop |
| Cross-3 | 125 | Performance | Synchronous I/O in async context (screenshots) |
| P1 agent_service:400-413 | 125 | Performance | DOM serialization and hashing on every step (synchronous) |
| P1 monitored_agent:141-146 | 125 | Performance | asyncio.sleep(3) after every file upload (excessive unconditional wait) |
| P1 monitored_agent:179-188 | 125 | Architecture | Duplicate DOM serialization in MonitoredAgent and agent_service |
| P1 step_code_buffer:131-133 | 125 | Performance | Pre-click wait 3000ms misplaced + post-click 3500ms = 6.5s per click in generated code |
| P2 stall_detector:74,100 | 125 | Performance | _history list grows without bounds (mitigated by per-run instances) |
| P2 event_manager:27 | 125 | Performance | _events dict grows indefinitely, cleanup() never called |
| DD-runs-11 | 126 | Performance | subprocess.run synchronous blocking in async context (180s max) |
| SSE-4 | 127 | Performance | Timeline/steps arrays O(n^2) copy cost in useRunStream |
| QS-07 | 128 | Performance | Unbounded collections: event_manager._events, useRunStream.steps/timeline, stall_detector._history |
| QS-08 | 128 | Performance | Sync I/O patterns in async: write_bytes (screenshots), subprocess.run (pytest), write_text (code gen) |

## Quick-Scan Findings

### [QS-01] Backend error handling: 3+ distinct patterns across files (MAINT-01/ARCH-03)
- **Severity:** Medium
- **Category:** Maintainability, Architecture
- **Description:** Error handling uses at least 3 different strategies: (1) `non_blocking_execute()` from error_utils.py (used in ~4 files: run_pipeline, agent_service, code_generator, report_service), (2) raw `try/except Exception` blocks (~20+ files), (3) bare operations with no error handling (many route handlers). The `error_utils.py` utilities were introduced in Phase 124 (v0.11.0) but only partially adopted. Files like `external_execution_engine.py` and `event_manager.py` use raw try/except even though they contain optional operations that could benefit from `non_blocking_execute`. The response.py helpers (`success_response`, `error_response`, `ErrorCodes`) are completely unused (See 126-FINDINGS.md #P3-resp-01).
- **Recommendation:** Define a clear error handling strategy: use `non_blocking_execute` for optional operations, raw try/except for business-critical paths. Remove unused response.py or adopt it.

### [QS-02] Backend logging: 3 different systems across files (ARCH-03)
- **Severity:** Medium
- **Category:** Architecture
- **Description:** The backend uses three logging approaches: (1) `logging.getLogger(__name__)` -- the standard Python pattern, used in most files (~25+), (2) `StructuredLogger` from `utils/logger.py` -- provides JSONL formatting, used in ~3 files, (3) `RunLogger` from `utils/run_logger.py` -- run-specific file logging, used in ~2 files. Additionally, `main.py` uses `print()` for startup messages (See 126-FINDINGS.md #DD-main-06) and sets `logging.DEBUG` globally (See 126-FINDINGS.md #DD-main-02). There is no documented guidance on when to use which logger. The StructuredLogger is defined but barely used, suggesting it was an aspirational improvement that was not adopted.
- **Recommendation:** Standardize on one primary logging approach per CONVENTIONS.md. Define when StructuredLogger vs standard getLogger is appropriate. Remove print() usage.

### [QS-03] Frontend hooks: 4 identical manual fetch patterns (MAINT-01)
- **Severity:** High
- **Category:** Maintainability
- **Description:** See 127-FINDINGS.md #App.tsx-React-Query. All 4 data-fetching hooks (useTasks, useReports, useDashboard, useBatchProgress) use the same boilerplate pattern: `useState` for data/loading/error, `useEffect` for triggering fetch, `useCallback` wrapping an async fetch function. This pattern is duplicated 4 times with minor variations. React Query (`@tanstack/react-query`) is installed and configured in App.tsx but no hook uses it. This is the most significant DRY violation in the frontend.
- **Recommendation:** Migrate all 4 hooks to React Query's `useQuery` pattern. Eliminates ~200 lines of boilerplate, adds caching/refetch/stale-while-revalidate for free.

### [QS-04] Inconsistent function naming patterns across backend (MAINT-03)
- **Severity:** Low
- **Category:** Maintainability
- **Description:** Function names for similar operations use different verb prefixes without clear convention: `get_settings()` vs `load_config()` for configuration loading; `get_logger()` vs `get_run_logger()` for logger creation; `save_screenshot()` vs `write_text()` for file output; `_run_detectors()` vs `_execute_actions()` for step processing. The Phase 123 naming normalization focused on snake_case compliance but did not address verb consistency.
- **Recommendation:** Define a naming convention for operation types: `get_` for retrieval, `create_` for construction, `execute_` for side-effectful operations, `_run_` for internal pipeline stages.

### [QS-05] Configuration dual source: .env vs YAML with divergent consumers (ARCH-03)
- **Severity:** High
- **Category:** Architecture
- **Description:** Two parallel configuration systems exist: (1) `backend/config/settings.py` reads from `.env` via Pydantic BaseSettings (consumed by run_pipeline.py, main.py, runs_routes.py), (2) `backend/llm/config.py` reads from `config/llm_config.yaml` via YAML (consumed by llm/factory.py). The LLMFactory uses LLMConfig while run_pipeline reads LLM parameters directly from Settings. If LLM parameters diverge between .env and YAML, the agent may use different model/temperature settings than the pipeline expects. CONCERNS.md already documents this as Tech Debt.
- **Recommendation:** Consolidate into a single configuration source. Settings (pydantic-settings) is the better choice since it supports .env and type validation. Remove or deprecate llm_config.yaml.

### [QS-06] Error handling bypass: raw try/except in 20+ files vs error_utils selective adoption (ARCH-03)
- **Severity:** Medium
- **Category:** Architecture
- **Description:** `error_utils.py` provides `non_blocking_execute()` and `silent_execute()` for optional operations (introduced in Phase 124). However, adoption is partial: only 4 files use non_blocking_execute. The remaining 20+ files that perform optional operations use raw try/except with inconsistent error handling. For example, `event_manager.publish()` at line 47 has no error handling for publish failures that could abort the pipeline, while `agent_service._run_detectors` at line 346 wraps detector calls in try/except with logging. This inconsistency means some optional operations silently fail while others log warnings.
- **Recommendation:** Identify all optional operations (publishing SSE events, saving screenshots, detector execution) and consistently apply non_blocking_execute. Document the pattern in CONVENTIONS.md.

### [QS-07] Unbounded in-memory collections across backend and frontend (PERF-01)
- **Severity:** High
- **Category:** Performance
- **Description:** Three unbounded collection patterns identified: (1) Backend `EventManager._events` dict grows indefinitely (See 125-FINDINGS.md #P2-event_manager:27), cleanup() never called. (2) Frontend `useRunStream` steps/timeline arrays grow with O(n^2) copy cost per step (See 127-FINDINGS.md #SSE-4). (3) Backend `StallDetector._history` grows per-run (mitigated by per-run instances, See 125-FINDINGS.md #P2-stall_detector:74). The first two are genuine memory leaks for long-running processes; the third is bounded by run duration. The cross-layer pattern (backend event_manager + frontend useRunStream) is a systemic issue where both layers accumulate data without cleanup.
- **Recommendation:** Backend: call event_manager.cleanup(run_id) in _finalize_run. Frontend: implement max timeline size or use ref-based mutable array. StallDetector: add cap at 1000 entries as defense-in-depth.

### [QS-08] Sync I/O in async context across 3 backend locations (PERF-01)
- **Severity:** Medium
- **Category:** Performance
- **Description:** Three locations perform synchronous blocking I/O in async context: (1) `agent_service.save_screenshot` calls `write_bytes()` synchronously (See 125-FINDINGS.md #P1-agent_service:127), (2) `runs_routes._execute_code_background` calls `subprocess.run()` synchronously (See 126-FINDINGS.md #DD-runs-11), (3) `run_pipeline._generate` calls `write_text()` synchronously (wrapped in non_blocking_execute which uses run_in_executor, so this one is correctly handled). Items 1 and 2 block the event loop during I/O, stalling SSE events and concurrent operations.
- **Recommendation:** Replace subprocess.run with asyncio.create_subprocess_exec. Replace write_bytes with await loop.run_in_executor(None, filepath.write_bytes, screenshot_bytes).

### [QS-09] Dead code: response.py 85 lines, PreSubmitGuard core logic, assertion_service stub (MAINT-01)
- **Severity:** Medium
- **Category:** Maintainability
- **Description:** Three significant dead code areas: (1) `api/response.py` defines success_response(), error_response(), and ErrorCodes class -- none are used by any route (See 126-FINDINGS.md #P3-resp-01). (2) `pre_submit_guard.py` check() method has 30+ lines of logic that are unreachable because the caller always passes actual_values=None (See 125-FINDINGS.md #P3-pre_submit_guard:109-114). (3) `assertion_service.py` check_element_exists has zero DOM checking logic, always returns True (See 125-FINDINGS.md #P2-assertion_service:88-110). Combined, these represent ~170 lines of dead or no-op code that misleads readers about actual behavior.
- **Recommendation:** Remove response.py entirely (85 lines). Document PreSubmitGuard as known limitation. Implement or remove check_element_exists stub.

### [QS-10] File size outliers: 6 files exceed 500 lines (MAINT-02)
- **Severity:** Medium
- **Category:** Maintainability
- **Description:** Six backend files exceed the recommended 500-line threshold (per coding-style.md: files should be <800 lines, 200-400 typical): dom_patch.py (777), action_translator.py (718), external_execution_engine.py (700), external_method_discovery.py (669), agent_service.py (658), run_pipeline.py (576). On the frontend, 4 files exceed 500 lines: DataMethodSelector.tsx (829, exceeds 800), TaskForm.tsx (560), AssertionSelector.tsx (546), types/index.ts (456). The backend files are primarily in the core and agent layers; the frontend files are all TaskModal components.
- **Recommendation:** DataMethodSelector.tsx (829) exceeds the 800-line hard limit and should be split. Backend files at 700+ lines could benefit from extraction of utility functions or sub-modules.

### [QS-11] ContextWrapper mutable shared state across pipeline stages (MAINT-01)
- **Severity:** Low
- **Category:** Maintainability
- **Description:** See 125-FINDINGS.md #P2-precondition_service:72-73. ContextWrapper holds mutable _data dict that flows from precondition execution through external assertions to variable_map construction. State from one stage is visible to all subsequent stages. The context mutation at run_pipeline.py:325 (setting external_assertion_summary) is a case where stage-specific data leaks into the shared context. This pattern is intentional for data passing but creates coupling between pipeline stages.
- **Recommendation:** Acceptable for current use. If stage isolation becomes important, use separate dicts per stage with explicit merge.

### [QS-12] ESLint 7x no-explicit-any in types/index.ts and DataMethodSelector.tsx (ARCH-03)
- **Severity:** Low
- **Category:** Architecture
- **Description:** See 127-FINDINGS.md #ESLint-Scan. TypeScript files have 7 instances of explicit `any` type: types/index.ts lines 91, 334, 339, 353 (4 instances in SSE event types and schema definitions) and DataMethodSelector.tsx lines 92, 321 (2 instances in external method data) and externalDataMethods.ts line 26. These `any` types bypass TypeScript's type safety for API responses and external method data.
- **Recommendation:** Define proper interfaces for external method responses. Replace `any` with specific types or `Record<string, unknown>` with runtime validation.

### [QS-13] 5 unused imports in run_pipeline.py orchestrator (MAINT-01)
- **Severity:** Low
- **Category:** Maintainability
- **Description:** See 125-FINDINGS.md #P1-run_pipeline:7,14,19,29 and 126-FINDINGS.md ruff results. The pipeline orchestrator has 5 unused imports (asyncio, HTTPException, TaskRepository, StepRepository, TaskUpdate) left over from the Phase 124 file split. These clutter the import section and mislead readers about dependencies.
- **Recommendation:** Remove all 5 unused imports. Trivial fix.

### [QS-14] step_code_buffer cross-class private method call (MAINT-03)
- **Severity:** Low
- **Category:** Maintainability
- **Description:** See 125-FINDINGS.md #P1-step_code_buffer:63. step_code_buffer.py calls `ActionTranslator._identify_action_type()` -- a private method (underscore prefix) of a different class. This violates encapsulation. If ActionTranslator refactors internal methods, this call breaks silently.
- **Recommendation:** Make _identify_action_type a public static method or extract to a module-level utility function.

### [QS-15] client.ts retry is linear (1s, 2s, 3s) not exponential as documented (ARCH-03)
- **Severity:** Medium
- **Category:** Architecture
- **Description:** See 127-FINDINGS.md #DD-CLI-01. The apiClient retry logic implements linear backoff (1s, 2s, 3s) despite CONVENTIONS.md documenting "exponential backoff (3 retries: 1s, 2s, 3s)" for the frontend client. The documentation describes the actual behavior correctly (1,2,3 is linear), but the intent may have been exponential (1,2,4). Additionally, the retry logic uses recursive control flow that causes toast notifications to persist after a successful retry, and there is no maximum retry count enforced -- the recursion depth is bounded only by the retry array length.
- **Recommendation:** Implement true exponential backoff (1s, 2s, 4s) or document the linear strategy as intentional. Fix toast persistence on retry success.

## Cross-Cutting Systemic Issues

### Error Handling Strategy
- **Pattern count:** 3 distinct strategies (non_blocking_execute, raw try/except, bare operations)
- **File coverage:** non_blocking_execute in 3 files (run_pipeline, runs_routes, error_utils); raw try/except in 28 files (95 total try: blocks); HTTPException in 9 files; raise_not_found in 4 files; bare operations in ~5 files
- **Consistency score:** Low -- error_utils.py helpers are selectively applied, not consistently adopted
- **See also:** QS-01, QS-06

### Logging Strategy
- **System count:** 3 different systems (getLogger, StructuredLogger, RunLogger) + print() in 2 files (main.py, validators.py)
- **File coverage:** getLogger(__name__) in 21 files; StructuredLogger in 2 files (logger.py, utils/__init__.py -- definition only, no active consumers found); RunLogger in 2 files (agent_service.py, run_logger.py); print() in 2 files
- **Consistency score:** Low -- StructuredLogger has zero consumers in application code (only defined and re-exported), no documented guidance on which logger to use when
- **See also:** QS-02, 126-FINDINGS.md #DD-main-06

### Configuration Management
- **Dual source impact:** get_settings() consumed by 10 files; LLMConfig/load_config consumed by 3 files (llm/config.py, llm/__init__.py, account_service.py); overlap in LLM parameters between settings.py and llm_config.yaml
- **Files affected:** settings.py, llm/config.py, llm/factory.py, run_pipeline.py, main.py, account_service.py
- **Consistency score:** Low -- two configuration sources with overlapping scope
- **See also:** QS-05, CONCERNS.md "Duplicated LLM configuration paths"

### Frontend State Management
- **Pattern count:** 1 pattern repeated 4 times (manual useState+useEffect+fetch)
- **Installed but unused:** React Query (@tanstack/react-query v5, ~40KB bundle size)
- **DRY violation:** ~200 lines of identical boilerplate across 4 hooks (useTasks, useReports, useDashboard, useBatchProgress)
- **See also:** QS-03, 127-FINDINGS.md #App.tsx-React-Query

### Async Blocking I/O
- **Instance count:** 2 confirmed sync I/O in async context (save_screenshot write_bytes in agent_service.py, subprocess.run in runs_routes.py)
- **1 correctly handled:** run_pipeline write_text via non_blocking_execute (run_in_executor wrapper)
- **Unbounded .append() patterns:** 22 files use .append() on long-lived collections; key concerns are event_manager._events, stall_detector._history, and useRunStream steps/timeline
- **Event loop impact:** Screenshots block 100KB-1MB writes, subprocess blocks up to 180 seconds
- **See also:** QS-07, QS-08, 125-FINDINGS.md #Cross-3, 126-FINDINGS.md #DD-runs-11

## Backend P1 Deep-Dive (MAINT-01/MAINT-02/MAINT-03)

### run_pipeline.py (576 lines, 3 C-grade functions)

#### [BD-01] SRP violation: 6 distinct concerns in orchestrator file
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** run_pipeline.py handles 6 distinct concerns: (1) LLM config resolution (get_llm_config/get_code_gen_llm_config, lines 51-72), (2) precondition execution (_run_preconditions, lines 75-129), (3) authentication/session management (_run_auth_and_session, lines 132-189), (4) assertion execution (_run_ui_assertions + _run_external_assertions + _publish_external_assertion_results, lines 192-337), (5) code generation orchestration (_run_code_generation, lines 340-381), (6) agent lifecycle (run_agent_background + _create_on_step + _finalize_run, lines 384-576). See 125-FINDINGS.md god-module analysis. NEW: The 6 extracted helper functions improved readability but the file still imports 16 symbols (lines 7-38), exceeding the typical module cohesion threshold.
- **Recommendation:** Extract LLM config functions to `backend/llm/config_helpers.py`. Extract assertion pipeline functions (_run_ui_assertions, _run_external_assertions, _publish_external_assertion_results) to a new `backend/core/assertion_pipeline.py`. This would reduce run_pipeline.py to ~300 lines focused purely on orchestration.

#### [BD-02] Repeated SSE publish pattern (event string construction)
- **Severity:** Medium
- **Category:** Maintainability (MAINT-01)
- **Description:** The SSE publish pattern `await event_manager.publish(run_id, f"event: {type}\ndata: {event.model_dump_json()}\n\n")` is repeated 9 times across the file (lines 99, 109, 123-124, 219, 257-258, 266-267, 333-334, 420, 467, 573). Each call manually constructs the SSE format string with f-string concatenation. The event_manager.publish API accepts a raw SSE string but does not provide a typed helper for constructing events.
- **Recommendation:** Add `event_manager.publish_event(run_id, event_type, event_data: BaseModel)` that handles SSE format construction internally. This eliminates 9 instances of format string duplication.

#### [BD-03] Duplicated login JS logic between agent_service and code_generator
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** The JavaScript code for filling login forms (account input via nativeInputValueSetter, password input, button click detection) is duplicated between `agent_service.py` (_fill_login_form, lines 153-218) and `code_generator.py` (_build_login_helper, lines 345-432). Both files contain nearly identical JS snippets: `document.querySelector('input[placeholder="请输入账号"]')`, `Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set`, and `document.querySelectorAll('button')` iteration for login button detection. The code_generator version produces output as Python string lines; the agent_service version executes directly. Any fix to the login logic (e.g., new ERP UI version) requires updating both files.
- **Recommendation:** Extract login JS templates to a shared module (e.g., `backend/agent/login_js.py`) with parameterized templates. agent_service would execute the template directly; code_generator would emit the template as string literals.

#### [BD-04] _sanitize_variables duplicates JSON-serialization check logic
- **Severity:** Low
- **Category:** Maintainability (MAINT-01)
- **Description:** `_sanitize_variables` (lines 43-48) manually checks `isinstance(v, (str, int, float, bool, list, dict, type(None)))` to filter out non-serializable values. This is a simplified version of JSON serialization filtering. A more robust approach would use `json.dumps` with a default handler or `Pydantic` model serialization, but the current implementation works for the known value types.
- **Recommendation:** Low priority. Accept for now. If more complex types appear in precondition variables, replace with `json.dumps(value, default=str)` approach.

#### [BD-05] C-grade functions: complexity from multi-branch pipeline stages
- **Severity:** Medium
- **Category:** Maintainability (MAINT-02)
- **Description:** Three functions grade C on radon cc: `run_agent_background` (the orchestrator), `_run_preconditions` (precondition loop with early return), and `_publish_external_assertion_results` (assertion result iteration with SSE+DB). The orchestrator's complexity comes from the 6-stage pipeline: preconditions -> auth -> agent -> UI assertions -> external assertions -> finalize + codegen. Each stage modifies `final_status` and `global_seq` through mutable counters. The 13-line try block (lines 517-567) with 6 sequential awaits is the primary complexity driver.
- **Recommendation:** Extract the try block body into `_execute_agent_pipeline()` that returns (final_status, context_for_codegen). This would make run_agent_background a thin wrapper of stage calls, reducing its complexity to A-grade.

### agent_service.py (658 lines, 2 C-grade functions)

#### [BD-06] SRP violation: 5 distinct concerns
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** AgentService handles 5 distinct concerns: (1) browser session creation and lifecycle (create_browser_session, run_with_streaming, run_with_cleanup, lines 47-658), (2) login form filling (_click_password_login_tab, _fill_login_form, _verify_login_success, _programmatic_login, pre_navigate, lines 130-318), (3) screenshot management (save_screenshot, lines 98-128), (4) browser state extraction and DOM hashing (_extract_browser_state, lines 386-414), (5) detector orchestration with step callback (_run_detectors, _extract_agent_output, _create_step_callback, lines 320-533). Concerns 2 and 3 could be extracted to separate services.
- **Recommendation:** Extract login logic to `backend/core/auth_navigator.py` (login is a distinct workflow unrelated to agent step processing). Extract screenshot logic to `backend/utils/screenshot.py` (pure utility with no agent dependencies).

#### [BD-07] DOM hash computation duplicated between agent_service and monitored_agent
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** See 125-FINDINGS.md Cross-2 for original discovery. NEW quantification: `hashlib.sha256(dom_str.encode('utf-8')).hexdigest()[:12]` appears at agent_service.py:406 and monitored_agent.py:184-186. Both locations call `dom_state.llm_representation()` then hash the result. The duplication means any change to the hash algorithm or representation format must be updated in two places.
- **Recommendation:** Extract to a shared `compute_dom_hash(dom_state) -> str` function in `backend/agent/dom_utils.py`. Both consumers should call this function.

#### [BD-08] Dual stall detection call: same StallDetector.check() invoked twice per step
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** See 125-FINDINGS.md Cross-2. StallDetector.check() is called from both MonitoredAgent.step_callback (monitored_agent.py:191-196) AND AgentService._run_detectors (agent_service.py:340-344). Both calls happen on every step with the same arguments. This doubles the stall detection count, causing the stall threshold to trigger at half the configured value. This is a correctness issue that was classified as an Architecture concern in Phase 125. From a MAINT-01 perspective, the two call sites mean the detection logic is coupled across two files.
- **Recommendation:** Remove one of the two call sites. The MonitoredAgent.step_callback is the correct location (it has direct access to the agent). The AgentService._run_detectors call is redundant.

#### [BD-09] C-grade functions: _run_detectors and _extract_agent_output
- **Severity:** Medium
- **Category:** Maintainability (MAINT-02)
- **Description:** `_run_detectors` (agent_service.py:320-384) complexity comes from 3 sequential detector blocks: stall detection (lines 339-347), failure mode detection (lines 349-368), and progress tracking (lines 374-380), all wrapped in try/except. `_extract_agent_output` (agent_service.py:417-447) complexity comes from 4 attribute checks with hasattr on agent_output (evaluation_previous_goal, memory, next_goal). Both functions are at C-grade (11-20 complexity).
- **Recommendation:** _run_detectors: Extract failure mode detection block (lines 349-368) to `_detect_failure_mode()`. _extract_agent_output: Use a list comprehension to collect non-None attributes instead of sequential hasattr checks.

#### [BD-10] _create_step_callback is 70-line closure with 5 concerns
- **Severity:** Medium
- **Category:** Maintainability (MAINT-02)
- **Description:** The step callback closure (agent_service.py:465-532) handles 5 sequential operations: (1) browser state extraction (line 467), (2) agent output extraction (line 470), (3) multi-action interacted_element extraction (lines 473-498), (4) screenshot saving (lines 513-516), (5) detector execution (lines 518-525), (6) external on_step call (lines 528-532). The interacted_element extraction block (lines 480-497) has 4 levels of nesting with try/except inside a for loop inside an if block.
- **Recommendation:** Extract interacted_element extraction (lines 473-498) to `_extract_action_dicts(agent_output, selector_map) -> list[dict]`. This reduces the closure to sequential calls.

#### [BD-11] Misleading name: _execute_actions does more than execute actions
- **Severity:** Medium
- **Category:** Maintainability (MAINT-03)
- **Description:** See 125-FINDINGS.md P1-monitored_agent:113-114. MonitoredAgent._execute_actions (monitored_agent.py:87-146) name implies action execution only, but it also runs PreSubmitGuard checks and adds an async sleep for file uploads. The method has 3 distinct behaviors: guard check, action execution, and post-upload wait. The name suggests it is a thin override of the parent method.
- **Recommendation:** Rename to `_execute_actions_with_guards` or `_run_step_with_monitors` to reflect the full behavior.

#### [BD-12] Misleading name: run_with_cleanup does not perform resource cleanup
- **Severity:** Medium
- **Category:** Maintainability (MAINT-03)
- **Description:** `AgentService.run_with_cleanup` (agent_service.py:607-658) name suggests resource cleanup (closing browser, releasing connections). In reality, it only wraps run_with_streaming with try/finally for logging. The docstring says "guaranteed cleanup logging" but the method name `run_with_cleanup` implies resource cleanup. No resources are actually cleaned up -- browser-use Agent handles browser lifecycle internally.
- **Recommendation:** Rename to `run_with_logging` or `run_tracked` to reflect actual behavior.

#### [BD-13] Private attribute mutation on external BrowserSession object
- **Severity:** Medium
- **Category:** Maintainability (MAINT-03)
- **Description:** See 125-FINDINGS.md P1-agent_service:294,307. agent_service.py sets `browser_session._pre_navigated = True` (lines 294, 307) on BrowserSession, an external class from browser-use. The underscore prefix indicates it is a private attribute. Setting it from outside the class violates encapsulation and depends on browser-use's internal implementation remaining stable. This is also a MAINT-03 concern because `_pre_navigated` is not documented as a public API.
- **Recommendation:** Track pre-navigation state internally in AgentService rather than mutating the BrowserSession. Pass the flag through the method signature or store it as `self._pre_navigated`.

### code_generator.py (553 lines, F-grade generate function)

#### [BD-14] F-grade generate() function: 190-line code assembly with 8 conditional blocks
- **Severity:** Critical
- **Category:** Maintainability (MAINT-02)
- **Description:** `PlaywrightCodeGenerator.generate` (code_generator.py:69-281) is the only F-grade function in the backend (radon cc > 40). The function builds a Python test file as a list of strings through 8 sequential conditional blocks: (1) assertions import (lines 101-104), (2) re import for url_contains (lines 107-110), (3) logging import (lines 112-116), (4) precondition imports (lines 118-123), (5) HealerError class (lines 126-137), (6) random function definitions (lines 139-159), (7) _get_data helper (lines 146-159), (8) _assert_external helper (lines 162-179), plus login helper injection, variable substitution, and assertion code generation. The function mixes string manipulation (parts.append) with conditional logic and regex processing. Adding a new assertion type requires modifying this function directly (Open/Closed violation).
- **Recommendation:** Refactor generate() into smaller methods: `_collect_imports()`, `_build_helpers()`, `_build_function_body()`. For the Open/Closed violation, create a registry pattern for assertion type handlers: `_ASSERTION_BUILDERS = {"url_contains": _translate_url_contains, ...}` so new types can be added without modifying generate().

#### [BD-15] Open/Closed violation: adding assertion types requires modifying generate()
- **Severity:** Medium
- **Category:** Maintainability (MAINT-01)
- **Description:** Adding a new assertion type (e.g., "status_code" or "response_time") requires modifying 3 places in code_generator.py: (1) the imports section to add any needed imports, (2) the `_build_assertions` method to add the elif branch, and (3) a new `_translate_*` method. The assertion type dispatch is a hardcoded elif chain (lines 468-479). This violates Open/Closed principle.
- **Recommendation:** Create an assertion handler registry: `_ASSERTION_BUILDERS: dict[str, Callable[[str], list[str]]]`. Each handler is a standalone function. New assertion types register without modifying existing code.

#### [BD-16] _build_login_helper returns 82-line list literal
- **Severity:** Medium
- **Category:** Maintainability (MAINT-02)
- **Description:** `_build_login_helper` (code_generator.py:345-432) returns a list of 82 Python code strings. The function is essentially a template that produces ~40 lines of generated Python code. The template is embedded as string literals with complex JavaScript inside f-strings. This makes it hard to read, test, and modify. The JavaScript template code duplicates agent_service.py login logic (see BD-03).
- **Recommendation:** Move the login template to a separate `.py.template` file or use Python's string.Template for cleaner parameterized code generation.

### step_code_buffer.py (414 lines)

#### [BD-17] Cross-class private method call: ActionTranslator._identify_action_type
- **Severity:** Low
- **Category:** Maintainability (MAINT-03)
- **Description:** See 125-FINDINGS.md P1-step_code_buffer:63 and QS-14. step_code_buffer.py calls `ActionTranslator._identify_action_type(action_dict)` at lines 63 and 275 -- a private method (underscore prefix) from a different class. This violates encapsulation. If ActionTranslator refactors internal methods, this call breaks silently.
- **Recommendation:** Make `_identify_action_type` a public `@staticmethod` named `identify_action_type` or extract to a module-level utility function in action_utils.py.

#### [BD-18] Mutable counters dict passed by reference through pipeline
- **Severity:** Low
- **Category:** Maintainability (MAINT-03)
- **Description:** run_pipeline.py creates `counters = {"step_count": 0, "global_seq": global_seq}` (line 514) and passes it to `_create_on_step`. The closure mutates `counters["step_count"]` and `counters["global_seq"]` directly (lines 396-397). This pattern uses a mutable dict as a shared state workaround -- it works but is non-obvious. A reader unfamiliar with Python closure semantics may not realize the dict is shared state.
- **Recommendation:** Use an explicit dataclass `PipelineCounters` with mutable fields, making the shared state pattern explicit and type-safe.

### monitored_agent.py (227 lines)

#### [BD-19] create_step_callback duplicates detector calls from agent_service
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** monitored_agent.py's `create_step_callback` (lines 148-227) calls stall_detector.check() and task_tracker.check_progress() -- the same calls that agent_service._run_detectors() makes. Both callbacks are active simultaneously during execution: agent_service's step callback is registered via `register_new_step_callback`, AND MonitoredAgent has its own internal callback mechanism. See BD-08 for the dual-call correctness issue. From MAINT-01, this is code duplication.
- **Recommendation:** Remove the detector calls from MonitoredAgent.create_step_callback. All detector orchestration should go through AgentService._run_detectors, which already handles error wrapping and logging.

#### [BD-20] PreSubmitGuard always receives None parameters (dead code in hot path)
- **Severity:** Medium
- **Category:** Maintainability (MAINT-03)
- **Description:** See 125-FINDINGS.md P3-pre_submit_guard:109-114. PreSubmitGuard.check() at monitored_agent.py:109-114 is called with `actual_values=None` and `submit_button_text=None` on every click action. The guard's core logic (field validation) is unreachable because it requires non-None actual_values. The function runs 30+ lines of setup code that always produces `should_block=False`. This is effectively a no-op in the hot path.
- **Recommendation:** Either implement actual value extraction from the DOM (the intended functionality) or remove the PreSubmitGuard call entirely, along with the PreSubmitGuard class.

### dom_patch.py (777 lines, 1 C-grade function)

#### [BD-21] 777-line monkey-patch file with 7 patches on 4 browser-use classes
- **Severity:** Medium
- **Category:** Maintainability (MAINT-01)
- **Description:** dom_patch.py contains 7 monkey-patches on 4 browser-use internal classes: (1) ClickableElementDetector.is_interactive, (2) PaintOrderRemover.calculate_paint_order, (3) DOMTreeSerializer._should_exclude_child, (4) DOMTreeSerializer._assign_interactive_indices_and_mark_new_nodes, (5-7) DOMTreeSerializer.serialize_tree (3 patches merged). The file has 20+ helper functions, 6 module-level mutable globals (_failure_tracker, _node_annotations, etc.), and complex DOM traversal logic. See CONCERNS.md "Monkey-patching browser-use internals" for the fragility concern. From MAINT-01, the file mixes ERP-specific business logic (IMEI detection, placeholder matching) with browser-use patch mechanics.
- **Recommendation:** Separate concerns: (1) `dom_patch_core.py` for monkey-patch application and lifecycle, (2) `erp_table_detector.py` for ERP-specific detection logic (_is_textual_td_cell, _detect_row_identity, _is_erp_table_cell_input). This would make the ERP logic testable independently of browser-use.

#### [BD-22] Module-level mutable globals with manual reset functions
- **Severity:** Medium
- **Category:** Maintainability (MAINT-03)
- **Description:** dom_patch.py uses 4 module-level mutable globals: `_failure_tracker` (dict), `_node_annotations` (dict), `_discovered_placeholders` (list), `_diagnostic_log_emitted` (bool). These are reset by `reset_failure_tracker()` and `_reset_node_annotations()` which use `global` statements. The reset is called from `apply_dom_patch()` (lines 550-551) but only when `_PATCHED` is already True (re-subscription case). This means the reset functions serve dual purpose: clearing state between runs and being called from external code. The naming `reset_failure_tracker` implies it only resets the tracker, but `_reset_node_annotations` also clears `_discovered_placeholders` and `_diagnostic_log_emitted`.
- **Recommendation:** Encapsulate all mutable state in a `DomPatchState` class with a single `reset()` method. Replace module-level globals with a module-level instance.

### external_execution_engine.py (700 lines, 3 C-grade functions)

#### [BD-23] Mixed abstraction levels: assertion execution + field discovery + operation parsing
- **Severity:** Medium
- **Category:** Maintainability (MAINT-01)
- **Description:** external_execution_engine.py handles 3 distinct concerns at different abstraction levels: (1) high-level assertion/data method execution (execute_assertion_method, execute_all_assertions, execute_data_method, lines 147-358), (2) low-level AST parsing for field discovery (ParamDictVisitor, parse_assertions_field_py, lines 509-627), (3) source code parsing for operation discovery (_parse_operation_line, _parse_operations_from_source, lines 379-451). The file grew from the original external_precondition_bridge.py split but the concerns are not cleanly separated. The field discovery functions use AST parsing while the execution functions use runtime introspection.
- **Recommendation:** Split into 3 modules: (1) `external_assertion_executor.py` for assertion execution, (2) `external_field_discovery.py` for AST-based field parsing, (3) `external_operation_parser.py` for operation code parsing.

#### [BD-24] execute_data_method has 2 fallback lookups that duplicate method resolution
- **Severity:** Medium
- **Category:** Maintainability (MAINT-01)
- **Description:** `execute_data_method` (external_execution_engine.py:294-358) performs method resolution in 3 stages: (1) direct getattr at line 325, (2) docstring-based lookup via `_build_docstring_method_map` at line 328, (3) second `_build_docstring_method_map` call at line 341 for error reporting. The docstring map is built up to twice per method call, even when the first getattr succeeds. The `_build_docstring_method_map` function scans all classes and methods, which is expensive.
- **Recommendation:** Cache the docstring method map (it's already cached at module level in external_method_discovery.py). Avoid building it twice on failure paths.

### Cross-File DRY Analysis

#### [BD-25] Login JS template duplicated between agent_service and code_generator
- **Severity:** High
- **Category:** Maintainability (MAINT-01)
- **Description:** (Cross-reference BD-03 for per-file analysis.) The JavaScript code for ERP login form filling is duplicated across 2 files: agent_service.py (executed at runtime) and code_generator.py (emitted as generated code). Both contain the same querySelector patterns for account/password inputs and button detection. Total duplicated JS code: ~80 lines across 2 files. This is the most significant DRY violation in the backend.
- **Recommendation:** Extract to shared login JS templates in `backend/agent/login_js.py`.

#### [BD-26] Mutable dict closures used in 3 pipeline files for state passing
- **Severity:** Medium
- **Category:** Maintainability (MAINT-03)
- **Description:** Three mutable dict closures are used for state passing in the pipeline: (1) `counters = {"step_count": 0, "global_seq": global_seq}` in run_pipeline.py:514, (2) `step_stats_data = {"value": None}` in agent_service.py:564, (3) `_prev_dom_hash_data = {"value": None}` in agent_service.py:565. These dicts are passed to closures and mutated by side effect. The pattern is consistent across files, suggesting an implicit convention. Using dataclasses would be more explicit.
- **Recommendation:** Replace with typed dataclasses: `PipelineCounters`, `StepStats`, `DomHashState`.

---
*Phase 128-01 breadth scan complete. Tool results, risk matrix, and cross-reference map produced.*
*Phase 128-02 Task 1: Backend P1 Deep-Dive MAINT-01/MAINT-02/MAINT-03 complete.*
