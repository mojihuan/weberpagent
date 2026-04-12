---
phase: 77-testflowservice-runs-py-integration
plan: 01
subsystem: testing
tags: [regex, jinja2, login-injection, variable-substitution, tdd]

# Dependency graph
requires:
  - phase: 74-cacheservice-contextwrapper
    provides: CacheService with cache/cached/all API
  - phase: 75-accountservice-settings
    provides: AccountService with resolve() and get_login_url()
provides:
  - TestFlowService with build_login_prefix() and _build_description()
  - Two-phase variable substitution: regex {{cached:key}} then Jinja2 {{variable}}
  - Login prefix injection (5-step text block)
  - Step number shifting by +5 for injected login steps
affects: [77-02, runs.py-integration, batches.py]

# Tech tracking
tech-stack:
  added: []
  patterns: [two-phase-variable-substitution, login-prefix-injection, step-renumbering]

key-files:
  created:
    - backend/core/test_flow_service.py
    - backend/tests/unit/test_test_flow_service.py
  modified: []

key-decisions:
  - "Regex phase before Jinja2 phase — prevents StrictUndefined crash on {{cached:xxx}}"
  - "Missing cache keys produce empty string with warning log, not an error"
  - "Step renumbering uses regex replacement on 步骤N：/步骤N: patterns"

patterns-established:
  - "Two-phase substitution: regex {{cached:KEY}} first, then Jinja2 {{variable}} second — order enforced by D-06"
  - "Login prefix as pure text — 5 numbered lines appended before user steps"
  - "Graceful degradation for missing cache values — empty string + warning log"

requirements-completed: [FLOW-01, FLOW-02, CACHE-05, ACCT-04]

# Metrics
duration: 3min
completed: 2026-04-11
---

# Phase 77 Plan 01: TestFlowService Login Prefix and Variable Substitution Summary

**TestFlowService with 5-line login prefix injection and two-phase variable substitution (regex {{cached:KEY}} then Jinja2 {{variable}}), step numbers shifted by +5**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-11T16:05:41Z
- **Completed:** 2026-04-11T16:09:01Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 2

## Accomplishments
- build_login_prefix() generates 5-line login instruction text (open URL, enter account, enter password, click login, confirm success)
- _build_description() orchestrates login prefix injection, two-phase variable replacement (regex then Jinja2), and step number shifting
- All 10 unit tests passing with TDD RED-GREEN flow
- No regressions in Phase 74 (CacheService) or Phase 75 (AccountService) tests

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: TestFlowService tests** - `0aff2ea` (test)
2. **Task 1 GREEN: TestFlowService implementation** - `c9fc2a5` (feat)

_Note: TDD task with RED (failing tests) then GREEN (implementation) commits._

## Files Created/Modified
- `backend/core/test_flow_service.py` - TestFlowService class with build_login_prefix() and _build_description()
- `backend/tests/unit/test_test_flow_service.py` - 10 unit tests covering login prefix, cached variable replacement, context variable replacement, step shifting, missing keys, mixed variables

## Decisions Made
- Regex phase runs before Jinja2 phase per D-06 -- prevents StrictUndefined crash on {{cached:xxx}} patterns
- Missing cache keys replaced with empty string plus warning log per D-05 -- no KeyError raised
- UndefinedError from Jinja2 caught gracefully with warning log -- returns original text if rendering fails

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- TestFlowService ready for wiring into runs.py run_agent_background() in Plan 02
- build_login_prefix() and _build_description() APIs stable, ready for AccountService integration
- CacheService shared instance pattern documented in 77-CONTEXT.md D-07/D-08

## Self-Check: PASSED

- FOUND: backend/core/test_flow_service.py
- FOUND: backend/tests/unit/test_test_flow_service.py
- FOUND: 77-01-SUMMARY.md
- FOUND: 0aff2ea (RED commit)
- FOUND: c9fc2a5 (GREEN commit)
- 10 tests passed, 0 failed

---
*Phase: 77-testflowservice-runs-py-integration*
*Completed: 2026-04-11*
