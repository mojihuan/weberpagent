# Domain Pitfalls

**Domain:** Bug fixes for the AI-generated Playwright test code execution pipeline (v0.10.6 milestone)
**Researched:** 2026-04-24
**Context:** Fixing five specific bugs in pytest invocation, code generation output, conftest isolation, self-healing error categorization, and end-to-end validation
**Confidence:** HIGH (based on direct code analysis of `self_healing_runner.py`, `action_translator.py`, `code_generator.py`, `llm_healer.py`, verified pytest-playwright CLI behavior, and existing FEATURES-HEAL01.md research)

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

---

### Pitfall 1: Replacing `--headed=false` with the Wrong Flag

**What goes wrong:** The current code at `self_healing_runner.py` line 193 passes `--headed=false` to pytest. This causes an immediate exit with code 4 and error: `argument --headed: ignored explicit argument 'false'`. Verified by running `uv run pytest --headed=false` which produces this exact error.

**Why it happens:** pytest-playwright uses a boolean flag `--headed` (no value). It defaults to headless mode. Passing `--headed=false` is parsed as `--headed` plus a stray `false` positional argument. The correct invocation is to simply omit `--headed` entirely, since headless is already the default.

**Consequences of fixing incorrectly:**
- Removing `--headed=false` and replacing with `--headless` (which does not exist in pytest-playwright) causes the same class of error
- Removing the flag entirely but accidentally introducing `--headed` (without the `=false`) would flip to headed mode, causing Chromium windows to appear on the server, consuming massive memory
- Changing to `--headed --browser chromium` (some blog posts suggest this) would make every run headed, which is catastrophic on the 2GB deployment server

**Prevention:**
- The fix is to remove `--headed=false` from the argument list entirely. No replacement flag is needed
- After the fix, the subprocess args should be: `["uv", "run", "pytest", test_file_path, "--timeout=60", "-v"]`
- Add a unit test that verifies the subprocess arguments do NOT contain `--headed` in any form
- Add a comment explaining that pytest-playwright defaults to headless and `--headed` is opt-in

**Detection:**
- Unit test: assert `"--headed"` not in subprocess_args (catches all variants: `--headed`, `--headed=false`, `--headed=true`)
- Integration test: run the generated code and verify no Chromium window appears (check process list for chromium/chrome processes with no display)
- Run `uv run pytest --help | grep headed` and confirm the flag description says "Run tests in headed mode" (i.e., headed is opt-in, not the default)

**Warning signs the fix broke something:**
- pytest exit code 4 with "unrecognized arguments" -- wrong flag name used
- Chromium processes visible in `ps aux` on the server after a code run -- accidentally enabled headed mode
- Timeout errors when running in headed mode on a headless server -- X11 display not available
- Server memory spike during code execution -- headed mode spawning visible browser windows

---

### Pitfall 2: Done Action Text with Newlines Breaking Code Generation

**What goes wrong:** The `done` action type in `action_translator.py` line 627 generates a comment like `# done: 任务完成: {text[:50]}`. The `text` value comes from `browser-use` agent output and can contain newlines, tabs, or other whitespace. When newlines are present, the generated code breaks because a Python comment only extends to the end of the line.

**Why it happens:** The `_translate_unknown` method at line 612 does not sanitize the text parameter before inserting it into the comment string. The `_escape_string` method at line 650 only escapes backslashes and double quotes -- it does NOT escape newlines, tabs, or carriage returns. This is correct for string literals (which go inside quotes), but comments are not inside quotes and newlines break the line structure.

**Concrete example:** If `done.text` = `"Task completed\nAll steps done successfully"`, the generated code becomes:
```python
    # done: 任务完成: Task completed
All steps done successfully
```
The second line `All steps done successfully` is not a comment, not valid Python, and causes `SyntaxError` when the file is executed by pytest.

**Consequences of fixing incorrectly:**
- Stripping ALL whitespace from `done` text loses meaningful content (the text summarizes what the agent accomplished)
- Truncating at 50 chars then stripping newlines may produce empty strings for texts that are all newlines
- Replacing newlines with `\\n` (escaped backslash-n) in a comment looks weird but is syntactically valid
- Over-sanitizing the text of other action types (extract, write_file, search) could produce confusing comments

