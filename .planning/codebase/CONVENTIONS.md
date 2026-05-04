# Coding Conventions

**Analysis Date:** 2025-05-02

## Language Conventions

**Backend (Python):**
- Python 3.11+ with type annotations using `str | None` union syntax (not `Optional[str]`)
- Docstrings in English with Chinese inline comments for business context
- Ruff as linter/formatter, line length 100 (`pyproject.toml`)
- mypy configured with `warn_return_any` and `warn_unused_configs`

**Frontend (TypeScript):**
- TypeScript 5.9 with strict mode enabled
- ES2022 target, ESNext modules, bundler resolution
- `verbatimModuleSyntax: true` -- use `import type` for type-only imports
- `noUnusedLocals: true`, `noUnusedParameters: true`
- `erasableSyntaxOnly: true` (no enums, use literal unions)
- ESLint 9 flat config with typescript-eslint, react-hooks, react-refresh plugins

## Naming Patterns

**Backend Files:**
- Modules: `snake_case.py` (e.g., `agent_service.py`, `run_logger.py`)
- Directories: `snake_case` (e.g., `api/`, `core/`, `llm/`)
- Route files match resource name: `tasks.py`, `runs.py`, `batches.py`

**Backend Python:**
- Classes: `PascalCase` (e.g., `AgentService`, `TaskRepository`, `StructuredLogger`)
- Functions/methods: `snake_case` (e.g., `create_browser_session`, `_persist`)
- Private helpers: leading underscore `_` (e.g., `_build_task_dict`, `_serialize_preconditions`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `SERVER_BROWSER_ARGS`, `MAX_FILE_SIZE`)
- Type variables: single `T` (`TypeVar("T")`)

**Frontend Files:**
- Components: `PascalCase.tsx` (e.g., `TaskForm.tsx`, `StepTimeline.tsx`)
- Non-component modules: `camelCase.ts` (e.g., `reasoningParser.ts`, `retry.ts`)
- Test files: `*.spec.ts` in `e2e/tests/`
- API modules: one file per resource (e.g., `tasks.ts`, `runs.ts`, `reports.ts`)

**Frontend TypeScript:**
- Interfaces: `PascalCase` (e.g., `Task`, `RunStatus`, `SSEStepEvent`)
- Type aliases: `PascalCase` (e.g., `RunStatus`, `TimelineItem`)
- Functions: `camelCase` (e.g., `parseReasoning`, `apiClient`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `API_BASE`, `MAX_RETRIES`) or `PascalCase` for records (e.g., `ROLE_LABELS`)
- Custom hooks: `use` prefix (e.g., `useTasks`, `useRunStream`, `useReports`)

## Code Style

**Backend Formatting:**
- Tool: Ruff (configured in `pyproject.toml`)
- Line length: 100 characters
- Target: Python 3.11

**Frontend Formatting:**
- Tool: ESLint 9 flat config (`frontend/eslint.config.js`)
- Indentation: 2 spaces (standard for JS/TS)
- Quotes: single quotes
- Trailing commas: present
- Tailwind CSS 4 for styling (utility classes only, no CSS modules)

**Frontend Component Pattern:**
```tsx
// Named function export (not default)
export function ComponentName({ prop }: Props) {
  return (
    <div className="tailwind-utility-classes">
      ...
    </div>
  )
}
```

## Import Organization

**Backend Python:**
1. Standard library (`import json`, `import asyncio`, `from pathlib import Path`)
2. Third-party (`from fastapi import ...`, `from sqlalchemy import ...`)
3. Local (`from backend.db.models import ...`, `from backend.config.settings import ...`)

**Frontend TypeScript:**
1. React / third-party libraries (`import { useState } from 'react'`)
2. Types (`import type { Task } from '../types'`)
3. API modules (`import { tasksApi } from '../api/tasks'`)
4. Local components/hooks/utils

Path aliases: None configured. Use relative paths (e.g., `'../types'`, `'../../api/client'`).

## Error Handling

**Backend -- Global Exception Handlers:**

The FastAPI app in `backend/api/main.py` registers three global exception handlers:
1. `StarletteHTTPException` -- returns `{"success": false, "error": {"code": "HTTP_xxx", ...}}`
2. `RequestValidationError` -- returns `{"success": false, "error": {"code": "VALIDATION_ERROR", ...}}`
3. `Exception` (catch-all) -- returns `{"success": false, "error": {"code": "INTERNAL_ERROR", ...}}`

