# Domain Pitfalls: ERP Integration (CacheService, AccountService, TestFlowService)

**Domain:** Adding run-scoped caching, multi-account login, test flow orchestration, and Excel template changes to an existing FastAPI + Playwright test automation platform (v0.9.1)
**Researched:** 2026-04-11
**Context:** v0.9.1 milestone -- CacheService, AccountService, TestFlowService, DB migration, Excel template update, Jinja2 variable replacement
**Confidence:** HIGH (based on direct code analysis of all affected files, SQLite documentation, Jinja2 behavior, and established patterns from previous milestone pitfalls)

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: Jinja2 StrictUndefined Crashes on {{cached:key}} Syntax

**What goes wrong:**
The existing `PreconditionService.substitute_variables()` (line 336-361 in `precondition_service.py`) uses Jinja2 with `StrictUndefined`. When the task description contains `{{cached:i}}`, Jinja2 interprets `cached:i` as a variable name lookup, cannot find it in the context dict, and throws `UndefinedError`. The entire run fails before the agent even starts.

The implementation plan's `TestFlowService._build_description()` uses regex to replace `{{cached:key}}` before Jinja2 processing. But the existing substitution in `run_agent_background()` (line 145 in `runs.py`) calls `PreconditionService.substitute_variables(task_description, context)` FIRST, before TestFlowService ever runs. The order of operations is wrong.

**Why it happens:**
There are two substitution points in the system:
1. Line 145 in `runs.py`: `PreconditionService.substitute_variables(task_description, context)` -- runs during existing flow
2. TestFlowService: regex replacement of `{{cached:key}}` then Jinja2 -- runs during new flow

If both run, or if the old substitution runs on text with `{{cached:key}}`, it crashes. The design doc assumes TestFlowService handles everything, but the existing `run_agent_background` function still runs substitution at line 145 for backward compatibility.

**Consequences:**
- Any task description containing `{{cached:i}}` fails with `UndefinedError: 'cached:i' is undefined`
- Run fails before agent starts, stuck in "failed" status
- No clear error message -- QA users see a cryptic Jinja2 error

**How to avoid:**
1. In `run_agent_background`, the `if task.login_role` branch must skip the existing `substitute_variables()` call entirely and delegate ALL substitution to TestFlowService
2. TestFlowService must do regex-based `{{cached:key}}` replacement BEFORE passing the result to Jinja2
3. Ensure the `{{cached:key}}` regex pattern is removed from the string before Jinja2 sees it: `re.sub(r'\{\{cached:(\w+)\}\}', replace_cached, text)` must produce a string with zero `{{cached:...}}` patterns
4. Add a guard: after regex replacement, verify no `{{cached:` patterns remain before calling Jinja2

**Warning signs:**
- `UndefinedError` in run logs mentioning "cached" or colon in variable name
- Tasks with `{{cached:key}}` in description always fail immediately
- Run fails at the precondition/variable-substitution phase, never reaches agent execution

**Phase to address:**
TestFlowService (Task 6-7 in implementation plan) -- the substitution order must be designed before wiring into `runs.py`

**Confidence:** HIGH -- direct code analysis of `precondition_service.py` line 336-361 (StrictUndefined), `runs.py` line 145 (substitute_variables call), and the `{{cached:key}}` syntax in the design doc

---

### Pitfall 2: Step Numbering Shift Breaks Step Tracking and SSE Events

**What goes wrong:**
The design doc injects 5 login steps before the user's steps. The implementation plan shifts user step numbers by +5 (e.g., "step 1" becomes "step 6"). But the `on_step` callback in `runs.py` uses the step number directly from the agent to save to the database as `step_index`. The SSE events and the step timeline in the UI expect sequential integers starting from 1.

If the injected login steps produce steps 1-5 from the agent, and the user's first step is step 6, the agent's internal step counter will actually be 1, 2, 3, 4, 5, 6, 7... -- NOT 6, 7, 8, 9, 10, 11... The "shift by +5" in the task description text does NOT change the agent's step counter. The agent starts counting from 1 regardless of what the task description says.

