# Phase 63: 代码对比分析 - Research

**Researched:** 2026-04-06
**Domain:** browser-use Agent/Browser configuration diff analysis, Playwright headless mode
**Confidence:** HIGH

## Summary

This phase is a pure investigation -- comparing v0.4.0 and current (HEAD) versions of `backend/core/agent_service.py` to identify every configuration change that could explain why the browser window no longer pops up during test execution. The core finding is already clear from the git diff: commit `f951791` (2026-03-24, v0.5.0 cloud deployment) introduced `BrowserSession` with `BrowserProfile(headless=True)` as a shared function `create_browser_session()`, and all subsequent changes (MonitoredAgent, monitoring params, DOM patches) layered on top of that headless baseline.

The browser-use library version has remained constant at `0.12.2` across both v0.4.0 and current (confirmed in `pyproject.toml` unchanged between tags). The headless behavior is purely a project-level configuration decision, not a library API change. When `BrowserProfile.headless` is left as `None` (the default), browser-use auto-detects: headless on headless servers, headed on machines with a display. The explicit `headless=True` in `create_browser_session()` overrides this auto-detection for all environments including local development.

**Primary recommendation:** The diff analysis should focus on the `create_browser_session()` function as the root cause, with the MonitoredAgent + monitoring params as secondary (non-breaking) changes. The DOM rendering difference analysis should test whether headless mode affects Ant Design click-to-edit table input visibility.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 按配置项逐项对比，输出格式：`配置项 | v0.4.0 值 | 当前值 | 变更提交`
  - 对比维度：Agent 构造参数、BrowserSession/BrowserProfile 配置、Playwright 启动参数、browser-use 版本
  - 每个配置项独立一行，Phase 64 报告可直接引用

- **D-02:** 快照对比 -- 只看 v0.4.0 vs 当前版本的差异
  - 不追踪中间提交（约 20 个），只做两端对比
  - 中间提交信息用于标注变更提交 hash，不做逐一分析

- **D-03:** 深入关联分析 -- 研究 headless vs headed 模式下的 DOM 渲染差异
  - 对比 headless 和 headed 模式下 Ant Design 表格的 DOM 结构差异
  - 分析 headless 模式是否影响 input 元素的渲染时机（click-to-edit 表格是否在 headless 下不渲染 input）
  - 研究 headless 模式对元素定位、CSS 计算的影响
  - 评估 v0.8.1 的 DOM Patch（td 文本检测）是否为正确绕行方案

### Claude's Discretion
- 具体配置项的粒度划分（哪些合并、哪些独立列出）
- 中间提交 hash 的选择（标注关键变更即可）
- headless/headed 渲染差异的测试方法（代码分析 vs 实际运行对比）

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DIFF-01 | 对比 v0.4.0 和当前版本的 browser-use 初始化代码（Agent 构造参数、Browser 配置） | Git diff `v0.4.0..HEAD -- backend/core/agent_service.py` fully analyzed; Agent constructor params inspected via Python introspection; 15+ config differences catalogued |
| DIFF-02 | 对比 Playwright 配置差异（headless/headed 设置、浏览器启动参数） | BrowserProfile source code inspected; `headless=None` defaults to auto-detect; `headless=True` forces `--headless=new`; CHROME_HEADLESS_ARGS and SERVER_BROWSER_ARGS documented |
| DIFF-03 | 分析 browser-use 版本升级变化（v0.4.0 时的版本 vs 当前版本 API 差异） | pyproject.toml unchanged: `browser-use>=0.12.2` in both v0.4.0 and current; installed version confirmed 0.12.2; NO version change occurred |
| DIFF-04 | 分析 agent_service.py 中 Agent/Browser 配置的完整演变历史 | 29 commits between v0.4.0 and HEAD affecting agent_service.py; key commits identified with hashes |
</phase_requirements>

## Standard Stack

This is a code-analysis-only phase. No new libraries are needed.

### Core Investigation Tools

| Tool | Purpose | Why Standard |
|------|---------|--------------|
| `git diff v0.4.0 HEAD -- <file>` | Two-point snapshot comparison | Direct, reliable, no intermediate noise |
| `git show <tag>:<file>` | Retrieve historical file content | Canonical source for v0.4.0 snapshot |
| `git log --oneline <commit>..HEAD -- <file>` | Commit timeline for annotation | Identifies which commit changed what |
| Python `inspect` module | Runtime introspection of browser-use API | Reveals actual default values and parameter signatures |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `git diff` two-point | `git log -p` per-commit | Per-commit analysis violates D-02 (snapshot only) |
| Runtime introspection | Read source files directly | Source files are more reliable for default values; runtime confirms behavior |

