# Phase 50: AgentService 集成 - Research

**Researched:** 2026-03-28
**Domain:** AgentService integration, MonitoredAgent wiring, step_callback detector calls
**Confidence:** HIGH

## Summary

Phase 50 integrates three already-built monitoring components (StallDetector, PreSubmitGuard, TaskProgressTracker) into AgentService.run_with_streaming(). The integration involves three concrete changes to a single file (backend/core/agent_service.py): (1) replacing `Agent(...)` with `MonitoredAgent(...)` while preserving all Phase 49 parameters, (2) adding detector calls inside the existing step_callback closure, and (3) passing run_logger into MonitoredAgent for structured monitoring logs. The MonitoredAgent subclass (Phase 48) already handles _prepare_context() injection and _execute_actions() blocking automatically -- once instantiated with the detectors, those overrides work without further integration code.

The key architectural insight is that MonitoredAgent's overrides (_prepare_context and _execute_actions) are triggered by browser-use's internal lifecycle automatically. The step_callback only needs to store intervention messages in _pending_interventions; the _prepare_context override picks them up on the next step. No new methods need to be created -- only wiring in existing code.

**Primary recommendation:** Replace `Agent` with `MonitoredAgent` at line 297 of agent_service.py, pass 3 detectors via keyword arguments, add ~15 lines of detector calls at the end of the existing step_callback (before on_step), and pass run_logger to the MonitoredAgent constructor for category="monitor" logging.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 保留现有 step_callback 不变，在其中添加检测器调用。不使用 MonitoredAgent.create_step_callback()
- **D-02:** 在现有 step_callback 末尾（日志逻辑之后、on_step 回调之前），通过 `agent._stall_detector.check()` 和 `agent._task_tracker.check_progress()` 调用检测器
- **D-03:** 检测器结果存入 `agent._pending_interventions`（由 MonitoredAgent._prepare_context() 自动注入）
- **D-04:** 将 run_logger 传入 MonitoredAgent 构造，使检测器干预和拦截事件通过 run_logger.log(category="monitor") 记录
- **D-05:** 在 _prepare_context() 注入干预消息时记录，在 _execute_actions() PreSubmitGuard 拦截时记录
- **D-06:** 将 `Agent(...)` 替换为 `MonitoredAgent(...)`，保留 Phase 49 的所有参数（extend_system_message、loop_detection_window 等）
- **D-07:** 3 个检测器实例在 MonitoredAgent 创建前初始化，通过关键字参数传入

### Claude's Discretion
- 检测器调用的具体位置（step_callback 中哪个时机最优）
- run_logger 在 MonitoredAgent 中的传递方式（构造参数 vs 属性注入）
- 单元测试的具体 mock 设计

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INTEG-01 | AgentService.run_with_streaming() 使用 MonitoredAgent 替代原生 Agent | agent_service.py:297 currently creates `Agent(...)`. Replace with `MonitoredAgent(...)`. MonitoredAgent.__init__ accepts `**kwargs` and passes them to `super().__init__()`, so all existing Agent parameters (task, llm, browser_session, etc.) work unchanged. MonitoredAgent is at backend/agent/monitored_agent.py. |
| INTEG-02 | 创建 3 个检测器实例（StallDetector, PreSubmitGuard, TaskProgressTracker），传入 MonitoredAgent | Instantiate before agent creation: `stall_detector = StallDetector()`, `pre_submit_guard = PreSubmitGuard()`, `task_progress_tracker = TaskProgressTracker()`. Pass via kwargs: `MonitoredAgent(stall_detector=..., pre_submit_guard=..., task_progress_tracker=..., **other_kwargs)`. |
| INTEG-03 | step_callback 中调用 StallDetector.check() 和 TaskProgressTracker.check_progress()，结果存入 `_pending_interventions` | step_callback already extracts action_name, target_index, evaluation, dom_hash (lines 218, 228, 176). Call `agent._stall_detector.check(action_name=action_name, target_index=target_index, evaluation=evaluation, dom_hash=dom_hash)`. Call `agent._task_tracker.check_progress(current_step=step, max_steps=max_steps)`. If should_intervene/should_warn, append message to `agent._pending_interventions`. Also call `agent._task_tracker.update_from_evaluation(evaluation)`. |
| INTEG-04 | 干预消息通过结构化日志记录（category="monitor"），便于排查 | Add `run_logger` parameter to MonitoredAgent.__init__. In _prepare_context, log each injected message via `run_logger.log("info", "monitor", message, step=...)`. In _execute_actions, log PreSubmitGuard blocks via `run_logger.log("warning", "monitor", message)`. In step_callback, log detector triggers via `run_logger.log("warning", "monitor", ...)`. |
| INTEG-05 | extend_system_message 传入 ENHANCED_SYSTEM_MESSAGE | Already done in Phase 49 (agent_service.py:303). No change needed -- MonitoredAgent passes `**kwargs` to super().__init__() which includes extend_system_message. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| MonitoredAgent | local (Phase 48) | Agent subclass with monitoring | Already built and tested in Phase 48 |
| StallDetector | local (Phase 48) | Consecutive failure / stagnant DOM detection | Already built, 100% test coverage |
| PreSubmitGuard | local (Phase 48) | Submit-time field validation | Already built, 100% test coverage |
| TaskProgressTracker | local (Phase 48) | Step budget warning | Already built, 100% test coverage |
| RunLogger | local | Structured JSONL logging | Already in agent_service.py, used for browser/agent logs |
| pytest | 8.x | Test framework | Python standard testing |
| pytest-asyncio | 0.x | Async test support | Used across all existing tests |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| unittest.mock | stdlib | Mocking Agent and browser objects | All unit tests in this phase |

