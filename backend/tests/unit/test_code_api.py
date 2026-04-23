"""Unit tests for GET /runs/{run_id}/code endpoint (CODE-01).

Tests mock RunRepository to avoid real database dependencies.
Covers:
  1. Success: returns line-numbered code text (D-01)
  2. No code: generated_code_path is null
  3. File not found: code file missing on disk
  4. Path traversal: code path outside outputs/ directory (D-03)
  5. Run not found: run_id does not exist
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
from fastapi.testclient import TestClient

from backend.api.main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Create test client with the runs router mounted."""
    return TestClient(app)


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
    repo = MagicMock()
    repo.get = AsyncMock(return_value=run)
    return repo


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGetRunCode:
    """Tests for GET /runs/{run_id}/code endpoint."""

    def test_get_code_success(self, client, tmp_path):
        """GET /runs/{run_id}/code returns 200 with line-numbered code text."""
        # Create a real temp file simulating generated code
        code_file = tmp_path / "test_generated.py"
        code_file.write_text("def test_xxx():\n    pass", encoding="utf-8")

        run = _make_run(generated_code_path=str(code_file))
        run_repo = _make_run_repo(run)

        with patch("backend.api.routes.runs.get_run_repo", return_value=run_repo):
            response = client.get("/runs/run-001/code")

        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")
        body = response.text
        assert "1 | def test_xxx():" in body
        assert "2 |     pass" in body

    def test_get_code_no_code(self, client):
        """GET /runs/{run_id}/code returns 404 when generated_code_path is null."""
        run = _make_run(generated_code_path=None)
        run_repo = _make_run_repo(run)

        with patch("backend.api.routes.runs.get_run_repo", return_value=run_repo):
            response = client.get("/runs/run-002/code")

        assert response.status_code == 404
        detail = response.json().get("detail", "")
        assert "无生成代码" in detail

    def test_get_code_file_not_found(self, client):
        """GET /runs/{run_id}/code returns 404 when code file does not exist on disk."""
        run = _make_run(generated_code_path="/nonexistent/path/test.py")
        run_repo = _make_run_repo(run)

        with patch("backend.api.routes.runs.get_run_repo", return_value=run_repo):
            response = client.get("/runs/run-003/code")

        assert response.status_code == 404

    def test_get_code_path_traversal(self, client):
        """GET /runs/{run_id}/code returns 403 for path outside outputs/ directory."""
        run = _make_run(generated_code_path="/etc/passwd")
        run_repo = _make_run_repo(run)

        with patch("backend.api.routes.runs.get_run_repo", return_value=run_repo):
            response = client.get("/runs/run-004/code")

        assert response.status_code == 403

    def test_get_code_run_not_found(self, client):
        """GET /runs/{run_id}/code returns 404 when run_id does not exist."""
        run_repo = _make_run_repo(run=None)

        with patch("backend.api.routes.runs.get_run_repo", return_value=run_repo):
            response = client.get("/runs/nonexistent/code")

        assert response.status_code == 404
