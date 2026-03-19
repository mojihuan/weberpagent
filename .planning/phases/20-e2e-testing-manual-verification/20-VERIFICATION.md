# Manual Verification Checklist - Data Method Integration

**Phase:** 20-e2e-testing-manual-verification
**Created:** 2026-03-19
**Purpose:** Comprehensive manual verification checklist for data method integration functionality

---

## Environment Setup

Before starting verification, ensure the following environment variables are configured:

- [ ] `ERP_BASE_URL` environment variable is set to the real ERP server URL
- [ ] `ERP_USERNAME` environment variable is set with valid ERP credentials
- [ ] `ERP_PASSWORD` environment variable is set with valid ERP credentials
- [ ] `WEBSERP_PATH` environment variable is set (if required by ERP system)
- [ ] `DASHSCOPE_API_KEY` is configured for AI execution
- [ ] Backend server is running on port 8080 (`uv run uvicorn backend.api.main:app --reload --port 8080`)
- [ ] Frontend server is running on port 5173 (`cd frontend && npm run dev`)
- [ ] Database is accessible and contains test data

### Quick Environment Check Commands

```bash
# Check environment variables
echo $ERP_BASE_URL
echo $ERP_USERNAME

# Check backend is running
curl http://localhost:8080/health

# Check frontend is running
curl http://localhost:5173
```

---

## DataMethodSelector UI Verification (MANUAL-01)

This section verifies the 4-step wizard DataMethodSelector component works correctly.

### Step 1: Method Selection

- [ ] "Get Data" button is visible in the task form (precondition section)
- [ ] Clicking "Get Data" button opens the modal dialog
- [ ] Modal title shows "Get Data from ERP"
- [ ] Method list loads with class groups (e.g., "BaseParams", "OtherParams")
- [ ] Clicking a class group expands to show methods within that class
- [ ] Search input filters methods correctly by name
- [ ] Method checkbox toggles selection state
- [ ] Multiple methods can be selected
- [ ] Selected methods appear in the summary area at the bottom
- [ ] Selected method count is displayed correctly
- [ ] "Next" button is disabled until at least one method is selected
- [ ] Clicking "Next" with selected methods proceeds to Step 2

### Step 2: Parameter Configuration

- [ ] Parameter inputs are displayed for each selected method
- [ ] Required parameters are marked with red asterisk (*)
- [ ] Optional parameters are shown without asterisk
- [ ] Parameter type hints are displayed (e.g., "integer", "string")
- [ ] Parameter descriptions/tooltips are visible
- [ ] Input validation works (e.g., number-only fields reject letters)
- [ ] "Back" button returns to Step 1
- [ ] "Next" button is disabled until all required parameters are filled
- [ ] Clicking "Next" with all required params proceeds to Step 3

### Step 3: Preview & Extraction

- [ ] "Preview" button is visible and enabled
- [ ] Clicking "Preview" executes the data method against real ERP
- [ ] Loading indicator shows during execution
- [ ] JSON viewer displays returned data in formatted view
- [ ] JSON viewer supports expand/collapse for nested structures
- [ ] Clicking a field in the JSON adds an extraction path
- [ ] Extraction path appears in the extraction list (e.g., `[0].imei`)
- [ ] Multiple extraction paths can be added
- [ ] Variable name input is displayed next to each extraction path
- [ ] Duplicate variable names are highlighted with warning color
- [ ] "Back" button returns to Step 2
- [ ] "Next" button proceeds to Step 4

### Step 4: Confirm & Generate

- [ ] Variable name inputs are displayed for each extraction path
- [ ] Variable names can be edited
- [ ] Duplicate variable names show validation error
- [ ] Code preview section shows generated Python code
- [ ] Generated code includes proper imports
- [ ] Generated code shows `context.get_data()` call with correct parameters
- [ ] Generated code shows variable assignments from extraction paths
- [ ] "Back" button returns to Step 3
- [ ] "Confirm" button is enabled when all validations pass
- [ ] Clicking "Confirm" closes the modal
- [ ] Generated code appears in the precondition textarea
- [ ] Modal can be closed via X button (cancels operation)
- [ ] Modal can be closed via Escape key (cancels operation)

---

## Real ERP Environment Verification (MANUAL-02)

