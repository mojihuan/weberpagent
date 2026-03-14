// e2e/tests/smoke.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Smoke Test - Complete User Flow', () => {
  test.skip('create -> execute -> monitor -> report', async ({ page }) => {
    // E2E-01: Create task
    await page.goto('/')
    await page.click('text=任务管理')
    await page.click('text=新建任务')

    await page.fill('[name="name"]', 'E2E Smoke Test Task')
    await page.fill('[name="description"]', '打开百度首页')
    await page.click('button:has-text("创建")')

    // Verify task created
    await expect(page.locator('text=E2E Smoke Test Task')).toBeVisible()

    // E2E-02: Execute task
    await page.click('button:has-text("执行")')

    // E2E-03: Monitor execution
    await expect(page.locator('text=执行监控')).toBeVisible()

    // Wait for completion (with timeout)
    await expect(page.locator('[data-testid="run-status"]')).toHaveText(/completed|failed/, { timeout: 60000 })

    // E2E-04 & E2E-05: View report
    await page.click('text=查看报告')
    await expect(page.locator('text=执行报告')).toBeVisible()
  })
})
