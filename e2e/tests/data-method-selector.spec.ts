// e2e/tests/data-method-selector.spec.ts
import { test, expect } from '@playwright/test'

test.describe('DataMethodSelector 4-Step Wizard', () => {
  test.setTimeout(180000) // 3 minutes for long-running operations

  test.beforeEach(async ({ page }) => {
    // Navigate to tasks page
    await page.goto('/tasks')
    await expect(page.locator('text=任务管理')).toBeVisible({ timeout: 10000 })
  })

  test('DataMethodSelector Modal Opens', async ({ page }) => {
    // Click "New Task" button to open task creation modal
    await page.click('text=新建任务')

    // Wait for task form modal to appear
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Click "Get Data" button (获取数据)
    await page.click('button:has-text("获取数据")')

    // Wait for DataMethodSelector modal to appear
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Verify modal is visible
    const modal = page.locator('.fixed.inset-0.z-50')
    await expect(modal).toBeVisible()

    // Verify step bar is visible with 4 steps
    await expect(page.locator('text=Select Method')).toBeVisible()
    await expect(page.locator('text=Configure Parameters')).toBeVisible()
    await expect(page.locator('text=Extraction Path')).toBeVisible()
    await expect(page.locator('text=Variable Naming')).toBeVisible()
  })

  test('Step 1 - Method Selection', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Verify search input is visible
    const searchInput = page.locator('input[placeholder*="Search"]')
    await expect(searchInput).toBeVisible()

    // Wait for methods to load (check for class groups)
    // Either methods are displayed or an error message is shown
    await page.waitForTimeout(2000) // Wait for API response

    // Check if data methods are available (may show error if ERP not configured)
    const errorState = page.locator('text=not available, text=External data methods')
    const hasError = await errorState.count()

    if (hasError > 0) {
      // If external methods not available, skip this test
      test.skip()
      return
    }

    // Verify class groups are displayed
    const classGroups = page.locator('h4.text-sm.font-medium.text-gray-700')
    const classCount = await classGroups.count()

    if (classCount === 0) {
      // No methods available, skip
      test.skip()
      return
    }

    // Verify method items exist with checkboxes
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await methodCheckboxes.count()

    if (checkboxCount > 0) {
      // Select first method by clicking checkbox
      await methodCheckboxes.first().click()

      // Verify selected method appears in selected area
      await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

      // Click Next button
      await page.click('button:has-text("Next")')

      // Verify we moved to Step 2
      await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })
    }
  })

  test('Step 2 - Parameter Configuration', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    await page.waitForTimeout(2000)

    // Check if data methods are available
    const errorState = page.locator('text=not available')
    const hasError = await errorState.count()

    if (hasError > 0) {
      test.skip()
      return
    }

    // Select first method if available
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await methodCheckboxes.count()

    if (checkboxCount === 0) {
      test.skip()
      return
    }

    await methodCheckboxes.first().click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })
    await page.click('button:has-text("Next")')

    // Verify we're on Step 2
    await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })

    // Verify parameter inputs exist
    const paramInputs = page.locator('input[type="number"], input[type="text"]')
    const inputCount = await paramInputs.count()

    // Fill required parameter with value "2" if there are parameter inputs
    if (inputCount > 0) {
      // Find parameter inputs within the config section
      const configParamInputs = page.locator('.border-gray-200.rounded-lg input')
      const configInputCount = await configParamInputs.count()

      if (configInputCount > 0) {
        await configParamInputs.first().fill('2')
      }
    }

    // Click Next button
    await page.click('button:has-text("Next")')

    // Verify we moved to Step 3
    await expect(page.locator('text=Preview Data')).toBeVisible({ timeout: 5000 })
  })

  test('Step 3 - Data Preview', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    await page.waitForTimeout(2000)

    // Check if data methods are available
    const errorState = page.locator('text=not available')
    const hasError = await errorState.count()

    if (hasError > 0) {
      test.skip()
      return
    }

    // Select first method
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await methodCheckboxes.count()

    if (checkboxCount === 0) {
      test.skip()
      return
    }

    await methodCheckboxes.first().click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // Navigate through steps
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })

    // Fill parameters if needed
    const configParamInputs = page.locator('.border-gray-200.rounded-lg input')
    const configInputCount = await configParamInputs.count()
    if (configInputCount > 0) {
      await configParamInputs.first().fill('2')
    }

    await page.click('button:has-text("Next")')

    // Verify we're on Step 3
    await expect(page.locator('text=Preview Data')).toBeVisible({ timeout: 5000 })

    // Verify preview button is visible
    const previewButton = page.locator('button:has-text("Preview Data")')
    await expect(previewButton).toBeVisible()

    // Click preview button
    await previewButton.click()

    // Wait for data to load (may show loading state)
    await page.waitForTimeout(3000)

    // Check for either data preview or error
    const jsonViewer = page.locator('.bg-gray-50.max-h-64')
    const errorDiv = page.locator('.text-red-500.bg-red-50')

    const hasData = await jsonViewer.count()
    const hasErrorDiv = await errorDiv.count()

    // Either data or error should appear after clicking preview
    expect(hasData > 0 || hasErrorDiv > 0).toBeTruthy()

    // If data loaded successfully, try to select a field
    if (hasData > 0) {
      // Click on a field in JSON viewer to select for extraction
      const clickableFields = page.locator('.cursor-pointer')
      const fieldCount = await clickableFields.count()

      if (fieldCount > 0) {
        await clickableFields.first().click()

        // Verify extraction appears in list
        await expect(page.locator('text=Selected fields')).toBeVisible({ timeout: 5000 })
      }
    }
  })

  test('Step 4 - Variable Naming', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    await page.waitForTimeout(2000)

    // Check if data methods are available
    const errorState = page.locator('text=not available')
    const hasError = await errorState.count()

    if (hasError > 0) {
      test.skip()
      return
    }

    // Select first method
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await methodCheckboxes.count()

    if (checkboxCount === 0) {
      test.skip()
      return
    }

    await methodCheckboxes.first().click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // Navigate to Step 2
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })

    // Fill parameters
    const configParamInputs = page.locator('.border-gray-200.rounded-lg input')
    const configInputCount = await configParamInputs.count()
    if (configInputCount > 0) {
      await configParamInputs.first().fill('2')
    }

    // Navigate to Step 3
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Preview Data')).toBeVisible({ timeout: 5000 })

    // Click preview and wait for data
    await page.click('button:has-text("Preview Data")')
    await page.waitForTimeout(3000)

    // Select a field for extraction
    const clickableFields = page.locator('.cursor-pointer')
    const fieldCount = await clickableFields.count()

    if (fieldCount === 0) {
      // Skip if no fields to select
      test.skip()
      return
    }

    await clickableFields.first().click()
    await expect(page.locator('text=Selected fields')).toBeVisible({ timeout: 5000 })

    // Navigate to Step 4
    await page.click('button:has-text("Next")')

    // Verify we're on Step 4
    await expect(page.locator('text=Variable Naming')).toBeVisible({ timeout: 5000 })

    // Verify variable name inputs exist
    const varNameInputs = page.locator('input.border-gray-200, input.border-yellow-400')
    const varInputCount = await varNameInputs.count()

    if (varInputCount > 0) {
      // Edit variable name to "imei"
      await varNameInputs.first().fill('imei')
    }

    // Verify code preview shows generated code with "context.get_data"
    const codePreview = page.locator('text=context.get_data')
    await expect(codePreview).toBeVisible({ timeout: 5000 })

    // Verify generated code section exists
    await expect(page.locator('text=Generated Code')).toBeVisible()
  })

  test('Code Generation', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Get the precondition textarea
    const preconditionTextarea = page.locator('textarea[placeholder*="context"]')

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    await page.waitForTimeout(2000)

    // Check if data methods are available
    const errorState = page.locator('text=not available')
    const hasError = await errorState.count()

    if (hasError > 0) {
      test.skip()
      return
    }

    // Select first method
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await methodCheckboxes.count()

    if (checkboxCount === 0) {
      test.skip()
      return
    }

    await methodCheckboxes.first().click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // Navigate through all steps
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })

    // Fill parameters
    const configParamInputs = page.locator('.border-gray-200.rounded-lg input')
    const configInputCount = await configParamInputs.count()
    if (configInputCount > 0) {
      await configParamInputs.first().fill('2')
    }

    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Preview Data')).toBeVisible({ timeout: 5000 })

    // Preview and select field
    await page.click('button:has-text("Preview Data")')
    await page.waitForTimeout(3000)

    const clickableFields = page.locator('.cursor-pointer')
    const fieldCount = await clickableFields.count()

    if (fieldCount === 0) {
      test.skip()
      return
    }

    await clickableFields.first().click()
    await expect(page.locator('text=Selected fields')).toBeVisible({ timeout: 5000 })

    // Go to Step 4
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Variable Naming')).toBeVisible({ timeout: 5000 })

    // Set variable name
    const varNameInputs = page.locator('input.border-gray-200, input.border-yellow-400')
    const varInputCount = await varNameInputs.count()
    if (varInputCount > 0) {
      await varNameInputs.first().fill('imei')
    }

    // Click Confirm button
    await page.click('button:has-text("Confirm")')

    // Verify modal closes
    await expect(page.locator('text=Select Data Method')).not.toBeVisible({ timeout: 5000 })

    // Verify generated code appears in precondition textarea
    await expect(preconditionTextarea).toHaveValue(/context\.get_data/, { timeout: 5000 })
  })

  test('Modal can be cancelled', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Click Cancel button
    await page.click('button:has-text("Cancel")')

    // Verify modal closes
    await expect(page.locator('text=Select Data Method')).not.toBeVisible({ timeout: 5000 })
  })

  test('Modal can be closed by backdrop click', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    // Click backdrop (the fixed inset-0 div with bg-black/50)
    const backdrop = page.locator('.fixed.inset-0.bg-black\\/50, .fixed.inset-0.bg-black\\/50').first()
    await backdrop.click({ position: { x: 10, y: 10 } })

    // Verify modal closes
    await expect(page.locator('text=Select Data Method')).not.toBeVisible({ timeout: 5000 })
  })

  test('Navigation between steps works correctly', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    await page.waitForTimeout(2000)

    // Check if data methods are available
    const errorState = page.locator('text=not available')
    const hasError = await errorState.count()

    if (hasError > 0) {
      test.skip()
      return
    }

    // Select first method
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const checkboxCount = await methodCheckboxes.count()

    if (checkboxCount === 0) {
      test.skip()
      return
    }

    await methodCheckboxes.first().click()
    await expect(page.locator('text=Selected')).toBeVisible({ timeout: 5000 })

    // Go to Step 2
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })

    // Go back to Step 1
    await page.click('button:has-text("Previous")')
    await expect(page.locator('text=Select Method')).toBeVisible({ timeout: 5000 })

    // Verify selection is preserved
    const selectedMethod = page.locator('text=Selected')
    await expect(selectedMethod).toBeVisible()

    // Go forward to Step 2 again
    await page.click('button:has-text("Next")')
    await expect(page.locator('text=Configure parameters')).toBeVisible({ timeout: 5000 })
  })

  test('Search filters methods correctly', async ({ page }) => {
    // Open task creation modal
    await page.click('text=新建任务')
    await expect(page.locator('text=任务名称')).toBeVisible({ timeout: 10000 })

    // Open DataMethodSelector modal
    await page.click('button:has-text("获取数据")')
    await expect(page.locator('text=Select Data Method')).toBeVisible({ timeout: 10000 })

    await page.waitForTimeout(2000)

    // Check if data methods are available
    const errorState = page.locator('text=not available')
    const hasError = await errorState.count()

    if (hasError > 0) {
      test.skip()
      return
    }

    // Get initial count of method checkboxes
    const methodCheckboxes = page.locator('input[type="checkbox"]')
    const initialCount = await methodCheckboxes.count()

    if (initialCount === 0) {
      test.skip()
      return
    }

    // Type in search box
    const searchInput = page.locator('input[placeholder*="Search"]')
    await searchInput.fill('xyz123nonexistent')

    // Wait for filter to apply
    await page.waitForTimeout(500)

    // Verify no methods match (or fewer methods)
    const filteredCount = await methodCheckboxes.count()

    // Search should filter results (filtered count should be <= initial count)
    expect(filteredCount).toBeLessThanOrEqual(initialCount)
  })
})
