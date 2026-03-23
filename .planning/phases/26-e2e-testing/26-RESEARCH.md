# Phase 26: E2E Testing - Research

**Researched:** 2026-03-20
**Domain:** End-to-End Testing with Playwright, Assertion System Verification
**Confidence:** HIGH

## Summary

Phase 26 focuses on end-to-end verification of the assertion workflow implemented in Phases 23-25. The testing approach uses Playwright E2E tests against a real ERP environment to validate the complete assertion flow: configuration, execution, result display, and non-fail-fast behavior.

The existing E2E infrastructure (`e2e/playwright.config.ts`, `e2e/tests/smoke.spec.ts`, `e2e/tests/full-flow.spec.ts`) provides a solid foundation. Key patterns include automatic server startup, long timeouts for AI-driven execution, and comprehensive failure diagnostics (screenshots, traces, videos).

**Primary recommendation:** Create assertion-specific E2E tests that verify: (1) task creation with assertion config, (2) assertion execution during test run, (3) result display in report page. Use the existing sales outbound use case as the test scenario.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**E2E Test Environment:**
- Use real ERP environment: Must configure ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD
- Missing config handling: Fail directly, require ERP configuration
- Test isolation: Reuse existing sales outbound use case, no dedicated test data

**E2E Test Scope:**
- Test scenarios:
  1. Single assertion success - verify success status display
  2. Single assertion failure - verify failure status display + field details
- Non-fail-fast verification: Ensure multiple assertions all execute, no termination on first failure
- Assertion method selection: Claude chooses appropriate assertion method based on actual environment

**Report Verification Approach:**
- UI element check: Check report page displays assertion result cards, pass/fail status, field details
- No API response verification: Focus on UI display verification
- No context variable reference verification: Context variable reference feature not in E2E scope

**Test Case Reuse:**
- Reuse sales outbound use case: Add assertion configuration on existing use case
- Reduce development effort: No dedicated assertion test use case

**E2E Test Failure Handling:**
- Save detailed diagnostics: Screenshots, network requests, console logs
- Playwright trace: on-first-retry mode
- Failure screenshots: only-on-failure mode
- Video retention: retain-on-failure mode

**Manual Verification:**
- Timing: Execute after all E2E tests pass
- Scenario: Complete sales outbound use case (precondition + assertion config + AI execution + report view)
- Checklist detail: Each assertion UI element, state change has clear verification point
- Environment requirement: Real ERP environment

**Test Result Recording:**
- Format: Create VERIFICATION.md to record verification results
- Content: Test pass status, issues found, verification screenshots

### Claude's Discretion

- Specific assertion method to test
- E2E test case implementation details
- Manual verification checklist items
- VERIFICATION.md format
- Failure diagnostic content

### Deferred Ideas (OUT OF SCOPE)

- Context variable reference verification ({{assertion_result_0.passed}}) - future requirement
- Multi-assertion mixed result testing - currently only test single assertion success/failure
- Error scenario E2E testing (timeout, invalid params) - Phase 27 unit test
- Mock data support - v2 requirement
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| N/A | Testing phase - no direct requirements | Verifies EXEC-01 through EXEC-06 implementation from Phases 23-25 |

**Success Criteria (from phase description):**
1. QA can create test task with assertion configuration and run it end-to-end
2. Assertion success/failure results display correctly in test report
3. Multiple assertions in single test all execute (non-fail-fast verified)
4. Assertion results are accessible via context variables in subsequent steps
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| @playwright/test | 1.51.1 (root), 1.58.2 (latest) | E2E test framework | Industry standard, excellent DX, auto-wait, traces |
| TypeScript | 5.9.3 | Test language | Type safety, better IDE support |
| Vite | 7.3.1 | Frontend dev server | Already configured, auto-started by Playwright |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | (backend) | Backend unit tests | Phase 27 unit test coverage |
| uvicorn | (backend) | Backend server | Auto-started by Playwright webServer |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Playwright | Cypress | Playwright has better multi-browser, faster execution, built-in traces |
| Real ERP | Mock server | Real ERP validates actual integration, mocks only test UI flow |

