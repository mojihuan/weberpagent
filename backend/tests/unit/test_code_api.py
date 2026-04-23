"""Unit tests for GET /runs/{run_id}/code endpoint (CODE-01)
and POST /runs/{run_id}/execute-code endpoint (CODE-02, CODE-03, STATUS-01).

Tests mock RunRepository via FastAPI dependency overrides to avoid real
database dependencies.

Covers:
  CODE-01:
  1. Success: returns line-numbered code text (D-01)
  2. No code: generated_code_path is null
  3. File not found: code file missing on disk
  4. Path traversal: code path outside outputs/ directory (D-03)
  5. Run not found: run_id does not exist

  CODE-02 / CODE-03 / STATUS-01:
  6. Execute accepted: POST /execute-code returns 202 with healing status
  7. Execute no code: returns 400 when generated_code_path is null
  8. Execute no role: returns 400 when task has no login_role
  9. Execute concurrent 409: returns 409 when run_id is already active
  10. Task status success on pass: background task updates Task.status to "success"
  11. Healing status reflects execution result: passed and failed cases
"""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.api.routes.runs import get_run_repo
from backend.db.repository import RunRepository
from backend.db.schemas import TaskUpdate


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Create test client with dependency overrides ready.

    Tests must set app.dependency_overrides[get_run_repo] themselves
    to control the mock repository per test case.
    """
    tc = TestClient(app)
    yield tc
    app.dependency_overrides.clear()


def _make_run(run_id="run-001", generated_code_path=None):
    """Create a mock Run object with the given attributes."""
    run = MagicMock()
    run.id = run_id
    run.task_id = "task-001"
    run.generated_code_path = generated_code_path
    run.status = "success"
    return run


def _make_run_repo(run=None):
    """Create a mock RunRepository whose .get() returns the given run."""
    repo = MagicMock(spec=RunRepository)
    repo.get = AsyncMock(return_value=run)
    return repo


def _override_repo(repo):
    """Register a dependency override for get_run_repo."""
    def _override():
        return repo
    app.dependency_overrides[get_run_repo] = _override


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGetRunCode:
    """Tests for GET /runs/{run_id}/code endpoint."""

    def test_get_code_success(self, client, tmp_path):
        """GET /runs/{run_id}/code returns 200 with line-numbered code text."""
        # Create a real temp file inside an outputs/ subdirectory so that
        # _validate_code_path's containment check (outputs root) can pass
        # when the CWD-relative "outputs" happens to resolve differently.
        # We patch _validate_code_path to bypass filesystem constraints.
        code_file = tmp_path / "test_generated.py"
        code_file.write_text("def test_xxx():\n    pass", encoding="utf-8")

        run = _make_run(generated_code_path=str(code_file))
        run_repo = _make_run_repo(run)
        _override_repo(run_repo)

        from unittest.mock import patch
        with patch("backend.api.routes.runs._validate_code_path", return_value=code_file):
            response = client.get("/api/runs/run-001/code")

        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")
        body = response.text
        assert "1 | def test_xxx():" in body
        assert "2 |     pass" in body

    def test_get_code_no_code(self, client):
        """GET /runs/{run_id}/code returns 404 when generated_code_path is null."""
        run = _make_run(generated_code_path=None)
        run_repo = _make_run_repo(run)
        _override_repo(run_repo)

        response = client.get("/api/runs/run-002/code")

        assert response.status_code == 404
        data = response.json()
        # Global exception handler wraps detail in error.message
        message = data.get("error", {}).get("message", "")
        assert "无生成代码" in message

    def test_get_code_file_not_found(self, client):
        """GET /runs/{run_id}/code returns 404 when code file does not exist on disk."""
        # Use a path under outputs/ so path traversal check passes,
        # but the file does not actually exist on disk.
        run = _make_run(generated_code_path="outputs/nonexistent_test_file.py")
        run_repo = _make_run_repo(run)
        _override_repo(run_repo)

        response = client.get("/api/runs/run-003/code")

        assert response.status_code == 404

    def test_get_code_path_traversal(self, client):
        """GET /runs/{run_id}/code returns 403 for path outside outputs/ directory."""
        run = _make_run(generated_code_path="/etc/passwd")
        run_repo = _make_run_repo(run)
        _override_repo(run_repo)

        response = client.get("/api/runs/run-004/code")

        assert response.status_code == 403

    def test_get_code_run_not_found(self, client):
        """GET /runs/{run_id}/code returns 404 when run_id does not exist."""
        run_repo = _make_run_repo(run=None)
        _override_repo(run_repo)

        response = client.get("/api/runs/nonexistent/code")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# CODE-02: POST /execute-code tests
# ---------------------------------------------------------------------------

class TestExecuteRunCode:
    """Tests for POST /runs/{run_id}/execute-code endpoint."""

    def _make_run_with_task(self, run_id="testrun1", code_path="outputs/testrun1/generated/test_testrun1.py",
                            task_id="task1", login_role="main"):
        """Create mock run and run-with-task objects for execute-code tests."""
        mock_run = MagicMock()
        mock_run.id = run_id
        mock_run.generated_code_path = code_path

        mock_task = MagicMock()
        mock_task.id = task_id
        mock_task.login_role = login_role

        mock_run_with_task = MagicMock()
        mock_run_with_task.task = mock_task

        return mock_run, mock_run_with_task

    def test_execute_code_accepted(self, client):
        """POST /execute-code returns 202 with valid run+code+role."""
        mock_run, mock_run_with_task = self._make_run_with_task()

        repo = _make_run_repo(mock_run)
        _override_repo(repo)

        with patch("backend.api.routes.runs.RunRepository") as MockRunRepo:
            mock_instance = AsyncMock()
            mock_instance.get_with_task.return_value = mock_run_with_task
            mock_instance.update_healing_status = AsyncMock()
            MockRunRepo.return_value = mock_instance

            with patch("backend.api.routes.runs._execute_code_background"):
                response = client.post("/api/runs/testrun1/execute-code")

        assert response.status_code == 202
        data = response.json()
        assert data["run_id"] == "testrun1"
        assert data["status"] == "healing"

    def test_execute_code_no_code(self, client):
        """POST /execute-code returns 400 when no generated_code_path."""
        mock_run = MagicMock()
        mock_run.id = "testrun1"
        mock_run.generated_code_path = None

        repo = _make_run_repo(mock_run)
        _override_repo(repo)

        response = client.post("/api/runs/testrun1/execute-code")

        assert response.status_code == 400
        message = response.json().get("error", {}).get("message", response.json().get("detail", ""))
        assert "无生成代码" in message

    def test_execute_code_no_role(self, client):
        """POST /execute-code returns 400 when task has no login_role."""
        mock_run = MagicMock()
        mock_run.id = "testrun1"
        mock_run.generated_code_path = "outputs/test.py"

        mock_task = MagicMock()
        mock_task.login_role = None

        mock_run_with_task = MagicMock()
        mock_run_with_task.task = mock_task

        repo = _make_run_repo(mock_run)
        _override_repo(repo)

        with patch("backend.api.routes.runs.RunRepository") as MockRunRepo:
            mock_instance = AsyncMock()
            mock_instance.get_with_task.return_value = mock_run_with_task
            MockRunRepo.return_value = mock_instance

            response = client.post("/api/runs/testrun1/execute-code")

        assert response.status_code == 400
        message = response.json().get("error", {}).get("message", response.json().get("detail", ""))
        assert "登录角色" in message

    def test_execute_code_concurrent_409(self, client):
        """POST /execute-code returns 409 when execution already active for this run."""
        import backend.api.routes.runs as runs_module

        # Simulate active execution
        runs_module._active_code_execution["testrun1"] = "2026-01-01T00:00:00"

        try:
            mock_run, mock_run_with_task = self._make_run_with_task()

            repo = _make_run_repo(mock_run)
            _override_repo(repo)

            with patch("backend.api.routes.runs.RunRepository") as MockRunRepo:
                mock_instance = AsyncMock()
                mock_instance.get_with_task.return_value = mock_run_with_task
                MockRunRepo.return_value = mock_instance

                response = client.post("/api/runs/testrun1/execute-code")

            assert response.status_code == 409
            message = response.json().get("error", {}).get("message", response.json().get("detail", ""))
            assert "正在进行中" in message
        finally:
            runs_module._active_code_execution.pop("testrun1", None)

    def test_execute_code_run_not_found(self, client):
        """POST /execute-code returns 404 when run_id does not exist."""
        repo = _make_run_repo(run=None)
        _override_repo(repo)

        response = client.post("/api/runs/nonexistent/execute-code")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# STATUS-01: Task status update on success
# ---------------------------------------------------------------------------

class TestTaskStatusSuccess:
    """Tests for _execute_code_background Task.status auto-update."""

    @pytest.mark.asyncio
    async def test_task_status_success_on_pass(self):
        """_execute_code_background updates Task.status to 'success' when result is 'passed'."""
        from backend.api.routes.runs import _execute_code_background
        from backend.core.self_healing_runner import HealingResult

        mock_result = HealingResult(
            final_status="passed",
            attempts=1,
            error_message="",
            repaired_code_path="outputs/test/test.py",
        )

        with patch("backend.api.routes.runs.SelfHealingRunner") as MockRunner:
            mock_runner_instance = AsyncMock()
            mock_runner_instance.run.return_value = mock_result
            MockRunner.return_value = mock_runner_instance

            with patch("backend.api.routes.runs.async_session") as mock_session_ctx:
                mock_session = AsyncMock()
                mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_session)
                mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=False)

                with patch("backend.api.routes.runs.RunRepository") as MockRunRepo:
                    mock_run_repo = AsyncMock()
                    MockRunRepo.return_value = mock_run_repo

                    with patch("backend.api.routes.runs.TaskRepository") as MockTaskRepo:
                        mock_task_repo = AsyncMock()
                        MockTaskRepo.return_value = mock_task_repo

                        await _execute_code_background(
                            run_id="testrun1",
                            test_file_path="outputs/testrun1/generated/test.py",
                            login_role="main",
                            task_id="task1",
                        )

                        # Verify healing status updated
                        mock_run_repo.update_healing_status.assert_called_once()
                        call_kwargs = mock_run_repo.update_healing_status.call_args[1]
                        assert call_kwargs["status"] == "passed"

                        # Verify Task.status updated to "success" (D-09)
                        mock_task_repo.update.assert_called_once_with(
                            "task1",
                            TaskUpdate(status="success"),
                        )


# ---------------------------------------------------------------------------
# CODE-03: Healing status read-path verification
# ---------------------------------------------------------------------------

class TestHealingStatusReadPath:
    """Tests verifying _execute_code_background persists healing_status correctly."""

    @pytest.mark.asyncio
    async def test_healing_status_passed(self):
        """After _execute_code_background with passed result, healing_status reflects correctly."""
        from backend.api.routes.runs import _execute_code_background
        from backend.core.self_healing_runner import HealingResult

        mock_result = HealingResult(
            final_status="passed",
            attempts=2,
            error_message="",
            repaired_code_path="outputs/test/test.py",
        )

        with patch("backend.api.routes.runs.SelfHealingRunner") as MockRunner:
            mock_runner_instance = AsyncMock()
            mock_runner_instance.run.return_value = mock_result
            MockRunner.return_value = mock_runner_instance

            with patch("backend.api.routes.runs.async_session") as mock_session_ctx:
                mock_session = AsyncMock()
                mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_session)
                mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=False)

                with patch("backend.api.routes.runs.RunRepository") as MockRunRepo:
                    mock_run_repo = AsyncMock()
                    MockRunRepo.return_value = mock_run_repo

                    with patch("backend.api.routes.runs.TaskRepository") as MockTaskRepo:
                        MockTaskRepo.return_value = AsyncMock()

                        await _execute_code_background(
                            run_id="run-pass",
                            test_file_path="outputs/run-pass/generated/test.py",
                            login_role="main",
                            task_id="task1",
                        )

                        mock_run_repo.update_healing_status.assert_called_once()
                        call_kwargs = mock_run_repo.update_healing_status.call_args[1]
                        assert call_kwargs["run_id"] == "run-pass"
                        assert call_kwargs["status"] == "passed"
                        assert call_kwargs["attempts"] == 2
                        assert call_kwargs["error"] is None

    @pytest.mark.asyncio
    async def test_healing_status_failed(self):
        """After _execute_code_background with failed result, healing_status reflects correctly."""
        from backend.api.routes.runs import _execute_code_background
        from backend.core.self_healing_runner import HealingResult

        mock_result = HealingResult(
            final_status="failed",
            attempts=3,
            error_message="AssertionError: expected 200 got 500",
            repaired_code_path="",
        )

        with patch("backend.api.routes.runs.SelfHealingRunner") as MockRunner:
            mock_runner_instance = AsyncMock()
            mock_runner_instance.run.return_value = mock_result
            MockRunner.return_value = mock_runner_instance

            with patch("backend.api.routes.runs.async_session") as mock_session_ctx:
                mock_session = AsyncMock()
                mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_session)
                mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=False)

                with patch("backend.api.routes.runs.RunRepository") as MockRunRepo:
                    mock_run_repo = AsyncMock()
                    MockRunRepo.return_value = mock_run_repo

                    with patch("backend.api.routes.runs.TaskRepository") as MockTaskRepo:
                        MockTaskRepo.return_value = AsyncMock()

                        await _execute_code_background(
                            run_id="run-fail",
                            test_file_path="outputs/run-fail/generated/test.py",
                            login_role="main",
                            task_id="task2",
                        )

                        mock_run_repo.update_healing_status.assert_called_once()
                        call_kwargs = mock_run_repo.update_healing_status.call_args[1]
                        assert call_kwargs["run_id"] == "run-fail"
                        assert call_kwargs["status"] == "failed"
                        assert call_kwargs["attempts"] == 3
                        assert call_kwargs["error"] == "AssertionError: expected 200 got 500"
