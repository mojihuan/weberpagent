# Technology Stack

**Analysis Date:** 2026-03-14

## Languages

**Primary:**
- Python 3.11 - Backend API and LLM integration
- TypeScript - Frontend React application

## Runtime

**Environment:**
- Python 3.11+ (with uv package manager)
- Node.js 18+ (for frontend)

**Package Managers:**
- uv - Python dependency management (replaces pip)
- npm - Frontend package management

**Lockfiles:**
- uv.lock - Python dependencies
- package-lock.json - Frontend dependencies

## Frameworks

**Core:**
- FastAPI - Python web framework (0.135.1)
- React - Frontend UI library (19.2.0)
- Vite - Frontend build tool (7.3.1)

**Testing:**
- pytest - Python testing framework (8.0.0)
- Playwright - Browser automation (1.40.0)

**Build/Dev:**
- Ruff - Python linting and formatting (0.4.0)
- ESLint - JavaScript linting (9.39.1)
- Tailwind CSS - CSS utility framework (4.2.1)

## Key Dependencies

**Critical:**
- browser-use>=0.12.2 - Browser automation with AI
- langchain-openai>=0.3.0 - LLM integration
- fastapi>=0.135.1 - Web framework
- react@19.2.0 - UI framework
- @tanstack/react-query@5.90.21 - Data fetching and caching

**Infrastructure:**
- uvicorn[standard]>=0.34.0 - ASGI server
- httpx>=0.28.1 - HTTP client
- pydantic>=2.4.0 - Data validation
- sqlalchemy>=2.0.0 - Database ORM
- aiosqlite>=0.20.0 - Async SQLite driver
- playwright>=1.40.0 - Browser automation

## Configuration

**Environment:**
- Environment variables for API keys and configuration
- YAML configuration files for LLM settings (`config/llm_config.yaml`)
- `.env` file for local development

**Build:**
- `pyproject.toml` - Python project configuration
- `package.json` - Node.js project configuration
- `ruff` configuration (line-length: 100)
- `tsconfig.json` - TypeScript configuration
- `vite.config.ts` - Vite build configuration

## Platform Requirements

**Development:**
- Python 3.11+
- Node.js 18+
- uv package manager
- Chrome/Chromium for Playwright

**Production:**
- ASGI server (uvicorn)
- Static file serving for frontend
- SQLite database (can be replaced with PostgreSQL/MySQL)

---

*Stack analysis: 2026-03-14*