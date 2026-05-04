# Phase 129: Test Scenario Planning - Findings

**Review Date:** 2026-05-04
**Scope:** Derivation of test scenarios from Phase 125-128 code review findings (~286 actionable findings)
**Methodology:** Filter-classify-score pipeline (per D-01, D-02, D-06)
**Input Sources:** 125-FINDINGS.md (32 actionable), 126-FINDINGS.md (78 actionable), 127-FINDINGS.md (95 actionable), 128-FINDINGS.md (72 actionable)

## Methodology

### Stage 1 -- Filter

For each finding from Phase 125-128, the filter applies one question:

> "If this bug reappeared after a refactor, would an automated test catch it before production?"

**KEEP criteria** (high regression protection value):
- Correctness bugs with specific input/output expectations
- Error handling gaps at I/O boundaries
- State mutation leaks between pipeline stages
- Race conditions (heartbeat overwrite, partial creation)
- Performance regressions with measurable thresholds (blocking I/O, unbounded growth)
- Security vulnerabilities exploitable via specific payloads (path traversal, SSRF)

**EXCLUDE criteria** (near-zero regression risk):
- Unused imports (ruff catches these automatically)
- Naming issues (l -> loc, Optional -> pipe syntax)
- Dead code removal (response.py, StructuredLogger -- fix once)
- Missing type annotations (no behavior change)
- Documentation issues
- Architecture concerns without specific behavior violations (god-module, SRP)
- One-time fixes that cannot regress

**BORDERLINE** (judged per case):
- Architecture issues: KEEP only when specific behavior is testable (e.g., "dual stall detection halves threshold")
- Security issues: KEEP when a testable attack payload exists
- Configuration issues: KEEP when settings should control behavior

### Stage 2 -- Classify

For each testable finding, assign one test type per D-03:
- `unit`: Pure logic, no external deps (StallDetector, schemas, parsers, pure functions)
- `integration`: Requires DB, API, or mocked external services (repository CRUD, pipeline stages, SSE event flow)
- `frontend-component`: Frontend component/hook tests (useRunStream, TaskForm, client.ts)
- `e2e`: Requires full stack running (user workflows)

### Stage 3 -- Score by ROI

```
ROI = Severity x Regression_Risk / Implementation_Cost
```

- **Severity**: Critical=4, High=3, Medium=2, Low=1 (from original finding)
- **Regression Risk**: High=3 (mutable state, shared instances, cross-module coupling), Medium=2 (multi-branch logic), Low=1 (isolated pure functions)
- **Implementation Cost**: Low=1 (pure functions, no mocks), Medium=2 (DB tests, simple mocks), High=3 (async/browser-dependent, complex setup)

ROI ranges: 0.22 (Low/Low/High) to 12.0 (Critical/High/Low). Sorted descending.

## Statistics

### By Source Phase

| Source Phase | Actionable Findings | Testable | Not Testable | Testable % |
|-------------|-------------------|----------|-------------|-----------|
| Phase 125 (backend core) | 32 | 14 | 18 | 44% |
| Phase 126 (API layer) | 78 | 18 | 60 | 23% |
| Phase 127 (frontend) | 95 | 13 | 82 | 14% |
| Phase 128 (code quality) | 72 | 22 | 50 | 31% |
| **Total** | **277** | **67** | **210** | **24%** |

Note: The ~277 count excludes N/A/verified-correct/informational entries from the original totals. The 24% testable rate is within the RESEARCH.md sanity check range (20-30%).

### By Severity

| Severity | Total Actionable | Testable | Not Testable |
|----------|-----------------|----------|-------------|
| High | 21 | 15 | 6 |
| Medium | 113 | 38 | 75 |
| Low | 143 | 14 | 129 |
| **Total** | **277** | **67** | **210** |

### By Test Type

| Test Type | Count | Notes |
|-----------|-------|-------|
| unit | 24 | Pure logic, no mocks needed |
| integration | 25 | DB/API/mocked services |
| frontend-component | 13 | Component/hook tests |
| e2e | 5 | Full-stack workflows |
| **Total** | **67** | |

### By ROI Score Range

| ROI Range | Count | Typical Content |
|-----------|-------|----------------|
| 6.0 - 12.0 (highest) | 12 | High severity, high regression risk, low implementation cost |
| 3.0 - 5.9 (high) | 23 | High/Medium severity, moderate risk |
| 1.5 - 2.9 (medium) | 22 | Medium severity, moderate risk/cost |
| 0.2 - 1.4 (lower) | 10 | Low severity or high implementation cost |

## Testable Findings Summary

Sorted by ROI descending. Each entry includes: finding ID, source phase, severity, test type, ROI score, and description.

### Backend Unit Tests (24 scenarios)

| # | Finding ID | Source | Severity | ROI | Test Scenario |
|---|-----------|--------|----------|-----|---------------|
| 1 | BD-08 / Cross-2 | 125/128 | High | 9.0 | **StallDetector dual invocation halves threshold.** Verify calling check() twice per step causes intervention at half configured threshold. Test: N failures recorded once -> assert intervention at N; N failures recorded twice -> assert intervention at N/2. Pure logic, no mocks. |
| 2 | assertion_service:88 | 125 | High | 9.0 | **check_element_exists stub returns True regardless of selector.** Verify that check_element_exists always returns (True, "", selector) when is_done=True, ignoring the selector parameter. Test: pass invalid/empty selector -> assert True returned. |
| 3 | BD-14 / code_generator:487,496 | 125/128 | Medium | 6.0 | **Unescaped assertion expected values produce invalid generated Python.** Verify that assertion values containing double quotes produce SyntaxError in generated code. Test: pass expected='He said "hello"' -> assert generated code has escaped quotes or validation catches it. |
| 4 | P1 step_code_buffer:227 | 125 | Medium | 6.0 | **Corrective evaluate detection breaks when click intervenes.** Verify _is_corrective_evaluate fails to detect corrective action when a click action exists between the failed input and the corrective evaluate. Test: records [fill(X), click(Y), evaluate(X)] -> assert corrective detection fails. |
| 5 | P3 task_progress_tracker:149 | 125 | Low | 3.0 | **Loose keyword matching marks wrong steps as completed.** Verify that update_from_evaluation marks step as completed when ANY of first 3 words match. Test: step="click submit button", eval="clicking dropdown menu" -> assert false positive match. |
| 6 | BD-15 / code_generator | 128 | Medium | 4.0 | **Adding assertion type requires modifying generate() elif chain (Open/Closed violation).** Test via refactoring: verify a registry-based assertion handler pattern produces same output as hardcoded elif for all existing types. |
| 7 | P1 step_code_buffer:63 | 125/128 | Low | 3.0 | **Cross-class private method call: _identify_action_type.** Verify ActionTranslator._identify_action_type produces correct action types for all known action dictionaries. After refactoring to public method, verify same behavior. |
| 8 | BD-18 / QS-11 | 125/128 | Low | 2.0 | **Mutable dict counters passed by reference.** Verify pipeline counters dict mutation across closure boundaries. Test: step_callback increments counters -> assert correct final values. |
| 9 | QS-04 | 128 | Low | 1.3 | **Inconsistent function naming patterns.** Verify naming convention enforcement (not a code test, but a lint/test check). Exclude from test scenarios -- this is a lint concern. |
| 10 | BD-04 | 128 | Low | 2.0 | **_sanitize_variables filters non-serializable values.** Verify filter correctly keeps str/int/float/bool/list/dict/None and excludes other types. Test: pass set, bytes, custom object -> assert filtered out. |
| 11 | P1 run_pipeline:325 | 125 | Medium | 6.0 | **external_assertion_summary leaks into variable_map.** Verify context['external_assertion_summary'] passes the variable_map filter. Test: set key in context -> build variable_map -> assert key not present OR filter catches it. |
| 12 | P2 precondition_service:72 | 125 | Low | 2.0 | **ContextWrapper shared mutable state across stages.** Verify that mutation in one stage (external_assertion_summary) is visible in subsequent stages. Test: set key in stage 1 -> read in stage 2 -> assert visible. |
| 13 | P3 external_module_loader:17 | 125 | Low | 2.0 | **14 module-level globals with globals() dynamic access.** Verify reset_cache() properly resets all cache variables. Test: load module -> set cache -> reset -> assert all None. |
| 14 | P2 precondition_service:59 | 125 | Low | 1.3 | **nest_asyncio.apply() modifies global event loop.** Verify calling apply() multiple times is idempotent. Test: call twice -> assert no exception. |
| 15 | QS-12 | 128 | Low | 2.0 | **ESLint 7x no-explicit-any in types/index.ts.** Verify TypeScript compilation passes after replacing `any` with proper types. Test: change types -> tsc --noEmit -> assert zero errors. |
| 16 | BD-16 | 128 | Medium | 4.0 | **_build_login_helper returns 82-line list literal.** Verify login helper output is syntactically valid Python. Test: call _build_login_helper -> ast.parse -> assert no SyntaxError. |
| 17 | BD-22 | 128 | Medium | 4.0 | **Module-level mutable globals in dom_patch with manual reset.** Verify reset functions properly clear all state. Test: apply patch -> modify state -> reset -> assert clean. |
| 18 | BD-17 | 128 | Low | 2.0 | **Cross-class private method call in step_code_buffer.** Same as #7 -- verify after refactoring to public method. |
| 19 | P2 test_flow_service:116 | 125 | Low | 3.0 | **Missing cache key silently replaced with empty string.** Verify {{cached:NONEXISTENT}} is replaced with empty string (not error). Test: pass missing key -> assert empty string + warning logged. |
| 20 | P2 test_flow_service:59 | 125 | Low | 2.0 | **Step number pattern only handles Chinese format.** Verify regex matches Chinese steps and rejects non-Chinese formats. Test: "Step 1:" -> assert no match. |
| 21 | BD-24 | 128 | Medium | 4.0 | **execute_data_method builds docstring map twice on failure.** Verify method resolution falls back correctly. Test: pass unknown method -> assert second lookup attempted -> assert proper error. |
| 22 | P1 step_code_buffer:131 | 125 | Medium | 6.0 | **Pre-click wait 3000ms misplaced before click.** Verify _derive_wait returns 3000ms for click actions. Test: pass click action -> assert wait_before=3000. |
| 23 | P1 step_code_buffer:380 | 125 | Medium | 6.0 | **Post-click networkidle always hits 3s timeout for non-navigation clicks.** Verify assemble adds networkidle wait for every click. Test: single click record -> assert generated code has networkidle check. |
| 24 | BD-14 | 128 | Critical | 12.0 | **F-grade generate() function -- 190-line code assembly.** Verify generate() produces valid Python for all assertion types (url_contains, text_exists, no_errors, element_exists). Test: each assertion type -> ast.parse output -> assert valid. |

### Backend Integration Tests (25 scenarios)

| # | Finding ID | Source | Severity | ROI | Test Scenario |
|---|-----------|--------|----------|-----|---------------|
| 25 | CP-1 / BD-39 / event_manager:27 | 125/128 | High | 6.0 | **EventManager._events never cleaned up.** Verify cleanup(run_id) removes all stored events. Verify cleanup is called after run completes. Test: publish events -> cleanup -> assert _events[run_id] empty. |
| 26 | CP-2 / BD-27 | 125/128 | High | 6.0 | **event_manager.publish has no error handling.** Verify publish does not crash on broken subscriber queue. Test: add subscriber -> corrupt queue -> publish -> assert no exception, other subscribers still receive. |
| 27 | BD-35 / Cross-3 | 125/128 | High | 6.0 | **save_screenshot sync write_bytes blocks event loop.** Verify screenshot write does not block concurrent async operations. Test: start screenshot write + concurrent SSE publish -> assert SSE not delayed (requires asyncio timing). |
| 28 | BD-36 / DD-runs-11 | 126/128 | High | 6.0 | **subprocess.run blocks event loop for 180s.** Verify code execution does not block concurrent requests. Test: start code execution + make concurrent API request -> assert concurrent request completes during execution. |
| 29 | BD-08 / Cross-2 | 125 | High | 3.0 | **Dual stall detection in agent_service and MonitoredAgent.** Integration test: create agent with StallDetector -> run 2 steps -> assert detector.check called twice per step. Mock the browser-use agent, verify actual call count. |
| 30 | P1 run_pipeline:499 | 125 | Medium | 4.0 | **Precondition failure skips "started" SSE event.** Verify event sequence when preconditions fail: precondition events -> finished(failed) -> None. Test: failing precondition -> subscribe to events -> assert no "started" event received. |
| 31 | DD-runs-05 | 126 | Medium | 4.0 | **Screenshot FileResponse with unvalidated database path.** Verify path validation prevents directory traversal. Test: set screenshot_path to "../../etc/passwd" -> assert 403 or validation error. |
| 32 | API-01 / DD-runs-06 | 126 | High | 3.0 | **Code execution endpoint missing path validation.** Verify _validate_code_path is called before subprocess.run. Test: set generated_code_path to "/etc/passwd" -> assert 403 or validation error. |
| 33 | DD-batch-03 | 126 | Medium | 4.0 | **Partial run creation on task_id validation failure.** Verify batch creation is atomic. Test: valid + invalid task_ids -> assert no runs created (rollback). |
| 34 | DD-runs-04 | 126 | Medium | 4.0 | **SSE event_generator has no try/except/finally.** Verify client disconnect during SSE stream does not crash server. Test: connect to stream -> disconnect immediately -> assert server still responds to new requests. |
| 35 | DD-batch-01 | 126 | Medium | 4.0 | **Fire-and-forget asyncio.create_task with no error callback.** Verify batch startup failures are logged. Test: pass invalid config -> assert error logged (not silently swallowed). |
| 36 | DD-runs-10 | 126 | Medium | 4.0 | **Stop run updates status but does not cancel agent.** Verify agent continues after stop request. Test: start run -> stop -> assert agent task still running. Documents known limitation. |
| 37 | CP-4 / BD-35 / BD-36 | 125/126/128 | Medium | 3.0 | **Sync I/O in async context: write_bytes + subprocess.run.** Verify both operations block the event loop. Test: measure event loop responsiveness during write_bytes -> assert blocked. |
| 38 | BD-40 / event_manager:84 | 125/128 | Medium | 4.0 | **Heartbeat task overwritten on re-subscribe without cancellation.** Verify re-subscribe creates orphaned heartbeat task. Test: subscribe -> subscribe again -> assert old task cancelled (currently fails). |
| 39 | DD-ext-assert-01 | 126 | Medium | 3.0 | **class_name/method_name flow to getattr() without validation.** Verify unknown class/method combinations are rejected at route level. Test: pass invalid class_name -> assert 400 (currently 500). |
| 40 | DD-ext-assert-02 | 126 | Medium | 3.0 | **api_params dict SSRF via external assertion methods.** Verify api_params with URL to internal resource is handled. Test: pass api_params with http://169.254.169.254 -> assert blocked or logged (currently allowed). |
| 41 | P2 assertion_service:88 | 125 | High | 6.0 | **check_element_exists stub -- integration with run_pipeline.** Verify assertion results always show "passed" for element_exists type regardless of DOM state. Test: run pipeline with element_exists assertion targeting non-existent element -> assert passed (demonstrates stub behavior). |
| 42 | P1 run_pipeline:543 | 125 | Medium | 4.0 | **Variable substitution via _variable_map construction.** Verify variable map correctly filters assertion-prefixed keys and includes precondition variables. Test: set context with known keys -> build variable_map -> assert correct content. |
| 43 | BD-41 | 128 | Medium | 4.0 | **Unawaited coroutine in batch_execution fire-and-forget.** Verify batch task exception is logged. Test: create batch with failing config -> assert exception logged via done callback (currently swallowed). |
| 44 | P1 agent_service:484 | 125 | Medium | 4.0 | **Potential IndexError when accessing agent_output.action[i].** Verify multi-action step with filtered actions produces correct element mapping. Test: agent returns 3 actions (1 empty) -> assert correct element for action 2 and 3. |
| 45 | DD-pipe-03 | 126 | Medium | 4.0 | **Precondition failure missing "started" SSE event.** Same as #30 -- integration test verifying SSE event sequence. |
| 46 | P2 precondition_service:243 | 125 | Medium | 3.0 | **exec() with full __builtins__ provides unrestricted runtime.** Verify precondition code can access os, subprocess. Test: exec("import os") -> assert no error (documents current behavior, not a bug fix test). |
| 47 | DD-pipe-06 | 126 | Medium | 3.0 | **Login credentials embedded in task description for LLM.** Verify credentials appear in task description on login fallback path. Test: trigger login fallback -> assert account/password in task_description (documents current behavior). |
| 48 | DD-main-02 | 126 | Medium | 3.0 | **Hardcoded DEBUG logging ignores LOG_LEVEL setting.** Verify LOG_LEVEL setting has no effect. Test: set LOG_LEVEL=WARNING in env -> assert log level still DEBUG. |
| 49 | BD-25 / BD-03 | 125/128 | High | 3.0 | **Login JS template duplicated between agent_service and code_generator.** Verify both files produce identical login JS logic. Test: extract JS from both -> assert string equality (documents duplication for regression protection during fix). |

