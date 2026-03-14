# Stack Research

**Domain:** AI-driven UI automation testing platform
**Researched:** 2026-03-14
**Confidence:** MEDIUM (some dependency version conflicts require runtime validation)

## Recommended Stack

This is an existing codebase. The research focuses on optimizing the current stack for v0.1 stability.

### Core Technologies

| Technology | Current Version | Recommended Version | Purpose | Notes |
|------------|-----------------|---------------------|---------|-------|
| Python | 3.11 | 3.11+ | Backend runtime | Good choice, stable |
| FastAPI | 0.135.1 | >=0.135.1 | Web framework | Current is latest stable |
| React | 19.2.0 | 19.x | Frontend UI | Stable, but see compatibility notes |
| TypeScript | 5.9.3 | 5.9.x | Type safety | Latest stable |
| Vite | 7.3.1 | 7.x | Build tool | Current is recent |
| Tailwind CSS | 4.2.1 | 4.x | Styling | New architecture, see setup notes |

### AI Integration Layer

| Technology | Current Version | Recommended Version | Purpose | Notes |
|------------|-----------------|---------------------|---------|-------|
| browser-use | >=0.12.2 | 0.12.1+ | AI browser automation | **Upgrade recommended to 0.12.1+** (pinned deps in 0.12.0+) |
| langchain-openai | >=0.3.0 | 0.3.x | LLM integration | Use with langchain-core for Qwen |
| langchain-core | >=0.3.0 | >=0.3.51 | Core LangChain | Must match langchain-openai version |
| dashscope | >=1.20.0 | 1.20.x | Alibaba Cloud SDK | Direct API calls, stable |
| Playwright | >=1.40.0 | 1.50+ | Browser automation | **Upgrade recommended** for async pytest support |

### Database Layer

| Technology | Current Version | Recommended Version | Purpose | Notes |
|------------|-----------------|---------------------|---------|-------|
| SQLAlchemy | >=2.0.0 | 2.0.x | ORM | Stable, async support |
| aiosqlite | >=0.20.0 | 0.20.x | Async SQLite | Works well with SQLAlchemy 2.0 |

### Supporting Libraries

| Library | Current Version | Purpose | When to Use |
|---------|-----------------|---------|-------------|
| pydantic | >=2.4.0 | Data validation | **CRITICAL: >=2.4.0 required** for CVE fix |
| pydantic-settings | >=2.0.0 | Settings management | Environment config |
| uvicorn[standard] | >=0.34.0 | ASGI server | Dev and production |
| httpx | >=0.28.1 | HTTP client | External API calls |
| tenacity | >=8.0.0 | Retry logic | LLM API resilience |
| python-dotenv | >=1.0.0 | Env file loading | Local development |
| pyyaml | >=6.0 | YAML parsing | Config files |

### Frontend Supporting Libraries

| Library | Current Version | Purpose | Notes |
|---------|-----------------|---------|-------|
| @tanstack/react-query | 5.90.21 | Data fetching | Works with React 19 |
| react-router-dom | 7.13.1 | Routing | React 19 compatible |
| lucide-react | 0.577.0 | Icons | Stable |
| recharts | 3.8.0 | Charts | For reports |

## Installation

```bash
# Backend (Python) - using uv
uv sync
uv run playwright install chromium

# Frontend (Node.js)
cd frontend && npm install
```

## Version Compatibility Issues

### Critical: Pydantic CVE-2024-3772

**Issue:** Pydantic versions < 2.4.0 contain a ReDoS vulnerability in email validation regex.

**Status:** Current pyproject.toml specifies `>=2.4.0` - **CORRECT**

**Action:** Verify installed version with `uv pip show pydantic`

### Warning: browser-use Dependency Pinning

