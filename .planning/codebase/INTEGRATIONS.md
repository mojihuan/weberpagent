# External Integrations

**Analysis Date:** 2026-03-14

## APIs & External Services

**LLM Providers:**
- OpenAI - GPT models (primary integration via browser-use)
  - SDK: browser-use built-in ChatOpenAI
  - Auth: OPENAI_API_KEY environment variable
- DashScope (阿里云) - 通义千问 models (legacy)
  - SDK: langchain-openai with custom base URL
  - Auth: DASHSCOPE_API_KEY environment variable
- Azure OpenAI - Enterprise OpenAI
  - SDK: browser-use Azure ChatOpenAI
  - Auth: AZURE_OPENAI_API_KEY environment variable

**Browser Automation:**
- Chrome DevTools Protocol - Browser control
  - SDK: playwright and browser-use
  - Configuration: CHROME_DEBUG_PORT environment variable

## Data Storage

**Databases:**
- SQLite - Local development database
  - Connection: aiosqlite async driver
  - ORM: SQLAlchemy 2.0 with async support
  - Location: `backend/data/database.db`

**File Storage:**
- Local filesystem - Screenshots and outputs
  - Location: `outputs/` directory
  - Structure: Organized by task ID

**Caching:**
- React Query - Frontend caching and state management
  - Client: @tanstack/react-query
  - Strategy: Server-side rendering with client-side caching

## Authentication & Identity

**Auth Provider:**
- Custom basic authentication for ERP systems
  - Implementation: HTTP basic auth for ERP login
  - Environment variables: ERP_USERNAME, ERP_PASSWORD
- No built-in user authentication system (uses environment-based auth)

## Monitoring & Observability

**Error Tracking:**
- Custom logging - Structured JSON logging
  - Implementation: Python logging module
  - Framework: StructuredLogger in utils

**Logs:**
- File-based logging with rotation
  - Levels: DEBUG for browser-use, INFO for general
  - Location: Console output during development

## CI/CD & Deployment

**Hosting:**
- Not specified - Designed for local development
- Can be deployed with Docker containers

**CI Pipeline:**
- pytest for automated testing
- Ruff for code quality
- ESLint for JavaScript linting

## Environment Configuration

**Required env vars:**
- `OPENAI_API_KEY` - OpenAI API key
- `ERP_BASE_URL` - Target ERP system URL
- `ERP_USERNAME` - ERP system username
- `ERP_PASSWORD` - ERP system password
- `DASHSCOPE_API_KEY` - Alternative LLM provider (optional)
- `AZURE_OPENAI_API_KEY` - Azure OpenAI key (optional)

**Secrets location:**
- `.env` file for local development
- `.env.example` template provided
- Config loaded via pydantic-settings

## Webhooks & Callbacks

**Incoming:**
- Server-Sent Events (SSE) for real-time execution monitoring
  - Endpoint: `/api/runs/{run_id}/stream`
  - Events: started, step, finished, error
- RESTful API endpoints for all CRUD operations

**Outgoing:**
- ERP system API calls via browser automation
- LLM API calls to OpenAI/DashScope/Azure
- No configured outgoing webhooks

---

*Integration audit: 2026-03-14*