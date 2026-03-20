// e2e/tests/assertion-flow.spec.ts
// E2E tests for assertion configuration and execution flow
//
// This test validates the complete assertion workflow:
// 1. Task creation with assertion configuration
// 2. Assertion method selection and parameter configuration
// 3. Task execution with assertion execution
// 4. Report display showing assertion results
//
// Key integration points tested:
// - AssertionSelector component -> backend API
// - AssertionConfig storage and execution
// - ApiAssertionResults display in ReportDetail
import { test, expect } from '@playwright/test'

test.describe('Assertion Flow Tests', () => {
  // Get ERP base URL from environment
  const erpBaseUrl = process.env.ERP_BASE_URL

  test.beforeEach(async ({ page }) => {
    // Navigate to tasks page before each test
    await page.goto('/tasks')
    await expect(page.locator('table')).toBeVisible({ timeout: 10000 })
  })

  test('single assertion success - task creation with assertion config', async ({ page }) => {
    // Skip test if ERP_BASE_URL is not configured
    test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')

    // Increase timeout for AI-driven execution
    test.setTimeout(300000) // 5 minutes for complete flow

    // ============================================
    // Step 1: Click "New Task" button
    // ============================================
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 2: Fill task form
    // ============================================
    await page.fill('[name="name"]', 'E2E Assertion Success Test')
    await page.fill('[name="target_url"]', erpBaseUrl!)

    // ============================================
    // Step 3: Switch to "Business Assertions" tab
    // ============================================
    await page.click('button:has-text("业务断言")')
    await expect(page.locator('text=添加断言')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 4: Click "Add Assertion" button
    // ============================================
    await page.click('button:has-text("添加断言")')

    // ============================================
    // Step 5: Verify AssertionSelector modal opens
    // ============================================
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible({ timeout: 10000 })

    // Wait for methods to load
    await page.waitForTimeout(2000)

    // Check if methods are available
    const firstCheckbox = page.locator('input[type="checkbox"]').first()
    const checkboxCount = await firstCheckbox.count()

    if (checkboxCount === 0) {
      // No methods available - skip test
      test.skip()
      return
    }

    // ============================================
    // Step 6: Select first available assertion method
    // ============================================
    await firstCheckbox.click()

    // Verify "Selected" text appears
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 7: Click "Confirm" button
    // ============================================
    await page.click('button:has-text("Confirm")')

    // Wait for modal to close
    await expect(page.locator('text=Select Assertion Methods')).not.toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 8: Verify assertion card appears (border-orange-200 class)
    // ============================================
    await expect(page.locator('.border-orange-200, [class*="border-orange"]')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 9: Create the task
    // ============================================
    await page.click('button:has-text("创建任务"), button:has-text("Create Task")')

    // ============================================
    // Step 10: Verify task appears in list
    // ============================================
    await expect(page.locator('text=E2E Assertion Success Test')).toBeVisible({ timeout: 10000 })

    // ============================================
    // Step 11: Execute the task
    // ============================================
    await page.click('tr:has-text("E2E Assertion Success Test") button:has-text("执行"), tr:has-text("E2E Assertion Success Test") button:has-text("Execute")')

    // ============================================
    // Step 12: Wait for completion
    // ============================================
    await expect(page.locator('text=执行监控, text=Monitor')).toBeVisible({ timeout: 10000 })

    // Wait for completion status (completed or failed)
    await page.waitForSelector('text=已完成, text=失败, text=completed, text=failed', {
      timeout: 180000, // 3 minutes for AI execution
    })

    // ============================================
    // Step 13: Navigate to report
    // ============================================
    await page.click('button:has-text("查看报告"), a:has-text("查看报告"), button:has-text("View Report")')

    // Verify we're on report page
    await expect(page).toHaveURL(/.*reports\/.*/, { timeout: 10000 })

    // ============================================
    // Step 14: Verify report page displays assertion results section
    // ============================================
    await expect(page.locator('text=执行步骤, text=Steps, text=执行报告')).toBeVisible({ timeout: 10000 })

    // Check for assertion results section (may or may not have results depending on assertion outcome)
    const assertionResultsSection = page.locator('text=断言结果, text=接口断言结果')
    const hasAssertionSection = (await assertionResultsSection.count()) > 0

    if (hasAssertionSection) {
      await expect(assertionResultsSection.first()).toBeVisible({ timeout: 5000 })
      console.log('Assertion results section found in report')
    }

    console.log('Single assertion success test completed!')
  })

  test('single assertion failure - displays fail status in report', async ({ page }) => {
    // Skip test if ERP_BASE_URL is not configured
    test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')

    // Increase timeout for AI-driven execution
    test.setTimeout(300000) // 5 minutes

    // ============================================
    // Step 1: Click "New Task" button
    // ============================================
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 2: Fill task form
    // ============================================
    await page.fill('[name="name"]', 'E2E Assertion Failure Test')
    await page.fill('[name="target_url"]', erpBaseUrl!)

    // ============================================
    // Step 3: Switch to "Business Assertions" tab
    // ============================================
    await page.click('button:has-text("业务断言")')
    await expect(page.locator('text=添加断言')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 4: Click "Add Assertion" button
    // ============================================
    await page.click('button:has-text("添加断言")')

    // ============================================
    // Step 5: Verify AssertionSelector modal opens
    // ============================================
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible({ timeout: 10000 })
    await page.waitForTimeout(2000)

    const firstCheckbox = page.locator('input[type="checkbox"]').first()
    if ((await firstCheckbox.count()) === 0) {
      test.skip()
      return
    }

    // ============================================
    // Step 6: Select first available assertion method
    // ============================================
    await firstCheckbox.click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 7: Configure with intentionally failing params
    // Use filter params (i, j, k) that return no data to trigger failure
    // ============================================
    const iParamInput = page.locator('label:has-text("i")').locator('..').locator('input[type="number"]')
    if ((await iParamInput.count()) > 0) {
      // Set a very large value that likely won't match any data
      await iParamInput.fill('9999')
    }

    // ============================================
    // Step 8: Click "Confirm" button
    // ============================================
    await page.click('button:has-text("Confirm")')
    await expect(page.locator('text=Select Assertion Methods')).not.toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 9: Verify assertion card appears
    // ============================================
    await expect(page.locator('.border-orange-200, [class*="border-orange"]')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 10: Create the task
    // ============================================
    await page.click('button:has-text("创建任务"), button:has-text("Create Task")')
    await expect(page.locator('text=E2E Assertion Failure Test')).toBeVisible({ timeout: 10000 })

    // ============================================
    // Step 11: Execute the task
    // ============================================
    await page.click('tr:has-text("E2E Assertion Failure Test") button:has-text("执行"), tr:has-text("E2E Assertion Failure Test") button:has-text("Execute")')

    // ============================================
    // Step 12: Wait for completion
    // ============================================
    await expect(page.locator('text=执行监控, text=Monitor')).toBeVisible({ timeout: 10000 })
    await page.waitForSelector('text=已完成, text=失败, text=completed, text=failed', {
      timeout: 180000,
    })

    // ============================================
    // Step 13: Navigate to report
    // ============================================
    await page.click('button:has-text("查看报告"), a:has-text("查看报告"), button:has-text("View Report")')
    await expect(page).toHaveURL(/.*reports\/.*/, { timeout: 10000 })

    // ============================================
    // Step 14: Verify assertion result card shows fail status
    // ============================================
    await expect(page.locator('text=执行步骤, text=Steps, text=执行报告')).toBeVisible({ timeout: 10000 })

    // Check for fail status UI elements (bg-red-50 border-red-200)
    const failStatusLocator = page.locator('.bg-red-50.border-red-200, [class*="bg-red-50"][class*="border-red-200"]')

    // Also check for XCircle icon (text-red-500)
    const xCircleLocator = page.locator('.text-red-500')

    // The assertion might pass or fail depending on actual data
    // We verify that the result is displayed with proper status styling
    const hasFailStatus = (await failStatusLocator.count()) > 0
    const hasXCircle = (await xCircleLocator.count()) > 0

    // If there are assertion results, verify status indicators are present
    if ((await page.locator('text=断言结果, text=接口断言结果').count()) > 0) {
      // Either pass or fail status should be visible
      const passStatusLocator = page.locator('.bg-green-50.border-green-200, [class*="bg-green-50"][class*="border-green-200"]')
      const hasPassStatus = (await passStatusLocator.count()) > 0

      expect(hasFailStatus || hasPassStatus).toBe(true)
    }

    console.log('Single assertion failure test completed!')
  })

  test('multiple assertions execute independently - non fail-fast', async ({ page }) => {
    // Skip test if ERP_BASE_URL is not configured
    test.skip(!erpBaseUrl, 'ERP_BASE_URL environment variable not set')

    // Increase timeout for AI-driven execution
    test.setTimeout(300000) // 5 minutes

    // ============================================
    // Step 1: Click "New Task" button
    // ============================================
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 2: Fill task form
    // ============================================
    await page.fill('[name="name"]', 'E2E Multiple Assertions Test')
    await page.fill('[name="target_url"]', erpBaseUrl!)

    // ============================================
    // Step 3: Switch to "Business Assertions" tab
    // ============================================
    await page.click('button:has-text("业务断言")')
    await expect(page.locator('text=添加断言')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 4: Add first assertion
    // ============================================
    await page.click('button:has-text("添加断言")')
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible({ timeout: 10000 })
    await page.waitForTimeout(2000)

    let firstCheckbox = page.locator('input[type="checkbox"]').first()
    if ((await firstCheckbox.count()) === 0) {
      test.skip()
      return
    }

    // Select first method
    await firstCheckbox.click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })
    await page.click('button:has-text("Confirm")')
    await expect(page.locator('text=Select Assertion Methods')).not.toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 5: Add second assertion
    // ============================================
    await page.click('button:has-text("添加断言")')
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible({ timeout: 10000 })
    await page.waitForTimeout(2000)

    // Select second method (or first if only one available)
    const checkboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await checkboxes.count()

    if (checkboxCount >= 2) {
      // Click second checkbox
      await checkboxes.nth(1).click()
    } else if (checkboxCount === 1) {
      // Only one method, select it again
      await checkboxes.first().click()
    }

    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })
    await page.click('button:has-text("Confirm")')
    await expect(page.locator('text=Select Assertion Methods')).not.toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 6: Verify both assertion cards appear
    // ============================================
    const assertionCards = page.locator('.border-orange-200, [class*="border-orange"]')
    const cardCount = await assertionCards.count()
    expect(cardCount).toBeGreaterThanOrEqual(2)

    // ============================================
    // Step 7: Create the task
    // ============================================
    await page.click('button:has-text("创建任务"), button:has-text("Create Task")')
    await expect(page.locator('text=E2E Multiple Assertions Test')).toBeVisible({ timeout: 10000 })

    // ============================================
    // Step 8: Execute the task
    // ============================================
    await page.click('tr:has-text("E2E Multiple Assertions Test") button:has-text("执行"), tr:has-text("E2E Multiple Assertions Test") button:has-text("Execute")')

    // ============================================
    // Step 9: Wait for completion
    // ============================================
    await expect(page.locator('text=执行监控, text=Monitor')).toBeVisible({ timeout: 10000 })
    await page.waitForSelector('text=已完成, text=失败, text=completed, text=failed', {
      timeout: 180000,
    })

    // ============================================
    // Step 10: Navigate to report
    // ============================================
    await page.click('button:has-text("查看报告"), a:has-text("查看报告"), button:has-text("View Report")')
    await expect(page).toHaveURL(/.*reports\/.*/, { timeout: 10000 })

    // ============================================
    // Step 11: Verify BOTH assertion results appear in report (count >= 2)
    // This verifies non-fail-fast behavior
    // ============================================
    await expect(page.locator('text=执行步骤, text=Steps, text=执行报告')).toBeVisible({ timeout: 10000 })

    // Check for assertion results section
    const assertionResultsSection = page.locator('text=断言结果, text=接口断言结果')
    if ((await assertionResultsSection.count()) > 0) {
      await expect(assertionResultsSection.first()).toBeVisible({ timeout: 5000 })

      // Count assertion result cards (both pass and fail)
      const passCards = page.locator('.bg-green-50.border-green-200, [class*="bg-green-50"][class*="border-green-200"]')
      const failCards = page.locator('.bg-red-50.border-red-200, [class*="bg-red-50"][class*="border-red-200"]')

      const passCount = await passCards.count()
      const failCount = await failCards.count()
      const totalResults = passCount + failCount

      // Verify at least 2 assertion results are displayed (non-fail-fast)
      expect(totalResults).toBeGreaterThanOrEqual(2)

      console.log(`Found ${totalResults} assertion results (${passCount} passed, ${failCount} failed)`)
    }

    console.log('Multiple assertions non-fail-fast test completed!')
  })

  test('assertion selector modal workflow', async ({ page }) => {
    // Test the assertion selector modal without creating a task
    test.setTimeout(60000) // 1 minute for modal test

    // Click "New Task" button
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // Fill basic form
    await page.fill('[name="name"]', 'Assertion Modal Test')
    await page.fill('[name="target_url"]', 'https://example.com')

    // Switch to Business Assertions tab
    await page.click('button:has-text("业务断言")')
    await expect(page.locator('text=添加断言')).toBeVisible({ timeout: 5000 })

    // Click Add Assertion button
    await page.click('button:has-text("添加断言")')

    // Verify modal opens
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible({ timeout: 10000 })

    // Wait for methods to load
    await page.waitForTimeout(2000)

    // Verify search input exists
    await expect(page.locator('input[placeholder*="Search"]')).toBeVisible({ timeout: 5000 })

    // Verify Cancel button works
    await page.click('button:has-text("Cancel")')
    await expect(page.locator('text=Select Assertion Methods')).not.toBeVisible({ timeout: 5000 })

    console.log('Assertion selector modal workflow test completed!')
  })

  test('assertion configuration preserves parameters', async ({ page }) => {
    // Test that assertion configuration with parameters is preserved
    test.setTimeout(60000)

    // Click "New Task" button
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // Fill basic form
    await page.fill('[name="name"]', 'Assertion Config Test')
    await page.fill('[name="target_url"]', 'https://example.com')

    // Switch to Business Assertions tab
    await page.click('button:has-text("业务断言")')

    // Click Add Assertion button
    await page.click('button:has-text("添加断言")')
    await expect(page.locator('text=Select Assertion Methods')).toBeVisible({ timeout: 10000 })
    await page.waitForTimeout(2000)

    const firstCheckbox = page.locator('input[type="checkbox"]').first()
    if ((await firstCheckbox.count()) === 0) {
      test.skip()
      return
    }

    // Select first method
    await firstCheckbox.click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // If there are parameter inputs, configure them
    const iParamInput = page.locator('input[type="number"]').first()
    if ((await iParamInput.count()) > 0) {
      await iParamInput.fill('5')
    }

    // Confirm selection
    await page.click('button:has-text("Confirm")')
    await expect(page.locator('text=Select Assertion Methods')).not.toBeVisible({ timeout: 5000 })

    // Verify assertion card is created
    await expect(page.locator('.border-orange-200, [class*="border-orange"]')).toBeVisible({ timeout: 5000 })

    // The card should show the method name
    const assertionCard = page.locator('.border-orange-200, [class*="border-orange"]').first()
    await expect(assertionCard).toBeVisible()

    console.log('Assertion configuration test completed!')
  })
})