### Frontend Component Tests (13 scenarios)

| # | Finding ID | Source | Severity | ROI | Test Scenario |
|---|-----------|--------|----------|-----|---------------|
| 50 | SSE-3 / DD-USE-01 / FD-12 | 127/128 | High | 9.0 | **All 7 JSON.parse calls in useRunStream lack try/catch.** Verify malformed SSE event data does not crash the stream. Test: emit event with invalid JSON -> assert error logged, stream continues, no state corruption. |
| 51 | DD-USE-04 / FD-13 | 127/128 | Medium | 4.0 | **Steps/timeline arrays grow with O(n^2) copy cost.** Verify array growth pattern. Test: emit 50 step events -> measure render count -> assert grows linearly with steps (currently O(n^2)). |
| 52 | DD-USE-02 / FD-14 | 127/128 | Medium | 4.0 | **isConnected set true before EventSource confirms connection.** Verify UI shows "connected" immediately after connect() call. Test: connect to unreachable server -> assert isConnected=true initially. |
| 53 | DD-TF-01 / FD-04 | 127/128 | Medium | 6.0 | **TaskForm stale data on edit-to-create mode switch.** Verify form retains old data when switching from edit to create. Test: edit task A -> switch to create mode -> assert form shows task A data (bug). |
| 54 | DD-CLI-01 | 127 | High | 6.0 | **Content-Type application/json set for FormData requests.** Verify file upload sends incorrect Content-Type. Test: upload file via apiClient -> assert Content-Type header is application/json (bug). |
| 55 | DD-CLI-03 | 127 | Medium | 4.0 | **Retry toast persists after successful retry.** Verify loading toast remains visible after retry succeeds. Test: trigger network error -> retry succeeds -> assert loading toast still visible (bug). |
| 56 | DD-DMS-01 / FD-08 | 127/128 | Medium | 4.0 | **Empty numeric input converts to 0.** Verify clearing int/float field shows 0. Test: clear number input -> assert value becomes 0 (bug). |
| 57 | DD-USE-03 | 127 | Medium | 4.0 | **Step handler does not deduplicate by index.** Verify duplicate step index creates duplicate entries. Test: emit two step events with index=3 -> assert two entries in steps array (bug). |
| 58 | DD-USE-09 | 127 | Medium | 4.0 | **external_assertions error-path format shows all-zeros.** Verify error path payload produces "0 total, 0 passed" summary. Test: emit error-path external_assertions event -> assert summary shows all zeros. |
| 59 | DD-TF-03 | 127 | Medium | 4.0 | **Operations loading state persists across precondition rows.** Verify loading spinner shows on all rows during availability check. Test: trigger operations check -> assert spinner on all precondition rows (bug). |
| 60 | FD-17 / QS-03 | 128 | High | 3.0 | **4 identical manual fetch hooks vs React Query unused.** Verify all 4 hooks use identical pattern. Test: grep useState+useEffect+fetch pattern -> assert 4 matches. Protects against partial migration. |
| 61 | DD-AS-02 | 127 | Medium | 4.0 | **Nested setState in AssertionSelector toggleMethod.** Verify state updates are batched correctly. Test: toggle method -> assert selectedKeys, configs, fieldParamsMap all updated in single render. |
| 62 | DD-USE-05 | 127 | Medium | 4.0 | **onerror handler does not handle CONNECTING state.** Verify permanently down server leaves UI "connected". Test: connect to permanently unreachable server -> wait -> assert isConnected stays true (bug). |

### E2E Tests (5 scenarios)

| # | Finding ID | Source | Severity | ROI | Test Scenario |
|---|-----------|--------|----------|-----|---------------|
| 63 | DD-runs-10 | 126 | Medium | 2.0 | **Stop run flow -- status updates but agent continues.** E2E: start run -> click stop -> verify status shows "stopped" -> verify agent still running (backend logs show continued execution). |
| 64 | DD-batch-03 + DD-batch-05 | 126 | Medium | 2.0 | **Batch execution with partial failure and no cancel.** E2E: create batch with mix of valid and invalid tasks -> verify error handling -> verify no cancel endpoint available. |
| 65 | DD-pipe-03 | 125/126 | Medium | 2.0 | **Precondition failure flow -- missing started event.** E2E: create task with failing precondition -> execute -> verify UI shows correct failed state (despite missing started event). |
| 66 | DD-ext-assert-01 | 126 | Medium | 2.0 | **External assertion execution with invalid class/method.** E2E: configure external assertion with non-existent class -> execute -> verify error handling. |
| 67 | P1 run_pipeline:499 | 125 | Medium | 2.0 | **Full pipeline with precondition + assertion + codegen.** E2E: execute task with preconditions, assertions, and code generation -> verify complete pipeline produces report and generated code. |

## Not Testable Findings

Findings excluded from test scenarios with rationale. Grouped by exclusion reason.

### Fix-Once, No Regression Risk (ruff/lint catches)

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| run_pipeline:7,14,19,29 | 125/126/128 | 5 unused imports in run_pipeline.py | ruff F401 catches these; one-time cleanup |
| action_translator:378 (6x) | 125/128 | Ambiguous variable name `l` | E741 catches; cosmetic, no behavior change |
| external_method_discovery:8 | 125 | Unused `ast` import | ruff F401 catches |
| error_utils:8 | 125 | Unused `asyncio` import | ruff F401 catches |
| DD-ext-data-03 | 126 | Optional[str] vs str \| None | Style preference, ruff catches |
| report_service:6 | 125 | Uses Optional instead of pipe syntax | Style preference |
| QS-13 | 128 | 5 unused imports in run_pipeline | Same as above, ruff catches |
| P3-dom_patch mypy | 125 | 9 mypy errors from monkey-patching | Expected per D-03, not fixable |

### Dead Code Removal (test after removal, not before)

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| P3-resp-01 / QS-09 | 126/128 | response.py 85 lines completely unused | Remove entirely; no test needed for dead code |
| BD-33 / QS-02 | 128 | StructuredLogger zero consumers | Dead code; remove and verify nothing breaks |
| BD-31 | 128 | LLMFactory bypassed by create_llm | Dead code; remove after verifying no consumers |
| P3 pre_submit_guard:109 | 125 | Dead core logic (actual_values always None) | Test only after wiring up DOM extraction (deferred) |
| QS-12 (ESLint) | 128 | 7x no-explicit-any in types | Replace `any` -> verify tsc passes; one-time fix |

### Architecture/Design Issues (no specific testable behavior)

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| ARCH-01 run_pipeline | 125 | God-module with 13+ deps | Refactoring concern, no specific behavior to test |
| ARCH-01 batch_execution | 125 | Upward dependency to API layer | Refactoring concern |
| ARCH-01 agent_service<->monitored_agent | 125 | Bidirectional knowledge | Refactoring concern |
| BD-01 | 128 | SRP violation: 6 concerns in run_pipeline | Refactoring concern |
| BD-06 | 128 | SRP violation: 5 concerns in agent_service | Refactoring concern |
| BD-21 | 128 | 777-line dom_patch with 7 monkey-patches | Size concern; individual patches already tested |
| BD-23 | 128 | Mixed abstraction in external_execution_engine | Refactoring concern |
| FD-06 | 128 | DataMethodSelector 829 lines exceeds limit | Refactoring concern |
| FD-03 | 128 | TaskForm SRP violation: 5 concerns | Refactoring concern |
| QS-10 | 128 | 6 files exceed 500 lines | Size concern |
| FD-07 | 128 | Duplicated modal pattern across 3 components | Refactoring concern |
| FD-18 | 128 | Modal layout duplicated across 4+ components | Refactoring concern |

### Documentation/Display Issues

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| DD-USE-07 | 127 | started handler ignores task_name | Display decision, not a bug |
| DD-USE-08 | 127 | finished handler ignores total_steps/duration_ms | Display decision |
| SSE-1 | 127 | Backend event fields silently ignored | Display optimization |
| SSE-5 | 127 | eslint-disable on useEffect deps | Safe per analysis |
| P3 ConfigPanel:39-44 | 127 | Hardcoded "30s/step" display | Display decision |
| P2-TYP-05 | 127 | Run interface mixes SSE and API data | Type design decision |
| DD-CLI-04 | 127 | Retry delay is linear not exponential | Works correctly, just different from documented |

### Response Format / API Consistency (breaking change risk)

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| API-08 | 126 | Response format inconsistency across routes | Would require frontend changes; not a regression risk |
| DD-main-04 | 126 | Returns 400 instead of FastAPI default 422 | Documented deviation, works correctly |
| P2-API-06 | 127 | "Mock" label in runs.ts comment | Cosmetic |
| P2-tasks-01 | 126 | create_task returns ORM Task | Works via response_model, type annotation only |

### Single-User Deployment Accepted

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| DD-main-01 | 126 | CORS allow_origins=["*"] | Single-user internal deployment |
| DD-main-08 | 126 | No auth on any endpoint | Single-user internal deployment |
| DD-main-05 | 126 | Stack traces in 500 responses | Single-user internal deployment |
| Cross-5 | 125 | Credentials in generated test files | Single-user, documented in CONCERNS.md |
| P2 precondition_service:243 | 125 | exec() with full __builtins__ | Single-user, documented in CONCERNS.md |

### console.error / Logging Style

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| DD-main-06 | 126 | print() in lifespan | One-time fix, no regression risk |
| P2-HK-01,05,08 | 127 | console.error in hooks | One-time fix, no regression risk |
| P2-PG-04,07,09 | 127 | console.error in pages | One-time fix, no regression risk |
| P2-CMP-11 | 127 | console.error in TaskRow | One-time fix, no regression risk |
| P3 QuickStart:26 | 127 | console.error | One-time fix |
| QS-02 | 128 | 3 logging systems | Refactoring concern, no regression risk |
| BD-34 | 128 | print() bypasses logging | One-time fix |

### Low-Impact / Cosmetic Issues

| Finding IDs | Source | Description | Rationale |
|-------------|--------|-------------|-----------|
| P3-dom_patch | 125 | Monkey-patch produces mypy errors | Expected, documented |
| P3-prompts | 125 | Backward-compat alias | No behavior change |
| P3-account_service | 125 | Lazy loading with sys.path | Works as designed |
| DD-batch-02,04 | 126 | batch_id format not validated | 404 on invalid, works correctly |
| DD-ext-ops-01 | 126 | Redundant WEBSERP_PATH check | Redundant but harmless |
| DD-ext-ops-03 | 126 | WEBSERP_PATH embedded in API response | Single-user |
| P2-reports-03 | 126 | Lazy import inside handler | Works correctly |
| P2-reports-04 | 126 | Two DB queries for report fallback | Works correctly |
| P3-Pagination:15 | 127 | Renders all page buttons | Works for current scale |
| P3-TrendChart/StatsChart | 127 | Inline style minHeight | Cosmetic |
| P3-BatchTaskCard:83 | 127 | Type assertion on StatusBadge | Works correctly |
| P3-ImageViewer:25 | 127 | DOM download | Works correctly |
| P3-EmptyState:7 | 127 | React.ReactNode inline | Works correctly |
| P2-HK-07 | 127 | setPage(1) redundant re-render | Performance, not regression |
| P2-HK-09 | 127 | refetch not wrapped in useCallback | Performance |
| P2-HK-11 | 127 | eslint-disable on useBatchProgress | Safe per analysis |
| P2-HK-12 | 127 | Interval starts before first fetch | Edge case |
| P2-CMP-02,04,08 | 127 | Array index as key | Works for append-only |
| P2-CMP-05 | 127 | imageLoaded not reset on step change | Edge case |
| P2-PG-08 | 127 | Legacy fallback inline objects | Fallback path, works |
| FD-02 | 128 | Array index key in JsonTreeViewer | Read-only, safe |
| FD-09 | 128 | ESLint exhaustive-deps warnings | Safe per analysis |
| FD-21 | 128 | EventSource cleanup on unmount | Works correctly |
| FD-22 | 128 | useBatchProgress polls when completed | Edge case |
| FD-15 | 128 | Linear backoff documented as exponential | Works correctly |