**Installation:**
```bash
# No new packages needed -- all dependencies already installed
uv sync
```

**Version verification:** All components are local code or stdlib. No new external dependencies.

## Architecture Patterns

### Recommended Project Structure (unchanged, showing modified file)
```
backend/core/
    agent_service.py          # MODIFIED: Replace Agent with MonitoredAgent, add detector wiring

backend/agent/
    monitored_agent.py        # MODIFIED: Add run_logger parameter + monitoring log calls
    stall_detector.py         # unchanged (Phase 48)
    pre_submit_guard.py       # unchanged (Phase 48)
    task_progress_tracker.py  # unchanged (Phase 48)
    prompts.py                # unchanged (Phase 49)

backend/tests/unit/
    test_agent_integration.py  # NEW: Integration wiring tests
```

### Pattern 1: MonitoredAgent Constructor Replacement
**What:** Replace `Agent(...)` with `MonitoredAgent(...)` at agent_service.py:297
**When to use:** This is the single point where Agent is created for streaming runs.
**Critical detail:** MonitoredAgent.__init__ uses keyword-only arguments for detectors (`stall_detector`, `pre_submit_guard`, `task_progress_tracker`), and passes `**kwargs` to `super().__init__()`. All Phase 49 parameters are preserved via kwargs.

**Before (current, line 297):**
```python
agent = Agent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
    extend_system_message=ENHANCED_SYSTEM_MESSAGE,
    loop_detection_window=10,
    max_failures=4,
    planning_replan_on_stall=2,
    enable_planning=True,
)
```

**After (Phase 50):**
```python
# Initialize detectors before agent creation
stall_detector = StallDetector()
pre_submit_guard = PreSubmitGuard()
task_progress_tracker = TaskProgressTracker()

agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
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
)
```

### Pattern 2: Detector Calls Inside Existing step_callback
**What:** Add ~15 lines of detector calls at the end of the existing step_callback, before the on_step callback (line ~282).
**When to use:** Every step already processes action_name, target_index, evaluation, dom_hash. Reuse these extracted values for detector calls.
**Critical detail (D-01/D-02):** Do NOT use MonitoredAgent.create_step_callback(). Use the existing step_callback in agent_service.py. Add detector calls at the end, before on_step.

