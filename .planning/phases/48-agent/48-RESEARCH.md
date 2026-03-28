# Phase 48: MonitoredAgent 子类与监控检测器 - Research

**Researched:** 2026-03-27
**Domain:** Python async patterns, browser-use Agent subclassing, pure unit testing (pytest, no real browser)
**Confidence:** HIGH

## Summary

This phase creates a `MonitoredAgent(Agent)` subclass that overrides two methods in browser-use's Agent (`_prepare_context` and `_execute_actions`) to inject intervention messages and optionally block submit actions. Three independent detectors (`StallDetector`, `PreSubmitGuard`, `TaskProgressTracker`) are each self-contained in a separate file with pure Python logic. All are invoked via `step_callback` to detect issues and accumulate intervention messages in `_pending_interventions`. `_prepare_context()` injects those messages into LLM context AFTER browser-use's built-in nudges. `_execute_actions()` checks PreSubmitGuard before executing the submit click, and blocks if needed.

Tests use mock `BrowserStateSummary`, `AgentOutput`, and `MessageManager` -- no real browser or LLM required. Coverage target: >= 80%.

**Primary recommendation:** Subclass browser-use `Agent`, override `_prepare_context()` to inject pending interventions after built-in nudges, clear `_pending_interventions` each cycle. Override `_execute_actions()` to optionally block submit clicks via PreSubmitGuard. All detectors are pure dataclass-based Python logic testable with mock data, no real browser.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** PreSubmitGuard uses JS evaluate via browser_context to get actual field values, compared with expected values
- **D-02:** Use ERP-specific JS validation scripts, not generic DOM scanning
- **D-03:** Each detector in its own file: `backend/agent/monitored_agent.py`, `backend/agent/stall_detector.py`, `backend/agent/pre_submit_guard.py`, `backend/agent/task_progress_tracker.py`
- **D-04:** Each detector self-manages its own state (StallDetector: consecutive failure counter, stagnant DOM counter; MonitoredAgent only creates instances and calls check())
- **D-05:** Intervention messages in Chinese, format: `[type label] + description + suggested action`
- **D-06:** Pure unit tests with mock. No real browser. Coverage >= 80%
- **D-07:** Detector exceptions do not block Agent execution; only log errors (category="monitor"). Agent continues without intervention features
- **D-08:** Fault-tolerant. Detector exceptions do not block execution; only log errors. Agent continues running.

### Claude's Discretion
- StallDetector internal data structure choice (deque vs list)
- PreSubmitGuard JS script specific selectors
- TaskProgressTracker step parsing regex implementation
- Unit test mock data design
- Intervention message wording

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SUB-01 | MonitoredAgent subclass, override `_prepare_context()` to inject custom interventions after built-in nudges | Agent._prepare_context() flow verified: context_messages cleared by prepare_step_state() at line 194, then built-in nudges injected via _add_context_message(). Our override runs super() first, then injects from _pending_interventions. |
| SUB-02 | step_callback only detects and stores intervention messages to `_pending_interventions`, does not directly call `_add_context_message()` | Verified: register_new_step_callback fires AFTER LLM output and BEFORE action execution. step_callback accumulates messages in list. _prepare_context injects them on the next step. Correct per CONTEXT.md D-04. |
| SUB-03 | Override `_execute_actions()` to optionally block submit click via PreSubmitGuard | Verified: _execute_actions() calls self.multi_act(). If PreSubmitGuard returns block, we skip the action and return an error ActionResult with the validation report. browser-use has similar pattern in _inject_replan_nudge() (line 1454). |
| MON-01 | StallDetector: consecutive 2 failures on same target_index with same action and failure evaluation triggers intervention | StallDetector tracks consecutive failures via _history list of StepRecords, checking action_name, target_index, evaluation, dom_hash. |
| MON-02 | StallDetector: 3 consecutive stagnant DOM hashes (page unchanged) triggers intervention | Verified via _check_stagnant_dom(): checks last N steps for identical dom_hash using set() of recent N hashes. |
| MON-03 | StallDetector: success resets consecutive failure counter | Verified: _check_consecutive_failures() breaks loop on success keyword in evaluation. |
| MON-04 | PreSubmitGuard: regex extract expected values from task description (sales amount, logistics fee, amount, payment status) | Verified via EXPECTATION_PATTERNS with Chinese and English patterns. |
| MON-05 | PreSubmitGuard: detect submit intent (click + confirm/save/submit button text), and block via _execute_actions override | Verified: checks action_name=="click" and SUBMIT_KEYWORDS in button text. |
| MON-06 | PreSubmitGuard: skip validation when no expectations found, skip blocking | Verified: _extract_expectations returns empty dict, guard returns should_block=False. |
| MON-07 | TaskProgressTracker: parse structured step list from task (supports Step N, Chinese numbered, checkbox, numbered formats) | Verified: STEP_PATTERNS regex list with 4 patterns. |
| MON-08 | TaskProgressTracker: emit warning when remaining_steps < remaining_tasks * 1.5, urgent when remaining_steps <= remaining_tasks | Verified: check_progress() computes remaining_steps = max_steps - current_step, compares against remaining_tasks. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| browser-use | 0.12.x | Agent base class to subclass | Standard browser automation framework |
| pytest | 8.x | Test framework | Python standard testing |
| dataclasses | stdlib | Detector return types | Frozen dataclasses for immutability |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| re | stdlib | Regex pattern matching | Field extraction, step parsing |
| collections.deque | stdlib | Bounded history for StallDetector | Efficient sliding window |

