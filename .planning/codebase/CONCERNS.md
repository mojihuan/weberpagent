# Codebase Concerns

**Analysis Date:** 2026-04-03

## Tech Debt

**Large file sizes:**
- Issue: Several files exceed ideal size limits
- Files:
  - `backend/api/routes/runs.py` (547 lines) - Full execution pipeline in single file
  - `backend/core/external_precondition_bridge.py` (51KB) - Complex external module integration
  - `backend/llm/config.py` (273 lines) - Config loading and validation
- Impact: Harder to maintain, harder to test
- Fix approach: Split into smaller modules by responsibility

**Legacy Agent Wrappers:**
- Issue: Multiple agent implementations (browser_agent.py, proxy_agent.py, monitored_agent.py)
- Files: `backend/agent/browser_agent.py`, `backend/agent/proxy_agent.py`, `backend/agent/monitored_agent.py`
- Impact: Confusion about which to use
- Fix approach: Deprecate old wrappers, document monitored_agent as primary

**Monolith Background Task:**
- Issue: `run_agent_background()` function handles entire pipeline
- File: `backend/api/routes/runs.py`
- Impact: Hard to test individual stages, long function
- Fix approach: Extract to `AgentOrchestrator` class

## Known Bugs

**No critical bugs identified in current analysis**

## Security Considerations

**API Keys via Environment:**
- Risk: Secrets in `.env` file, need to ensure gitignore
- Files: `.env`, `backend/config/settings.py`
- Current mitigation: `.env` not committed to git
- Recommendations: Document required env vars clearly

**Precondition Code Execution:**
- Risk: User-provided Python code executed via `exec()`
- Files: `backend/core/precondition_service.py`
- Current mitigation: Sandboxed with limited builtins, timeout
- Recommendations: Consider more restrictive sandbox or dedicated execution service

**No Rate Limiting:**
- Risk: API abuse, LLM API quota exhaustion
- Files: `backend/api/main.py`
- Current mitigation: None
- Recommendations: Add rate limiting middleware

## Performance Bottlenecks

**Sequential Precondition Execution:**
- Problem: Preconditions execute sequentially, not in parallel
- Files: `backend/api/routes/runs.py:91-142`
- Cause: Simple for-loop with await
- Improvement: Use `asyncio.gather()` for independent preconditions

**Screenshot Storage:**
- Problem: Screenshots saved synchronously during execution
- Files: `backend/core/agent_service.py:292-298`
- Impact: Adds latency to step callbacks
- Improvement: Queue screenshot saves for async processing

**LLM Retry Overhead:**
- Problem: 3 retries with exponential backoff can cause long waits
- Files: `backend/llm/factory.py:156-221`
- Impact: Up to 7 seconds delay on failures (1s + 2s + 4s)
- Improvement: Tune retry parameters, add circuit breaker

## Fragile Areas

**DOM Patch Compatibility:**
- Files: `backend/agent/dom_patch.py`
- Why fragile: Monkey-patches browser-use internals
- Safe modification: Test with browser-use version upgrades
- Risk: Browser-use updates may break patches

**Detector Configuration:**
- Files: `backend/agent/stall_detector.py`, `backend/agent/pre_submit_guard.py`
- Why fragile: Hardcoded thresholds (2 consecutive failures, 3 stagnant steps)
- Safe modification: Add configuration options
- Test coverage: Unit tests needed

**Context Variable Substitution:**
- Files: `backend/core/precondition_service.py:336-361`
- Why fragile: Jinja2 strict undefined mode can fail on missing variables
- Safe modification: Improve error messages, add validation
- Test coverage: Missing

## Scaling Limits

**SQLite Concurrency:**
- Current capacity: WAL mode supports concurrent reads, limited writes
- Limit: High write volume will cause lock contention
- Scaling path: Migrate to PostgreSQL for production

**SSE Memory:**
- Current capacity: EventManager stores all events in memory
- Limit: Long-running executions accumulate memory
- Scaling path: Implement event pagination, limit history

**Agent Step Count:**
- Current capacity: Default max_steps=10, configurable up to 100
- Limit: Very long tasks may timeout
- Scaling path: Add checkpoint/resume capability

## Dependencies at Risk

**browser-use:**
- Risk: Active development, breaking changes possible
- Impact: Agent execution depends on internal APIs
- Migration plan: Monitor releases, test before upgrades
- Version: 0.12.2+ currently used

**dashscope SDK:**
- Risk: Alibaba Cloud SDK, regional availability
- Impact: Primary LLM integration
- Migration plan: Abstract behind BaseLLM, support multiple providers

## Missing Critical Features

**Test Coverage:**
- Problem: No unit tests for detectors, services, or core logic
- Files: `backend/tests/` mostly empty
- Blocks: Safe refactoring
- Priority: High

**Checkpoint/Resume:**
- Problem: Long executions cannot resume after failure
- Files: `backend/core/agent_service.py`
- Blocks: Production reliability
- Priority: Medium

**LLM Cost Tracking:**
- Problem: No tracking of API usage or costs
- Files: `backend/llm/` not instrumented
- Blocks: Cost monitoring
- Priority: Low

## Test Coverage Gaps

**Detectors:**
- What's not tested: StallDetector, PreSubmitGuard, TaskProgressTracker
- Files: `backend/agent/stall_detector.py`, etc.
- Risk: Regression in stall detection logic
- Priority: High

**PreconditionService:**
- What's not tested: Variable substitution, context management
- Files: `backend/core/precondition_service.py`
- Risk: Wrong variable substitution
- Priority: High

**Event Streaming:**
- What's not tested: SSE connection management, reconnection
- Files: `backend/core/event_manager.py`
- Risk: Stream drops, missed events
- Priority: Medium

---

*Concerns audit: 2026-04-03*