## Systemic Patterns Cross-Reference

Map of CP-1 through CP-5 to specific testable findings that contribute to each pattern.

### CP-1: Memory Leak -- Unbounded Data Accumulation (High)

**Root cause:** Neither backend nor frontend implements lifecycle-aware cleanup.

| Testable Finding | Test Type | What the Test Verifies |
|-----------------|-----------|----------------------|
| #25 (BD-39 / event_manager:27) | integration | EventManager._events grows without cleanup; cleanup() never called |
| #38 (BD-40 / event_manager:84) | integration | Heartbeat task leak on re-subscribe |
| #51 (FD-13 / SSE-4) | frontend-component | useRunStream steps/timeline O(n^2) copy growth |

**Recommended integration test:** Full pipeline run -> verify cleanup called in _finalize_run -> verify _events empty -> verify no heartbeat tasks remaining.

### CP-2: Error Handling Gap at External Boundaries (High)

**Root cause:** Defensive programming skipped at I/O serialization boundaries.

| Testable Finding | Test Type | What the Test Verifies |
|-----------------|-----------|----------------------|
| #26 (BD-27) | integration | event_manager.publish crashes on broken subscriber |
| #50 (FD-12 / DD-USE-01) | frontend-component | JSON.parse crashes on malformed SSE data |
| #34 (DD-runs-04) | integration | SSE event_generator no try/except on client disconnect |
| #55 (DD-CLI-03) | frontend-component | Retry toast persists after successful retry |

**Recommended integration test:** Publish event with malformed data -> verify both backend (publish continues) and frontend (stream continues, error logged).

### CP-3: Installed-but-Unused Systems (Medium)

**Root cause:** Aspirational improvements not completed; partial adoption leaves dead code.

| Testable Finding | Test Type | What the Test Verifies |
|-----------------|-----------|----------------------|
| #60 (FD-17 / QS-03) | frontend-component | 4 hooks use manual fetch despite React Query installed |
| N/A (QS-09) | -- | response.py, StructuredLogger, LLMFactory dead code (not testable -- remove instead) |

Note: CP-3 is primarily an observation, not a bug. The test (#60) protects against partial migration if React Query adoption begins.

### CP-4: Blocking Operations in Performance-Sensitive Paths (Medium)

**Root cause:** Sync operations in async/render contexts not optimized.

| Testable Finding | Test Type | What the Test Verifies |
|-----------------|-----------|----------------------|
| #27 (BD-35 / Cross-3) | integration | save_screenshot write_bytes blocks event loop |
| #28 (BD-36 / DD-runs-11) | integration | subprocess.run blocks event loop for 180s |
| #37 (CP-4) | integration | Combined blocking I/O measurement |
| #51 (FD-13) | frontend-component | O(n^2) array copy blocks render cycle |

**Recommended integration test:** Start screenshot write + concurrent SSE publish -> measure SSE delivery latency -> assert below threshold.

### CP-5: Mutable State Coupling (Low)

**Root cause:** No explicit state management abstractions.

| Testable Finding | Test Type | What the Test Verifies |
|-----------------|-----------|----------------------|
| #8 (BD-18 / QS-11) | unit | Mutable dict counters passed by reference |
| #12 (precondition_service:72) | unit | ContextWrapper shared mutable state |
| #61 (DD-AS-02) | frontend-component | Nested setState in AssertionSelector |

Note: CP-5 has the lowest priority. The patterns work but are fragile under refactoring. Tests protect against accidental breakage during state management changes.

## Deferred Scenarios

Findings that are testable but require a code fix before tests can be written.

### DEFERRED-1: PreSubmitGuard blocks submit when values differ

- **Source:** 125-FINDINGS P3 pre_submit_guard:109-114, P1 monitored_agent:113-114
- **Severity:** Medium (would be High if functional)
- **Prerequisite:** Wire up DOM value extraction in MonitoredAgent before calling guard.check()
- **Test Scenario:** Verify PreSubmitGuard.check() with actual_values != expected_values returns should_block=True. Currently the core logic is unreachable (actual_values always None).
- **Priority:** Deferred until code fix implements DOM value extraction.

### DEFERRED-2: assertion_service check_element_exists -- implement actual DOM checking

- **Source:** 125-FINDINGS P2 assertion_service:88-110
- **Severity:** High (users get false confidence)
- **Prerequisite:** Implement actual DOM element checking via page.evaluate() before agent session closes
- **Test Scenario:** Verify check_element_exists returns False for non-existent selector. Currently returns True regardless.
- **Note:** Test #2 in unit tests verifies the CURRENT (stub) behavior. A separate test for correct behavior is deferred until implementation.
- **Priority:** Deferred until code fix implements real DOM checking.

### DEFERRED-3: EventManager automatic cleanup integration

- **Source:** 125-FINDINGS P2 event_manager:27, 128 BD-39
- **Severity:** Medium (performance, not correctness)
- **Prerequisite:** Call event_manager.cleanup(run_id) in _finalize_run
- **Test Scenario:** Verify cleanup is called automatically after run completes. Currently cleanup() exists but is never called.
- **Note:** Test #25 verifies manual cleanup works. Automatic cleanup test is deferred until the code fix adds the call.
- **Priority:** Deferred until code fix adds cleanup call to _finalize_run.

### DEFERRED-4: Stop run actually cancels the running agent

- **Source:** 126-FINDINGS DD-runs-10
- **Severity:** Medium (resource waste)
- **Prerequisite:** Implement agent cancellation mechanism (store asyncio.Task reference, call task.cancel())
- **Test Scenario:** Verify agent stops executing after stop request. Currently status updates but agent continues.
- **Note:** Test #63 (E2E) documents current behavior. Cancellation test deferred until mechanism is implemented.
- **Priority:** Deferred until code fix implements cancellation.

### DEFERRED-5: External assertion methods validation against registry

- **Source:** 126-FINDINGS DD-ext-assert-01, DD-ext-data-01
- **Severity:** Medium (security hardening)
- **Prerequisite:** Add route-level validation of class_name/method_name against discovered method registry
- **Test Scenario:** Verify unknown class/method combinations return 400 instead of 500.
- **Note:** Test #39 documents current behavior (500 on unknown). Validation test deferred until route-level check is added.
- **Priority:** Deferred until code fix adds validation.

## Backend Unit Test Scenarios

Detailed expansion of the 24 backend unit test scenarios identified in Plan 01. Each scenario provides enough specificity for implementation without re-reading source FINDINGS files.

### [TS-BE-01] StallDetector double-invocation causes premature stall intervention
- **Severity:** High
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 agent_service.py:340-347 (Cross-2); 128-FINDINGS.md BD-08
- **Description:** Verify that calling `StallDetector.check()` with consecutive failure records triggers `should_intervene=True` at the correct threshold (not at half threshold). The dual-call bug means each actual failure produces TWO history entries, so the configured `max_consecutive_failures=2` triggers after just 1 actual failure.
  - **Test 1 (baseline):** Record N failures once -> assert `should_intervene` fires at exactly N (correct behavior).
  - **Test 2 (bug demo):** Record N failures TWICE (simulating dual invocation) -> assert `should_intervene` fires at N/2 (demonstrates the bug, expected to FAIL until code fix).
  - **Test 3 (reset):** Record N-1 failures, then 1 success, then more failures -> assert counter resets on success and does NOT intervene prematurely.
  - **Test 4 (stagnant DOM):** Record identical dom_hash for max_stagnant_steps, record TWICE per step -> assert stagnant detection triggers at half steps (bug).
- **Priority:** P0 -- High severity correctness bug with high regression risk; pure logic, easy to test
- **Mock requirements:** None (pure logic, no external dependencies)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-02] assertion_service.check_element_exists stub returns True for all inputs
- **Severity:** High
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P2 assertion_service.py:88-110; 128-FINDINGS.md QS-09
- **Description:** Verify that `check_element_exists` always returns `(True, "", selector)` when `history.is_done=True`, regardless of the selector parameter value. This confirms the stub behavior is documented.
  - **Test 1:** Pass valid CSS selector with `is_done=True` -> assert returns `(True, "", selector)`.
  - **Test 2:** Pass empty string selector with `is_done=True` -> assert returns `(True, "", "")`.
  - **Test 3:** Pass `None` as selector with `is_done=True` -> assert returns `(True, "", None)`.
  - **Test 4:** Pass `is_done=False` -> assert returns `(False, ...)` (completion check, not element check).
- **Priority:** P0 -- documents a High-severity stub that gives users false confidence
- **Mock requirements:** Mock `AssertionHistory` with `is_done` attribute
- **Implementation cost:** Low
- **Testability:** Testable now (tests verify current stub behavior; separate test for correct behavior is DEFERRED-2)

### [TS-BE-03] step_code_buffer._is_corrective_evaluate fails when click intervenes between fill and evaluate
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 step_code_buffer.py:227-257
- **Description:** Verify `_is_corrective_evaluate()` detection breaks when a click action exists between a failed input and a corrective evaluate. The search stops at any click/navigate action (line 254), which is too aggressive.
  - **Test 1 (no click):** Records `[fill("name", "John"), evaluate("name", "John")]` -> assert corrective detected (correct).
  - **Test 2 (click intervenes, bug):** Records `[fill("name", "John"), click("other"), evaluate("name", "John")]` -> assert corrective NOT detected (demonstrates bug).
  - **Test 3 (navigate intervenes):** Records `[fill("name", "John"), navigate("url"), evaluate("name", "John")]` -> assert corrective NOT detected.
  - **Test 4 (input intervenes):** Records `[fill("name", "John"), input("age", "25"), evaluate("name", "John")]` -> assert corrective NOT detected.
- **Priority:** P1 -- Medium severity, regression protection for code generation correctness
- **Mock requirements:** None (pure logic with StepRecord objects)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-04] code_generator._substitute_variables false match on short values
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 code_generator.py:241-242 (VERIFIED-OK but false match risk noted)
- **Description:** Verify `_substitute_variables_in_code` uses global string replace (`code.replace(f'"{escaped}"', var_name)`) which could cause false matches when a short fill value appears in multiple `fill()` calls with different semantic meanings.
  - **Test 1 (unique value):** Variable map `{"name": "John"}`, code has `fill("John")` -> assert correctly substituted.
  - **Test 2 (short value collision):** Variable map `{"code": "A"}`, code has `fill("A")` and `fill("Category A")` -> assert BOTH get substituted (false match on "Category A" if it contains "A").
  - **Test 3 (no match):** Variable map `{"name": "John"}`, code has `fill("Jane")` -> assert no substitution.
  - **Test 4 (empty value):** Variable map `{"name": ""}`, code has `fill("")` -> assert substitution or skip.
- **Priority:** P1 -- Medium severity, protects code generation correctness during refactoring
- **Mock requirements:** None (pure string manipulation)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-05] task_progress_tracker.update_from_evaluation false-positive keyword matching
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P3 task_progress_tracker.py:149-152
- **Description:** Verify `update_from_evaluation` marks a step as completed when ANY of the first 3 words from the step description appear in the evaluation text. This loose matching causes false positives.
  - **Test 1 (exact match):** Step "click submit button", evaluation "clicked submit button successfully" -> assert completed (correct).
  - **Test 2 (false positive):** Step "click submit button", evaluation "clicking dropdown menu" -> assert completed (false positive -- shares word "click").
  - **Test 3 (no match):** Step "enter quantity", evaluation "page loaded successfully" -> assert NOT completed (correct rejection).
  - **Test 4 (Chinese text):** Step "填写数量", evaluation "成功填写数量字段" -> assert completed (Chinese keyword matching).
  - **Test 5 (partial word match):** Step "delete record", evaluation "deleted records" -> assert behavior documented.
- **Priority:** P2 -- Low severity, but protects progress tracking accuracy during refactoring
- **Mock requirements:** None (pure logic with step list and evaluation text)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-06] External assertion context mutation leaks into variable_map
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md Cross-4, P1 run_pipeline.py:325; 126-FINDINGS.md DD-pipe-04
- **Description:** Verify that `_run_external_assertions` mutating `context['external_assertion_summary']` leaks past the variable_map filter. The filter `not k.startswith("assertion")` does NOT match keys starting with "external_assertion". Currently mitigated by `isinstance(v, (str, int, float))` guard if the summary is a dict.
  - **Test 1 (dict summary, current behavior):** Context has `{"external_assertion_summary": {"total": 5}}` -> build variable_map -> assert key NOT present (isinstance guard filters dicts).
  - **Test 2 (string summary, latent bug):** Context has `{"external_assertion_summary": "5/10 passed"}` -> build variable_map -> assert key IS present (latent bug, passes isinstance str check).
  - **Test 3 (assertion-prefixed key):** Context has `{"assertion_result_0": "passed"}` -> build variable_map -> assert key NOT present (filter correctly blocks).
  - **Test 4 (normal variable):** Context has `{"order_number": "ORD-001"}` -> build variable_map -> assert key IS present (correct).
- **Priority:** P1 -- Medium severity, latent bug that could surface if summary format changes
- **Mock requirements:** None (pure dict filtering logic)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-07] test_flow_service._shift_step_numbers boundary values
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P2 test_flow_service.py:174-193
- **Description:** Verify `_shift_step_numbers` correctly handles step number boundaries, large offsets, and non-Chinese formats.
  - **Test 1 (normal shift):** "步骤1：Login" with offset=2 -> assert "步骤3：Login".
  - **Test 2 (full-width colon):** "步骤1：Login" -> assert colon preserved.
  - **Test 3 (multi-digit step):** "步骤99：Submit" with offset=5 -> assert "步骤104：Submit".
  - **Test 4 (no steps):** "Plain text without steps" -> assert unchanged.
  - **Test 5 (English format, not matched):** "Step 1: Login" -> assert unchanged (regex only matches Chinese).
  - **Test 6 (negative offset):** "步骤5：Submit" with offset=-2 -> assert "步骤3：Submit" or assert behavior documented.
  - **Test 7 (offset to zero):** "步骤1：Login" with offset=-1 -> assert "步骤0：Login" or edge case behavior.
