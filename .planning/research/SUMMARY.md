# Project Research Summary

**Project:** aiDriveUITest
**Domain:** AI-Driven UI Testing Platform (Existing Codebase)
**Current Milestone:** v0.3 - External Precondition Integration
**Researched:** 2026-03-17
**Confidence:** HIGH

## Executive Summary

aiDriveUITest is an AI-driven UI automation testing platform that enables QA testers to write test cases in natural language. The system uses Browser-Use + Qwen 3.5 Plus to interpret test descriptions and execute them via Playwright. This is an **existing codebase** with v0.1-v0.2 already delivered; v0.3 focuses on integrating an external precondition module (webseleniumerp).

The recommended approach for v0.3 is **bridge module integration**: add webseleniumerp to PYTHONPATH and create a dedicated `ExternalPreconditionBridge` module that isolates external imports, provides centralized error handling, and exposes operation codes (FA1, HC1, etc.) via a new API endpoint. The existing architecture (Repository pattern, SSE EventManager, FastAPI BackgroundTasks, PreconditionService) should be preserved and extended.

Key risks include the missing `config/settings.py` in webseleniumerp (in .gitignore), import isolation, and operation code parsing reliability. These must be addressed with proper setup documentation and a robust bridge module implementation.

## Key Findings

### Recommended Stack

The current technology choices are stable and appropriate. Key recommendations focus on version pinning and external module integration patterns.

**Core technologies:**
- **Python 3.11+ / FastAPI 0.135.1+**: Backend runtime and web framework - stable, async SSE support
- **React 19.x / TypeScript 5.9.x**: Frontend - current versions work well together
- **browser-use 0.12.1+**: AI browser automation - pin due to dependency changes in 0.12.0+
- **SQLAlchemy 2.0.x + aiosqlite**: Async database - MUST use async engine
- **Playwright 1.50+**: Browser automation - upgrade for async pytest support

**Critical version requirements:**
- Pydantic >=2.4.0 (CVE-2024-3772 fix)
- langchain-core >=0.3.51 (compatibility with langchain-openai 0.3.x)

**New for v0.3:**
- webseleniumerp via PYTHONPATH + ExternalPreconditionBridge module

### Expected Features

*Note: FEATURES.md research was not generated. Feature analysis derived from PROJECT.md and ARCHITECTURE.md.*

**v0.1-v0.2 Delivered:**
- Task Management (create/edit/copy/delete) - complete
- AI Execution (Browser-Use + Qwen 3.5 Plus) - complete
- Real-time Monitoring (SSE progress updates) - complete
- Test Reports (screenshots, assertions, timing) - complete
- Precondition System (Python code execution, context caching) - complete
- API Assertion System (status, response body, JSON path, time cost) - complete
- Dynamic Data Support (external module, random generators, time calculation) - complete

**v0.3 Active (External Precondition Integration):**
- External precondition module path configuration (WEBSERP_PATH)
- Frontend operation code selector (dropdown: FA1, HC1, etc.)
- Precondition execution result display

**Defer (v0.4+):**
- Batch execution (Excel import)
- User authentication/permissions
- Server deployment

### Architecture Approach

The platform follows a clean layered architecture with event-driven real-time updates. For v0.3, the key addition is the ExternalPreconditionBridge module.

**Major components:**
1. **Presentation Layer (React)**: Pages consume TanStack Query hooks, SSE via useRunStream hook. NEW: PreconditionEditor with OperationCodeSelector
2. **API Layer (FastAPI)**: REST endpoints + SSE streaming. NEW: `/external-operations` endpoint
3. **Service Layer**: AgentService (browser-use), EventManager (SSE pub-sub), PreconditionService (exec runner). NEW: ExternalPreconditionBridge
4. **Data Layer**: Repository pattern for data access, SQLite + SQLAlchemy async

**New v0.3 Component - ExternalPreconditionBridge:**
- `configure_external_path(WEBSERP_PATH)`: Add webseleniumerp to sys.path
- `load_pre_front_class()`: Load PreFront class with caching
- `get_available_operations()`: Parse and return operation codes dict
- `execute_operations(codes)`: Execute selected precondition operations

**Critical dependency warning:**
- webseleniumerp's `config/settings.py` is in .gitignore and must be created locally

### Critical Pitfalls

1. **Missing config/settings.py in webseleniumerp** - The external project has this file in .gitignore; must create a minimal template with DATA_PATHS configuration before integration will work

2. **LLM Non-Determinism Causing Test Flakiness** - Set temperature=0 for test execution, implement caching strategies, run multiple trials with pass rate metrics

3. **SSE Connection Management During Long-Running Tasks** - Implement heartbeat events every 15-30s, store all progress in database immediately, add client-side reconnection logic

4. **SQLite Blocking the Async Event Loop** - Always use async engine with aiosqlite driver, keep transactions short, test under concurrent load early

