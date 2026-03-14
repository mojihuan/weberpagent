# Architecture

**Analysis Date:** 2026-03-14

## Pattern Overview

**Overall:** Layered Architecture with Event-Driven Processing

**Key Characteristics:**
- Separation of concerns across frontend/backend layers
- Event-driven real-time updates via SSE
- Repository pattern for data access
- Service layer for business logic encapsulation
- Browser-Use as the core AI automation engine

## Layers

**Presentation Layer (Frontend):**
- Purpose: React-based UI for user interaction
- Location: `frontend/src/`
- Contains: React components, pages, hooks, API clients
- Depends on: REST API endpoints, SSE streams
- Uses: React Router for navigation, TanStack Query for state management

**API Layer (Backend):**
- Purpose: FastAPI REST API with SSE support
- Location: `backend/api/`
- Contains: API routes, request/response schemas, CORS middleware
- Depends on: Core services, database layer
- Used by: Frontend client applications

**Service Layer:**
- Purpose: Business logic orchestration
- Location: `backend/core/`
- Contains: Agent service, event manager, assertion service
- Depends on: LLM adapters, repository layer, file system
- Used by: API layer routes

**Data Layer:**
- Purpose: Data persistence and access
- Location: `backend/db/`
- Contains: SQLAlchemy ORM models, repository classes, schemas
- Depends on: SQLite database
- Used by: Service layer, API layer

**External Integration Layer:**
- Purpose: AI engine and browser automation
- Location: `backend/llm/`, browser-use external dependency
- Contains: LLM factory, configuration adapters
- Depends on: OpenAI/DashScope APIs, Playwright browser
- Used by: Service layer (AgentService)

## Data Flow

**Test Execution Flow:**

1. **Request Initiation**
   - Frontend sends POST to `/api/runs` with task details
   - Backend creates Run record in database (status: pending)

2. **Background Processing**
   - FastAPI BackgroundTasks start agent execution
   - EventManager publishes SSE events to subscribers
   - Run status updated to "running"

3. **AI Agent Execution**
   - AgentService creates browser-use Agent with configured LLM
   - Agent executes steps based on natural language task
   - Step callback captures actions, reasoning, screenshots

4. **Real-time Updates**
   - Each step triggers callback with action/reasoning/screenshot
   - Repository saves step data to database
   - EventManager publishes SSE events to frontend
   - Frontend updates UI in real-time

5. **Completion & Reporting**
   - Agent finishes execution (success/failed/stopped)
   - EventManager publishes final event
   - AssertionService validates results against configured assertions
   - ReportRepository generates test report

6. **Frontend Display**
   - SSE stream updates execution timeline
   - Screenshots displayed in monitoring interface
   - Final report shown with step-by-step results

**State Management:**
- Database: Persistent storage for Tasks, Runs, Steps, Reports
- EventManager: In-memory event streaming for real-time updates
- React Query: Client-side state management and caching

## Key Abstractions

**Task:**
- Purpose: Represents a test case definition
- Examples: `backend/db/models.py` Task class, `frontend/src/types/index.ts` Task interface
- Pattern: Entity with relationships to Runs and configuration

**Run:**
- Purpose: Represents a single test execution instance
- Examples: `backend/db/models.py` Run class, `frontend/src/types/index.ts` Run interface
- Pattern: Aggregate root containing Steps and Report

**AgentService:**
- Purpose: Orchestrates browser-use Agent execution
- Examples: `backend/core/agent_service.py`
- Pattern: Facade pattern hiding browser-use complexity

**EventManager:**
- Purpose: Manages SSE event streaming and subscriptions
- Examples: `backend/core/event_manager.py`
- Pattern: Pub-sub pattern with in-memory event history

**Repository:**
- Purpose: Abstracts data access operations
- Examples: `backend/db/repository.py`
- Pattern: Repository pattern for data persistence

## Entry Points

**Backend Entry Point:**
- Location: `backend/api/main.py`
- Triggers: HTTP requests from frontend, background tasks
- Responsibilities: CORS setup, route registration, logging configuration

**Frontend Entry Point:**
- Location: `frontend/src/main.tsx`
- Triggers: Application startup, route navigation
- Responsibilities: React app initialization, routing setup

**API Endpoints:**
- `POST /api/tasks` - Create new test task
- `GET /api/tasks` - List all tasks
- `POST /api/runs` - Start test execution
- `GET /api/runs/{id}` - Get execution status (with SSE)
- `GET /api/reports` - List test reports
- `GET /api/dashboard` - Dashboard statistics

## Error Handling

**Strategy:** Centralized error handling with graceful degradation

**Patterns:**
- API layer: HTTPException with status codes and error messages
- Service layer: Try-catch blocks with logging, fallback behaviors
- Agent execution: Exception capture in step callbacks
- SSE: Error events published for frontend display
- Database: SQLAlchemy transaction rollback on errors

## Cross-Cutting Concerns

**Logging:**
- Structured logging with timestamps and context IDs
- DEBUG level for browser-use agent traces
- Error logging with stack traces and execution context

**Validation:**
- Pydantic schemas for API request/response validation
- Type-safe interfaces in frontend TypeScript
- Input sanitization for user-provided task descriptions

**Authentication:**
- Basic auth support for ERP system access
- API key-based LLM authentication
- Environment-based configuration security

---

*Architecture analysis: 2026-03-14*
