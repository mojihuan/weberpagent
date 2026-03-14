"""Unit tests for ORM models (Assertion and AssertionResult)."""

import pytest
from datetime import datetime

from backend.db.models import Task, Run, Assertion


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        "name": "Test Task",
        "description": "A test task for unit testing",
        "target_url": "https://example.com",
        "max_steps": 10,
        "status": "draft",
    }


@pytest.fixture
def sample_run_data():
    """Sample run data for testing"""
    return {
        "status": "pending",
    }


@pytest.fixture
def sample_assertion_data():
    """Sample assertion data for testing"""
    return {
        "name": "Check URL contains login",
        "type": "url_contains",
        "expected": "/login",
    }


# ============================================================================
# Task Model Tests (existing, for reference)
# ============================================================================


def test_task_model(sample_task_data):
    """Task model has all required fields"""
    task = Task(**sample_task_data)

    assert task.name == "Test Task"
    assert task.description == "A test task for unit testing"
    assert task.target_url == "https://example.com"
    assert task.max_steps == 10
    assert task.status == "draft"
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_run_relationship(sample_task_data, sample_run_data):
    """Task has runs relationship"""
    task = Task(**sample_task_data)
    run = Run(**sample_run_data, task=task)

    assert run in task.runs
    assert run.task == task


# ============================================================================
# Task 1: Assertion Model Tests
# ============================================================================


def test_assertion_model(sample_assertion_data):
    """Assertion model has id, task_id, name, type, expected, created_at fields"""
    assertion = Assertion(
        id="abc12345",
        task_id="task1234",
        **sample_assertion_data,
    )

    assert assertion.id == "abc12345"
    assert assertion.task_id == "task1234"
    assert assertion.name == "Check URL contains login"
    assert assertion.type == "url_contains"
    assert assertion.expected == "/login"
    # created_at is set on flush to database, field definition is verified via inspection
    from sqlalchemy import inspect
    mapper = inspect(Assertion)
    assert "created_at" in mapper.columns


def test_assertion_task_id_foreign_key():
    """Assertion.task_id is ForeignKey to tasks.id"""
    from sqlalchemy import inspect

    mapper = inspect(Assertion)
    task_id_column = mapper.columns["task_id"]

    # Verify it's a ForeignKey
    assert task_id_column.foreign_keys is not None
    fk = list(task_id_column.foreign_keys)[0]
    assert fk.target_fullname == "tasks.id"


def test_assertion_task_relationship(sample_task_data, sample_assertion_data):
    """Assertion has relationship to Task via back_populates"""
    task = Task(**sample_task_data)
    assertion = Assertion(**sample_assertion_data, task=task)

    # Bidirectional relationship
    assert assertion.task == task
    assert assertion in task.assertions


# ============================================================================
# Task 2: AssertionResult Model Tests (skip until Task 2)
# ============================================================================


@pytest.mark.skip(reason="AssertionResult model will be implemented in Task 2")
def test_assertion_result_model():
    """AssertionResult model has id, run_id, assertion_id, status, message, actual_value, created_at fields"""
    pass


@pytest.mark.skip(reason="AssertionResult model will be implemented in Task 2")
def test_assertion_result_run_id_foreign_key():
    """AssertionResult.run_id is ForeignKey to runs.id"""
    pass


@pytest.mark.skip(reason="AssertionResult model will be implemented in Task 2")
def test_assertion_result_assertion_id_foreign_key():
    """AssertionResult.assertion_id is ForeignKey to assertions.id"""
    pass


# ============================================================================
# Task 3: Relationship Tests (skip until Task 3)
# ============================================================================


@pytest.mark.skip(reason="Full relationship tests will be implemented in Task 3")
def test_assertion_relationships():
    """Test bidirectional relationships and cascade delete"""
    pass
