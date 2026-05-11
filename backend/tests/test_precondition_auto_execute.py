"""Tests for auto-execution of precondition operation codes."""
import pytest
from unittest.mock import patch

from backend.core.precondition_service import PreconditionService


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
    """If execute_operations raises, the precondition should be marked as failed."""
    code = "context['preconditions'] = ['INVALID']"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        mock_exec.side_effect = RuntimeError("Unknown operation code")
        result = await service.execute_single(code, 0)

    assert result.success is False
    assert "Unknown operation code" in result.error


# --- Test 4: Idempotency — already-executed codes are skipped ---
@pytest.mark.asyncio
async def test_no_double_execution(service):
    """If an operation code was already executed, don't execute it again."""
    service.context['_executed_operations'] = {'FA1'}
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


# --- Test 6: Empty list — no auto-execute ---
@pytest.mark.asyncio
async def test_no_auto_execute_for_empty_list(service):
    """If context['preconditions'] is an empty list, don't auto-execute."""
    code = "context['preconditions'] = []"

    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        result = await service.execute_single(code, 0)

    assert result.success is True
    mock_exec.assert_not_called()


# --- Test 7: Multiple preconditions only execute new codes ---
@pytest.mark.asyncio
async def test_second_precondition_only_executes_new_codes(service):
    """Second precondition with partially overlapping codes only executes new ones."""
    # First precondition: execute FA1 + HC1
    code1 = "context['preconditions'] = ['FA1', 'HC1']"
    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        mock_exec.return_value = (True, "ok", {})
        result1 = await service.execute_single(code1, 0)

    assert result1.success is True
    mock_exec.assert_called_once_with(['FA1', 'HC1'])

    # Second precondition: only HB2 is new
    code2 = "context['preconditions'] = ['FA1', 'HB2']"
    with patch(
        "backend.core.precondition_service.execute_operations"
    ) as mock_exec:
        mock_exec.return_value = (True, "ok", {})
        result2 = await service.execute_single(code2, 1)

    assert result2.success is True
    mock_exec.assert_called_once_with(['HB2'])