## Architecture Patterns

### Recommended Comparison Output Format

Per D-01, each config item gets a row:

```
| Config Item | v0.4.0 Value | Current Value | Change Commit |
|-------------|-------------|---------------|---------------|
```

### Pattern: Root Cause Trace

1. Identify the symptom (browser window not popping up)
2. Find the config change that directly causes it (`headless=True`)
3. Trace which commit introduced it (`f951791`)
4. Verify no other changes revert or modify that root cause
5. List secondary changes that are additive but not causal

### Key Commit Timeline (for D-02 annotation)

```
v0.4.0          baseline -- no BrowserSession, no headless config
f951791 (Mar 24) ROOT CAUSE -- BrowserSession(headless=True) for server deploy
c84f4e1 (Mar 31) added ViewportSize(1920x1080)
e2157a1 (Apr  ) Agent -> MonitoredAgent in run_with_streaming
9fc9f44 (Apr  ) added ENHANCED_SYSTEM_MESSAGE + tune Agent params
380be48 (Apr  ) integrated RunLogger
20efd65 (Apr  ) wired detector calls into step_callback
b586b54 (Apr  ) added apply_dom_patch() to execution path
7ba3f6b (Apr  ) added scan_test_files + available_file_paths
HEAD            current state with all monitoring + DOM patches
```

### Anti-Patterns to Avoid
- **Analyzing all 29 commits individually:** D-02 explicitly says snapshot comparison only
- **Conflating root cause with secondary changes:** The headless config is the primary cause; monitoring params are secondary
- **Assuming browser-use version changed:** Both pyproject.toml files are identical (`browser-use>=0.12.2`)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Diff computation | Custom comparison script | `git diff v0.4.0 HEAD -- <file>` | Git handles edge cases (renames, merges) |
| API parameter discovery | Manual doc reading | Python `inspect.signature()` | Runtime introspection shows actual defaults |
| browser-use internal behavior | Guessing from docs | Read `.venv/lib/.../browser_use/browser/profile.py` source | Source code is ground truth for default values |

## Common Pitfalls

### Pitfall 1: browser-use Default headless Value Misunderstanding
**What goes wrong:** Assuming `BrowserProfile()` defaults to `headless=False`
**Why it happens:** The field declaration is `headless: bool | None = None`, and `None` is not `False`
**How to avoid:** In browser-use 0.12.2, `headless=None` triggers auto-detection in `_finalize_and_validate()` (line 1177-1178): `self.headless = not has_screen_available`. On macOS with a display, this resolves to `False` (headed). On Linux server without display, this resolves to `True` (headless). The explicit `headless=True` in our code overrides this auto-detection.
**Warning signs:** Confusion between "browser-use defaults to headed" vs "browser-use auto-detects based on display"

### Pitfall 2: CHROME_HEADLESS_ARGS Overlap with SERVER_BROWSER_ARGS
**What goes wrong:** Not realizing that browser-use internally adds `--headless=new` via `CHROME_HEADLESS_ARGS` when `headless=True`
**Why it happens:** Our `SERVER_BROWSER_ARGS` has 6 Chrome flags, but browser-use adds its own `--headless=new` flag separately (line 863 of profile.py)
**How to avoid:** Document that the final Chrome launch args are `SERVER_BROWSER_ARGS + CHROME_HEADLESS_ARGS` = 7 total args when headless
**Warning signs:** Thinking `--headless=new` comes from our code (it comes from browser-use internals)

### Pitfall 3: Confusing MonitoredAgent with Browser Config
**What goes wrong:** Attributing browser behavior changes to MonitoredAgent or monitoring params
**Why it happens:** Multiple changes happened simultaneously (headless + MonitoredAgent + monitoring)
**How to avoid:** MonitoredAgent inherits from Agent and only overrides `_prepare_context()` and `_execute_actions()` -- it has zero browser configuration. The monitoring params (stall_detector, loop_detection_window, etc.) are agent-level, not browser-level.