- **Priority:** P2 -- Low severity, edge case protection
- **Mock requirements:** None (pure regex replacement)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-08] code_generator assertion expected values with special characters produce invalid Python
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 code_generator.py:487,496
- **Description:** Verify assertion values containing double quotes produce SyntaxError in generated code. Lines 487 and 496 embed `expected` values directly into generated f-strings without escaping.
  - **Test 1 (normal value):** expected="Order created" -> assert generated code is valid Python (ast.parse succeeds).
  - **Test 2 (double quote):** expected='He said "hello"' -> assert generated code has broken string literal (ast.parse fails).
  - **Test 3 (backslash):** expected="C:\\Users\\test" -> assert generated code handling of backslashes.
  - **Test 4 (single quote):** expected="It's done" -> assert generated code handling of single quotes.
  - **Test 5 (newline):** expected="Line1\nLine2" -> assert generated code handling of newlines.
- **Priority:** P1 -- Medium severity, protects code generation from user input with special characters
- **Mock requirements:** None (string manipulation + ast.parse validation)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-09] code_generator F-grade generate() produces valid Python for all assertion types
- **Severity:** Critical
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-14 (F-grade function)
- **Description:** Verify `PlaywrightCodeGenerator.generate()` produces syntactically valid Python for all 4 assertion types (url_contains, text_exists, no_errors, element_exists). This is the only F-grade function in the backend and the most complex.
  - **Test 1 (url_contains):** Generate with url_contains assertion -> assert ast.parse succeeds on output.
  - **Test 2 (text_exists):** Generate with text_exists assertion -> assert ast.parse succeeds.
  - **Test 3 (no_errors):** Generate with no_errors assertion -> assert ast.parse succeeds.
  - **Test 4 (element_exists):** Generate with element_exists assertion -> assert ast.parse succeeds.
  - **Test 5 (multiple assertions):** Generate with all 4 types -> assert ast.parse succeeds.
  - **Test 6 (with preconditions):** Generate with precondition variables -> assert variable substitution in output.
  - **Test 7 (with login):** Generate with login config -> assert login helper in output, ast.parse succeeds.
- **Priority:** P0 -- Critical severity, validates the most complex backend function
- **Mock requirements:** Mock Assertion schema objects, mock login_config dict
- **Implementation cost:** Medium (requires constructing test fixtures for each assertion type)
- **Testability:** Testable now

### [TS-BE-10] code_generator Open/Closed violation -- elif chain produces correct output
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-15
- **Description:** Verify that the hardcoded elif chain in `_build_assertions` produces identical output to a hypothetical registry-based approach. This test protects against regressions during the recommended refactoring.
  - **Test 1:** Build assertions for each type via current elif chain -> capture output.
  - **Test 2:** After refactoring to registry pattern, verify same output for all types.
  - **Test 3:** Verify that adding a new assertion type (mock) via registry does not require modifying generate().
- **Priority:** P2 -- Medium severity, refactoring protection
- **Mock requirements:** Mock Assertion objects for each type
- **Implementation cost:** Medium
- **Testability:** Testable now (tests current behavior; documents refactoring goal)

### [TS-BE-11] step_code_buffer pre-click wait is 3000ms (misplaced before click)
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 step_code_buffer.py:131-133
- **Description:** Verify `_derive_wait()` returns 3000ms wait for click actions. This wait is placed BEFORE the click, but async page updates happen AFTER the click. Combined with post-click waits, total is ~6.5s per click.
  - **Test 1 (click action):** Pass click action dict -> assert `wait_before=3000`.
  - **Test 2 (fill action):** Pass fill action dict -> assert `wait_before` is 0 or absent.
  - **Test 3 (navigate action):** Pass navigate action dict -> assert wait behavior.
  - **Test 4 (popup element):** Pass action with popup element -> assert popup-specific wait handling.
- **Priority:** P1 -- Medium severity performance issue in generated code
- **Mock requirements:** None (pure logic with action dictionaries)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-12] step_code_buffer post-click networkidle always hits 3s timeout
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 step_code_buffer.py:380-395
- **Description:** Verify `assemble()` adds a post-click stability action for every click with `wait_for_load_state("networkidle", timeout=3000)`. For non-navigation clicks, network is already idle, so this always times out at 3 seconds.
  - **Test 1 (single click):** One click record -> assert generated code has `wait_for_load_state("networkidle", timeout=3000)` + `wait_for_timeout(500)`.
  - **Test 2 (navigation click):** Click that navigates -> assert networkidle wait is useful (not directly testable in unit test, but verify the code structure).
  - **Test 3 (no clicks):** Fill-only records -> assert no networkidle wait in output.
  - **Test 4 (10 clicks):** 10 click records -> count total wait statements -> assert 10 * (3s + 0.5s) = 35s of waits.
- **Priority:** P1 -- Medium severity, significant performance impact on generated test execution
- **Mock requirements:** None (pure logic with StepRecord list)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-13] _sanitize_variables filters non-serializable values correctly
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-04
- **Description:** Verify `_sanitize_variables` correctly keeps `str/int/float/bool/list/dict/None` and filters out other types.
  - **Test 1 (keep str):** `{"name": "John"}` -> assert kept.
  - **Test 2 (keep int):** `{"count": 42}` -> assert kept.
  - **Test 3 (keep None):** `{"value": None}` -> assert kept.
  - **Test 4 (filter set):** `{"items": {1, 2}}` -> assert filtered out.
  - **Test 5 (filter bytes):** `{"data": b"raw"}` -> assert filtered out.
  - **Test 6 (filter custom object):** `{"obj": object()}` -> assert filtered out.
  - **Test 7 (nested dict):** `{"config": {"key": "val"}}` -> assert kept.
  - **Test 8 (list of str):** `{"items": ["a", "b"]}` -> assert kept.
- **Priority:** P2 -- Low severity, utility function validation
- **Mock requirements:** None (pure type checking)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-14] _build_login_helper produces syntactically valid Python
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-16
- **Description:** Verify `_build_login_helper` returns Python code that is syntactically valid. The function returns an 82-line list literal with complex JavaScript embedded in f-strings.
  - **Test 1:** Call `_build_login_helper(origin="http://erp.test", account="admin", password="pass123")` -> join lines -> assert `ast.parse` succeeds.
  - **Test 2:** Call with special characters in password (`pass"word`) -> assert escaping handles double quotes.
  - **Test 3:** Call with backslash in account (`dom\\admin`) -> assert escaping handles backslashes.
- **Priority:** P1 -- Medium severity, validates code generation correctness
- **Mock requirements:** None (string list construction + ast.parse)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-15] dom_patch reset functions properly clear all state
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-22
- **Description:** Verify dom_patch module-level mutable globals and reset functions properly clear all state. The module uses manual reset of mutable globals.
  - **Test 1:** Apply patches -> call reset function -> assert all state variables return to initial values.
  - **Test 2:** Apply patches -> modify state -> call reset -> assert clean state.
  - **Test 3:** Call reset twice -> assert idempotent (no error, state stays clean).
- **Priority:** P2 -- Medium severity, protects monkey-patch state management
- **Mock requirements:** Requires importing dom_patch module (may need browser-use available)
- **Implementation cost:** Medium
- **Testability:** Testable now (may need browser-use import, which could add complexity)

### [TS-BE-16] execute_data_method builds docstring map twice on failure
- **Severity:** Medium
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-24; 125-FINDINGS.md P3 external_module_loader
- **Description:** Verify method resolution fallback when docstring-based lookup fails. The code builds the docstring map twice on failure -- once during initial lookup, once during fallback.
  - **Test 1 (known method):** Pass known class/method -> assert single lookup, success on first try.
  - **Test 2 (unknown method):** Pass unknown method name -> assert second lookup attempted -> assert proper error message.
  - **Test 3 (wrong class):** Pass unknown class name -> assert error without crash.
- **Priority:** P2 -- Medium severity, validates external method resolution robustness
- **Mock requirements:** Mock external module with known classes/methods
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-17] external_module_loader reset_cache properly resets all 14 globals
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P3 external_module_loader:17-43
- **Description:** Verify `reset_cache()` properly resets all 14 module-level cache variables. The `_lazy_load` function uses `globals()[var_name]` for reading and writing, which is fragile.
  - **Test 1:** Load module -> set cache values -> call `reset_cache()` -> assert all 14 globals are None.
  - **Test 2:** Call `reset_cache()` without prior load -> assert no error, all globals None.
  - **Test 3:** Partial load -> `reset_cache()` -> assert complete reset.
- **Priority:** P2 -- Low severity, cache management validation
- **Mock requirements:** None (module-level state manipulation)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-18] nest_asyncio.apply() is idempotent
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P2 precondition_service:59
- **Description:** Verify calling `nest_asyncio.apply()` multiple times is idempotent and does not raise exceptions. The code calls apply() on every data method execution.
  - **Test 1:** Call `nest_asyncio.apply()` once -> assert no exception.
  - **Test 2:** Call `nest_asyncio.apply()` twice -> assert no exception (idempotent).
  - **Test 3:** Call `nest_asyncio.apply()` 10 times -> assert no exception, event loop still functional.
- **Priority:** P2 -- Low severity, validates async safety assumption
- **Mock requirements:** None (event loop manipulation)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-19] test_flow_service missing cache key silently replaced with empty string
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P2 test_flow_service:116-123
- **Description:** Verify `{{cached:NONEXISTENT}}` is replaced with empty string (not error) when cache key is missing. Silent replacement can mask typos in cache references.
  - **Test 1 (missing key):** Text with `{{cached:order_number}}`, empty cache -> assert replaced with empty string.
  - **Test 2 (existing key):** Text with `{{cached:order_number}}`, cache has `order_number: "ORD-001"` -> assert replaced with "ORD-001".
  - **Test 3 (typo key):** Text with `{{cached:order_nubmer}}`, cache has `order_number` -> assert replaced with empty string (typo silently produces empty).
  - **Test 4 (multiple keys):** Text with `{{cached:a}} and {{cached:b}}`, only `a` in cache -> assert `a` replaced, `b` empty string.
- **Priority:** P2 -- Low severity, documents silent data loss behavior
- **Mock requirements:** None (string replacement with cache dict)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-20] test_flow_service step number pattern only handles Chinese format
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P2 test_flow_service:59-60
- **Description:** Verify regex `_STEP_NUMBER_PATTERN` matches Chinese step format and rejects non-Chinese formats.
  - **Test 1 (Chinese colon):** "步骤1：Login" -> assert match, captures "1".
  - **Test 2 (Chinese full-width colon):** "步骤1：Login" -> assert match.
  - **Test 3 (English "Step 1:"):** "Step 1: Login" -> assert no match.
  - **Test 4 (numbered "1."):** "1. Login" -> assert no match.
  - **Test 5 (hash "#1"):** "#1 Login" -> assert no match.
  - **Test 6 (multi-digit):** "步骤12：Submit" -> assert match, captures "12".
- **Priority:** P2 -- Low severity, documents format limitation
- **Mock requirements:** None (pure regex matching)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-21] ContextWrapper shared mutable state across pipeline stages
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P2 precondition_service:72-73; 128-FINDINGS.md QS-11
- **Description:** Verify that mutation in one pipeline stage (via ContextWrapper) is visible in subsequent stages. This documents intentional shared state behavior.
  - **Test 1:** Create ContextWrapper -> set key in "stage 1" -> read in "stage 2" -> assert value visible.
  - **Test 2:** Set `external_assertion_summary` -> assert it passes through to `to_dict()` output.
  - **Test 3:** Call `reset_assertion_tracking()` -> assert assertion-specific state cleared but other data preserved.
- **Priority:** P2 -- Low severity, documents intentional shared state pattern
- **Mock requirements:** None (dict-like object manipulation)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-22] Mutable dict counters closure behavior
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md BD-18 / QS-11
- **Description:** Verify pipeline counters dict mutation across closure boundaries works correctly. The mutable dict `{"step_count": 0, "global_seq": 0}` is shared between `_create_on_step` closure and the pipeline orchestrator.
  - **Test 1:** Create counter dict -> pass to closure -> increment in closure -> assert outer dict reflects change.
  - **Test 2:** Multiple increments -> assert correct final values.
  - **Test 3:** Counter starts at non-zero (global_seq) -> assert increments add to initial value.
- **Priority:** P2 -- Low severity, documents closure-based state sharing pattern
- **Mock requirements:** None (dict manipulation + closure)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-23] ActionTranslator._identify_action_type cross-class private method call
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 step_code_buffer:63; 128-FINDINGS.md BD-17, QS-14
- **Description:** Verify `ActionTranslator._identify_action_type` produces correct action types for all known action dictionaries. After refactoring to public method, verify same behavior.
  - **Test 1 (click action):** `{"action": "click"}` -> assert type is "click".
  - **Test 2 (fill action):** `{"action": "fill", "value": "text"}` -> assert type is "fill".
  - **Test 3 (evaluate action):** `{"action": "evaluate"}` -> assert type is "evaluate".
  - **Test 4 (empty dict):** `{}` -> assert type is handled (empty or unknown).
  - **Test 5 (unknown action):** `{"action": "custom_new_type"}` -> assert type is handled.
- **Priority:** P2 -- Low severity, refactoring protection
- **Mock requirements:** None (pure logic with action dictionaries)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-24] TypeScript compilation passes after replacing `any` types
- **Severity:** Low
- **Test Type:** Unit
- **Source Finding:** See 128-FINDINGS.md QS-12; 127-FINDINGS.md ESLint Scan
- **Description:** Verify TypeScript compilation (`tsc --noEmit`) passes after replacing `any` types in `types/index.ts`. This is a build-time test, not a runtime test. 7 explicit `any` types exist across `types/index.ts` and `DataMethodSelector.tsx`.
  - **Test 1:** Run `tsc --noEmit` on current code -> assert zero errors (baseline).
  - **Test 2:** Replace `any` with `Record<string, unknown>` for API response types -> assert `tsc --noEmit` still passes.
  - **Test 3:** Define proper interfaces for SSE event types -> assert `tsc --noEmit` passes.