**Prevention:**
- In `_translate_unknown`, sanitize the summary text to replace newlines with spaces before building the comment: `summary = summary.replace("\n", " ").replace("\r", "")`
- Apply this sanitization AFTER the lambda produces the summary, at line 638-639, so ALL unknown action types benefit from it
- Alternatively, sanitize inside each lambda, but this is error-prone (easy to miss one). Centralized sanitization is safer
- Keep the 50-char truncation for `done` text but ensure it happens AFTER newline replacement

**Detection:**
- Unit test: translate a `done` action with multi-line text and verify the output `.code` field contains no literal newlines
- Unit test: translate an `extract` action with multi-line query and verify single-line output
- Run `ast.parse()` on the generated code to verify syntactic validity
- Fuzz test: translate actions with text containing `\n`, `\r\n`, `\t`, `\0`, and verify no syntax errors

**Warning signs the fix broke something:**
- Done actions generate empty comments -- over-aggressive stripping
- Other action types (extract, search) lose their parameter information -- sanitization applied too early
- Generated file still fails `ast.parse()` -- newline leakage from a different path (e.g., LLM healer output)

---

### Pitfall 3: WatchFiles Hot-Reload Triggered by Conftest Generation

**What goes wrong:** The `SelfHealingRunner._generate_conftest()` method writes `conftest.py` into the same directory as the generated test file (`outputs/{run_id}/generated/conftest.py`). When the backend is running with `uvicorn --reload` (the documented development command), WatchFiles detects the new `conftest.py` and triggers a full server restart, killing in-progress test execution and losing the healing state.

**Why it happens:** The documented development command is `uv run uvicorn backend.api.main:app --reload --port 8080`. WatchFiles monitors the entire project directory for Python file changes. When `conftest.py` (a pytest plugin file) appears in any subdirectory, WatchFiles sees it as a source code change and restarts the server process. The production deployment uses `reload=False` (in `run_server.py` line 36), so this only affects development.

However, there is a deeper issue: even in production, writing `conftest.py` into the `outputs/` directory means pytest discovers it during collection. If the runner's conftest.py and the project's top-level conftest.py have conflicting fixtures, tests may fail in unpredictable ways.