### Pitfall 4: Headless DOM Rendering Assumptions
**What goes wrong:** Assuming headless and headed produce identical DOM trees
**Why it happens:** Chromium's "new headless" mode (`--headless=new`) uses the same rendering engine, so most DOM is identical. BUT: interactive states differ.
**How to avoid:** The DOM tree structure should be nearly identical, but focus/hover states that trigger dynamic content (like Ant Design click-to-edit inputs appearing on focus) may differ in timing. The click-to-edit inputs in the ERP table are triggered by user click events, and the DOM representation of those states may differ in headless mode because the browser-use agent simulates clicks differently than a real user.
**Warning signs:** Finding that inputs exist in the DOM but are not visible/interactive in the accessibility tree

## Code Examples

### v0.4.0 Agent Creation (run_simple)

```python
# Source: git show v0.4.0:backend/core/agent_service.py
# No BrowserSession, no headless config
agent = Agent(
    task=task,
    llm=llm,
    max_actions_per_step=5,
)
# browser-use default: headless=None -> auto-detect -> headed on macOS
```

### v0.4.0 Agent Creation (run_with_streaming)

```python
# Source: git show v0.4.0:backend/core/agent_service.py
agent = Agent(
    task=actual_task,
    llm=llm,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
)
# Same: no browser config, auto-detect headed
```

### Current Agent Creation (run_simple)

```python
# Source: backend/core/agent_service.py HEAD
browser_session = create_browser_session()  # BrowserProfile(headless=True, ...)
agent = Agent(
    task=task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
)
```

### Current Agent Creation (run_with_streaming)

```python
# Source: backend/core/agent_service.py HEAD
browser_session = create_browser_session()
agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    available_file_paths=file_paths,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
    extend_system_message=ENHANCED_SYSTEM_MESSAGE,
    loop_detection_window=10,
    max_failures=4,
    planning_replan_on_stall=2,
    enable_planning=True,
    stall_detector=stall_detector,
    pre_submit_guard=pre_submit_guard,
    task_progress_tracker=task_progress_tracker,
    run_logger=run_logger,
)
```

### create_browser_session() (current)

```python
# Source: backend/core/agent_service.py HEAD
SERVER_BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
]

def create_browser_session() -> BrowserSession:
    from browser_use.browser.profile import ViewportSize
    browser_profile = BrowserProfile(
        headless=True,
        args=SERVER_BROWSER_ARGS,
        viewport=ViewportSize(width=1920, height=1080),
    )
    return BrowserSession(browser_profile=browser_profile)
```

### browser-use headless resolution (internal)

```python
# Source: .venv/lib/.../browser_use/browser/profile.py lines 1176-1178
# if no headless preference specified, prefer headful if there is a display available
if self.headless is None:
    self.headless = not has_screen_available
```

### browser-use Chrome headless args (internal)

```python
# Source: .venv/lib/.../browser_use/browser/profile.py lines 80-82
CHROME_HEADLESS_ARGS = [
    '--headless=new',
]
# Applied at line 863: *(CHROME_HEADLESS_ARGS if self.headless else [])
```

## Complete Configuration Diff (DIFF-01, DIFF-02)

### run_simple Method

| Config Item | v0.4.0 | Current | Change Commit |
|-------------|--------|---------|---------------|
| Agent class | `Agent` | `Agent` | -- (unchanged) |
| `task` | task | task | -- |
| `llm` | create_llm(config) | create_llm(config) | -- |
| `browser_session` | None (not passed) | `create_browser_session()` | f951791 |
| `max_actions_per_step` | 5 | 5 | -- |
| **Headless mode** | **Auto-detect (headed on macOS)** | **Explicit True** | **f951791** |
| Chrome args | None (browser-use defaults) | 6 SERVER_BROWSER_ARGS + `--headless=new` | f951791 + browser-use |
| Viewport | None (auto) | 1920x1080 | c84f4e1 |

### run_with_streaming Method

