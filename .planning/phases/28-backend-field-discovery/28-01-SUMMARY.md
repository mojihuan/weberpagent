---
phase: 28-backend-field-discovery
plan: 01
subsystem: backend
tags: [ast, parsing, field-discovery, assertions]

# Dependency graph
requires:
  - phase: 23-backend-assertion-discovery
    provides: External assertion bridge pattern, cache structure
provides:
  - AST-based field discovery from base_assertions_field.py
  - Field grouping by naming patterns
  - Chinese description generation from camelCase names
  - Time field detection via AST and suffix matching
affects: [frontend-field-selector, assertion-execution]

# Tech tracking
tech-stack:
  added: []
  patterns: [ast.NodeVisitor, singleton-cache, regex-grouping, keyword-mapping]

key-files:
  created:
    - backend/tests/unit/test_assertions_field_parser.py
  modified:
    - backend/core/external_precondition_bridge.py

key-decisions:
  - "Use AST parsing instead of runtime import to avoid BaseApi dependency"
  - "Use naming pattern inference for field grouping instead of manual config"
  - "Use keyword mapping for Chinese description generation"

patterns-established:
  - "ParamDictVisitor: ast.NodeVisitor pattern for extracting param dictionary"
  - "GROUP_RULES: Ordered regex patterns for field group inference"
  - "KEYWORD_MAPPINGS: Dict mapping English words to Chinese descriptions"

requirements-completed: [FLD-01]

# Metrics
duration: 12min
completed: 2026-03-21
---

# Phase 28 Plan 01: AST Field Parser Summary

**AST-based parser extracts assertion fields from base_assertions_field.py with grouping and Chinese descriptions**

## Performance

- **Duration:** 12 min
- **Started:** 2026-03-21T15:00:38Z
- **Completed:** 2026-03-21T15:12:45Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- AST parser extracts all field names from param dictionary without runtime dependency
- Time field detection via get_formatted_datetime() AST call and suffix matching
- Field grouping using naming patterns (sales*, purchase*, inventory*, order*, *Time)
- Chinese description generation from camelCase using 90+ keyword mappings

## Task Commits

Each task was committed atomically:

1. **Task 1: Write unit tests for AST parser** - `047d3cb` (test)
2. **Task 2: Implement AST parser functions** - `8818366` (feat)

## Files Created/Modified
- `backend/tests/unit/test_assertions_field_parser.py` - 32 unit tests for field discovery functions
- `backend/core/external_precondition_bridge.py` - Added ParamDictVisitor, parse_assertions_field_py, get_assertion_fields_grouped

## Decisions Made
- Used AST parsing instead of runtime import to avoid heavy BaseApi dependency chain
- Used naming pattern inference for field grouping (self-maintaining as fields change)
- Used keyword mapping for description generation (simple and extensible)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - implementation followed research recommendations exactly.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Field discovery layer complete, ready for API endpoint integration (Plan 02)
- Parser tested with sample code matching actual base_assertions_field.py structure

---
*Phase: 28-backend-field-discovery*
*Completed: 2026-03-21*