**Insertion point (after line ~280, before on_step call):**
```python
# ===== Detector calls (Phase 50, D-02/D-03) =====
try:
    # Stall detection -- reuse already-extracted action_name, target_index, evaluation, dom_hash
    stall_result = agent._stall_detector.check(
        action_name=action_name,
        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
        evaluation=agent_output.evaluation_previous_goal if agent_output else "",
        dom_hash=dom_hash,
    )
    if stall_result.should_intervene:
        agent._pending_interventions.append(stall_result.message)
        run_logger.log("warning", "monitor", "Stall detected",
                       step=step, message=stall_result.message[:100])

    # Progress tracking
    progress_result = agent._task_tracker.check_progress(
        current_step=step,
        max_steps=max_steps,
    )
    if progress_result.should_warn:
        agent._pending_interventions.append(progress_result.message)
        run_logger.log("warning", "monitor", "Progress warning",
                       step=step, level=progress_result.level,
                       remaining_steps=progress_result.remaining_steps,
                       remaining_tasks=progress_result.remaining_tasks,
                       message=progress_result.message[:100])

    # Update completed steps from evaluation
    if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
        agent._task_tracker.update_from_evaluation(
            agent_output.evaluation_previous_goal or ""
        )
except Exception as e:
    logger.error(f"[{run_id}][MONITOR] Detector error (non-blocking): {e}")
    run_logger.log("error", "monitor", f"Detector error: {e}", step=step)
```