- **Priority:** P2 -- Low severity, type safety improvement validation
- **Mock requirements:** None (TypeScript compiler check)
- **Implementation cost:** Medium (requires running tsc)
- **Testability:** Testable now

## Backend Integration Test Scenarios

Detailed expansion of the 25 backend integration test scenarios identified in Plan 01. Integration tests require database, API client, or mocked external services.

### [TS-BE-25] EventManager lifecycle -- cleanup prevents memory leak across runs (CP-1)
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P2 event_manager.py:27; 128-FINDINGS.md CP-1, QS-07
- **Description:** Verify EventManager cleanup lifecycle prevents unbounded memory growth. `_events` dict accumulates all events per run_id, and `cleanup()` exists but is never called.
  - **Test 1 (manual cleanup):** Subscribe to a run -> publish 10 events -> call `cleanup(run_id)` -> assert `_events[run_id]` is empty or removed.
  - **Test 2 (pipeline cleanup, DEFERRED):** Run full pipeline (mocked agent) -> verify cleanup is called in `_finalize_run`. Currently fails because cleanup is never called. Test for when code fix is applied.
  - **Test 3 (heartbeat cancellation):** Subscribe -> publish events -> cleanup -> assert heartbeat task cancelled and removed from `_heartbeat_tasks`.
  - **Test 4 (re-subscribe after cleanup):** Subscribe -> cleanup -> subscribe again -> assert no stale events from previous subscription.
  - **Test 5 (memory growth measurement):** Publish 1000 events -> assert `_events` memory is bounded (or measure size before/after cleanup).
- **Priority:** P0 -- High severity systemic pattern (CP-1), protects long-running server stability
- **Mock requirements:** Real EventManager instance; mock agent execution for pipeline test
- **Implementation cost:** Medium
- **Testability:** Tests 1,3,4,5 testable now; Test 2 DEFERRED until cleanup is called in _finalize_run

### [TS-BE-26] SSE error handling -- broken subscriber does not crash publisher (CP-2)
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md BD-27; 128-FINDINGS.md CP-2, QS-06
- **Description:** Verify `event_manager.publish` does not crash when a subscriber's queue is broken. The publish method iterates all subscriber queues with no error handling.
  - **Test 1 (broken queue):** Add subscriber -> corrupt its queue (e.g., close it) -> publish event -> assert no exception thrown.
  - **Test 2 (other subscribers receive):** Add 2 subscribers -> break 1 queue -> publish -> assert the intact subscriber still receives the event.
  - **Test 3 (empty subscribers):** Publish to run_id with no subscribers -> assert no error (events stored in _events for history replay).
  - **Test 4 (malformed event data):** Publish event with non-serializable data -> assert error handling (currently no try/except, expected to fail until fix).
- **Priority:** P0 -- High severity systemic pattern (CP-2), protects SSE reliability
- **Mock requirements:** Real EventManager; mock subscriber queues
- **Implementation cost:** Medium
- **Testability:** Tests 1,2,3 testable now; Test 4 documents current behavior (no error handling)

### [TS-BE-27] save_screenshot sync write_bytes blocks event loop (CP-4)
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md BD-35 / Cross-3; 128-FINDINGS.md CP-4, QS-08
- **Description:** Verify screenshot write does not block concurrent async operations. `save_screenshot` calls `filepath.write_bytes(screenshot_bytes)` synchronously.
  - **Test 1 (blocking measurement):** Start screenshot write with 1MB data -> concurrently start SSE publish -> measure SSE delivery latency -> assert not delayed by screenshot.
  - **Test 2 (concurrent screenshots):** Start 2 simultaneous screenshot writes -> assert both complete -> measure total time (if serialized, 2x; if non-blocking, ~1x).
  - **Test 3 (with fix):** After wrapping in `asyncio.to_thread`, verify concurrent operations not delayed.
- **Priority:** P0 -- High severity systemic pattern (CP-4), event loop blocking affects all users
- **Mock requirements:** Real file system write; asyncio timing measurement
- **Implementation cost:** Medium
- **Testability:** Testable now (measures current blocking behavior)

### [TS-BE-28] subprocess.run blocks event loop for 180 seconds (CP-4)
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-runs-11; 128-FINDINGS.md CP-4, QS-08
- **Description:** Verify code execution via `subprocess.run` blocks the event loop for up to 180 seconds, preventing concurrent API requests.
  - **Test 1 (blocking measurement):** Start code execution (long-running test) -> concurrently make API request (e.g., GET /api/dashboard) -> assert API request response time.
  - **Test 2 (concurrent execution):** Start 2 code executions -> assert they run sequentially (not concurrently) due to event loop blocking.
  - **Test 3 (with fix):** After replacing with `asyncio.create_subprocess_exec`, verify concurrent operations proceed during execution.
- **Priority:** P0 -- High severity, blocks entire server during test execution
- **Mock requirements:** FastAPI TestClient; subprocess that runs for known duration
- **Implementation cost:** High
- **Testability:** Testable now (documents current blocking behavior)

### [TS-BE-29] Dual stall detection in full agent pipeline
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md Cross-2, P1 agent_service.py:340-347; 128-FINDINGS.md BD-08, BD-19
- **Description:** Verify that the shared StallDetector instance is called twice per step -- once from MonitoredAgent.step_callback and once from agent_service._run_detectors.
  - **Test 1 (call count):** Create agent with StallDetector -> mock step callback to count detector.check() calls -> run 2 steps -> assert 4 total calls (2 per step).
  - **Test 2 (history inflation):** Create agent -> run steps with failures -> inspect StallDetector._history -> assert each failure appears twice.
  - **Test 3 (threshold halving):** Create agent with max_consecutive_failures=4 -> generate 2 actual failures (but 4 history entries from dual call) -> assert intervention fires (demonstrates threshold halving).
- **Priority:** P1 -- High severity, requires mocking agent internals
- **Mock requirements:** Mock browser-use Agent; real StallDetector; real MonitoredAgent
- **Implementation cost:** High
- **Testability:** Testable now

### [TS-BE-30] Pipeline precondition failure skips "started" SSE event
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P1 run_pipeline.py:499-500; 126-FINDINGS.md DD-pipe-03
- **Description:** Verify SSE event sequence when preconditions fail. The "started" event (line 512) is skipped because precondition failure returns early at line 500.
  - **Test 1 (normal flow):** Run pipeline with passing preconditions -> subscribe to events -> assert "started" event received before "finished".
  - **Test 2 (failing preconditions):** Run pipeline with failing precondition -> subscribe to events -> assert NO "started" event received -> assert "finished" event with status="failed" IS received.
  - **Test 3 (event ordering):** Verify events arrive in correct order for success path: precondition events -> started -> step events -> finished.
- **Priority:** P1 -- Medium severity, UI state confusion risk
- **Mock requirements:** Mock precondition service (success/failure); real EventManager; FastAPI TestClient for SSE stream
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-31] Screenshot FileResponse with unvalidated database path
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-runs-05, API-02
- **Description:** Verify path traversal attack on screenshot endpoint. `step.screenshot_path` from database is served directly as FileResponse without validation.
  - **Test 1 (normal screenshot):** Valid screenshot path -> GET screenshot endpoint -> assert 200 with image data.
  - **Test 2 (path traversal):** Set screenshot_path to `"../../etc/passwd"` in test DB -> GET screenshot endpoint -> assert 403 or validation error (currently serves file, bug).
  - **Test 3 (absolute path):** Set screenshot_path to `/etc/passwd` -> assert 403 (currently serves file).
  - **Test 4 (within outputs/):** Set screenshot_path to valid outputs/ path -> assert 200.
- **Priority:** P1 -- Medium severity security issue (path traversal)
- **Mock requirements:** In-memory SQLite with manipulated screenshot_path; FastAPI TestClient
- **Implementation cost:** Medium
- **Testability:** Testable now (tests document current vulnerable behavior)

### [TS-BE-32] Code execution endpoint missing path validation
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md API-01, DD-runs-06
- **Description:** Verify `_validate_code_path` is NOT called before `subprocess.run` in the execute endpoint. This is the highest-severity security finding.
  - **Test 1 (normal execution):** Valid generated_code_path -> POST execute-code -> assert 200 (test runs).
  - **Test 2 (path traversal):** Set generated_code_path to `"/etc/passwd"` in test DB -> POST execute-code -> assert 403 or validation error (currently executes, critical bug).
  - **Test 3 (with fix):** After adding `_validate_code_path` in endpoint, verify traversal is blocked.
- **Priority:** P0 -- High severity, arbitrary code execution risk
- **Mock requirements:** In-memory SQLite with manipulated generated_code_path; FastAPI TestClient; mock subprocess
- **Implementation cost:** Medium
- **Testability:** Testable now (documents critical security gap)

### [TS-BE-33] Batch execution partial creation on task_id validation failure
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-batch-03
- **Description:** Verify batch creation when some task_ids are invalid. Current implementation creates runs for valid tasks before failing on invalid ones, leaving partial state.
  - **Test 1 (all valid):** Create batch with 3 valid task_ids -> assert 3 runs created, batch links all 3.
  - **Test 2 (partial invalid):** Create batch with 2 valid + 1 invalid task_ids -> assert no runs created (rollback) OR assert partial state documented.
  - **Test 3 (empty list):** Create batch with empty task_ids -> assert validation error.
  - **Test 4 (all invalid):** Create batch with 3 invalid task_ids -> assert 404 error, no batch created.
- **Priority:** P1 -- Medium severity, data integrity concern
- **Mock requirements:** In-memory SQLite with Task records; FastAPI TestClient
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-34] SSE event_generator client disconnect does not crash server
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-runs-04, API-03
- **Description:** Verify client disconnect during SSE stream does not crash the server. The event_generator has no try/except/finally.
  - **Test 1 (normal completion):** Connect to SSE stream -> receive all events -> assert clean disconnect.
  - **Test 2 (early disconnect):** Connect to SSE stream -> disconnect after first event -> assert server still responds to new requests.
  - **Test 3 (rapid connect/disconnect):** Connect and immediately disconnect 10 times -> assert server stable.
  - **Test 4 (reconnect after disconnect):** Disconnect -> reconnect to same run_id -> assert history replay works.
- **Priority:** P1 -- Medium severity, server stability
- **Mock requirements:** FastAPI TestClient with SSE stream support; real EventManager
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-35] Fire-and-forget batch startup failure logging
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-batch-01, API-04; 128-FINDINGS.md BD-41
- **Description:** Verify batch startup failures are logged via done callback. `asyncio.create_task` with no `add_done_callback` means silent failure.
  - **Test 1 (successful batch):** Create valid batch -> assert batch runs start.
  - **Test 2 (failing batch config):** Create batch that fails immediately (mock service.start to raise) -> assert exception logged (currently swallowed).
  - **Test 3 (with fix):** After adding done_callback, verify error appears in logs.
- **Priority:** P1 -- Medium severity, operational visibility
- **Mock requirements:** Mock BatchExecutionService.start to raise; log capture fixture
- **Implementation cost:** Medium
- **Testability:** Testable now (documents current silent failure behavior)

### [TS-BE-36] Stop run does not cancel agent execution
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-runs-10
- **Description:** Verify that calling stop endpoint updates status but does NOT actually cancel the running agent task.
  - **Test 1 (status update):** Start run -> call stop endpoint -> assert run status is "stopped" in database.
  - **Test 2 (agent continues):** Start run -> stop -> assert agent still running (check agent task reference or logs).
  - **Test 3 (resource consumption):** Start run -> stop -> verify LLM API calls continue (currently they do).
  - **Test 4 (with fix, DEFERRED):** After implementing task.cancel(), verify agent actually stops.
- **Priority:** P1 -- Medium severity, resource waste; documents known limitation
- **Mock requirements:** FastAPI TestClient; mock agent that runs for known duration; in-memory SQLite
- **Implementation cost:** Medium
- **Testability:** Tests 1,2,3 testable now; Test 4 DEFERRED until cancellation mechanism implemented

### [TS-BE-37] Combined sync I/O blocking measurement (CP-4)
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 128-FINDINGS.md CP-4, QS-08; 125-FINDINGS.md Cross-3; 126-FINDINGS.md DD-runs-11
- **Description:** Combined measurement of event loop blocking from all sync I/O operations: `write_bytes` (screenshots) + `subprocess.run` (code execution).
  - **Test 1 (screenshot blocking):** Measure event loop responsiveness during 1MB screenshot write -> assert blocked for write duration.
  - **Test 2 (subprocess blocking):** Measure event loop responsiveness during subprocess.run -> assert blocked for subprocess duration.
  - **Test 3 (concurrent with SSE):** Start blocking I/O + SSE publish simultaneously -> measure SSE delivery latency -> assert delayed.
- **Priority:** P1 -- Medium severity, combined performance measurement
- **Mock requirements:** asyncio timing measurement; file write fixture; subprocess fixture
- **Implementation cost:** High
- **Testability:** Testable now (measures current blocking behavior)

### [TS-BE-38] Heartbeat task leak on re-subscribe
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P2 event_manager.py:84-85; 128-FINDINGS.md CP-1
- **Description:** Verify re-subscribing to the same run_id creates an orphaned heartbeat task. The old heartbeat task is overwritten but NOT cancelled.
  - **Test 1 (first subscribe):** Subscribe to run_id -> assert exactly 1 heartbeat task in `_heartbeat_tasks[run_id]`.
  - **Test 2 (re-subscribe):** Subscribe to run_id -> subscribe again -> assert old task cancelled (currently fails, old task leaked).
  - **Test 3 (task count):** Subscribe 5 times to same run_id -> count heartbeat tasks -> assert 1 (currently leaks 4 orphaned tasks).
  - **Test 4 (with fix):** After adding `if run_id in self._heartbeat_tasks: self._heartbeat_tasks[run_id].cancel()`, verify re-subscribe works correctly.
