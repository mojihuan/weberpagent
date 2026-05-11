# Auto-Execute Precondition Operations — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Auto-detect `context['preconditions'] = ['FA1', 'HC1']` pattern in precondition code and call `execute_operations()` so ERP data is actually generated before `get_data()` queries it.

**Architecture:** Insert detection logic in `PreconditionService.execute_single()` after `exec()` completes. If `context['preconditions']` is a `list[str]` and hasn't been executed yet, call `execute_operations()` from `external_execution_engine.py`. Use `_operations_executed` flag for idempotency.

**Tech Stack:** Python 3.11+, pytest, unittest.mock

---

### Task 1: Write failing tests for auto-execute behavior

**Files:**
- Create: `backend/tests/test_precondition_auto_execute.py`

**Step 1: Write the test file**

```python
"""Tests for auto-execution of precondition operation codes."""
import pytest
from unittest.mock import patch, MagicMock

from backend.core.precondition_service import PreconditionService, ContextWrapper


@pytest.fixture
def service():
    return PreconditionService()


# --- Test 1: Auto-detect triggers execute_operations ---
@pytest.mark.asyncio
async def test_auto_execute_triggers_on_preconditions_key(service):
    """When code sets context['preconditions'] = ['FA1', 'HC1'],
    execute_operations should be called automatically."""
    code = "context['preconditions'] = ['FA1', 'HC1']"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        mock_exec.return_value = (True, "ok", {})
        result = await service.execute_single(code, 0)

    assert result.success is True
    mock_exec.assert_called_once_with(['FA1', 'HC1'])


# --- Test 2: No auto-execute when preconditions key absent ---
@pytest.mark.asyncio
async def test_no_auto_execute_without_preconditions_key(service):
    """Code that doesn't set context['preconditions'] should not trigger execute_operations."""
    code = "context['x'] = 42"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        result = await service.execute_single(code, 0)

    assert result.success is True
    mock_exec.assert_not_called()


# --- Test 3: Failure in execute_operations propagates ---
@pytest.mark.asyncio
async def test_auto_execute_failure_propagates(service):
    """If execute_operations fails, the precondition should be marked as failed."""
    code = "context['preconditions'] = ['INVALID']"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        mock_exec.return_value = (False, "Unknown operation code", {})
        result = await service.execute_single(code, 0)

    assert result.success is False
    assert "Unknown operation code" in result.error


# --- Test 4: Idempotency — no double execution ---
@pytest.mark.asyncio
async def test_no_double_execution(service):
    """If _operations_executed is already True, don't execute again."""
    service.context['_operations_executed'] = True
    service.context['preconditions'] = ['FA1']

    code = "context['preconditions'] = ['FA1']"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        result = await service.execute_single(code, 0)

    assert result.success is True
    mock_exec.assert_not_called()


# --- Test 5: preconditions is not a list — no auto-execute ---
@pytest.mark.asyncio
async def test_no_auto_execute_for_non_list(service):
    """If context['preconditions'] is not a list, don't auto-execute."""
    code = "context['preconditions'] = 'FA1'"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        result = await service.execute_single(code, 0)

    assert result.success is True
    mock_exec.assert_not_called()
```

**Step 2: Run tests to verify they fail**

Run: `cd /Users/huhu/project/weberpagent && uv run pytest backend/tests/test_precondition_auto_execute.py -v`

Tests 1, 3 should FAIL (auto-execute not implemented yet).
Tests 2, 4, 5 should PASS (no change needed for non-trigger cases — but test 4 may fail if `_operations_executed` logic isn't there).

Expected: At least test 1 and test 3 FAIL with `AttributeError` or `assert not called`.

**Step 3: Commit the test file**

```bash
git add backend/tests/test_precondition_auto_execute.py
git commit -m "test: add failing tests for auto-execute precondition operations"
```

---

### Task 2: Implement auto-execute logic in execute_single()

**Files:**
- Modify: `backend/core/precondition_service.py:362-370` (the try block in `execute_single`)

**Step 1: Add import and auto-execute logic**

In `precondition_service.py`, at the top of the file, add the import:

```python
from backend.core.external_execution_engine import execute_operations
```

Then in `execute_single()`, inside the try block, **after** the `await asyncio.wait_for(...)` line and **before** `result.success = True`, insert:

```python
            # Auto-execute precondition operation codes if present
            op_codes = self.context.get('preconditions')
            if (
                isinstance(op_codes, list)
                and not self.context.get('_operations_executed')
            ):
                success, error, _ = execute_operations(op_codes)
                if not success:
                    raise RuntimeError(
                        f"Precondition operations failed: {error}"
                    )
                self.context['_operations_executed'] = True
                logger.info(
                    f"前置条件 {index}: 自动执行操作码 {op_codes}"
                )
```

The full try block should look like:

```python
        try:
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, lambda: exec(code, env)),
                timeout=timeout
            )

            # Auto-execute precondition operation codes if present
            op_codes = self.context.get('preconditions')
            if (
                isinstance(op_codes, list)
                and not self.context.get('_operations_executed')
            ):
                success, error, _ = execute_operations(op_codes)
                if not success:
                    raise RuntimeError(
                        f"Precondition operations failed: {error}"
                    )
                self.context['_operations_executed'] = True
                logger.info(
                    f"前置条件 {index}: 自动执行操作码 {op_codes}"
                )

            result.success = True
            result.variables = self.context.to_dict()
            logger.info(f"前置条件 {index} 执行成功，变量: {list(result.variables.keys())}")
```

**Step 2: Run all tests to verify**

Run: `cd /Users/huhu/project/weberpagent && uv run pytest backend/tests/test_precondition_auto_execute.py -v`

Expected: All 5 tests PASS.

**Step 3: Run full test suite to verify no regressions**

Run: `cd /Users/huhu/project/weberpagent && uv run pytest backend/tests/ -v`

Expected: All existing tests still pass.

**Step 4: Commit**

```bash
git add backend/core/precondition_service.py
git commit -m "feat: auto-execute precondition operation codes from context['preconditions']"
```

---

### Task 3: Run tests and verify end-to-end

**Files:** None (verification only)

**Step 1: Run full test suite**

Run: `cd /Users/huhu/project/weberpagent && uv run pytest backend/tests/ -v`

Expected: All tests pass.

**Step 2: Verify the fix works with the user's actual scenario**

The user's Excel precondition code:

```python
# Element 1: now auto-executes FA1 + HC1
context['preconditions'] = ['FA1', 'HC1']

# Element 2: now queries fresh data from the operations above
items = context.get_data('PcImport', '库存管理|库存列表', i=2, j=13)
context.fill_excel('new_purchase_order', row=2, col=1, value=items[0]['imei'])
context['excel_file'] = context.get_excel_path('new_purchase_order')
```

Element 1 will now:
1. Store `['FA1', 'HC1']` in context
2. Auto-detect after exec
3. Call `execute_operations(['FA1', 'HC1'])` → creates new purchase order + sales outbound in ERP
4. Set `_operations_executed = True`

Element 2 will then:
1. `get_data` queries ERP → gets fresh data including the newly created items
2. Fills Excel with the new IMEI
3. Stores file path in context