**Installation:**
```bash
pip install pytest  # Already installed via uv sync
```

**Version verification:** stdlib modules require no additional installation.

## Architecture Patterns

### Recommended Project Structure
```
backend/agent/
    __init__.py
    monitored_agent.py        # MonitoredAgent(Agent) subclass
    stall_detector.py          # StallDetector dataclass
    pre_submit_guard.py        # PreSubmitGuard dataclass
    task_progress_tracker.py   # TaskProgressTracker dataclass
    prompts.py                 # CHINESE_ENHANCEMENT (existing), ENHANCED_SYSTEM_MESSAGE (Phase 49)
    browser_agent.py           # Deprecated UIBrowserAgent (reference only)
    proxy_agent.py             # Proxy agent (unrelated)

backend/tests/unit/
    test_monitored_agent.py    # MonitoredAgent + detector tests
```

### Pattern 1: Agent Subclassing for Message Injection
**What:** Override `_prepare_context()` to inject custom messages after browser-use clears context_messages.
**When to use:** When you need to pass intervention messages into the LLM's context.
**Critical constraint:** browser-use's `prepare_step_state()` clears `context_messages` (line 194 of MessageManager). Therefore injection MUST happen AFTER `super()._prepare_context()`.

The built-in nudges (replan, exploration, loop detection, budget warning) also call `_add_context_message()` -- they run AFTER `create_state_messages()` but BEFORE our custom injection point.

**Implementation:**
```python
class MonitoredAgent(Agent):
    def __init__(self, *, stall_detector, pre_submit_guard, task_progress_tracker, **kwargs):
        super().__init__(**kwargs)
        self._stall_detector = stall_detector
        self._pre_submit_guard = pre_submit_guard
        self._task_tracker = task_progress_tracker
        self._pending_interventions: list[str] = []

    async def _prepare_context(self, step_info=None):
        result = await super()._prepare_context(step_info)
        # After super(), context_messages contains built-in nudges.
        # Now inject our custom interventions.
        if self._pending_interventions:
            for msg in self._pending_interventions:
                self._message_manager._add_context_message(UserMessage(content=msg))
            self._pending_interventions = []
        return result
```

**Key timing:**
1. `_prepare_context()` calls `prepare_step_state()` which clears `context_messages` (line 194)
2. Then calls `create_state_messages()` which sets the state message
3. Then calls built-in nudges that use `_add_context_message()` (lines 1129-1133 of Agent service.py)
4. Our override runs AFTER `super()._prepare_context()` -- so built-in nudges AND custom interventions are in `context_messages` together
5. `get_messages()` returns all messages including our injected ones

### Pattern 2: Action Blocking via _execute_actions Override
**What:** Override `_execute_actions()` to optionally block submit clicks.
**When to use:** When PreSubmitGuard detects a submit click with mismatched fields.
**Critical constraint:** `_execute_actions()` is only 5 lines in browser-use (calls `self.multi_act()`). To block an action, we must skip calling super and return an error result. The LLM will see the error in the next step and try a different approach.

