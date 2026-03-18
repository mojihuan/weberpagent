# Phase 16: 端到端验证 - Research

**Researched:** 2026-03-18
**Domain:** End-to-end Integration Testing, Error Handling
**Confidence:** HIGH

## Summary

This phase validates the complete integration of the precondition system built in Phases 13-15. The validation uses backend integration tests (pytest) rather than frontend E2E tests (Playwright) as decided in CONTEXT.md. Key focus areas are:

1. **Complete Flow Testing**: Select operation codes -> Generate code -> Execute precondition -> Verify results
2. **Error Scenario Coverage**: Path not configured, path doesn't exist, module import failure, execution exceptions
3. **Manual Test Checklist**: Document steps for real environment verification with actual webseleniumerp project

**Primary recommendation:** Create integration tests in `backend/tests/integration/test_e2e_precondition_integration.py` that mock the external webseleniumerp project using tmp_path fixtures, following the existing test patterns in `test_precondition_flow.py`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Use Real Project**: Use real webseleniumerp project for testing, verify actual integration effect
- **Backend Integration Tests**: Test backend API endpoints, bridge module, execution logic, no browser dependency
- **Complete Flow Test**: Test complete flow (select operation code -> generate code -> execute precondition -> result passing), covers VAL-01

### Error Scenarios to Cover
1. **Path Not Configured**: WEBSERP_PATH not configured or empty, frontend shows prompt message
2. **Path Doesn't Exist**: WEBSERP_PATH points to non-existent directory or non-directory file
3. **Module Import Failure**: common.base_prerequisites import fails, returns HTTP 503
4. **Execution Exception**: PreFront.operations() throws exception during execution

### Validation Result Recording
- **Backend Tests**: Use pytest to write integration tests, pass/fail as validation results
- **Manual Test Checklist**: Create manual test checklist document, record test steps and expected results for real environment verification

### Claude's Discretion
- Test file naming and location
- Specific test case assertion details
- Manual test checklist format

### Deferred Ideas (OUT OF SCOPE)
None - discussion stayed within phase scope

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| VAL-01 | Complete flow test: select operation code -> execute precondition -> view results | Integration test mocking full flow via API endpoints and PreconditionService |
| VAL-02 | Error handling: external project missing, config error, execution failure | Error scenario tests covering 4 specific error cases defined in CONTEXT.md |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pytest | 8.0.0+ | Test framework | Project standard, already configured in pyproject.toml |
| pytest-asyncio | 0.24.0+ | Async test support | Required for testing async PreconditionService methods |
| fastapi.testclient.TestClient | Built-in | HTTP endpoint testing | Standard for FastAPI integration tests |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| unittest.mock.patch | Built-in | Mock external dependencies | Isolate bridge module from real webseleniumerp |
| tmp_path fixture | Built-in (pytest) | Temporary file system | Create mock webseleniumerp directory structure |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| tmp_path fixtures | Real webseleniumerp path | Real path requires external project; tmp_path provides isolation |
| Mock PreFront class | Real PreFront import | Real import requires full webseleniumerp setup; mock tests work independently |

**Installation:**
Already configured in `pyproject.toml`. No additional packages needed.

## Architecture Patterns

### Recommended Test Structure
```
backend/tests/
├── integration/
│   ├── test_precondition_flow.py       # Existing - reference pattern
│   └── test_e2e_precondition_integration.py  # NEW - Phase 16 tests
├── api/
│   └── test_external_operations.py     # Existing - API endpoint tests
└── unit/
    └── test_external_bridge.py         # Existing - bridge unit tests
```

### Pattern 1: Mock External Module with tmp_path
**What:** Create mock webseleniumerp directory structure with required files
**When to use:** Testing bridge module and PreconditionService without real external project
**Example:**
```python
# Source: Based on test_precondition_flow.py pattern
@pytest.fixture
def mock_webseleniumerp(tmp_path: Path) -> Path:
    """Create mock webseleniumerp directory with PreFront class."""
    weberp_dir = tmp_path / "webseleniumerp"
    weberp_dir.mkdir()

    # Create common/base_prerequisites.py with PreFront class
    common_dir = weberp_dir / "common"
    common_dir.mkdir()
    (common_dir / "__init__.py").write_text("")
    (common_dir / "base_prerequisites.py").write_text('''
class PreFront:
    def __init__(self):
        self.executed_operations = []

    def operations(self, codes):
        """Execute precondition operations."""
        self.executed_operations = codes
        # Simulate setting context variables
        return self
''')

    # Create config/settings.py
    config_dir = weberp_dir / "config"
    config_dir.mkdir()
    (config_dir / "settings.py").write_text('DATA_PATHS = {}')

    return weberp_dir
```