Meanwhile, the `global_seq` counter in `runs.py` (line 83) tracks sequence numbers for precondition results, steps, and assertions on a single timeline. If precondition results get seq 1-3, and agent steps get step_index 1-10 from the agent callback, the sequence numbering and step_index numbering diverge.

**Why it happens:**
The implementation plan shifts the step numbers in the task description TEXT (`re.sub(r'^步骤(\d+)[:：]', ...)`), but this only changes what the AI reads. The agent's internal step counter starts from 1 regardless. The `step_callback` receives the agent's internal step number, not the number in the text.

**Consequences:**
- Database steps show step_index 1-5 (login) then 6+ (user), but the agent reports step 1-10 internally. The step_index and the text step numbers do not match.
- Step timeline in the UI shows confusing numbering
- The `sequence_number` (global timeline) and `step_index` (per-run) become inconsistent
- Precondition results already consumed sequence numbers 1-N, then steps start at step_index 1 with sequence_number N+1

**How to avoid:**
1. Do NOT shift step numbers in the task description. Let the agent number steps naturally (1, 2, 3...). The login steps will be steps 1-5, user steps will be 6+ in the agent's output.
2. Mark injected login steps differently: add a metadata field like `is_login_step: true` to the step data in the database
3. Use `global_seq` for timeline ordering (already implemented in Phase 59). Precondition results, login steps, user steps, and assertions all get sequential `sequence_number` values. The `step_index` is the agent's raw counter.
4. Test this end-to-end: verify that a task with login_role produces correct step_index and sequence_number values in the database

**Warning signs:**
- Steps in the database have step_index values that do not match the step numbers in the action text
- UI timeline shows steps out of order or with gaps
- Steps with the same step_index but different sequence_numbers

**Phase to address:**
TestFlowService (Task 6-7) -- step numbering strategy must be decided before building the description builder

**Confidence:** HIGH -- direct code analysis of `on_step` callback (runs.py line 164-210), `global_seq` counter (line 83), and `MonitoredAgent` step numbering behavior

---

### Pitfall 3: Excel Template Column Position Change Breaks Old Template Imports

**What goes wrong:**
The current `TEMPLATE_COLUMNS` in `excel_template.py` defines columns as: name, description, target_url, max_steps, preconditions, assertions (6 columns). The new template changes this to: name, login_role, description, max_steps, preconditions, assertions (6 columns, target_url removed, login_role inserted at position 2).

The parser (`excel_parser.py`) maps columns by INDEX position using `TEMPLATE_COLUMNS` -- it iterates `for col_idx, col_def in enumerate(TEMPLATE_COLUMNS)` and reads the cell at that column index. The header validation (`_validate_headers`) checks that row 1 headers match `TEMPLATE_COLUMNS`.

When a user uploads an OLD template (without login_role, with target_url at position 2), the header validation will catch the mismatch and reject the file. This is GOOD. But the error message will be cryptic: "column 2 header should be 'login_role', actual is 'task description'" -- confusing for QA users who just downloaded the template last week.

**Why it happens:**
The template changed fundamentally -- a column was inserted and another was removed. The parser relies on exact header matching. There is no backward compatibility or version detection.

**Consequences:**
- All existing Excel files become invalid
- QA users must re-download templates and reformat their test cases
- No migration path for existing Excel data
- Error messages do not explain what changed or how to fix it

**How to avoid:**
1. Keep `target_url` in the new template. Add `login_role` as a new column. This preserves backward compatibility: old files are still parseable (login_role column missing = use default), and new files work too.
2. If removing `target_url` is required, add template version detection: include a version number in a cell or a named range (e.g., `B1` says "v2"). The parser checks version and selects the appropriate column mapping.
3. At minimum, provide a clear migration error message: "This template uses the old format. Please download the new template from [link]. Changes: 'target URL' column removed, 'login role' column added at position 2."
4. Update the README sheet in the template to include the version and a changelog.