All error responses include a `request_id` (UUID4) for traceability. Stack traces included only at DEBUG log level.

**Backend Route-Level Error Handling:**
- Use `HTTPException(status_code=xxx, detail="...")` for expected errors
- Use `raise_not_found(entity_type, entity_id)` from `backend/api/helpers.py` for 404s
- Use `error_response(code, message)` from `backend/api/response.py` for structured errors

**Backend Non-Blocking Error Handling:**
- Use `non_blocking_execute()` from `backend/core/error_utils.py` for optional operations
- Use `silent_execute()` for cleanup/side-effects
- Monitor/detector errors log and continue (never block main flow)

**Frontend Error Handling:**
- API errors handled centrally in `frontend/src/api/client.ts` via `ApiError` class
- Network errors: automatic retry with exponential backoff (3 retries: 1s, 2s, 3s)
- Toast notifications via `sonner` for all API errors
- `console.error` used in catch blocks (13 occurrences across pages and hooks)

**Retry Pattern (Backend LLM):**
- LLM calls use `tenacity` with exponential backoff (1s, 2s, 4s), max 3 attempts
- Configured in `backend/llm/factory.py` via `@retry` decorator
- Non-retryable errors: 401, 403, auth failures, quota errors
- Function `_should_retry_llm_error()` classifies errors by pattern matching

## API Response Format

**Standard response structure** defined in `backend/api/response.py`:

```python
# Success
{"success": True, "data": ..., "meta": ...}

# Error
{"success": False, "error": {"code": "NOT_FOUND", "message": "...", "request_id": "..."}}
```

**Error codes** from `ErrorCodes` class in `backend/api/response.py`:
- `NOT_FOUND`, `VALIDATION_ERROR`, `INTERNAL_ERROR`, `BAD_REQUEST`

**Frontend API client** in `frontend/src/api/client.ts`:
- Generic `apiClient<T>(endpoint, options)` function
- Auto-parses error response and shows toast
- Returns typed data on success
- FormData uploads bypass the JSON client (see `importPreview`/`importConfirm` in `tasks.ts`)

## State Management

**Frontend State Management:**
- Server state: `@tanstack/react-query` (v5) via `QueryClientProvider` in `App.tsx`
  - `refetchOnWindowFocus: false` as default
- Local component state: `useState` hooks
- Real-time data: custom hooks with `EventSource` (SSE) for run streaming
- No Redux, Zustand, or other global state stores

**Custom Hook Pattern:**
```tsx
// frontend/src/hooks/useTasks.ts
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)
  // ...filters, pagination, selections
  const fetchTasks = useCallback(async () => { ... }, [deps])
  useEffect(() => { fetchTasks() }, [fetchTasks])
  return { tasks, loading, filters, ... }
}
```

**SSE Streaming Pattern:**
```tsx
// frontend/src/hooks/useRunStream.ts
export function useRunStream(options: UseRunStreamOptions): UseRunStreamReturn {
  // EventSource for real-time updates
  // Immutable state updates via spread: { ...prev, steps: [...prev.steps, newStep] }
}
```

**Backend State:**
- No in-memory state (stateless services)
- Database: SQLite via SQLAlchemy async (`aiosqlite`)
- Sessions: `async_sessionmaker` with `expire_on_commit=False`
- Configuration: singleton via `lru_cache` (`get_settings()`)

## Database Patterns

**ORM:** SQLAlchemy 2.0 with async sessions and declarative base

**ID Generation:** 8-char hex from UUID4 (`uuid.uuid4().hex[:8]`) via `generate_id()` in `backend/db/models.py`

**Repository Pattern:**
```python
# backend/db/repository.py
class BaseRepository:
    def __init__(self, session: AsyncSession): ...
    async def _persist(self, entity: Any) -> Any: ...  # add + commit + refresh

class TaskRepository(BaseRepository):
    async def create(self, data: TaskCreate) -> Task: ...
    async def get(self, task_id: str) -> Optional[Task]: ...
    async def list(self, status: Optional[str] = None) -> List[Task]: ...
    async def update(self, task_id: str, data: TaskUpdate) -> Optional[Task]: ...
    async def delete(self, task_id: str) -> bool: ...
```

