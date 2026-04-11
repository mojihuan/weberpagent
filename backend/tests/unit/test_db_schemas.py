"""Tests for DB layer Pydantic schemas (AssertionResponse, AssertionResultResponse)."""

import pytest
from datetime import datetime

from backend.db.schemas import AssertionResponse, AssertionResultResponse


class TestAssertionResponse:
    """Tests for AssertionResponse schema."""

    def test_assertion_response_has_all_fields(self):
        """AssertionResponse has all required fields from Assertion ORM model."""
        response = AssertionResponse(
            id="abc12345",
            task_id="task0001",
            name="URL Check",
            type="url_contains",
            expected="/dashboard",
            created_at=datetime(2026, 1, 1, 12, 0, 0),
        )
        assert response.id == "abc12345"
        assert response.task_id == "task0001"
        assert response.name == "URL Check"
        assert response.type == "url_contains"
        assert response.expected == "/dashboard"
        assert response.created_at == datetime(2026, 1, 1, 12, 0, 0)

    def test_assertion_response_from_attributes(self):
        """AssertionResponse can be created from ORM model instance (from_attributes)."""
        # Mock ORM model with matching attributes
        class MockAssertion:
            id = "xyz98765"
            task_id = "task0002"
            name = "Text Check"
            type = "text_exists"
            expected = "Welcome"
            created_at = datetime(2026, 3, 14, 9, 0, 0)

        response = AssertionResponse.model_validate(MockAssertion())
        assert response.id == "xyz98765"
        assert response.task_id == "task0002"
        assert response.name == "Text Check"
        assert response.type == "text_exists"
        assert response.expected == "Welcome"

    def test_assertion_response_type_variants(self):
        """AssertionResponse supports all assertion types."""
        for assertion_type in ["url_contains", "text_exists", "no_errors"]:
            response = AssertionResponse(
                id="test0001",
                task_id="task0001",
                name=f"Test {assertion_type}",
                type=assertion_type,
                expected="some value",
                created_at=datetime.now(),
            )
            assert response.type == assertion_type


class TestAssertionResultResponse:
    """Tests for AssertionResultResponse schema."""

    def test_assertion_result_response_has_all_fields(self):
        """AssertionResultResponse has all required fields from AssertionResult ORM model."""
        response = AssertionResultResponse(
            id="result001",
            run_id="run00001",
            assertion_id="assert01",
            status="pass",
            message="URL contains expected path",
            actual_value="/dashboard/home",
            created_at=datetime(2026, 1, 1, 12, 30, 0),
        )
        assert response.id == "result001"
        assert response.run_id == "run00001"
        assert response.assertion_id == "assert01"
        assert response.status == "pass"
        assert response.message == "URL contains expected path"
        assert response.actual_value == "/dashboard/home"
        assert response.created_at == datetime(2026, 1, 1, 12, 30, 0)

    def test_assertion_result_response_from_attributes(self):
        """AssertionResultResponse can be created from ORM model instance (from_attributes)."""
        # Mock ORM model with matching attributes
        class MockAssertionResult:
            id = "result002"
            run_id = "run00002"
            assertion_id = "assert02"
            status = "fail"
            message = "Expected text not found"
            actual_value = "Page content without expected text"
            created_at = datetime(2026, 3, 14, 10, 0, 0)

        response = AssertionResultResponse.model_validate(MockAssertionResult())
        assert response.id == "result002"
        assert response.run_id == "run00002"
        assert response.assertion_id == "assert02"
        assert response.status == "fail"
        assert response.message == "Expected text not found"

    def test_assertion_result_response_optional_fields(self):
        """AssertionResultResponse handles optional fields (message, actual_value)."""
        response = AssertionResultResponse(
            id="result003",
            run_id="run00003",
            assertion_id="assert03",
            status="pass",
            created_at=datetime.now(),
        )
        assert response.message is None
        assert response.actual_value is None

    def test_assertion_result_response_status_variants(self):
        """AssertionResultResponse supports pass and fail status."""
        for status in ["pass", "fail"]:
            response = AssertionResultResponse(
                id=f"result_{status}",
                run_id="run00001",
                assertion_id="assert01",
                status=status,
                created_at=datetime.now(),
            )
            assert response.status == status


class TestTaskLoginRole:
    """Tests for login_role field in Task schemas."""

    def test_task_create_with_login_role(self):
        from backend.db.schemas import TaskCreate

        tc = TaskCreate(name="Test", description="Desc", login_role="main")
        assert tc.login_role == "main"

    def test_task_create_without_login_role(self):
        from backend.db.schemas import TaskCreate

        tc = TaskCreate(name="Test", description="Desc")
        assert tc.login_role is None

    def test_task_update_login_role(self):
        from backend.db.schemas import TaskUpdate

        tu = TaskUpdate(login_role="special")
        assert tu.login_role == "special"

    def test_task_update_login_role_clear(self):
        from backend.db.schemas import TaskUpdate

        tu = TaskUpdate(login_role=None)
        assert tu.login_role is None

    def test_task_response_from_orm_includes_login_role(self):
        from backend.db.schemas import TaskResponse
        from datetime import datetime

        class MockTask:
            id = "test1234"
            name = "Test"
            description = "Desc"
            target_url = ""
            max_steps = 10
            status = "draft"
            created_at = datetime(2026, 4, 11)
            updated_at = datetime(2026, 4, 11)
            preconditions = None
            external_assertions = None
            login_role = "main"

        response = TaskResponse.model_validate(MockTask())
        assert response.login_role == "main"

    def test_task_response_from_orm_login_role_none(self):
        from backend.db.schemas import TaskResponse
        from datetime import datetime

        class MockTask:
            id = "test1234"
            name = "Test"
            description = "Desc"
            target_url = ""
            max_steps = 10
            status = "draft"
            created_at = datetime(2026, 4, 11)
            updated_at = datetime(2026, 4, 11)
            preconditions = None
            external_assertions = None
            login_role = None

        response = TaskResponse.model_validate(MockTask())
        assert response.login_role is None