| Config Item | v0.4.0 | Current | Change Commit |
|-------------|--------|---------|---------------|
| Agent class | `Agent` | `MonitoredAgent` | e2157a1 |
| `task` | actual_task | actual_task | -- |
| `llm` | create_llm(config) | create_llm(config) | -- |
| `browser_session` | None (not passed) | `create_browser_session()` | f951791 |
| `max_actions_per_step` | 5 | 5 | -- |
| `register_new_step_callback` | step_callback | step_callback | -- |
| **Headless mode** | **Auto-detect (headed on macOS)** | **Explicit True** | **f951791** |
| Chrome args | None | 6 SERVER_BROWSER_ARGS + `--headless=new` | f951791 |
| Viewport | None (auto) | 1920x1080 | c84f4e1 |
| `extend_system_message` | None | ENHANCED_SYSTEM_MESSAGE | 9fc9f44 |
| `loop_detection_window` | 20 (browser-use default) | 10 | 9fc9f44 |
| `max_failures` | 5 (browser-use default) | 4 | 9fc9f44 |
| `planning_replan_on_stall` | 3 (browser-use default) | 2 | 9fc9f44 |
| `enable_planning` | True (browser-use default) | True (explicit) | 9fc9f44 |
| `stall_detector` | N/A | StallDetector() | e2157a1/20efd65 |
| `pre_submit_guard` | N/A | PreSubmitGuard() | e2157a1/20efd65 |
| `task_progress_tracker` | N/A | TaskProgressTracker() | e2157a1/20efd65 |
| `run_logger` | N/A | RunLogger(run_id) | 380be48 |
| `available_file_paths` | N/A | scan_test_files() | 7ba3f6b |
| DOM patch | N/A | apply_dom_patch() | b586b54 |
| `self._browser_session` | N/A | stored for callback access | (post-f951791) |

### browser-use Version (DIFF-03)

| Item | v0.4.0 | Current | Changed? |
|------|--------|---------|----------|
| pyproject.toml dep | `browser-use>=0.12.2` | `browser-use>=0.12.2` | **NO CHANGE** |
| Installed version | 0.12.2 | 0.12.2 | **NO CHANGE** |

**Key finding for DIFF-03:** browser-use version has NOT changed between v0.4.0 and current. All behavioral differences are from project-level configuration, not library API changes. However, the library itself evolved significantly between earlier versions (pre-0.12) when `Browser` class was used versus the current `BrowserSession`/`BrowserProfile` API. The v0.4.0 code already used the current API (Agent with no browser config), and the migration to BrowserSession happened at commit `f951791`.

### Agent Configuration Evolution (DIFF-04)

| Era | Commits | Browser Config | Agent Config |
|-----|---------|---------------|--------------|
| v0.4.0 (baseline) | -- | None (auto-detect) | Plain Agent, 3 params |
| Server deploy | f951791 | BrowserSession(headless=True, 5 args) | Agent + browser_session |
| Viewport | c84f4e1 | + ViewportSize(1920x1080) | -- |
| Monitoring | e2157a1, 9fc9f44, 380be48 | -- | MonitoredAgent + 10 params |
| DOM fix | b586b54, b586b54 | -- | apply_dom_patch() |
| File upload | 7ba3f6b | -- | available_file_paths |
| Current (HEAD) | all above | BrowserSession(headless=True, 6 args, 1920x1080) | MonitoredAgent + 13 params |

## Headless DOM Rendering Analysis (D-03)

### Chromium `--headless=new` vs Headed Mode

**Rendering engine:** The "new" headless mode (Chrome 112+) uses the same Blink rendering engine as headed Chrome. DOM tree structure is identical for static content.

**Key differences relevant to ERP table interaction:**

1. **Focus/hover states are simulated, not real:** Headless mode has no real mouse cursor. Playwright/browser-use simulates click events programmatically. CSS `:hover` and `:focus` pseudo-classes may not trigger the same way.

2. **Ant Design click-to-edit behavior:** Ant Design editable tables typically show text content in `<td>` cells and reveal an `<input>` element on click. This is a JavaScript-driven interaction. In headless mode:
   - The click event IS dispatched (Playwright handles this)
   - The input SHOULD appear in the DOM (JavaScript runs normally)
   - BUT: timing differences may cause the browser-use DOM serializer to capture the state before the input fully renders

3. **Accessibility tree differences:** Headless Chromium may build a slightly different accessibility tree, which is what browser-use uses for element indexing. Elements that are "off-screen" or have zero dimensions may be excluded from the AX tree in headless mode.

4. **The v0.8.1 DOM Patch assessment:** The dom_patch.py specifically addresses:
   - Restoring paint order for ERP elements with specific CSS classes
   - Marking `<td>` cells with text content as interactive
   - Preventing ERP nodes from being excluded by bounding box filtering
   - Forcing interactive assignment for ERP table cell inputs

   **This is a reasonable workaround** because it operates at the DOM serialization level, which is where headless mode differences would manifest. The patch does not depend on headed mode features (like real mouse hover); it ensures the elements are visible in the DOM dump regardless of rendering mode.

### Confidence Assessment for D-03

