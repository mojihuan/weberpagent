---
phase: 03-service-layer-restoration
plan: "04"
subsystem: [sse, llm, retry]
tags: [sse, heartbeat, llm, retry, tenacity, exponential-backoff]

# Dependency graph
requires:
  - phase: 02-data-layer-enhancement
provides:
  - SSE heartbeat for long-running connections
  - LLM retry logic with exponential backoff
affects:
  - frontend-sse-connections
  - llm-service-calls

# Tech tracking
tech-stack:
  added: [tenacity]
  patterns: [asyncio-background-tasks, sse-comments, exponential-backoff]

key-files:
  created:
    - backend/tests/unit/test_event_manager.py
    - backend/tests/unit/test_llm_retry.py
  modified:
    - backend/core/event_manager.py
    - backend/llm/factory.py

key-decisions:
  - "SSE heartbeat uses comment format (:heartbeat) invisible to EventSource clients"
  - "Heartbeat interval: 20 seconds (configurable via heartbeat_interval parameter)"
  - "LLM retry: exponential backoff (1s, 2s, 4s) with max 3 attempts"
  - "Non-retryable errors: 401, 403, invalid API key, quota exceeded"

patterns-established:
  - "Async generator with finally cleanup for heartbeat task cancellation"
  - "Tenacity @retry decorator with retry_if_exception_type for selective retry"

requirements-completed: [SVC-04]

# Metrics
duration: 8 min
completed: "2026-03-14T10:35:00Z"
---

# Phase 3 Plan 4: SSE Heartbeat and LLM Retry Summary

Added SSE heartbeat support to EventManager and LLM retry logic with exponential backoff to factory.

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-14T10:27:00Z
- **Completed:** 2026-03-14T10:35:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- SSE connections now receive heartbeat comments every 20 seconds to prevent timeout during long executions
- LLM calls automatically retry on transient errors (timeout, connection, rate limit) with exponential backoff
- Non-retryable errors (auth, quota, invalid key) fail immediately without wasted retry attempts

## Task Commits

Each task was committed atomically:

1. **Task 1: Add SSE heartbeat to EventManager** - `9eb903f` (test), `d0fdba7` (feat)
2. **Task 2: Add LLM retry logic to factory** - `7e0613b` (test), `adeb8d5` (feat)

## Files Created/Modified

- `backend/core/event_manager.py` - Added heartbeat_interval parameter, _send_heartbeat method, heartbeat task management
- `backend/llm/factory.py` - Added tenacity retry decorator, _should_retry_llm_error helper, RETRYABLE_ERRORS constant
- `backend/tests/unit/test_event_manager.py` - Created with 9 tests covering heartbeat functionality
- `backend/tests/unit/test_llm_retry.py` - Created with 18 tests covering retry logic

## Decisions Made

- SSE heartbeat uses comment format (`:heartbeat\n\n`) which is invisible to EventSource clients
- Heartbeat interval defaults to 20 seconds, configurable via constructor parameter
- LLM retry uses exponential backoff (1s, 2s, 4s) with maximum 3 attempts
- Non-retryable error patterns: 401, 403, unauthorized, invalid api key, quota, insufficient
- Retryable error patterns: 429, 503, timeout, rate limit, connection, connect

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed test for heartbeat task cancellation**
- **Found during:** Task 1 (GREEN phase)
- **Issue:** Test `test_heartbeat_task_cancelled_on_unsubscribe` failed because async generator's finally block doesn't run when breaking from the loop
- **Fix:** Changed test to use explicit `aclose()` on the generator to ensure cleanup runs
- **Files modified:** backend/tests/unit/test_event_manager.py
- **Verification:** All 9 tests pass
- **Committed in:** d0fdba7 (Task 1 commit)

**2. [Rule 1 - Bug] Fixed mock path for BrowserUseChatOpenAI**
- **Found during:** Task 2 (GREEN phase)
- **Issue:** Tests failed because `BrowserUseChatOpenAI` is imported inside the function, not at module level
- **Fix:** Changed mock path from `backend.llm.factory.BrowserUseChatOpenAI` to `browser_use.llm.openai.chat.ChatOpenAI`
- **Files modified:** backend/tests/unit/test_llm_retry.py
- **Verification:** All 18 tests pass
- **Committed in:** adeb8d5 (Task 2 commit)

**3. [Rule 1 - Bug] Added "connect" to retryable error patterns**
- **Found during:** Task 2 (GREEN phase)
- **Issue:** ConnectionError("Failed to connect") was not recognized as retryable because message didn't contain "connection"
- **Fix:** Added "connect" to the retryable patterns list
- **Files modified:** backend/llm/factory.py
- **Verification:** test_retry_on_connection_error passes
- **Committed in:** adeb8d5 (Task 2 commit)

---

**Total deviations:** 3 auto-fixed (all bugs)
**Impact on plan:** Minor test and implementation adjustments. All fixes necessary for correctness.

## Issues Encountered

None - TDD approach caught issues early in RED phase.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- SSE heartbeat and LLM retry ready for integration testing
- Service layer restoration progressing as planned

## Self-Check: PASSED

- All 4 key files exist
- All 4 commits found in git history

---
*Phase: 03-service-layer-restoration*
*Completed: 2026-03-14*