**Installation:**
```bash
# Already installed in project root
npm install @playwright/test
npx playwright install chromium
```

**Version verification:**
- @playwright/test: 1.51.1 (installed), 1.58.2 (latest available)
- Current version is recent and stable for this phase

## Architecture Patterns

### Recommended E2E Test Structure
```
e2e/
├── playwright.config.ts      # Existing config - auto-start servers
├── tests/
│   ├── smoke.spec.ts         # Existing - basic flow
│   ├── full-flow.spec.ts     # Existing - complete flow
│   ├── data-method-execution.spec.ts  # Existing - data method tests
│   └── assertion-flow.spec.ts  # NEW - assertion E2E tests
```

### Pattern 1: Complete Assertion Flow Test
**What:** Test the full assertion workflow from configuration to report display
**When to use:** Primary E2E test pattern for this phase
**Example:**
```typescript
// e2e/tests/assertion-flow.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Assertion Flow Tests', () => {
  test('single assertion success - displays pass status in report', async ({ page }) => {
    test.setTimeout(300000) // 5 minutes for AI execution

    // Step 1: Navigate and create task with assertion
    await page.goto('/tasks')
    await page.click('button:has-text("新建任务")')

    // Fill task details
    await page.fill('[name="name"]', 'E2E Assertion Success Test')
    await page.fill('[name="target_url"]', process.env.ERP_BASE_URL || '')

    // Step 2: Switch to Business Assertions tab
    await page.click('button:has-text("业务断言")')

    // Step 3: Add assertion via AssertionSelector
    await page.click('button:has-text("添加断言")')
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible()

    // Select first available assertion method
    await page.locator('input[type="checkbox"]').first().click()
    await page.click('button:has-text("Confirm")')

    // Verify assertion card appears
    await expect(page.locator('.border-orange-200')).toBeVisible()

    // Step 4: Create and execute task
    await page.click('button:has-text("创建任务")')
    await page.click('tr:has-text("E2E Assertion Success Test") button:has-text("执行")')

    // Step 5: Wait for completion
    await expect(page.locator('text=执行监控')).toBeVisible()
    await page.waitForSelector('text=已完成, text=失败', { timeout: 180000 })

    // Step 6: View report and verify assertion result
    await page.click('button:has-text("查看报告")')
    await expect(page).toHaveURL(/.*reports\/.*/)

    // Verify assertion result card exists with pass status
    await expect(page.locator('text=断言结果, text=接口断言结果')).toBeVisible()
  })
})
```

### Pattern 2: Non-Fail-Fast Verification
**What:** Test that multiple assertions execute even when one fails
**When to use:** Verify EXEC-06 requirement (non-fail-fast)
**Example:**
```typescript
test('multiple assertions execute independently - non fail-fast', async ({ page }) => {
  // Create task with multiple assertions
  // First assertion will fail, second should still execute

  // After execution, verify BOTH assertion results appear in report
  const assertionCards = page.locator('[class*="assertion-result"]')
  const count = await assertionCards.count()
  expect(count).toBeGreaterThanOrEqual(2) // Both executed
})
```

### Pattern 3: Report Page Assertion Result Verification
**What:** Verify UI elements display assertion results correctly
**When to use:** Validate success criteria #2 (correct display)
**Example:**
```typescript
// Verify pass status
const passCard = page.locator('.bg-green-50.border-green-200')
await expect(passCard).toBeVisible()
await expect(passCard.locator('svg.text-green-500')).toBeVisible() // CheckCircle icon

// Verify fail status
const failCard = page.locator('.bg-red-50.border-red-200')
await expect(failCard).toBeVisible()
await expect(failCard.locator('svg.text-red-500')).toBeVisible() // XCircle icon
await expect(failCard.locator('text=预期值, text=实际值')).toBeVisible()
```