- **Priority:** P1 -- Medium severity, resource leak in reconnection scenarios
- **Mock requirements:** Real EventManager instance
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-39] External assertion unknown class/method returns 500 instead of 400
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-ext-assert-01, API-09
- **Description:** Verify that unknown class_name/method_name combinations flow to `getattr()` without validation, producing a 500 error instead of a 400 validation error.
  - **Test 1 (valid method):** Call with known class/method from external module -> assert 200.
  - **Test 2 (unknown class):** Call with `class_name="NonExistentClass"` -> assert 500 (current) or 400 (desired).
  - **Test 3 (unknown method):** Call with valid class but `method_name="nonexistent_method"` -> assert 500 (current) or 400 (desired).
  - **Test 4 (special chars):** Call with `class_name="__class__"` -> assert behavior is safe (probing risk).
- **Priority:** P1 -- Medium severity, security hardening
- **Mock requirements:** External module available or mocked; FastAPI TestClient
- **Implementation cost:** Medium
- **Testability:** Testable now (documents current 500 behavior)

### [TS-BE-40] External assertion api_params SSRF via HTTP requests
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-ext-assert-02
- **Description:** Verify that `api_params` dict with URLs to internal resources is handled. Currently, user-controlled params flow directly to external methods that may make HTTP requests.
  - **Test 1 (normal params):** Call with valid api_params -> assert 200.
  - **Test 2 (internal URL):** Call with `api_params={"url": "http://169.254.169.254/metadata"}` -> assert behavior documented (currently allowed).
  - **Test 3 (localhost URL):** Call with `api_params={"url": "http://localhost:6379/"}` -> assert behavior documented.
  - **Test 4 (with fix, DEFERRED):** After adding URL allowlisting, verify internal URLs blocked.
- **Priority:** P1 -- Medium severity, SSRF risk for public deployment
- **Mock requirements:** External module with HTTP-calling method; FastAPI TestClient
- **Implementation cost:** High
- **Testability:** Tests 1,2,3 testable now; Test 4 DEFERRED until URL validation added

### [TS-BE-41] assertion_service check_element_exists stub -- integration with pipeline
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P2 assertion_service.py:88-110
- **Description:** Verify assertion results always show "passed" for element_exists type regardless of DOM state. This integration test confirms the stub behavior at the pipeline level.
  - **Test 1 (existing element):** Run pipeline with element_exists assertion targeting real element -> assert passed (stub always returns True).
  - **Test 2 (non-existent element):** Run pipeline with element_exists assertion targeting `".nonexistent-class-xyz"` -> assert PASSED (demonstrates stub always passes, bug).
  - **Test 3 (comparison with text_exists):** Run same test with text_exists assertion targeting non-existent text -> assert behavior differs from element_exists.
- **Priority:** P0 -- High severity, users get false confidence in element existence checks
- **Mock requirements:** Mock agent execution; real assertion_service; real run_pipeline
- **Implementation cost:** Medium
- **Testability:** Testable now (documents critical stub behavior)

### [TS-BE-42] Variable substitution via _variable_map construction
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P1 run_pipeline.py:543; 126-FINDINGS.md DD-pipe-04
- **Description:** Verify variable map correctly filters assertion-prefixed keys and includes precondition variables. Tests the _variable_map construction logic end-to-end.
  - **Test 1 (precondition variables):** Set context with `{"order_number": "ORD-001", "customer": "Acme"}` -> build variable_map -> assert both present.
  - **Test 2 (assertion filtered):** Set context with `{"assertion_result_0": "passed", "order_number": "ORD-001"}` -> assert assertion_result_0 filtered, order_number present.
  - **Test 3 (external_assertion_summary leak):** Set context with `{"external_assertion_summary": "5/10"}` -> assert key IS present (latent bug, passes filter).
  - **Test 4 (non-serializable filtered):** Set context with `{"callback": lambda: None}` -> assert filtered out by isinstance guard.
- **Priority:** P1 -- Medium severity, protects code generation variable substitution
- **Mock requirements:** None (dict construction and filtering logic)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-43] Unawaited coroutine in batch_execution fire-and-forget
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 128-FINDINGS.md BD-41
- **Description:** Verify batch task exception is properly logged when `asyncio.create_task` is used without error callback.
  - **Test 1 (normal batch):** Create valid batch -> assert tasks execute without exception.
  - **Test 2 (exception in task):** Mock batch_execution to raise before first await -> assert "Task exception was never retrieved" warning or assert custom error handling.
  - **Test 3 (with fix):** After adding `add_done_callback`, verify exception logged with useful context.
- **Priority:** P1 -- Medium severity, operational visibility
- **Mock requirements:** Mock BatchExecutionService; asyncio task inspection; log capture
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-44] Potential IndexError when accessing agent_output.action[i] in multi-action steps
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P1 agent_service.py:484
- **Description:** Verify multi-action step with filtered actions produces correct element mapping. The index `i` from `enumerate(all_actions)` diverges from `agent_output.action[i]` when actions are filtered.
  - **Test 1 (no filtering):** Agent returns 3 non-empty actions -> assert all elements mapped correctly.
  - **Test 2 (one empty action):** Agent returns [fill, empty_dict, click] -> extract_all_actions filters to [fill, click] -> assert element mapping for fill uses index 0, click uses index 2 (NOT index 1).
  - **Test 3 (two empty actions):** Agent returns [empty, fill, empty, click] -> assert element mapping uses original indices.
  - **Test 4 (all empty):** Agent returns [empty, empty] -> assert no IndexError.
- **Priority:** P1 -- Medium severity, incorrect locator generation in code output
- **Mock requirements:** Mock agent_output with action list; real extract_all_actions
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-45] Pipeline precondition failure SSE event sequence
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-pipe-03 (duplicate of TS-BE-30 from pipeline perspective)
- **Description:** Integration test verifying SSE event sequence when precondition fails. Focuses on the pipeline's event publishing behavior.
  - **Test 1 (success path events):** Run with passing preconditions -> capture all events -> assert sequence: precondition -> started -> steps -> finished.
  - **Test 2 (failure path events):** Run with failing preconditions -> capture all events -> assert sequence: precondition -> finished(failed) -> assert "started" MISSING.
  - **Test 3 (None sentinel):** Verify None sentinel is the final event in all paths.
- **Priority:** P1 -- Medium severity, SSE event ordering
- **Mock requirements:** Mock precondition service; real EventManager; SSE event capture
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-46] exec() with full __builtins__ provides unrestricted runtime
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P2 precondition_service:243
- **Description:** Verify precondition code can access os, subprocess via full `__builtins__`. Documents current behavior for security awareness.
  - **Test 1 (import os):** Execute `import os; result = os.path.exists(".")` -> assert no error (documents current capability).
  - **Test 2 (subprocess access):** Execute `import subprocess` -> assert no error (documents current capability).
  - **Test 3 (safe operation):** Execute `result = 2 + 2` -> assert result is 4 (normal precondition behavior).
  - **Test 4 (timeout):** Execute infinite loop -> assert 30-second timeout triggers.
- **Priority:** P2 -- Medium severity, documents accepted single-user behavior
- **Mock requirements:** None (real exec() in test environment with timeout)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-47] Login credentials embedded in task description for LLM
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-pipe-06
- **Description:** Verify credentials appear in task description on login fallback path. Documents credential exposure in LLM prompts.
  - **Test 1 (login fallback):** Trigger login fallback path -> capture task_description -> assert account/password strings present.
  - **Test 2 (successful login):** Trigger successful programmatic login -> assert credentials NOT in task_description.
  - **Test 3 (log output):** Trigger login fallback -> capture log output -> assert credentials visible in logs at line 188.
- **Priority:** P2 -- Medium severity, documents credential exposure pattern
- **Mock requirements:** Mock account_service; mock login flow; log capture
- **Implementation cost:** Medium
- **Testability:** Testable now

### [TS-BE-48] Hardcoded DEBUG logging ignores LOG_LEVEL setting
- **Severity:** Medium
- **Test Type:** Integration
- **Source Finding:** See 126-FINDINGS.md DD-main-02
- **Description:** Verify LOG_LEVEL setting has no effect on actual logging level. `main.py:44` hardcodes `logging.DEBUG`.
  - **Test 1 (default):** Start app with default settings -> assert root logger level is DEBUG.
  - **Test 2 (env override):** Set `LOG_LEVEL=WARNING` in env -> assert root logger level is STILL DEBUG (bug).
  - **Test 3 (stack traces):** Set `LOG_LEVEL=ERROR` -> trigger 500 error -> assert stack trace still included in response (bug).
  - **Test 4 (with fix):** After using settings.log_level, assert env override works.
- **Priority:** P1 -- Medium severity, configuration control gap
- **Mock requirements:** Environment variable fixture; FastAPI TestClient
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-BE-49] Login JS template duplicated between agent_service and code_generator
- **Severity:** High
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P1 code_generator.py:487,496; 128-FINDINGS.md BD-03
- **Description:** Verify both files produce identical login JS logic. ~80 lines of login JS are duplicated between `agent_service.py` and `code_generator.py`.
  - **Test 1 (string equality):** Extract JS snippets from both files -> assert string equality (currently they should match).
  - **Test 2 (regression detection):** Modify JS in one file -> assert test detects divergence.
  - **Test 3 (with fix):** After extracting to shared module, verify both consumers produce same output.
- **Priority:** P1 -- High severity DRY violation, protects login logic consistency
- **Mock requirements:** None (string comparison of JS snippets)
- **Implementation cost:** Low
- **Testability:** Testable now

### Backend Scenario Summary

**Total scenarios: 49 (24 unit + 25 integration)**

#### By Severity

| Severity | Unit | Integration | Total |
|----------|------|-------------|-------|
| Critical | 1 | 0 | 1 |
| High | 2 | 8 | 10 |
| Medium | 15 | 16 | 31 |
| Low | 6 | 1 | 7 |
| **Total** | **24** | **25** | **49** |

#### By Priority

| Priority | Unit | Integration | Total |
|----------|------|-------------|-------|
| P0 | 3 | 5 | 8 |
| P1 | 9 | 16 | 25 |
| P2 | 12 | 4 | 16 |
| **Total** | **24** | **25** | **49** |

#### By Testability

| Status | Count | Scenarios |
|--------|-------|-----------|
| Testable now | 47 | All except 2 partially deferred |
| Partially DEFERRED | 2 | TS-BE-25 Test 2 (cleanup call), TS-BE-36 Test 4 (agent cancel) |

#### Top 5 Highest ROI Scenarios

1. **TS-BE-01** StallDetector dual-invocation (P0, High, no mocks, Low cost) -- ROI: pure logic, highest correctness impact
2. **TS-BE-09** F-grade generate() validation (P0, Critical, Medium cost) -- ROI: validates most complex function
3. **TS-BE-26** SSE error handling (P0, High, Medium cost) -- ROI: systemic pattern CP-2, server stability
4. **TS-BE-25** EventManager lifecycle (P0, High, Medium cost) -- ROI: systemic pattern CP-1, memory leak prevention
5. **TS-BE-32** Code execution path validation (P0, High, Medium cost) -- ROI: highest security impact

#### Systemic Pattern Coverage

| Pattern | Integration Scenario | Unit Scenario |
|---------|---------------------|---------------|
| CP-1 Memory leak | TS-BE-25, TS-BE-38 | N/A |
| CP-2 Error handling gap | TS-BE-26, TS-BE-34 | TS-BE-01 (dual detection) |
| CP-3 Installed-but-unused | N/A (observation, not bug) | N/A |
| CP-4 Blocking I/O | TS-BE-27, TS-BE-28, TS-BE-37 | TS-BE-11, TS-BE-12 (generated code waits) |
| CP-5 Mutable state | TS-BE-42 | TS-BE-06, TS-BE-21, TS-BE-22 |

---

*Backend Unit Test Scenarios expanded: 2026-05-04*
*Plan 129-02: Task 1 -- 24 unit test scenarios from Plan 01 inventory*
*Plan 129-02: Task 2 -- 25 integration test scenarios + backend scenario summary*

## Frontend Component Test Scenarios

Detailed expansion of the 13 frontend component test scenarios identified in Plan 01. Each scenario provides enough specificity for implementation without re-reading source FINDINGS files. Note: frontend test framework (vitest + testing-library) is not yet configured; implementation cost reflects this setup overhead.

### [TS-FE-01] useRunStream JSON.parse error handling -- malformed SSE data crashes stream
- **Severity:** High
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-USE-01 (useRunStream.ts:44,59,83,110,126,147,163); 128-FINDINGS.md FD-12, CP-2
- **Description:** Verify all 7 JSON.parse calls in useRunStream handle malformed data gracefully. Currently, malformed JSON causes the exception to propagate to EventSource's listener callback. EventSource catches listener exceptions internally, but the event is silently lost and run state becomes inconsistent -- the `if (!prev) return prev` guard means a malformed `started` event leaves `run` as null, preventing all subsequent updates.
  - **Test 1 (malformed JSON in started event):** Emit `started` event with `data: {invalid json` -> assert error logged, stream continues, no state corruption.
  - **Test 2 (malformed JSON in step event):** After successful `started`, emit `step` event with broken JSON -> assert error logged, run state still has previous steps, stream continues.
  - **Test 3 (missing data field):** Emit event with no `data` field (`e.data` is undefined) -> assert JSON.parse error caught, no crash.
  - **Test 4 (null data field):** Emit event with `data: null` -> assert handled gracefully.
  - **Test 5 (recovery after malformed event):** Emit malformed `step`, then valid `step` -> assert second step processed correctly, run state consistent.
- **Priority:** P0 -- High severity, single malformed event can silently break entire run monitoring
- **Mock requirements:** Mock EventSource to emit custom events; render hook with @testing-library/react-hooks or vitest
- **Implementation cost:** Medium (requires vitest/testing-library setup, EventSource mock)
- **Testability:** Testable now (after framework setup)

### [TS-FE-02] useRunStream unbounded array growth with O(n^2) copy cost
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-USE-04, SSE-4; 128-FINDINGS.md FD-13, CP-1
- **Description:** Verify steps and timeline arrays grow without bound via spread operator. Each append copies the entire array (O(n) per step), causing O(n^2) total copy cost for a full run. For a 50-step test, this produces ~1,275 element copies for steps alone.
  - **Test 1 (array growth):** Emit 50 step events -> measure `run.steps.length` -> assert 50 entries.
  - **Test 2 (O(n^2) copy cost measurement):** Emit N step events, measure total spread operations -> assert cost grows quadratically (not linearly).
  - **Test 3 (cleanup on unmount):** Subscribe, emit events, unmount -> assert arrays reset to initial state on next mount.
  - **Test 4 (large run):** Emit 200 step events -> assert no memory error, arrays contain 200 entries.