### Pattern 3: run_logger Integration with MonitoredAgent
**What:** Pass run_logger to MonitoredAgent so _prepare_context and _execute_actions can log monitor events.
**When to use (D-04/D-05):** MonitoredAgent needs run_logger for structured logging of intervention injection and action blocking.
**Implementation options (Claude's Discretion):**

Option A (Recommended): Add `run_logger` as an optional keyword parameter to MonitoredAgent.__init__:
```python
class MonitoredAgent(Agent):
    def __init__(self, *, ..., run_logger=None, **kwargs):
        super().__init__(**kwargs)
        self._run_logger = run_logger
        # ...existing code...

    async def _prepare_context(self, step_info=None):
        result = await super()._prepare_context(step_info)
        try:
            if self._pending_interventions:
                for msg in self._pending_interventions:
                    self._message_manager._add_context_message(UserMessage(content=msg))
                    if self._run_logger:
                        self._run_logger.log("info", "monitor", "Intervention injected",
                                             message=msg[:100])
                self._pending_interventions = []
        except Exception as e:
            logger.error("[monitor] Failed to inject interventions: %s", e)
        return result
```

### Anti-Patterns to Avoid
- **Using MonitoredAgent.create_step_callback():** CONTEXT.md D-01 explicitly forbids this. The existing step_callback in agent_service.py already has all the data extraction logic (DOM hash, action parsing, logging). Using create_step_callback() would duplicate this logic and lose the existing screenshot saving, structured logging, etc.
- **Importing MonitoredAgent from wrong path:** Must import from `backend.agent.monitored_agent`, not from `backend.core.monitored_agent` (file does not exist there).
- **Forgetting to update existing tests:** test_agent_params.py and test_agent_service.py mock `backend.core.agent_service.Agent`. After the change, these tests must mock `backend.core.agent_service.MonitoredAgent` instead. The import in agent_service.py changes from `from browser_use import Agent` to include `from backend.agent.monitored_agent import MonitoredAgent`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Agent subclass with monitoring | Custom Agent wrapper | MonitoredAgent (Phase 48) | Already built, tested, handles _prepare_context and _execute_actions overrides |
| Stall detection | Custom loop detection | StallDetector.check() | Already built with consecutive failure + stagnant DOM logic |
| Progress tracking | Custom step budget tracking | TaskProgressTracker.check_progress() | Already built with warning/urgent levels |
| Submit validation | Custom form validation | PreSubmitGuard.check() | Already built with regex extraction and field comparison |
| Message injection timing | Custom context injection | MonitoredAgent._prepare_context() | Already handles post-super() injection after browser-use clears context_messages |

**Key insight:** This phase is pure wiring. No new algorithms or detection logic. Every component already exists and is tested. The task is connecting them in agent_service.py.

## Common Pitfalls

### Pitfall 1: Mock Path Mismatch After Agent Replacement
**What goes wrong:** Existing tests mock `backend.core.agent_service.Agent`. After replacing with MonitoredAgent, the mock path changes to `backend.core.agent_service.MonitoredAgent`, and tests silently create real MonitoredAgent instances (which fail because browser-use is not properly mocked).
**Why it happens:** agent_service.py currently imports `Agent` from browser_use. After Phase 50, it imports `MonitoredAgent` from backend.agent.monitored_agent. Tests that mock `backend.core.agent_service.Agent` no longer intercept the constructor.
**How to avoid:** Update all test files that mock Agent in agent_service context:
- `backend/tests/unit/test_agent_params.py` -- change mock target from `Agent` to `MonitoredAgent`
- `backend/tests/test_agent_service.py` -- change mock target from `Agent` to `MonitoredAgent`
- `backend/tests/integration/test_agent_service.py` -- change mock target from `Agent` to `MonitoredAgent`
**Warning signs:** Tests fail with browser-use import errors or real MonitoredAgent constructor errors.

### Pitfall 2: Detector State Persisting Across Runs
**What goes wrong:** If detector instances are created once and reused across runs, stale state from a previous run causes false positives (stall warnings at step 1, progress warnings for completed tasks).
**Why it happens:** StallDetector._history accumulates records. TaskProgressTracker._completed_steps accumulates completed step indices.
**How to avoid:** Create fresh detector instances INSIDE run_with_streaming(), before MonitoredAgent creation. This is already specified in D-07 (detectors initialized before agent creation).
**Warning signs:** Intervention messages appear at step 1 of a new run.

### Pitfall 3: dom_hash Variable Scope in step_callback
**What goes wrong:** The dom_hash variable is computed inside the `if browser_state:` block (line 176) but is used in the `else` block as `dom_hash = ""` (line 202). The detector calls at the end of step_callback reference dom_hash. If browser_state is None, dom_hash is set to "" correctly, but the variable might not be defined at all if the `else` branch doesn't execute (Python scoping).
**Why it happens:** Looking at the code carefully: dom_hash is initialized as "" inside the `if browser_state:` branch (line 176) and set to "" in the `else` branch (line 202). But it's NOT initialized before the if/else. If there's a code path where neither branch executes (unlikely but possible), dom_hash would be undefined.
**How to avoid:** Initialize `dom_hash = ""` at the top of step_callback (before the browser_state check), or verify that the current code always sets it.
**Warning signs:** NameError for dom_hash in detector calls.

### Pitfall 4: target_index Extraction Mismatch
**What goes wrong:** The step_callback extracts target_index as `action_params.get('index')` (line 228), which works for click actions where params is `{"index": 5}`. But the StallDetector.check() in MonitoredAgent.create_step_callback() uses a slightly different extraction path. The integration must use the same extraction that the existing step_callback already uses.
**Why it happens:** action_params is extracted from `action_dict[action_name]` (line 221-222). For click actions, action_params = `{"index": 5, ...}`. For input actions, action_params = `{"text": "...", "index": 1, ...}`. Using `action_params.get("index")` works for both.
**How to avoid:** Use the already-extracted `action_params` dict from the step_callback, calling `.get("index")`. Do NOT re-extract from agent_output.
**Warning signs:** StallDetector never triggers because target_index is always None.

### Pitfall 5: evaluation Variable Not Defined for Detector Calls
**What goes wrong:** The evaluation text is extracted deep inside the `if agent_output:` block (line 233: `agent_output.evaluation_previous_goal`). If agent_output is None, evaluation is never set, and the detector call fails with NameError.
**Why it happens:** The existing step_callback doesn't have a standalone evaluation variable -- it uses `agent_output.evaluation_previous_goal` inline for logging.
**How to avoid:** Extract `evaluation = agent_output.evaluation_previous_goal if agent_output and hasattr(agent_output, "evaluation_previous_goal") else ""` before the detector calls. Or initialize it at the top of step_callback.
**Warning signs:** NameError for evaluation in detector calls.

## Code Examples

### Complete agent_service.py Changes (Agent Creation Section)

```python
# Source: agent_service.py, lines ~290-320 (AFTER changes)
# Note: evaluation variable needs to be available for detector calls

# ... existing code for target_url prepending ...

logger.info(f"[{run_id}] Creating MonitoredAgent: task={actual_task[:80]}..., max_steps={max_steps}")

# Initialize detectors (D-07)
stall_detector = StallDetector()
pre_submit_guard = PreSubmitGuard()
task_progress_tracker = TaskProgressTracker()

agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
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
    run_logger=run_logger,  # D-04
)
```

### Complete step_callback Detector Addition (before on_step call)

```python
# Source: agent_service.py, insert before on_step callback (around line 282)
# Variables already available: action_name, action_params, evaluation (needs extraction), dom_hash

# Extract evaluation for detector use (must be available regardless of agent_output state)
evaluation = ""
if agent_output and hasattr(agent_output, "evaluation_previous_goal"):
    evaluation = agent_output.evaluation_previous_goal or ""

# ===== Detector calls (Phase 50, INTEG-03/INTEG-04) =====
try:
    # Stall detection
    stall_result = agent._stall_detector.check(
        action_name=action_name,
        target_index=action_params.get("index") if isinstance(action_params, dict) else None,
        evaluation=evaluation,
        dom_hash=dom_hash,
    )
    if stall_result.should_intervene:
        agent._pending_interventions.append(stall_result.message)
        run_logger.log("warning", "monitor", "Stall detected",
                       step=step, message=stall_result.message[:100])

    # Progress tracking
    progress_result = agent._task_tracker.check_progress(
        current_step=step,
        max_steps=max_steps,
    )
    if progress_result.should_warn:
        agent._pending_interventions.append(progress_result.message)
        run_logger.log(progress_result.level, "monitor", "Progress warning",
                       step=step, level=progress_result.level,
                       remaining_steps=progress_result.remaining_steps,
                       remaining_tasks=progress_result.remaining_tasks)

    # Update completed steps from evaluation
    agent._task_tracker.update_from_evaluation(evaluation)

except Exception as e:
    logger.error(f"[{run_id}][MONITOR] Detector error (non-blocking): {e}")
    run_logger.log("error", "monitor", f"Detector error: {e}", step=step)
```

### MonitoredAgent run_logger Addition (monitored_agent.py changes)

```python
# Source: backend/agent/monitored_agent.py
# Changes needed to MonitoredAgent.__init__ and _prepare_context

class MonitoredAgent(Agent):
    def __init__(
        self,
        *,
        stall_detector: StallDetector | None = None,
        pre_submit_guard: PreSubmitGuard | None = None,
        task_progress_tracker: TaskProgressTracker | None = None,
        run_logger: Any = None,  # NEW: D-04
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._stall_detector = stall_detector or StallDetector()
        self._pre_submit_guard = pre_submit_guard or PreSubmitGuard()
        self._task_tracker = task_progress_tracker or TaskProgressTracker()
        self._run_logger = run_logger  # NEW
        self._pending_interventions: list[str] = []
        # ... rest of __init__ unchanged ...

    async def _prepare_context(self, step_info: Any = None) -> Any:
        result = await super()._prepare_context(step_info)
        try:
            if self._pending_interventions:
                for msg in self._pending_interventions:
                    self._message_manager._add_context_message(UserMessage(content=msg))
                    if self._run_logger:
                        self._run_logger.log("info", "monitor", "Intervention injected",
                                             message=msg[:100])
                self._pending_interventions = []
        except Exception as e:
            logger.error("[monitor] Failed to inject interventions: %s", e)
        return result

    async def _execute_actions(self) -> None:
        # ... existing code ...
        if guard_result.should_block:
            # ... existing blocking code ...
            if self._run_logger:
                self._run_logger.log("warning", "monitor", "Submit blocked",
                                     message=guard_result.message[:100])
            return
        # ... rest unchanged ...
```

### Test Mock Pattern for MonitoredAgent Integration

```python
# Source: backend/tests/unit/test_agent_integration.py (new file)
# Pattern for testing that MonitoredAgent is created with correct parameters

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

async def _invoke_run_with_streaming(mock_agent_cls):
    """Call AgentService.run_with_streaming with mocked deps, return agent kwargs."""
    from backend.core.agent_service import AgentService

    svc = AgentService(output_dir="/tmp/test_outputs")

    mock_instance = AsyncMock()
    mock_run_result = MagicMock()
    mock_run_result.is_successful.return_value = True
    mock_instance.run = AsyncMock(return_value=mock_run_result)
    mock_agent_cls.return_value = mock_instance

    async def noop_on_step(*args, **kwargs):
        pass

    with patch("backend.core.agent_service.create_llm", return_value=MagicMock()):
        with patch("backend.core.agent_service.create_browser_session", return_value=MagicMock()):
            await svc.run_with_streaming(
                task="test task",
                run_id="test-run",
                on_step=noop_on_step,
                max_steps=1,
            )

    return mock_agent_cls.call_args.kwargs


class TestMonitoredAgentIntegration:
    @pytest.mark.asyncio
    async def test_uses_monitored_agent(self):
        """AgentService creates MonitoredAgent, not Agent."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_cls:
            kwargs = await _invoke_run_with_streaming(mock_cls)

        from backend.agent.monitored_agent import MonitoredAgent
        assert mock_cls.call_args is not None

    @pytest.mark.asyncio
    async def test_detectors_passed(self):
        """MonitoredAgent receives stall_detector, pre_submit_guard, task_progress_tracker."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_cls:
            kwargs = await _invoke_run_with_streaming(mock_cls)

        assert "stall_detector" in kwargs
        assert "pre_submit_guard" in kwargs
        assert "task_progress_tracker" in kwargs

    @pytest.mark.asyncio
    async def test_run_logger_passed(self):
        """MonitoredAgent receives run_logger (D-04)."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_cls:
            kwargs = await _invoke_run_with_streaming(mock_cls)

        assert "run_logger" in kwargs

    @pytest.mark.asyncio
    async def test_preserves_phase49_params(self):
        """MonitoredAgent still receives all Phase 49 params (INTEG-05)."""
        with patch("backend.core.agent_service.MonitoredAgent") as mock_cls:
            kwargs = await _invoke_run_with_streaming(mock_cls)

        assert kwargs.get("extend_system_message") is not None
        assert kwargs.get("loop_detection_window") == 10
        assert kwargs.get("max_failures") == 4
        assert kwargs.get("planning_replan_on_stall") == 2
        assert kwargs.get("enable_planning") is True
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `Agent(...)` in agent_service.py | `MonitoredAgent(...)` with detector wiring | Phase 50 | Monitoring components activated |
| No monitor-category logs | `run_logger.log(category="monitor")` | Phase 50 | Structured audit trail for interventions |
| Step callback only logs | Step callback + detector calls + _pending_interventions | Phase 50 | Active stall/progress detection per step |

**Deprecated/outdated:**
- `backend.core.agent_service.Agent` import: Will be replaced by `MonitoredAgent` import. The `Agent` import may still be needed for `run_simple()` if it's not migrated.
- `test_agent_params.py` mock target: Must change from `Agent` to `MonitoredAgent`. This test file may need to be updated or merged with the new integration test.

## Open Questions

1. **run_simple() Migration**
   - What we know: `run_simple()` (lines 84-115) still uses `Agent(...)` directly without monitoring. CONTEXT.md scope is only `run_with_streaming()`.
   - What's unclear: Whether `run_simple()` should also be migrated.
   - Recommendation: Leave `run_simple()` unchanged per scope. It's a simpler code path, and CONTEXT.md explicitly scopes Phase 50 to `run_with_streaming()`.

2. **Existing test_agent_params.py Fate**
   - What we know: This test mocks `backend.core.agent_service.Agent` and checks parameter passing. After Phase 50, the import changes to MonitoredAgent.
   - What's unclear: Whether to update this file or create a new one.
   - Recommendation: Update test_agent_params.py to mock `MonitoredAgent` instead of `Agent`, and add new detector-related assertions to it. This is more maintainable than creating a parallel file.

3. **evaluation Variable Initialization**
   - What we know: evaluation text (`agent_output.evaluation_previous_goal`) is currently used inline in the step_callback logging section (line 233-235). It is NOT extracted into a standalone variable.
   - What's unclear: Best location to extract it -- at the top of step_callback, or just before detector calls.
   - Recommendation: Extract just before detector calls (closest to usage), with a default of "". This avoids touching existing code structure.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies identified -- all changes are code-only, using existing local modules)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/unit/test_agent_integration.py -x` |
| Full suite command | `uv run pytest backend/tests/unit/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INTEG-01 | AgentService creates MonitoredAgent, not Agent | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestMonitoredAgentIntegration::test_uses_monitored_agent -x` | Wave 0 (new file) |
| INTEG-01 | MonitoredAgent receives all Phase 49 params | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestMonitoredAgentIntegration::test_preserves_phase49_params -x` | Wave 0 (new file) |
| INTEG-02 | 3 detector instances passed to MonitoredAgent | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestMonitoredAgentIntegration::test_detectors_passed -x` | Wave 0 (new file) |
| INTEG-03 | step_callback calls StallDetector.check() and stores in _pending_interventions | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestStepCallbackDetectors::test_stall_detector_called -x` | Wave 0 (new file) |
| INTEG-03 | step_callback calls TaskProgressTracker.check_progress() and stores warnings | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestStepCallbackDetectors::test_progress_tracker_called -x` | Wave 0 (new file) |
| INTEG-04 | Detector triggers logged via run_logger.log(category="monitor") | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestMonitorLogging::test_stall_logged_as_monitor -x` | Wave 0 (new file) |
| INTEG-04 | run_logger passed to MonitoredAgent constructor | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestMonitoredAgentIntegration::test_run_logger_passed -x` | Wave 0 (new file) |
| INTEG-05 | extend_system_message=ENHANCED_SYSTEM_MESSAGE preserved | unit | `uv run pytest backend/tests/unit/test_agent_integration.py::TestMonitoredAgentIntegration::test_preserves_phase49_params -x` | Wave 0 (new file) |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_agent_integration.py -x`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_agent_integration.py` -- new file covering INTEG-01~05
- [ ] `backend/tests/unit/test_agent_params.py` -- update mock target from Agent to MonitoredAgent
- [ ] `backend/tests/test_agent_service.py` -- update mock target from Agent to MonitoredAgent
- [ ] `backend/tests/integration/test_agent_service.py` -- update mock target from Agent to MonitoredAgent

## Sources

### Primary (HIGH confidence)
- `backend/core/agent_service.py` -- full file read, Agent creation at line 297, step_callback lines 155-288
- `backend/agent/monitored_agent.py` -- full file read, MonitoredAgent class with constructor, _prepare_context, _execute_actions, create_step_callback
- `backend/agent/stall_detector.py` -- full file read, StallDetector.check() signature
- `backend/agent/pre_submit_guard.py` -- full file read, PreSubmitGuard.check() signature
- `backend/agent/task_progress_tracker.py` -- full file read, TaskProgressTracker.check_progress() and update_from_evaluation()
- `backend/agent/prompts.py` -- full file read, ENHANCED_SYSTEM_MESSAGE constant
- `backend/utils/run_logger.py` -- full file read, RunLogger.log() with category parameter
- `browser_use/agent/service.py` -- Agent.__init__ signature (lines 131-209), register_new_step_callback call (lines 1685-1697)

### Secondary (MEDIUM confidence)
- Phase 48 RESEARCH.md -- verified MonitoredAgent architecture and _prepare_context timing
- Phase 49 RESEARCH.md -- verified extend_system_message mechanism and parameter defaults

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All components are local code, already built and tested
- Architecture: HIGH - Verified by reading all source files directly, MonitoredAgent kwargs pass-through confirmed
- Pitfalls: HIGH - Identified from direct code analysis (mock paths, variable scoping, test updates)
- Testing: HIGH - Pure unit tests with mocks, established pattern from test_agent_params.py

**Research date:** 2026-03-28
**Valid until:** 2026-04-28 (stable -- no external dependency changes expected)
