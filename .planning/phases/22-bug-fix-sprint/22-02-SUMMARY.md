---
phase: 22-bug-fix-sprint
plan: 02
subsystem: testing
tags: [pytest, archive, cleanup, legacy-tests]

# Dependency graph
requires: []
provides:
  - Clean pytest collection without import errors
  - Archived legacy test files with documentation
affects: [testing, bug-fix-sprint]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Archive legacy tests in _archived/ directory with README.md documentation"
    - "Use git mv to preserve history when moving files"

key-files:
  created:
    - backend/tests/_archived/README.md
    - backend/tests/_archived/conftest.py
  modified: []
  moved:
    - backend/tests/test_agent.py → backend/tests/_archived/
    - backend/tests/test_agent_optimized.py → backend/tests/_archived/
    - backend/tests/test_code_generator.py → backend/tests/_archived/
    - backend/tests/test_code_optimizer.py → backend/tests/_archived/
    - backend/tests/test_code_reviewer.py → backend/tests/_archived/
    - backend/tests/test_dashboard_api.py → backend/tests/_archived/
    - backend/tests/test_decision.py → backend/tests/_archived/
    - backend/tests/test_delivery_form.py → backend/tests/_archived/
    - backend/tests/test_executor.py → backend/tests/_archived/
    - backend/tests/test_form_filler_integration.py → backend/tests/_archived/
    - backend/tests/test_login_e2e.py → backend/tests/_archived/
    - backend/tests/test_memory.py → backend/tests/_archived/
    - backend/tests/test_memory_integration.py → backend/tests/_archived/
    - backend/tests/test_orchestrator.py → backend/tests/_archived/
    - backend/tests/test_perception.py → backend/tests/_archived/
    - backend/tests/test_phase5_unit.py → backend/tests/_archived/
    - backend/tests/test_purchase_e2e.py → backend/tests/_archived/
    - backend/tests/test_sandbox.py → backend/tests/_archived/

---

# Plan 22-02: Archive Legacy Test Files

## Summary

Successfully archived 18 legacy test files that imported deleted modules, eliminating import errors during pytest collection.

## Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| 1 | Create archive directory and move legacy test files | ✓ Complete |
| 2 | Create README.md documenting archival reason | ✓ Complete |
| 3 | Verify pytest collection works without import errors | ✓ Complete |

## Key Accomplishments

- Moved 18 legacy test files to `backend/tests/_archived/`
- Created comprehensive README.md documenting each file's archival reason
- Added conftest.py to archived directory for test isolation
- Verified pytest collection no longer fails with ModuleNotFoundError

## Files Modified

- `backend/tests/_archived/` - New directory containing 18 archived test files
- `backend/tests/_archived/README.md` - Documentation explaining archival reasons
- `backend/tests/_archived/conftest.py` - Test configuration for archived tests

## Commits

- `4592a1d` - chore(22-02): archive 18 legacy test files
- `e61c691` - docs(22-02): add README documenting archived test files

## Verification

```bash
# Verify no import errors during collection
uv run pytest --collect-only backend/tests/ 2>&1 | grep -c "ModuleNotFoundError"
# Output: 0 (no errors)
```

## Notes

- Git history preserved via `git mv` command
- Files can be restored by updating imports to current module structure
- Archived tests reference deleted modules like `backend.agent_simple`, `backend.agent_simple.decision`, etc.
