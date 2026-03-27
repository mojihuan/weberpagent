# Phase 45: 代码移除 - Research

**Researched:** 2026-03-26
**Domain:** Python code cleanup / browser-use extension removal
**Confidence:** HIGH

## Summary

Phase 45 focuses on removing all custom browser-use extensions added in v0.6.0-v0.6.1 to simplify the codebase and reduce maintenance burden. The goal is to revert to native browser-use capabilities while preserving core functionality (basic logging, screenshots, step stats).

The removal targets are clearly identified and isolated:
1. `backend/agent/tools/` directory - scroll_table_tool.py and __init__.py
2. `agent_service.py` - 4 methods (`_post_process_td_click`, `_fallback_input`, `_collect_element_diagnostics`, and `LoopInterventionTracker` class)
3. Related imports and variable references in `step_callback`
4. Unit tests that test the removed functionality

**Primary recommendation:** Systematic deletion following the dependency order: remove imports first, then delete methods, then delete files, then update tests. This prevents broken imports during the process.

## User Constraints (from REQUIREMENTS.md)

### Locked Decisions (Phase 45 Scope)
- CLEANUP-01: Remove scroll_table_and_input tool - delete `backend/agent/tools/` directory
- CLEANUP-02: Remove TD post-processing logic - delete `_post_process_td_click` method
- CLEANUP-03: Remove JavaScript fallback - delete `_fallback_input` method
- CLEANUP-04: Remove element diagnostics logging - delete `_collect_element_diagnostics` method
- CLEANUP-05: Remove loop intervention logic - delete `LoopInterventionTracker` class

### Out of Scope
- SIMPLIFY-01, SIMPLIFY-02 (Phase 46)
- TEST-01, VALIDATE-01 (Phase 46-47)
- Frontend code changes
- browser-use core library modifications

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CLEANUP-01 | Remove scroll_table_and_input tool | Delete `backend/agent/tools/` directory, update imports in `agent_service.py` and `backend/agent/__init__.py` |
| CLEANUP-02 | Remove TD post-processing logic | Delete `_post_process_td_click` method (lines 184-255 in agent_service.py), remove TD-related calls in step_callback |
| CLEANUP-03 | Remove JavaScript fallback | Delete `_fallback_input` method (lines 257-330 in agent_service.py), remove fallback calls in step_callback |
| CLEANUP-04 | Remove element diagnostics logging | Delete `_collect_element_diagnostics` method (lines 332-422 in agent_service.py), remove diagnostics variables |
| CLEANUP-05 | Remove loop intervention logic | Delete `LoopInterventionTracker` class (lines 29-158 in agent_service.py), remove tracker instantiation and calls |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11+ | Runtime | Project requirement |
| pytest | 8.0.0+ | Testing | Already configured in pyproject.toml |
| pytest-asyncio | 0.24.0+ | Async test support | Already configured |

### No New Dependencies Required
This phase is purely code removal. No new libraries or packages are needed.

## Architecture Patterns

### Current Code Structure (Files to Modify/Delete)

```
backend/
├── agent/
│   ├── __init__.py           # REMOVE: register_scroll_table_tool, ScrollTableInputParams exports
│   └── tools/                 # DELETE ENTIRE DIRECTORY
│       ├── __init__.py        # DELETE
│       └── scroll_table_tool.py  # DELETE (256 lines)
├── core/
│   └── agent_service.py      # MODIFY: Remove 4 methods + class + imports
└── tests/
    ├── unit/
    │   ├── test_agent_service.py  # MODIFY: Remove test classes for deleted methods
    │   └── test_scroll_table_tool.py  # DELETE
    └── e2e/
        └── test_scroll_table_e2e.py  # DELETE
```

### Removal Order (Critical for Clean Execution)

```
Step 1: Remove imports
        - backend/agent/__init__.py: Remove tool exports
        - backend/core/agent_service.py: Remove `from backend.agent.tools import register_scroll_table_tool`

Step 2: Remove step_callback references
        - Remove `tools = register_scroll_table_tool()` call
        - Remove `tracker` instantiation
        - Remove `loop_intervention_data`, `td_post_process_result`, `element_diagnostics` variables
        - Remove TD post-processing and fallback logic blocks
        - Remove tracker.should_intervene() calls

Step 3: Delete methods from agent_service.py
        - Delete LoopInterventionTracker class (lines 29-158)
        - Delete _post_process_td_click (lines 184-255)
        - Delete _fallback_input (lines 257-330)
        - Delete _collect_element_diagnostics (lines 332-422)

Step 4: Delete tool files
        - rm -rf backend/agent/tools/

Step 5: Update/delete tests
        - Delete backend/tests/unit/test_scroll_table_tool.py
        - Delete backend/tests/e2e/test_scroll_table_e2e.py
        - Remove test classes from test_agent_service.py:
          - TestLoopInterventionTracker
          - TestTdPostProcess
          - TestTDPostProcessing
          - TestFallbackInput
          - TestElementDiagnostics
```

