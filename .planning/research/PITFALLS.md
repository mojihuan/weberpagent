# Pitfalls Research

**Domain:** AI-driven UI Testing Platform (Browser-Use + FastAPI + React)
**Researched:** 2026-03-14
**Confidence:** MEDIUM (based on web research, not hands-on production experience)

## Critical Pitfalls

### Pitfall 1: LLM Non-Determinism Causing Test Flakiness

**What goes wrong:**
AI agents are inherently non-deterministic - the same test input can produce different execution paths, timing, and outcomes. Tests pass locally but fail in CI, or produce inconsistent results across runs. This undermines the core value proposition of reliable automated testing.

**Why it happens:**
LLMs generate probabilistic outputs. Browser-use agents interpret natural language tasks and make real-time decisions about which elements to click, what to type, and how to handle unexpected UI states. Temperature settings, token sampling, and context variations all contribute to variability.

**How to avoid:**
1. **Set temperature to 0** for test execution to maximize determinism
2. **Use caching strategies** (e.g., LangWatch caching) to lock in successful execution paths
3. **Run multiple trials** per test and track pass rate metrics rather than single-run pass/fail
4. **Implement threshold-based assertions** instead of exact matches (e.g., "element appears within 5 seconds" vs "element appears at exactly 3.2 seconds")
5. **Separate software bugs from AI flakiness** - track these as different categories

**Warning signs:**
- Same test passes 3/5 times with no code changes
- Test failures correlate with LLM provider latency spikes
- Execution step counts vary significantly between runs

**Phase to address:** Phase 1 (Core Flow) - establish deterministic patterns early

---

### Pitfall 2: SSE Connection Management During Long-Running AI Tasks

**What goes wrong:**
AI browser automation tasks can run for minutes. SSE connections drop mid-execution, causing:
- Frontend UI stuck in "loading" state
- Lost progress updates
- Browser instances left orphaned (memory leak)
- Database records in inconsistent states

**Why it happens:**
SSE has no built-in reconnection state recovery. Proxies/load balancers may timeout connections. Browser-use agents continue running even after clients disconnect. FastAPI BackgroundTasks don't automatically clean up when connections close.

**How to avoid:**
1. **Implement heartbeat events** every 15-30 seconds to keep connections alive
2. **Store all progress in database** immediately, not in memory - SSE is just notification, not state storage
3. **Use FastAPI lifespan events** for proper browser cleanup on server shutdown
4. **Add client-side reconnection logic** with event ID tracking to resume from last received event
5. **Monitor agent task status** - if client disconnects, either pause agent or mark run as "abandoned"

**Warning signs:**
- Frontend shows stale data after refresh
- Server memory grows over time (orphaned browser processes)
- Database shows "running" status for tasks that should be complete

**Phase to address:** Phase 1 (Core Flow) - SSE reliability is foundational

---

### Pitfall 3: SQLite Blocking the Async Event Loop

**What goes wrong:**
Under load (multiple concurrent test runs), the application becomes unresponsive. API requests queue up and timeout. Real-time SSE updates lag or stop entirely.

**Why it happens:**
SQLite is a file-based database with limited write concurrency. Using synchronous SQLAlchemy engines or blocking queries in async FastAPI handlers blocks the entire event loop - all requests suffer, not just database operations.

**How to avoid:**
1. **Always use async engine** with `aiosqlite` driver - never sync `create_engine()` in async apps
2. **Use connection pooling** (consider `aiosqlitepool` for better concurrency)
3. **Keep transactions short** - write immediately, don't hold transactions open during AI execution
4. **Consider write queue pattern** - queue writes to a single writer if high concurrency needed
5. **Test under concurrent load** early - SQLite limitations appear at 5-10 concurrent writes

**Warning signs:**
- API response time increases with concurrent users
- `RuntimeWarning: coroutine was never awaited` in logs
- Database operations work in isolation but fail during parallel test runs

**Phase to address:** Phase 1 (Core Flow) - database architecture is hard to change later

---

### Pitfall 4: Screenshot Storage Bloat in SQLite

**What goes wrong:**
Database file grows rapidly (each test run can generate 10-50 screenshots at 100KB-500KB each). Database queries slow down. Backups become unwieldy. SQLite file corruption risk increases.