### Pattern 2: Complete Flow Integration Test
**What:** Test the entire flow from API to PreconditionService
**When to use:** Validating VAL-01 complete flow requirement
**Example:**
```python
# Source: Based on existing test patterns
@pytest.mark.asyncio
async def test_complete_flow_select_execute_verify(mock_webseleniumerp):
    """Test VAL-01: Complete flow from operation code selection to result verification."""
    # 1. Configure bridge with mock path
    from backend.core import external_precondition_bridge
    external_precondition_bridge.configure_external_path(str(mock_webseleniumerp))

    # 2. Generate precondition code (simulating frontend OperationCodeSelector)
    code = generate_precondition_code(['FA1', 'HC1'], str(mock_webseleniumerp))

    # 3. Execute via PreconditionService
    service = PreconditionService()
    success, results = await service.execute_all([code])

    # 4. Verify results
    assert success is True
    assert 'precondition_result' in service.get_context()
```

### Pattern 3: Error Scenario Test
**What:** Test error handling for each failure scenario
**When to use:** Validating VAL-02 error handling requirements
**Example:**
```python
# Source: Based on test_external_operations.py patterns
class TestErrorScenarios:
    """Tests for VAL-02 error handling scenarios."""

    def test_path_not_configured_returns_503(self, client):
        """Scenario 1: WEBSERP_PATH not configured."""
        with patch('backend.api.routes.external_operations.is_available', return_value=False):
            response = client.get("/api/external-operations")
            assert response.status_code == 503

    def test_path_not_exists_error(self, tmp_path):
        """Scenario 2: Path points to non-existent directory."""
        from backend.config.validators import validate_weberp_path
        with pytest.raises(SystemExit):
            validate_weberp_path(str(tmp_path / "nonexistent"))
```

### Anti-Patterns to Avoid
- **Don't use real webseleniumerp path in tests**: Tests must be isolated and reproducible
- **Don't skip cache reset between tests**: Bridge module uses singleton pattern; reset_cache() is required
- **Don't mock at wrong level**: Patch at route module level (e.g., `backend.api.routes.external_operations.is_available`), not bridge module level

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Mock external directory | Create files manually | tmp_path fixture | tmp_path is automatically cleaned up |
| HTTP client for tests | Custom client | TestClient(app) | Handles cookies, auth, async correctly |
| Async test execution | Manual event loop | @pytest.mark.asyncio | pytest-asyncio handles setup/teardown |

**Key insight:** The existing test infrastructure (conftest.py fixtures, pytest configuration) is sufficient. No new testing infrastructure needed.

## Common Pitfalls

### Pitfall 1: Singleton State Bleeding
**What goes wrong:** Bridge module caches PreFront class and operations; tests interfere with each other
**Why it happens:** Module-level globals in `external_precondition_bridge.py` persist across tests
**How to avoid:** Use `reset_cache()` fixture with `autouse=True` in test class
**Warning signs:** Test passes in isolation but fails when run with other tests

### Pitfall 2: Patching at Wrong Level
**What goes wrong:** Mocking `external_precondition_bridge.is_available` doesn't affect route handler
**Why it happens:** Route imports function directly; patching bridge module doesn't affect already-resolved reference
**How to avoid:** Patch at route module level: `backend.api.routes.external_operations.is_available`
**Warning signs:** Mock not applied, real function called

### Pitfall 3: Missing Mock Module Structure
**What goes wrong:** PreFront import fails even with mock path configured
**Why it happens:** Missing `__init__.py` or wrong directory structure
**How to avoid:** Follow exact webseleniumerp structure: `common/base_prerequisites.py` with `common/__init__.py`
**Warning signs:** ImportError in test output

### Pitfall 4: Execution Exception Not Propagating
**What goes wrong:** PreFront.operations() exception not caught by PreconditionService
**Why it happens:** Exception in exec() is caught but context variable still set
**How to avoid:** Check `result.success` not just context existence; verify error message
**Warning signs:** Test passes but shouldn't

## Code Examples

Verified patterns from existing test files:

### Test Fixture: Reset Bridge Cache
```python
# Source: backend/tests/api/test_external_operations.py
@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache before and after each test."""
    from backend.core import external_precondition_bridge
    external_precondition_bridge.reset_cache()
    yield
    external_precondition_bridge.reset_cache()
```

