# Phase 1: Foundation Fixes - Research

**Researched:** 2026-03-14
**Domain:** Python/FastAPI Infrastructure - Configuration, API Response Format, Async Database, LLM Determinism, Browser Cleanup
**Confidence:** HIGH

## Summary

Phase 1 focuses on establishing a stable technical foundation for the aiDriveUITest platform. The research covers five critical areas: centralized configuration management, consistent API response format, async database patterns, LLM deterministic configuration, and browser resource cleanup.

**Primary recommendation:** Implement these fixes systematically using established FastAPI/SQLAlchemy patterns before building new features. Each fix is isolated and testable independently.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Environment Configuration**: Single `.env` file with `KEY=VALUE` format. Backend uses `DASHSCOPE_API_KEY`, `OPENAI_API_KEY`, `ERP_BASE_URL`, `ERP_USERNAME`, `ERP_PASSWORD`. Frontend uses `VITE_API_BASE`. `.env.example` provides template. Local development can use defaults without `.env`.
- **API Response Format**:
  - Success: `{success: true, data: T, meta?: {page: number, total: number}}`
  - Error: `{success: false, error: {code: "ERROR_CODE", message: "...", request_id: "UUID", stack?: "..."}}` with HTTP status codes (400, 404, 500)
- **Async Database**: aiosqlite async engine with 5-connection pool, per-request sessions
- **LLM Determinism**: temperature=0, no caching, exponential backoff retry (max 3 times)
- **Browser Cleanup**: try/finally pattern with error logging

### Claude's Discretion
- Implementation details for each fix
- Exact code structure and file organization
- Test coverage approach

### Deferred Ideas (OUT OF SCOPE)
None - discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| FND-01 | Environment configuration is centralized (no hardcoded URLs/API keys) | Section: Environment Configuration |
| FND-02 | API responses use consistent format (success, data, error, meta) | Section: API Response Format |
| FND-03 | All async database operations use async engine (no blocking) | Section: Async Database Patterns |
| FND-04 | LLM temperature is set to 0 for deterministic test execution | Section: LLM Deterministic Configuration |
| FND-05 | Browser cleanup uses try/finally pattern (no memory leaks) | Section: Browser Cleanup Pattern |
</phase_requirements>

## Current State Analysis

### FND-01: Environment Configuration

**Current Issues:**
- `frontend/src/api/client.ts` has hardcoded `API_BASE = 'http://localhost:8080/api'`
- `backend/llm/factory.py` uses `temperature=0.1` as default instead of 0
- `backend/api/routes/runs.py` has `get_llm_config()` with inline `os.getenv()` calls and hardcoded default URL
- No centralized configuration module in `backend/config/` (currently empty `__init__.py`)

**Existing Assets:**
- `.env.example` already exists with proper structure
- `backend/llm/config.py` has sophisticated YAML-based LLM config (but overkill for this phase)
- Environment variables are already used in some places

### FND-02: API Response Format

**Current Issues:**
- Routes return Pydantic models directly without wrapper
- Error responses use `HTTPException` with `detail` field (not structured error format)
- No `request_id` for debugging
- No consistent `success` field in responses

**Existing Assets:**
- `backend/db/schemas.py` has response models but no wrapper
- FastAPI exception handling infrastructure is in place

### FND-03: Async Database

**Current Issues:**
- `backend/db/database.py` uses `create_async_engine(DATABASE_URL, echo=False)` with no pool configuration
- Uses default pool settings instead of explicit 5 connections
- No explicit connection pool validation

**Existing Assets:**
- Already using aiosqlite with SQLAlchemy async
- `async_sessionmaker` and `get_db()` dependency injection work correctly

### FND-04: LLM Determinism

**Current Issues:**
- `backend/llm/factory.py:create_llm()` uses `temperature=0.1` default
- `backend/api/routes/runs.py:get_llm_config()` uses `temperature=float(os.getenv("LLM_TEMPERATURE", "0.1"))`
- No seed parameter for additional determinism

