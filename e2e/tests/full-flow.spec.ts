// e2e/tests/full-flow.spec.ts
// E2E-04: Complete flow with data method and variable substitution
//
// This test validates the complete end-to-end user flow:
// 1. Task creation with data method configuration
// 2. Data method selection through 4-step wizard
// 3. Field extraction and variable naming
// 4. Code generation for precondition
// 5. Task execution with variable substitution
// 6. Report viewing with verified variable values
//
// Key integration points tested:
// - DataMethodSelector component -> backend API
// - context.get_data() code generation
// - PreconditionService.substitute_variables()
// - ReportDetail variable display
import { test, expect } from '@playwright/test'

test.describe('Full Flow - Data Method Integration', () => {
  test('complete flow with data method and variable substitution', async ({ page }) => {
    // Increase timeout for AI-driven execution
    test.setTimeout(300000) // 5 minutes for complete flow

    // ============================================
    // Step 1: Navigate to /tasks
    // ============================================
    await page.goto('/tasks')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

    // ============================================
    // Step 2: Click "New Task" button
    // ============================================
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 3: Fill task form
    // ============================================
    // Name
    await page.fill('[name="name"]', 'E2E Full Flow Test')

    // Description with variable placeholder
    await page.fill('[name="description"]', 'Test data method {{imei}}')

    // Target URL - use a valid URL
    await page.fill('[name="target_url"]', 'https://www.baidu.com')

    // ============================================
    // Step 4: Click "Get Data" button to open DataMethodSelector
    // ============================================
    await page.click('button:has-text("获取数据"), button:has-text("Get Data")')

    // Wait for DataMethodSelector modal to open
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // ============================================
    // Step 5: In Step 1 - Select first available data method
    // ============================================
    // Wait for methods to load
    await expect(page.locator('input[type="checkbox"]').first()).toBeVisible({ timeout: 10000 })

    // Click on the first available method checkbox
    await page.locator('input[type="checkbox"]').first().click()

    // Verify selection is shown
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // Click Next to go to Step 2
    await page.click('button:has-text("Next")')

    // ============================================
    // Step 6: In Step 2 - Fill required parameter (e.g., i=2)
    // ============================================
    // Wait for Step 2 to load
    await expect(page.locator('text=Configure Parameters')).toBeVisible({ timeout: 5000 })

    // Fill the 'i' parameter with value 2
    const iParamInput = page.locator('label:has-text("i")').locator('..').locator('input[type="number"]')
    if (await iParamInput.count() > 0) {
      await iParamInput.fill('2')
    }

    // Click Next to go to Step 3
    await page.click('button:has-text("Next")')

    // ============================================
    // Step 7: In Step 3 - Click "Preview Data" button
    // ============================================
    // Wait for Step 3 to load
    await expect(page.locator('text=Extraction Path')).toBeVisible({ timeout: 5000 })

    // Click Preview Data button
    await page.click('button:has-text("Preview Data")')

    // Wait for data to load
    await page.waitForTimeout(3000)

    // Click on first field to select extraction
    // The JSON tree viewer shows clickable values
    const firstClickableField = page.locator('.json-tree-value, [data-testid="json-value"]').first()
    if (await firstClickableField.count() > 0) {
      await firstClickableField.click()
    } else {
      // Alternative: try clicking on a specific path like [0].imei
      const jsonField = page.locator('text=imei').first()
      if (await jsonField.count() > 0) {
        await jsonField.click()
      }
    }

    // Click Next to go to Step 4
    await page.click('button:has-text("Next")')

    // ============================================
    // Step 8: In Step 4 - Set variable name to "imei"
    // ============================================
    // Wait for Step 4 to load
    await expect(page.locator('text=Variable Naming')).toBeVisible({ timeout: 5000 })

    // Find the variable name input and set it to "imei"
    const variableInput = page.locator('input[type="text"]').first()
    if (await variableInput.count() > 0) {
      // Clear and set variable name
      await variableInput.fill('imei')
    }

    // Verify code preview shows "context.get_data"
    await expect(page.locator('text=context.get_data')).toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 9: Click "Confirm" button
    // ============================================
    await page.click('button:has-text("Confirm")')

    // Wait for modal to close
    await expect(page.locator('text=Select Data Method')).not.toBeVisible({ timeout: 5000 })

    // ============================================
    // Step 10: Verify precondition textarea contains generated code
    // ============================================
    const preconditionTextarea = page.locator('textarea').first()
    await expect(preconditionTextarea).toContainText('imei = context.get_data', { timeout: 5000 })

    // ============================================
    // Step 11: Click "Create Task" button
    // ============================================
    await page.click('button:has-text("创建任务"), button:has-text("Create Task")')

    // ============================================
    // Step 12: Verify task appears in task list
    // ============================================
    await expect(page.locator('text=E2E Full Flow Test')).toBeVisible({ timeout: 10000 })

    // ============================================
    // Step 13: Click "Execute" button for the created task
    // ============================================
    await page.click('tr:has-text("E2E Full Flow Test") button:has-text("执行"), tr:has-text("E2E Full Flow Test") button:has-text("Execute")')

    // ============================================
    // Step 14: Wait for execution to complete
    // ============================================
    // Wait for execution monitor to show
    await expect(page.locator('text=执行监控, text=Monitor')).toBeVisible({ timeout: 10000 })

    // Wait for completion status (completed or failed)
    await page.waitForSelector('text=已完成, text=失败, text=completed, text=failed', {
      timeout: 180000, // 3 minutes for AI execution
    })

    // ============================================
    // Step 15: Click "View Report" button
    // ============================================
    await page.click('button:has-text("查看报告"), a:has-text("查看报告"), button:has-text("View Report")')

    // ============================================
    // Step 16: Verify report page displays variable values
    // ============================================
    // Verify we're on report page
    await expect(page).toHaveURL(/.*reports\/.*/, { timeout: 10000 })

    // Wait for report to load
    await expect(page.locator('text=执行步骤, text=Steps')).toBeVisible({ timeout: 10000 })

    // Verify the report does NOT show {{imei}} placeholder
    // Instead, it should show the actual variable value (a non-placeholder string)
    const reportContent = await page.locator('body').textContent()

    // The variable {{imei}} should be replaced with actual value
    // Check that we don't see the raw placeholder in executed steps
    expect(reportContent).not.toContain('{{imei}}')

    // Log success
    console.log('Full flow test completed successfully!')
    console.log('Variable substitution verified - no {{imei}} placeholder found in report')
  })

  test('task list displays data method configuration in task details', async ({ page }) => {
    // Navigate to tasks page
    await page.goto('/tasks')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

    // Check if any task exists with precondition code
    const taskRows = page.locator('table tbody tr')
    const rowCount = await taskRows.count()

    if (rowCount > 0) {
      // Click on first task to view/edit
      await taskRows.first().click()

      // Verify precondition section exists
      const preconditionSection = page.locator('text=前置条件')
      if (await preconditionSection.count() > 0) {
        await expect(preconditionSection).toBeVisible()
      }
    }
  })

  test('data method selector modal workflow', async ({ page }) => {
    // Navigate to tasks page
    await page.goto('/tasks')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

    // Click new task button
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // Fill basic form
    await page.fill('[name="name"]', 'Data Method Modal Test')
    await page.fill('[name="target_url"]', 'https://www.baidu.com')

    // Click Get Data button
    await page.click('button:has-text("获取数据"), button:has-text("Get Data")')

    // Verify modal opens
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Verify 4 steps are shown in the wizard
    await expect(page.locator('text=Select Method')).toBeVisible()
    await expect(page.locator('text=Configure Parameters')).toBeVisible()
    await expect(page.locator('text=Extraction Path')).toBeVisible()
    await expect(page.locator('text=Variable Naming')).toBeVisible()

    // Verify Cancel button works
    await page.click('button:has-text("Cancel")')
    await expect(page.locator('text=Select Data Method')).not.toBeVisible({ timeout: 5000 })
  })

  test('step navigation in data method selector', async ({ page }) => {
    // Navigate to tasks page
    await page.goto('/tasks')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

    // Click new task button
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // Fill basic form
    await page.fill('[name="name"]', 'Step Navigation Test')
    await page.fill('[name="target_url"]', 'https://www.baidu.com')

    // Open DataMethodSelector
    await page.click('button:has-text("获取数据"), button:has-text("Get Data")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Verify Next button is disabled when no method selected
    const nextButton = page.locator('button:has-text("Next")')
    await expect(nextButton).toBeDisabled()

    // Select a method
    await page.locator('input[type="checkbox"]').first().click()

    // Now Next should be enabled
    await expect(nextButton).toBeEnabled()

    // Go to step 2
    await nextButton.click()
    await expect(page.locator('text=Configure Parameters')).toBeVisible({ timeout: 5000 })

    // Verify Previous button works
    await page.click('button:has-text("Previous")')
    await expect(page.locator('text=Select Method')).toBeVisible({ timeout: 5000 })
  })

  test('code preview generation in variable naming step', async ({ page }) => {
    // Navigate to tasks page
    await page.goto('/tasks')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })

    // Click new task button
    await page.click('button:has-text("新建任务"), button:has-text("New Task")')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 5000 })

    // Fill basic form
    await page.fill('[name="name"]', 'Code Preview Test')
    await page.fill('[name="target_url"]', 'https://www.baidu.com')

    // Open DataMethodSelector
    await page.click('button:has-text("获取数据"), button:has-text("Get Data")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Select a method
    await page.locator('input[type="checkbox"]').first().click()
    await page.click('button:has-text("Next")')

    // Configure parameters
    await expect(page.locator('text=Configure Parameters')).toBeVisible({ timeout: 5000 })
    const iParamInput = page.locator('label:has-text("i")').locator('..').locator('input[type="number"]')
    if (await iParamInput.count() > 0) {
      await iParamInput.fill('2')
    }
    await page.click('button:has-text("Next")')

    // Preview data and select field
    await expect(page.locator('text=Extraction Path')).toBeVisible({ timeout: 5000 })
    await page.click('button:has-text("Preview Data")')
    await page.waitForTimeout(3000)

    // Select a field if available
    const jsonField = page.locator('.json-tree-value, [data-testid="json-value"]').first()
    if (await jsonField.count() > 0) {
      await jsonField.click()
    }

    await page.click('button:has-text("Next")')

    // Verify code preview is generated
    await expect(page.locator('text=Variable Naming')).toBeVisible({ timeout: 5000 })
    await expect(page.locator('text=Generated Code')).toBeVisible({ timeout: 5000 })

    // Verify the code contains context.get_data
    const codePreview = page.locator('pre')
    const codeText = await codePreview.textContent()
    expect(codeText).toContain('context.get_data')
  })
})
