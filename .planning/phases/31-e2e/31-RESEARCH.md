# Phase 31: E2E Testing - Research

**Researched:** 2026-03-22
**Domain:** Playwright E2E Testing, Three-Layer Assertion Parameters, "now" Time Conversion
**Confidence:** HIGH

## Summary

This phase extends existing E2E tests in `e2e/tests/assertion-flow.spec.ts` to cover v0.4.1 features: three-layer parameter structure (data/api_params/field_params) and "now" time conversion. The research confirms that existing E2E patterns are well-established and can be directly extended without architectural changes.

**Primary recommendation:** Extend `assertion-flow.spec.ts` with 3 new test cases following the established pattern: skip if no ERP env vars, 5-minute timeout, create task -> configure assertion with field_params -> execute -> verify report display.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Use real ERP environment (requires ERP_BASE_URL environment variable)
- **D-02:** Do NOT implement Mock ERP mode (different from ROADMAP.md original plan)
- **D-03:** Skip tests when environment variables are missing (test.skip), consistent with Phase 26
- **D-04:** Extend existing assertion-flow.spec.ts, do NOT create new files
- **D-05:** Add 3 new test cases to cover v0.4.1 functionality
- **D-06:** Reuse existing test pattern (create task -> configure assertion -> execute -> view report)
- **D-07:** field_params configuration test - configure field_params in UI (e.g., statusStr='done'), verify correct transmission
- **D-08:** "now" time conversion test - configure time field as "now", verify assertion passes
- **D-09:** Assertion success scenario - verify all fields pass, result shows passed: true
- **D-10:** Verify results through UI (report page), NOT direct API response checks
- **D-11:** Verify assertion result card displays green (bg-green-50 border-green-200)
- **D-12:** Verify field-level details display correctly (name/expected/actual/passed)

### Claude's Discretion
- **D-13:** Specific assertion method to use for testing
- **D-14:** Test case implementation details
- **D-15:** Timeout settings (5 minutes recommended, consistent with existing tests)
- **D-16:** Failure diagnostic message format

### Deferred Ideas (OUT OF SCOPE)
- Mock ERP mode - using real ERP instead
- Assertion failure scenario tests - already covered in existing tests
- Parallel assertion execution tests - already have multiple assertions test
- API response verification - only verify through UI

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| E2E-01 | Complete assertion flow test (configure -> execute -> result display), using real ERP | Existing `assertion-flow.spec.ts` provides full pattern; extend with field_params configuration via FieldParamsEditor component |
| E2E-02 | Test both assertion success and failure scenarios | Existing tests cover failure; add new tests for field_params success and "now" conversion success |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| @playwright/test | ^1.40.0 | E2E testing framework | Project standard, auto-starts servers, trace/screenshot/video support |
| playwright | ^1.40.0 | Browser automation | Paired with @playwright/test |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| typescript | ^5.x | Test file type safety | All E2E test files |

**Installation:**
```bash
cd e2e && npm install
```

**Version verification:** Already installed in project. Run `cd e2e && npm list @playwright/test` to verify.

## Architecture Patterns

### Recommended Project Structure
```
e2e/
├── tests/
│   ├── assertion-flow.spec.ts  # EXTEND THIS FILE (5 existing tests + 3 new tests)
│   └── smoke.spec.ts           # Reference for basic patterns
├── playwright.config.ts        # Existing config (120s timeout, auto webServer)
└── package.json
```

### Pattern 1: E2E Test Structure (Established)
**What:** Standard test pattern used across all assertion-flow tests
**When to use:** All new E2E tests must follow this pattern
**Example:**
```typescript
// Source: e2e/tests/assertion-flow.spec.ts
test('field_params configuration test', async ({ page }) => {
  // 1. Skip if no ERP environment
  test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')

  // 2. Set timeout for AI-driven execution
  test.setTimeout(300000) // 5 minutes

  // 3. Navigate to tasks and create new task
  await page.goto('/tasks')
  await page.click('button:has-text("New Task")')

  // 4. Fill form and switch to Business Assertions tab
  await page.fill('[name="name"]', 'E2E Field Params Test')
  await page.fill('[name="target_url"]', erpBaseUrl!)
  await page.click('button:has-text("业务断言")')

  // 5. Add assertion and configure field_params
  // ... (see FieldParamsEditor interaction below)

  // 6. Execute and wait for completion
  // ... (standard execution pattern)

  // 7. Verify report displays correct results
  // ... (check bg-green-50 border-green-200)
})
```