This section verifies the complete data method execution flow with real ERP credentials.

### Task Creation with Data Method

- [ ] Navigate to task creation page
- [ ] Create a new task with name "Data Method Test"
- [ ] Add task description (can include variable placeholders like `{{imei}}`)
- [ ] Click "Get Data" button in precondition section
- [ ] Select `BaseParams.inventory_list_data` method
- [ ] Configure parameters: `i=2`, `j=13`
- [ ] Preview the data method execution
- [ ] Add extraction path: `[0].imei` -> `imei`
- [ ] Confirm and generate code
- [ ] Verify generated code appears in precondition textarea
- [ ] Save the task successfully

### Task Execution with Real ERP

- [ ] Navigate to the created task
- [ ] Click "Run" button to execute the task
- [ ] Verify execution starts (status changes to "Running")
- [ ] Wait for precondition execution to complete
- [ ] Verify precondition status shows success
- [ ] Verify data method executes successfully (no errors in logs)
- [ ] Verify variables are stored in execution context
- [ ] Verify AI execution uses substituted variables (if description contains `{{imei}}`)
- [ ] Verify API assertions receive substituted variables (if configured)
- [ ] Verify execution completes (success or failure based on test expectations)

### Execution Logs Verification

- [ ] Open execution logs/trace
- [ ] Verify `get_data()` call is logged
- [ ] Verify ERP response data is logged (can be truncated for large responses)
- [ ] Verify variable extraction is logged (e.g., "Extracted imei = XXXXX")
- [ ] Verify variable substitution is logged where applicable

---

## Report Display Verification (MANUAL-03)

This section verifies the report page correctly displays data method execution results.

### Navigation to Report

- [ ] Navigate to reports list page
- [ ] Find the report for the executed test
- [ ] Click to open the report details

### Precondition Execution Display

- [ ] Precondition execution status is displayed (success/failure)
- [ ] Precondition execution duration is shown
- [ ] "View Details" or expand option is available for precondition

### Variables Section

- [ ] Variables section is visible in the report
- [ ] Variable names are displayed (e.g., `imei`, `product_name`)
- [ ] Variable values are displayed
- [ ] Variable values match the actual data returned from ERP
- [ ] Variable values are NOT showing `{{variable_name}}` placeholder
- [ ] Multiple variables are listed correctly

### API Assertion Results

- [ ] API assertion results are displayed (if configured)
- [ ] Assertion status is shown (pass/fail)
- [ ] API assertion code shows substituted values (NOT `{{var}}`)
- [ ] Example: If assertion was `response.data.imei == "{{imei}}"`, report shows actual value
- [ ] Assertion error messages are clear (if failed)

### Step Execution Details

- [ ] Each step execution is displayed
- [ ] Step status is shown (success/failure)
- [ ] Step duration is displayed
- [ ] Step details/errors are visible when expanded
- [ ] Variable substitution is visible in step descriptions (if applicable)

### Overall Report Quality

- [ ] Report layout is clean and readable
- [ ] All sections are properly collapsed/expanded
- [ ] No JavaScript console errors in browser dev tools
- [ ] Report can be exported/downloaded (if feature exists)
- [ ] Report can be shared via URL (if feature exists)

---

## Test Scenarios

### Scenario 1: Single Field Extraction (Inventory IMEI)

**Purpose:** Verify basic data retrieval and single field extraction

**Steps:**
1. Create task with `BaseParams.inventory_list_data` method
2. Configure parameters: `i=2`, `j=13`
3. Add extraction: `[0].imei` -> `imei`
4. Execute task

**Verification:**
- [ ] Task executes without errors
- [ ] Report shows variable `imei` with actual value
- [ ] Variable value is a valid IMEI format (e.g., 15 digits)
- [ ] Variable value matches data from ERP preview

### Scenario 2: Multi-field Extraction

**Purpose:** Verify multiple field extraction from single data method call

**Steps:**
1. Create task with `BaseParams.inventory_list_data` method
2. Configure parameters: `i=2`
3. Add extractions:
   - `[0].imei` -> `imei`
   - `[0].product_name` -> `product_name`
4. Execute task

**Verification:**
- [ ] Task executes without errors
- [ ] Report shows both variables: `imei` and `product_name`
- [ ] Both values match ERP data
- [ ] Both values are displayed correctly