**IMPORTANT:** Only the FIRST action in the action list is checked. If a submit click is detected, the rest of the actions are still executed. This is intentional -- submit is a terminal action that should not be mixed with other actions.

**IMPORTANT:** PreSubmitGuard.check() signature requires `actual_values` as a parameter (from design doc). In unit tests, pass `actual_values=None` or a mock dict. In Phase 50 integration, `browser_session.page.evaluate()` will be used to get actual values. This means Phase 48 PreSubmitGuard is fully testable without a browser.

**Implementation:**
```python
async def _execute_actions(self):
    if self.state.last_model_output is None:
        await super()._execute_actions()
        return

    actions = self.state.last_model_output.action
    if not actions:
        await super()._execute_actions()
        return

    # Check first action for submit intent
    first_action = actions[0]
    action_data = first_action.model_dump(exclude_unset=True)
    action_name = next(iter(action_data.keys()), 'unknown')

    if action_name != 'click':
        await super()._execute_actions()
        return

    # PreSubmitGuard checks require actual_values from JS
    # For unit testing, pass None; integration will use browser
    result = self._pre_submit_guard.check(
        action_name=action_name,
        target_index=action_data.get('click', {}).get('index'),
        task=self.task,
        actual_values=None,  # None in unit tests; dict in integration
        submit_button_text=...,  # Would come from DOM in integration
    )

    if not result.should_block:
        await super()._execute_actions()
        return

    # Block the submit click
    error_msg = result.message
    self.state.last_result = [ActionResult(error=error_msg)]
    self._message_manager._add_context_message(UserMessage(content=error_msg))
    logger.warning(f"[PreSubmitGuard] Blocked submit: {error_msg[:100]}")
```

### Pattern 3: Detector Self-Management
**What:** Each detector maintains its own state internally.
**When to use:** All detectors -- StallDetector tracks history, TaskProgressTracker tracks steps/completed steps, PreSubmitGuard caches expectations.
**Key insight:** MonitoredAgent only creates instances and calls check(). It does not manage detector state.

### Anti-Patterns to Avoid
- **Tight coupling via shared mutable state:** Do NOT pass mutable objects between detectors. Each detector returns a frozen result (dataclass with frozen=True). MonitoredAgent accumulates results in a local list. This ensures detectors are independent and testable in isolation.
- **Storing detector references as class-level state:** Do NOT store detectors as class-level state. Create them per-run and pass via constructor. This makes testing easier.
- **Overriding too many methods:** Only override `_prepare_context()` and `_execute_actions()`. Do not override step(), run(), or other methods. This keeps the subclass surface area small.
- **Injecting messages in step_callback:** Do NOT call `_add_context_message()` in step_callback. It fires AFTER the LLM call and the messages would be cleared by next step's `prepare_step_state()`. Instead, append to `_pending_interventions` and inject in `_prepare_context()`.
- **Modifying _pending_interventions in _execute_actions:** Do NOT clear _pending_interventions in _execute_actions. They are consumed in the next step's `_prepare_context()`. If you clear them too early, the next step loses its intervention messages. Clear only AFTER successful injection.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Stall detection logic | Custom loop detection from scratch | StallDetector dataclass | Proven patterns, edge cases covered, easy to test |
| Message injection timing | Custom message injection in step_callback | Override `_prepare_context()` after super() | context_messages get cleared; must inject after built-in nudges |
| Submit action blocking | Custom action filtering in _execute_actions | Override `_execute_actions()` with PreSubmitGuard check | PreSubmitGuard returns frozen result; no browser needed for decision |
| Task step parsing | Custom regex parsing | TaskProgressTracker dataclass | Support 4 formats, well-tested with unit tests |
| DOM fingerprinting | Custom hashing/comparison | StallDetector._check_stagnant_dom() | Simple set comparison of last N hashes; proven, fast |

**Key insight:** Each detector is a self-contained dataclass with a single `check()` method. MonitoredAgent is a thin orchestrator that wires detectors together. No complex framework needed.

## Common Pitfalls

