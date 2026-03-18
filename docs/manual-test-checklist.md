# Manual Test Checklist: Precondition Integration

This checklist validates the complete precondition integration with a real webseleniumerp project.

## Prerequisites

- [ ] webseleniumerp project cloned locally
- [ ] `config/settings.py` created in webseleniumerp (see README.md for template)
- [ ] Backend server running: `uv run uvicorn backend.api.main:app --reload --port 8080`
- [ ] Frontend server running: `cd frontend && npm run dev`

## Environment Setup

1. Add to `.env`:
   ```
   WEBSERP_PATH=/path/to/your/webseleniumerp
   ```
2. Restart backend server to load new configuration

---

## Test 1: Complete Flow (VAL-01)

**Purpose:** Verify complete flow from operation code selection to precondition execution

### Steps:

1. [ ] Open frontend at http://localhost:5173
2. [ ] Navigate to Task creation page
3. [ ] Click "Select Operation Codes" button above precondition textarea
4. [ ] Verify: Modal shows operation codes grouped by module
5. [ ] Select operation codes: FA1, HC1
6. [ ] Click "Confirm" button
7. [ ] Verify: Precondition textarea contains generated code with:
   - `sys.path.insert(0, '/path/to/webseleniumerp')`
   - `from common.base_prerequisites import PreFront`
   - `pre_front.operations(['FA1', 'HC1'])`
8. [ ] Create and run the task
9. [ ] Verify: Task execution includes precondition step
10. [ ] Verify: Precondition execution shows success status

### Expected Results:

- [ ] Operation codes load successfully from real webseleniumerp
- [ ] Generated code is valid Python
- [ ] Precondition executes without errors
- [ ] Context variable `precondition_result` is set to 'success'

---

## Test 2: Error - Path Not Configured (VAL-02)

**Purpose:** Verify error handling when WEBSERP_PATH is not set

### Steps:

1. [ ] Remove or comment out WEBSERP_PATH in `.env`
2. [ ] Restart backend server
3. [ ] Try to open operation code selector in frontend
4. [ ] Verify: Button shows error tooltip or is disabled

### Expected Results:

- [ ] API returns 503 Service Unavailable
- [ ] Frontend shows appropriate error message
- [ ] Error message mentions WEBSERP_PATH configuration

---

## Test 3: Error - Path Doesn't Exist (VAL-02)

**Purpose:** Verify error handling when WEBSERP_PATH points to invalid location

### Steps:

1. [ ] Set WEBSERP_PATH to non-existent path: `WEBSERP_PATH=/nonexistent/path`
2. [ ] Restart backend server
3. [ ] Check startup logs for validation error

### Expected Results:

- [ ] Backend startup shows error message: "WEBSERP_PATH directory not found"
- [ ] Error includes solution hint

---

## Test 4: Error - Missing config/settings.py (VAL-02)

**Purpose:** Verify error handling when webseleniumerp config is missing

### Steps:

1. [ ] Set WEBSERP_PATH correctly
2. [ ] Rename or delete `webseleniumerp/config/settings.py`
3. [ ] Restart backend server
4. [ ] Check startup logs for validation error

### Expected Results:

- [ ] Backend startup shows error message: "config/settings.py not found"
- [ ] Error includes template for creating the file

---

## Test 5: Error - Execution Exception (VAL-02)

**Purpose:** Verify error handling when PreFront.operations() throws exception

### Steps:

1. [ ] Configure valid WEBSERP_PATH
2. [ ] Create a precondition with code that raises exception:
   ```python
   raise ValueError("Test exception")
   ```
3. [ ] Run the task
4. [ ] Check execution result

### Expected Results:

- [ ] Precondition execution shows failure status
- [ ] Error message contains exception details
- [ ] Task does not proceed to main steps

---

## Sign-off

- [ ] All tests completed
- [ ] All expected results verified
- [ ] Issues documented: _______________

**Tester:** _______________
**Date:** _______________
**Environment:** _______________