### Scenario 3: Variable Substitution in Description

**Purpose:** Verify `{{variable}}` placeholder substitution in task description

**Steps:**
1. Create task with description: "Search for product {{product_name}} with IMEI {{imei}}"
2. Configure data method with extractions for both variables
3. Execute task

**Verification:**
- [ ] AI execution prompt contains substituted values
- [ ] Report shows description with actual values (NOT placeholders)
- [ ] Example: "Search for product [Actual Product Name] with IMEI [Actual IMEI]"

### Scenario 4: Variable Substitution in API Assertion

**Purpose:** Verify `{{variable}}` placeholder substitution in API assertions

**Steps:**
1. Create task with API assertion containing `{{imei}}`
2. Configure data method to extract `imei`
3. Execute task

**Verification:**
- [ ] Assertion code shows substituted value in report
- [ ] Assertion passes if logic is correct
- [ ] Report clearly shows the substituted value used

### Scenario 5: Error Handling - Invalid Method

**Purpose:** Verify graceful error handling for invalid data method

**Steps:**
1. Manually edit precondition code to use invalid method name
2. Execute task

**Verification:**
- [ ] Task fails gracefully with clear error message
- [ ] Error message indicates method not found
- [ ] Report shows failure status
- [ ] No application crash

### Scenario 6: Error Handling - Invalid Extraction Path

**Purpose:** Verify graceful error handling for invalid extraction path

**Steps:**
1. Create task with valid data method
2. Configure extraction path that doesn't exist: `[99].nonexistent_field` -> `var`
3. Execute task

**Verification:**
- [ ] Task fails gracefully with clear error message
- [ ] Error message indicates extraction path not found
- [ ] Report shows failure status
- [ ] No application crash

---

## Results

| Check | Status | Notes |
|-------|--------|-------|
| Environment Setup | [ ] PASS / [ ] FAIL | |
| DataMethodSelector Step 1 | [ ] PASS / [ ] FAIL | |
| DataMethodSelector Step 2 | [ ] PASS / [ ] FAIL | |
| DataMethodSelector Step 3 | [ ] PASS / [ ] FAIL | |
| DataMethodSelector Step 4 | [ ] PASS / [ ] FAIL | |
| Real ERP Execution | [ ] PASS / [ ] FAIL | |
| Variables in Report | [ ] PASS / [ ] FAIL | |
| Scenario 1: Single Extraction | [ ] PASS / [ ] FAIL | |
| Scenario 2: Multi-field | [ ] PASS / [ ] FAIL | |
| Scenario 3: Description Sub | [ ] PASS / [ ] FAIL | |
| Scenario 4: Assertion Sub | [ ] PASS / [ ] FAIL | |
| Scenario 5: Invalid Method | [ ] PASS / [ ] FAIL | |
| Scenario 6: Invalid Path | [ ] PASS / [ ] FAIL | |

**Overall Result:** [ ] PASS / [ ] FAIL

---

## Issues Found

| Issue # | Severity | Description | Reproduction Steps | Status |
|---------|----------|-------------|-------------------|--------|
| 1 | | | | [ ] Open / [ ] Fixed |
| 2 | | | | [ ] Open / [ ] Fixed |
| 3 | | | | [ ] Open / [ ] Fixed |

---

## Screenshots

Capture screenshots for the following scenarios:

| Screenshot | File Name | Description |
|------------|-----------|-------------|
| DataMethodSelector Modal | `dms-modal.png` | Full modal showing 4-step wizard |
| Method Selection | `dms-step1.png` | Step 1 with methods selected |
| Parameter Config | `dms-step2.png` | Step 2 with parameters filled |
| Preview Results | `dms-step3.png` | Step 3 showing JSON preview |
| Generated Code | `dms-step4.png` | Step 4 showing generated code |
| Execution Report | `report-overview.png` | Report page overview |
| Variables Section | `report-variables.png` | Variables section close-up |
| Assertion Substitution | `report-assertion.png` | API assertion with substituted values |

---

## Sign-off

**Tester:** ___________________
**Date:** ___________________
**Signature:** ___________________

---

*Document created for Phase 20-e2e-testing-manual-verification*
*Requirements: MANUAL-01, MANUAL-02, MANUAL-03*