**Research Finding:**
Per [Medium article "Temperature=0 is a Lie"](https://medium.com/write-a-catalyst/temperature-0-is-a-lie-why-your-llm-is-still-random-b58e26b65752), temperature=0 alone does NOT guarantee reproducibility due to GPU non-determinism. However, for practical test execution consistency, temperature=0 significantly improves predictability.

### FND-05: Browser Cleanup

**Current Issues:**
- `backend/agent/browser_agent.py` has `try/except` but browser-use Agent handles cleanup internally
- `backend/core/agent_service.py` has no explicit cleanup pattern
- No error logging for browser cleanup failures

**Existing Assets:**
- browser-use library manages browser lifecycle internally
- Screenshot saving has error handling

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | 0.100+ | Web framework | Async support, OpenAPI, Pydantic integration |
| Pydantic | 2.x | Data validation | Type safety, schema generation |
| SQLAlchemy | 2.x | ORM | Async support with aiosqlite |
| aiosqlite | 0.19+ | SQLite async driver | Non-blocking database I/O |
| python-dotenv | 1.x | Environment loading | Standard `.env` file support |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| browser-use | 0.12+ | AI browser automation | Core automation engine |
| Playwright | 1.40+ | Browser control | browser-use dependency |

## Architecture Patterns

### Recommended Configuration Structure

```
backend/
  config/
    __init__.py      # Export settings singleton
    settings.py      # Pydantic BaseSettings class
```

### Pattern 1: Pydantic Settings for Configuration

**What:** Centralized configuration using Pydantic BaseSettings
**When to use:** All environment variable access
**Example:**

```python
# Source: Pydantic v2 documentation pattern
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # LLM Configuration
    dashscope_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "qwen3.5-plus"
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_temperature: float = 0.0  # Changed from 0.1

    # ERP Configuration
    erp_base_url: str = ""
    erp_username: str = ""
    erp_password: str = ""

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/database.db"

    # Server
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Pattern 2: Consistent API Response Wrapper

**What:** Standard response envelope for all API responses
**When to use:** All API route responses
**Example:**

```python
# Source: FastAPI error handling patterns
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
import uuid

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None
    meta: Optional[dict] = None

class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str
    stack: Optional[str] = None

def success_response(data: T, meta: dict = None) -> ApiResponse[T]:
    return ApiResponse(success=True, data=data, meta=meta)

def error_response(code: str, message: str, request_id: str = None) -> ApiResponse:
    return ApiResponse(
        success=False,
        error={
            "code": code,
            "message": message,
            "request_id": request_id or str(uuid.uuid4())
        }
    )
```

### Pattern 3: FastAPI Exception Handler

**What:** Global exception handler for consistent error format
**When to use:** Application-level error handling
**Source:** [FastAPI Handling Errors Documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/)

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uuid

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": str(exc.detail),
                "request_id": request_id
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = str(uuid.uuid4())
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "request_id": request_id,
                "details": exc.errors()
            }
        }
    )
```

### Pattern 4: SQLAlchemy Async with Connection Pool

**What:** Explicit connection pool configuration for SQLite
**When to use:** Database engine creation
**Source:** [SQLAlchemy 2.1 Async Documentation](http://docs.sqlalchemy.org/en/latest/orm/extensions/asyncio.html)

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# SQLite with explicit pool settings
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,        # Connection pool size
    max_overflow=0,     # No overflow connections for SQLite
    pool_pre_ping=True, # Validate connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
```

### Pattern 5: LLM Deterministic Configuration

**What:** Configure LLM for reproducible test execution
**When to use:** Creating LLM instances for test automation
**Source:** [vLLM Reproducibility Documentation](https://docs.vllm.ai/en/latest/usage/reproducibility/)

```python
def get_llm_config() -> dict:
    """Get LLM configuration with deterministic settings"""
    return {
        "model": settings.llm_model,
        "api_key": settings.dashscope_api_key or settings.openai_api_key,
        "base_url": settings.llm_base_url,
        "temperature": 0.0,  # Deterministic output
        # Note: seed parameter can be added for additional determinism
        # but temperature=0 is the primary control
    }
```

### Pattern 6: Browser Cleanup with try/finally

**What:** Ensure browser resources are always cleaned up
**When to use:** Any code that controls browser lifecycle
**Example:**

```python
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def managed_browser(agent_service: AgentService, run_id: str):
    """Context manager for browser lifecycle"""
    browser = None
    try:
        browser = await agent_service.create_browser()
        yield browser
    except Exception as e:
        logger.error(f"[{run_id}] Browser error: {e}")
        raise
    finally:
        if browser:
            try:
                await browser.close()
                logger.info(f"[{run_id}] Browser closed successfully")
            except Exception as cleanup_error:
                logger.error(f"[{run_id}] Browser cleanup failed: {cleanup_error}")
```

### Anti-Patterns to Avoid

- **Hardcoded URLs/API Keys**: Never embed configuration values in source code
- **Mixed Error Formats**: Don't return different error structures for different endpoints
- **Blocking Database Calls**: Never use sync SQLAlchemy with FastAPI async routes
- **Missing Browser Cleanup**: Never rely on garbage collection for browser processes

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Configuration management | Custom env loader | Pydantic BaseSettings | Type safety, validation, caching |
| Error responses | Manual dict construction | FastAPI exception handlers | Consistent format, automatic status codes |
| Database sessions | Manual session management | FastAPI Depends + async_sessionmaker | Proper cleanup, connection pooling |
| LLM configuration | Inline os.getenv calls | Centralized settings class | Single source of truth |

## Common Pitfalls

### Pitfall 1: Temperature=0 Does Not Guarantee Determinism
**What goes wrong:** Developers assume temperature=0 means identical outputs every time
**Why it happens:** GPU operations introduce non-determinism even with temperature=0
**How to avoid:** Set temperature=0 for consistency, but document that 100% reproducibility is not guaranteed
**Warning signs:** Tests that depend on exact LLM output matching

### Pitfall 2: SQLite Pool Size Confusion
**What goes wrong:** Setting large pool sizes for SQLite
**Why it happens:** Developers apply PostgreSQL patterns to SQLite
**How to avoid:** SQLite is file-based; 5 connections is sufficient for development
**Warning signs:** "database is locked" errors

### Pitfall 3: Missing request_id in Error Responses
**What goes wrong:** Debugging production issues without traceability
**Why it happens:** Forgetting to include request_id in error format
**How to avoid:** Generate UUID in exception handler, include in all error responses
**Warning signs:** Cannot correlate user error reports with server logs

### Pitfall 4: Frontend Hardcoded API URL
**What goes wrong:** Frontend fails when deployed to different environment
**Why it happens:** Hardcoded localhost URL in client code
**How to avoid:** Use Vite's `VITE_API_BASE` environment variable
**Warning signs:** CORS errors or connection refused in production

## Code Examples

### FND-01: Centralized Configuration

```python
# backend/config/settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # LLM Configuration
    dashscope_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "qwen3.5-plus"
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_temperature: float = 0.0

    # ERP Configuration
    erp_base_url: str = ""
    erp_username: str = ""
    erp_password: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage in routes
from backend.config import get_settings

settings = get_settings()
llm_config = {
    "model": settings.llm_model,
    "api_key": settings.dashscope_api_key or settings.openai_api_key,
    "base_url": settings.llm_base_url,
    "temperature": settings.llm_temperature,
}
```

```typescript
// frontend/src/api/client.ts
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'
```

### FND-02: Consistent API Response Format

```python
# backend/api/response.py
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
import uuid

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None
    meta: Optional[dict] = None

def success(data: T, meta: dict = None) -> dict:
    return {"success": True, "data": data, "meta": meta}

def error(code: str, message: str, status_code: int = 400) -> tuple[dict, int]:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "request_id": str(uuid.uuid4())
        }
    }, status_code
