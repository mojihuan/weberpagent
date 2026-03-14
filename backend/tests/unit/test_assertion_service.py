"""Tests for AssertionService ORM integration."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.assertion_service import AssertionService
from backend.db.repository import AssertionResultRepository, RunRepository, TaskRepository
from backend.db.schemas import TaskCreate
from backend.db.models import Assertion, AssertionResult


class MockHistory:
    """Mock browser-use history object for testing."""

    def __init__(
        self,
        final_url: str | None = None,
        extracted_content: str | None = None,
        is_done: bool = False,
        has_errors: bool = False,
    ):
        self.is_done = is_done
        self._has_errors = has_errors
        if final_url or extracted_content:
            self.final_result = MagicMock()
            self.final_result.url = final_url
            self.final_result.extracted_content = extracted_content
        else:
            self.final_result = None


class TestAssertionServiceInit:
    """Tests for AssertionService initialization."""

    async def test_init_accepts_async_session(self, db_session: AsyncSession):
        """AssertionService.__init__ accepts AsyncSession."""
        service = AssertionService(db_session)
        assert service.session == db_session
        assert isinstance(service.result_repo, AssertionResultRepository)

    async def test_init_creates_result_repo(self, db_session: AsyncSession):
        """AssertionService creates AssertionResultRepository internally."""
        service = AssertionService(db_session)
        assert hasattr(service, "result_repo")
        assert isinstance(service.result_repo, AssertionResultRepository)


class TestAssertionServiceCheckUrlContains:
    """Tests for check_url_contains method."""

    async def test_check_url_contains_returns_tuple(self, db_session: AsyncSession):
        """check_url_contains returns tuple (passed: bool, message: str, actual: str)."""
        service = AssertionService(db_session)
        history = MockHistory(final_url="https://example.com/dashboard", is_done=True)

        passed, message, actual = await service.check_url_contains(history, "dashboard")

        assert isinstance(passed, bool)
        assert isinstance(message, str)
        assert isinstance(actual, str)

    async def test_check_url_contains_passes_when_url_contains_expected(
        self, db_session: AsyncSession
    ):
        """check_url_contains passes when URL contains expected string."""
        service = AssertionService(db_session)
        history = MockHistory(final_url="https://example.com/dashboard", is_done=True)

        passed, message, actual = await service.check_url_contains(history, "dashboard")

        assert passed is True
        assert message == ""
        assert actual == "https://example.com/dashboard"

    async def test_check_url_contains_fails_with_detailed_message(
        self, db_session: AsyncSession
    ):
        """Failed assertion includes detailed message like \"URL 不包含 'dashboard'，实际为 'login'\"."""
        service = AssertionService(db_session)
        history = MockHistory(final_url="https://example.com/login", is_done=True)

        passed, message, actual = await service.check_url_contains(history, "dashboard")

        assert passed is False
        assert "URL 不包含" in message
        assert "dashboard" in message
        assert "login" in message
        assert actual == "https://example.com/login"

    async def test_check_url_contains_handles_no_final_result(
        self, db_session: AsyncSession
    ):
        """check_url_contains handles missing final_result gracefully."""
        service = AssertionService(db_session)
        history = MockHistory()  # No final_result

        passed, message, actual = await service.check_url_contains(history, "dashboard")

        assert passed is False
        assert "无法获取 URL" in message or "URL" in message


class TestAssertionServiceCheckTextExists:
    """Tests for check_text_exists method."""

    async def test_check_text_exists_returns_tuple(self, db_session: AsyncSession):
        """check_text_exists returns tuple (passed: bool, message: str, actual: str)."""
        service = AssertionService(db_session)
        history = MockHistory(
            extracted_content="Welcome to the dashboard", is_done=True
        )

        passed, message, actual = service.check_text_exists(history, "Welcome")

        assert isinstance(passed, bool)
        assert isinstance(message, str)
        assert isinstance(actual, str)

    async def test_check_text_exists_passes_when_text_found(
        self, db_session: AsyncSession
    ):
        """check_text_exists passes when text is found in extracted_content."""
        service = AssertionService(db_session)
        history = MockHistory(
            extracted_content="Welcome to the dashboard", is_done=True
        )

        passed, message, actual = service.check_text_exists(history, "Welcome")

        assert passed is True
        assert message == ""
        assert "Welcome" in actual

    async def test_check_text_exists_fails_with_detailed_message(
        self, db_session: AsyncSession
    ):
        """Failed assertion includes detailed message."""
        service = AssertionService(db_session)
        history = MockHistory(extracted_content="Hello World", is_done=True)

        passed, message, actual = service.check_text_exists(history, "Welcome")

        assert passed is False
        assert "Welcome" in message