**Consequences of fixing incorrectly:**
- Moving conftest to a temp directory like `/tmp/weberpagent-{run_id}/` may cause pytest collection to not find it at all (pytest only discovers conftest.py in the test file's directory or parent directories)
- Adding `outputs/` to a WatchFiles exclusion list (e.g., `--reload-exclude outputs`) could hide real source code changes if outputs happen to be in a source directory
- Writing conftest in the project root instead of the output directory could affect ALL pytest runs, not just the generated test
- Writing to a fixed temp directory creates a race condition between concurrent code executions

**Prevention:**
- The output directory `outputs/{run_id}/generated/` is already isolated from source code by design. The issue is specifically about the `--reload` flag watching it
- For development: use `--reload-exclude "outputs"` when running `uvicorn --reload`. This is a development-only concern
- For the conftest itself: verify it is written to `output_dir` (the generated test file's directory, not the project root). The current code at line 342 does this correctly: `conftest_path = output_dir / "conftest.py"` where `output_dir = Path(test_file_path).parent`
- For production: `reload=False` is already set, so no WatchFiles issue exists
- Consider documenting the `--reload-exclude` option in CLAUDE.md or run_server.py

**Detection:**
- In development: run a code execution and watch the uvicorn terminal for "Restarting with watchfiles" messages
- In production: verify no server restart happens during code execution
- Test that the conftest.py is cleaned up after execution completes (`_cleanup()` deletes it)
- Test that the conftest.py is NOT written to the project root or any source directory

**Warning signs the fix broke something:**
- Server restarts during code execution in development -- WatchFiles still watching outputs/
- pytest fails with "fixture 'browser_context_args' not found" -- conftest written too far from the test file
- Concurrent code executions interfere with each other -- shared conftest path
- conftest.py survives after execution -- cleanup failed, stale conftest affects future pytest runs

---

### Pitfall 4: Error Categorization Too Aggressive, Skipping Legitimate LLM Healing

**What goes wrong:** The error categorization for HEAL-01 (already researched in FEATURES-HEAL01.md) distinguishes ENV errors (skip LLM) from CODE errors (attempt LLM healing). If the regex patterns are too broad or the exit code mapping is wrong, legitimate healable errors get classified as ENV errors and the LLM healer is never invoked, making the self-healing pipeline useless.

**Why it happens:** The proposed classifier uses `re.search(pattern, combined_output)` where `combined = stderr + stdout`. If the output contains a false positive match (e.g., the word "SyntaxError" appears in a Playwright error message like "Error: strict mode violation - SyntaxError in locator"), the classifier misidentifies a runtime error as a syntax error, skipping the DOM-based LLM healing that could actually fix it.

Similarly, `ModuleNotFoundError` could appear in a traceback as a symptom of a different error (e.g., Playwright fails to import a module due to environment corruption), when the real issue is a locator failure that LLM could fix.

**Consequences of fixing incorrectly:**
- Classifying ALL `returncode == 1` with "Error" in output as `CODE_RUNTIME` would miss import/syntax errors
- Classifying any output containing "SyntaxError" as `CODE_SYNTAX` could skip DOM healing for false positives
- Classifying timeout errors as `CODE_RUNTIME` would waste LLM calls on tests that just need more time
- Making the classifier return `ENV_*` for any unrecognized pattern would break the healing pipeline for new error types
- Adding `returncode == 1` to the fast-fail path would kill ALL healing, which is the entire point of the self-healing runner

**Prevention:**
- Anchor regex patterns to pytest's specific output format, not just the error name. For example:
  - SyntaxError: `r"^E\s+SyntaxError:"` (pytest prefixes assertion errors with "E   ")
  - ImportError: `r"^E\s+ModuleNotFoundError:"` or `r"^E\s+ImportError:"`
  - These patterns match pytest-formatted output, not arbitrary mentions in error messages
- Use exit code as the primary classifier (returncode 2/3/4/5 are ALWAYS ENV), and pattern matching only for returncode 1
- Default to `CODE_RUNTIME` for any `returncode == 1` that does not match specific patterns -- this preserves the healing pipeline for unknown error types
- Add a "catch-all" test case: any stderr that does not match known patterns should classify as `CODE_RUNTIME`, not as an ENV error
- Test with real pytest output, not synthetic patterns

**Detection:**
- Unit test: "SyntaxError" appearing inside a Playwright error message should classify as `CODE_RUNTIME`, not `CODE_SYNTAX`
- Unit test: empty stderr with returncode 1 should classify as `CODE_RUNTIME` (safe default)
- Integration test: a legitimate locator failure should still get LLM healing after the classifier is added
- Monitor healing success rate before and after the change -- if it drops significantly, the classifier is too aggressive

**Warning signs the fix broke something:**
- LLM healer is never invoked for any test failure -- all errors classified as ENV
- Healing success rate drops from whatever it was to 0% -- over-aggressive pattern matching
- SyntaxError in Playwright output gets classified as `CODE_SYNTAX` and skips DOM-based healing
- Tests that used to self-heal now fail permanently -- classifier changed the behavior for previously-working cases

---

### Pitfall 5: ast.parse Validation Rejecting Valid Generated Code

**What goes wrong:** The `code_generator.py` `validate_syntax()` method at line 257 and `self_healing_runner.py` line 331 both use `ast.parse(code)` to validate generated code. If the code generation produces syntactically valid Python that `ast.parse` cannot handle (e.g., Unicode identifiers in function names, f-strings with complex expressions), or if the validation is applied at the wrong granularity, valid generated code gets rejected.

**Why it happens:** The `_sanitize_function_name()` at line 211 preserves Chinese characters (`\u4e00-\u9fff` range), which are valid Python 3 identifiers but may surprise some AST tools. The generated code also includes `HealerError(...)` with keyword arguments, string literals with escaped characters, and try-except blocks with variable capture.

More importantly, `ast.parse()` validates the ENTIRE file. If the code generator produces a partial file (e.g., during incremental repair in `_apply_fix`), the repaired code may be syntactically incomplete when parsed as a whole, even though the individual line is valid.

**Consequences of fixing incorrectly:**
- Removing `ast.parse` validation entirely allows broken code to reach pytest, wasting a subprocess invocation
- Making `ast.parse` more permissive (try/except around it) defeats its purpose
- Applying `ast.parse` to individual LLM snippets instead of the full file misses cross-line syntax issues (indentation, unclosed blocks)
- Applying `ast.parse` to the LLM snippet alone (as done in `llm_healer.py` line 193) may accept code that breaks when inserted into the file context (e.g., code with wrong indentation level)

**Prevention:**
- Keep `ast.parse` validation on the FULL generated file, not individual snippets
- In `_apply_fix()` (line 404), after splicing the LLM snippet into the file, validate the ENTIRE repaired file with `ast.parse`, not just the snippet
- The existing code at line 331 already does this correctly: `ast.parse(repaired_code)` where `repaired_code` is the full file after splice
- In `llm_healer.py` line 193, the `ast.parse(cleaned_code)` on the snippet is a PRE-filter only. The final validation in `self_healing_runner.py` line 331 is the authoritative check. This two-stage approach is correct and should be preserved
- Test with Chinese function names: `def test_销售出库测试(page: Page) -> None:` should pass `ast.parse`

**Detection:**
- Unit test: `ast.parse()` on a generated file with Chinese function name should succeed
- Unit test: `ast.parse()` on a file with try-except blocks containing HealerError should succeed
- Unit test: `ast.parse()` on a repaired file where LLM snippet was inserted should succeed
- Test: generate code from a real agent history and verify `validate_syntax()` returns True

**Warning signs the fix broke something:**
- Generated code that used to pass validation now fails -- Unicode handling changed
- LLM snippets that look valid get rejected -- pre-filter too strict
- Repaired code passes `ast.parse` but fails at runtime (indentation mismatch between snippet and file context) -- validation not catching structural issues

---

## Moderate Pitfalls

### Pitfall 6: _escape_string Missing Newline Handling for Non-Comment Output

**What goes wrong:** The `_escape_string()` method at line 650 only escapes `\` and `"`. For string literal contexts (inside quotes), this is mostly correct. But the `evaluate` action at line 545 does its own newline escaping: `_escape_string(code_str).replace("\n", "\\n")`. If any other action type receives a parameter with newlines and does NOT do this extra escaping, the generated code will have broken string literals.

**Prevention:**
- Audit all action types that put parameter values inside quoted strings: navigate (url), send_keys (keys), evaluate (code), input (text), select_dropdown (text), upload_file (path)
- Of these, `evaluate` already handles newlines. The others (navigate, send_keys, input, select_dropdown, upload_file) typically do not have newlines in their parameters, but should be hardened
- Consider adding `\n`, `\r`, `\t` escaping to `_escape_string()` itself, making it safe for all contexts
- If modifying `_escape_string`, be careful not to break the comment generation in `_translate_unknown` where newlines in comments are a DIFFERENT problem (Pitfall 2)

**Detection:**
- Unit test each action type with parameter values containing `\n`, `\r`, `\t`
- Verify the generated code passes `ast.parse()`

---

### Pitfall 7: _apply_fix Line Number Off-By-One in Self-Healing Repair

**What goes wrong:** The `_apply_fix()` method at line 404 uses 1-indexed line numbers from `_extract_error_line()`. The error line extraction at line 368 uses `re.search(r"test_\w+\.py:(\d+)", error_output)` to find the line number. If pytest reports the line number differently (e.g., the line BEFORE the error, or the decorator line instead of the function body), the fix gets applied to the wrong line.

**Why it happens:** pytest's traceback format varies:
- `test_xxx.py:42: Error` -- points to line 42 where the error occurred
- `test_xxx.py:40: in test_xxx` -- points to the call site, not the error line
- The regex `r"test_\w+\.py:(\d+)"` matches the FIRST occurrence, which may be the call site rather than the error line

**Prevention:**
- Use `re.findall()` instead of `re.search()` to get all line numbers, and prefer the LAST match (closest to the actual error)
- When no line number is found, the fallback strategy of finding the last `page.` line and replacing it is reasonable but fragile -- log a warning when using this fallback
- Test with real pytest output that has multiple `test_xxx.py:N` matches

**Detection:**
- Unit test `_extract_error_line` with a pytest traceback containing multiple file:line references
- Verify the LAST match is returned, not the first

---

### Pitfall 8: _read_dom_snapshot Step Number Extraction False Positive

**What goes wrong:** The `_read_dom_snapshot()` method at line 381 extracts a step number from the error output using `re.search(r"step[_\s](\d+)", error_output, re.IGNORECASE)`. If the error output contains text like "stepped on error" or "Step class" from Python internals, a wrong step number is extracted, and the wrong DOM snapshot is loaded for LLM healing.

**Prevention:**
- Tighten the regex to match only pytest output patterns: `r"(?:step|Step)[_\s](\d+)"` and require it to appear in a traceback line (prefixed with `E   ` or in a file path context)
- Or match the specific DOM snapshot path format: `r"dom/step_(\d+)\.txt"`
- The fallback to `step_1.txt` at line 397 is a safe default if the regex fails

**Detection:**
- Unit test with error output containing "stepped" or "Step" in unrelated context
- Verify fallback to step_1 when no step number is found

---

### Pitfall 9: HealingResult Frozen Dataclass Preventing Category Extension

**What goes wrong:** `HealingResult` at line 98 is a frozen dataclass with fields: `final_status`, `attempts`, `error_message`, `repaired_code_path`. If HEAL-01 adds an `error_category` field, all existing code that constructs `HealingResult` must be updated, including the 10+ return statements in `SelfHealingRunner.run()`.

**Prevention:**
- The FEATURES-HEAL01.md research recommends embedding the category as a string prefix in `error_message` (e.g., `"[env_invocation] unrecognized arguments"`). This avoids changing the dataclass entirely
- If a dedicated field is desired later, it can have a default value: `error_category: str = ""` -- but frozen dataclasses with defaults still require all positional args to be provided
- The safest approach: keep HealingResult unchanged, embed category in error_message string, parse it on the consumer side if needed

**Detection:**
- Verify all `HealingResult(...)` construction sites compile without changes
- Verify existing tests that assert on `error_message` content still pass

---

## Minor Pitfalls

### Pitfall 10: Timeout Branch Still Calls LLM Repair

**What goes wrong:** At line 201-214, when `subprocess.TimeoutExpired` is caught, the code calls `self._llm_repair()` on the timeout error. LLM repair on a timeout is almost never useful -- the test hung, and no code change will fix it if the issue is a Playwright selector wait or an infinite loop. The FEATURES-HEAL01.md correctly identifies this as `ENV_TIMEOUT` which should fail immediately.

**Prevention:**
- When the timeout categorization is implemented, ensure the timeout branch returns `HealingResult(failed)` immediately without calling `_llm_repair()`
- This is already covered by the FEATURES-HEAL01 design but worth calling out because the current code at line 206-213 calls `_llm_repair` inside the timeout catch block

---

### Pitfall 11: _truncate_error Truncates Category Prefix

**What goes wrong:** If the category is embedded as a prefix in `error_message` (e.g., `"[env_invocation] error: unrecognized arguments..."`) and the error is long, `_truncate_error()` at line 361 truncates from the front, potentially cutting off the category prefix. The consumer then cannot parse the category.

**Prevention:**
- Extract the category prefix before truncation, truncate the body, then re-attach the prefix
- Or truncate the error body BEFORE prepending the category prefix
- Or increase the `max_length` to account for the category prefix (category strings are ~20 chars, so `max_length=2020` would work)

---

### Pitfall 12: conftest.py Conflicting with Project-Level conftest

**What goes wrong:** The generated `conftest.py` defines `browser_context_args` fixture with `scope="session"`. If the project has a top-level `conftest.py` (it does not currently, but could in the future), pytest's conftest discovery would load both, and the session-scoped fixture might conflict.

**Prevention:**
- The current project has no top-level conftest.py, so this is not an immediate issue
- The `_cleanup()` method at line 345 deletes the conftest after execution, preventing long-term conflicts
- If a project-level conftest is added later, ensure it does not define `browser_context_args`

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| EXEC-01: Fix `--headed=false` | Pitfall 1: Wrong replacement flag | Remove flag entirely; test subprocess args contain no `--headed` variant |
| EXEC-02: Fix done action text | Pitfall 2: Newlines in comments | Sanitize summary text: replace newlines with spaces after lambda evaluation |
| EXEC-03: Isolate conftest output | Pitfall 3: WatchFiles in dev mode | `--reload-exclude "outputs"` for dev; production already uses `reload=False` |
| HEAL-01: Error categorization | Pitfall 4: Over-aggressive skipping | Anchor regex to pytest output format; default to CODE_RUNTIME for unknown returncode=1 |
| E2E-01: End-to-end validation | Pitfall 5: ast.parse false rejection | Validate full file, not snippets; test with Chinese function names |
| Post-fix regression | Pitfall 9: HealingResult schema change | Embed category in error_message string, do not add dataclass field |
| Timeout handling | Pitfall 10: LLM repair on timeout | Return failed immediately on TimeoutExpired, skip LLM repair |

## Test Requirements Per Fix

| Fix | Required Tests | Rationale |
|-----|---------------|-----------|
| EXEC-01 | 1. Assert subprocess args do not contain `--headed` 2. Assert removing the flag does not add `--headless` (which also does not exist) | Prevent the exact mistake the fix addresses |
| EXEC-02 | 1. Translate `done` with multi-line text, verify single-line output 2. Translate `done` with empty text 3. Translate `extract` with multi-line query 4. `ast.parse()` on generated file with `done` action | Newline leakage is the core issue; must verify for all unknown types |
| EXEC-03 | 1. Verify conftest written to `output_dir` (test file's parent) 2. Verify conftest cleaned up after execution 3. Verify no conftest written to project root | Isolation is the goal; verify the boundary |
| HEAL-01 | 1. Unit tests for classifier (10+ cases from FEATURES-HEAL01 test plan) 2. Integration test: ENV error returns immediately without LLM call 3. Integration test: CODE_RUNTIME still invokes LLM 4. False positive test: "SyntaxError" in Playwright output classifies as CODE_RUNTIME | Classifier correctness determines whether healing works at all |
| E2E-01 | 1. Generate code from real agent history, run pytest, verify meaningful result 2. Verify Chinese function names compile 3. Verify generated code with HealerError compiles | The entire pipeline must work end-to-end |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces after the fixes.

- [ ] **`--headed=false` removal:** Verify the subprocess args list is `["uv", "run", "pytest", test_file_path, "--timeout=60", "-v"]` with NO headed-related flag of any kind. A grep for `--headed` in self_healing_runner.py should return zero results.
- [ ] **Done text sanitization:** Verify the fix covers ALL action types that go through `_translate_unknown`, not just `done`. The `extract` and `search` actions also have free-text parameters that could contain newlines.
- [ ] **Error categorization integration:** Verify the classifier is called BEFORE `_llm_repair()`, not after. If the classifier is called after the first LLM attempt, ENV errors still waste one LLM call.
- [ ] **ast.parse on full file:** Verify the validation in `_llm_repair()` line 331 parses the ENTIRE repaired file, not just the LLM snippet. The snippet alone may parse but break the file structure.
- [ ] **Timeout fast-fail:** Verify the TimeoutExpired branch does NOT call `_llm_repair()` after the categorization change is in place.
- [ ] **conftest cleanup:** Verify `_cleanup()` runs in ALL code paths: success, failure, exception, and timeout. Currently it does, but the timeout branch at line 201 calls `continue` without cleanup -- cleanup only happens in the outer finally-equivalent blocks.

## Sources

- pytest-playwright CLI: `uv run pytest --help` output verified `--headed` is a boolean flag with no value argument -- HIGH confidence, verified in project environment
- `uv run pytest --headed=false` produces `error: argument --headed: ignored explicit argument 'false'` -- HIGH confidence, verified by execution
- Direct code analysis: `backend/core/self_healing_runner.py` (subprocess invocation, conftest generation, LLM repair, cleanup), `backend/core/action_translator.py` (action translation, string escaping, done handling), `backend/core/code_generator.py` (file generation, syntax validation), `backend/core/llm_healer.py` (LLM response cleaning, ast.parse pre-filter) -- HIGH confidence
- Existing research: `.planning/research/FEATURES-HEAL01.md` (error categorization design) -- HIGH confidence, same codebase
- `backend/run_server.py` line 36: `reload=False` in production -- HIGH confidence, direct code
- uvicorn `--reload` with WatchFiles: documented in CLAUDE.md and README.md as standard dev command -- HIGH confidence

---
*Pitfalls research for: v0.10.6 bug fix milestone -- fixing pytest invocation, code generation, conftest isolation, error categorization*
*Researched: 2026-04-24*
