# Project Research Summary

**Project:** aiDriveUITest
**Domain:** AI-Driven UI Testing Platform (Existing Codebase Stabilization)
**Researched:** 2026-03-14
**Confidence:** MEDIUM-HIGH

## Executive Summary

aiDriveUITest is an AI-driven UI automation testing platform that enables QA testers to write test cases in natural language. The system uses Browser-Use + Qwen 3.5 Plus to interpret test descriptions and execute them via Playwright. This is an **existing codebase stabilization project** (v0.1), not a greenfield build - the core functionality already exists but has structural issues requiring targeted refactoring.

The recommended approach is **incremental restructuring** preserving the core layered architecture while fixing data flow issues, standardizing API responses, and adding missing database schema elements. The existing architecture (Repository pattern, SSE EventManager, FastAPI BackgroundTasks) is sound and should be preserved.

Key risks include LLM non-determinism causing test flakiness, SSE connection management during long-running tasks, and SQLite concurrency limitations. These must be addressed early in Phase 1 since they affect the core user experience.

## Key Findings

### Recommended Stack

The current technology choices are appropriate for v0.1. Key recommendations focus on version pinning and security patches rather than technology changes.

**Core technologies:**
- **Python 3.11+ / FastAPI 0.135.1+**: Backend runtime and web framework - stable, well-suited for async SSE streaming
- **React 19.x / TypeScript 5.9.x**: Frontend - current versions work well together
- **browser-use 0.12.1+**: AI browser automation - critical to pin due to dependency changes in 0.12.0+
- **SQLAlchemy 2.0.x + aiosqlite**: Async database - MUST use async engine to avoid event loop blocking
- **Playwright 1.50+**: Browser automation - upgrade recommended for async pytest support

**Critical version requirements:**
- Pydantic >=2.4.0 (CVE-2024-3772 fix - ReDoS vulnerability)
- langchain-core >=0.3.51 (compatibility with langchain-openai 0.3.x)

### Expected Features

*Note: FEATURES.md research was not generated. Feature analysis derived from PROJECT.md and ARCHITECTURE.md.*

**Must have (table stakes) - existing but needs fixes:**
- Task Management (create/edit/copy/delete test tasks) - exists, needs data flow fixes
- AI Execution (Browser-Use + Qwen 3.5 Plus) - exists, needs deterministic configuration
- Real-time Monitoring (SSE progress updates) - exists, needs connection management
- Test Reports (screenshots, assertions, timing) - exists, needs storage optimization

**Should have (competitive) - partially implemented:**
- Assertion System (URL check, text exists, no errors) - exists but schema gaps
- LLM Adapter (OpenAI/Qwen/DeepSeek multi-backend) - exists, needs cleanup

**Defer (v0.2+):**
- User authentication/permissions - single-user local use for v0.1
- Task scheduling (timed execution, task dependencies) - high complexity
- Server deployment - local development only for v0.1
- Multi-language support - Chinese only

### Architecture Approach

The platform follows a clean layered architecture with event-driven real-time updates. Current implementation has a solid foundation but requires targeted restructuring.

**Major components:**
1. **Presentation Layer (React)**: Pages consume TanStack Query hooks, SSE via useRunStream hook
2. **API Layer (FastAPI)**: REST endpoints + SSE streaming, BackgroundTasks for async execution
3. **Service Layer**: AgentService (browser-use), EventManager (SSE pub-sub), AssertionService (needs restoration)
4. **Data Layer**: Repository pattern for data access, SQLite + SQLAlchemy async

**Identified issues requiring fixes:**
- Database schema lacks assertions/assertion_results tables
- Frontend-backend type mismatches (step_index vs index, screenshot_path vs screenshot URL)
- Inconsistent API response format (some wrapped, some direct)
- Missing RunRepository.get_steps() method
- Hardcoded API base URL in frontend

### Critical Pitfalls

1. **LLM Non-Determinism Causing Test Flakiness** - Set temperature=0 for test execution, implement caching strategies, run multiple trials with pass rate metrics
2. **SSE Connection Management During Long-Running Tasks** - Implement heartbeat events every 15-30s, store all progress in database immediately, add client-side reconnection logic
3. **SQLite Blocking the Async Event Loop** - Always use async engine with aiosqlite driver, keep transactions short, test under concurrent load early
4. **Screenshot Storage Bloat in SQLite** - Store screenshots as files on disk, keep only paths in database, implement retention policy
5. **Browser-Use Agent Memory Leak** - Always use context managers for browser cleanup, wrap execution in try/finally, set maximum agent run time

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Foundation Fixes
**Rationale:** Core infrastructure issues (hardcoded URLs, missing methods, async patterns) must be fixed before any feature work. These affect everything downstream.
**Delivers:** Stable foundation with proper configuration, consistent API responses, working data flow
**Addresses:** Task management, API response standardization
**Avoids:** Hardcoded configuration anti-pattern, inconsistent error handling