**Issue:** browser-use 0.12.0+ pins all dependencies (see [GitHub #4215](https://github.com/browser-use/browser-use/pull/4215))

**Impact:** May conflict with other packages requiring different langchain versions

**Mitigation:**
- Current spec `browser-use>=0.12.2` is correct
- Test installation with `uv sync` to verify no conflicts
- If conflicts occur, consider using browser-use's bundled langchain

### Warning: LangChain Ecosystem Version Matrix

**Issue:** langchain-openai 0.3.x requires langchain-core >=0.3.51

**Current State:** Both specified as `>=0.3.0` - may resolve to incompatible versions

**Recommendation:** Pin explicitly:
```toml
"langchain-openai>=0.3.0,<0.4.0",
"langchain-core>=0.3.51,<1.0.0",
```

### Note: React 19 + TanStack Query

**Status:** Compatible but verify
- TanStack Query v5 requires React 18+ (works with React 19)
- Some wrapper libraries may have issues
- Test data fetching thoroughly

### Note: Playwright Version

**Current:** `>=1.40.0`
**Recommended:** Upgrade to `>=1.50.0`

**Reason:** Playwright 1.50+ includes async pytest plugin support, useful for testing the AI agent itself.

## Configuration Recommendations

### Backend pyproject.toml Optimization

```toml
[project]
dependencies = [
    # AI/Browser automation - pin carefully
    "browser-use>=0.12.1,<0.13.0",
    "langchain-openai>=0.3.0,<0.4.0",
    "langchain-core>=0.3.51,<1.0.0",
    "playwright>=1.50.0,<2.0.0",

    # Web framework
    "fastapi>=0.135.1",
    "uvicorn[standard]>=0.34.0",
    "httpx>=0.28.1",

    # Data validation - CRITICAL for security
    "pydantic>=2.4.0",  # CVE-2024-3772 fix
    "pydantic-settings>=2.0.0",

    # Database
    "sqlalchemy>=2.0.0",
    "aiosqlite>=0.20.0",

    # Utilities
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "tenacity>=8.0.0",
    "dashscope>=1.20.0",

    # Testing
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
]
```

### SQLAlchemy Async Best Practices

```python
# In database base class
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass

# In session configuration
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,  # CRITICAL for async
    class_=AsyncSession
)
```

### Frontend package.json Status

Current versions are appropriate for v0.1:
- React 19.2.0 - stable
- TypeScript 5.9.3 - latest
- Vite 7.3.1 - current
- Tailwind CSS 4.2.1 - new architecture but stable

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Pydantic <2.4.0 | CVE-2024-3772 ReDoS vulnerability | Pydantic >=2.4.0 |
| Playwright <1.40.0 | Missing async pytest features | Playwright >=1.50.0 |
| React 18 (if on 19) | Downgrade unnecessary | Stay on React 19 |
| SQLite for production | Concurrent write limitations | PostgreSQL with asyncpg |

## Security Considerations

### Addressed
- Pydantic >=2.4.0 (CVE-2024-3772 fix)

### To Verify
- [ ] dashscope API key stored in environment, not code
- [ ] ERP credentials stored securely
- [ ] No hardcoded secrets in frontend build

### For Production (v0.2+)
- Add rate limiting to FastAPI endpoints
- Enable HTTPS
- Consider PostgreSQL instead of SQLite for concurrent access

## Sources

- [FastAPI Release Notes](https://fastapi.tiangolo.com/release-notes/) - Version compatibility (HIGH confidence)
- [browser-use GitHub Releases](https://github.com/browser-use/browser-use/releases) - Latest version 0.12.1 (HIGH confidence)
- [browser-use Issue #4285](https://github.com/browser-use/browser-use/issues/4285) - OpenAI dependency pinning (HIGH confidence)
- [CVE-2024-3772 NVD](https://nvd.nist.gov/vuln/detail/cve-2024-3772) - Pydantic vulnerability (HIGH confidence)
- [LangChain Migration Docs](https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5) - React Query compatibility (HIGH confidence)
- [SQLAlchemy Async Guide](https://dev.to/amverum/asynchronous-sqlalchemy-2-a-simple-step-by-step-guide) - Best practices (MEDIUM confidence)
- [Playwright Release Notes](https://playwright.dev/docs/release-notes) - Version features (HIGH confidence)
- [DashScope OpenAI Compatibility](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope) - Qwen integration (HIGH confidence)

---
*Stack research for: aiDriveUITest v0.1*
*Researched: 2026-03-14*
