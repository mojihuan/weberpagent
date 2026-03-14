# Testing

**Analysis Date:** 2026-03-14

## Test Framework

**Backend:**
- Framework: pytest
- Location: `backend/tests/`
- Configuration: `pyproject.toml` (pytest settings)

**Frontend:**
- Framework: Not detected (no test files found)
- Location: Would be `frontend/src/__tests__/` or `*.test.ts(x)`

## Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_dashboard_api.py    # Dashboard API tests
├── test_delivery_form.py    # Delivery form E2E tests
└── test_purchase_e2e.py     # Purchase flow E2E tests
```

## Test Patterns

**Fixture Pattern (conftest.py):**
```python
@pytest.fixture
def client():
    """Create test client for API testing."""
    app = FastAPI()
    # Setup...
    yield TestClient(app)
    # Teardown...
```

**API Test Pattern:**
```python
def test_dashboard_stats(client):
    """Test dashboard statistics endpoint."""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
```

**E2E Test Pattern (browser-use):**
```python
async def test_delivery_form():
    """Test delivery form submission flow."""
    agent = Agent(task="Fill delivery form...", llm=llm)
    result = await agent.run()
    assert result.is_done
```

## Mocking Strategy

**LLM Mocking:**
- Mock browser-use Agent for unit tests
- Use fake responses for predictable testing

**Database Mocking:**
- Use SQLite in-memory database for tests
- Fixture-based test data isolation

**API Mocking:**
- Mock external ERP system responses
- Use TestClient for internal API testing

## Coverage

**Current Coverage:**
- Backend: Partial (API endpoints, some E2E flows)
- Frontend: Not measured (no tests)

**Coverage Command:**
```bash
uv run pytest backend/tests/ -v --cov=backend --cov-report=term-missing
```

## Test Commands

```bash
# Run all backend tests
uv run pytest backend/tests/ -v

# Run specific test file
uv run pytest backend/tests/test_dashboard_api.py -v

# Run with coverage
uv run pytest backend/tests/ --cov=backend

# Run E2E tests (requires browser)
uv run pytest backend/tests/test_purchase_e2e.py -v
```

## Test Data

**Location:** `backend/data/` (JSON files for testing)

**Fixtures:** Defined in `conftest.py`

**Test Config:** `backend/config/test_targets.yaml`

## Best Practices

1. **Isolation:** Each test should be independent
2. **Fixtures:** Use conftest.py for shared setup
3. **Mocking:** Mock external dependencies (LLM, browser)
4. **Coverage:** Aim for 80%+ coverage on new code
5. **Naming:** `test_<feature>_<scenario>_<expected_result>`

## Missing Test Coverage

- Frontend unit tests (no test files)
- Error handling paths
- Edge cases in agent execution
- SSE streaming functionality
- Report generation logic

---

*Testing analysis: 2026-03-14*
