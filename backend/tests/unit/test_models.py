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
    from sqlalchemy import inspect

    task = Task(**sample_task_data)

    assert task.name == "Test Task"
    assert task.description == "A test task for unit testing"
    assert task.target_url == "https://example.com"
    assert task.max_steps == 10
    assert task.status == "draft"
    # created_at and updated_at are set on flush to database
    # Verify field definitions via inspection
    mapper = inspect(Task)
    assert "created_at" in mapper.columns
    assert "updated_at" in mapper.columns


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
# Task 2: AssertionResult Model Tests
# ============================================================================


def test_assertion_result_model():
    """AssertionResult model has id, run_id, assertion_id, status, message, actual_value, created_at fields"""
    from backend.db.models import AssertionResult

    assertion_result = AssertionResult(
        id="res12345",
        run_id="run12345",
        assertion_id="assert123",
        status="pass",
        message="URL matched expected pattern",
        actual_value="/login/page",
    )

    assert assertion_result.id == "res12345"
    assert assertion_result.run_id == "run12345"
    assert assertion_result.assertion_id == "assert123"
    assert assertion_result.status == "pass"
    assert assertion_result.message == "URL matched expected pattern"
    assert assertion_result.actual_value == "/login/page"
    # created_at is set on flush to database, field definition is verified via inspection
    from sqlalchemy import inspect
    mapper = inspect(AssertionResult)
    assert "created_at" in mapper.columns


def test_assertion_result_run_id_foreign_key():
    """AssertionResult.run_id is ForeignKey to runs.id"""
    from sqlalchemy import inspect
    from backend.db.models import AssertionResult

    mapper = inspect(AssertionResult)
    run_id_column = mapper.columns["run_id"]

    assert run_id_column.foreign_keys is not None
    fk = list(run_id_column.foreign_keys)[0]
    assert fk.target_fullname == "runs.id"


def test_assertion_result_assertion_id_foreign_key():
    """AssertionResult.assertion_id is ForeignKey to assertions.id"""
    from sqlalchemy import inspect
    from backend.db.models import AssertionResult

    mapper = inspect(AssertionResult)
    assertion_id_column = mapper.columns["assertion_id"]

    assert assertion_id_column.foreign_keys is not None
    fk = list(assertion_id_column.foreign_keys)[0]
    assert fk.target_fullname == "assertions.id"


# ============================================================================
# Task 3: Relationship Tests
# ============================================================================


def test_assertion_relationships(sample_task_data, sample_run_data, sample_assertion_data):
    """Test bidirectional relationships and cascade delete"""
    from backend.db.models import AssertionResult

    # Create objects
    task = Task(**sample_task_data)
    run = Run(**sample_run_data, task=task)
    assertion = Assertion(**sample_assertion_data, task=task)
    assertion_result = AssertionResult(
        run=run,
        assertion=assertion,
        status="pass",
        message="Test passed",
    )

    # Test bidirectional access
    # Task -> Assertion
    assert assertion in task.assertions
    assert assertion.task == task

    # Run -> AssertionResult
    assert assertion_result in run.assertion_results
    assert assertion_result.run == run

    # AssertionResult -> Assertion
    assert assertion_result.assertion == assertion
    assert assertion_result in assertion.results


def test_task_assertion_cascade_delete(sample_task_data, sample_assertion_data):
    """Deleting Task cascades to delete Assertion records"""
    from sqlalchemy import inspect

    task = Task(**sample_task_data)
    assertion = Assertion(**sample_assertion_data, task=task)

    # Verify cascade is configured on Task.assertions relationship
    # "all, delete-orphan" expands to individual cascade options
    task_mapper = inspect(Task)
    assertions_rel = task_mapper.relationships["assertions"]
    assert "delete" in assertions_rel.cascade
    assert "delete-orphan" in assertions_rel.cascade


def test_run_assertion_result_cascade_delete():
    """Run.assertion_results relationship has cascade delete configured"""
    from sqlalchemy import inspect
    from backend.db.models import AssertionResult

    run_mapper = inspect(Run)
    assertion_results_rel = run_mapper.relationships["assertion_results"]
    assert "delete" in assertion_results_rel.cascade
    assert "delete-orphan" in assertion_results_rel.cascade


# ============================================================================
# Task: Step.loop_intervention field tests (Phase 39, LOG-01)
# ============================================================================


def test_step_loop_intervention_field_exists():
    """Step model has loop_intervention Text field for storing diagnostic JSON"""
    from sqlalchemy import inspect
    from backend.db.models import Step

    mapper = inspect(Step)
    assert "loop_intervention" in mapper.columns
    # Verify it's a Text column
    col = mapper.columns["loop_intervention"]
    assert col.type.__class__.__name__ == "Text"


def test_step_loop_intervention_nullable():
    """Step.loop_intervention is Optional (nullable=True)"""
    from sqlalchemy import inspect
    from backend.db.models import Step

    mapper = inspect(Step)
    col = mapper.columns["loop_intervention"]
    assert col.nullable is True


def test_step_loop_intervention_stores_json():
    """Step can store and retrieve JSON string in loop_intervention"""
    from backend.db.models import Step
    import json

    diagnostic = {
        "stagnation": 5,
        "max_repetition_count": 3,
        "recent_actions": [{"action": "click", "params": {"index": 1}}],
        "intervention_triggered": True,
    }
    json_str = json.dumps(diagnostic, ensure_ascii=False)

    step = Step(
        run_id="run12345",
        step_index=1,
        action="click",
        status="success",
        loop_intervention=json_str,
    )

    assert step.loop_intervention == json_str
    # Verify it can be parsed back
    parsed = json.loads(step.loop_intervention)
    assert parsed["stagnation"] == 5
    assert parsed["intervention_triggered"] is True


# ============================================================================
# Task login_role field tests (Phase 76, DATA-01)
# ============================================================================


def test_task_login_role_field_exists():
    """Task model has login_role VARCHAR(20) nullable column."""
    from sqlalchemy import inspect

    mapper = inspect(Task)
    assert "login_role" in mapper.columns
    col = mapper.columns["login_role"]
    assert col.nullable is True


def test_task_login_role_default_none():
    """Task login_role defaults to None when not specified."""
    task = Task(name="Test", description="Test desc")
    assert task.login_role is None
