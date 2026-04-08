---
phase: 70-excel
plan: 02
subsystem: api
tags: [openpyxl, excel, parser, type-coercion, error-collection, collect-all]

# Dependency graph
requires:
  - phase: 70-01
    provides: TEMPLATE_COLUMNS shared column contract, generate_template() for round-trip testing
provides:
  - "ParsedRow frozen dataclass (row_number, data dict, errors list)"
  - "ParseResult frozen dataclass (rows, total_rows, has_errors)"
  - "parse_excel(BytesIO) -> ParseResult with collect-all error handling"
  - "Type coercion helpers: _coerce_string, _coerce_int, _coerce_json_list"
  - "33 unit tests covering all edge cases including template round-trip"
affects: [71-excel-import]

# Tech tracking
tech-stack:
  added: []
  patterns: [collect-all error strategy, frozen dataclass result types, lenient type coercion, header validation on load]

key-files:
  created:
    - backend/utils/excel_parser.py
    - backend/tests/unit/test_excel_parser.py
  modified: []

key-decisions:
  - "Empty row detection uses cell.value is None check (not empty string) because data_only=True normalizes empty strings to None"
  - "Required field validation checks data dict values after coercion, not raw cell values"
  - "JSON parse errors store raw string in data[field] so UI can display what user typed"
  - "Header mismatch returns ParseResult with row_number=0 as sentinel for non-row errors"
  - "Merged cell check uses isinstance(cell, MergedCell) from openpyxl"

patterns-established:
  - "Collect-all error pattern: all row errors collected, never raise on individual rows"
  - "Lenient coercion: numbers to strings, floats to ints, empty to defaults"
  - "Template round-trip test as integration validation"

requirements-completed: [TMPL-01, TMPL-02]

# Metrics
duration: 6min
completed: 2026-04-08
---

# Phase 70 Plan 02: Excel Parser Summary

**ExcelParser with collect-all error strategy, lenient type coercion (_coerce_string/_coerce_int/_coerce_json_list), ParsedRow/ParseResult frozen dataclasses, and template round-trip validation**

## Performance

- **Duration:** 6 min
- **Started:** 2026-04-08T05:03:39Z
- **Completed:** 2026-04-08T05:10:27Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Implemented parse_excel() with full type coercion for all 6 TEMPLATE_COLUMNS types
- Collect-all error strategy: multiple errors per row and across rows, all preserved
- 33 unit tests covering type coercion, JSON parsing, empty rows, merged cells, required fields, header validation, and round-trip
- Template round-trip verified: generate_template() -> parse_excel() produces 2 rows with zero errors

## Task Commits

Each task was committed atomically:

1. **Task 1: Create ExcelParser with type coercion and error collection** - `63956b4` (test: RED) + `0c5fc08` (feat: GREEN)
2. **Task 2: Comprehensive parser unit tests including round-trip** - `41db518` (test)

_Note: Task 1 followed TDD workflow -- RED commit (failing tests + stub) then GREEN commit (implementation)._

## Files Created/Modified
- `backend/utils/excel_parser.py` - Parser with ParsedRow, ParseResult, parse_excel, type coercion helpers (180 lines)
- `backend/tests/unit/test_excel_parser.py` - 33 unit tests in 9 test classes (250 lines)

## Decisions Made
- Empty row detection based on `cell.value is None` check per openpyxl data_only=True behavior (empty strings normalized to None)
- JSON parse errors store raw string in data dict so Phase 71 preview UI can display original input
- Header validation returns early with row_number=0 sentinel for non-row-level errors
- MergedCell detection uses isinstance check on cell objects from iter_rows

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed wrong variable name in _validate_headers**
- **Found during:** Task 1 (TDD GREEN phase)
- **Issue:** Referenced undefined `expected_columns` instead of `expected_headers`
- **Fix:** Changed to correct variable name `expected_headers`
- **Files modified:** backend/utils/excel_parser.py
- **Verification:** All 16 tests pass after fix
- **Committed in:** 0c5fc08 (part of Task 1 GREEN commit)

**2. [Rule 1 - Bug] Fixed empty row detection to account for data_only=True behavior**
- **Found during:** Task 1 (TDD GREEN phase)
- **Issue:** openpyxl with data_only=True normalizes empty strings to None, making rows with explicit empty strings appear as completely empty
- **Fix:** Changed _is_empty_row to check `cell.value is not None` (not `str(val).strip() != ""`) -- rows are empty only when ALL cells have None value
- **Files modified:** backend/utils/excel_parser.py
- **Verification:** All tests pass
- **Committed in:** 0c5fc08 (part of Task 1 GREEN commit)

**3. [Rule 1 - Bug] Fixed test assertions for required field errors**
- **Found during:** Task 1 (TDD GREEN phase)
- **Issue:** Tests for missing required fields used empty strings `["", "", ...]` which become None under data_only=True, causing rows to be skipped entirely
- **Fix:** Changed test data to use rows with a non-None value (target_url) so the row is parsed, then required field validation catches the missing name/description
- **Files modified:** backend/tests/unit/test_excel_parser.py
- **Verification:** All 16 tests pass
- **Committed in:** 0c5fc08 (part of Task 1 GREEN commit)

---

**Total deviations:** 3 auto-fixed (all Rule 1 bugs, all related to openpyxl data_only=True behavior)
**Impact on plan:** All auto-fixes necessary for correctness. No scope creep. The core openpyxl data_only=True quirk was the root cause of all three fixes.

## Issues Encountered
- openpyxl's data_only=True mode normalizes empty strings to None, which required careful handling in both the parser and test expectations

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- ExcelParser ready for Phase 71 file upload/import workflow
- parse_excel() returns structured data that can be directly validated against TaskCreate schema
- Error messages are user-friendly Chinese strings for preview UI display
- Raw JSON strings preserved on parse errors for UI to show original user input

## Self-Check: PASSED

All files verified present: excel_parser.py, test_excel_parser.py, 70-02-SUMMARY.md
All commits verified: 63956b4, 0c5fc08, 41db518

---
*Phase: 70-excel*
*Completed: 2026-04-08*