### Pitfall 1: context_messages Cleared Too Early
**What goes wrong:** Injecting intervention messages in step_callback (via `_add_context_message`) appears to work, but `prepare_step_state()` on the next step clears `context_messages` (line 194 of MessageManager), so the injected messages are lost.
**Why it happens:** The browser-use Agent flow is: step_callback fires after LLM output -> _execute_actions -> _finalize. On the next step, `_prepare_context()` calls `prepare_step_state()` which does `self.state.history.context_messages.clear()`. This happens BEFORE built-in nudges.
**How to avoid:** Store interventions in `_pending_interventions` list in step_callback. Inject them in `_prepare_context()` AFTER `super()._prepare_context()` call (which includes built-in nudges). This way they survive the `get_messages()` call.
**Warning signs:** Intervention messages appear in logs but LLM does not change behavior.

### Pitfall 2: Overriding Too Many Methods
**What goes wrong:** Overriding many Agent methods creates maintenance burden and breakage on browser-use updates.
**Why it happens:** The temptation to override many methods to add hooks.
**How to avoid:** Only override `_prepare_context()` and `_execute_actions()`. These are the only two extension points needed. Everything else uses the parent class as-is.
**Warning signs:** Unit tests break when browser-use updates its internal API.

### Pitfall 3: Stale Detector State Across Runs
**What goes wrong:** If detector state persists across runs, stale data from a previous run causes false positives.
**Why it happens:** Detectors are created once and reused.
**How to avoid:** Create fresh detector instances per run. In Phase 50, AgentService will create new instances for each `run_with_streaming()` call.
**Warning signs:** Intervention messages appear at the start of a new run.

### Pitfall 4: PreSubmitGuard False Positives
**What goes wrong:** PreSubmitGuard blocks legitimate submit clicks because regex extraction is too greedy or too strict.
**Why it happens:** Regex patterns may match unexpected text in task descriptions (e.g., "amount" matching in non-field contexts).
**How to avoid:** Only trigger when action is "click" AND button text contains submit keywords AND expectations were actually extracted. When `_extract_expectations()` returns empty dict, skip validation entirely (MON-06).
**Warning signs:** Agent fails to submit valid forms.

### Pitfall 5: TaskProgressTracker with Unstructured Tasks
**What goes wrong:** If task description has no parseable steps, tracker tracks zero tasks and never emits warnings.
**Why it happens:** Not all tasks follow "Step N: ..." format.
**How to avoid:** When `_steps` is empty after `parse_task()`, `check_progress()` returns empty ProgressResult immediately (verified in code and tests).
**Warning signs:** No progress warnings ever appear.

### Pitfall 6: StallDetector _check_consecutive_failures Bug
**What goes wrong:** The impl plan's `_check_consecutive_failures()` iterates `self._history` in reversed order, checking `record.action_name != last_action or record.target_index != last_index`. On the FIRST iteration, `last_action` and `last_index` are None, so the first record always breaks immediately.
**Why it happens:** The loop initializes `last_action = None` and `last_index = None`, then on the first iteration checks `record.action_name != None` which is always True, breaking the loop before counting any failures.
**How to avoid:** Initialize `last_action` and `last_index` from the first record BEFORE the comparison. The correct flow: read first record to set baseline, then count consecutive matches from the end.
**Warning signs:** StallDetector never triggers on consecutive failures.

**Correct implementation:**
```python
def _check_consecutive_failures(self) -> StallResult:
    consecutive = 0
    last_action = None
    last_index = None

    for record in reversed(self._history):
        is_failure = bool(FAILURE_KEYWORDS.search(record.evaluation))
        if not is_failure:
            break  # Success resets
        if last_action is None:
            # First failure record -- set baseline
            last_action = record.action_name
            last_index = record.target_index
            consecutive = 1
            continue
        if record.action_name != last_action or record.target_index != last_index:
            break  # Different action or target
        consecutive += 1

    if consecutive >= self.max_consecutive_failures:
        return StallResult(should_intervene=True, message=...)
    return StallResult(should_intervene=False, message="")
```

## Code Examples

Verified patterns from browser-use Agent source code analysis:

### _prepare_context Flow (from browser_use/agent/service.py lines 1063-1136)
```python
# Source: .venv/lib/python3.11/site-packages/browser_use/agent/service.py
# The CRITICAL flow for message injection:

async def _prepare_context(self, step_info=None):
    # 1. Get browser state
    browser_state_summary = await self.browser_session.get_browser_state_summary(...)

    # 2. prepare_step_state() CLEARS context_messages (line 194 of MessageManager)
    self._message_manager.prepare_step_state(
        browser_state_summary=browser_state_summary,
        model_output=self.state.last_model_output,
        result=self.state.last_result,
        step_info=step_info,
    )

    # 3. create_state_messages() sets the state message
    self._message_manager.create_state_messages(...)

    # 4. Built-in nudges ADD context messages via _add_context_message()
    await self._inject_budget_warning(step_info)     # line 1129
    self._inject_replan_nudge()                      # line 1130
    self._inject_exploration_nudge()                 # line 1131
    self._inject_loop_detection_nudge()              # line 1133

    # 5. OUR INJECTION POINT: After super()._prepare_context()
    # Inject _pending_interventions here -- they will be in context_messages
    # and will be included in get_messages()
    return browser_state_summary
```

### _execute_actions (from browser_use/agent/service.py lines 1187-1193)
```python
# Source: .venv/lib/python3.11/site-packages/browser_use/agent/service.py
# Only 5 lines -- easy to override:

async def _execute_actions(self):
    if self.state.last_model_output is None:
        raise ValueError('No model output to execute actions from')

    result = await self.multi_act(self.state.last_model_output.action)
    self.state.last_result = result
```

### _add_context_message (from MessageManager, line 553-557)
```python
# Source: .venv/lib/python3.11/site-packages/browser_use/agent/message_manager/service.py
# Public method -- appends to context_messages list:

def _add_context_message(self, message: BaseMessage) -> None:
    self.state.history.context_messages.append(message)
```

### register_new_step_callback (from Agent.__init__, line 571)
```python
# Stored as self.register_new_step_callback
# Called in _handle_post_llm_processing() (lines 1685-1697)
# AFTER LLM output, BEFORE action execution:

if self.register_new_step_callback and self.state.last_model_output:
    if inspect.iscoroutinefunction(self.register_new_step_callback):
        await self.register_new_step_callback(
            browser_state_summary,
            self.state.last_model_output,
            self.state.n_steps,
        )
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| step_callback direct injection | _pending_interventions + _prepare_context override | Phase 48 | Messages survive context_messages clearing |
| No action blocking | _execute_actions override with PreSubmitGuard | Phase 48 | Can block submit clicks with validation report |
| Monolithic detector file | One file per detector | Phase 48 | Independent testability, maintainability |
| browser-use loop detection (5/8/12 thresholds) | StallDetector (2 failure threshold) | Phase 48 | Faster stall detection, aggressive for limited step budget |

**Deprecated/outdated:**
- Phase 39 loop intervention code: Already cleaned in Phase 45. New implementation is fresh, no legacy from Phase 39.
- UIBrowserAgent: Marked as deprecated in codebase but can reference for `extend_system_message` usage pattern. `MonitoredAgent` replaces this class's role.
- `CHINESE_ENHANCEMENT` prompt: Will be replaced by `ENHANCED_SYSTEM_MESSAGE` in Phase 49. MonitoredAgent does not use `CHINESE_ENHANCEMENT` directly. It will use `extend_system_message` parameter passed from Phase 50. `extend_system_message` is injected at Agent construction time (line 498-499 of Agent.__init__). MonitoredAgent passes it through to parent via `**kwargs`.

**Data class design notes:**
- `StallDetector.check()` returns `StallResult(should_intervene=True/False, message="")` -- frozen dataclass, immutable result. Do NOT return mutable objects. Use `frozen=True` on result dataclasses. Aligns with CLAUDE.md immutability requirement.
- `TaskProgressTracker` uses mutable internal state (`_steps`, `_completed_steps`) but the output `check_progress()` is a frozen `ProgressResult`. This is acceptable since progress tracking requires mutable state. Use `dataclass` without `frozen=True` for TaskProgressTracker itself.
- `StallDetector._history` should use `collections.deque(maxlen=50)` to cap history at 50 records. The design doc uses a plain list. Deque is safer for performance. The history will grow to at most ~30 records per run (30 steps). For Phase 48, both work. In Phase 50 integration, consider deque for bounded history.

**IMPORTANT: File path discrepancy between impl plan and CONTEXT.md.** The impl plan places files at `backend/core/` but CONTEXT.md D-03 specifies `backend/agent/`. CONTEXT.md takes precedence. Planners should use the CONTEXT.md file paths (`backend/agent/`) not the impl plan paths (`backend/core/`).

## Open Questions

1. **PreSubmitGuard JS Execution Without Real Browser**
   - What we know: PreSubmitGuard needs actual field values from JS (`page.evaluate()`). In unit tests, we pass `actual_values=None` or mock values. Integration uses real browser.
   - What's unclear: Exact JS selectors for ERP fields will be determined in Phase 50.
   - Recommendation: For Phase 48, mock the JS call. The check() method signature accepts `actual_values` as a parameter, making it fully testable without a browser.

2. **TaskProgressTracker.update_from_evaluation() keyword matching quality**
   - What we know: `update_from_evaluation()` splits step text into first 3 words and checks if ANY keyword is in evaluation text. This is loose matching.
   - What's unclear: Whether loose matching causes false completions.
   - Recommendation: For Phase 48, simple keyword matching is acceptable -- the tracker is a hint, not the source of truth. Phase 49 prompt optimization may make it unnecessary.

3. **ProgressResult warning vs urgent thresholds**
   - What we know: remaining_steps < remaining_tasks * 1.5 for warning, remaining_steps <= remaining_tasks for urgent.
   - What's unclear: The boundary case (remaining_steps == remaining_tasks * 1.5, e.g., remaining_steps=6, remaining_tasks=4 -> 6 < 6 is False, so no warning).
   - Recommendation: Add explicit test for boundary case.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/unit/test_monitored_agent.py -x` |