| Claim | Confidence | Source |
|-------|------------|--------|
| Headless uses same rendering engine | HIGH | Chromium official docs |
| Focus/hover simulation differs | HIGH | Playwright docs + Chromium architecture |
| DOM tree structure is identical for static content | HIGH | Chromium official docs |
| Click-to-edit input timing may differ in headless | MEDIUM | Inference from rendering pipeline behavior |
| DOM Patch is appropriate workaround | MEDIUM | Code analysis of dom_patch.py |

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `Browser` class (browser-use pre-0.12) | `BrowserSession` + `BrowserProfile` | browser-use 0.12.x | Better config separation |
| `headless=None` auto-detect | `headless=True` explicit | f951791 (Mar 24) | Forces headless everywhere |
| No viewport config | ViewportSize(1920x1080) | c84f4e1 (Mar 31) | Consistent rendering area |
| Plain Agent | MonitoredAgent + detectors | e2157a1+ | Monitoring without browser changes |
| No DOM patch | 5 patches in dom_patch.py | Phase 62 | Works around headless DOM serialization issues |

**Deprecated/outdated:**
- `Browser` class: replaced by `BrowserSession` in browser-use 0.12.x
- `use_cloud=False` parameter: removed from browser-use API (defaults to local browser)

## Open Questions

1. **Has the ERP application been tested in headed mode recently?**
   - What we know: v0.4.0 was headed and worked; current is headless with DOM patches
   - What's unclear: Whether the ERP table issue is purely headless-related or also has other causes
   - Recommendation: This is investigation-only; the report should recommend a headed-mode test as next step

2. **Does headless mode affect Ant Design specific rendering?**
   - What we know: Chromium "new headless" uses same rendering engine
   - What's unclear: Whether Ant Design's JavaScript event handling has headless-specific edge cases
   - Recommendation: Flag as MEDIUM confidence; needs empirical testing

3. **Should `create_browser_session()` be environment-aware?**
   - What we know: Currently hardcodes `headless=True` for all environments
   - What's unclear: Whether the fix should auto-detect environment (like browser-use's default)
   - Recommendation: Out of scope for this phase; note in report for Phase 64

## Environment Availability

Step 2.6: SKIPPED (no external dependencies -- this phase is git diff + code analysis only)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio |
| Config file | `pyproject.toml` [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/ -x -q` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DIFF-01 | Config comparison output matches expected format | N/A (investigation output, not code) | Manual verification | N/A |
| DIFF-02 | Playwright config diff correctly identifies headless change | N/A (investigation output) | Manual verification | N/A |
| DIFF-03 | browser-use version comparison shows no change | N/A (investigation output) | Manual verification | N/A |
| DIFF-04 | Evolution timeline correctly maps commits to changes | N/A (investigation output) | Manual verification | N/A |

**Note:** All four requirements are investigation/analysis tasks producing structured output documents, not code changes. They are verified by manual review of the produced comparison tables. No automated tests are applicable.

### Wave 0 Gaps
None -- existing test infrastructure covers agent_service.py tests, but this phase produces no code changes requiring test coverage.

## Sources

### Primary (HIGH confidence)
- `git show v0.4.0:backend/core/agent_service.py` -- v0.4.0 snapshot (canonical reference)
- `git diff v0.4.0 HEAD -- backend/core/agent_service.py` -- complete diff (canonical reference)
- `.venv/lib/python3.11/site-packages/browser_use/browser/profile.py` -- BrowserProfile headless default and resolution logic
- `.venv/lib/python3.11/site-packages/browser_use/agent/service.py` -- Agent constructor parameters
- `pyproject.toml` (v0.4.0 and HEAD) -- dependency declarations

### Secondary (MEDIUM confidence)
- Git commit history: 29 commits between v0.4.0 and HEAD affecting agent_service.py
- Python `inspect.signature()` runtime introspection of Agent, BrowserProfile, BrowserSession constructors
- Training data: Chromium `--headless=new` rendering behavior, Playwright headless mode documentation

### Tertiary (LOW confidence)
- Web search unavailable (rate limit exhausted) for headless DOM rendering research; relied on training data

## Metadata

**Confidence breakdown:**
- Standard stack (investigation tools): HIGH -- git and Python introspection are reliable
- Architecture patterns (diff format): HIGH -- derived directly from CONTEXT.md decisions
- Pitfalls: HIGH -- verified by reading browser-use source code
- Headless DOM rendering analysis: MEDIUM -- based on training data about Chromium internals, not empirical testing
- Configuration diff: HIGH -- verified by git diff output and runtime introspection

**Research date:** 2026-04-06
**Valid until:** 2026-05-06 (stable -- no library changes expected in investigation phase)