### Pattern 2: FieldParamsEditor Interaction
**What:** How to interact with the FieldParamsEditor component in E2E tests
**When to use:** When configuring field_params in assertion selector
**Example:**
```typescript
// After selecting assertion method, field_params section appears
// FieldParamsEditor component structure:
// - Search input with placeholder "Search fields..."
// - Accordion groups (click to expand)
// - Checkboxes for field selection
// - Input field for expected value
// - "now" button for time fields

// 1. Wait for fields to load
await page.waitForTimeout(2000)

// 2. Search for a field (optional)
const searchInput = page.locator('input[placeholder*="Search"]')
await searchInput.fill('status')

// 3. Expand a group if needed
await page.click('button:has-text("通用字段")')

// 4. Select a field checkbox
await page.check('input[type="checkbox"]')

// 5. Fill expected value
const valueInput = page.locator('input[placeholder="Expected value"]')
await valueInput.fill('已完成')

// 6. For time fields, click "now" button
const nowButton = page.locator('button:has-text("now")')
await nowButton.click()
```

### Pattern 3: Report Result Verification
**What:** How to verify assertion results in report page
**When to use:** All tests that need to verify assertion result display
**Example:**
```typescript
// Source: ReportDetail.tsx, ApiAssertionResults.tsx
// Navigate to report page
await page.click('button:has-text("查看报告")')
await expect(page).toHaveURL(/.*reports\/.*/)

// Check for API assertion results section
await expect(page.locator('text=接口断言结果')).toBeVisible()

// Verify green success card (bg-green-50 border-green-200)
const successCard = page.locator('.bg-green-50.border-green-200')
await expect(successCard).toBeVisible()

// Verify red failure card (bg-red-50 border-red-200)
const failCard = page.locator('.bg-red-50.border-red-200')

// Check pass rate display
await expect(page.locator('text=通过率')).toBeVisible()
```

### Anti-Patterns to Avoid
- **Creating new test files:** Must extend existing assertion-flow.spec.ts per D-04
- **Using Mock ERP:** Must use real ERP per D-01, D-02
- **Direct API verification:** Must verify through UI per D-10
- **Short timeouts:** AI execution needs 5 minutes, not default 2 minutes

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test server startup | Custom server management | `webServer` in playwright.config.ts | Already configured, auto-starts uvicorn + npm run dev |
| Failure diagnostics | Custom screenshot logic | `trace: 'on-first-retry'`, `screenshot: 'only-on-failure'` | Built-in Playwright features |
| ERP environment detection | Custom validation | `test.skip(!erpBaseUrl, ...)` | Established pattern in existing tests |

**Key insight:** All infrastructure is already in place. Just extend existing test file with new test cases.

## Common Pitfalls

### Pitfall 1: FieldParamsEditor Loading Timing
**What goes wrong:** Fields API call takes time, checkboxes not immediately available
**Why it happens:** FieldParamsEditor fetches fields from `/api/external-assertions/fields` on mount
**How to avoid:** Add `await page.waitForTimeout(2000)` after opening assertion selector modal
**Warning signs:** `await page.check('input[type="checkbox"]')` fails with "element not found"

### Pitfall 2: Time Field "now" Button Not Visible
**What goes wrong:** "now" button only appears for time fields (is_time_field=true)
**Why it happens:** Backend determines time fields from AST parsing, not all fields have this flag
**How to avoid:** Search for known time fields (e.g., `createTime`, `updateTime`) or verify button exists before clicking
**Warning signs:** `page.locator('button:has-text("now")')` returns count 0

### Pitfall 3: Report Page Assertion Results Not Displayed
**What goes wrong:** Report page shows no assertion results even though execution completed
**Why it happens:** `api_assertion_results` array is empty when no assertions configured, or assertions failed to execute
**How to avoid:** Verify assertion configuration was saved correctly before executing; check backend logs for assertion execution errors
**Warning signs:** `page.locator('text=接口断言结果')` not visible after navigating to report

### Pitfall 4: ERP Environment Variables Missing
**What goes wrong:** Tests fail immediately with connection errors
**Why it happens:** ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD not set in environment
**How to avoid:** Always use `test.skip(!erpBaseUrl, ...)` at test start; document required env vars in test comments
**Warning signs:** First API call fails with network error

## Code Examples