**Warning signs:**
- Import fails on any Excel file created before the update
- Error message references wrong column names
- Users report "template worked yesterday, broken today"

**Phase to address:**
Excel template update (Task 5) -- backward compatibility decision must be made before modifying TEMPLATE_COLUMNS

**Confidence:** HIGH -- direct code analysis of `excel_parser.py` (header validation at line 104-123, column iteration at line 174), and `excel_template.py` TEMPLATE_COLUMNS definition

---

### Pitfall 4: ContextWrapper Constructor Change Breaks Existing Code Paths

**What goes wrong:**
The implementation plan changes `ContextWrapper.__init__` to accept an optional `cache` parameter: `def __init__(self, cache: CacheService | None = None)`. The existing code creates `ContextWrapper` instances in two places:

1. `PreconditionService.__init__` (line 203): `self.context: ContextWrapper = ContextWrapper()` -- this is fine, the parameter is optional
2. `runs.py` line 267-269: manual `ContextWrapper()` creation for external assertions:
```python
if not isinstance(context, ContextWrapper):
    context_wrapper = ContextWrapper()
    context_wrapper._data = context.copy() if context else {}
else:
    context_wrapper = context
```

The second case is problematic: when `login_role` is set, the `PreconditionService` creates a `ContextWrapper` with a `CacheService`, but when `login_role` is NOT set (backward compatibility), the existing code creates a bare `ContextWrapper()` without a cache. Then when `execute_all_assertions` tries to use `context_wrapper.cache()` or `context_wrapper.cached()`, it creates a default `CacheService()` that is not shared with the one from `PreconditionService`.

More critically, the `PreconditionService` instance is only created inside the `if preconditions:` block (runs.py line 88-89). If there are no preconditions but there IS a `login_role`, the `PreconditionService` and its `ContextWrapper` are never created. The `context` variable remains an empty dict `{}` (line 86). The assertion code at line 267 checks `isinstance(context, ContextWrapper)` -- this returns `False` for a plain dict, so it creates a new `ContextWrapper()`. This new instance has no cache and no precondition data.

**Why it happens:**
The `ContextWrapper` is created in multiple places with different ownership. The precondition path creates one, the assertion path creates another. Adding cache to `ContextWrapper` without unifying the creation point leads to split-brain state.

**Consequences:**
- Cache data from preconditions is invisible to assertions
- Assertion code calling `context.cached('i')` gets `KeyError` because the assertion's ContextWrapper has a different CacheService
- Runs fail with cryptic "cache key 'i' does not exist" errors during assertion phase

**How to avoid:**
1. Create ONE `CacheService` instance at the top of `run_agent_background`, before any branching
2. Pass the SAME `CacheService` to both `PreconditionService` and assertion execution
3. If `login_role` is set, always create a `ContextWrapper` with the shared `CacheService`, even if there are no preconditions
4. Test the path: task with `login_role` but NO preconditions, followed by assertions that use `cached()` -- this is the most fragile path

**Warning signs:**
- `KeyError` in assertion execution saying "cache key does not exist"
- Assertion results show "execution error" instead of "pass/fail"
- Cache data visible in precondition results but missing in assertion context

**Phase to address:**
TestFlowService wiring (Task 7) -- the shared CacheService lifecycle must be designed as part of the `run_agent_background` refactor

**Confidence:** HIGH -- direct code analysis of `runs.py` lines 86-147 (precondition block), lines 263-362 (assertion block), and `ContextWrapper` usage in both blocks

---

### Pitfall 5: Account Credentials Leak into Agent Logs and Screenshots

**What goes wrong:**
The `build_login_prefix()` function injects account and password directly into the task description text: `"2. Enter {account} in the account input box\n3. Enter {password} in the password input box"`. This text becomes the agent's task string. The agent may include this text in:
1. Step action logs: `action = "input_text: Y59800075"` -- saved to database
2. Reasoning logs: `"I entered password Aa123456 into the field"` -- saved to database
3. Screenshots: if the password field shows the actual characters before masking
4. The `RunLogger` structured logs in `data/outputs/{run_id}/` directory
5. The task description stored in the `steps` table via `add_step()`

