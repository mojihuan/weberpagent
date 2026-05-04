---
phase: 129-测试规划
plan: 02
subsystem: testing
tags: [test-scenarios, regression-testing, backend-unit, backend-integration, findings-analysis]

# Dependency graph
requires:
  - phase: 129-01
    provides: 67 filtered, classified, scored testable findings in 129-FINDINGS.md
  - phase: 125-backend-core-review
    provides: 32 actionable findings (backend core logic)
  - phase: 126-api
    provides: 78 actionable findings (API layer + security)
  - phase: 128-代码质量审查
    provides: 72 actionable findings (code quality + CP-1~CP-5)
provides:
  - 49 detailed backend test scenarios (24 unit + 25 integration) in 129-FINDINGS.md
  - Each scenario includes: name, severity, source finding, test descriptions, priority, mock requirements, implementation cost, testability
  - Backend Scenario Summary with counts by severity, priority, testability
  - Top 5 highest ROI scenarios identified
  - Systemic pattern (CP-1~CP-5) to test scenario cross-reference
affects: [129-03, future test implementation milestone]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Test scenario expansion: each Plan 01 finding expanded with concrete test descriptions, inputs/outputs, edge cases"
    - "Backend Scenario Summary: severity/priority/testability breakdown with ROI ranking"

key-files:
  created:
    - .planning/phases/129-测试规划/129-02-SUMMARY.md
  modified:
    - .planning/phases/129-测试规划/129-FINDINGS.md

key-decisions:
  - "P0 unit tests: StallDetector dual-invocation, assertion stub documentation, F-grade generate() validation -- highest ROI pure logic tests"
  - "P0 integration tests: EventManager lifecycle (CP-1), SSE error handling (CP-2), sync I/O blocking (CP-4), code execution path validation"
  - "2 partially deferred scenarios: EventManager auto-cleanup test (requires code fix), agent cancellation test (requires mechanism)"
  - "Systemic pattern coverage: all CP-1~CP-5 have at least one integration test scenario"
  - "49 total backend scenarios represent 73% of all 67 testable findings (some findings produce multiple test scenarios)"

patterns-established:
  - "Detailed test scenario format with 8 required fields per D-07 enables implementation without re-reading source findings"
  - "Multi-test description per scenario (4-6 test cases) provides specific inputs, expected outputs, and edge cases"

requirements-completed: [TEST-01, TEST-02]

# Metrics
duration: 6min
completed: 2026-05-04
---

# Phase 129 Plan 02: Backend Test Scenario Detail Summary

**Expanded 49 backend test scenarios (24 unit + 25 integration) from Plan 01 findings, each with concrete test descriptions, source finding references, mock requirements, and ROI scoring -- covering all 5 systemic patterns**

## Performance

- **Duration:** 6 min
- **Started:** 2026-05-04T03:57:46Z
- **Completed:** 2026-05-04T04:04:12Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Expanded all 24 backend unit testable findings into detailed test scenarios with 4-6 test cases each
- Expanded all 25 backend integration testable findings into detailed test scenarios with 3-4 test cases each
- Created Backend Scenario Summary with severity/priority/testability breakdown
- Identified Top 5 highest ROI scenarios: StallDetector (P0), F-grade generate (P0), SSE error handling (P0), EventManager lifecycle (P0), code execution path validation (P0)
- Cross-referenced all 5 systemic patterns (CP-1~CP-5) to specific test scenarios
- Documented 2 partially deferred integration tests with clear prerequisites

## Task Commits

Each task was committed atomically:

1. **Task 1: Expand backend unit test scenarios** - `ecc4b53` (docs)
2. **Task 2: Expand backend integration test scenarios** - `7bfeb7c` (docs)

**Plan metadata:** pending (final commit after STATE.md update)

## Files Created/Modified
- `.planning/phases/129-测试规划/129-FINDINGS.md` - Added "## Backend Unit Test Scenarios" (24 scenarios) and "## Backend Integration Test Scenarios" (25 scenarios + summary)

## Decisions Made
- P0 scenarios prioritized by severity x regression_risk / implementation_cost: StallDetector dual-invocation and F-grade generate() are highest ROI for unit tests; EventManager lifecycle and SSE error handling for integration tests
- 2 scenarios partially deferred: TS-BE-25 Test 2 (EventManager auto-cleanup requires _finalize_run fix), TS-BE-36 Test 4 (agent cancellation requires mechanism)
- Each scenario includes 3-6 specific test cases with concrete inputs and expected outputs, not just "test the feature"
- Systemic pattern coverage table maps each CP-1~CP-5 to both integration and unit test scenarios

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- 129-FINDINGS.md backend section is complete for Plan 03 consumption
- Plan 03 will expand frontend component tests (13 scenarios) + E2E tests (5 scenarios) + final phase summary
- 49 backend scenarios provide the core test implementation roadmap for the future test milestone
- Deferred scenarios documented with clear prerequisites for post-fix implementation

## Self-Check: PASSED

- FOUND: .planning/phases/129-测试规划/129-FINDINGS.md
- FOUND: .planning/phases/129-测试规划/129-02-SUMMARY.md
- FOUND: commit ecc4b53 (Task 1: unit scenarios)
- FOUND: commit 7bfeb7c (Task 2: integration scenarios)

---
*Phase: 129-测试规划*
*Completed: 2026-05-04*
