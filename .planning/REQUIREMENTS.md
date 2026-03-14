# Requirements: aiDriveUITest v0.1

**Defined:** 2026-03-14
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v1 Requirements

Requirements for v0.1 release. Each maps to roadmap phases.

### Foundation

- [x] **FND-01**: Environment configuration is centralized (no hardcoded URLs/API keys)
- [x] **FND-02**: API responses use consistent format (success, data, error, meta)
- [x] **FND-03**: All async database operations use async engine (no blocking)
- [x] **FND-04**: LLM temperature is set to 0 for deterministic test execution
- [x] **FND-05**: Browser cleanup uses try/finally pattern (no memory leaks)

### Database

- [x] **DATA-01**: Assertion model exists with type, expected fields (links to Task via task_id)
- [x] **DATA-02**: AssertionResult model exists with status, message, actual_value fields (links to Run and Assertion)
- [x] **DATA-03**: Run-Assertion relationship is properly configured
- [x] **DATA-04**: Screenshot storage uses file system (not BLOB in database) — **Already implemented**
- [x] **DATA-05**: RunRepository.get_steps() method exists and works

### Service Layer

- [x] **SVC-01**: AssertionService validates assertions against run results
- [x] **SVC-02**: ReportService generates test reports with all step details
- [x] **SVC-03**: AgentService uses proper LLM configuration (temperature=0)
- [x] **SVC-04**: SSE EventManager includes heartbeat events (15-30s interval)
- [x] **SVC-05**: All background tasks update database status on completion/error

### Frontend

- [x] **UI-01**: API types match backend response schemas exactly
- [x] **UI-02**: Task list displays all tasks with correct data
- [x] **UI-03**: Execution monitor shows real-time step updates via SSE
- [x] **UI-04**: Screenshot panel displays images from correct paths
- [x] **UI-05**: Report page shows assertion results and step details
- [x] **UI-06**: API base URL is configurable via environment variable

### End-to-End Flow

- [x] **E2E-01**: User can create a new test task with natural language description
- [x] **E2E-02**: User can execute a task and see real-time progress
- [x] **E2E-03**: User can view execution screenshots for each step
- [x] **E2E-04**: User can view final test report with assertion results
- [x] **E2E-05**: Complete flow works without errors (create -> execute -> monitor -> report)

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Authentication

- **AUTH-01**: User can sign up with email and password
- **AUTH-02**: User session persists across browser refresh
- **AUTH-03**: User can only access their own tasks and reports

### Task Scheduling

- **SCHED-01**: User can schedule tasks to run at specific times
- **SCHED-02**: User can set up recurring task execution
- **SCHED-03**: Task dependencies and execution order

### Advanced Features

- **ADV-01**: Test data management (CRUD for test fixtures)
- **ADV-02**: Task templates with variable substitution
- **ADV-03**: Multi-browser support (Firefox, Safari)
- **ADV-04**: Video recording of test execution
- **ADV-05**: Parallel test execution

## Out of Scope

Explicitly excluded from v0.1. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| User authentication | v0.1 is single-user local use only |
| Task scheduling | Non-essential for core flow validation |
| Test data management | Complex feature, defer to v0.2 |
| Multi-browser support | Focus on Chromium first |
| Video recording | Storage costs, not critical for v0.1 |
| Docker deployment | Local development environment only for v0.1 |
| PostgreSQL migration | SQLite sufficient for v0.1 scale |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FND-01 | Phase 1 | Complete |
| FND-02 | Phase 1 | Complete |
| FND-03 | Phase 1 | Complete |
| FND-04 | Phase 1 | Complete |
| FND-05 | Phase 1 | Complete |
| DATA-01 | Phase 2 | Complete |
| DATA-02 | Phase 2 | Complete |
| DATA-03 | Phase 2 | Complete |
| DATA-04 | Phase 2 | Complete (pre-existing) |
| DATA-05 | Phase 2 | Complete |
| SVC-01 | Phase 3 | Complete |
| SVC-02 | Phase 3 | Complete |
| SVC-03 | Phase 3 | Complete |
| SVC-04 | Phase 3 | Complete |
| SVC-05 | Phase 3 | Complete |
| UI-01 | Phase 4 | Complete |
| UI-02 | Phase 4 | Complete |
| UI-03 | Phase 4 | Complete |
| UI-04 | Phase 4 | Complete |
| UI-05 | Phase 4 | Complete |
| UI-06 | Phase 4 | Complete |
| E2E-01 | Phase 4 | Complete |
| E2E-02 | Phase 4 | Complete |
| E2E-03 | Phase 4 | Complete |
| E2E-04 | Phase 4 | Complete |
| E2E-05 | Phase 4 | Complete |

**Coverage:**
- v1 requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0

---
*Requirements defined: 2026-03-14*
*Last updated: 2026-03-14 - UI-05 complete (Report assertion results display)*