**Dependency Injection:**
```python
# Route-level DI via FastAPI Depends
async def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)
```

**Pydantic Schemas -- three-file approach:**
1. `backend/db/models.py` -- SQLAlchemy ORM models
2. `backend/db/schemas.py` -- Pydantic v2 schemas (legacy, kept for backward compat)
3. `backend/api/schemas/index.py` -- Pydantic request/response models with validators

**JSON Field Handling:**
- ORM stores JSON as `Text` columns
- Serialization via `json.dumps(data, ensure_ascii=False)`
- Deserialization in Pydantic `@field_validator(mode='before')` or `@model_validator(mode='before')`

## Logging

**Backend Logging:**
- Python `logging` module, configured in `backend/api/main.py` lifespan
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Module-level logger pattern: `logger = logging.getLogger(__name__)`
- Structured JSONL logging via `backend/utils/logger.py` (`StructuredLogger`)
- Run-specific logging via `backend/utils/run_logger.py` (`RunLogger`)
- Prefixed log messages with `[run_id]` for traceability (e.g., `f"[{run_id}] Starting execution"`)

**Frontend Logging:**
- `console.error` in catch blocks (error-level only)
- `sonner` toast notifications for user-facing errors
- No structured logging library

## Comments and Documentation

**Backend Docstrings:**
- Module-level docstrings in Chinese (e.g., `"""任务管理路由"""`)
- Function docstrings with English Args/Returns sections
- Phase references in comments (e.g., `# Phase 59: Add sequence_number columns`)
- Decision references (e.g., `# Per D-06: HTTP endpoints in runs_routes.py`)

**Frontend Comments:**
- Block comments for E2E test suites explaining the test scenario
- Step markers in tests (e.g., `// Step 1: Navigate to tasks page`)
- No JSDoc/TSDoc usage

## Module Design

**Backend Exports:**
- `__init__.py` files with explicit `__all__` exports (see `backend/db/__init__.py`)
- Backward-compat re-exports for refactored modules (e.g., `backend/api/routes/runs.py`)
- No barrel files for route modules; each route file defines its own `router`

**Frontend Exports:**
- Component directories have `index.ts` barrel files (e.g., `components/Report/index.ts`)
- Named exports only (no default exports except `App` in `App.tsx`)

## Immutability Patterns

**Frontend State Updates:**
- Immutable state updates via spread operator:
  ```tsx
  setRun(prev => ({
    ...prev,
    steps: [...prev.steps, newStep],
    timeline: [...prev.timeline, { type: 'step' as const, data: newStep }],
  }))
  ```
- `useMemo` for computed values (filtering, sorting, pagination)
- `useCallback` for stable function references

**Backend:**
- Mixed approach: ORM entities mutated in-place via `setattr` in repository layer
- Mutable dicts used for shared state in closures (e.g., `step_stats_data`, `agent_ref`)
- Frozen dataclasses for detector results (e.g., `StallResult`, `FailureResult`)

## Validation

**Backend:**
- Pydantic v2 models with `Field()` constraints (e.g., `min_length=1, max_length=200`)
- `field_validator` and `model_validator` for complex transformations
- `Literal` types for enum-like fields (e.g., `Literal["draft", "ready"]`)
- Regex patterns via `Field(pattern="^(draft|ready|success)$")`

**Frontend:**
- No runtime validation library (no Zod, Yup, etc.)
- TypeScript types provide compile-time safety
- API responses typed via generics (`apiClient<T>`)

## Routing Convention

**Backend Routes:**
- All routes prefixed with `/api` via `app.include_router(router, prefix="/api")`
- Route files define their own sub-prefix (e.g., `APIRouter(prefix="/tasks")`)
- Full path pattern: `/api/{resource}` or `/api/{resource}/{id}`
- Tags used for OpenAPI documentation grouping

**Frontend Routes:**
- Defined in `frontend/src/App.tsx` using react-router-dom v7
- Layout route wraps all pages (sidebar + content area)
- Pages in `frontend/src/pages/` matching route segments

---

*Convention analysis: 2025-05-02*