The current system saves all step actions and reasoning to SQLite without any filtering. Reports display these logs to the user. If the server is shared or if reports are exported, credentials are exposed.

**Why it happens:**
The design puts credentials in the task description because the AI agent needs to know what to type. There is no masking layer between the agent's output and the database/logs.

**Consequences:**
- All account credentials stored in plain text in SQLite `steps` table
- Credentials visible in the test report UI
- Credentials in log files on the server
- If database is backed up (daily cron job per deployment notes), credentials persist in backups

**How to avoid:**
1. Short term: accept that credentials appear in agent output. This is a test automation tool running locally, not a public SaaS. Document this limitation.
2. Medium term: add a post-processing step in `on_step()` that redacts known credential patterns from the `action` and `reasoning` strings before saving to the database
3. Masking pattern: before saving, replace `account_info.account` with `[ACCOUNT]` and `account_info.password` with `[PASSWORD]` in action/reasoning text
4. Never log credentials at INFO level. The `run_agent_background` already logs account info at line 848: `logger.info(f"[{run_id}] login role: {login_role}, account: {account_info.account}")` -- remove the account value from this log line

**Warning signs:**
- Plain text passwords visible in the test report step timeline
- Log files containing account credentials
- Database queries on `steps` table returning credential strings

**Phase to address:**
TestFlowService wiring (Task 7) -- add masking to the `on_step` callback as part of the integration

**Confidence:** HIGH -- direct code analysis of `on_step` callback (runs.py line 164-210), `build_login_prefix()` in implementation plan, and `RunLogger` usage in `agent_service.py`

---

### Pitfall 6: SQLite Migration Fails on Existing Database with Data

**What goes wrong:**
The implementation plan adds `login_role` to the Task model and runs `ALTER TABLE tasks ADD COLUMN login_role VARCHAR(20)`. The existing `init_db()` in `database.py` (lines 39-64) already has a pattern for this: check `PRAGMA table_info(tasks)`, add column if missing.

But there are two problems:

1. **Gunicorn with 2 workers**: Each worker calls `init_db()` on startup. If both workers try to `ALTER TABLE` simultaneously, one gets `sqlite3.OperationalError: duplicate column name` because SQLite's `ALTER TABLE ADD COLUMN` is not idempotent in concurrent scenarios. The existing pattern checks `PRAGMA table_info` first, which should prevent this -- but if both workers read the PRAGMA result BEFORE either has executed the ALTER, both proceed and one fails.

2. **Existing data has NULL values**: All existing tasks will have `login_role = NULL`. The code must handle `task.login_role is None` everywhere. The implementation plan makes it `Optional[str]` in the model, which is correct. But the Excel parser sets `login_role` as `required: True` in the new template. Existing tasks in the database that were created via the old template have no `login_role`. The frontend task detail page will show `login_role: null`, which the dropdown should handle (show "unselected" state).

**Why it happens:**
SQLite's `ALTER TABLE ADD COLUMN` is a DDL operation that acquires a write lock. With Gunicorn's 2 workers, both run `init_db()` at startup. The check-then-alter pattern has a race condition.

**Consequences:**
- One worker crashes on startup with "duplicate column name" error
- Gunicorn restarts that worker, which retries and succeeds (because the other worker already added the column)
- Intermittent startup failures in production
- Existing tasks have `NULL` login_role, which must be handled in every code path

**How to avoid:**
1. Wrap the ALTER TABLE in a try/except for `OperationalError` with "duplicate column" in the message. Log a warning and continue. The existing pattern already checks PRAGMA first, but add the exception handler as a safety net.
2. The existing pattern in `database.py` (lines 48-63) already does this correctly for `sequence_number` and `batch_id`. Follow the same pattern for `login_role`.
3. In the frontend, handle `login_role: null` by showing an empty/unselected dropdown state
4. In `run_agent_background`, check `if task.login_role` (falsy check on None) to branch between new flow and existing flow. None and empty string both skip the new flow.

