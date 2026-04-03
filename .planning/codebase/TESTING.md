# Testing Patterns

**Analysis Date:** 2026-04-03

## Test Framework

**Backend:**
- Framework: pytest 8.0.0+
- Location: `backend/tests/`
- Config: `pyproject.toml` pytest section
- Async: pytest-asyncio 0.24.0+

**Frontend:**
- Framework: Playwright (E2E only)
- Location: `e2e/`
- No unit tests currently

## Test File Organization

**Backend:**
```
backend/tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_*.py            # Unit/integration tests
```

**E2E:**
```
e2e/
├── *.spec.ts            # Playwright E2E tests
```

## Test Structure

**Fixture Pattern (conftest.py):**
```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def db_session():
    """Create async database session for tests."""
    # Setup
    session = AsyncSession(bind=engine)
    yield session
    await session.rollback()
```

**Service Test Pattern:**
```python
class TestAgentService:
    @pytest.fixture
    def agent_service(self):
        return AgentService(output_dir="outputs")

    @pytest.mark.asyncio
    async def test_run_simple(self, agent_service):
        result = await agent_service.run_simple(
            task="Open example.com",
            max_steps=3,
        )
        assert result is not None
```

## Mocking

**LLM Mocking:**
```python
from unittest.mock import MagicMock

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.invoke = MagicMock(return_value=MagicMock(content="click(index=1)"))
    return llm
```

**Detector Mocking:**
```python
@pytest.fixture
def mock_stall_detector():
    from backend.agent.stall_detector import StallDetector, StallResult

    detector = StallDetector()
    # Override check to return non-intervention
    detector.check = MagicMock(
        return_value=StallResult(should_intervene=False, message="")
    )
    return detector
```

## Test Commands

```bash
# Run all backend tests
uv run pytest backend/tests/ -v

# Run with coverage
uv run pytest backend/tests/ --cov=backend --cov-report=term

# Run specific test file
uv run pytest backend/tests/test_dashboard_api.py -v

# Run E2E tests
cd e2e && npx playwright test

# Run E2E with UI
cd e2e && npx playwright test --ui
```

## Coverage

**Current:**
- Backend: Partial (API endpoints covered)
- Frontend: No unit tests

**Target:** 80%+ for new code

## Test Types

**Unit Tests:**
- Services (AgentService, PreconditionService)
- Detectors (StallDetector, PreSubmitGuard)
- Utilities (RunLogger, ContextWrapper)

**Integration Tests:**
- API endpoints (tasks, runs, reports)
- Database operations
- SSE streaming

**E2E Tests:**
- Critical user flows (login, task creation, execution)
- Playwright with browser automation

## Common Patterns

**Async Testing:**
```python
@pytest.mark.asyncio
async def test_async_service():
    result = await service.execute()
    assert result.success is True
```

**Error Testing:**
```python
def test_precondition_syntax_error():
    result = asyncio.run(
        service.execute_single(code="invalid syntax !!", index=0)
    )
    assert result.success is False
    assert "SyntaxError" in result.error
```

## Missing Test Coverage

**Critical Gaps:**
- MonitoredAgent detector integration tests
- SSE event streaming tests
- PreconditionService variable substitution tests
- Report generation service tests
- Frontend component tests

**Recommended additions:**
- `backend/tests/test_detectors.py` - Detector unit tests
- `backend/tests/test_sse.py` - SSE streaming tests
- `backend/tests/test_preconditions.py` - Precondition service tests

---

*Testing analysis: 2026-04-03*