### Test Case 1: field_params Configuration
```typescript
// Source: Based on assertion-flow.spec.ts pattern
test('field_params configuration - verify field parameter transmission', async ({ page }) => {
  test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')
  test.setTimeout(300000)

  await page.goto('/tasks')
  await page.click('button:has-text("新建任务")')
  await page.fill('[name="name"]', 'E2E Field Params Test')
  await page.fill('[name="target_url"]', erpBaseUrl!)

  // Switch to assertions tab
  await page.click('button:has-text("业务断言")')
  await page.click('button:has-text("添加断言")')
  await expect(page.locator('text=Select Assertion Methods')).toBeVisible()
  await page.waitForTimeout(2000)

  // Select assertion method
  await page.locator('input[type="checkbox"]').first().click()
  await expect(page.locator('text=Selected')).toBeVisible()

  // Configure field_params - scroll to field params section
  const fieldParamsSection = page.locator('text=Assertion Fields')
  await expect(fieldParamsSection).toBeVisible()

  // Search for a field
  const searchInput = page.locator('input[placeholder*="Search"]')
  await searchInput.fill('status')

  // Select field and set value
  await page.locator('.border-gray-100 input[type="checkbox"]').first().check()
  const valueInput = page.locator('input[placeholder="Expected value"]')
  await valueInput.fill('已完成')

  await page.click('button:has-text("Confirm")')
  await expect(page.locator('.border-orange-200')).toBeVisible()

  // Create and execute
  await page.click('button:has-text("创建任务")')
  await expect(page.locator('text=E2E Field Params Test')).toBeVisible()
  await page.click('tr:has-text("E2E Field Params Test") button:has-text("执行")')

  // Wait for completion
  await page.waitForSelector('text=已完成', { timeout: 180000 })

  // Verify report
  await page.click('button:has-text("查看报告")')
  await expect(page.locator('text=接口断言结果')).toBeVisible()
  await expect(page.locator('.bg-green-50.border-green-200, .bg-red-50.border-red-200')).toBeVisible()
})
```

### Test Case 2: "now" Time Conversion
```typescript
// Source: Based on _convert_now_values() in external_precondition_bridge.py
test('now time conversion - verify "now" converts to current datetime', async ({ page }) => {
  test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')
  test.setTimeout(300000)

  await page.goto('/tasks')
  await page.click('button:has-text("新建任务")')
  await page.fill('[name="name"]', 'E2E Now Time Test')
  await page.fill('[name="target_url"]', erpBaseUrl!)

  await page.click('button:has-text("业务断言")')
  await page.click('button:has-text("添加断言")')
  await page.waitForTimeout(2000)

  await page.locator('input[type="checkbox"]').first().click()

  // Search for a time field
  const searchInput = page.locator('input[placeholder*="Search"]')
  await searchInput.fill('Time')

  // Select time field
  await page.locator('.border-gray-100 input[type="checkbox"]').first().check()

  // Click "now" button
  const nowButton = page.locator('button:has-text("now")')
  if (await nowButton.count() > 0) {
    await nowButton.click()
    // Verify "now" appears in input
    const valueInput = page.locator('input[placeholder="Expected value"]')
    await expect(valueInput).toHaveValue('now')
  }

  await page.click('button:has-text("Confirm")')
  // ... continue with execution and verification
})
```