**Warning signs:**
- "duplicate column name" errors in server startup logs
- Worker restart in Gunicorn logs after deployment
- Tasks created before the update show no login role in the UI

**Phase to address:**
DB migration (Task 4) -- follow the existing migration pattern in `database.py` exactly

**Confidence:** HIGH -- direct code analysis of `database.py` init_db (lines 39-64), existing migration patterns for sequence_number and batch_id columns

---

### Pitfall 7: Cache Precondition Type ("cache") Conflicts with Existing Precondition Parsing

**What goes wrong:**
Existing preconditions are stored as a JSON array of strings: `["code1", "code2"]`. Each string is Python code executed via `exec()`. The new design introduces a JSON object format for cache-type preconditions: `{"type": "cache", "method": "PcImport.inventory_list", "params": {...}, "cache_key": "i", "cache_field": "imei"}`.

The existing parsing in `run_agent_background` (runs.py line 443-449) does:
```python
preconditions = json.loads(task.preconditions)
```
This returns a list. Then it iterates:
```python
for i, code in enumerate(preconditions):
    if not code.strip():
        continue
    result = await precondition_service.execute_single(code, i)
```

If `code` is a dict (the new cache-type precondition), `code.strip()` will crash with `AttributeError: 'dict' object has no attribute 'strip'`. The existing precondition execution path does not handle dict-type preconditions.

**Why it happens:**
The existing code assumes every element in the preconditions list is a string (Python code). The new format mixes strings and dicts in the same array.

**Consequences:**
- Any task with a cache-type precondition crashes during execution
- `AttributeError` in run logs
- Run stuck in "failed" status

**How to avoid:**
1. Before iterating preconditions, check each element's type:
```python
for i, item in enumerate(preconditions):
    if isinstance(item, dict):
        # Cache-type precondition
        result = await precondition_service.execute_cache_precondition(json.dumps(item), i)
    elif isinstance(item, str):
        if not item.strip():
            continue
        result = await precondition_service.execute_single(item, i)
    else:
        logger.warning(f"Precondition {i}: unexpected type {type(item)}")
        continue
```
2. This type-dispatching must happen in BOTH the new TestFlowService path AND the existing `run_agent_background` path (for backward compatibility with tasks that have mixed precondition types)

**Warning signs:**
- `AttributeError: 'dict' object has no attribute 'strip'` in run logs
- Precondition execution fails immediately for tasks with cache-type preconditions
- Runs that worked before the update now fail

**Phase to address:**
Cache precondition execution (Task 8) -- the type-dispatching must be built into the precondition iteration loop

**Confidence:** HIGH -- direct code analysis of `runs.py` line 443-449 (precondition parsing), line 88-142 (precondition execution loop), and the new precondition format in the design doc

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Two separate execution paths in `run_agent_background` (if/else on login_role) | Preserves backward compatibility without refactoring existing code | Divergent execution paths become harder to maintain; bug fixes must be applied to both paths | MVP only -- plan to unify into TestFlowService for all tasks after validation |
| Regex-based `{{cached:key}}` replacement instead of custom Jinja2 extension | Simpler to implement, no Jinja2 subclassing | Fragile regex can break on edge cases (e.g., `{{cached:i}}` inside a Jinja2 expression) | Acceptable if regex is simple and well-tested; document limitations |
| Hardcoded login step count (5 steps) in shift logic | Simple implementation | If login flow changes (e.g., 2FA added), step shift breaks | Never -- instead, do not shift step numbers at all (see Pitfall 2) |
| Reading user_info.py via import from sys.path | Reuses existing config file from webseleniumerp | Tight coupling to external project's file structure; breaks if webseleniumerp restructures | Acceptable for now -- webseleniumerp is a stable external project owned by the same team |
| Storing preconditions as mixed string/dict JSON array | No schema change needed for preconditions column | Type ambiguity requires isinstance checks everywhere preconditions are processed | Acceptable for MVP -- consider a proper precondition schema in a future milestone |