### What to Preserve in step_callback

The following should remain intact after cleanup:
- URL logging from browser_state
- DOM state logging and file writing
- Element tree info logging
- Action extraction from agent_output
- Reasoning extraction (evaluation, memory, next_goal)
- Screenshot saving
- step_stats basic structure (action_count, element_count)
- on_step callback invocation

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| N/A | This phase removes code | Native browser-use | Simpler maintenance |

**Key insight:** This phase is about deletion, not creation. The "don't hand-roll" principle applies to what we're removing - these custom extensions were hand-rolled solutions that should have been handled by browser-use natively or better test case design.

## Runtime State Inventory

> Not applicable - this is a code cleanup phase, not a rename/refactor/migration phase.

| Category | Items Found | Action Required |
|----------|-------------|-----------------|
| Stored data | None | N/A |
| Live service config | None | N/A |
| OS-registered state | None | N/A |
| Secrets/env vars | None | N/A |
| Build artifacts | None | N/A |

## Common Pitfalls

### Pitfall 1: Removing Methods Before Removing Their Callers
**What goes wrong:** Deleting a method while code still references it causes NameError at runtime.
**Why it happens:** Linear top-to-bottom editing without checking dependencies.
**How to avoid:** Remove all call sites first (in step_callback), then delete the method definitions.
**Warning signs:** IDE/linter errors about undefined names.

### Pitfall 2: Forgetting to Remove Test Files
**What goes wrong:** Test suite fails with import errors for deleted modules.
**Why it happens:** Focus on source code, forget about test files.
**How to avoid:** Include test file deletion in the plan explicitly.
**Warning signs:** `pytest` fails with `ModuleNotFoundError` or `ImportError`.

### Pitfall 3: Breaking Agent Creation
**What goes wrong:** Agent creation fails because `tools` parameter still references deleted function.
**Why it happens:** `tools=tools` in Agent() constructor still expects a value.
**How to avoid:** Either remove `tools` parameter entirely or set `tools=None`.
**Warning signs:** `TypeError: 'NoneType' object is not callable` or similar.

### Pitfall 4: Incomplete step_callback Cleanup
**What goes wrong:** References to deleted variables like `tracker`, `td_post_process_result` remain.
**Why it happens:** Variables are used in multiple places within the nested callback function.
**How to avoid:** Search for all occurrences of each variable name before declaring cleanup complete.
**Warning signs:** `NameError: name 'tracker' is not defined` at runtime.

### Pitfall 5: Leaving Dead Imports
**What goes wrong:** Import statement for deleted module remains, causing import error.
**Why it happens:** Import is at top of file, easy to miss when focusing on method deletion.
**How to avoid:** After deleting files, run `ruff check` or `pyright` to catch unused imports.
**Warning signs:** `ImportError: cannot import name 'register_scroll_table_tool'`.

## Code Examples

### Before: agent_service.py imports (line 15)
```python
from backend.agent.tools import register_scroll_table_tool
```

### After: Remove this import entirely
```python
# Import removed - no longer using custom tools
```

### Before: Agent creation with tools (line 777-784)
```python
agent = Agent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    tools=tools,  # REMOVE THIS
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
)
```

### After: Agent creation without custom tools
```python
agent = Agent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
)
```

### Before: Variables to remove in run_with_streaming (lines 521-533)
```python
# Create custom tools with scroll_table_and_input (Phase 40)
tools = register_scroll_table_tool()

# Create loop intervention tracker (per D-01)
tracker = LoopInterventionTracker(window_size=20, stagnation_threshold=5)
loop_intervention_data = {"value": None}  # Mutable container for closure (Phase 39, LOG-01)
step_stats_data = {"value": None}  # Mutable container for step stats (Phase 41, LOG-02)
td_post_process_result = None  # TD 后处理结果临时存储 (Phase 42, D-06)
# Initialize element_diagnostics (Phase 44, LOG-03, per D-01, D-02)
element_diagnostics = {
    "non_interactive_elements": [],
    "fallback_triggered": False,
    "fallback_reason": None
}
```

### After: Simplified variable setup
```python
step_stats_data = {"value": None}  # Mutable container for step stats
```

### step_callback - Logic to Remove

**TD Post-Processing Block (lines 609-619):**
```python
# TD 后处理 (Phase 42, Per D-01, D-02, D-06)
nonlocal td_post_process_result
if action_name == 'click' and self._browser_session:
    try:
        page = await self._browser_session.get_current_page()
        if page:
            td_result = await self._post_process_td_click(page)
            td_post_process_result = td_result
            logger.info(f"[{run_id}] TD post-process result: {td_result}")
    except Exception as e:
        logger.warning(f"[{run_id}] TD post-processing error: {e}")
```