### Test: API 503 Response
```python
# Source: backend/tests/api/test_external_operations.py
def test_list_operations_returns_503_when_unavailable(client):
    """Test GET /api/external-operations returns 503 when external module unavailable."""
    with patch(
        'backend.api.routes.external_operations.is_available',
        return_value=False
    ), patch(
        'backend.api.routes.external_operations.get_unavailable_reason',
        return_value='WEBSERP_PATH not configured'
    ):
        response = client.get("/api/external-operations")
        assert response.status_code == 503
```

### Test: Mock PreFront Execution
```python
# Source: backend/tests/unit/test_precondition_service.py
@pytest.mark.asyncio
async def test_complex_precondition_code_pattern(service, tmp_path):
    """Test complete bridge-generated code pattern with mock module."""
    # Create mock PreFront-like module
    mock_module = tmp_path / "common"
    mock_module.mkdir()
    (mock_module / "__init__.py").write_text("")
    (mock_module / "base_prerequisites.py").write_text('''
class PreFront:
    def __init__(self):
        self.executed_operations = []

    def operations(self, codes):
        self.executed_operations = codes
        return self
''')

    code = f'''
import sys
sys.path.insert(0, '{tmp_path}')

from common.base_prerequisites import PreFront

pre_front = PreFront()
pre_front.operations(['FA1', 'HC1'])

context['precondition_result'] = 'success'
context['executed_ops'] = pre_front.executed_operations
'''
    result = await service.execute_single(code, 0)

    assert result.success is True, f"Error: {result.error}"
    assert result.variables.get('precondition_result') == 'success'
    assert result.variables.get('executed_ops') == ['FA1', 'HC1']
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual test execution | pytest automated tests | Phase 2 | Consistent verification |
| Mock PreFront class | tmp_path with real structure | Phase 14 | More realistic integration testing |

**Deprecated/outdated:**
- Using `erp_api_module_path` for precondition imports: Replaced by bridge module with `weberp_path`

## Open Questions

1. **Should tests require real webseleniumerp project?**
   - What we know: CONTEXT.md says "use real webseleniumerp project"
   - What's unclear: Should CI/CD tests have access to external project, or only local dev?
   - Recommendation: Create tests with mock structure (tmp_path) for CI; create manual test checklist for real project verification

2. **Manual test checklist format**
   - What we know: Need document with test steps and expected results
   - What's unclear: Markdown file location and specific format
   - Recommendation: Create `docs/manual-test-checklist.md` or add section to phase SUMMARY

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0+ with pytest-asyncio 0.24.0+ |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| VAL-01 | Complete flow: select -> execute -> result | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestCompleteFlow -v` | Wave 0 |
| VAL-02 | Error: path not configured | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestErrorScenarios::test_path_not_configured -v` | Wave 0 |
| VAL-02 | Error: path doesn't exist | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestErrorScenarios::test_path_not_exists -v` | Wave 0 |
| VAL-02 | Error: module import failure | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestErrorScenarios::test_module_import_failure -v` | Wave 0 |
| VAL-02 | Error: execution exception | integration | `uv run pytest backend/tests/integration/test_e2e_precondition_integration.py::TestErrorScenarios::test_execution_exception -v` | Wave 0 |

### Sampling Rate
- **Per task commit:** Quick run of modified test file
- **Per wave merge:** Full integration test suite
- **Phase gate:** All tests green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/integration/test_e2e_precondition_integration.py` - New file for Phase 16 tests
- [ ] Manual test checklist document - For real webseleniumerp verification

*(Existing test infrastructure in conftest.py and pytest.ini_options is sufficient)*

## Sources

### Primary (HIGH confidence)
- `backend/core/external_precondition_bridge.py` - Bridge module implementation
- `backend/core/precondition_service.py` - Precondition execution service
- `backend/api/routes/external_operations.py` - API endpoint implementation
- `backend/tests/integration/test_precondition_flow.py` - Existing test patterns

### Secondary (MEDIUM confidence)
- `backend/tests/api/test_external_operations.py` - API endpoint test patterns
- `backend/tests/unit/test_external_bridge.py` - Bridge unit test patterns
- `backend/tests/unit/test_precondition_service.py` - Service test patterns

### Tertiary (LOW confidence)
- None - All information verified from code

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All testing tools already in project
- Architecture: HIGH - Existing test patterns are well-established
- Pitfalls: HIGH - Based on actual test code patterns

**Research date:** 2026-03-18
**Valid until:** 30 days (stable testing patterns)
