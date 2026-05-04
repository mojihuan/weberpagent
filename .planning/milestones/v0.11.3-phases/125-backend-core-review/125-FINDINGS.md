# Phase 125: Backend Core Logic Review - Findings

**Review Date:** 2026-05-03
**Scope:** 31 files, ~8,089 lines
**Methodology:** Breadth-first scan + focused deep-dive (per D-01)

## Tool Results

### ruff Scan

14 issues found (8 fixable):

```
F401 [*] `asyncio` imported but unused              -- backend/api/routes/run_pipeline.py:7
F401 [*] `fastapi.HTTPException` imported but unused -- backend/api/routes/run_pipeline.py:14
F401 [*] `backend.db.repository.TaskRepository` imported but unused -- backend/api/routes/run_pipeline.py:19
F401 [*] `backend.db.repository.StepRepository` imported but unused -- backend/api/routes/run_pipeline.py:19
F401 [*] `backend.db.schemas.TaskUpdate` imported but unused -- backend/api/routes/run_pipeline.py:29
E741 Ambiguous variable name: `l` (6 occurrences)   -- backend/core/action_translator.py:378,382,416,420,450,451
F401 [*] `asyncio` imported but unused              -- backend/core/error_utils.py:8
F401 [*] `ast` imported but unused                  -- backend/core/external_method_discovery.py:8
F401 [*] `importlib` imported but unused            -- backend/core/external_module_loader.py:8
```

**Notable:** 5 unused imports in run_pipeline.py (the orchestrator file) suggest it was split from a larger file and leftover imports were not cleaned up. The `l` variable naming in action_translator.py is cosmetic but repeated 6 times.

### mypy Scan

136 errors in 21 files (31 checked). Key categories:

- **dom_patch.py:** 9 errors -- monkey-patching produces `Cannot assign to a method` and type mismatches. Expected given the patching strategy.
- **run_pipeline.py:** 1 error -- `_build_description` receives `str | None` where `str` expected (login_url param).
- **agent_service.py:** 6 errors -- private attribute `_pre_navigated` on BrowserSession, dict/element type confusion in step callback.
- **runs_routes.py:** ~20 errors -- None-safety on ORM relationships (task.name, run.status) and schema construction.
- **action_translator.py:** 3 errors -- frozenset assigned to set, callable used as type hint.
- **Other files:** Mostly `Returning Any from function` in repository.py and `Extra keys` in settings.py.

**Notable for logic review:** The mypy errors in run_pipeline.py:183 (`login_url: str | None` passed as `str`) is a genuine type safety gap that could cause a runtime TypeError if `login_url` is None when `_build_description` is called during login fallback. The agent_service.py `_pre_navigated` attribute is set on BrowserSession without declaration -- a fragile pattern that depends on browser-use internal implementation.

## Risk Priority Matrix

| Priority | File | Lines | Risk Justification |
|----------|------|-------|--------------------|
| P1 | run_pipeline.py | 576 | 6-stage orchestrator, error propagation, state management, double None publish on precondition failure |
| P1 | agent_service.py | 658 | Agent lifecycle, dual step callback, screenshot blocking I/O, mutable dict closures |
| P1 | code_generator.py | 553 | Code assembly, credential embedding, variable substitution ordering |
| P1 | step_code_buffer.py | 414 | Evaluate-to-fill conversion, duplicate wait logic, corrective detection |
| P1 | monitored_agent.py | 227 | PreSubmitGuard dead code (actual_values=None), upload sleep in async context |
| P2 | precondition_service.py | 378 | exec() with full __builtins__, nest_asyncio usage, ContextWrapper mutation |
| P2 | stall_detector.py | 221 | Unbounded _history growth, consecutive failure detection only on action[0] |
| P2 | assertion_service.py | 157 | check_element_exists always returns True (stub) |
| P2 | event_manager.py | 156 | Memory leak (no cleanup), heartbeat task overwrite on re-subscribe |
| P2 | test_flow_service.py | 193 | Step number shifting only handles Chinese step patterns |
| P2 | batch_execution.py | 107 | Semaphore._value internal access, fire-and-forget with no recovery |
| P3 | action_translator.py | 718 | E741 naming (6x), callable type hint, frozenset/set mismatch |
| P3 | dom_patch.py | 777 | 9 mypy errors from monkey-patching, expected per D-03 |
| P3 | external_execution_engine.py | 700 | context mutation in _run_external_assertions leaks into variable_map |
| P3 | external_method_discovery.py | 669 | Unused ast import, complex alias patching logic |
| P3 | locator_chain_builder.py | 233 | Multi-strategy locator generation, well-structured |
| P3 | report_service.py | 197 | Optional type usage (uses `Optional`), minor |
| P3 | auth_service.py | 116 | Token prefix logged (first 20 chars), response variable used outside try |
| P3 | account_service.py | 108 | Lazy loading, sys.path manipulation |
| P3 | external_module_loader.py | 218 | 14 module-level globals, globals() dynamic lookup |
| P3 | pre_submit_guard.py | 149 | Dead code: actual_values/submit_button_text always None from caller |
| P3 | task_progress_tracker.py | 152 | Mutable _completed_steps set, loose keyword matching |
| P3 | prompts.py | 89 | CHINESE_ENHANCEMENT backward-compat alias |
| P3 | action_utils.py | 60 | Clean extraction logic, no issues |
| P3 | cache_service.py | 56 | Immutable deep-copy pattern, well-implemented |
| P3 | error_utils.py | 69 | Unused asyncio import, scan_with_fallback retained per D-09 |
| P3 | random_generators.py | 75 | Standard random generators |
| P3 | time_utils.py | 26 | Simple time formatting |
| P3 | external_precondition_bridge.py | 21 | Re-export facade, clean |
| P3 | __init__.py (agent) | 16 | Re-exports only |

## Quick-Scan Findings (P3 Files)

### [P3] action_translator.py:378,382,416,420,450,451 -- Ambiguous variable name `l`
- **Severity:** Low
- **Category:** Architecture
- **Description:** Six uses of single-character variable `l` for locators in generator expressions. Confusable with `1` in many fonts. The `callable` type hint at line 672 is also not valid for mypy (should be `Callable`).
- **Recommendation:** Rename `l` to `loc` in all 6 occurrences. Change `callable` to `Callable` at line 672.

### [P3] dom_patch.py -- Monkey-patch produces 9 mypy errors
- **Severity:** Low
- **Category:** Architecture
- **Description:** Assigning to class methods (`ClickableElementDetector.is_interactive = ...`) triggers `Cannot assign to a method` errors. The `@staticmethod` wrapper at line 729 is applied to a non-method function, causing type confusion. Expected per D-03.
- **Recommendation:** No action needed -- this is an inherent consequence of monkey-patching. The patches work correctly at runtime.

### [P3] external_execution_engine.py:325 -- Context mutation leaks into variable_map
- **Severity:** Medium
- **Category:** Correctness
- **Description:** `_run_external_assertions` mutates the `context` dict by setting `context['external_assertion_summary'] = summary`. Later in run_pipeline.py:543-547, context is used to build `variable_map` for code generation. The filter `not k.startswith("assertion")` catches keys like `assertion_result_0` but NOT `external_assertion_summary` (starts with "external_", not "assertion"). This means external assertion metadata leaks into generated test code as variable substitutions.
- **Recommendation:** Either (a) change the filter to `not k.startswith(("assertion", "external_assertion"))`, or (b) avoid mutating the shared context dict -- use a separate dict for external assertion metadata.

### [P3] external_module_loader.py:17-43 -- 14 module-level globals with dynamic globals() access
- **Severity:** Low
- **Category:** Architecture
- **Description:** The `_lazy_load` function uses `globals()[var_name]` for reading and writing cache variables. This is fragile (misspelled variable names would silently fail) and makes testing harder. The `reset_cache()` function manually resets all 14 globals.
- **Recommendation:** Encapsulate in a class (e.g., `ExternalModuleRegistry`) with explicit attributes. Reduces fragility and improves testability.

### [P3] external_method_discovery.py:8 -- Unused `ast` import
- **Severity:** Low
- **Category:** Architecture
- **Description:** `import ast` at line 8 is never used in this file. The ast-dependent logic was moved to external_execution_engine.py (ParamDictVisitor).
- **Recommendation:** Remove the unused import.