## Integration Gotchas

Common mistakes when connecting to external services/libraries.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Jinja2 + `{{cached:key}}` syntax | Passing `{{cached:key}}` to Jinja2 with StrictUndefined, causing UndefinedError | Regex-replace `{{cached:key}}` patterns BEFORE Jinja2 processing, then run Jinja2 on the cleaned string |
| SQLite ADD COLUMN with Gunicorn 2 workers | Both workers run ALTER TABLE simultaneously, one gets "duplicate column" error | Check PRAGMA table_info + wrap ALTER TABLE in try/except OperationalError |
| Excel parser + TEMPLATE_COLUMNS change | Parser uses column index, so inserting a column shifts all subsequent columns | Parser maps by header name (already validates headers), but old templates with different headers will be rejected with a clear message |
| ContextWrapper + CacheService lifecycle | Creating separate CacheService instances for preconditions and assertions | Create ONE CacheService at the top of `run_agent_background`, pass it to all services |
| Precondition list + mixed types (string/dict) | Iterating `for code in preconditions` and calling `.strip()` on dict elements | Type-check each element: `isinstance(item, dict)` for cache type, `isinstance(item, str)` for code type |
| AccountService + user_info.py import | Importing from sys.path that may not be configured when AccountService is created | Use the existing `external_precondition_bridge.configure_external_path()` to ensure path is set before importing |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| CacheService storing large API responses in memory | Memory grows during batch execution with many cache-heavy tasks | CacheService should store only extracted field values, not full API responses. Add a size limit per key (e.g., 1KB) | 10+ parallel runs with large API responses cached |
| Regex replacement on very long task descriptions | Slow variable substitution for tasks with 50+ steps | The regex `{{cached:(\w+)}}` is fast for reasonable inputs. No action needed unless descriptions exceed 10KB | Unlikely to break -- typical task descriptions are < 5KB |
| AccountService importing user_info.py on every run | sys.path manipulation and module import on every `AccountService()` creation | Cache the config dict at module level (like existing `_login_api_instance` pattern in external_precondition_bridge) | 100+ sequential runs per batch |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Credentials in agent task description | Plain text passwords saved in SQLite steps table, visible in UI reports | Post-process step action/reasoning to mask known credential values before database save |
| Credentials in server logs | `logger.info` with account info visible in `journalctl` | Remove account value from log lines; log only the role name |
| Credentials in backup files | Daily database backup contains all credential instances in steps table | Short-term: acceptable for local tool. Medium-term: implement step-data encryption or credential redaction |
| user_info.py credentials readable by service | Service runs as root, config file has plaintext passwords | This is the existing deployment pattern. Changing it requires a broader security review. |

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Old Excel template silently rejected with cryptic error | QA users do not understand "column 2 header should be 'login role', actual is 'task description'" | Provide version-specific error: "This template uses the v1 format. Please download the latest template." |
| login_role required in new template but optional in UI | Users confused about whether login role is mandatory | Make login_role optional in the template with default "main". Most tasks use the main account. |
| No preview of injected login steps | Users cannot see what the agent will actually execute (login + their steps) | Show the full composed task description in the run detail view, with login steps highlighted differently |
| Cache key naming is opaque | Users do not know what `{{cached:i}}` means in the step description | Provide autocomplete or a "cached variables" panel showing available cache keys and their current values |
| Role names in English (main, special, vice) | QA users are Chinese speakers, role names are technical | Use Chinese labels in the dropdown: "main account (main)", "warehouse account (special)" etc. |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **CacheService integration:** Often missing the shared lifecycle -- verify that the SAME CacheService instance is used by both preconditions and assertions (check by testing a task with cache precondition + cache assertion)
- [ ] **Backward compatibility:** Often missing the path where `login_role is None` -- verify that tasks created before the update still execute correctly without errors
- [ ] **Step numbering:** Often missing the mismatch between text step numbers and agent step_index -- verify by running a task with login_role and checking step_index values in the database
- [ ] **Precondition type dispatching:** Often missing the isinstance check for dict-type preconditions -- verify by creating a task with a cache-type precondition and confirming it does not crash on `.strip()`
- [ ] **Excel old template rejection:** Often missing clear migration messaging -- verify by uploading an old-format template and confirming the error message explains what changed
- [ ] **Credential masking in logs:** Often missing the removal of credential values from log.info calls -- verify by running a task with login_role and checking server logs for plaintext passwords
- [ ] **No-precondition path:** Often missing the case where task has login_role but NO preconditions -- verify that cache assertions still work (CacheService should exist even without preconditions)
- [ ] **Batch execution compatibility:** Often missing the test that batch execution works with login_role tasks -- verify by creating a batch with 3 tasks, some with login_role and some without

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Jinja2 UndefinedError on {{cached:key}} | LOW | Fix substitution order in run_agent_background. Deploy fix. Re-run failed tasks. |
| Step numbering mismatch in database | MEDIUM | No data migration needed -- sequence_number is correct, step_index is just a display label. Fix the frontend to use sequence_number for timeline ordering. |
| Old Excel template rejection | LOW | Add template version detection and clearer error message. No data migration. |
| ContextWrapper split-brain (separate caches) | MEDIUM | Refactor run_agent_background to create CacheService once at the top. Test all paths. |
| Credentials leaked in logs/database | HIGH | Cannot redact retroactively from existing database without a migration script. Add masking going forward. Rotate exposed credentials. |
| SQLite migration race condition | LOW | Already handled by existing try/except pattern. Just ensure the new column follows the same pattern. |
| Precondition type crash (.strip on dict) | LOW | Add isinstance check. Deploy fix. Re-run failed tasks. |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Jinja2 {{cached:key}} crash | Task 6-7: TestFlowService + wiring | Unit test: call substitute_variables with `{{cached:i}}` in text, verify no UndefinedError |
| Step numbering shift | Task 6: TestFlowService | Integration test: run task with login_role, verify step_index values in database match agent output |
| Excel old template breakage | Task 5: Excel template update | Manual test: upload old-format template, verify clear error message |
| ContextWrapper split cache | Task 7: Wire into runs.py | Unit test: create ContextWrapper without cache, then with shared cache, verify same CacheService instance |
| Credential leak in logs | Task 7: Wire into runs.py | Grep test: run task with login_role, then grep logs for known password -- verify zero matches |
| SQLite migration race | Task 4: DB migration | Startup test: run init_db twice concurrently, verify no crash |
| Precondition type crash | Task 8: Cache precondition | Unit test: pass dict to precondition loop, verify isinstance dispatch handles it correctly |

## Sources

- Direct code analysis: `backend/core/precondition_service.py` (ContextWrapper, Jinja2 substitution), `backend/core/external_precondition_bridge.py` (singleton patterns), `backend/core/agent_service.py` (agent step callback), `backend/api/routes/runs.py` (execution pipeline), `backend/db/models.py` (Task model), `backend/db/database.py` (init_db migration pattern), `backend/utils/excel_template.py` (TEMPLATE_COLUMNS), `backend/utils/excel_parser.py` (column mapping)
- Design documents: `docs/plans/2026-04-11-erp-integration-design.md`, `docs/plans/2026-04-11-erp-integration-impl.md`
- Previous pitfalls: `.planning/research/PITFALLS.md` (v0.9.0 -- SQLite concurrent writes, browser cleanup patterns)
- SQLite documentation: ALTER TABLE limitations, busy_timeout, WAL mode single-writer constraint
- Jinja2 documentation: StrictUndefined behavior, custom variable_start_string/variable_end_string

---
*Pitfalls research for: v0.9.1 ERP integration (CacheService, AccountService, TestFlowService, DB migration, Excel template update)*
*Researched: 2026-04-11*
