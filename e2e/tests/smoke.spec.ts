// e2e/tests/smoke.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Smoke Test - Complete User Flow', () => {
  test('create -> execute -> monitor -> report', async ({ page }) => {
    // Increase timeout for AI-driven execution
    test.setTimeout(180000) // 3 minutes

    // E2E-01: Navigate and verify app loads
    await page.goto('/')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

    // Navigate to tasks
    await page.click('text=任务管理')
    await expect(page).toHaveURL(/.*tasks/)

    // Create new task
    await page.click('text=新建任务')

    // Fill task form
    await page.fill('[name="name"]', 'E2E Smoke Test Task')
    await page.fill('[name="description"]', '打开百度首页')

    // Submit form
    await page.click('button:has-text("创建")')

    // Verify task created (check for task in list or success toast)
    await expect(page.locator('text=E2E Smoke Test Task')).toBeVisible({ timeout: 10000 })

    // E2E-02: Execute task
    // Click execute button for the created task
    await page.click('tr:has-text("E2E Smoke Test Task") button:has-text("执行")')

    // E2E-03: Monitor execution
    await expect(page.locator('text=执行监控')).toBeVisible({ timeout: 10000 })

    // Wait for completion (AI execution can take time)
    // Look for status change to completed or failed
    await page.waitForSelector('text=已完成, text=失败, text=completed, text=failed', {
      timeout: 120000,
    })

    // E2E-04 & E2E-05: Navigate to report
    // Click view report button
    await page.click('button:has-text("查看报告"), a:has-text("查看报告")')

    // Verify report page
    await expect(page.locator('text=执行报告, text=报告')).toBeVisible({ timeout: 10000 })

    // Verify assertion results section exists (if any assertions)
    const assertionSection = page.locator('text=断言结果')
    // Don't fail if no assertions - just check if visible when present
    if ((await assertionSection.count()) > 0) {
      await expect(assertionSection).toBeVisible()
    }
  })
})
