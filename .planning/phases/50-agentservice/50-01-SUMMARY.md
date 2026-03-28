---
phase: 50-agentservice
plan: 01
subsystem: agent
tags: [browser-use, monitored-agent, stall-detector, pre-submit-guard, task-progress-tracker, run-logger]

# Dependency graph
requires:
  - phase: 48-agent
    provides: "MonitoredAgent, StallDetector, PreSubmitGuard, TaskProgressTracker classes"
  - phase: 49-prompt-optimization
    provides: "ENHANCED_SYSTEM_MESSAGE and Agent parameter tuning in agent_service.py"
provides:
  - "MonitoredAgent replaces Agent in run_with_streaming() production code path"
  - "3 detector instances (StallDetector, PreSubmitGuard, TaskProgressTracker) created per run"
  - "run_logger passed to MonitoredAgent for category='monitor' structured logging"
  - "Test mock targets updated from Agent to MonitoredAgent where appropriate"
affects: [50-02, agent-service-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [detector-per-run-instantiation, run-logger-monitor-category]

key-files:
  created: []
  modified:
    - backend/agent/monitored_agent.py
    - backend/core/agent_service.py
    - backend/tests/unit/test_agent_params.py
    - backend/tests/test_agent_service.py

key-decisions:
  - "Detector instances created fresh per run (D-07) to avoid stale state across runs"
  - "run_simple() tests kept mocking Agent since run_simple() was not changed"
  - "integration/test_agent_service.py kept mocking Agent since tests only exercise run_simple()"

patterns-established:
  - "Monitor logging via self._run_logger.log(level, 'monitor', message, **extra)"
  - "Detector instantiation before MonitoredAgent construction, passed as keyword args"

requirements-completed: [INTEG-01, INTEG-02, INTEG-05]

# Metrics
duration: 4min
completed: 2026-03-28
---

# Phase 50 Plan 01: Agent Replacement Summary

**MonitoredAgent replaces Agent in run_with_streaming() with 3 fresh detector instances per run and run_logger for structured monitor logging**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-28T08:27:40Z
- **Completed:** 2026-03-28T08:31:48Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- MonitoredAgent.__init__ now accepts run_logger parameter for structured logging
- _prepare_context() logs "Intervention injected" via run_logger when interventions are injected
- _execute_actions() logs "Submit blocked" via run_logger when PreSubmitGuard blocks a submit
- agent_service.py creates MonitoredAgent with StallDetector, PreSubmitGuard, TaskProgressTracker instances
- run_logger passed to MonitoredAgent (D-04), enabling category="monitor" structured logs
- All Phase 49 parameters preserved (extend_system_message, loop_detection_window=10, max_failures=4, planning_replan_on_stall=2, enable_planning=True)
- run_simple() untouched, still uses Agent()
- 20/20 relevant tests pass (1 pre-existing failure excluded)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add run_logger to MonitoredAgent and update test mock targets** - `a2e258d` (feat)
2. **Task 2: Replace Agent with MonitoredAgent in agent_service.py** - `e2157a1` (feat)

## Files Created/Modified
- `backend/agent/monitored_agent.py` - Added run_logger parameter and logging in _prepare_context and _execute_actions
- `backend/core/agent_service.py` - Replaced Agent with MonitoredAgent in run_with_streaming(), added detector imports and instantiation
- `backend/tests/unit/test_agent_params.py` - Updated mock target from Agent to MonitoredAgent (5 occurrences)
- `backend/tests/test_agent_service.py` - Updated mock target for test_run_with_callback only; test_run_simple_mock kept Agent

## Decisions Made
- Detector instances created fresh per run rather than shared -- prevents stale state from one run leaking into another (D-07)
- run_simple() tests (test_agent_service.py::test_run_simple_mock, integration/test_agent_service.py) kept mocking Agent since that method was not changed per plan scope
- run_logger logging uses if-guard pattern (if self._run_logger:) for zero-overhead when no logger is provided

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Reverted mock target change in run_simple() tests**
- **Found during:** Task 1 (test mock target updates)
- **Issue:** Plan specified changing ALL test files mocking `backend.core.agent_service.Agent` to `MonitoredAgent`, but test_run_simple_mock and integration tests call run_simple() which still uses Agent(), not MonitoredAgent. Patching MonitoredAgent would not intercept the actual Agent() call.
- **Fix:** Kept test_run_simple_mock and integration/test_agent_service.py mocking Agent since they test run_simple(), not run_with_streaming(). Only changed mocks in tests that exercise run_with_streaming().
- **Files modified:** backend/tests/test_agent_service.py, backend/tests/integration/test_agent_service.py
- **Verification:** 20/20 relevant tests pass
- **Committed in:** a2e258d (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Correctness fix. Plan's blanket mock change was too broad -- only tests exercising run_with_streaming() needed updating.

## Issues Encountered
- Pre-existing test failure: test_agent_service.py::test_run_with_callback missing run_id argument (out of scope, not caused by this plan)

## Next Phase Readiness
- MonitoredAgent is now wired into the production code path
- step_callback in agent_service.py has access to agent._stall_detector, agent._task_tracker, agent._pending_interventions via closure
- Plan 02 can add detector call code to the existing step_callback

---
*Phase: 50-agentservice*
*Completed: 2026-03-28*

## Self-Check: PASSED

All files exist, all commits verified, all content requirements met:
- 5/5 files found
- 2/2 task commits found (a2e258d, e2157a1)
- All required imports present in agent_service.py
- MonitoredAgent() creation with detectors + run_logger confirmed
- run_logger parameter and logging calls confirmed in monitored_agent.py
