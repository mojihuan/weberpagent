# Domain Pitfalls

**Domain:** AI-driven UI automation testing platform
**Researched:** 2026-03-23

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: LLM Non-Determinism Causing Test Flakiness

**What goes wrong:** AI agents are inherently non-deterministic - the same test input can produce different execution paths, timing, and outcomes. Tests pass locally but fail in CI, or produce inconsistent results across runs. This undermines the core value proposition of reliable automated testing.

**Why it happens:** LLMs generate probabilistic outputs. Browser-use agents interpret natural language tasks and make real-time decisions about which elements to click, what to type, and how to handle unexpected UI states. Temperature settings, token sampling, and context variations all contribute to variability.

**Consequences:** Unreliable test results, wasted debugging time, loss of trust in automation

**Prevention:**
1. Set temperature to 0 for test execution to maximize determinism
2. Use caching strategies to lock in successful execution paths
3. Run multiple trials per test and track pass rate metrics rather than single-run pass/fail
4. Implement threshold-based assertions instead of exact matches
5. Separate software bugs from AI flakiness - track these as different categories

**Detection:**
- Same test passes 3/5 times with no code changes
- Test failures correlate with LLM provider latency spikes
- Execution step counts vary significantly between runs

---

### Pitfall 2: Over-Automation at UI Layer

**What goes wrong:** Teams try to automate everything at the UI layer, resulting in slow, brittle test suites that provide little value. More tests does not equal better quality.

**Why it happens:** UI automation is easy to visualize and demo, leading to over-investment. Teams skip the harder work of API-level testing and data validation.

**Consequences:** Slow CI pipelines, high maintenance cost, low signal-to-noise ratio

**Prevention:**
1. Follow the testing pyramid - more unit/integration tests, fewer UI tests
2. Use UI automation only for critical user journeys
3. Move data validation to API layer where possible
4. Implement precondition system for data setup instead of UI-driven preparation

**Detection:**
- Test suite takes > 30 minutes to run
- Flaky test rate > 20%
- Tests break frequently due to minor UI changes

---

### Pitfall 3: Missing Assertion Validation

**What goes wrong:** Tests execute successfully but don't actually verify the expected outcomes. AI agent completes the steps but the test passes even when the business logic is broken.

**Why it happens:** Relying solely on "no errors during execution" as success criteria. Missing explicit assertions for business requirements.

**Consequences:** False confidence in test results, bugs slip through to production

**Prevention:**
1. Require at least one assertion per test case
2. Implement multi-layer assertions (URL, text, API, business logic)
3. Use the platform's assertion system for comprehensive validation
4. Review assertion coverage during code review

**Detection:**
- Tests pass but manual verification shows failures
- Assertion count per test is 0 or very low
- No failed assertion results in reports

---

### Pitfall 4: SSE Connection Drops During Long-Running Tests

**What goes wrong:** AI browser automation tasks can run for minutes. SSE connections drop mid-execution, causing:
- Frontend UI stuck in "loading" state
- Lost progress updates
- Browser instances left orphaned (memory leak)
- Database records in inconsistent states

**Why it happens:** SSE has no built-in reconnection state recovery. Proxies/load balancers may timeout connections. Browser-use agents continue running even after clients disconnect.

**Consequences:** Poor user experience, resource leaks, inconsistent state

**Prevention:**
1. Implement heartbeat events every 15-30 seconds
2. Store all progress in database immediately, not in memory
3. Use FastAPI lifespan events for proper browser cleanup
4. Add client-side reconnection logic with event ID tracking

**Detection:**
- Frontend shows stale data after refresh
- Server memory grows over time (orphaned browser processes)
- Database shows "running" status for tasks that should be complete

---

### Pitfall 5: Screenshot Storage Bloat

**What goes wrong:** Database file grows rapidly (each test run can generate 10-50 screenshots at 100KB-500KB each). Database queries slow down. Backups become unwieldy.

**Why it happens:** Storing binary blobs (screenshots) directly in database is convenient but scales poorly.

**Consequences:** Slow queries, large backups, database corruption risk

