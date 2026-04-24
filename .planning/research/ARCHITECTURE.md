# Architecture Research: Generated Test Code Output Isolation

**Domain:** Bug fix -- isolating AI-generated test code output to prevent server reload interference and syntax errors
**Researched:** 2026-04-24
**Confidence:** HIGH (direct codebase analysis, verified with sample generated files)

## Problem Statement

Three bugs in the generated test code execution pipeline:

1. **EXEC-02:** The `done` action from `browser-use` produces multi-line text in its `text` parameter. `_translate_unknown` truncates to 50 chars but does not strip newlines, causing raw non-Python text to appear after the comment line in the generated `.py` file.
2. **EXEC-03:** `conftest.py` written inside `outputs/{run_id}/` triggers WatchFiles reload during local development (`uvicorn --reload`), interrupting the running server.
3. **EXEC-01 (related):** `--headed=false` is not a valid pytest-playwright flag (covered in `STACK-v0.10.6.md`).

This document addresses the architectural decisions for EXEC-02 and EXEC-03.

## Current Architecture

### File Layout (Current -- Problematic)

```
project_root/
  outputs/                          <-- inside project root, watched by WatchFiles
    {run_id}/
      generated/
        test_{run_id}.py            <-- generated Playwright test (with syntax errors)
      dom/
        step_1.txt ... step_N.txt
      screenshots/
        step_1.png ... step_N.png
      logs/
  backend/
    core/
      code_generator.py             <-- writes to outputs/{run_id}/generated/
      self_healing_runner.py        <-- writes conftest.py + .storage_state.json to same dir
```

### The "done" Action Bug -- Root Cause Trace

```
browser-use Agent finishes
    |
    v
model_actions() returns list including:
  {"done": {"text": "销售出库流程已完成！\n\n所有步骤执行成功：\n✓ 步骤1：..."}, "interacted_element": None}
    |
    v
ActionTranslator._identify_action_type() returns "done"
    |
    v
_translate_unknown("done", params) at action_translator.py:627
    summary = f"任务完成: {p.get('text', '')[:50]}"
    # text[:50] contains newlines: "销售出库流程已完成！\n\n所有步骤执行成功：\n✓ 步骤1：点击库存管理\n✓ 步骤2"
    code = f"    # done: {summary}"
    # Result: "    # done: 任务完成: 销售出库流程已完成！\n\n所有步骤执行成功：\n✓ 步骤1：点击库存管理\n✓ 步骤2"
    |
    v
TranslatedAction.code has embedded newlines WITHOUT comment prefix
    |
    v
_build_body joins with "\n" -- raw text lines appear outside comments
    |
    v
Generated .py file has syntax errors from line 158+ (non-Python text)
```

**Evidence from real output** (`outputs/5a96ad7f/generated/test_5a96ad7f.py`):
```python
# Line 156 (correct):
    # done: 任务完成: 销售出库流程已完成！

# Lines 158-162 (syntax error -- raw text without comment prefix):
所有步骤执行成功：
✓ 步骤1：点击库存管理
✓ 步骤2：点击出库管理
```

### The WatchFiles Bug -- Trigger Sequence

```
Local dev: uv run uvicorn backend.api.main:app --reload --port 8080
    |
    v
watchfiles monitors CWD for *.py changes
    |
    v
SelfHealingRunner.run() writes conftest.py to outputs/{run_id}/
    |
    v
watchfiles detects new .py file --> triggers server reload
    |
    v
Server restarts mid-execution, killing in-flight requests
```

**Note:** Production uses `reload=False` in `run_server.py:36`, so this is **development-only**.

## Recommended Architecture: Bug Fixes

### Fix 1: EXEC-02 -- Strip Newlines in "done" Action Comment

**File:** `backend/core/action_translator.py`, line 627

**Current code:**
```python
"done": lambda p: f"任务完成: {p.get('text', '')[:50]}",
```

**Problem:** `text[:50]` preserves `\n` characters. The comment line `# done: 任务完成: ...` gets broken into multiple lines, and only the first line has the `#` prefix.

**Fix:** Replace newlines with spaces before truncation.

