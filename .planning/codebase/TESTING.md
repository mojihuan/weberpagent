# Testing Patterns

**Analysis Date:** 2025-05-02

## Test Framework

**Backend:**
- Framework: pytest 8.0.0+ (in `pyproject.toml` dependencies)
- Async: pytest-asyncio 0.24.0+
- Playwright integration: pytest-playwright 0.7.0+
- Timeout: pytest-timeout 2.4.0+ (in dev dependency group)
- Reports: pytest-html 4.0.0+ (in dev dependency group)
- No `pytest.ini`, `conftest.py`, or `pyproject.toml` pytest section found -- uses defaults
- No dedicated `backend/tests/` directory currently exists in the codebase

**Frontend (E2E):**
- Framework: Playwright (`@playwright/test` ^1.51.1)
- Config: `e2e/playwright.config.ts`
- Runner: `npm run test:e2e` (from project root `package.json`)

**Frontend (Unit):**
- Not present -- no unit test framework configured
- No vitest, jest, or testing-library setup

**Assertion Library:**
- Backend: pytest built-in assertions (`assert x == y`)
- E2E: Playwright `expect` assertions

## Run Commands

```bash
# Backend tests (pytest)
uv run pytest backend/tests/ -v           # Run all (directory does not currently exist)
uv run pytest backend/tests/test_foo.py   # Run specific file

# E2E tests (Playwright)
npm run test:e2e                          # Run all E2E tests
npm run test:e2e:ui                       # Run with Playwright UI
npm run test:e2e:report                   # View HTML report

# Frontend
cd frontend && npm run lint               # ESLint only (no test runner)
```

## Test File Organization

**Backend:**
- No `backend/tests/` directory or test files currently exist in the codebase
- One test file at `backend/core/test_flow_service.py` (likely a misnamed module, not an actual test)
- `pyproject.toml` lists `pytest`, `pytest-asyncio`, `pytest-playwright` as dependencies
- No `conftest.py` in the project root or `backend/` directory

**E2E Tests:**
```
e2e/
├── playwright.config.ts          # Playwright configuration
└── tests/
    ├── smoke.spec.ts             # Basic smoke test (create->execute->monitor->report)
    ├── task-flow.spec.ts         # Task listing, execution monitor, screenshots, reports
    ├── assertion-flow.spec.ts    # Assertion configuration and execution flow (7 tests)
    ├── variable-substitution.spec.ts  # Variable {{variable}} replacement (4 tests)
    ├── data-method-selector.spec.ts   # DataMethodSelector 4-step wizard
    ├── data-method-execution.spec.ts  # Data method execution and response handling
    └── full-flow.spec.ts         # Complete end-to-end with data method + variable substitution
```

## E2E Test Configuration

**Playwright Config** (`e2e/playwright.config.ts`):
```typescript
{
  testDir: './tests',
  fullyParallel: false,           // Sequential execution
  workers: 1,                     // Single worker for consistency
  timeout: 120000,                // 2 minutes per test
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:11001',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    { command: 'uv run uvicorn backend.api.main:app --port 11002', url: 'http://localhost:11002' },
    { command: 'cd frontend && npm run dev', url: 'http://localhost:11001' },
  ],
}
```

## E2E Test Structure

**Suite Organization:**
```typescript
// Pattern from all spec files:
import { test, expect } from '@playwright/test'

test.describe('Feature Name Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/tasks')
    await expect(page.locator('table')).toBeVisible({ timeout: 10000 })
  })

  test('test description - what this verifies', async ({ page }) => {
    test.setTimeout(180000) // Override for AI-driven operations
    // ... test steps with numbered comments
  })
})
```

**Timeout Strategy:**
- Default: 120s (2 min) per test
- AI-execution tests: 180s (3 min) or 300s (5 min) via `test.setTimeout()`
- Modal-only tests: 60s (1 min)
- All timeouts account for slow AI-driven browser interactions

**Conditional Skip Pattern:**
```typescript
// Skip if external service not configured
test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')

// Skip if no data available
const firstCheckbox = page.locator('input[type="checkbox"]').first()
if ((await firstCheckbox.count()) === 0) {
  test.skip()
  return
}
```

**Bilingual Locator Pattern:**
Tests use both Chinese and English text for UI elements:
```typescript
await page.click('button:has-text("新建任务"), button:has-text("New Task")')
await page.waitForSelector('text=已完成, text=失败, text=completed, text=failed')
```