**Why it happens:**
Storing binary blobs (screenshots) directly in SQLite is convenient but scales poorly. Each screenshot adds to database pages, increasing I/O for all queries. No easy way to clean up old screenshots without database operations.

**How to avoid:**
1. **Store screenshots as files** on disk (e.g., `data/screenshots/{run_id}/{step_num}.png`)
2. **Store only file paths in database** - keep database lean
3. **Implement retention policy** - delete screenshots after N days or after report generation
4. **Consider compression** for long-term storage
5. **Add cleanup job** that runs on server startup or scheduled interval

**Warning signs:**
- Database file > 100MB after a week of testing
- Simple queries taking > 100ms
- Backup/restore operations timing out

**Phase to address:** Phase 2 (Data Layer) - storage strategy affects data model

---

### Pitfall 5: Browser-Use Agent Memory Leak

**What goes wrong:**
Server memory consumption grows continuously. After running many tests, the server runs out of memory and crashes. Chromium processes accumulate even after tests complete.

**Why it happens:**
Browser-use creates Playwright browser instances that must be explicitly closed. If exceptions occur during execution, cleanup code may not run. Background tasks that error out may leave browser instances orphaned.

**How to avoid:**
1. **Always use context managers** (`async with Browser() as browser:`) for automatic cleanup
2. **Wrap agent execution in try/finally** with explicit browser.close()
3. **Implement process monitoring** - alert if Chromium processes exceed threshold
4. **Consider browser-use Cloud** for production to offload memory management
5. **Set maximum agent run time** to prevent runaway processes

**Warning signs:**
- `ps aux | grep chromium` shows many orphaned processes
- Server memory usage doesn't decrease after test runs complete
- OOM errors in server logs

**Phase to address:** Phase 1 (Core Flow) - resource cleanup is critical from day one

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Store screenshots in SQLite | Simpler code, single backup | Database bloat, slow queries, corruption risk | Never for production |
| Skip SSE heartbeat implementation | Faster initial development | Connection drops, poor UX, lost state | Prototyping only |
| Use sync database operations | Easier to understand | Blocks event loop, poor concurrency | Never in async FastAPI |
| Hard-code LLM temperature | Simpler configuration | Inconsistent test results, hard to debug | Never - always make configurable |
| Skip reconnection logic | Faster frontend development | Poor UX on long-running tests | MVP only, must add before production |
| No cleanup job for old data | Simpler ops | Disk fills up, database grows indefinitely | During active development only |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Browser-Use + Qwen | Using default temperature (0.7) | Set `temperature=0` for test determinism |
| FastAPI + SSE | Storing state in EventManager memory | Store state in database, SSE is just notification |
| SQLite + Async | Using sync engine `create_engine()` | Use `create_async_engine()` with `aiosqlite` |
| BackgroundTasks + DB | Not handling exceptions in background task | Wrap in try/except, always update run status |
| Playwright + Docker | Missing dependencies for Chromium | Install `playwright install-deps chromium` |
| SSE + Proxies | No timeout/heartbeat configuration | Add nginx proxy timeouts, implement heartbeats |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| No database connection pool | Latency spikes under load | Use `aiosqlitepool` or equivalent | 5+ concurrent test runs |
| Screenshots in database | Slow queries, large backups | Store as files, keep paths in DB | 100+ test runs |
| No browser instance limit | OOM crashes | Semaphore to limit concurrent browsers | Memory constrained environments |
| Unbounded event history | Memory leak in EventManager | Limit history size, use circular buffer | Long-running server |
| No query pagination | API timeouts on large datasets | Always paginate list endpoints | 1000+ records |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| ERP credentials in code | Credential exposure | Use environment variables, never commit |
| No input sanitization on task description | Prompt injection, unexpected agent behavior | Validate/sanitize user input before passing to LLM |
| Screenshots contain sensitive data | PII/credential leak in reports | Mask sensitive fields, implement screenshot redaction |
| No rate limiting on API | Resource exhaustion, cost overruns | Implement per-IP and per-user rate limits |
| LLM API key in frontend | Key theft, unauthorized usage | All LLM calls from backend only |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No progress indication during long runs | Users think app is frozen | Show step-by-step progress via SSE |
| Generic error messages | Users don't know what went wrong | Show specific error with suggested actions |
| No way to stop running test | Wasted resources, frustration | Implement stop/cancel functionality |
| Lost progress on page refresh | Users lose context | Persist state in database, restore on load |
| No execution history | Can't debug past failures | Keep run history with searchable filters |