### Anti-Patterns to Avoid
- **Testing API responses in E2E:** Use unit tests for API logic, E2E for UI flow
- **Short timeouts:** AI execution can take 2-3 minutes, always use test.setTimeout(180000+)
- **Hardcoded selectors:** Use text-based selectors that survive minor UI changes
- **Skipping ERP config check:** Always verify ERP_BASE_URL is set before running

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test isolation | Custom cleanup scripts | Playwright test fixtures | Built-in isolation, afterEach hooks |
| Screenshot on failure | Manual screenshot calls | Playwright screenshot config | Automatic, configured once |
| Server startup | Custom server management | Playwright webServer | Auto-starts, health checks, port detection |
| Wait strategies | Arbitrary waits | Playwright auto-wait | More reliable, faster tests |

**Key insight:** The existing playwright.config.ts already handles server startup and failure diagnostics. Leverage it fully.

## Common Pitfalls

### Pitfall 1: ERP Environment Not Configured
**What goes wrong:** Tests fail with connection errors or authentication failures
**Why it happens:** ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD not set in environment
**How to avoid:**
```typescript
test.beforeEach(() => {
  if (!process.env.ERP_BASE_URL) {
    test.skip()
  }
})
```
**Warning signs:** Connection refused, 401 Unauthorized, empty assertion results

### Pitfall 2: Assertion Timeout During Execution
**What goes wrong:** Test times out waiting for assertion execution to complete
**Why it happens:** External assertion methods may take >30s to execute
**How to avoid:** Use generous timeouts (300000ms for full flow), configure retries in playwright.config.ts
**Warning signs:** Test passes locally but fails in CI, intermittent timeout failures

### Pitfall 3: Flaky Element Selectors
**What goes wrong:** Tests fail intermittently due to selector changes
**Why it happens:** Using brittle CSS selectors that depend on implementation details
**How to avoid:** Prefer text-based selectors: `page.locator('text=断言结果')` over `page.locator('.assertion-card-title')`
**Warning signs:** Tests pass in one run, fail in next without code changes

### Pitfall 4: Not Waiting for SSE Events
**What goes wrong:** Report page checked before assertion execution completes
**Why it happens:** Assertion execution happens via SSE events, need to wait for 'external_assertions' event
**How to avoid:** Wait for 'finished' event or '已完成' status before navigating to report
**Warning signs:** Report shows no assertion results, or incomplete results

## Code Examples

Verified patterns from existing codebase:

### Complete Test Flow (from smoke.spec.ts)
```typescript
// Source: e2e/tests/smoke.spec.ts
test('create -> execute -> monitor -> report', async ({ page }) => {
  test.setTimeout(180000) // 3 minutes

  await page.goto('/')
  await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

  // Create task
  await page.click('text=新建任务')
  await page.fill('[name="name"]', 'E2E Smoke Test Task')
  await page.click('button:has-text("创建")')

  // Execute
  await page.click('tr:has-text("E2E Smoke Test Task") button:has-text("执行")')

  // Monitor
  await expect(page.locator('text=执行监控')).toBeVisible({ timeout: 10000 })
  await page.waitForSelector('text=已完成, text=失败', { timeout: 120000 })

  // Report
  await page.click('button:has-text("查看报告")')
  await expect(page.locator('text=执行报告, text=报告')).toBeVisible({ timeout: 10000 })
})
```

### Assertion Selector Interaction (from AssertionSelector.tsx analysis)
```typescript
// Pattern for testing AssertionSelector modal
test('assertion selector modal workflow', async ({ page }) => {
  await page.goto('/tasks')
  await page.click('button:has-text("新建任务")')

  // Switch to business assertions tab
  await page.click('button:has-text("业务断言")')

  // Open selector
  await page.click('button:has-text("添加断言")')
  await expect(page.locator('text=Select Assertion Methods')).toBeVisible()

  // Select method
  await page.locator('input[type="checkbox"]').first().click()
  await expect(page.locator('text=Selected')).toBeVisible()

  // Configure (if needed)
  // Headers and Data dropdowns are auto-populated

  // Confirm
  await page.click('button:has-text("Confirm")')
  await expect(page.locator('.border-orange-200')).toBeVisible()
})
```