## Test Coverage

**Backend Unit/Integration Tests:**
- Not present -- `backend/tests/` directory does not exist
- pytest dependencies listed in `pyproject.toml` but no test files found
- Coverage: 0% for backend code

**Frontend Unit Tests:**
- Not present -- no test framework configured
- Coverage: 0% for frontend code

**E2E Tests:**
- 7 spec files covering major user flows
- Tests are conditional (skip when external dependencies unavailable)
- Coverage: functional flows only, no edge case testing

**Coverage Gap Summary:**
| Area | Unit | Integration | E2E |
|------|------|-------------|-----|
| Backend API routes | None | None | Covered |
| Backend services | None | None | Covered |
| Backend DB/repository | None | None | None |
| Backend agent/detectors | None | None | None |
| Frontend components | None | None | Covered |
| Frontend hooks | None | None | Covered |
| Frontend utils | None | None | None |

## Mocking

**Backend Mocking (defined but unused):**
No test files exist to demonstrate mocking patterns. The following pattern is expected based on project conventions:
```python
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.invoke = MagicMock(return_value=MagicMock(content="click(index=1)"))
    return llm

@pytest.mark.asyncio
async def test_service_with_mock(mock_llm):
    result = await service.execute(llm=mock_llm)
    assert result is not None
```

**E2E Mocking:**
- No mocking in E2E tests -- tests run against real backend and browser
- Environment variable `ERP_BASE_URL` controls whether external-dependent tests run
- `test.skip()` used when external services unavailable

**What to Mock (when adding backend tests):**
- LLM calls (expensive, non-deterministic)
- Browser session / Agent
- External module discovery
- File system operations

**What NOT to Mock:**
- Database operations (use in-memory SQLite)
- Pydantic validation (test directly)
- JSON serialization/deserialization

## Fixtures and Factories

**No test fixtures currently exist.** When adding tests, expected patterns:

```python
# conftest.py (to be created)
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest.fixture
def task_repo(db_session):
    return TaskRepository(db_session)
```

## E2E Test Anti-Patterns Observed

**Flexible Assertions:**
Many E2E tests use conditional checks instead of hard assertions:
```typescript
// Common pattern: check and proceed even if missing
const assertionSection = page.locator('text=断言结果')
if ((await assertionSection.count()) > 0) {
    await expect(assertionSection).toBeVisible()
}
// Test passes regardless -- not a true assertion
```

**Long Waits:**
```typescript
await page.waitForTimeout(2000)  // Hard-coded waits for data loading
```

**Catch-all Error Handling:**
```typescript
await page.click('button:has-text("Cancel")').catch(() => {})
```

## Test Environment Setup

**Backend Server (for E2E):**
- Started by Playwright `webServer` config
- Command: `uv run uvicorn backend.api.main:app --port 11002`
- Uses real `.env` file for configuration
- SQLite database at `backend/data/database.db`

**Frontend Dev Server (for E2E):**
- Started by Playwright `webServer` config
- Command: `cd frontend && npm run dev`
- Proxies `/api` to backend via Vite config

**Environment Variables (for E2E):**
- `ERP_BASE_URL` -- required for assertion-flow tests (skipped if not set)
- `VITE_API_BASE` -- optional, defaults to `http://localhost:11002/api`
- `VITE_API_PROXY_TARGET` -- optional proxy target for frontend dev server

## Recommended Test Additions

**Backend Unit Tests (Priority: High):**
- `backend/tests/test_repository.py` -- CRUD operations with in-memory SQLite
- `backend/tests/test_schemas.py` -- Pydantic validation and serialization
- `backend/tests/test_error_utils.py` -- Error handling utilities
- `backend/tests/test_excel_parser.py` -- Excel import/export

**Backend Integration Tests (Priority: Medium):**
- `backend/tests/test_api_tasks.py` -- Task CRUD API endpoints
- `backend/tests/test_api_runs.py` -- Run execution API
- `backend/tests/test_precondition_service.py` -- Precondition execution

**Frontend Unit Tests (Priority: Medium):**
- `frontend/src/utils/__tests__/reasoningParser.test.ts`
- `frontend/src/utils/__tests__/retry.test.ts`
- Component smoke tests for key UI components

---

*Testing analysis: 2025-05-02*