class TestAssertionServiceCheckNoErrors:
    """Tests for check_no_errors method."""

    async def test_check_no_errors_returns_tuple(self, db_session: AsyncSession):
        """check_no_errors returns tuple (passed: bool, message: str, actual: str)."""
        service = AssertionService(db_session)
        history = MockHistory(is_done=True)

        passed, message, actual = service.check_no_errors(history)

        assert isinstance(passed, bool)
        assert isinstance(message, str)
        assert isinstance(actual, str)

    async def test_check_no_errors_passes_when_is_done(self, db_session: AsyncSession):
        """check_no_errors passes when history.is_done is True."""
        service = AssertionService(db_session)
        history = MockHistory(is_done=True)

        passed, message, actual = service.check_no_errors(history)

        assert passed is True
        assert message == ""

    async def test_check_no_errors_fails_when_not_done(self, db_session: AsyncSession):
        """check_no_errors fails when history.is_done is False."""
        service = AssertionService(db_session)
        history = MockHistory(is_done=False)

        passed, message, actual = service.check_no_errors(history)

        assert passed is False
        assert message != ""


class TestAssertionServiceCheckElementExists:
    """Tests for check_element_exists method (NEW assertion type)."""

    async def test_check_element_exists_returns_tuple(self, db_session: AsyncSession):
        """check_element_exists returns tuple (passed: bool, message: str, actual: str)."""
        service = AssertionService(db_session)
        history = MockHistory(is_done=True)

        passed, message, actual = await service.check_element_exists(
            history, "#login-button"
        )

        assert isinstance(passed, bool)
        assert isinstance(message, str)
        assert isinstance(actual, str)

    async def test_check_element_exists_passes_when_done(
        self, db_session: AsyncSession
    ):
        """check_element_exists passes when execution completed without errors."""
        service = AssertionService(db_session)
        history = MockHistory(is_done=True)

        passed, message, actual = await service.check_element_exists(
            history, "#login-button"
        )

        assert passed is True
        assert actual == "#login-button"


