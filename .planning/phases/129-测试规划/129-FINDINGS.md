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

---

*Backend Unit Test Scenarios expanded: 2026-05-04*
*Plan 129-02: Task 1 -- 24 unit test scenarios from Plan 01 inventory*
