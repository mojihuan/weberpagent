# Technology Stack

**Analysis Date:** 2026-04-03

## Languages

**Primary:**
- Python 3.11 - Backend API, LLM integration, browser automation
- TypeScript - Frontend React application

**Secondary:**
- HTML/CSS - Frontend styling (Tailwind CSS)

## Runtime

**Environment:**
- Python 3.11+ (with uv package manager)
- Node.js 18+ (for frontend)

**Package Managers:**
- uv - Python dependency management (primary)
- npm - Frontend package management

**Lockfiles:**
- `uv.lock` - Python dependencies
- `package-lock.json` - Frontend dependencies

## Frameworks

**Core:**
- FastAPI 0.135.1+ - Python web framework with async support
- React 19.2.0 - Frontend UI library
- Vite 7.3.1 - Frontend build tool

**Browser Automation:**
- browser-use 0.12.2+ - AI-powered browser automation (uses CDP/Playwright)
- Playwright 1.40.0+ - Browser automation (underlying driver)

**LLM Integration:**
- langchain-openai 0.3.0+ - LLM integration
- dashscope 1.20.0+ - Alibaba Cloud AI API

**Testing:**
- pytest 8.0.0+ - Python testing framework
- pytest-asyncio 0.24.0+ - Async test support

**Build/Dev:**
- Ruff 0.4.0+ - Python linting/formatting
- ESLint 9.39.1 - JavaScript linting
- Tailwind CSS 4.2.1 - CSS utility framework

## Key Dependencies

**Critical:**
- `browser-use>=0.12.2` - Core AI browser automation
- `langchain-openai>=0.3.0` - LLM model integration
- `langchain-core>=0.3.0` - LangChain core utilities
- `fastapi>=0.135.1` - Web framework
- `uvicorn[standard]>=0.34.0` - ASGI server

**Frontend:**
- `react@19.2.0` - UI framework
- `@tanstack/react-query@5.90.21` - Data fetching/caching
- `react-router-dom` - Client-side routing
- `tailwindcss@4.2.1` - CSS framework

**Data & Persistence:**
- `sqlalchemy>=2.0.0` - ORM
- `aiosqlite>=0.20.0` - Async SQLite driver
- `pydantic>=2.4.0` - Data validation
- `pydantic-settings>=2.0.0` - Settings management

**Utilities:**
- `httpx>=0.28.1` - HTTP client
- `tenacity>=8.0.0` - Retry logic
- `jinja2>=3.1.6` - Template engine (variable substitution)
- `nest_asyncio>=1.5.0` - Nested asyncio support
- `pyyaml>=6.0` - YAML config parsing

## Configuration

**Environment:**
- `.env` file for local development
- Pydantic BaseSettings for type-safe config

**Key env vars:**
- `DASHSCOPE_API_KEY` - Alibaba Cloud AI API key
- `OPENAI_API_KEY` - OpenAI API key
- `LLM_MODEL` - Model name (default: qwen3.5-plus)
- `LLM_BASE_URL` - API base URL
- `ERP_BASE_URL` - Target ERP system URL
- `ERP_USERNAME` / `ERP_PASSWORD` - ERP credentials

**Build Config:**
- `pyproject.toml` - Python project configuration (uv-based)
- `package.json` - Node.js dependencies
- `ruff.toml` or `pyproject.toml[tool.ruff]` - Linting config
- `tsconfig.json` - TypeScript configuration
- `vite.config.ts` - Vite build configuration

## Platform Requirements

**Development:**
- Python 3.11+
- Node.js 18+
- uv package manager
- Chrome/Chromium browser

**Production:**
- ASGI server (uvicorn with gunicorn workers)
- SQLite or PostgreSQL database
- Chrome/Chromium in headless mode

---

*Stack analysis: 2026-04-03*