### Phase 2: Data Layer Enhancement
**Rationale:** Database schema gaps (assertions tables) and storage strategy (screenshot files) are hard to change later. Must be done before service layer work.
**Delivers:** Complete database schema, optimized screenshot storage, assertion data model
**Uses:** SQLAlchemy async patterns, file-based screenshot storage
**Implements:** AssertionRepository, schema migrations

### Phase 3: Service Layer Restoration
**Rationale:** With foundation and data layer stable, restore and wire up assertion evaluation and report generation.
**Delivers:** Working assertion evaluation, automated report generation, complete test execution flow
**Uses:** AgentService integration, AssertionService restoration from archived code
**Implements:** End-to-end test execution with assertions

### Phase 4: Frontend Alignment
**Rationale:** Frontend depends on stable backend API. Fix type mismatches and ensure all components work with standardized responses.
**Delivers:** Fully functional UI, correct data display, proper error handling
**Implements:** API response transforms, type safety, environment configuration

### Phase Ordering Rationale

- **Phase 1 first**: Configuration and API standardization affects all other work - must be done first
- **Phase 2 second**: Database changes are invasive; do before service layer which depends on schema
- **Phase 3 third**: Services need stable data layer to function correctly
- **Phase 4 last**: Frontend consumes stable backend; fix after backend is solid

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** Assertion types and evaluation logic - need to review archived code and determine which assertion types to support in v0.1
- **Phase 3:** Report generation templates - may need research on report format and content

Phases with standard patterns (skip research-phase):
- **Phase 1:** Well-documented FastAPI patterns, standard configuration approaches
- **Phase 4:** Standard React/TanStack Query patterns, straightforward type alignment

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Based on official docs and version compatibility research |
| Features | MEDIUM | FEATURES.md not generated; inferred from PROJECT.md and codebase analysis |
| Architecture | HIGH | Based on comprehensive codebase analysis and established patterns |
| Pitfalls | MEDIUM | Based on web research and community sources, not hands-on production experience |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- **Missing FEATURES.md**: Feature prioritization based on inference rather than dedicated research. Validate feature list with actual codebase testing during Phase 1.
- **Assertion types scope**: Research mentions multiple assertion types but does not specify which to implement in v0.1. Review archived assertion code during Phase 2 planning.
- **Report format requirements**: Report content and format not specified. Clarify during Phase 3 planning.

## Sources

### Primary (HIGH confidence)
- [FastAPI Release Notes](https://fastapi.tiangolo.com/release-notes/) - Version compatibility
- [browser-use GitHub Releases](https://github.com/browser-use/browser-use/releases) - Latest version and dependency pinning
- [CVE-2024-3772 NVD](https://nvd.nist.gov/vuln/detail/cve-2024-3772) - Pydantic vulnerability
- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices) - Architecture patterns
- SQLAlchemy 2.0 Async Documentation - Database patterns

### Secondary (MEDIUM confidence)
- [AI Agent Testing Pyramid - Block Engineering](https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents) - AI flakiness vs software flakiness
- [Async SQLAlchemy Engine in FastAPI](https://medium.com/@mojimich2015/async-sqlalchemy-engine-in-fastapi-the-guide-e5acdba75c99) - Async patterns
- [SSE Production Considerations](https://dev.to/miketalbot/server-sent-events-are-still-not-production-ready-after-a-decade) - SSE reliability issues
- [Testing AI Agents: Non-Deterministic Behavior](https://www.sitepoint.com/testing-ai-agents-deterministic-evaluation-in-a-non-deterministic-world/) - Handling flakiness

### Tertiary (LOW confidence)
- [9 Production Realities for AI Agents](https://dev.to/franciscohumarang/the-9-production-realities-for-ai-agents) - Practical guidance
- [FastAPI Background Tasks + SSE Tutorial](https://dev.to/zachary62/build-an-llm-web-app-in-python-from-scratch-part-4-fastapi-background-tasks-sse-21g4) - Pattern examples

---
*Research completed: 2026-03-14*
*Ready for roadmap: yes*