### [P3] pre_submit_guard.py:109-114 -- Dead code: actual_values and submit_button_text always None
- **Severity:** Medium
- **Category:** Correctness
- **Description:** MonitoredAgent._execute_actions (line 113-114) always passes `actual_values=None, submit_button_text=None` to PreSubmitGuard.check(). This means the guard's core logic (lines 86-117) is unreachable -- it always returns `should_block=False` at line 87 or 90. The submit-blocking feature is completely non-functional.
- **Recommendation:** Document as known limitation. To activate, wire up DOM value extraction from the browser page in MonitoredAgent before calling guard.check().

### [P3] task_progress_tracker.py:149-152 -- Loose keyword matching for step completion
- **Severity:** Low
- **Category:** Correctness
- **Description:** `update_from_evaluation` marks a step as completed if ANY of the first 3 words from the step description appear in the evaluation text (case-insensitive). This is very loose -- a step like "click submit button" would match any evaluation containing the word "click", even if that click was for a different purpose.
- **Recommendation:** Require at least 2 of 3 keywords to match, or use a more structured matching strategy. Current approach may produce false-positive progress tracking.

### [P3] auth_service.py:84-86 -- Token prefix logged
- **Severity:** Low
- **Category:** Security
- **Description:** Line 84-86 logs `token={token[:20]}...` which exposes the first 20 characters of the access token. Combined with knowledge of the token format (JWT), this could aid token reconstruction.
- **Recommendation:** Replace with `token=***REDACTED***` or log only the last 4 characters.

### [P3] auth_service.py:96-100 -- `response` variable used outside try/except
- **Severity:** Medium
- **Category:** Correctness
- **Description:** The `except (KeyError, TypeError)` block at line 96-100 references `response.text[:200]`, but `response` is assigned inside the `async with` block. If `response.json()` raises a KeyError/TypeError, `response` may be out of scope or undefined in the except handler, causing an UnboundLocalError.
- **Recommendation:** Store `response.text` in a local variable before parsing, or wrap the JSON access separately.

### [P3] error_utils.py:8 -- Unused `asyncio` import
- **Severity:** Low
- **Category:** Architecture
- **Description:** `import asyncio` is present but never used. `scan_with_fallback` is documented as unused per D-09 but retained for future use.
- **Recommendation:** Remove unused `asyncio` import.

### [P3] report_service.py:6 -- Uses `Optional` instead of `str | None`
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 6 imports `Optional` from typing, used in `generate_report` return type. Project convention (CLAUDE.md) prefers `str | None`.
- **Recommendation:** Replace `Optional[Report]` with `Report | None`.

### [P3] locator_chain_builder.py -- Well-structured, no significant issues
- **Severity:** N/A
- **Category:** N/A
- **Description:** Multi-strategy locator generation with clean priority ordering, proper PUA character filtering, and 3-locator cap. No logic errors found.

### [P3] cache_service.py -- Well-implemented immutable pattern
- **Severity:** N/A
- **Category:** N/A
- **Description:** Deep-copy on store and retrieve guarantees immutability. Uses spread operator for functional updates (`self._store = {**self._store, key: ...}`). No issues found.

### [P3] action_utils.py -- Clean extraction logic
- **Severity:** N/A
- **Category:** N/A
- **Description:** Both `extract_action_info` and `extract_all_actions` handle edge cases properly (None input, empty action list, non-dict params). No issues found.

### [P3] random_generators.py, time_utils.py -- Standard utilities
- **Severity:** N/A
- **Category:** N/A
- **Description:** Simple, well-documented utility functions. No issues found.

### [P3] external_precondition_bridge.py -- Clean re-export facade
- **Severity:** N/A
- **Category:** N/A
- **Description:** 21-line file with only re-exports and `noqa: F401` annotations. No issues.

### [P3] prompts.py -- Backward-compatible alias retained
- **Severity:** N/A
- **Category:** Architecture
- **Description:** `CHINESE_ENHANCEMENT = ENHANCED_SYSTEM_MESSAGE` alias retained for backward compatibility. The comment references files that no longer exist (browser_agent.py, proxy_agent.py). Safe to remove if no external consumers exist.

### [P3] account_service.py -- Lazy loading with sys.path manipulation
- **Severity:** Low
- **Category:** Architecture
- **Description:** `_ensure_loaded` adds to `sys.path` if not present. Same pattern as external_module_loader. The module-level singleton (`account_service = AccountService()`) means state persists across requests.
- **Recommendation:** No immediate action. Be aware of shared mutable state in testing scenarios.

## Cross-File Findings (from breadth scan)

### [Cross-1] Double None SSE event on precondition failure
- **Severity:** Medium
- **Category:** Correctness
- **Files:** run_pipeline.py:119-125, run_pipeline.py:574-575
- **Description:** When `_run_preconditions` fails, it publishes `None` (line 124) then returns. The caller returns early. But if execution reaches the `finally` block at line 574-575, another `None` is published. For the precondition failure path specifically, the `finally` is NOT reached (early return at line 500), so this is NOT a double-publish. However, if an exception occurs after preconditions succeed but before the try block, both `_finalize_run` (which sets finished status) and the `finally` block publish events. The `finished` event is published inside `_finalize_run` AND the `None` sentinel in finally -- these are different events, so this is correct behavior.