**Fallback Input Block (lines 621-671):**
```python
# Fallback input for td elements (Phase 43, Per D-01, D-04)
if action_name == 'input' and self._browser_session:
    # ... entire block to remove ...
```

**Element Diagnostics Link Block (lines 673-679):**
```python
# Link fallback info to element_diagnostics (Phase 44, per D-03)
if td_post_process_result and td_post_process_result.get('fallback'):
    element_diagnostics['fallback_triggered'] = True
    # ... rest of block ...
```

**Tracker Record Calls (lines 607, 706-707):**
```python
tracker.record_action(action_name, action_params)
# ...
tracker.record_page_state(url, dom_hash)
```

**Loop Intervention Block (lines 735-750):**
```python
# Check for loop intervention (D-01, D-02)
if tracker.should_intervene():
    intervention_msg = tracker.get_intervention_message()
    diagnostic = tracker.get_diagnostic_info()
    # ... rest of block ...
```

**step_stats with TD info (lines 730-732):**
```python
# 添加 TD 后处理结果 (Phase 42, D-06)
if td_post_process_result:
    step_stats['td_post_process'] = td_post_process_result
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom scroll_table_and_input tool | Native browser-use actions | v0.6.2 | Less maintenance, simpler code |
| LoopInterventionTracker | Rely on browser-use internal detection | v0.6.2 | Remove ~130 lines of custom logic |
| TD post-processing / fallback | Trust browser-use to handle table inputs | v0.6.2 | Remove ~150 lines of JS hacks |

**Deprecated/outdated:**
- `scroll_table_and_input` tool: Custom tool for table input, now relying on native browser-use
- `LoopInterventionTracker`: Custom loop detection, browser-use has built-in `ActionLoopDetector`
- TD post-processing: Workaround for focus issues, let browser-use handle natively

## Open Questions

1. **Should we keep the `_browser_session` reference?**
   - What we know: Currently stored for TD post-processing access to page
   - What's unclear: If any remaining code needs it after cleanup
   - Recommendation: Check if any preserved code needs page access; if not, remove this too

2. **What should step_stats contain post-cleanup?**
   - What we know: Currently has action_count, element_count, stagnation, td_post_process
   - What's unclear: Exact structure needed for frontend/reporting
   - Recommendation: Keep action_count and element_count; remove stagnation and td_post_process

## Environment Availability

> Skip this section - no external dependencies for code removal phase.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| N/A | Code cleanup only | - | - | - |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0+ |
| Config file | pyproject.toml (tool.pytest.ini_options) |
| Quick run command | `uv run pytest backend/tests/unit/test_agent_service.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CLEANUP-01 | scroll_table_tool files deleted | file check | `test ! -d backend/agent/tools/` | N/A (manual) |
| CLEANUP-02 | _post_process_td_click removed | import check | `grep -c "_post_process_td_click" backend/core/agent_service.py` | N/A (manual) |
| CLEANUP-03 | _fallback_input removed | import check | `grep -c "_fallback_input" backend/core/agent_service.py` | N/A (manual) |
| CLEANUP-04 | _collect_element_diagnostics removed | import check | `grep -c "_collect_element_diagnostics" backend/core/agent_service.py` | N/A (manual) |
| CLEANUP-05 | LoopInterventionTracker removed | import check | `grep -c "LoopInterventionTracker" backend/core/agent_service.py` | N/A (manual) |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_agent_service.py -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] Tests for removed methods must be deleted (test classes in test_agent_service.py)
- [ ] Test files for scroll_table_tool must be deleted (test_scroll_table_tool.py, test_scroll_table_e2e.py)
- [ ] Agent creation test should be updated to not pass tools parameter

*(Validation of code removal is primarily structural - verify files don't exist, imports don't reference deleted code)*

## Sources

### Primary (HIGH confidence)
- Code inspection of `backend/core/agent_service.py` (840 lines)
- Code inspection of `backend/agent/tools/scroll_table_tool.py` (256 lines)
- Code inspection of test files
- pyproject.toml for pytest configuration

### Secondary (MEDIUM confidence)
- REQUIREMENTS.md for phase scope and success criteria
- ROADMAP.md for milestone context

### Tertiary (LOW confidence)
- None required - this is a straightforward code removal based on direct inspection

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new dependencies needed
- Architecture: HIGH - All files and code locations identified with line numbers
- Pitfalls: HIGH - Based on common Python refactoring patterns

**Research date:** 2026-03-26
**Valid until:** N/A - Code removal patterns are stable
