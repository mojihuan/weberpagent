# Deferred Items - Phase 20

## E2E Test Infrastructure Issue

**Issue:** Playwright webServer configuration not starting frontend/backend servers automatically.

**Symptoms:**
- All E2E tests fail with `net::ERR_CONNECTION_REFUSED at http://localhost:5173`
- Existing smoke.spec.ts also fails with same error
- webServer timeout (30s) may not be sufficient for uv/npm startup

**Workaround:** Start servers manually before running E2E tests:
```bash
# Terminal 1: Start backend
uv run uvicorn backend.api.main:app --port 8080

# Terminal 2: Start frontend
cd frontend && npm run dev

# Terminal 3: Run tests
cd e2e && npx playwright test
```

**Scope:** This is a pre-existing infrastructure issue, not caused by 20-01 changes.
Deferred to Phase 22 (bug fixes) or separate infrastructure task.

**Date:** 2026-03-19