- **Priority:** P1 -- Medium severity, performance degradation for long runs; mirrors backend CP-1
- **Mock requirements:** Mock EventSource; render hook; performance measurement utilities
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-03] TaskForm stale data on edit-to-create mode switch
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-TF-01; 128-FINDINGS.md FD-04
- **Description:** Verify form retains old data when switching from edit mode to create mode. The `initialData` useEffect does not reset when `initialData` becomes null, leaving stale data visible.
  - **Test 1 (edit to create):** Render TaskForm with initialData (edit mode, task A data) -> set initialData to null (create mode) -> assert form fields are NOT empty (bug -- stale task A data persists).
  - **Test 2 (create to edit):** Render TaskForm with no initialData (create mode) -> set initialData to task A -> assert form shows task A data (correct).
  - **Test 3 (edit A to edit B):** Render TaskForm with task A initialData -> switch to task B initialData -> assert form shows task B data (correct).
  - **Test 4 (edit to create then back):** Edit task A -> create mode (stale A) -> edit task B -> assert task B data shown (correct, stale A cleared by new initialData).
- **Priority:** P1 -- Medium severity, user creates tasks with wrong data from stale form state
- **Mock requirements:** Render TaskForm component with controlled initialData prop; mock child modal components
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-04] client.ts retry toast persists after successful retry
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-CLI-03; 128-FINDINGS.md QS-15
- **Description:** Verify loading toast with id 'network-retry' remains visible after a successful retry. When retry succeeds on the second attempt, the recursive call at line 49 returns successfully, bypassing the `toast.dismiss('network-retry')` on line 52.
  - **Test 1 (retry succeeds):** Mock fetch to fail once then succeed -> call apiClient -> assert loading toast dismissed on success (currently fails -- toast persists).
  - **Test 2 (retry exhausts):** Mock fetch to fail 4 times (3 retries + initial) -> assert loading toast dismissed, error toast shown.
  - **Test 3 (no retry needed):** Mock fetch to succeed immediately -> assert no loading toast shown.
- **Priority:** P1 -- Medium severity, confusing UX with persistent loading indicator
- **Mock requirements:** Mock fetch/global; toast mock to track show/dismiss calls
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-05] DataMethodSelector empty numeric input converts to 0
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-DMS-01; 128-FINDINGS.md FD-08
- **Description:** Verify clearing an int/float input field immediately shows 0. `parseInt('')` returns NaN, which is converted to 0 via `isNaN(parsed) ? 0 : parsed`. The same pattern exists in AssertionSelector.
  - **Test 1 (clear int field):** Type "42" in int input -> clear field -> assert displayed value is "0" (bug -- should be empty).
  - **Test 2 (clear float field):** Type "3.14" in float input -> clear field -> assert displayed value is "0" (bug).
  - **Test 3 (intentional 0):** Type "0" -> assert value is "0" (correct, but indistinguishable from cleared field).
  - **Test 4 (negative number):** Type "-5" -> assert value is "-5" (correct).
- **Priority:** P1 -- Medium severity, confusing UX for numeric parameter entry
- **Mock requirements:** Render DataMethodSelector component; mock API responses for method discovery
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-06] useRunStream isConnected set true before EventSource confirms connection
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-USE-02; 128-FINDINGS.md FD-14
- **Description:** Verify UI shows "connected" immediately after connect() call, before the server confirms. `setIsConnected(true)` runs synchronously after `new EventSource()` constructor, but the HTTP request has not completed.
  - **Test 1 (unreachable server):** Connect to unreachable URL -> assert isConnected=true initially (bug -- should be connecting/false until onopen).
  - **Test 2 (successful connection):** Connect to working SSE endpoint -> assert isConnected=true after connect() call (correct from user perspective, but premature).
  - **Test 3 (connection refused):** Connect to URL that returns connection refused -> assert isConnected stays true until onerror fires.
- **Priority:** P1 -- Medium severity, misleading connection status for unreachable servers
- **Mock requirements:** Mock EventSource constructor; control readyState and event firing timing
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-07] client.ts Content-Type application/json set for FormData requests
- **Severity:** High
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-CLI-01
- **Description:** Verify apiClient sends Content-Type: application/json for all requests including FormData. When body is FormData, the browser should set multipart/form-data boundary automatically.
  - **Test 1 (JSON request):** Call apiClient with JSON body -> assert Content-Type is application/json (correct).
  - **Test 2 (FormData request):** Call apiClient with FormData body -> assert Content-Type is application/json (bug -- should be absent or multipart/form-data).
  - **Test 3 (FormData override):** Call apiClient with FormData and explicit Content-Type header -> assert caller override respected.
- **Priority:** P0 -- High severity, file upload (Excel import) is broken if server validates Content-Type
- **Mock requirements:** Mock fetch to capture request headers; FormData constructor
- **Implementation cost:** Low
- **Testability:** Testable now (after framework setup)

### [TS-FE-08] useRunStream step handler does not deduplicate by index
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-USE-03
- **Description:** Verify duplicate step events with the same index create duplicate entries in the steps array. The precondition handler correctly uses findIndex for deduplication, but the step handler does not.
  - **Test 1 (duplicate step index):** Emit step event with index=3 -> emit another step event with index=3 -> assert two entries in steps array (bug -- should update in-place).
  - **Test 2 (out-of-order steps):** Emit step index=5, then index=3 -> assert both present, no deduplication issue.
  - **Test 3 (precondition dedup comparison):** Emit precondition with index=1 twice -> assert only one entry (correct precondition behavior).
- **Priority:** P1 -- Medium severity, UI shows duplicate steps for retried backend events
- **Mock requirements:** Mock EventSource; render useRunStream hook
- **Implementation cost:** Low
- **Testability:** Testable now (after framework setup)

### [TS-FE-09] useRunStream external_assertions error-path shows all-zeros summary
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-USE-09
- **Description:** Verify error-path external_assertions payload produces "0 total, 0 passed, 0 failed" summary. The backend error path sends `{type: 'error', message: str}` but the frontend reads `data.total` etc., which default to 0 via `?? 0`.
  - **Test 1 (error path):** Emit external_assertions event with `{type: 'error', message: 'Module failed'}` -> assert summary shows 0/0/0 (bug -- should show error state).
  - **Test 2 (normal path):** Emit external_assertions event with `{total: 5, passed: 3, failed: 2}` -> assert summary shows 5/3/2 (correct).
  - **Test 3 (missing fields):** Emit event with `{total: 5}` only -> assert passed/failed default to 0.
- **Priority:** P2 -- Medium severity, misleading assertion results display
- **Mock requirements:** Mock EventSource; render useRunStream hook
- **Implementation cost:** Low
- **Testability:** Testable now (after framework setup)

### [TS-FE-10] TaskForm operations loading state persists across precondition rows
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-TF-03
- **Description:** Verify loading spinner shows on all precondition rows simultaneously during availability check. A single loading state applies to all rows rather than per-row granularity.
  - **Test 1 (single row loading):** Trigger availability check -> assert spinner on ALL rows (bug -- should be row-specific).
  - **Test 2 (multiple rows):** Add 3 precondition rows -> trigger check -> assert all 3 show spinner simultaneously.
  - **Test 3 (check complete):** Trigger check -> wait for response -> assert spinner removed from all rows.
- **Priority:** P2 -- Medium severity, UX issue during precondition configuration
- **Mock requirements:** Render TaskForm with precondition rows; mock API for operation code availability
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-11] 4 identical manual fetch hooks vs React Query unused
- **Severity:** High
- **Test Type:** Frontend Component
- **Source Finding:** See 128-FINDINGS.md FD-17, QS-03; 127-FINDINGS.md App.tsx React Query
- **Description:** Verify all 4 hooks (useTasks, useReports, useDashboard, useBatchProgress) use identical useState+useEffect+fetch pattern. React Query is installed but no hook uses it. This test protects against partial migration -- if migration begins, verify all 4 are migrated.
  - **Test 1 (pattern detection):** Grep for useState+useEffect+fetch pattern in hooks/ -> assert 4 matches (useTasks, useReports, useDashboard, useBatchProgress).
  - **Test 2 (React Query unused):** Grep for useQuery/useMutation in hooks/ -> assert 0 matches.
  - **Test 3 (after migration):** After migrating to React Query, assert useQuery in all 4 hooks, assert no manual useState+useEffect+fetch.
- **Priority:** P1 -- High severity DRY violation, protects against partial migration during fix
- **Mock requirements:** None (static analysis / grep-based test)
- **Implementation cost:** Low
- **Testability:** Testable now

### [TS-FE-12] AssertionSelector nested setState in toggleMethod
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-AS-02
- **Description:** Verify state updates in toggleMethod are batched correctly. The function calls multiple setState functions (setSelectedKeys, setConfigs, setFieldParamsMap) which should batch in React 18+ automatic batching, but the pattern is fragile under certain callback contexts.
  - **Test 1 (single toggle):** Toggle method on -> assert selectedKeys, configs, fieldParamsMap all updated in single render cycle.
  - **Test 2 (toggle off):** Toggle method off -> assert all three state updates clear the method's data.
  - **Test 3 (rapid toggles):** Toggle on, immediately toggle off -> assert final state is method off (no stale state from race).
- **Priority:** P2 -- Medium severity, potential stale state in rapid interactions
- **Mock requirements:** Render AssertionSelector component; mock external method API
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### [TS-FE-13] useRunStream onerror handler does not handle CONNECTING state
- **Severity:** Medium
- **Test Type:** Frontend Component
- **Source Finding:** See 127-FINDINGS.md DD-USE-05
- **Description:** Verify permanently down server leaves UI "connected" because onerror only handles readyState === CLOSED. During reconnection, readyState is CONNECTING, which the handler ignores.
  - **Test 1 (server permanently down):** Connect to URL, fire onerror with readyState=CONNECTING -> assert isConnected stays true (bug -- should show reconnecting).
  - **Test 2 (connection closed):** Fire onerror with readyState=CLOSED -> assert isConnected=false (correct).
  - **Test 3 (brief interruption):** Fire onerror with readyState=CONNECTING, then fire onopen -> assert isConnected transitions true (correct recovery).
  - **Test 4 (extended interruption):** Fire onerror with readyState=CONNECTING 5 times -> assert isConnected stays true throughout (documents current behavior).
- **Priority:** P1 -- Medium severity, permanently down server never shows disconnected state
- **Mock requirements:** Mock EventSource; control readyState in onerror callback
- **Implementation cost:** Medium
- **Testability:** Testable now (after framework setup)

### Frontend Scenario Summary

**Total scenarios: 13**

#### By Severity

| Severity | Count |
|----------|-------|
| High | 3 |
| Medium | 10 |
| **Total** | **13** |

#### By Priority

| Priority | Count |
|----------|-------|
| P0 | 2 |
| P1 | 6 |
| P2 | 5 |
| **Total** | **13** |

#### Top 3 Highest ROI Scenarios

1. **TS-FE-01** JSON.parse error handling (P0, High) -- single malformed event breaks entire run stream
2. **TS-FE-07** Content-Type for FormData (P0, High) -- file upload broken for Excel import
3. **TS-FE-11** Manual fetch hooks vs React Query (P1, High) -- DRY violation protecting against partial migration

---

*Frontend Component Test Scenarios expanded: 2026-05-04*
*Plan 129-03: Task 1 -- 13 frontend component scenarios from Plan 01 inventory*

## E2E Gap Scenarios

Analysis of existing E2E spec files (7 files in `e2e/tests/`) identifying missing coverage. Per D-04, E2E is supplementary to backend/frontend tests and not the focus. Existing specs cover happy paths with conditional skip patterns.

### [TS-E2E-01] Precondition failure flow -- error state display
- **Severity:** Medium
- **Test Type:** E2E
- **Source Finding:** See 125-FINDINGS.md P1 run_pipeline.py:499-500; 126-FINDINGS.md DD-pipe-03
- **Description:** Verify UI displays correct error state when a task has failing precondition code. Currently, the "started" SSE event is skipped on precondition failure, potentially leaving the UI in an ambiguous state.
  - **Step 1:** Create task with precondition code that always fails (e.g., `raise Exception("test failure")`).
  - **Step 2:** Execute the task via UI (click run button).
  - **Step 3:** Wait for run to complete (max 60s).
  - **Step 4:** Verify run status shows "failed" (not "running" or "pending").
  - **Step 5:** Verify error message contains precondition failure indication.
  - **Expected outcome:** UI shows failed status with precondition error details.
- **Priority:** P2
- **Existing Coverage:** `full-flow.spec.ts` covers happy path only (successful precondition + assertion + codegen).
- **Gap:** No E2E test for the error path when preconditions fail. The missing "started" event means the UI may show an incomplete state.

### [TS-E2E-02] Assertion failure flow -- report shows failure details
- **Severity:** Medium
- **Test Type:** E2E
- **Source Finding:** See 127-FINDINGS.md assertion handler analysis
- **Description:** Verify assertion failure results appear correctly in the test report. Existing assertion tests only verify configuration, not failure outcome display.
  - **Step 1:** Create task with an assertion that will fail (e.g., text_exists with text that does not exist on the page).
  - **Step 2:** Execute the task.
  - **Step 3:** Navigate to the report page.
  - **Step 4:** Verify assertion section shows "failed" status for the failing assertion.
  - **Step 5:** Verify actual_value field is populated (or shows appropriate message).
  - **Expected outcome:** Report clearly displays assertion failure with expected vs actual values.
- **Priority:** P2
- **Existing Coverage:** `assertion-flow.spec.ts` (7 tests) covers assertion configuration and execution but not failure result display.
- **Gap:** No E2E test verifying how assertion failures appear in the report UI.