```python
"done": lambda p: f"任务完成: {p.get('text', '').replace(chr(10), ' ').replace(chr(13), ' ')[:50]}",
```

Or more readably, extract to a helper:
```python
def _summarize_done(params: dict) -> str:
    text = params.get('text', '').replace('\n', ' ').replace('\r', ' ')
    return f"任务完成: {text[:50]}"
```

**Alternative (deeper fix):** Apply newline stripping to ALL unknown action type summaries, not just "done". The `_translate_unknown` method already truncates to prevent long lines, but no other action type has been observed with multi-line text. However, defensive programming suggests stripping newlines at the point where the comment is constructed:

```python
return TranslatedAction(
    code=f"    # {action_type}: {summary.replace(chr(10), ' ').replace(chr(13), ' ')}",
    ...
)
```

**Recommendation:** Strip newlines at the return site in `_translate_unknown` rather than in individual summarizer lambdas. This is a single-point fix that covers all unknown action types.

**Change scope:** 1 line in `_translate_unknown` return statement (line 644).

### Fix 2: EXEC-03 -- Exclude outputs/ from WatchFiles

**Two options evaluated:**

#### Option A: `--reload-exclude` on dev command (RECOMMENDED)

```bash
uv run uvicorn backend.api.main:app --reload --port 8080 --reload-exclude "outputs/*"
```

**Why this is sufficient:**
- `outputs/` only contains generated test artifacts (`.py`, `.json`, `.png`, `.txt`), never source code
- The `--reload-exclude` flag accepts glob patterns (verified uvicorn docs)
- `.storage_state.json` is already excluded by default pattern `.*`, but `conftest.py` is not
- Production is unaffected (`reload=False` already set in `run_server.py:36`)
- Zero code changes required

**Files to update:**
- `CLAUDE.md` line 34: update the dev startup command
- `README.md`: update any documented dev commands

#### Option B: Move output directory to /tmp/ (NOT RECOMMENDED)

Moving `outputs/` to `/tmp/weberpagent/{run_id}/` would also prevent WatchFiles triggers.

**Why NOT recommended:**
- Requires changing `base_dir` parameter threaded through `code_generator.py`, `self_healing_runner.py`, and the route layer
- Breaks the existing path convention where `outputs/{run_id}/generated/` is relative to project root
- The "view code" endpoint (`GET /runs/{id}/code`) reads from the stored `generated_code_path` -- if this changes to `/tmp/...`, file cleanup on restart becomes a concern
- The `outputs/` directory contains screenshots and DOM dumps used by the reporting UI -- moving these breaks existing URL patterns

**Conclusion:** Option A is a one-line documentation fix. Option B is an architectural change with cascading effects. The simpler fix is correct here.

### Fix 3 (Supporting): Add validate_syntax Guard Before Write

**File:** `backend/core/code_generator.py`, after line 115

The `PlaywrightCodeGenerator` already has a `validate_syntax()` method (line 257) that runs `ast.parse()`. It should be used in `generate_and_save()` before writing to disk:

```python
content = self.generate(run_id, task_name, task_id, translated)

# Guard: validate before write
if not self.validate_syntax(content):
    logger.warning(f"[{run_id}] Generated code has syntax errors, attempting cleanup")
    # The fix to _translate_unknown should prevent this,
    # but log as a safety net

output_path.write_text(content, encoding="utf-8")
```

This is a defensive measure. With Fix 1 applied, syntax errors from multi-line text should not occur, but the guard catches any future regressions.

## Revised Data Flow (After Fixes)

### Code Generation Flow (Fixed)

```
browser-use Agent completes
    |
    v
model_actions() -> list of action dicts
    |
    v
ActionTranslator.translate_with_llm() for each action
    |
    v
_translate_unknown("done", {"text": "multi\nline\ntext"})
    |
    v  [FIX: newlines replaced with spaces]
    code = "    # done: 任务完成: multi line text (first 50 chars, single line)"
    |
    v
PlaywrightCodeGenerator.generate() assembles full file
    |
    v  [FIX: validate_syntax guard before write]
ast.parse(content) -- verify syntactically valid Python
    |
    v
Write to outputs/{run_id}/generated/test_{run_id}.py
```