```

### FND-03: Async Database Configuration

```python
# backend/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./data/database.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### FND-04: LLM Temperature Configuration

```python
# backend/llm/factory.py (modification)
def create_llm(llm_config: dict | None = None) -> "ChatOpenAI":
    config = llm_config or {}
    temperature = config.get("temperature", 0.0)  # Changed from 0.1
    # ... rest of function
```

### FND-05: Browser Cleanup Pattern

```python
# backend/core/agent_service.py (addition)
async def run_with_cleanup(
    self,
    task: str,
    run_id: str,
    on_step: Callable,
    max_steps: int = 10,
    llm_config: dict | None = None,
) -> Any:
    """Execute with guaranteed cleanup"""
    try:
        result = await self.run_with_streaming(
            task=task,
            run_id=run_id,
            on_step=on_step,
            max_steps=max_steps,
            llm_config=llm_config,
        )
        return result
    except Exception as e:
        logger.error(f"[{run_id}] Execution failed: {e}")
        raise
    finally:
        # browser-use handles browser cleanup internally
        # but we log for debugging
        logger.info(f"[{run_id}] Execution completed, resources cleaned up")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Inline os.getenv | Pydantic BaseSettings | 2023+ | Type safety, validation |
| Manual error dict | FastAPI exception handlers | FastAPI 0.68+ | Consistent format |
| Sync SQLite | aiosqlite + async engine | SQLAlchemy 2.0 | Non-blocking I/O |
| temperature=0.1 | temperature=0 | This phase | Deterministic tests |

**Deprecated/outdated:**
- Manual environment variable parsing: Use Pydantic Settings instead
- Sync database operations: All DB access must use async engine

## Open Questions

1. **Should we add seed parameter for additional LLM determinism?**
   - What we know: temperature=0 is primary control, seed provides additional reproducibility
   - What's unclear: Browser-use/ChatOpenAI compatibility with seed parameter
   - Recommendation: Start with temperature=0, add seed if needed

2. **Should error responses include stack traces in production?**
   - What we know: Stack traces help debugging but expose internals
   - What's unclear: Production deployment context
   - Recommendation: Include stack only when LOG_LEVEL=DEBUG, omit otherwise

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | `pyproject.toml` (existing) |
| Quick run command | `uv run pytest backend/tests/ -v -x` |
| Full suite command | `uv run pytest backend/tests/ -v --cov=backend` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FND-01 | Config values from env vars | unit | `pytest backend/tests/test_config.py -v` | No - Wave 0 |
| FND-02 | API responses have consistent format | unit | `pytest backend/tests/test_api_response.py -v` | No - Wave 0 |
| FND-03 | Database operations non-blocking | integration | `pytest backend/tests/test_db_async.py -v` | No - Wave 0 |
| FND-04 | LLM temperature=0 | unit | `pytest backend/tests/test_llm_config.py -v` | Exists (partial) |
| FND-05 | Browser cleanup on error | integration | `pytest backend/tests/test_browser_cleanup.py -v` | No - Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/ -v -x` (stop on first failure)
- **Per wave merge:** `uv run pytest backend/tests/ -v --cov=backend`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/test_config.py` - tests FND-01 configuration centralization
- [ ] `backend/tests/test_api_response.py` - tests FND-02 response format consistency
- [ ] `backend/tests/test_db_async.py` - tests FND-03 async database patterns
- [ ] `backend/tests/test_llm_config.py` - update to verify temperature=0 for FND-04
- [ ] `backend/tests/test_browser_cleanup.py` - tests FND-05 browser cleanup patterns
- [ ] `backend/tests/conftest.py` - add shared fixtures for response validation

### Test Scenarios by Requirement

**FND-01 Test Scenarios:**
1. Verify all config values load from environment
2. Verify default values work without .env file
3. Verify frontend API_BASE uses VITE_API_BASE

**FND-02 Test Scenarios:**
1. Success response has success=true, data field
2. Error response has success=false, error with code/message/request_id
3. HTTP exceptions return correct status codes
4. Validation errors return 400 with structured error

**FND-03 Test Scenarios:**
1. Database engine has pool_size=5
2. Concurrent requests don't block
3. Sessions properly closed after request

**FND-04 Test Scenarios:**
1. create_llm() returns temperature=0 by default
2. get_llm_config() returns temperature=0
3. Environment variable override works

**FND-05 Test Scenarios:**
1. Browser cleanup runs on success
2. Browser cleanup runs on exception
3. Cleanup errors are logged

## Sources

### Primary (HIGH confidence)
- [FastAPI Handling Errors Documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/) - Exception handler patterns
- [SQLAlchemy 2.1 Async Documentation](http://docs.sqlalchemy.org/en/latest/orm/extensions/asyncio.html) - Connection pool configuration
- [SQLite SQLAlchemy Documentation](http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html) - aiosqlite dialect

### Secondary (MEDIUM confidence)
- [Better Stack: FastAPI Error Handling](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/) - Consistent error response patterns
- [Stack Overflow: Unify Response Format](https://stackoverflow.com/questions/77854089/how-to-unify-the-response-format-in-fastapi-while-preserving-pydantic-data-model) - Response wrapper pattern

### Tertiary (LOW confidence)
- [Medium: Temperature=0 is a Lie](https://medium.com/write-a-catalyst/temperature-0-is-a-lie-why-your-llm-is-still-random-b58e26b65752) - LLM determinism limitations (requires validation)
- [vLLM Reproducibility](https://docs.vllm.ai/en/latest/usage/reproducibility/) - Seed parameter behavior (platform-specific)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All libraries are stable and well-documented
- Architecture: HIGH - Patterns are from official documentation
- Pitfalls: MEDIUM - Some LLM determinism claims need runtime validation

**Research date:** 2026-03-14
**Valid until:** 30 days - stable patterns, 7 days for LLM behavior specifics