### [TS-E2E-03] Batch execution monitoring -- progress page updates
- **Severity:** Medium
- **Test Type:** E2E
- **Source Finding:** See 126-FINDINGS.md DD-batch-03, DD-batch-05
- **Description:** Verify batch progress page shows correct run statuses as batch tasks execute. No existing test covers the batch monitoring flow.
  - **Step 1:** Create 3 tasks (2 valid, 1 with assertion configuration).
  - **Step 2:** Select all 3 tasks and trigger batch execution.
  - **Step 3:** Navigate to batch progress page.
  - **Step 4:** Verify progress bar updates as runs complete.
  - **Step 5:** Verify individual task cards show correct status (running/completed/failed).
  - **Step 6:** Wait for all runs to complete.
  - **Step 7:** Verify final batch status shows completion counts.
  - **Expected outcome:** Batch progress page correctly tracks and displays all run statuses in real-time.
- **Priority:** P2
- **Existing Coverage:** None. `full-flow.spec.ts` tests single task execution only.
- **Gap:** Complete absence of batch execution monitoring E2E coverage.

### [TS-E2E-04] Stop run flow -- status updates but agent continues (known limitation)
- **Severity:** Medium
- **Test Type:** E2E
- **Source Finding:** See 126-FINDINGS.md DD-runs-10
- **Description:** Verify the stop run button updates status in the UI. Documents current known limitation where the agent continues executing after stop.
  - **Step 1:** Create a task with multiple steps.
  - **Step 2:** Execute the task.
  - **Step 3:** Wait for first step to appear in run monitor.
  - **Step 4:** Click the stop button.
  - **Step 5:** Verify run status changes to "stopped" in the UI.
  - **Step 6:** Verify that (currently) the agent may continue executing -- document this as known limitation.
  - **Expected outcome:** Status shows "stopped" but backend logs may show continued agent execution. Test documents current behavior for future fix validation.
- **Priority:** P2
- **Existing Coverage:** None. No existing spec tests the stop flow.
- **Gap:** Stop functionality is untested at E2E level. Related backend issue: DD-runs-10 (stop does not cancel agent).

### [TS-E2E-05] External module integration error handling
- **Severity:** Medium
- **Test Type:** E2E
- **Source Finding:** See 126-FINDINGS.md DD-ext-assert-01, DD-ext-data-01
- **Description:** Verify error handling when external data method fails or returns unexpected data. Existing tests cover happy path only.
  - **Step 1:** Create task with external data method configuration.
  - **Step 2:** Configure method with invalid parameters (e.g., method name that does not exist).
  - **Step 3:** Execute the task.
  - **Step 4:** Verify error handling in the UI (error message, not crash).
  - **Step 5:** Alternatively, configure method with valid name but parameters that cause a runtime error in the external module.
  - **Step 6:** Verify error is displayed appropriately.
  - **Expected outcome:** External module errors produce user-visible error messages, not silent failures or UI crashes.
- **Priority:** P2
- **Existing Coverage:** `data-method-execution.spec.ts` covers happy path (successful method call with response display). `data-method-selector.spec.ts` covers UI wizard for method selection.
- **Gap:** No E2E test for external module error scenarios (invalid method, runtime failure, timeout).

### E2E Scenario Summary

**Total scenarios: 5**

#### By Severity

| Severity | Count |
|----------|-------|
| Medium | 5 |
| **Total** | **5** |

#### By Priority

| Priority | Count |
|----------|-------|
| P2 | 5 |
| **Total** | **5** |

#### Existing E2E Coverage Summary

| Spec File | Coverage | Gap Scenario |
|-----------|----------|-------------|
| smoke.spec.ts | Basic create/execute/monitor/report | No error path |
| task-flow.spec.ts | Task listing, monitor, screenshots, reports | No failure flows |
| assertion-flow.spec.ts | Assertion configuration (7 tests) | No assertion failure results |
| variable-substitution.spec.ts | Variable {{variable}} replacement (4 tests) | Complete |
| data-method-selector.spec.ts | DataMethodSelector wizard | No error handling |
| data-method-execution.spec.ts | Data method execution happy path | No module failure |
| full-flow.spec.ts | Complete end-to-end with data method | No error paths |

---

*E2E Gap Scenarios expanded: 2026-05-04*
*Plan 129-03: Task 1 -- 5 E2E gap scenarios from RESEARCH.md pre-identified candidates*

## Final Summary

Complete statistics and implementation roadmap for all 67 test scenarios derived from Phase 125-128 findings.

### Overall Statistics

| Category | Count | P0 | P1 | P2 | DEFERRED |
|----------|-------|----|----|----|----------|
| Backend Unit | 24 | 3 | 9 | 12 | 0 |
| Backend Integration | 25 | 5 | 16 | 4 | 2 (partial) |
| Frontend Component | 13 | 2 | 6 | 5 | 0 |
| E2E | 5 | 0 | 0 | 5 | 1 (stop flow) |
| **Total** | **67** | **10** | **31** | **26** | **3** |

Note: DEFERRED count reflects scenarios with at least one test case that requires a code fix. Most deferred scenarios also have immediately testable cases that document current behavior.

### Source Phase Distribution

| Source Phase | Test Scenarios | Percentage | Key Contributions |
|-------------|---------------|------------|-------------------|
| Phase 125 (backend core) | 28 | 42% | StallDetector, code_generator, step_code_buffer, EventManager, agent_service |
| Phase 126 (API layer) | 17 | 25% | SSE error handling, batch execution, code execution security, external assertions |
| Phase 127 (frontend) | 13 | 19% | useRunStream, TaskForm, client.ts, DataMethodSelector |
| Phase 128 (code quality) | 7 | 10% | Systemic patterns (CP-1~CP-5), naming, dead code detection |
| Cross-phase (125+126+128) | 2 | 3% | Login JS duplication, dual stall detection |
| **Total** | **67** | **100%** | |

### Severity Distribution

| Severity | Backend Unit | Backend Integration | Frontend | E2E | Total |
|----------|-------------|--------------------|---------|----|-------|
| Critical | 1 | 0 | 0 | 0 | 1 |
| High | 2 | 8 | 3 | 0 | 13 |
| Medium | 15 | 16 | 10 | 5 | 46 |
| Low | 6 | 1 | 0 | 0 | 7 |
| **Total** | **24** | **25** | **13** | **5** | **67** |

### Top 10 Highest ROI Scenarios

| Rank | ID | Name | Severity | Priority | ROI Rationale |
|------|----|------|----------|----------|---------------|
| 1 | TS-BE-09 | F-grade generate() produces valid Python | Critical | P0 | Most complex function (F-grade), code generation correctness |
| 2 | TS-BE-01 | StallDetector dual-invocation halves threshold | High | P0 | Pure logic, no mocks, High severity correctness bug |
| 3 | TS-FE-01 | JSON.parse error handling in useRunStream | High | P0 | Single malformed event breaks entire run stream |
| 4 | TS-BE-02 | assertion_service stub returns True always | High | P0 | Documents false confidence in element existence checks |
| 5 | TS-FE-07 | Content-Type for FormData requests | High | P0 | File upload (Excel import) broken on strict servers |
| 6 | TS-BE-25 | EventManager lifecycle / memory leak (CP-1) | High | P0 | Systemic pattern, long-running server stability |
| 7 | TS-BE-26 | SSE error handling / broken subscriber (CP-2) | High | P0 | Systemic pattern, SSE reliability for all users |
| 8 | TS-BE-32 | Code execution endpoint missing path validation | High | P0 | Highest security impact, arbitrary code execution risk |
| 9 | TS-BE-27 | save_screenshot blocks event loop (CP-4) | High | P0 | Systemic pattern, affects all concurrent users |
| 10 | TS-BE-28 | subprocess.run blocks event loop 180s (CP-4) | High | P0 | Blocks entire server during test execution |

### Implementation Roadmap Recommendation

Five-phase implementation sequence, ordered by ROI and dependency:

**Phase A: Test Infrastructure (1-2 days)**
- Create `backend/tests/conftest.py` with shared fixtures (db_session, mock_llm, client)
- Create `backend/tests/__init__.py` and test directory structure
- Configure pytest in `pyproject.toml` (async_mode, testpaths)
- Set up `vitest` + `@testing-library/react` in frontend
- Create frontend test helpers (mock EventSource, mock fetch)
- Verify infrastructure with smoke test

**Phase B: P0 Backend Unit Tests (2-3 days)**
- TS-BE-01: StallDetector dual-invocation
- TS-BE-02: assertion_service stub documentation
- TS-BE-09: F-grade generate() validation (all assertion types)
- These 3 tests provide highest ROI with zero mocks needed (except TS-BE-09 needs mock Assertion objects)

**Phase C: P0 Backend Integration Tests (3-4 days)**
- TS-BE-25: EventManager lifecycle (CP-1)
- TS-BE-26: SSE error handling (CP-2)
- TS-BE-27: save_screenshot blocking (CP-4)
- TS-BE-28: subprocess.run blocking (CP-4)
- TS-BE-32: Code execution path validation (security)
- TS-BE-41: assertion_service stub at pipeline level
- These 6 tests cover all systemic patterns and the highest security finding

**Phase D: P1 Frontend + Remaining Backend (3-4 days)**
- TS-FE-01: JSON.parse error handling (P0 frontend)
- TS-FE-07: Content-Type for FormData (P0 frontend)
- TS-FE-03: TaskForm stale data
- TS-FE-04: Retry toast persistence
- TS-FE-11: Manual fetch vs React Query
- Remaining P1 backend scenarios (TS-BE-03 through TS-BE-08, TS-BE-10, TS-BE-29 through TS-BE-49)
- Total: ~37 P1 scenarios across frontend and backend

**Phase E: P2 E2E + Remaining Scenarios (2-3 days)**
- TS-E2E-01 through TS-E2E-05: E2E gap scenarios
- Remaining P2 backend unit scenarios
- Total: ~26 P2 scenarios

**Estimated total effort: 11-16 days for full implementation**

### Requirements Coverage

Mapping of TEST-01 and TEST-02 requirements to specific test scenario IDs.

#### TEST-01: Missing test coverage for core business flows

Core business flows that lack test protection, mapped to scenarios that fill the gap:

| Core Flow | Missing Coverage | Test Scenarios |
|-----------|-----------------|----------------|
| Test execution pipeline (precondition -> agent -> assertion -> codegen -> report) | No integration test for full pipeline stages | TS-BE-25, TS-BE-26, TS-BE-30, TS-BE-41, TS-BE-42, TS-BE-45, TS-E2E-01, TS-E2E-02, TS-E2E-05 |
| AI agent step execution | Dual stall detection, multi-action mapping | TS-BE-01, TS-BE-29, TS-BE-44 |
| Code generation (Playwright output) | F-grade function untested, special chars, assertion types | TS-BE-03, TS-BE-08, TS-BE-09, TS-BE-10, TS-BE-11, TS-BE-12, TS-BE-14 |
| Assertion system | Element existence stub, external assertion handling | TS-BE-02, TS-BE-39, TS-BE-40, TS-BE-41 |
| SSE real-time monitoring | Event lifecycle, error handling, client disconnect | TS-BE-25, TS-BE-26, TS-BE-34, TS-FE-01, TS-FE-02, TS-FE-08 |
| Batch execution | Partial creation, fire-and-forget, progress monitoring | TS-BE-33, TS-BE-35, TS-BE-43, TS-E2E-03 |
| Task management (CRUD) | No repository tests exist | TS-BE-06, TS-BE-07, TS-BE-19, TS-BE-20 |

**TEST-01 is satisfied by 52 test scenarios across all categories.**

#### TEST-02: Boundary value, error path, race condition, timeout gaps

Specific boundary conditions and error paths that lack test protection:

| Boundary/Error Type | Missing Coverage | Test Scenarios |
|--------------------|-----------------|----------------|
| Boundary values: step number regex, cache key replacement | Chinese-only format, silent empty replacement | TS-BE-07, TS-BE-19, TS-BE-20 |
| Boundary values: special characters in code generation | Quotes, backslashes, newlines in assertion values | TS-BE-08, TS-BE-14 |
| Error paths: SSE malformed data | JSON.parse crash, broken subscriber queue | TS-BE-26, TS-FE-01, TS-FE-09 |
| Error paths: precondition failure | Missing "started" event, UI state confusion | TS-BE-30, TS-BE-45, TS-E2E-01 |
| Error paths: external module failures | Unknown class/method, SSRF, assertion error path | TS-BE-39, TS-BE-40, TS-FE-09, TS-E2E-05 |
| Race conditions: heartbeat task overwrite | Re-subscribe without cancelling old task | TS-BE-38 |
| Race conditions: batch partial creation | Non-atomic batch creation on validation failure | TS-BE-33 |
| Race conditions: step deduplication | Duplicate step index handling | TS-FE-08 |
| Timeout: exec() unrestricted runtime | Precondition code can run indefinitely | TS-BE-46 |
| Timeout: event loop blocking | Screenshot write + subprocess.run block all I/O | TS-BE-27, TS-BE-28, TS-BE-37 |
| Error paths: client disconnect | SSE stream without try/except/finally | TS-BE-34 |
| Error paths: stop run without cancellation | Agent continues after stop request | TS-BE-36, TS-E2E-04 |

**TEST-02 is satisfied by 35 test scenarios covering boundary values, error paths, race conditions, and timeouts.**

### Systemic Pattern Coverage Summary

All 5 systemic patterns from Phase 128 are covered by at least one test scenario:

| Pattern | Backend Unit | Backend Integration | Frontend | Total |
|---------|-------------|--------------------|---------|-------|
| CP-1 Memory leak | -- | TS-BE-25, TS-BE-38 | TS-FE-02 | 3 |
| CP-2 Error handling gap | TS-BE-01 | TS-BE-26, TS-BE-34 | TS-FE-01, TS-FE-04, TS-FE-09, TS-FE-13 | 7 |
| CP-3 Installed-but-unused | -- | -- | TS-FE-11 | 1 |
| CP-4 Blocking I/O | TS-BE-11, TS-BE-12 | TS-BE-27, TS-BE-28, TS-BE-37 | TS-FE-02 | 6 |
| CP-5 Mutable state | TS-BE-06, TS-BE-21, TS-BE-22 | TS-BE-42 | TS-FE-12 | 5 |
| **Total** | **6** | **8** | **7** | **22** |

22 of 67 scenarios (33%) directly test systemic patterns, confirming high ROI for cross-cutting issues.

---

*Final Summary completed: 2026-05-04*
*Plan 129-03: Task 1 -- Frontend + E2E scenarios + Final Summary*
*Phase 129 complete: 67 test scenarios (24 unit + 25 integration + 13 frontend + 5 E2E)*