### Code Execution Flow (Fixed)

```
User triggers "Run Code"
    |
    v
POST /runs/{id}/run-code
    |
    v
SelfHealingRunner.run()
    |
    v
Write conftest.py + .storage_state.json to outputs/{run_id}/
    |                                             ^
    |   (WatchFiles does NOT reload because       |
    |    --reload-exclude "outputs/*")            |
    v                                            |
subprocess: uv run pytest test_{run_id}.py       |
    --timeout=60 -v                              |
    (no --headed=false)                          |
    |
    v
_cleanup() deletes conftest.py + .storage_state.json
```

## Component Boundaries (After Fixes)

| Component | Change | Impact |
|-----------|--------|--------|
| `action_translator.py:644` | Strip newlines in `_translate_unknown` return | Prevents syntax errors in generated code |
| `code_generator.py:115` | Add `validate_syntax()` guard before file write | Safety net for regressions |
| `CLAUDE.md:34` | Add `--reload-exclude "outputs/*"` to dev command | Prevents WatchFiles reload |
| `self_healing_runner.py:193` | Remove `--headed=false` from subprocess args | Already documented in STACK-v0.10.6.md |

## Anti-Patterns to Avoid

### Anti-Pattern 1: Filtering "done" Actions from model_actions()

**What people do:** Strip the `done` action entirely from `raw_actions` before translation.

**Why it is wrong:** The `done` action is a legitimate action that marks task completion. Removing it loses information. The comment it generates (`# done: 任务完成: ...`) is useful for understanding the generated test file.

**Do this instead:** Fix the newline handling in `_translate_unknown` so the comment is valid Python.

### Anti-Pattern 2: Moving outputs/ to /tmp/ Just for WatchFiles

**What people do:** Relocate the entire output directory to `/tmp/` to escape WatchFiles monitoring.

**Why it is wrong:** Breaks path conventions used by the code viewer endpoint, screenshot serving, DOM snapshot reading, and the reporting UI. Creates cascading changes across multiple modules.

**Do this instead:** Use `--reload-exclude "outputs/*"` on the uvicorn command. Zero code changes.

### Anti-Pattern 3: Sanitizing at File Write Time Instead of Translation Time

**What people do:** Post-process the entire generated file to strip non-Python text after assembly.

**Why it is wrong:** Fragile heuristic (what counts as "non-Python text"?). Breaks if valid Python code happens to look like natural language. The fix belongs at the source: the translation layer that constructs each line.

**Do this instead:** Fix `_translate_unknown` to produce single-line comments. The translation layer is the correct place to enforce "one TranslatedAction = one logical line of code."

## Summary of Required Changes

| Bug | File | Line(s) | Change | Complexity |
|-----|------|---------|--------|------------|
| EXEC-02 | `action_translator.py` | 644 | Strip `\n`/`\r` in `_translate_unknown` return statement | 1 line |
| EXEC-02 (guard) | `code_generator.py` | 115-116 | Add `validate_syntax()` check + warning log before write | 3 lines |
| EXEC-03 | `CLAUDE.md` | 34 | Add `--reload-exclude "outputs/*"` to uvicorn command | 1 line |
| EXEC-01 | `self_healing_runner.py` | 193 | Remove `"--headed=false"` from subprocess args | 1 line |

Total: 4 files, approximately 6 lines changed. No new dependencies, no architectural restructuring.

## Sources

- Direct codebase analysis: `backend/core/action_translator.py` (lines 612-647), `backend/core/code_generator.py` (lines 83-125, 240-255), `backend/core/self_healing_runner.py` (lines 168-176, 186-197, 340-358)
- Generated file analysis: `outputs/5a96ad7f/generated/test_5a96ad7f.py` (lines 156-162), `outputs/0dddee85/generated/test_0dddee85.py` (lines 12-15)
- Configuration: `pyproject.toml` (lines 42-47), `backend/run_server.py` (line 36), `backend/api/main.py`
- Existing research: `.planning/research/STACK-v0.10.6.md` (EXEC-01 and EXEC-03 solutions)

---
*Architecture research for: Generated test code output isolation and execution pipeline fixes*
*Researched: 2026-04-24*