5. **Screenshot Storage Bloat in SQLite** - Store screenshots as files on disk, keep only paths in database, implement retention policy

## Implications for Roadmap

Based on research, suggested phase structure for v0.3:

### Phase 1: Configuration Foundation
**Rationale:** External module integration requires proper path configuration before any code can work.
**Delivers:** WEBSERP_PATH environment variable, config/settings.py template documentation
**Addresses:** External precondition module path configuration
**Avoids:** Hardcoded paths anti-pattern, import failures

### Phase 2: Backend Bridge Module
**Rationale:** Create isolation layer between weberpagent and webseleniumerp for clean error handling.
**Delivers:** ExternalPreconditionBridge module, `/external-operations` API endpoint
**Uses:** sys.path manipulation, inspect module for code parsing
**Implements:** get_available_operations(), load_pre_front_class(), execute_operations()

### Phase 3: Frontend Integration
**Rationale:** With backend bridge ready, add UI for selecting operation codes.
**Delivers:** OperationCodeSelector component, useExternalOperations hook, updated PreconditionEditor
**Uses:** TanStack Query for data fetching, existing PreconditionEditor patterns
**Implements:** Visual operation code selection, result display

### Phase 4: End-to-End Validation
**Rationale:** Verify complete flow from operation selection through execution.
**Delivers:** Working external precondition integration, test documentation
**Addresses:** Precondition execution result display

### Phase Ordering Rationale

- **Phase 1 first**: Configuration is a hard dependency - imports will fail without proper PYTHONPATH
- **Phase 2 second**: Bridge module isolates external code; must exist before frontend can call APIs
- **Phase 3 third**: Frontend depends on backend API being available
- **Phase 4 last**: Integration testing requires all components working

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** Operation code parsing from PreFront.operations() source - inspect.getsource parsing may be fragile if source format changes
- **Phase 3:** Frontend component design for operation code selector - need to decide on multi-select vs single-select, grouping, search

Phases with standard patterns (skip research-phase):
- **Phase 1:** Standard environment configuration, well-documented Python path handling
- **Phase 4:** Standard integration testing, existing patterns from v0.1-v0.2

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Based on official docs and version compatibility research |
| Features | MEDIUM | FEATURES.md not generated; inferred from PROJECT.md and codebase analysis |
| Architecture | HIGH | Based on comprehensive codebase analysis, direct webseleniumerp source review |
| Pitfalls | MEDIUM | Based on web research and community sources, not hands-on production experience |
| External Integration | HIGH | Based on direct code review of webseleniumerp and established Python import patterns |

**Overall confidence:** HIGH

### Gaps to Address

- **Missing FEATURES.md**: Feature prioritization based on inference rather than dedicated research. Current features are well-defined in PROJECT.md.
- **Operation code parsing robustness**: The inspect.getsource approach may break if webseleniumerp code format changes. Consider fallback or caching.
- **webseleniumerp config documentation**: Need clear setup guide for creating config/settings.py

## Sources

### Primary (HIGH confidence)
- [FastAPI Release Notes](https://fastapi.tiangolo.com/release-notes/) - Version compatibility
- [browser-use GitHub Releases](https://github.com/browser-use/browser-use/releases) - Latest version and dependency pinning
- [CVE-2024-3772 NVD](https://nvd.nist.gov/vuln/detail/cve-2024-3772) - Pydantic vulnerability
- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices) - Architecture patterns
- SQLAlchemy 2.0 Async Documentation - Database patterns
- webseleniumerp source code analysis - Direct code review for PreFront class structure

### Secondary (MEDIUM confidence)
- [AI Agent Testing Pyramid - Block Engineering](https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents) - AI flakiness vs software flakiness
- [Async SQLAlchemy Engine in FastAPI](https://medium.com/@mojimich2015/async-sqlalchemy-engine-in-fastapi-the-guide-e5acdba75c99) - Async patterns
- [SSE Production Considerations](https://dev.to/miketalbot/server-sent-events-are-still-not-production-ready-after-a-decade) - SSE reliability issues
- [Testing AI Agents: Non-Deterministic Behavior](https://www.sitepoint.com/testing-ai-agents-deterministic-evaluation-in-a-non-deterministic-world/) - Handling flakiness

### Tertiary (LOW confidence)
- [9 Production Realities for AI Agents](https://dev.to/franciscohumarang/the-9-production-realities-for-ai-agents) - Practical guidance
- [FastAPI Background Tasks + SSE Tutorial](https://dev.to/zachary62/build-an-llm-web-app-in-python-from-scratch-part-4-fastapi-background-tasks-sse-21g4) - Pattern examples

---
*Research completed: 2026-03-17*
*Updated for: v0.3 External Precondition Integration*
*Ready for roadmap: yes*
