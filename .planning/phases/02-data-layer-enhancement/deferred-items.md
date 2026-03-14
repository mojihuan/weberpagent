# Deferred Items

## Pre-existing Test Failures (Out of Scope)

These test failures existed before 02-03 plan execution and are not caused by current changes:

### 1. test_browser_cleanup.py::TestRunAgentBackgroundWiring
- **Error:** Module import error - `backend.core.agent_service` missing `run_agent_background`
- **Reason:** Pre-existing fixture/module configuration issue
- **Action:** Defer to service layer phase

### 2. test_api_responses.py
- **Error:** `no such table: tasks` - database not initialized for integration tests
- **Reason:** Integration test fixture issue, not related to schema changes
- **Action:** Defer to integration test infrastructure fix

### 3. test_database_concurrent.py
- **Error:** `no such table: tasks` - database not initialized
- **Reason:** Same fixture issue as test_api_responses
- **Action:** Defer to integration test infrastructure fix

## Verified Passing Tests

All Phase 2 data layer tests pass:
- `test_db_schemas.py` - 7/7 passed
- `test_screenshot_storage.py` - 7/7 passed
- `test_repository.py` - 4/4 passed
- `test_models.py` - 11/11 passed
- `test_settings.py` - 5/5 passed