### [Cross-2] Dual stall detection in agent_service and MonitoredAgent
- **Severity:** Medium
- **Category:** Correctness
- **Files:** agent_service.py:320-383, monitored_agent.py:148-227
- **Description:** Stall detection runs TWICE per step -- once in `MonitoredAgent.create_step_callback()` (line 191-203) and once in `agent_service._run_detectors()` (line 340-347). Both create separate `StallDetector.check()` calls. But wait: `agent_service._run_detectors` calls `agent._stall_detector.check()` -- the SAME detector instance on the MonitoredAgent. And `MonitoredAgent.step_callback` also calls `self._stall_detector.check()`. Since both callbacks run for every step, the detector's `_history` gets duplicate entries. This means consecutive failure counts are inflated (each failure is recorded twice), which could cause premature stall intervention at half the configured threshold.
- **Recommendation:** Remove stall detection from either `MonitoredAgent.step_callback` or `agent_service._run_detectors`. The MonitoredAgent version is cleaner (runs in browser-use's callback lifecycle), but the agent_service version also handles failure mode detection. Consolidate into one location.

### [Cross-3] Synchronous I/O in async context (screenshots)
- **Severity:** Medium
- **Category:** Performance
- **Files:** agent_service.py:127
- **Description:** `save_screenshot` at line 127 calls `filepath.write_bytes(screenshot_bytes)` synchronously. The method is declared `async` but performs no `await`. During batch execution with concurrency 2-4, this blocks the event loop for 100KB-1MB+ writes.
- **Recommendation:** Wrap in `await asyncio.to_thread(filepath.write_bytes, screenshot_bytes)` or `await loop.run_in_executor(None, filepath.write_bytes, screenshot_bytes)`.

### [Cross-4] external_assertion_summary leaks into variable_map via incomplete filter
- **Severity:** Medium
- **Category:** Correctness
- **Files:** run_pipeline.py:325, run_pipeline.py:543-546
- **Description:** `_run_external_assertions()` mutates the `context` dict by setting `context['external_assertion_summary'] = summary`. The variable_map filter at line 546 uses `not k.startswith("assertion")` which does NOT catch keys starting with "external_assertion" (they start with "external_", not "assertion"). However, the `isinstance(v, (str, int, float))` guard at line 546 would filter it out if the summary value is a dict or list (not a primitive type). This is a latent filter gap that could surface if the summary format changes to a string.
- **Recommendation:** Change the filter to `not k.startswith(("assertion", "external_assertion"))` for defense-in-depth.

### [Cross-5] Login credentials embedded in generated test files
- **Severity:** Low (internal tool)
- **Category:** Security
- **Files:** code_generator.py:197-201, run_pipeline.py:556-560
- **Description:** Login credentials (account/password) are embedded as string literals in generated test files via `_form_login(page, "{origin}", "{account}", "{password}")`. These files are stored on disk and accessible via the code viewer API endpoint.
- **Recommendation:** Already documented in CONCERNS.md. For internal single-user deployment this is acceptable. Consider environment variable injection for future multi-user deployment.

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total files reviewed | 31 |
| Total lines scanned | ~8,089 |
| ruff issues | 14 (8 fixable, 6 naming) |
| mypy errors (in-scope) | ~20 (excluding dom_patch expected errors) |
| P1 findings (deep-dive needed) | 5 files |
| P2 findings (supporting services) | 6 files |
| P3 findings (quick scan) | 20 files |
| Cross-file findings | 5 |
| Critical issues | 0 |
| High issues | 1 (dual stall detection inflates failure count) |
| Medium issues | 5 |
| Low issues | 8 |

## Files Requiring No Further Review

The following P3 files had no significant findings and do not need deep-dive:
- action_utils.py, cache_service.py, locator_chain_builder.py, random_generators.py, time_utils.py, external_precondition_bridge.py, __init__.py (agent)

## Deep-Dive Findings (P1 Files)

### run_pipeline.py

### [VERIFIED-OK] run_pipeline.py:543 -- isinstance(context, dict) check is correct
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Initially flagged as a bug where `isinstance(context, dict)` would fail for ContextWrapper. **Verification revealed this is incorrect.** `_run_preconditions()` returns `precondition_service.get_context()` which calls `self.context.to_dict()` → `copy.deepcopy(self._data)` — a plain `dict`. When no preconditions exist, it returns `{}` (empty dict). In all code paths, `context` is a plain `dict`, so `isinstance(context, dict)` always returns `True`. Variable substitution via `_variable_map` works correctly for tasks with preconditions.
- **Impact:** No issue. The variable_map is properly constructed and variable substitution works as designed.
- **Recommendation:** None needed.

### [P1] run_pipeline.py:325 -- external_assertion_summary leaks into variable_map when isinstance check is bypassed
- **Severity:** Medium
- **Category:** Correctness
- **Description:** `_run_external_assertions()` at line 325 mutates the `context` dict by setting `context['external_assertion_summary'] = summary`. If the isinstance check at line 543 were fixed, this key would pass through the filter at line 546 because `not k.startswith("assertion")` does not match keys starting with "external_assertion". The key `external_assertion_summary` would appear as a variable substitution in generated test code.
- **Impact:** Generated test code would get a spurious variable substitution for `external_assertion_summary`, potentially breaking test execution.
- **Recommendation:** Change the filter at line 546 to `not k.startswith(("assertion", "external_assertion"))`, or avoid mutating the shared context -- use a separate dict for external assertion metadata.
- **RESEARCH Reference:** Pitfall 3 (context mutation between pipeline stages)

### [P1] run_pipeline.py:499-500 -- Precondition failure early return skips status="running" and "started" SSE event
- **Severity:** Medium
- **Category:** Correctness
- **Description:** When `_run_preconditions()` returns `None` (failure), line 500 does `return` immediately. But lines 510-512 (which set status to "running" and publish the "started" SSE event) have NOT executed yet. The frontend will see a "finished" event with status="failed" without ever receiving a "started" event. This could cause UI state confusion (the run transitions from initial to failed without going through running).
- **Impact:** Frontend UI may not properly render the failed state if it expects a "started" event before "finished". The SSE event ordering is: precondition events -> finished(failed) -> None sentinel. The "started" event is missing.
- **Recommendation:** Move the "started" event publication to before preconditions, or ensure the frontend handles receiving "finished" without "started" gracefully.
- **RESEARCH Reference:** Pitfall 2 (double None) -- verified this is NOT a double-publish issue (early return skips finally), but a missing-started-event issue.

### [P1] run_pipeline.py:7,14,19,29 -- 5 unused imports in pipeline orchestrator
- **Severity:** Low
- **Category:** Architecture
- **Description:** `asyncio`, `HTTPException`, `TaskRepository`, `StepRepository`, and `TaskUpdate` are imported but never used. These are leftovers from when pipeline code was part of the larger runs.py file.
- **Impact:** Clutters imports, confuses readers about what the pipeline depends on.
- **Recommendation:** Remove all 5 unused imports. Verified by ruff F401 checks.

### [P1] run_pipeline.py:510 -- run status set to "running" after auth, before agent execution
- **Severity:** Low
- **Category:** Correctness
- **Description:** The run status is set to "running" at line 510, AFTER auth/session setup (step 2) but BEFORE agent execution (step 3). If the agent crashes immediately or the try block at line 517 throws before step 3, the run will be stuck in "running" status unless the except block at line 569 catches it (which it does -- line 571 sets "failed"). This is correctly handled.
- **Impact:** No actual issue -- the except block properly cleans up the status. Documenting as verified correct.
- **Recommendation:** None needed. Error handling is correct.

### agent_service.py

### [P1] agent_service.py:127 -- Synchronous file write in async method blocks event loop
- **Severity:** Medium
- **Category:** Performance
- **Description:** `save_screenshot()` at line 127 calls `filepath.write_bytes(screenshot_bytes)` which is synchronous blocking I/O. The method is declared `async` but contains no `await`. Screenshots range from 100KB to 1MB+. During batch execution (concurrency 2-4), this blocks the event loop for each screenshot write, stalling all other async tasks including SSE event publishing and other concurrent runs.
- **Impact:** Under concurrent execution, screenshot writes create visible latency spikes. SSE events are delayed, and parallel runs are serialized during I/O.
- **Recommendation:** Wrap in `await asyncio.to_thread(filepath.write_bytes, screenshot_bytes)` or `await loop.run_in_executor(None, filepath.write_bytes, screenshot_bytes)`.
- **RESEARCH Reference:** Pitfall 4 (screenshot I/O in async context)

### [P1] agent_service.py:294,307 -- Fragile attribute setting on BrowserSession internals
- **Severity:** Medium
- **Category:** Architecture
- **Description:** Lines 294 and 307 set `browser_session._pre_navigated = True` on the BrowserSession object. This attribute is not declared in browser-use's BrowserSession class -- it's a dynamic attribute. If browser-use changes its internal API or adds a `_pre_navigated` attribute with different semantics, this will break silently or cause unexpected behavior. This was flagged by mypy as a type error.
- **Impact:** browser-use upgrades could break the pre-navigation flag mechanism, causing unnecessary re-navigation or login failures.
- **Recommendation:** Track pre-navigation state in AgentService (e.g., `self._pre_navigated_sessions: set`) instead of setting attributes on external library objects. Or use `hasattr`/`getattr` with a project-unique prefix like `_weberpagent_pre_navigated`.

### [P1] agent_service.py:340-347 -- Dual stall detection: MonitoredAgent and agent_service both call StallDetector.check()
- **Severity:** High
- **Category:** Correctness
- **Description:** The `StallDetector` instance is shared between `MonitoredAgent` (created at line 580) and `agent_service._run_detectors()` (line 340). Both call `stall_detector.check()` on every step:
  1. MonitoredAgent's `create_step_callback()` at line 191 calls `self._stall_detector.check()` -- this is the SAME detector instance because MonitoredAgent was constructed with `stall_detector=stall_detector` at line 592.
  2. agent_service's `_run_detectors()` at line 340 calls `agent._stall_detector.check()` -- same instance.
  Both calls append to `_history`, so every step generates TWO history entries. The consecutive failure detection counts double, meaning the configured threshold of `max_consecutive_failures=2` triggers after just 1 actual failure (because it sees 2 entries). Similarly, stagnant DOM detection (`max_stagnant_steps=3`) triggers after just 2 actual steps.
- **Impact:** Stall intervention fires at approximately half the intended threshold. This causes premature agent intervention and potentially unnecessary corrective actions. The agent may be redirected when it was actually making progress.
- **Recommendation:** Remove stall detection from one of the two locations. Options:
  - (a) Remove from `agent_service._run_detectors()` (lines 340-347) and rely on MonitoredAgent's callback. Also remove progress tracking duplication (lines 374-380).
  - (b) Remove from MonitoredAgent's callback (lines 190-203) and keep only in agent_service.
  Option (a) is cleaner since MonitoredAgent owns the detectors. However, agent_service's `_run_detectors` also handles `detect_failure_mode` and `_prev_dom_hash_data` tracking which are unique to agent_service -- these should remain.
- **RESEARCH Reference:** Pitfall 1 (dual step callback) and Cross-2 (dual stall detection)

### [P1] agent_service.py:374-380 -- Dual progress tracking: MonitoredAgent and agent_service both call TaskProgressTracker
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Same pattern as dual stall detection. `TaskProgressTracker.check_progress()` and `update_from_evaluation()` are called both in MonitoredAgent's step_callback (lines 206-220) and in agent_service's `_run_detectors()` (lines 374-380). The tracker instance is shared. `update_from_evaluation` at line 220 (MonitoredAgent) and line 380 (agent_service) both mark steps as completed based on keyword matching. Double-calling `update_from_evaluation` may cause off-by-one errors in remaining step counts.
- **Impact:** Progress tracking counts are inflated. The progress warning threshold fires prematurely.
- **Recommendation:** Same as stall detection fix -- remove from one location. Keep in MonitoredAgent, remove from agent_service._run_detectors.

### [P1] agent_service.py:400-413 -- DOM serialization and hashing on every step is synchronous and expensive
- **Severity:** Medium
- **Category:** Performance
- **Description:** `_extract_browser_state()` calls `dom_state.llm_representation()` which serializes the entire DOM tree into a string, then `hashlib.sha256()` hashes it. For complex ERP pages, the DOM representation can be tens of KB. This happens synchronously in the step callback on every step. Combined with the screenshot write blocking (finding above), each step has two synchronous blocking operations.
- **Impact:** Step callbacks are slower than necessary. For pages with large DOMs, serialization alone can take 10-50ms.
- **Recommendation:** Consider caching the DOM hash when the DOM hasn't changed (check URL or element_count first). Or offload hashing to a thread pool.

### [P1] agent_service.py:484 -- Potential IndexError when accessing agent_output.action[i]
- **Severity:** Medium
- **Category:** Correctness
- **Description:** At line 484, the code accesses `agent_output.action[i]` where `i` is the loop index from `enumerate(all_actions)`. `all_actions` is built by iterating `agent_output.action` and extracting non-empty dicts. But `agent_output.action[i]` assumes the index `i` corresponds to the same position in the original action list. If any action was skipped (empty dict, filtered out by the `if not action_dict: continue` in `extract_all_actions`), the indices diverge and `agent_output.action[i]` returns the wrong action model, leading to incorrect `interacted_element` extraction.
- **Impact:** For multi-action steps where some actions are filtered out, the wrong element's DOM data is attached to subsequent actions. This causes incorrect locator generation in the code buffer.
- **Recommendation:** Track the original index in `extract_all_actions` or iterate `agent_output.action` directly in the step callback instead of relying on `all_actions` indices.

### code_generator.py

### [P1] code_generator.py:198-201 -- Credentials embedded as string literals in generated test files
- **Severity:** Low (internal tool)
- **Category:** Security
- **Description:** The login_config at lines 198-201 embeds `origin`, `account`, and `password` as string literals directly into generated test files via f-string: `_form_login(page, "{origin}", "{account}", "{password}")`. The generated files are stored on disk in `outputs/{run_id}/generated/test_{run_id}.py` and are accessible via the code viewer API endpoint. The escaping at lines 198-200 only handles double quotes (`"` -> `\\"`), not backslashes or other special characters. If credentials contain backslashes, the generated code will have broken string literals.
- **Impact:** (1) Credentials are stored in plaintext on disk. (2) Credentials containing backslashes (e.g., Windows-style paths) will break the generated Python code with a SyntaxError. For the current internal deployment this is acceptable but should be addressed before multi-user deployment.
- **Recommendation:** For immediate: ensure escaping also handles backslashes (`\\` -> `\\\\`). For future: use environment variable injection instead of embedding credentials.
- **RESEARCH Reference:** Cross-5 (login credentials in generated files)

### [VERIFIED-OK] code_generator.py:241-242 -- Variable substitution works correctly
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Initially flagged as broken because `variable_map` was believed to always be `None`. **Verification confirmed that `context` is always a plain `dict` (see run_pipeline.py:543 correction), so `_variable_map` is properly constructed and variable substitution works as designed.** However, `_substitute_variables_in_code` uses a global string replace (`code.replace(f'"{escaped}"', var_name)`) which could cause false matches if a short value appears in multiple fill() calls with different semantic meanings. This is a minor concern, not a blocker.
- **Impact:** Variable substitution works. Minor risk of false matches in the string replacement strategy.
- **Recommendation:** Consider using positional replacement instead of global string replace to avoid false matches.

### [P1] code_generator.py:487,496 -- Unescaped assertion expected values in f-string generated code
- **Severity:** Medium
- **Category:** Security
- **Description:** Lines 487 and 496 embed `expected` values directly into generated f-strings without escaping: `re.compile(".*{expected}.*")` and `expect(page.locator("body")).to_contain_text("{expected}")`. If an assertion's expected value contains a double quote (`"`), the generated Python code will have a broken string literal causing a SyntaxError. For example, `expected='He said "hello"'` would generate `expect(page.locator("body")).to_contain_text("He said "hello"")`.
- **Impact:** Assertions with special characters in expected values produce syntactically invalid test code. The syntax validation at line 273 catches this and logs a warning but does not fix it.
- **Recommendation:** Escape the `expected` value before embedding: `expected.replace('"', '\\"')`. Apply to all assertion translation methods.

### [P1] code_generator.py:273-279 -- Syntax validation failure logs warning but returns broken code
- **Severity:** Low
- **Category:** Correctness
- **Description:** The `validate_syntax` check at line 273 calls `ast.parse(content)` on failure and logs a warning. But the content is still returned as-is. The `if not self.validate_syntax(content)` check at line 273 calls `ast.parse` a second time inside the block (line 275) for the error message. This means the code is parsed twice on failure. More importantly, the broken code is saved to disk and will fail when executed.
- **Impact:** Generated test files with syntax errors are written to disk. Users who try to run them get confusing Python syntax errors.
- **Recommendation:** The double-parse is minor. Consider adding a comment marker `# SYNTAX ERROR: ...` at the top of the file when validation fails, so users immediately know the generated code has issues.

### step_code_buffer.py

### [P1] step_code_buffer.py:131-133 -- Pre-click wait of 3000ms is excessive for generated test code
- **Severity:** Medium
- **Category:** Performance
- **Description:** `_derive_wait()` returns `page.wait_for_timeout(3000)` for click actions at line 133. This wait is placed BEFORE the click action (it becomes `wait_before` in the StepRecord). Then in `assemble()` at lines 382-395, an additional post-click stability wait is added (`wait_for_load_state("networkidle", timeout=3000)` + `wait_for_timeout(500)`). The total wait per click action is: 3000ms pre-click + networkidle timeout + 500ms post-click = approximately 6.5 seconds per click. For a test with 10 click actions, that is ~65 seconds of waits.
- **Impact:** Generated test code executes very slowly. The 3-second pre-click wait was intended to allow "async updates" (per comment), but the wait is before the click -- the async update happens after the click, not before.
- **Recommendation:** Remove or reduce the pre-click wait. The post-click networkidle + 500ms wait in `assemble()` already covers async page updates. The pre-click wait only makes sense for specific scenarios (e.g., waiting for a dropdown to render), which is handled by the popup element check at line 128.
- **RESEARCH Reference:** Pitfall 6 (duplicate wait logic)

### [P1] step_code_buffer.py:63 -- _identify_action_type called as private method from different class
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 63 calls `ActionTranslator._identify_action_type(action_dict)` -- a private method (prefixed with underscore) of a different class. This violates encapsulation. The method should either be a public static method or a module-level utility.
- **Impact:** If ActionTranslator refactors its internal methods, this call will break silently.
- **Recommendation:** Rename `_identify_action_type` to `identify_action_type` (public static method) or extract to a standalone utility function.

### [P1] step_code_buffer.py:227-257 -- Corrective evaluate detection only checks last input, not all recent inputs
- **Severity:** Medium
- **Category:** Correctness
- **Description:** `_is_corrective_evaluate()` at lines 250-255 searches `_records` in reverse for an input action with the same fill value. It stops the search when it encounters any "click", "input", or "navigate" action (line 254). This means if there is a click between the failed input and the corrective evaluate, the corrective detection fails and the evaluate gets converted to .fill() -- which is exactly the operation that already failed. The break condition is too aggressive.
- **Impact:** In scenarios where the agent clicks a different element before using evaluate to correct a prior input (e.g., clicking away and back), the corrective detection fails. The evaluate gets converted to .fill() which triggers the same component formatting issue that caused the original failure.
- **Recommendation:** Extend the search window: look back through more record types, or use a configurable search depth instead of stopping at the first click/navigate.

### [P1] step_code_buffer.py:380-395 -- Post-click stability wait always adds networkidle with 3s timeout
- **Severity:** Medium
- **Category:** Performance
- **Description:** `assemble()` inserts a post-click stability action for every click. The `wait_for_load_state("networkidle", timeout=3000)` at line 385 waits up to 3 seconds for the network to become idle. For non-navigation clicks (button clicks, tab switches, checkbox toggles), the network is typically already idle, so this always hits the 3-second timeout because `networkidle` waits for the condition OR timeout. The try/except catches the Playwright timeout error, but the 3-second wait still occurs.
- **Impact:** Every click action in generated test code adds a minimum 3-second wait even when no network activity is expected. Combined with the pre-click wait, this makes generated tests extremely slow.
- **Recommendation:** Reduce the networkidle timeout to 1000ms or use `page.wait_for_timeout(500)` only. The 500ms post-click timeout at line 389 already covers DOM rendering. The networkidle check is primarily useful for navigation clicks (which are a different action type).

### monitored_agent.py

### [P1] monitored_agent.py:113-114 -- PreSubmitGuard always receives None for actual_values and submit_button_text
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Lines 113-114 hardcode `actual_values=None` and `submit_button_text=None` in the PreSubmitGuard.check() call. This means the guard's core logic (lines 86-117 in pre_submit_guard.py) is completely unreachable. The method always returns `GuardResult(should_block=False, message="")` at line 87 or 90. The submit-blocking feature is a no-op -- it never blocks any submit.
- **Impact:** The PreSubmitGuard feature was designed to prevent premature submits when form field values don't match expectations. Since it never blocks, the agent can submit forms with incorrect values. This could cause data integrity issues in the ERP system being tested.
- **Recommendation:** Document as known limitation. To activate: extract actual DOM values via `page.evaluate()` before the guard check, and pass the clicked button's text as `submit_button_text`. This requires implementing DOM value extraction in the async context.
- **RESEARCH Reference:** Pitfall 7 (PreSubmitGuard dead code)

### [P1] monitored_agent.py:141-146 -- asyncio.sleep(3) after upload_file blocks event loop in async context
- **Severity:** Medium
- **Category:** Performance
- **Description:** Lines 141-146 add `await asyncio.sleep(3)` after every upload_file action. While `asyncio.sleep` is non-blocking (it yields to the event loop), a 3-second unconditional wait is excessive. During this wait, the agent is stalled but the event loop is free. The comment says "let ERP asynchronously process the uploaded file" but 3 seconds is arbitrary.
- **Impact:** Every file upload adds 3 seconds to execution time. If the ERP processes the file faster, time is wasted. If it needs longer, the wait is insufficient anyway.
- **Recommendation:** Replace with a polling strategy: check for upload completion (e.g., thumbnail rendered, file size updated) with a 5-second timeout and 500ms polling interval. Or make the wait configurable via settings.

### [P1] monitored_agent.py:179-188 -- DOM serialization and hashing duplicated in MonitoredAgent step callback
- **Severity:** Low
- **Category:** Architecture
- **Description:** Lines 179-188 compute `dom_hash` by calling `dom_state.llm_representation()` + `hashlib.sha256()`, which is the same computation that `agent_service._extract_browser_state()` performs (agent_service.py lines 400-406). The dom_hash is computed in BOTH MonitoredAgent's callback and agent_service's callback, doubling the CPU cost of DOM serialization on every step.
- **Impact:** Every step performs DOM serialization twice. This is wasteful but the impact is mitigated by the fact that both callbacks run in the same event loop and the DOM state object may cache `llm_representation()`.
- **Recommendation:** Pass the dom_hash from agent_service's callback to MonitoredAgent's callback (or vice versa) to avoid double computation. Or verify that `llm_representation()` is cached internally and note the redundancy is harmless.

### [P1] monitored_agent.py:54 -- _pending_interventions is a mutable list shared across callback and _prepare_context
- **Severity:** Low
- **Category:** Architecture
- **Description:** `_pending_interventions` is appended to in `step_callback` (lines 198, 213) and consumed+cleared in `_prepare_context` (lines 71-82). Both run on the same async event loop, so there is no true race condition. However, if `step_callback` raises between an `append` and the list being fully processed, the exception handler at line 222 catches it, but any interventions already appended remain in the list. This is actually correct behavior (they will be consumed in the next `_prepare_context` call), but the list is never bounded -- if `_prepare_context` is never called (agent stops), interventions accumulate.
- **Impact:** Minimal in practice. Interventions are bounded by max_steps. The agent always calls `_prepare_context` before each step, so accumulation is capped.
- **Recommendation:** No action needed. The pattern is sound given the single-threaded async execution model.

## P2 Supporting Services Findings

### precondition_service.py (378 lines)

### [P2] precondition_service.py:243 -- exec() with full `__builtins__` provides unrestricted Python runtime
- **Severity:** Medium (acceptable for single-user deployment)
- **Category:** Security
- **Description:** Line 243 passes `'__builtins__': __builtins__` to the exec() environment. This gives precondition code access to the full Python standard library including `os`, `subprocess`, `socket`, `shutil`, and all other modules. Any task creator can execute arbitrary code on the server. The exec is wrapped in `run_in_executor` with a 30-second timeout, but the timeout only limits wall-clock time, not the capabilities available during execution.
- **Impact:** In a multi-user deployment, any user can execute arbitrary code including file deletion, network access, and process spawning. Currently acceptable because the platform is single-user/internal.
- **Recommendation:** Already documented in CONCERNS.md. For future multi-user deployment: remove `__builtins__` and provide an explicit safe subset using `RestrictedPython` or a subprocess sandbox.
- **CONCERNS.md Reference:** Confirmed -- "exec() for user-provided code" entry.

### [P2] precondition_service.py:59 -- nest_asyncio.apply() modifies global event loop policy
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 59 calls `nest_asyncio.apply()` which patches the global event loop to allow nested `asyncio.run()` calls. This modification is irreversible within the process lifetime. If `execute_data_method_sync` is called multiple times, `nest_asyncio.apply()` is called each time (idempotent but wasteful). The comment says "This is safe because we're in run_in_executor which runs in a thread pool" but `nest_asyncio.apply()` patches the MAIN event loop, not the thread's loop.
- **Impact:** Global event loop modification. Could theoretically interact with other async operations in unexpected ways. In practice, nest_asyncio is well-tested and this is a known workaround for the sync-to-async bridge pattern.
- **Recommendation:** Call `nest_asyncio.apply()` once at module load or application startup rather than on every data method call.

### [P2] precondition_service.py:72-73 -- ContextWrapper is shared mutable state across pipeline stages
- **Severity:** Low
- **Category:** Architecture
- **Description:** ContextWrapper holds `_data` dict and `_assertion_summary` dict. Both are mutated in-place by `__setitem__`, `store_assertion_result`, and `reset_assertion_tracking`. The same ContextWrapper instance flows from precondition execution through `_run_external_assertions` to variable_map construction. State from one stage is visible to all subsequent stages. This is intentional (precondition variables must be available for assertion evaluation), but the mutation at run_pipeline.py:325 (`context['external_assertion_summary'] = summary`) shows a case where stage-specific data leaks into the shared context.
- **Impact:** No state leakage between runs (new ContextWrapper per run). Within a run, cross-stage contamination is possible as documented in the run_pipeline.py:325 finding.
- **Recommendation:** Acceptable for current use. If stage isolation becomes important, use separate dicts per stage with an explicit merge step.

### [P2] precondition_service.py:371-378 -- Jinja2 StrictUndefined properly catches undefined variables
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** `substitute_variables` uses `Environment(undefined=StrictUndefined)` which raises `UndefinedError` on missing variables. This is the correct behavior -- it prevents silent empty-string substitution for undefined variables. However, callers (test_flow_service.py `_replace_context_variables`) catch `UndefinedError` and log a warning, falling back to the original text with unsubstituted variables. This means undefined variables produce warnings rather than errors, which may mask configuration issues.
- **Impact:** Undefined template variables produce warnings instead of hard failures. This is a design choice (permissive execution), not a bug.
- **Recommendation:** No action needed. The warning-based approach is appropriate for a QA testing tool where partial execution is preferable to hard failure.

### stall_detector.py (221 lines)

### [P2] stall_detector.py:74,100 -- `_history` list grows without bounds
- **Severity:** Low
- **Category:** Performance
- **Description:** `_history` is a list that appends one `_StepRecord` per `check()` call. There is no trimming or cap. However, each `StallDetector` instance is created fresh per run (confirmed in agent_service.py), and typical runs have 10-30 steps. With dual stall detection (Cross-2), this doubles to 20-60 records. Even for long runs with 100+ steps, memory usage is negligible (each record is ~4 small fields).
- **Impact:** Negligible. The detector instances are short-lived (created per run, garbage collected after run completes).
- **Recommendation:** No action needed. Add a cap only if runs with 1000+ steps become common.
- **RESEARCH Reference:** Open Question 2 (StallDetector unbounded history) -- confirmed Low risk.

### [P2] stall_detector.py:30-31 -- StallResult is properly frozen dataclass
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** `StallResult(should_intervene, message)` uses `@dataclass(frozen=True)`, making it immutable. Similarly, `FailureDetectionResult` is also frozen. This is correct per project coding conventions. No mutation is possible after construction.
- **Recommendation:** None needed.

### [P2] stall_detector.py:110-140 -- Consecutive failure detection correctly handles success resets
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** `_check_consecutive_failures` iterates history in reverse. When it encounters a non-failure record (no FAILURE_KEYWORDS match), it breaks immediately (line 119). This correctly implements "success resets the counter" (MON-03). The logic only counts consecutive failures on the same action_name AND target_index combination (line 126), preventing false positives from failures on different elements.
- **Recommendation:** None needed. Logic is correct.

### [P2] stall_detector.py:142-160 -- Stagnant DOM detection uses recent-N window correctly
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** `_check_stagnant_dom` checks if the last `max_stagnant_steps` (default 3) entries all have the same `dom_hash`. The slice `self._history[-self.max_stagnant_steps:]` correctly handles cases where history has fewer entries than the threshold (line 144 returns early). The set comparison `len(hashes) == 1` is an efficient way to check all-identical.
- **Recommendation:** None needed.

### assertion_service.py (157 lines)

### [P2] assertion_service.py:88-110 -- check_element_exists is a stub that always returns True when is_done
- **Severity:** High
- **Category:** Correctness
- **Description:** `check_element_exists` at lines 103-107 returns `(True, "", selector)` whenever `history.is_done` is True. There is zero actual DOM element checking. The selector parameter is completely ignored. This means `element_exists` assertions ALWAYS pass for successfully completed runs, regardless of whether the element actually exists in the DOM. This is a stub implementation that was never completed.
- **Impact:** Users relying on `element_exists` assertions get false confidence -- assertions pass even when elements don't exist. This is the most impactful stub in the codebase.
- **Recommendation:** Implement actual DOM element checking via `page.evaluate(selector => document.querySelector(selector) !== null, selector)` before the agent session closes. Alternatively, document that `element_exists` assertions are not functional and recommend `text_exists` or `url_contains` instead.
- **RESEARCH Reference:** Pitfall 8 (Assertion Service Element Check Stub) -- confirmed.
- **CONCERNS.md Reference:** Confirmed -- "check_element_exists always returns True when is_done".

### [P2] assertion_service.py:54-61 -- check_url_contains correctly checks final URL
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Uses `_check_attribute` with `history.final_result.url` path and `lambda a, e: e in a` for substring matching. The generic `_check_attribute` helper properly handles None/missing attributes with fallback messages. Correct implementation.
- **Recommendation:** None needed.

### [P2] assertion_service.py:63-68 -- check_text_exists correctly checks extracted_content
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Uses `_check_attribute` with `history.final_result.extracted_content` path. The `_check_attribute` helper resolves the dotted attribute path via getattr chain, with proper None guards at each level.
- **Recommendation:** None needed.

### [P2] assertion_service.py:70-86 -- check_no_errors correctly checks is_done flag
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Returns `(history.is_done, ...)` which is True when the agent completed successfully. Correct implementation.
- **Recommendation:** None needed.

### [P2] assertion_service.py:24-52 -- `_check_attribute` generic helper is well-designed
- **Severity:** N/A (verified correct)
- **Category:** Architecture
- **Description:** The generic `_check_attribute` method with dotted path resolution, optional check_fn, and fallback_message is a clean abstraction that eliminates repetitive try/except blocks. It handles None propagation at each path level correctly.
- **Recommendation:** None needed.

### event_manager.py (156 lines)

### [P2] event_manager.py:27 -- `_events` dict grows indefinitely, cleanup() is never called
- **Severity:** Medium
- **Category:** Performance
- **Description:** `self._events` stores all SSE events per run_id as a `defaultdict(list)`. Events are appended at line 47 but only removed by `cleanup()` at line 140-152. However, `cleanup()` is never called anywhere in the codebase (verified by grep). After hundreds of runs, all event histories remain in memory. Each event is an SSE string (typically 200-500 bytes), so 1000 runs with 20 events each would accumulate ~10MB.
- **Impact:** Gradual memory growth in long-running server processes. For typical usage patterns (10-50 runs per day with server restarts), this is negligible. For 24/7 production deployment, it becomes a memory leak.
- **Recommendation:** Call `event_manager.cleanup(run_id)` after each run completes. Add it to `_finalize_run` in run_pipeline.py. Alternatively, add TTL-based cleanup with a background task.
- **CONCERNS.md Reference:** Confirmed -- "Event manager memory leak".

### [P2] event_manager.py:84-85 -- Heartbeat task overwritten on re-subscribe for same run_id
- **Severity:** Medium
- **Category:** Correctness
- **Description:** Line 85 stores heartbeat task as `self._heartbeat_tasks[run_id] = heartbeat_task`. If `subscribe()` is called multiple times for the same run_id (e.g., frontend reconnect), the previous heartbeat task reference is overwritten but NOT cancelled. The old task continues running, publishing to its own subscriber queue which has been removed from `_subscribers`. However, the queue itself is not garbage collected because the task holds a reference to it via the closure.
- **Impact:** Each re-subscribe creates an orphaned heartbeat task that runs until `is_finished(run_id)` returns True. For a long-running test with multiple reconnects, this accumulates orphaned tasks. Each task wakes every 20 seconds and iterates `_subscribers[run_id]` which may be empty -- minimal CPU cost but unbounded accumulation.
- **Recommendation:** Before creating a new heartbeat task at line 84, check if one already exists for the run_id and cancel it:
  ```python
  if run_id in self._heartbeat_tasks:
      self._heartbeat_tasks[run_id].cancel()
  ```
- **RESEARCH Reference:** Pitfall 5 (EventManager Heartbeat Task Leak) -- confirmed.

### [P2] event_manager.py:87-101 -- History replay for late subscribers works correctly
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Lines 89-94 iterate `_events[run_id]` to replay history before switching to live events. The `is_finished` check at line 93 handles the case where the run completed before the subscriber connected. The `yield` statement makes this a proper async generator that FastAPI can stream via SSE.
- **Recommendation:** None needed.

### [P2] event_manager.py:102-116 -- Finally block properly cleans up subscriber and heartbeat
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** The finally block at lines 102-116 handles cleanup: removes the queue from subscribers, cancels the heartbeat task, catches `CancelledError`, and removes the task reference. If `subscribe()` raises before finally (e.g., during history replay at line 90), the finally block still executes and properly cleans up. This is correct.
- **Recommendation:** None needed.

### test_flow_service.py (193 lines)

### [P2] test_flow_service.py:59-60 -- Step number pattern only handles Chinese step format
- **Severity:** Low
- **Category:** Correctness
- **Description:** `_STEP_NUMBER_PATTERN` matches `步骤(\d+)[：:]` which only covers the Chinese step format. Steps written in other formats (e.g., "Step 1:", "1.", "#1") are not shifted. This means the login prefix injection step-offset only works for Chinese-language task descriptions.
- **Impact:** Low -- the application is Chinese-only per project scope. All task descriptions use the Chinese format.
- **Recommendation:** No action needed for current scope. If internationalization is added, extend the pattern to match additional formats.

### [P2] test_flow_service.py:89-98 -- Two-phase substitution order is correctly handled
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** Phase 1 (regex) replaces `{{cached:KEY}}` before Phase 2 (Jinja2) replaces `{{variable}}`. This ordering is critical because Jinja2's `StrictUndefined` would raise on `{{cached:xxx}}` patterns if run first. The code correctly handles this per D-06. The early return at line 158 (`if '{{' not in text`) skips Jinja2 processing when no patterns remain after regex phase, which is an optimization.
- **Recommendation:** None needed.

### [P2] test_flow_service.py:116-123 -- Missing cache key silently replaced with empty string
- **Severity:** Low
- **Category:** Correctness
- **Description:** When a `{{cached:KEY}}` pattern references a key not in `cache_values`, line 121 replaces it with an empty string and logs a warning. This means tasks with typos in cache references silently produce empty values. The task will execute with missing data rather than failing explicitly.
- **Impact:** Silent data loss. A task referencing `{{cached:order_number}}` when the actual key is `{{cached:order_num}}` will execute with an empty string instead of the cached value.
- **Recommendation:** Consider raising an error or returning the original `{{cached:KEY}}` pattern unchanged (to make the typo visible in the task description) instead of replacing with empty string.

### [P2] test_flow_service.py:174-193 -- Step number shifting preserves separator character correctly
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** `_shift_step_numbers` uses regex `步骤(\d+)([：:])` and preserves the separator (full-width or half-width colon) via `match.group(0)[-1]`. The offset is added to the original number. Edge cases: if the offset makes numbers exceed single digits (e.g., step 96 + offset 5 = step 101), the replacement still works correctly because the regex captures any number of digits.
- **Recommendation:** None needed.

### batch_execution.py (107 lines)

### [P2] batch_execution.py:50 -- `self._semaphore._value` accesses asyncio.Semaphore private attribute
- **Severity:** Low
- **Category:** Architecture
- **Description:** Line 50 reads `self._semaphore._value` for logging the effective concurrency. `asyncio.Semaphore` does not expose a public `.value` property. This accesses an internal implementation detail that could change between Python versions (though it has been stable across 3.8-3.13). The underscore prefix signals this is a private attribute.
- **Impact:** If Python's asyncio internals change, the log message shows incorrect concurrency. No functional impact -- the semaphore itself works correctly regardless.
- **Recommendation:** Remove the `_value` access from logging, or use a local variable to track available concurrency instead of relying on internal state.
- **RESEARCH Reference:** Pitfall 9 (BatchExecutionService Semaphore Logging) -- confirmed.

### [P2] batch_execution.py:53-59 -- Task tracking via `self._tasks` but `asyncio.gather` with `return_exceptions=True`
- **Severity:** N/A (verified correct)
- **Category:** Correctness
- **Description:** `self._tasks` stores all `asyncio.Task` objects at line 53-56. `asyncio.gather(*self._tasks, return_exceptions=True)` at line 59 ensures one task failure does not cancel others (per D-10). Exceptions are returned as values, not raised. The `_finalize_batch` method always runs after gather completes.
- **Impact:** Correct implementation. Tasks are properly tracked and isolated.
- **Recommendation:** None needed.

### [P2] batch_execution.py:43 -- `_active_batches` module-level dict prevents GC
- **Severity:** Low
- **Category:** Architecture
- **Description:** `_active_batches[self.batch_id] = self` at line 43 stores a reference to the service instance to prevent garbage collection while the batch is running. It is cleaned up in `_finalize_batch` finally block at line 107. This is a well-known pattern for preventing premature GC of asyncio tasks.
- **Recommendation:** None needed.

## Architecture Analysis

### [ARCH-01] Module Coupling Analysis

#### Coupling Map

The following maps all P1/P2 files and their backend internal imports:

```
run_pipeline.py (API layer)
  -> agent_service.py (core layer)
  -> event_manager.py (core layer)
  -> report_service.py (core layer)
  -> assertion_service.py (core layer)
  -> precondition_service.py (core layer)
  -> external_precondition_bridge (core layer)
  -> step_code_buffer.py (core layer)
  -> error_utils.py (core layer)
  -> config.get_settings (config layer)
  -> db.database, db.repository, db.schemas (data layer)
  -> test_flow_service.py (lazy import)
  -> account_service.py (lazy import)
  -> cache_service.py (lazy import)
  Total: 13+ module dependencies

agent_service.py (core layer)
  -> monitored_agent.py (agent layer)
  -> stall_detector.py (agent layer)
  -> pre_submit_guard.py (agent layer)
  -> task_progress_tracker.py (agent layer)
  -> action_utils.py (agent layer)
  -> prompts.py (agent layer)
  -> dom_patch.py (agent layer)
  -> llm.factory (llm layer)
  -> utils.run_logger (utils layer)
  Total: 9 module dependencies

monitored_agent.py (agent layer)
  -> action_utils.py (agent layer)
  -> pre_submit_guard.py (agent layer)
  -> stall_detector.py (agent layer)
  -> task_progress_tracker.py (agent layer)
  -> browser_use (external)
  Total: 5 module dependencies

step_code_buffer.py (core layer)
  -> action_translator.py (core layer)
  -> code_generator.py (core layer)
  Total: 2 module dependencies

code_generator.py (core layer)
  -> action_translator.py (core layer)
  Total: 1 module dependency

precondition_service.py (core layer)
  -> cache_service.py (core layer)
  -> external_precondition_bridge (core layer)
  -> random_generators.py (core layer)
  -> time_utils.py (core layer)
  Total: 4 module dependencies

assertion_service.py (core layer)
  -> api.schemas (API layer -- CROSS-LAYER)
  -> db.repository (data layer)
  -> db.models (data layer)
  Total: 3 module dependencies

event_manager.py (core layer)
  -> (no internal dependencies)
  Total: 0 module dependencies

test_flow_service.py (core layer)
  -> (no internal dependencies)
  Total: 0 module dependencies

batch_execution.py (core layer)
  -> db.database (data layer)
  -> db.repository (data layer)
  -> api.routes.run_pipeline (API layer -- CROSS-LAYER, UPWARD)
  Total: 3 module dependencies

stall_detector.py (agent layer)
  -> (no internal dependencies)
  Total: 0 module dependencies
```

#### Coupling Findings

### [ARCH-01] Coupling: run_pipeline.py -> 13+ modules (God-module pattern)
- **Severity:** High
- **Description:** `run_pipeline.py` imports from 13+ internal modules spanning all layers (API, core, agent, config, data). It serves as the central orchestrator, which is an accepted pattern, but the sheer number of dependencies makes it fragile to changes in any layer. Any refactoring in core, agent, or data layers requires checking run_pipeline for breakage.
- **Recommendation:** The orchestrator pattern is acceptable. However, the lazy imports at lines 148-149 and 448-452 (test_flow_service, account_service, cache_service) suggest these could be constructor-injected or moved to a factory. The 5 unused imports (asyncio, HTTPException, TaskRepository, StepRepository, TaskUpdate) should be removed to reduce noise.

### [ARCH-01] Coupling: batch_execution.py -> api.routes.run_pipeline (upward dependency)
- **Severity:** Medium
- **Description:** `batch_execution.py` (core layer) imports `run_agent_background` from `api.routes.run_pipeline` (API layer). This creates an upward dependency: the core layer depends on the API layer. If the API layer is refactored or the pipeline module is moved, batch_execution breaks. The typical layer convention is API -> core -> data, not core -> API.
- **Recommendation:** Extract `run_agent_background` from `api/routes/run_pipeline.py` into a separate module in `backend/core/` (e.g., `backend/core/run_orchestrator.py`). Both `run_pipeline.py` and `batch_execution.py` would then import from the core layer, eliminating the upward dependency.

### [ARCH-01] Coupling: assertion_service.py -> api.schemas (cross-layer upward)
- **Severity:** Low
- **Description:** `assertion_service.py` (core layer) imports `Assertion` from `backend.api.schemas.index` (API layer). This is an upward dependency where core depends on API schema definitions. The Assertion model is likely a Pydantic schema used for request validation, but the service uses it as a data type for assertion evaluation.
- **Recommendation:** Move the `Assertion` schema to `backend/db/schemas.py` (where other data schemas live) or create a shared types module. Services should not depend on API-layer schemas.

### [ARCH-01] Coupling: agent_service.py <-> monitored_agent.py (bidirectional knowledge)
- **Severity:** Medium
- **Description:** `agent_service.py` creates and configures `MonitoredAgent` (line 580-592 in full file), passing detectors and callbacks. `MonitoredAgent` internally runs those same detectors in its own step callback. Both files need to know about the detector interface (StallDetector, PreSubmitGuard, TaskProgressTracker). Changes to detector signatures require updating both files. The dual stall/progress tracking finding (Cross-2, agent_service.py:340-347) is a direct consequence of this coupling.
- **Recommendation:** Consolidate detector execution into one location. MonitoredAgent should be the sole owner of detector execution (since it owns the browser-use callback lifecycle). Agent_service should provide configuration but not duplicate detector calls.

### [ARCH-01] Coupling: external_precondition_bridge -> external_module_loader (facade coupling)
- **Severity:** Low
- **Description:** The bridge module re-exports from three split modules (loader, discovery, engine). This is a clean facade pattern. The coupling is intentional and well-managed via `noqa: F401` annotations. Changes to any of the three underlying modules only affect the bridge, not consumers.
- **Recommendation:** No action needed. The facade pattern is appropriate.

### [ARCH-01] Coupling: No circular dependencies detected
- **Severity:** N/A
- **Description:** Scanning all import statements across the 31 files, no circular import cycles were found. The lazy imports in run_pipeline.py (lines 148-149, 302, 448-452, 553) are used for optional dependencies and do not indicate circularity -- they exist for import-time optimization, not cycle avoidance.
- **Recommendation:** None needed.

### [ARCH-02] Abstraction Analysis

### [ARCH-02] Abstraction: assertion_service.py -- element_exists check is a misleading stub (under-abstraction)
- **Type:** Under-abstraction
- **Severity:** High
- **Description:** `check_element_exists` presents a clean interface (`selector -> (bool, str, str)`) but the implementation is a stub that ignores the selector entirely. The method signature implies DOM element checking but the body performs a completion-status check instead. This is misleading to consumers who expect actual element verification.
- **Recommendation:** Either (a) implement actual element checking, or (b) rename to `check_completion_status` and document that `element_exists` assertion type maps to completion checking. The current state creates false confidence in test results.

### [ARCH-02] Abstraction: PreSubmitGuard -- dead logic from None parameters (wrong abstraction level)
- **Type:** Wrong level
- **Severity:** Medium
- **Description:** PreSubmitGuard's `check()` method accepts `actual_values` and `submit_button_text` parameters, but the caller (MonitoredAgent) always passes None. The guard's core logic (comparing actual vs. expected form values) is unreachable. The abstraction exists at the wrong level -- DOM value extraction should be the guard's responsibility, not the caller's. By requiring the caller to extract DOM values, the guard's utility depends on caller cooperation, which hasn't been implemented.
- **Recommendation:** Refactor PreSubmitGuard to extract DOM values internally via `page.evaluate()`, removing the need for callers to provide them. The guard should be self-contained: given a page object and the expected form state, determine whether to block the submit.

### [ARCH-02] Abstraction: step_code_buffer.py -- duplicate wait logic between _derive_wait and assemble (wrong abstraction boundary)
- **Type:** Wrong level
- **Severity:** Medium
- **Description:** Wait logic is split across two methods: `_derive_wait()` adds wait code BEFORE actions (pre-click 3000ms), and `assemble()` adds stability waits AFTER click actions (networkidle + 500ms). The pre-click vs. post-click distinction is not clearly documented, and the total wait per click action (~6.5s) is an emergent property of both methods working together. Neither method alone has complete knowledge of the wait strategy.
- **Recommendation:** Consolidate wait logic into one location. Either `_derive_wait` should own all waits for an action (pre + post), or `assemble` should own all timing. The current split makes it difficult to reason about total wait time or adjust the strategy.

### [ARCH-02] Abstraction: _check_attribute in assertion_service.py (good abstraction)
- **Type:** Good abstraction
- **Severity:** N/A
- **Description:** The `_check_attribute` generic helper properly abstracts the common pattern of dotted-path attribute access with None guards, optional comparison, and fallback messages. It reduced repetitive try/except blocks across 4 check methods. This is a well-applied abstraction.
- **Recommendation:** None needed.

### [ARCH-02] Abstraction: ContextWrapper dict-like interface (appropriate)
- **Type:** Good abstraction
- **Severity:** N/A
- **Description:** ContextWrapper provides dict-like access (`__getitem__`, `__setitem__`, `__contains__`, `get`, `keys`) plus domain-specific methods (`get_data`, `cache`, `store_assertion_result`). The dict-like interface allows it to be used seamlessly in exec() environments and template substitution, while the domain methods add value. The `to_dict()` method provides a clean exit point for serialization.
- **Recommendation:** None needed.

### [ARCH-02] Abstraction: EventManager pub/sub (clean but incomplete)
- **Type:** Under-abstraction
- **Severity:** Low
- **Description:** EventManager provides clean publish/subscribe semantics with history replay and heartbeat. However, it lacks lifecycle management -- there is no automatic cleanup, no TTL, no maximum event count. The `cleanup()` method exists but is never called. The abstraction is clean but incomplete.
- **Recommendation:** Add automatic cleanup integration (call `cleanup` in `_finalize_run` or add TTL-based cleanup).

### [ARCH-02] Abstraction: StallDetector frozen results (appropriate immutability)
- **Type:** Good abstraction
- **Severity:** N/A
- **Description:** `StallResult` and `FailureDetectionResult` are frozen dataclasses, preventing mutation after construction. This is consistent with project coding conventions and prevents subtle bugs from shared mutable state.
- **Recommendation:** None needed.

## Summary

### Findings by Severity
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 14 |
| Low | 16 |
| Info/N/A | 21 |
| **Total** | **53** |

Note: Total includes N/A (verified correct) entries and 2 verified-ok corrections. Actionable findings (Critical+High+Medium+Low) = 32.

### Findings by Category
| Category | Count |
|----------|-------|
| Correctness | 19 |
| Architecture | 18 |
| Performance | 6 |
| Security | 5 |
| N/A (verified) | 4 |

### Findings by Layer
| Layer | Count |
|-------|-------|
| Pipeline (run_pipeline.py) | 7 |
| Agent Service (agent_service.py) | 7 |
| Code Generation (code_generator.py, step_code_buffer.py) | 8 |
| Agent Layer (monitored_agent.py, stall_detector.py, pre_submit_guard.py) | 8 |
| Supporting Services (precondition, assertion, event_manager, test_flow, batch) | 17 |
| External Integration (external_*.py) | 2 |
| Cross-cutting (coupling/abstraction analysis) | 3 |

### Top 5 Findings (by severity + impact)

1. **[P2] assertion_service.py:88-110 -- check_element_exists is a stub that always returns True.** Element existence assertions provide zero actual verification. Users get false confidence in test results. (High/Correctness)

2. **[P1] agent_service.py:340-347 -- Dual stall detection inflates failure counts to half the configured threshold.** StallDetector.check() is called twice per step (once in MonitoredAgent, once in agent_service), recording duplicate history entries. The agent intervenes prematurely. (High/Correctness)

3. **[P1] step_code_buffer.py:131-133,380-395 -- Excessive wait times in generated test code (~6.5s per click).** Pre-click 3000ms wait (misplaced) + post-click networkidle 3000ms timeout + 500ms stability wait per click action. A 10-click test accumulates ~65 seconds of waits. (Medium/Performance)

4. **[P2] event_manager.py:84-85 -- Heartbeat task leak on re-subscribe.** Old heartbeat task not cancelled when new subscriber connects, creating orphaned tasks. (Medium/Correctness)

5. **[P1] agent_service.py:127 -- Synchronous file write in async method blocks event loop.** `save_screenshot()` performs blocking I/O in async context, stalling SSE events and concurrent runs. (Medium/Performance)

### Confirmed CONCERNS.md Issues

| CONCERNS.md Entry | Status | Finding Reference |
|-------------------|--------|-------------------|
| exec() for user-provided code | Confirmed | P2 precondition_service.py:243 |
| Monkey-patching browser-use internals | Confirmed (P3, out of deep-dive scope) | P3 dom_patch.py |
| Manual schema migrations in init_db() | Not reviewed (data layer, out of scope) | N/A |
| Duplicated LLM configuration paths | Not reviewed (config layer, out of scope) | N/A |
| Module-level mutable global state | Confirmed | P3 external_module_loader.py:17-43 |
| 8-character UUID collision risk | Not reviewed (data layer, out of scope) | N/A |
| Batch fire-and-forget execution | Confirmed | P2 batch_execution.py:43 |
| Event manager memory leak | Confirmed | P2 event_manager.py:27 |
| CORS allows all origins | Not reviewed (API layer, out of scope) | N/A |
| No authentication or authorization | Not reviewed (API layer, out of scope) | N/A |
| Stack traces exposed in production | Not reviewed (API layer, out of scope) | N/A |
| Credentials in generated test files | Confirmed | P1 code_generator.py:198-201 |
| SQLite connection pool for concurrent writes | Not reviewed (data layer, out of scope) | N/A |
| selectinload N+1 on task list | Not reviewed (data layer, out of scope) | N/A |
| DOM serialization and hashing on every step | Confirmed | P1 agent_service.py:400-413 |
| Screenshot base64 decode on every step | Confirmed | P1 agent_service.py:127 |

### New Issues Not in CONCERNS.md

1. **Dual stall detection** (High) -- same detector called twice per step, inflating failure counts
2. **external_assertion_summary leaks into variable_map** (Medium) -- filter does not match "external_assertion" prefix (latent gap, currently mitigated by isinstance guard)
3. **Pre-click wait misplaced** (Medium) -- 3000ms wait before click, not after
4. **Potential IndexError in multi-action step callback** (Medium) -- all_actions index may diverge from agent_output.action index
5. **Unescaped assertion expected values in generated code** (Medium) -- double quotes break Python syntax
6. **Heartbeat task leak on re-subscribe** (Medium) -- old task not cancelled when new subscriber connects
7. **Fragile attribute setting on BrowserSession** (Medium) -- `_pre_navigated` dynamic attribute
8. **auth_service.py response variable scope** (Medium) -- `response.text` in except handler may be unbound

---

*Findings documented: 2026-05-03*
*Breadth scan (P3) completed: 2026-05-03*
*Deep-dive (P1) completed: 2026-05-03*
*Supporting services (P2) completed: 2026-05-03*
*Architecture analysis (ARCH-01/ARCH-02) completed: 2026-05-03*
