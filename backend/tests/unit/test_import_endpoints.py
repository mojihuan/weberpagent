"""Unit tests for import preview and confirm endpoints.

Tests POST /tasks/import/preview and POST /tasks/import/confirm
for file validation, preview with errors, and atomic batch creation.
"""

import io

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook

from backend.api.main import app
from backend.utils.excel_template import TEMPLATE_COLUMNS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_workbook(
    headers: list[str] | None = None,
    rows: list[list] | None = None,
) -> io.BytesIO:
    """Build a minimal .xlsx workbook for testing."""
    wb = Workbook()
    ws = wb.active
    ws.title = "测试用例"
    if headers is None:
        headers = [col["header"] for col in TEMPLATE_COLUMNS]
    ws.append(headers)
    if rows:
        for row in rows:
            ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _valid_xlsx_bytes() -> io.BytesIO:
    """Create a valid .xlsx with 2 valid data rows."""
    return _make_workbook(rows=[
        ["Task A", "Description A", "https://a.com", 10, None, None],
        ["Task B", "Description B", "https://b.com", 20, None, None],
    ])


def _invalid_rows_xlsx_bytes() -> io.BytesIO:
    """Create a .xlsx with some rows missing required fields."""
    return _make_workbook(rows=[
        ["Valid Task", "Valid desc", "", 10, None, None],
        [None, None, "https://a.com", 10, None, None],  # missing name + description
    ])


# ---------------------------------------------------------------------------
# Tests: Preview endpoint
# ---------------------------------------------------------------------------


class TestImportPreview:
    """Tests for POST /tasks/import/preview."""

    def test_preview_valid_file(self):
        """Upload valid .xlsx -> 200 with rows containing row_number, data, valid=true."""
        buf = _valid_xlsx_bytes()
        client = TestClient(app)
        response = client.post(
            "/api/tasks/import/preview",
            files={"file": ("test.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "rows" in data
        assert len(data["rows"]) == 2
        assert data["total_rows"] == 2
        assert data["valid_count"] == 2
        assert data["error_count"] == 0
        assert data["has_errors"] is False
        for row in data["rows"]:
            assert "row_number" in row
            assert "data" in row
            assert "errors" in row
            assert row["valid"] is True

    def test_preview_shows_errors(self):
        """Upload .xlsx with invalid rows -> 200 with has_errors=true, error rows have non-empty errors list."""
        buf = _invalid_rows_xlsx_bytes()
        client = TestClient(app)
        response = client.post(
            "/api/tasks/import/preview",
            files={"file": ("test.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_errors"] is True
        assert data["error_count"] >= 1
        error_rows = [r for r in data["rows"] if r["errors"]]
        assert len(error_rows) >= 1

    def test_preview_rejects_non_xlsx(self):
        """Upload .txt file -> 400 with detail containing 'xlsx'."""
        client = TestClient(app)
        response = client.post(
            "/api/tasks/import/preview",
            files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
        )
        assert response.status_code == 400
        body = response.json()
        detail = body.get("error", {}).get("message", "") or body.get("detail", "")
        assert "xlsx" in detail.lower() or "xlsx" in str(body).lower()

    def test_preview_rejects_oversized(self):
        """Upload >5MB file -> 400 with detail containing '5MB'."""
        client = TestClient(app)
        big_content = b"x" * (5 * 1024 * 1024 + 1)
        response = client.post(
            "/api/tasks/import/preview",
            files={"file": ("big.xlsx", io.BytesIO(big_content), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == 400
        body = response.json()
        detail = body.get("error", {}).get("message", "") or body.get("detail", "")
        assert "5MB" in detail or "5MB" in str(body)

    def test_preview_rejects_empty(self):
        """Upload 0-byte file -> 400 with detail containing '空'."""
        client = TestClient(app)
        response = client.post(
            "/api/tasks/import/preview",
            files={"file": ("empty.xlsx", io.BytesIO(b""), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == 400
        body = response.json()
        detail = body.get("error", {}).get("message", "") or body.get("detail", "")
        assert "空" in detail or "空" in str(body)


# ---------------------------------------------------------------------------
# Tests: Confirm endpoint
# ---------------------------------------------------------------------------


class TestImportConfirm:
    """Tests for POST /tasks/import/confirm."""

    def test_confirm_creates_tasks(self):
        """Upload valid .xlsx -> 200 with status=success, created_count=N, verify N Tasks exist in DB."""
        buf = _valid_xlsx_bytes()
        client = TestClient(app)
        response = client.post(
            "/api/tasks/import/confirm",
            files={"file": ("test.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["created_count"] == 2

        # Verify tasks exist in DB by listing them
        list_response = client.get("/api/tasks")
        assert list_response.status_code == 200
        tasks = list_response.json()
        task_names = {t["name"] for t in tasks}
        assert "Task A" in task_names
        assert "Task B" in task_names

    def test_confirm_rejects_invalid(self):
        """Upload .xlsx with errors -> 400, no Tasks created."""
        buf = _invalid_rows_xlsx_bytes()
        client = TestClient(app)
        # Get initial task count
        initial = client.get("/api/tasks").json()

        response = client.post(
            "/api/tasks/import/confirm",
            files={"file": ("test.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        assert response.status_code == 400
        body = response.json()
        detail = body.get("error", {}).get("message", "") or body.get("detail", "")
        assert "无效行" in detail or "无效行" in str(body)

        # Verify no new tasks created
        after = client.get("/api/tasks").json()
        assert len(after) == len(initial)

    def test_confirm_rollback_on_error(self):
        """Verify atomicity (all-or-nothing) when any row fails at DB level.

        Creates a file with a row that has name > 200 chars, which should
        cause a DB error (String(200) column). Verify 0 tasks exist after.
        """
        long_name = "A" * 201  # exceeds String(200)
        buf = _make_workbook(rows=[
            ["Valid Task", "Valid desc", "", 10, None, None],
            [long_name, "Description", "", 10, None, None],
        ])
        client = TestClient(app)
        initial = client.get("/api/tasks").json()

        response = client.post(
            "/api/tasks/import/confirm",
            files={"file": ("test.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        )
        # Should fail with 500 or 400 due to DB constraint
        assert response.status_code in (400, 500)

        # Verify no new tasks created (all rolled back)
        after = client.get("/api/tasks").json()
        assert len(after) == len(initial)

    def test_confirm_rejects_non_xlsx(self):
        """Upload .txt file -> 400."""
        client = TestClient(app)
        response = client.post(
            "/api/tasks/import/confirm",
            files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
        )
        assert response.status_code == 400