**Prevention:**
1. Store screenshots as files on disk
2. Store only file paths in database
3. Implement retention policy - delete old screenshots
4. Add cleanup job that runs periodically

**Detection:**
- Database file > 100MB after a week of testing
- Simple queries taking > 100ms
- Backup/restore operations timing out

---

## Moderate Pitfalls

### Pitfall 1: SQLite Event Loop Blocking

**What goes wrong:** Under load (multiple concurrent test runs), the application becomes unresponsive. API requests queue up and timeout.

**Prevention:**
1. Always use async engine with aiosqlite driver
2. Use connection pooling
3. Keep transactions short
4. Test under concurrent load early

---

### Pitfall 2: Browser Instance Memory Leaks

**What goes wrong:** Server memory consumption grows continuously. After running many tests, the server runs out of memory and crashes.

**Prevention:**
1. Always use context managers for browser instances
2. Wrap agent execution in try/finally with explicit cleanup
3. Implement process monitoring
4. Set maximum agent run time

---

### Pitfall 3: Hardcoded Configuration

**What goes wrong:** API URLs, credentials, and paths hardcoded in code. Application breaks in different environments.

**Prevention:**
1. Use environment variables for all configuration
2. Provide .env.example template
3. Validate configuration at startup

---

### Pitfall 4: Inconsistent Error Handling

**What goes wrong:** Some endpoints return HTTPException, others return error dicts. Frontend can't handle errors consistently.

**Prevention:**
1. Always use HTTPException with consistent format
2. Define standard error response structure
3. Document error codes

---

## Minor Pitfalls

### Pitfall 1: Missing Database Migrations

**What goes wrong:** Schema changes applied manually. Team members have inconsistent database schemas.

**Prevention:** Use Alembic for migrations (v0.2+)

---

### Pitfall 2: No Input Sanitization

**What goes wrong:** User input passed directly to LLM without validation. Prompt injection or unexpected agent behavior.

**Prevention:** Validate and sanitize all user input before passing to LLM

---

### Pitfall 3: Generic Error Messages

**What goes wrong:** Error messages like "Something went wrong" don't help users understand or fix the issue.

**Prevention:** Provide specific error messages with suggested actions

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|----------------|------------|
| Core Flow | LLM non-determinism | Set temperature=0, implement retry logic |
| Real-time Monitoring | SSE connection drops | Add heartbeats, store state in DB |
| Data Layer | SQLite blocking | Use async engine, test concurrent load |
| Precondition System | Missing config/settings.py | Document setup, provide template |
| External Integration | Import failures | Use bridge module with error handling |
| Assertion System | Missing validation | Require assertions, multi-layer checks |
| Reporting | Screenshot bloat | Store files on disk, implement retention |

## Sources

### Primary (HIGH confidence)
- [AI Agent Testing Pyramid - Block Engineering](https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents) - Distinguishes software flakiness vs AI-related flakiness
- [Testing AI Agents: Validating Non-Deterministic Behavior](https://www.sitepoint.com/testing-ai-agents-deterministic-evaluation-in-a-non-deterministic-world/) - Handling flakiness
- [Test Automation Challenges 2026](https://medium.com/@arnabroyy/top-9-challenges-in-automation-testing-2026-e3f4c2e538f8) - Common pitfalls
- [Test Automation Trends 2026](https://www.testdevlab.com/blog/test-automation-trends-2026) - Industry direction
- [SSE Production Considerations](https://dev.to/miketalbot/server-sent-events-are-still-not-production-ready-after-a-decade) - SSE reliability issues

### Secondary (MEDIUM confidence)
- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices) - Architecture patterns
- [Async SQLAlchemy in FastAPI](https://medium.com/@mojimoch2015/async-sqlalchemy-engine-in-fastapi-the-guide-e5acdba75c99) - Database patterns
- [Software Testing Trends 2026](https://www.testresults.io/articles/software-testing-trends-for-enterprises-in-2026-whats-broken-whats-next) - Industry analysis

---
*Pitfalls research for: AI-driven UI Testing Platform*
*Researched: 2026-03-23*
