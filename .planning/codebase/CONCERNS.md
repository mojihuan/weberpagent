# Codebase Concerns

**Analysis Date:** 2026-03-14

## Tech Debt

**Hardcoded credentials in config files:**
- Issue: Password hardcoded in `backend/config/test_targets.yaml`
- Files: `[backend/config/test_targets.yaml:11]`
- Impact: Security risk if configuration is committed
- Fix approach: Move to environment variables or secure config system

**Large file sizes:**
- Issue: Several files exceed ideal size limits (200-400 lines)
- Files:
  - `[backend/api/routes/runs.py]` (298 lines) - Consider splitting into smaller modules
  - `[backend/llm/config.py]` (272 lines) - Consider extracting validation logic
  - `[backend/llm/openai.py]` (265 lines) - Consider separating concerns
- Impact: Harder to maintain and understand
- Fix approach: Extract smaller modules, separate concerns (validation, API calls, etc.)

**Broad exception handling:**
- Issue: Missing proper error handling in repository pattern
- Files: `[backend/db/repository.py]`
- Impact: Silent failures, hard to debug issues
- Fix approach: Add specific exception handling and proper error propagation

## Known Bugs

**Memory view error in browser automation:**
- Symptoms: Memory type conversion errors during screenshot processing
- Files: `[backend/utils/screenshot.py]` (not fully inspected)
- Trigger: Occurs during browser automation steps
- Workaround: Debug logs enabled in `backend/api/main.py`
- Status: Documented in `docs/troubleshooting/memoryview-error-fix.md`

**Missing exception handling in repository:**
- Symptoms: Potential silent failures in database operations
- Files: `[backend/db/repository.py]`
- Trigger: When database operations fail unexpectedly
- Workaround: None identified
- Priority: High - could lead to data integrity issues

## Security Considerations

**Hardcoded password exposure:**
- Risk: Test credentials committed to version control
- Files: `[backend/config/test_targets.yaml]`
- Current mitigation: Only in test config, not production
- Recommendations:
  - Move to environment variables
  - Use secret management system
  - Add to .gitignore if not already

**Environment variable management:**
- Risk: Multiple API keys handled through env vars (DASHSCOPE_API_KEY, OPENAI_API_KEY)
- Files: `[backend/llm/config.py]`, `[backend/api/routes/runs.py]`
- Current mitigation: Proper env var checks
- Recommendations: Centralize config management, add validation

**File system access:**
- Risk: Screenshots stored locally without encryption
- Files: `[backend/data/screenshots/]`
- Current mitigation: Directory access restricted
- Recommendations: Consider secure storage for sensitive screenshots

## Performance Bottlenecks

**Synchronous database operations:**
- Problem: Repository pattern lacks proper error handling
- Files: `[backend/db/repository.py]`
- Cause: No transaction rollback or error propagation
- Improvement path: Add proper exception handling and session management

**Large max_steps values in tests:**
- Problem: Some tests use high step counts (25-30)
- Files: `[backend/tests/test_delivery_form.py:114]`, `[backend/tests/test_purchase_e2e.py:62]`
- Cause: Complex scenarios require more steps
- Improvement path: Optimize test scenarios, reduce where possible

**In-memory storage:**
- Problem: Task and run storage uses JSON files
- Files: `[backend/data/tasks.json]`, `[backend/data/runs.json]`
- Cause: Simple file-based persistence
- Improvement path: Migrate to proper database for production

## Fragile Areas

**Browser automation dependency:**
- Files: `[backend/agent/browser_agent.py]`, `[backend/agent/proxy_agent.py]`
- Why fragile: Heavy reliance on external browser automation libraries
- Safe modification: Test thoroughly with different page structures
- Test coverage: Present but may not cover all edge cases

**LLM integration layer:**
- Files: `[backend/llm/factory.py]`, `[backend/llm/base.py]`
- Why fragile: Multiple LLM providers with different APIs
- Safe modification: Use factory pattern, add abstraction layer
- Test coverage: Good coverage of LLM switching

**Event streaming:**
- Files: `[backend/api/routes/runs.py]`, `[backend/core/event_manager.py]`
- Why fragile: Real-time event delivery can fail
- Safe modification: Add retry logic and error recovery
- Test coverage: Limited e2e testing of streaming

## Scaling Limits

**File-based storage:**
- Current capacity: Small JSON files
- Limit: Not scalable for production traffic
- Scaling path: Migrate to SQLite or PostgreSQL already configured

**In-memory task management:**
- Current capacity: Limited by server memory
- Limit: Single process limitation
- Scaling path: Add proper queue system (Celery or similar)

**Screenshot storage:**
- Current capacity: Local filesystem
- Limit: Storage space and access speed
- Scaling path: Cloud storage integration

## Dependencies at Risk

**browser-use:**
- Risk: Heavy dependency on specific browser automation library
- Impact: Core functionality relies on this package
- Migration plan: Evaluate alternative browser automation frameworks

**FastAPI + SQLAlchemy:**
- Risk: Version compatibility issues
- Impact: API layer and database access
- Migration plan: Keep updated, test compatibility before upgrades

## Missing Critical Features

**Input validation:**
- Problem: Limited validation on API endpoints
- Files: `[backend/api/schemas/index.py]`
- Blocks: Preventing invalid requests
- Priority: High - security and data integrity

**Rate limiting:**
- Problem: No rate limiting on API endpoints
- Files: `[backend/api/main.py]`
- Blocks: API abuse prevention
- Priority: Medium - production readiness

**Monitoring and observability:**
- Problem: Limited metrics and logging
- Files: `[backend/utils/logger.py]`
- Blocks: Performance monitoring and debugging
- Priority: Medium - operational readiness

## Test Coverage Gaps

**Error handling paths:**
- What's not tested: Database failure scenarios
- Files: `[backend/db/repository.py]`
- Risk: Silent failures in data operations
- Priority: High - data integrity

**Browser error scenarios:**
- What's not tested: Page loading failures, element not found
- Files: `[backend/agent/browser_agent.py]`
- Risk: Automation failures not properly handled
- Priority: Medium - reliability

**Configuration validation:**
- What's not tested: Invalid LLM configurations
- Files: `[backend/llm/config.py]`
- Risk: Invalid configs causing runtime errors
- Priority: Medium - robustness

---

*Concerns audit: 2026-03-14*