class TestAssertionServiceEvaluateAll:
    """Tests for evaluate_all method."""

    @pytest.fixture
    async def task_repo(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @pytest.fixture
    async def run_repo(self, db_session: AsyncSession) -> RunRepository:
        return RunRepository(db_session)

    @pytest.fixture
    async def setup_data(
        self, db_session: AsyncSession, task_repo: TaskRepository, run_repo: RunRepository
    ):
        """Create a task with assertions and a run for testing."""
        task = await task_repo.create(
            TaskCreate(name="Test Task", description="Test description")
        )

        # Create assertions
        assertion1 = Assertion(
            task_id=task.id,
            name="Check URL",
            type="url_contains",
            expected="dashboard",
        )
        db_session.add(assertion1)

        assertion2 = Assertion(
            task_id=task.id,
            name="Check Text",
            type="text_exists",
            expected="Welcome",
        )
        db_session.add(assertion2)

        assertion3 = Assertion(
            task_id=task.id,
            name="No Errors",
            type="no_errors",
            expected="true",
        )
        db_session.add(assertion3)

        assertion4 = Assertion(
            task_id=task.id,
            name="Element Exists",
            type="element_exists",
            expected="#submit-button",
        )
        db_session.add(assertion4)

        await db_session.commit()
        await db_session.refresh(assertion1)
        await db_session.refresh(assertion2)
        await db_session.refresh(assertion3)
        await db_session.refresh(assertion4)

        run = await run_repo.create(task_id=task.id)

        return {
            "task": task,
            "assertions": [assertion1, assertion2, assertion3, assertion4],
            "run": run,
        }

    async def test_evaluate_all_returns_list_of_assertion_results(
        self, db_session: AsyncSession, setup_data
    ):
        """evaluate_all() returns list[AssertionResult] and stores to database."""
        service = AssertionService(db_session)
        history = MockHistory(
            final_url="https://example.com/dashboard",
            extracted_content="Welcome to the app",
            is_done=True,
        )

        results = await service.evaluate_all(
            run_id=setup_data["run"].id,
            assertions=setup_data["assertions"],
            history=history,
        )

        assert isinstance(results, list)
        assert len(results) == 4
        for result in results:
            assert isinstance(result, AssertionResult)

    async def test_evaluate_all_stores_results_to_database(
        self, db_session: AsyncSession, setup_data
    ):
        """evaluate_all() stores results to database via AssertionResultRepository."""
        service = AssertionService(db_session)
        history = MockHistory(
            final_url="https://example.com/dashboard",
            extracted_content="Welcome to the app",
            is_done=True,
        )

        results = await service.evaluate_all(
            run_id=setup_data["run"].id,
            assertions=setup_data["assertions"],
            history=history,
        )

        # Verify results are stored by checking they have IDs
        for result in results:
            assert result.id is not None
            assert result.run_id == setup_data["run"].id

    async def test_evaluate_all_handles_failed_assertions(
        self, db_session: AsyncSession, setup_data
    ):
        """evaluate_all() handles failed assertions with detailed messages."""
        service = AssertionService(db_session)
        # History that will fail URL check
        history = MockHistory(
            final_url="https://example.com/login",
            extracted_content="Welcome to the app",
            is_done=True,
        )

        results = await service.evaluate_all(
            run_id=setup_data["run"].id,
            assertions=setup_data["assertions"],
            history=history,
        )

        # Find the URL assertion result
        url_result = next(
            r for r in results if r.assertion_id == setup_data["assertions"][0].id
        )
        assert url_result.status == "fail"
        assert "URL 不包含" in url_result.message
        assert "dashboard" in url_result.message

    async def test_evaluate_all_handles_unknown_assertion_type(
        self, db_session: AsyncSession, task_repo: TaskRepository, run_repo: RunRepository
    ):
        """evaluate_all() handles unknown assertion types gracefully."""
        task = await task_repo.create(
            TaskCreate(name="Test Task", description="Test description")
        )

        # Create assertion with unknown type
        unknown_assertion = Assertion(
            task_id=task.id,
            name="Unknown Type",
            type="unknown_type",
            expected="something",
        )
        db_session.add(unknown_assertion)
        await db_session.commit()
        await db_session.refresh(unknown_assertion)

        run = await run_repo.create(task_id=task.id)

        service = AssertionService(db_session)
        history = MockHistory(is_done=True)

        results = await service.evaluate_all(
            run_id=run.id,
            assertions=[unknown_assertion],
            history=history,
        )

        assert len(results) == 1
        assert results[0].status == "fail"
        assert "未知断言类型" in results[0].message


class TestAssertionServiceBackwardCompatibility:
    """Tests for backward compatibility with existing run_all_assertions method."""

    async def test_run_all_assertions_still_exists(self, db_session: AsyncSession):
        """run_all_assertions method still exists for backward compatibility."""
        service = AssertionService(db_session)
        assert hasattr(service, "run_all_assertions")

    async def test_run_all_assertions_returns_dict(self, db_session: AsyncSession):
        """run_all_assertions returns dict[str, bool] for backward compatibility."""
        service = AssertionService(db_session)
        history = MockHistory(
            final_url="https://example.com/dashboard",
            extracted_content="Welcome",
            is_done=True,
        )

        from backend.api.schemas.index import Assertion as AssertionSchema

        assertions = [
            AssertionSchema(name="URL Check", type="url_contains", expected="dashboard"),
            AssertionSchema(name="Text Check", type="text_exists", expected="Welcome"),
        ]

        results = await service.run_all_assertions(history, assertions)

        assert isinstance(results, dict)
        assert "URL Check" in results
        assert "Text Check" in results
