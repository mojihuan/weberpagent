"""Unit tests for GET /runs/{run_id}/code endpoint (CODE-01).

Tests mock RunRepository via FastAPI dependency overrides to avoid real
database dependencies.

Covers:
  1. Success: returns line-numbered code text (D-01)
  2. No code: generated_code_path is null
  3. File not found: code file missing on disk
  4. Path traversal: code path outside outputs/ directory (D-03)
  5. Run not found: run_id does not exist
"""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.api.routes.runs import get_run_repo
from backend.db.repository import RunRepository


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
