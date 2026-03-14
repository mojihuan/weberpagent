# Codebase Structure

**Analysis Date:** 2026-03-14

## Directory Layout

```
aiDriveUITest/
├── backend/                        # Python backend (FastAPI)
│   ├── api/                        # API layer
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── routes/                 # API route definitions
│   │   │   ├── tasks.py            # Task management endpoints
│   │   │   ├── runs.py             # Execution management + SSE
│   │   │   ├── reports.py          # Report query endpoints
│   │   │   └── dashboard.py       # Dashboard data endpoints
│   │   └── schemas/                # Pydantic models
│   │       ├── __init__.py
│   │       ├── index.py           # Main schemas (Task, Run, Step, Report)
│   │       └── task.py            # Task-specific schemas
│   ├── core/                       # Core business logic
│   │   ├── agent_service.py        # Browser-Use agent wrapper
│   │   ├── event_manager.py        # SSE event management
│   │   └── assertion_service.py    # Result validation
│   ├── db/                         # Data layer
│   │   ├── models.py               # SQLAlchemy ORM models
│   │   ├── schemas.py              # Data transfer objects
│   │   ├── repository.py           # Repository pattern implementation
│   │   └── database.py             # Database connection setup
│   ├── llm/                        # LLM integration
│   │   ├── factory.py              # LLM instance factory
│   │   └── openai.py              # OpenAI-compatible implementation
│   ├── agent/                      # Browser-Use integration (archived)
│   ├── config/                     # Configuration files
│   ├── data/                       # Runtime data storage
│   │   └── screenshots/           # Screenshot storage
│   ├── storage/                    # File storage utilities
│   ├── tests/                      # Backend tests
│   │   ├── __init__.py
│   │   ├── test_dashboard_api.py  # Dashboard API tests
│   │   └── conftest.py            # Test configuration
│   └── utils/                      # Utility functions
├── frontend/                       # React frontend
│   ├── src/
│   │   ├── pages/                  # Page components
│   │   │   ├── Dashboard.tsx       # Dashboard page
│   │   │   ├── Tasks.tsx          # Task management page
│   │   │   ├── TaskDetail.tsx     # Task detail page
│   │   │   ├── RunList.tsx        # Execution list page
│   │   │   ├── RunMonitor.tsx     # Real-time monitoring page
│   │   │   ├── Reports.tsx        # Reports list page
│   │   │   └── ReportDetail.tsx   # Report detail page
│   │   ├── components/             # Reusable components
│   │   │   ├── Layout.tsx         # Main layout component
│   │   │   ├── Sidebar.tsx        # Navigation sidebar
│   │   │   ├── TaskDetail/       # Task detail components
│   │   │   ├── RunMonitor/       # Monitoring components
│   │   │   └── common/           # Common UI components
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── api/                   # API client
│   │   │   ├── client.ts          # Base API client
│   │   │   ├── tasks.ts          # Task API calls
│   │   │   ├── runs.ts           # Run API calls
│   │   │   └── reports.ts        # Report API calls
│   │   ├── types/                 # TypeScript type definitions
│   │   │   └── index.ts          # Main type exports
│   │   ├── assets/                # Static assets
│   │   └── App.tsx                # Main app component
│   ├── public/                     # Public assets
│   ├── package.json               # Dependencies and scripts
│   └── dist/                       # Build output
├── docs/                          # Documentation
│   ├── plans/                     # Design and implementation plans
│   └── troubleshooting/           # Issue resolution guides
├── .planning/codebase/             # Architecture analysis documents
├── .venv/                         # Python virtual environment
├── .env.example                   # Environment variables template
├── pyproject.toml                 # Python project configuration
├── uv.lock                        # Dependency lock file
└── README.md                      # Project documentation
```

## Directory Purposes

**backend/api/:**
- Purpose: HTTP API interface layer
- Contains: FastAPI routes, request/response schemas, CORS configuration
- Key files: `main.py` (entry point), `routes/*.py` (endpoints)

**backend/core/:**
- Purpose: Business logic and service orchestration
- Contains: Agent service, event management, assertion logic
- Key files: `agent_service.py` (browser-use wrapper), `event_manager.py` (SSE)

**backend/db/:**
- Purpose: Data persistence and access
- Contains: Database models, repositories, DTOs
- Key files: `models.py` (ORM), `repository.py` (data access)

**frontend/src/:**
- Purpose: React application source code
- Contains: Components, pages, API clients, types
- Key files: `App.tsx` (main app), `pages/*.tsx` (page components)

**docs/plans/:**
- Purpose: Project planning and design documentation
- Contains: Implementation plans, architectural decisions
- Key files: Various markdown files for different features

## Key File Locations

**Entry Points:**
- `backend/api/main.py`: FastAPI application entry
- `frontend/src/main.tsx`: React application entry

**Configuration:**
- `.env.example`: Environment variables template
- `pyproject.toml`: Python project configuration
- `frontend/package.json`: Frontend dependencies

**Core Logic:**
- `backend/core/agent_service.py`: AI agent orchestration
- `backend/db/repository.py`: Data access abstraction
- `frontend/src/api/client.ts`: HTTP client configuration

**Testing:**
- `backend/tests/`: Backend test files
- Frontend tests: Not detected in current structure

## Naming Conventions

**Files:**
- Python: `snake_case.py` (e.g., `agent_service.py`)
- TypeScript/React: `PascalCase.tsx` (e.g., `TaskDetail.tsx`)
- Test files: `test_*.py` or `*_test.py`

**Directories:**
- Lowercase with underscores: `api/`, `core/`, `db/`
- PascalCase for React: `components/`, `pages/`
- Singular nouns where appropriate: `repository.py` (not `repositories/`)

**Variables/Classes:**
- Python: `snake_case` for variables/functions, `PascalCase` for classes
- TypeScript: `camelCase` for variables/functions, `PascalCase` for interfaces/classes
- Database models: `PascalCase` (e.g., `Task`, `Run`)

## Where to Add New Code

**New Test Feature:**
- Primary code: `backend/api/routes/tasks.py` or new route file
- Tests: `backend/tests/test_[feature].py`
- Frontend: `frontend/src/pages/TaskDetail/components/`

**New Component/Module:**
- Implementation:
  - Backend: `backend/core/[feature]_service.py`
  - Frontend: `frontend/src/components/[Feature]/`
- API: `backend/api/routes/[feature].py`
- Types: `frontend/src/types/[feature].ts`

**Utilities/Helpers:**
- Backend utilities: `backend/utils/[helper].py`
- Frontend utilities: `frontend/src/hooks/use[Helper].ts`
- Shared types: `frontend/src/types/index.ts`

## Special Directories

**backend/data/screenshots/:**
- Purpose: Stores execution screenshots
- Generated: Yes (by AgentService)
- Committed: No (should be in .gitignore)

**docs/plans/:**
- Purpose: Project planning and documentation
- Generated: Yes (by planning process)
- Committed: Yes (version-controlled documentation)

**.venv/:**
- Purpose: Python virtual environment
- Generated: Yes (by uv sync)
- Committed: No (in .gitignore)

---

*Structure analysis: 2026-03-14*