| Full suite command | `uv run pytest backend/tests/unit/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SUB-01 | MonitoredAgent._prepare_context injects interventions after super() | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_prepare_context_injects_interventions -x` | Wave 0 |
| SUB-02 | step_callback stores interventions in _pending_interventions | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_step_callback_stores_intervention -x` | Wave 0 |
| SUB-03 | MonitoredAgent._execute_actions blocks submit on PreSubmitGuard block | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_execute_actions_blocks_submit -x` | Wave 0 |
| MON-01 | StallDetector triggers on 2 consecutive failures same target | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_stall_two_failures -x` | Wave 0 |
| MON-02 | StallDetector triggers on 3 stagnant DOM hashes | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_stagnant_dom -x` | Wave 0 |
| MON-03 | StallDetector resets on success | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_stall_reset_on_success -x` | Wave 0 |
| MON-04 | PreSubmitGuard extracts expected values from task | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_pre_submit_extracts_values -x` | Wave 0 |
| MON-05 | PreSubmitGuard blocks submit on field mismatch | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_pre_submit_blocks -x` | Wave 0 |
| MON-06 | PreSubmitGuard skips when no expectations | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_pre_submit_skips -x` | Wave 0 |
| MON-07 | TaskProgressTracker parses step formats | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_progress_parse -x` | Wave 0 |
| MON-08 | TaskProgressTracker emits urgent warning | unit | `uv run pytest backend/tests/unit/test_monitored_agent.py::test_progress_urgent -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_monitored_agent.py -x`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_monitored_agent.py` -- covers all SUB-* and MON-* requirements
- [ ] Framework install: pytest already installed via uv

## Sources

### Primary (HIGH confidence)
- browser-use Agent source code (`.venv/lib/python3.11/site-packages/browser_use/agent/service.py`) -- _prepare_context, _execute_actions, register_new_step_callback flow
- browser-use MessageManager source (`.venv/lib/python3.11/site-packages/browser_use/agent/message_manager/service.py`) -- prepare_step_state clears context_messages, _add_context_message appends to list
- CONTEXT.md decisions D-01 through D-08 -- locked implementation choices
- Implementation plan (`docs/plans/2026-03-27-agent-reliability-impl.md`) -- TDD code examples

### Secondary (MEDIUM confidence)
- Design doc (`docs/plans/2026-03-27-agent-reliability-design.md`) -- architecture and requirements
- Existing codebase (`backend/core/agent_service.py`) -- current step_callback integration pattern
- Existing codebase (`backend/agent/browser_agent.py`) -- deprecated but shows extend_system_message usage pattern

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using installed packages (browser-use, pytest, dataclasses, re)
- Architecture: HIGH - Verified by reading browser-use source code directly
- Pitfalls: HIGH - Discovered from source code analysis and design doc
- Testing: HIGH - Pure unit tests with mocks, no browser needed

**Research date:** 2026-03-27
**Valid until:** 2026-04-27 (browser-use API changes could affect subclassing)