### Test Case 3: Three-Layer Params Success
```typescript
test('three-layer params success - all fields pass with green display', async ({ page }) => {
  test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')
  test.setTimeout(300000)

  // Create task with full three-layer configuration
  // data: 'main', api_params: { i: 1, headers: 'main' }, field_params: { statusStr: '...' }

  await page.goto('/tasks')
  await page.click('button:has-text("新建任务")')
  await page.fill('[name="name"]', 'E2E Three Layer Success')
  await page.fill('[name="target_url"]', erpBaseUrl!)

  await page.click('button:has-text("业务断言")')
  await page.click('button:has-text("添加断言")')
  await page.waitForTimeout(2000)

  await page.locator('input[type="checkbox"]').first().click()

  // Configure api_params (i, j, k parameters)
  const iParamInput = page.locator('label:has-text("i")').locator('..').locator('input')
  if (await iParamInput.count() > 0) {
    await iParamInput.fill('1')
  }

  // Configure field_params
  const fieldParamsSection = page.locator('text=Assertion Fields')
  await expect(fieldParamsSection).toBeVisible()

  // Select multiple fields for comprehensive test
  const fieldCheckboxes = page.locator('.border-gray-100 input[type="checkbox"]')
  const count = Math.min(3, await fieldCheckboxes.count())
  for (let i = 0; i < count; i++) {
    await fieldCheckboxes.nth(i).check()
    const valueInputs = page.locator('input[placeholder="Expected value"]')
    await valueInputs.nth(i).fill('test_value')
  }

  await page.click('button:has-text("Confirm")')
  await page.click('button:has-text("创建任务")')

  // Execute and verify
  await page.click('tr:has-text("E2E Three Layer Success") button:has-text("执行")')
  await page.waitForSelector('text=已完成', { timeout: 180000 })

  // Verify all assertion result cards show green (passed)
  await page.click('button:has-text("查看报告")')
  await expect(page.locator('text=接口断言结果')).toBeVisible()

  // Check for green success cards
  const successCards = page.locator('.bg-green-50.border-green-200')
  const failCards = page.locator('.bg-red-50.border-red-200')

  // At least one result card should be visible
  const successCount = await successCards.count()
  const failCount = await failCards.count()
  expect(successCount + failCount).toBeGreaterThan(0)
})
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single-layer params | Three-layer params (data/api_params/field_params) | v0.4.1 (Phase 28-30) | More granular assertion configuration |
| Manual time entry | "now" auto-conversion | v0.4.1 (Phase 30) | Simplified time field testing |
| Hardcoded fields | Dynamic field discovery via AST | v0.4.1 (Phase 28) | 300+ fields auto-discovered |

**Deprecated/outdated:**
- `params` as single parameter object: Use `api_params` and `field_params` separately (backward compatible via D-06)

## Open Questions

1. **Which specific assertion method to use for tests?**
   - What we know: PcAssert, MgAssert, McAssert classes available with multiple methods each
   - What's unclear: Which method has the most reliable test data in the ERP
   - Recommendation: Use `attachment_inventory_list_assert` as referenced in ROADMAP.md, or first available method

2. **Time field availability in test ERP?**
   - What we know: Time fields like `createTime`, `updateTime` exist in field discovery
   - What's unclear: Whether these fields have consistent data in the test ERP
   - Recommendation: If "now" test fails, document as environment-specific limitation

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright Test ^1.40.0 |
| Config file | e2e/playwright.config.ts |
| Quick run command | `cd e2e && npx playwright test assertion-flow.spec.ts --grep "field_params\|now\|three-layer"` |
| Full suite command | `cd e2e && npx playwright test assertion-flow.spec.ts` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| E2E-01 | Complete assertion flow with three-layer params | E2E | `npx playwright test assertion-flow.spec.ts -g "three-layer"` | Extend existing |
| E2E-02 | Assertion success and failure scenarios | E2E | `npx playwright test assertion-flow.spec.ts` | Extend existing |

### Sampling Rate
- **Per test run:** `cd e2e && npx playwright test assertion-flow.spec.ts`
- **Specific test:** `cd e2e && npx playwright test assertion-flow.spec.ts -g "test name"`
- **Debug mode:** `cd e2e && npx playwright test assertion-flow.spec.ts --debug`

### Wave 0 Gaps
None - existing E2E test infrastructure is complete. Just need to add 3 new test cases to existing file.

## Sources

### Primary (HIGH confidence)
- `e2e/tests/assertion-flow.spec.ts` - Existing E2E test patterns (5 tests, 300s timeout, skip without ERP)
- `e2e/playwright.config.ts` - Playwright configuration (120s global timeout, webServer auto-start)
- `frontend/src/components/TaskModal/FieldParamsEditor.tsx` - Field params UI component
- `backend/core/external_precondition_bridge.py` - Three-layer params handling, "now" conversion

### Secondary (MEDIUM confidence)
- `frontend/src/components/TaskModal/AssertionSelector.tsx` - Full assertion selector flow with FieldParamsEditor integration
- `frontend/src/pages/ReportDetail.tsx` - Report page structure with ApiAssertionResults
- `frontend/src/components/Report/ApiAssertionResults.tsx` - Assertion result card styling (bg-green-50/border-green-200)

### Tertiary (LOW confidence)
- None - all information verified from source code

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using existing Playwright setup, no new dependencies
- Architecture: HIGH - Extending existing test file, established patterns
- Pitfalls: HIGH - Based on actual code analysis of timing and UI components

**Research date:** 2026-03-22
**Valid until:** 30 days (stable E2E patterns)