## "Looks Done But Isn't" Checklist

- [ ] **SSE Updates:** Often missing reconnection logic -- verify client reconnects after network blip
- [ ] **Browser Cleanup:** Often missing on exception -- verify browser closes even when agent crashes
- [ ] **Database Status:** Often stuck in "running" -- verify status updates on all exit paths (success, error, cancel)
- [ ] **Screenshot Display:** Often broken paths -- verify frontend can actually load saved screenshots
- [ ] **Error Propagation:** Often swallowed in background tasks -- verify frontend shows backend errors
- [ ] **Concurrent Runs:** Often breaks at 2+ runs -- verify with multiple simultaneous test executions

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Screenshots in SQLite | HIGH | Export blobs to files, migrate schema, update all queries |
| No SSE heartbeats | MEDIUM | Add heartbeat endpoint, update frontend to track, deploy |
| Sync DB in async app | HIGH | Rewrite all database code with async patterns |
| Memory leak (browser) | MEDIUM | Add cleanup code, restart server to clear existing leaks |
| No cleanup job | LOW | Add scheduled cleanup, manually clean existing data |
| LLM non-determinism | MEDIUM | Add caching layer, adjust temperature, re-run tests |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| LLM Non-Determinism | Phase 1 (Core Flow) | Run same test 5 times, verify consistent behavior |
| SSE Connection Management | Phase 1 (Core Flow) | Test with network interruptions, verify reconnection |
| SQLite Event Loop Blocking | Phase 2 (Data Layer) | Load test with 10 concurrent runs, verify no blocking |
| Screenshot Storage Bloat | Phase 2 (Data Layer) | Run 100 tests, verify database size < 10MB |
| Browser Memory Leak | Phase 1 (Core Flow) | Run 50 tests, verify memory returns to baseline |
| Missing Error Handling | Phase 1 (Core Flow) | Simulate failures, verify cleanup and status updates |

## Sources

- [AI Agent Testing Pyramid - Block Engineering](https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents) - Distinguishes software flakiness vs AI-related flakiness
- [Testing AI Agents: Validating Non-Deterministic Behavior - SitePoint](https://www.sitepoint.com/testing-ai-agents-deterministic-evaluation-in-a-non-deterministic-world/) - Handling flakiness and score variance
- [SSE Not Production Ready - dev.to](https://dev.to/miketalbot/server-sent-events-are-still-not-production-ready-after-a-decade-a-lesson-for-me-a-warning-for-you-2gie) - SSE proxy/load balancer issues
- [The Hidden Risks of SSE - Medium](https://medium.com/@2957607810/the-hidden-risks-of-sse-server-sent-events-what-developers-often-overlook-14221a4b3bfe) - Scalability challenges with SSE
- [Async SQLAlchemy Engine in FastAPI - Medium](https://medium.com/@mojimich2015/async-sqlalchemy-engine-in-fastapi-the-guide-e5acdba75c99) - Don't block the event loop with sync engines
- [SQLite ALTER Limitations - Stack Overflow](https://stackoverflow.com/questions/30378233/sqlite-lack-of-alter-support-alembic-migration-failing-because-of-this-solutio) - Migration challenges with SQLite
- [Browser-Use GitHub Repository](https://github.com/browser-use/browser-use) - Official documentation and patterns
- [FastAPI Background Tasks + SSE Tutorial - dev.to](https://dev.to/zachary62/build-an-llm-web-app-in-python-from-scratch-part-4-fastapi-background-tasks-sse-21g4) - Pattern for combining BackgroundTasks with SSE
- [FastAPI Lifespan Events - Official Docs](https://fastapi.tiangolo.com/advanced/events/) - Proper cleanup on startup/shutdown
- [9 Production Realities for AI Agents - dev.to](https://dev.to/franciscohumarang/the-9-production-realities-for-ai-agents-a-guide-to-building-reliable-agents-from-a-flakestorm-4g1n) - Practical guide to handling "flakestorms"

---
*Pitfalls research for: AI-driven UI Testing Platform*
*Researched: 2026-03-14*
