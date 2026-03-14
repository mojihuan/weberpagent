# Roadmap: aiDriveUITest v0.1

## Overview

This roadmap stabilizes an existing AI-driven UI testing platform. Starting from foundation fixes (configuration, async patterns), we enhance the data layer (schema, storage), restore service layer functionality (assertions, reports), and finally align the frontend for complete end-to-end flow. Each phase builds on the previous, ensuring the core value - natural language test execution - works reliably.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation Fixes** - Configuration, API standardization, async patterns
- [ ] **Phase 2: Data Layer Enhancement** - Database schema, screenshot storage, repository methods
- [ ] **Phase 3: Service Layer Restoration** - Assertion evaluation, report generation, SSE heartbeats
- [ ] **Phase 4: Frontend + E2E Alignment** - UI types, data display, complete user flow

## Phase Details

### Phase 1: Foundation Fixes
**Goal**: Stable foundation with proper configuration, consistent API responses, and correct async patterns
**Depends on**: Nothing (first phase)
**Requirements**: FND-01, FND-02, FND-03, FND-04, FND-05
**Success Criteria** (what must be TRUE):
  1. All configuration values (API URLs, LLM settings) come from environment variables with no hardcoded values
  2. All API endpoints return responses in the same format (success, data, error, meta fields)
  3. Database operations never block the event loop during concurrent requests
  4. LLM test execution produces consistent results for the same input (temperature=0)
  5. Browser processes are always cleaned up even when errors occur
**Plans**: 6 plans in 3 waves (including Wave 0 test scaffolding)

Plans:
- [x] 01-00-PLAN.md - Wave 0 test scaffolding (creates test stub files)
- [x] 01-01-PLAN.md - Environment configuration centralization (Wave 1, FND-01)
- [x] 01-02-PLAN.md - API response format standardization (Wave 1, FND-02)
- [x] 01-03-PLAN.md - Async database patterns verification (Wave 1, FND-03)
- [x] 01-04-PLAN.md - LLM deterministic configuration (Wave 2, depends on 01-01, FND-04)
- [x] 01-05-PLAN.md - Browser cleanup pattern implementation (Wave 2, FND-05)

### Phase 2: Data Layer Enhancement
**Goal**: Complete database schema with optimized screenshot storage and working repository methods
**Depends on**: Phase 1
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04 (verification-only), DATA-05
**Success Criteria** (what must be TRUE):
  1. Assertion model stores type, expected for each assertion (actual_value is on AssertionResult)
  2. AssertionResult model captures pass/fail status with messages and actual values
  3. Run records properly link to their associated assertion results
  4. Screenshots are stored as files on disk, not as BLOBs in the database (pre-existing, verify only)
  5. RunRepository.get_steps() returns all step data for a given run
**Plans**: 4 plans in 3 waves (including Wave 0 test scaffolding)

Plans:
- [x] 02-00-PLAN.md - Wave 0 test scaffolding for model and repository tests
- [x] 02-01-PLAN.md - Assertion and AssertionResult ORM model creation (Wave 1, DATA-01, DATA-02, DATA-03)
- [ ] 02-02-PLAN.md - RunRepository.get_steps() method implementation (Wave 1, DATA-05)
- [ ] 02-03-PLAN.md - Pydantic schemas and screenshot verification (Wave 2, DATA-04 verification, depends on 02-01, 02-02)

### Phase 3: Service Layer Restoration
**Goal**: Working assertion evaluation, automated report generation, and reliable SSE streaming
**Depends on**: Phase 2
**Requirements**: SVC-01, SVC-02, SVC-03, SVC-04, SVC-05
**Success Criteria** (what must be TRUE):
  1. AssertionService evaluates assertions against run results and produces pass/fail outcomes
  2. ReportService generates test reports containing all step details, screenshots, and assertion results
  3. AgentService uses temperature=0 for deterministic test execution
  4. SSE connections receive heartbeat events every 15-30 seconds to maintain connection
  5. All background tasks update database status on completion or error
**Plans**: TBD

Plans:
- [ ] 03-01: AssertionService implementation
- [ ] 03-02: ReportService implementation
- [ ] 03-03: AgentService LLM configuration
- [ ] 03-04: SSE heartbeat implementation
- [ ] 03-05: Background task status updates

### Phase 4: Frontend + E2E Alignment
**Goal**: Fully functional UI with correct data display and complete end-to-end user flow
**Depends on**: Phase 3
**Requirements**: UI-01, UI-02, UI-03, UI-04, UI-05, UI-06, E2E-01, E2E-02, E2E-03, E2E-04, E2E-05
**Success Criteria** (what must be TRUE):
  1. Frontend TypeScript types match backend Pydantic schemas exactly
  2. Task list displays all tasks with correct names, descriptions, and statuses
  3. Execution monitor shows real-time step updates including screenshots via SSE
  4. Report page displays assertion results with pass/fail status for each step
  5. User can complete the full flow: create task -> execute -> monitor -> view report without errors
**Plans**: TBD

Plans:
- [ ] 04-01: Frontend type alignment with backend
- [ ] 04-02: Task list display fix
- [ ] 04-03: Execution monitor SSE integration
- [ ] 04-04: Report page implementation
- [ ] 04-05: End-to-end flow verification

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation Fixes | 5/5 | Complete | 01-00, 01-01, 01-02, 01-03, 01-04, 01-05 |
| 2. Data Layer Enhancement | 2/4 | In progress | 02-00, 02-01 |
| 3. Service Layer Restoration | 0/5 | Not started | - |
| 4. Frontend + E2E Alignment | 0/5 | Not started | - |

---
*Roadmap created: 2026-03-14*
*Last updated: 2026-03-14 - Completed 02-01 Assertion ORM models*
