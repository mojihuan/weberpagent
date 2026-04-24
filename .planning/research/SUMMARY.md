# Project Research Summary

**Project:** aiDriveUITest -- v0.10.6 milestone: bug fixes for generated test code execution pipeline
**Domain:** Self-healing Playwright test execution pipeline (5 interrelated bugs)
**Researched:** 2026-04-24
**Confidence:** HIGH

## Executive Summary

This research covers five bugs in the AI-generated Playwright test code execution pipeline of aiDriveUITest. The bugs fall into two categories: three "execution blockers" (EXEC-01/02/03) that prevent generated code from running at all, and two "healing improvements" (HEAL-01, E2E-01) that make the self-healing pipeline smarter and more cost-efficient. All five bugs are traced to specific lines in specific files, with root causes verified by code analysis and (in the case of EXEC-01) direct execution against the installed pytest-playwright plugin.

The recommended approach is surgical line-level fixes across four files (`self_healing_runner.py`, `action_translator.py`, `code_generator.py`, and documentation), plus one new small module (`pytest_error_classifier.py`) for error categorization. Total scope: approximately 6 lines changed in existing files plus one new ~50-line module. No new dependencies, no version bumps, no architectural restructuring. The fixes are ordered by dependency: EXEC-01 and EXEC-02 must land before HEAL-01 (because HEAL-01's classifier will categorize the errors these fixes eliminate, and we want to verify the classifier works against clean post-fix behavior).

The key risk is in HEAL-01: over-aggressive error categorization could skip legitimate LLM healing opportunities. The mitigation is to anchor regex patterns to pytest's specific output format (`E   SyntaxError:` not just `SyntaxError`) and default all unrecognized `returncode == 1` errors to `CODE_RUNTIME` (the healable category). A secondary risk is that the `_escape_string` method does not handle newlines in string literal contexts beyond the `evaluate` action, which could cause future syntax errors from other action types.

## Key Findings

### Recommended Stack (No Changes Needed)

Current versions in `pyproject.toml` are fully compatible with all fixes. No upgrades required.

**Core technologies:**
- pytest-playwright >=0.7.0: headless is the default; `--headed` is the only toggle (no `--headed=false`, no `--headless`)
- uvicorn[standard] >=0.34.0: `--reload-exclude` accepts glob patterns for dev-mode isolation
- pytest >=8.0.0: exit codes 0-5 are stable and well-documented for error categorization
- Python 3.11+: `enum.Enum`, `ast.parse`, `re.search` -- all standard library, no new deps

### Expected Features

**Must have (table stakes for v0.10.6):**
- EXEC-01: Remove `--headed=false` from subprocess args -- single line deletion in `self_healing_runner.py:193`
- EXEC-02: Strip newlines in `_translate_unknown` return -- single line change in `action_translator.py:644`
- EXEC-03: Add `--reload-exclude "outputs/*"` to dev uvicorn command -- documentation change only
- HEAL-01: Error categorization with 8 categories (4 ENV, 4 CODE) -- new `pytest_error_classifier.py` module + integration into healing loop
- E2E-01: End-to-end validation that generated code runs and produces meaningful results

**Should have (competitive improvements):**
- Pre-flight syntax check: run `ast.parse()` on generated code before invoking pytest subprocess
- Healing telemetry: track "skipped LLM for ENV error" vs "invoked LLM for CODE error" counts
- Error category logging: structured metrics on failure type distribution

**Defer (v2+):**
- Syntax-only LLM repair mode (separate prompt without DOM snapshot overhead)
- Complex error taxonomy beyond 8 categories
- LLM-based import fixing (should be fixed at the code generator level, not the healer)

### Architecture Approach

The fixes preserve the existing component boundaries. The new `pytest_error_classifier.py` module is a pure function with no side effects, following the project's pattern of small, focused modules. The classifier sits between "pytest subprocess failed" and "call LLM repair" in the `SelfHealingRunner.run()` loop, acting as a gate that prevents wasteful LLM calls for environment and infrastructure errors.

**Major components (changes):**
1. `self_healing_runner.py` -- remove `--headed=false` (EXEC-01), integrate error classifier before LLM calls (HEAL-01)
2. `action_translator.py` -- strip newlines in `_translate_unknown` return statement (EXEC-02)
3. `code_generator.py` -- add `validate_syntax()` guard before file write (supporting fix for EXEC-02)
4. `pytest_error_classifier.py` (NEW) -- pure function categorizing pytest exit codes + stderr patterns into 8 error categories
5. Documentation (`CLAUDE.md`, `README.md`) -- add `--reload-exclude "outputs/*"` to dev commands (EXEC-03)

### Critical Pitfalls

1. **Replacing `--headed=false` with the wrong flag** -- The fix is to remove the flag entirely, not replace it. `--headless` does not exist. `--headed` (without `=false`) enables headed mode, which is catastrophic on a headless server. Prevention: unit test that subprocess args contain no variant of `--headed`.

2. **Newlines in `done` action text breaking code generation** -- The `text[:50]` truncation preserves `\n` characters, producing multi-line "comments" where only the first line has the `#` prefix. Prevention: strip newlines at the `_translate_unknown` return site so all unknown action types benefit.

3. **WatchFiles hot-reload triggered by conftest generation** -- Development-only; production uses `reload=False`. Prevention: `--reload-exclude "outputs/*"` on the dev command. Do NOT move outputs to `/tmp/` -- it breaks path conventions across multiple modules.

4. **Over-aggressive error categorization skipping legitimate LLM healing** -- If regex patterns match false positives (e.g., "SyntaxError" appearing in a Playwright error), healable errors get classified as unhealable. Prevention: anchor regexes to pytest output format (`E   SyntaxError:`) and default unrecognized `returncode == 1` to `CODE_RUNTIME`.

5. **`ast.parse` rejecting valid generated code with Chinese identifiers** -- Chinese characters are valid Python 3 identifiers but may surprise some tools. Prevention: validate the full file after splice, not individual snippets; test with Chinese function names.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Execution Blockers (EXEC-01 + EXEC-02 + EXEC-03)
**Rationale:** These three fixes are prerequisites for everything else. Until `--headed=false` is removed and done-action newlines are stripped, no generated code can run successfully. They are all trivial single-line changes with no dependencies between them.
**Delivers:** AI-generated Playwright code that can execute through pytest without immediate crashes
**Addresses:** EXEC-01 (subprocess args), EXEC-02 (newline sanitization), EXEC-03 (WatchFiles isolation)
**Avoids:** Pitfall 1 (wrong flag replacement), Pitfall 2 (newline leakage), Pitfall 3 (WatchFiles reload)
**Files changed:** `self_healing_runner.py`, `action_translator.py`, `code_generator.py`, `CLAUDE.md`

### Phase 2: Self-Healing Error Categorization (HEAL-01)
**Rationale:** Depends on Phase 1 being complete so the classifier can be tested against clean post-fix behavior. With EXEC-01 fixed, every run no longer triggers exit code 4, so the classifier's ENV detection can be validated against real scenarios rather than the current "everything is an ENV error" state.
**Delivers:** Smart error categorization that skips LLM calls for ENV/import errors and preserves healing for genuine locator failures. Estimated 100% LLM cost savings on ENV errors.
**Addresses:** HEAL-01 -- exit-code fast-fail, error pattern classification, skip-healing for ENV errors, categorized error messages
**Avoids:** Pitfall 4 (over-aggressive skipping), Pitfall 9 (HealingResult schema breakage), Pitfall 10 (LLM repair on timeout)
**Files changed:** New `pytest_error_classifier.py`, modified `self_healing_runner.py`

### Phase 3: End-to-End Validation (E2E-01)
**Rationale:** Must come last because it validates that the entire pipeline works correctly after all fixes. This is the "did we actually fix it" phase.
**Delivers:** Confidence that AI-generated code runs end-to-end: agent executes task, code is generated without syntax errors, pytest runs in headless mode, self-healing categorizes errors correctly, and meaningful results are returned.
**Addresses:** E2E-01 -- full pipeline validation
**Avoids:** Pitfall 5 (ast.parse false rejection), Pitfall 6 (string escape gaps), Pitfall 7 (line number off-by-one)
**Files changed:** Test files only; potential minor fixes discovered during validation

### Phase Ordering Rationale

- Phase 1 comes first because EXEC-01 and EXEC-02 are hard blockers: no code can run at all until they are fixed
- Phase 2 depends on Phase 1: the error classifier needs to be tested against a pipeline where the basic execution works
- Phase 3 depends on both: end-to-end validation is meaningless if individual fixes are still in progress
- EXEC-03 (documentation fix) is bundled with Phase 1 because it is trivial and related to the execution environment
- All three phases are small: Phase 1 is ~6 lines, Phase 2 is one new module, Phase 3 is testing

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2 (HEAL-01):** The regex patterns for error classification need validation against real pytest output from the project's specific test cases. The FEATURES-HEAL01.md provides a solid starting point, but edge cases (Chinese characters in error messages, Playwright-specific error formatting) may need iterative tuning.

Phases with standard patterns (skip research-phase):
- **Phase 1 (EXEC-01/02/03):** All three fixes are fully specified with exact line numbers and code snippets. No additional research needed.
- **Phase 3 (E2E-01):** Standard integration testing patterns. The test plan in PITFALLS.md covers the required cases.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Verified by direct execution (`uv run pytest --headed=false`), official docs, installed version compatibility confirmed |
| Features | HIGH | Error categorization taxonomy verified against official pytest exit code docs and direct codebase analysis of 4 modules |
| Architecture | HIGH | Component boundaries unchanged; new module follows existing project patterns; data flow traced from browser-use through code generation to pytest execution |
| Pitfalls | HIGH | 12 pitfalls identified from direct code analysis; 5 critical, 4 moderate, 3 minor; all traced to specific lines with concrete detection strategies |

**Overall confidence:** HIGH

### Gaps to Address

- **Regex pattern tuning for HEAL-01:** The proposed patterns (`_SYNTAX_PATTERNS`, `_IMPORT_PATTERNS`) are based on standard pytest output, but the project generates Chinese-language test names and uses browser-use with Qwen 3.5 Plus, which may produce non-standard error output. Patterns should be validated against 5-10 real pytest outputs from generated test files before finalizing.
- **`_escape_string` completeness for non-`evaluate` actions:** Pitfall 6 identifies that `navigate`, `send_keys`, `input`, `select_dropdown`, and `upload_file` actions do not escape newlines in their string parameters. While these parameters rarely contain newlines today, this is a latent bug. Can be deferred past v0.10.6 but should be tracked.
- **Timeout branch cleanup:** The timeout handler at `self_healing_runner.py:201-214` currently calls `_llm_repair()` and continues the loop. HEAL-01 should change this to immediate failure, but the cleanup (`_cleanup()`) must still run. Verify all code paths execute cleanup.

## Sources

### Primary (HIGH confidence)
- [Playwright Python - Pytest Plugin Reference](https://playwright.dev/python/docs/test-runners) -- CLI arguments, headless default behavior
- [Playwright Python - Running Tests](https://playwright.dev/python/docs/running-tests) -- Confirmation that headless is default
- [pytest Exit Codes -- Official Documentation](https://docs.pytest.org/en/stable/reference/exit-codes.html) -- Exit codes 0-5 definition
- [Uvicorn Settings](https://uvicorn.dev/settings/) -- `--reload-exclude` glob pattern support
- Direct code analysis: `self_healing_runner.py`, `action_translator.py`, `code_generator.py`, `llm_healer.py`
- Direct execution: `uv run pytest --headed=false` producing `error: argument --headed: ignored explicit argument 'false'`

### Secondary (MEDIUM confidence)
- [pytest INTERNALERROR -- GitHub Issue #11765](https://github.com/pytest-dev/pytest/issues/11765) -- Internal error patterns
- [pytest-playwright headed mode -- Stack Overflow](https://stackoverflow.com/questions/78767744) -- Community confirmation
- [Uvicorn GitHub Discussion #1978](https://github.com/Kludex/uvicorn/discussions/1978) -- WatchFiles exclude patterns

### Tertiary (LOW confidence)
- [CallSphere blog -- headless vs headed](https://callsphere.tech/blog/headless-vs-headed-playwright-when-ai-agents-need-visible-browser) -- Blog post, not authoritative

---
*Research completed: 2026-04-24*
*Ready for roadmap: yes*
