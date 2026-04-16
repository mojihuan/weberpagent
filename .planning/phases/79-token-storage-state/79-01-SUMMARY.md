---
phase: 79-token-storage-state
plan: 01
subsystem: auth
tags: [httpx, storage_state, playwright, browser-use, jwt, localStorage]

# Dependency graph
requires:
  - phase: 75-accountservice-settings
    provides: AccountService.resolve(role) for credential resolution
  - phase: 74-cacheservice-contextwrapper
    provides: Settings singleton pattern
provides:
  - AuthService: HTTP token acquisition + storage_state construction
  - TokenFetchError: structured error with role + reason
  - create_authenticated_session(role): pre-authenticated BrowserSession factory
  - auth_service module-level singleton
affects: [80-testflow-integration, 81-batch-compat]

# Tech tracking
tech-stack:
  added: [httpx (async HTTP client)]
  patterns: [storage_state injection, auth session factory, TDD red-green]

key-files:
  created:
    - backend/core/auth_service.py
    - backend/core/auth_session_factory.py
    - backend/tests/unit/test_auth_service.py
  modified: []

key-decisions:
  - "httpx.AsyncClient with 10s timeout for ERP token fetch"
  - "storage_state dict passed directly to BrowserSession, no file I/O"
  - "TokenFetchError propagates from factory, caller handles fallback"

patterns-established:
  - "Auth service pattern: HTTP fetch + state construction + factory function"
  - "TokenFetchError with role context for structured auth error handling"

requirements-completed: [AUTH-01, AUTH-02]

# Metrics
duration: 5m
completed: 2026-04-16
---

# Phase 79 Plan 01: Token 获取与 Storage State 构造 Summary

**httpx-based ERP token fetch + Playwright storage_state with Admin-Token localStorage injection + authenticated BrowserSession factory**

## Performance

- **Duration:** 5m
- **Started:** 2026-04-16T14:41:25Z
- **Completed:** 2026-04-16T14:46:28Z
- **Tasks:** 2
- **Files modified:** 3 (created)

## Accomplishments
- AuthService.fetch_token() acquires ERP JWT via HTTP POST /auth/login with 10s timeout
- AuthService.build_storage_state() constructs Playwright storage_state dict with Admin-Token + Admin-Expires-In localStorage
- create_authenticated_session(role) factory creates pre-authenticated BrowserSession with storage_state injection
- All 11 unit tests passing covering success, timeout, HTTP errors, malformed response, and error propagation

## Task Commits

Each task was committed atomically (TDD red + green):

1. **Task 1 RED: AuthService tests** - `9991092` (test)
2. **Task 1 GREEN: AuthService implementation** - `d65517a` (feat)
3. **Task 2 RED: factory tests** - `b5747b5` (test)
4. **Task 2 GREEN: factory implementation** - `f456053` (feat)

## Files Created/Modified
- `backend/core/auth_service.py` - AuthService with fetch_token, build_storage_state, get_storage_state_for_role, TokenFetchError
- `backend/core/auth_session_factory.py` - create_authenticated_session(role) factory using auth_service singleton
- `backend/tests/unit/test_auth_service.py` - 11 unit tests (8 auth + 3 factory) with full mock coverage

## Decisions Made
- Used httpx.AsyncClient with 10s timeout for ERP token fetch (per D-08, D-09)
- storage_state dict passed directly to BrowserSession constructor, no file I/O (per D-06)
- TokenFetchError propagates from factory to caller; Phase 80 handles fallback (per D-15, D-16)
- No token caching — fresh fetch per session, matching 720s token lifetime (per D-11)
- BrowserSession receives storage_state directly in constructor, no separate BrowserProfile needed

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

Initial test assertions for timeout/missing-data cases used English substrings ("timeout", "access_token") that didn't match the Chinese error messages from implementation. Fixed by asserting on actual Chinese content ("超时", "响应格式异常"). Both test and implementation are correct; the test expectations were adjusted to match the intended behavior.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- AuthService + create_authenticated_session ready for Phase 80 integration
- Phase 80 will call create_authenticated_session(role) in run_agent_background() for tasks with login_role
- Phase 80 will catch TokenFetchError and fallback to existing create_browser_session() + 5-step text login
- create_browser_session() in agent_service.py remains untouched for zero-regression guarantee

---
*Phase: 79-token-storage-state*
*Completed: 2026-04-16*

## Self-Check: PASSED

- FOUND: backend/core/auth_service.py
- FOUND: backend/core/auth_session_factory.py
- FOUND: backend/tests/unit/test_auth_service.py
- FOUND: .planning/phases/79-token-storage-state/79-01-SUMMARY.md
- FOUND: 9991092 (test: AuthService tests RED)
- FOUND: d65517a (feat: AuthService implementation GREEN)
- FOUND: b5747b5 (test: factory tests RED)
- FOUND: f456053 (feat: factory implementation GREEN)