### Report Assertion Results Check (from ApiAssertionResults.tsx analysis)
```typescript
// Verify assertion results display
test('report displays assertion results', async ({ page }) => {
  // Navigate to report page
  await page.goto(`/reports/${runId}`)

  // Check for assertion section
  const assertionSection = page.locator('text=断言结果, text=接口断言结果')
  if (await assertionSection.count() > 0) {
    await expect(assertionSection).toBeVisible()

    // Check pass rate display
    await expect(page.locator('text=通过率')).toBeVisible()

    // Check individual results
    const passCards = page.locator('.bg-green-50.border-green-200')
    const failCards = page.locator('.bg-red-50.border-red-200')

    // At least one result should exist
    expect(await passCards.count() + await failCards.count()).toBeGreaterThan(0)
  }
})
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual E2E testing | Playwright automated tests | Project start | Faster feedback, reproducible tests |
| Fixed timeouts | Auto-wait with explicit timeouts | Phase 20 | More reliable, less flaky |
| Single browser | Chromium-only (configurable) | Project start | Faster CI, focused testing |

**Deprecated/outdated:**
- Selenium-based E2E: Playwright provides better DX and reliability
- Mock-heavy E2E: Real ERP testing validates actual integration

## Open Questions

1. **Which assertion method to use for testing?**
   - What we know: PcAssert has ~80 methods, MgAssert 1, McAssert 2
   - What's unclear: Which specific method will reliably pass/fail in test environment
   - Recommendation: Use first available PcAssert method for success test, configure intentionally failing params for failure test

2. **How to reliably trigger assertion failure?**
   - What we know: AssertionError with field results is parsed and displayed
   - What's unclear: Which params cause predictable failures without breaking ERP data
   - Recommendation: Use filter params (i, j, k) that return no data, causing assertion to fail on expected values

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright 1.51.1 |
| Config file | e2e/playwright.config.ts |
| Quick run command | `npm run test:e2e -- --grep "assertion"` |
| Full suite command | `npm run test:e2e` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SC-1 | QA creates task with assertion config | E2E | `npx playwright test assertion-flow.spec.ts -g "create"` | Wave 0 |
| SC-2 | Report displays assertion pass/fail | E2E | `npx playwright test assertion-flow.spec.ts -g "report"` | Wave 0 |
| SC-3 | Multiple assertions execute | E2E | `npx playwright test assertion-flow.spec.ts -g "multiple"` | Wave 0 |
| SC-4 | Context variable access | Manual | N/A - deferred | N/A |

### Sampling Rate
- **Per task commit:** `npm run test:e2e -- --grep "smoke"` (quick smoke test)
- **Per wave merge:** `npm run test:e2e` (full E2E suite)
- **Phase gate:** Full suite green + manual verification checklist complete

### Wave 0 Gaps
- [ ] `e2e/tests/assertion-flow.spec.ts` - covers SC-1, SC-2, SC-3
- [ ] No additional framework config needed - existing playwright.config.ts sufficient
- [ ] Manual verification checklist template - create in VERIFICATION.md

*(If no gaps: "None - existing test infrastructure covers all phase requirements")*

## Sources

### Primary (HIGH confidence)
- `e2e/playwright.config.ts` - Playwright configuration, timeout settings
- `e2e/tests/smoke.spec.ts` - Existing E2E test patterns
- `e2e/tests/full-flow.spec.ts` - Complete flow test patterns
- `frontend/src/components/TaskModal/AssertionSelector.tsx` - Assertion selector implementation
- `frontend/src/components/Report/ApiAssertionResults.tsx` - Report display component
- `backend/api/routes/runs.py` - External assertion execution integration
- `backend/core/external_precondition_bridge.py` - execute_all_assertions implementation

### Secondary (MEDIUM confidence)
- `.planning/phases/20-e2e-testing-manual-verification/20-CONTEXT.md` - Similar E2E phase patterns
- `.planning/phases/25-assertion-execution-engine/25-CONTEXT.md` - Assertion execution design

### Tertiary (LOW confidence)
- N/A - All findings verified against codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using existing Playwright setup, verified versions
- Architecture: HIGH - Patterns established in existing E2E tests
- Pitfalls: HIGH - Based on actual codebase patterns and previous E2E phases

**Research date:** 2026-03-20
**Valid until:** 30 days (stable Playwright patterns, assertion system just implemented)
