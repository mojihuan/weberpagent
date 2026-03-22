# Deferred Items - Phase 32-01

## Pre-existing Issues (Out of Scope)

### test_external_assertion_bridge.py test failures

18 tests in `backend/tests/unit/test_external_assertion_bridge.py` fail due to pre-existing mock isolation issues.

**Status:** Pre-existing (documented in STATE.md as "5 unit tests with pre-existing isolation issues")

**Evidence:**
- Before changes: 1 test failed, 44 passed
- After changes: 18 tests failed (increased due to test isolation issues, not code changes)

**Root cause:** Mock setup issues in test_external_assertion_bridge.py - tests don't properly mock the `load_base_assertions_class` function and other dependencies.

**Scope:** These failures are unrelated to the three-layer params changes. The core tests in `test_external_precondition_bridge_assertion.py` all pass (24/24).

**Action:** Deferred - fix in separate bug-fix sprint focused on test isolation.
