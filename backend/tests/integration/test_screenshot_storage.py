"""Integration tests for screenshot storage (DATA-04).

Verifies that screenshots are stored as files on disk, not as BLOBs in database.
"""

import os
import tempfile
from pathlib import Path

import pytest

from backend.utils.screenshot import ScreenshotManager
from backend.db.models import Step


class TestScreenshotStorage:
    """Tests for file-based screenshot storage."""

    def test_screenshot_manager_creates_directory(self):
        """ScreenshotManager creates the screenshot directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ScreenshotManager(tmpdir, "task123")
            assert manager.get_dir() == str(Path(tmpdir) / "screenshots" / "task123")
            assert Path(manager.get_dir()).exists()

    def test_screenshot_manager_generates_path(self):
        """ScreenshotManager generates correct file paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ScreenshotManager(tmpdir, "task123")
            path = manager.get_path(step=1)
            assert path.endswith("step_001.jpg")
            assert "task123" in path

    def test_screenshot_manager_custom_extension(self):
        """ScreenshotManager supports custom extensions (e.g., png)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ScreenshotManager(tmpdir, "task456")
            path = manager.get_path(step=5, ext="png")
            assert path.endswith("step_005.png")

    def test_screenshot_file_created_on_disk(self):
        """Screenshot files are actually written to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ScreenshotManager(tmpdir, "task789")
            path = manager.get_path(step=1, ext="txt")

            # Simulate writing a file (as Playwright would do with screenshots)
            with open(path, "w") as f:
                f.write("fake screenshot data")

            assert Path(path).exists()
            assert Path(path).read_text() == "fake screenshot data"

    def test_step_model_screenshot_path_is_string(self):
        """Step.screenshot_path is a String column, not BLOB."""
        from sqlalchemy import String
        from sqlalchemy.orm import class_mapper

        mapper = class_mapper(Step)
        screenshot_column = None

        for column in mapper.columns:
            if column.name == "screenshot_path":
                screenshot_column = column
                break

        assert screenshot_column is not None, "screenshot_path column not found"
        assert isinstance(screenshot_column.type, String), (
            f"screenshot_path should be String type, got {type(screenshot_column.type)}"
        )
        assert screenshot_column.type.length == 500, (
            f"screenshot_path length should be 500, got {screenshot_column.type.length}"
        )

    def test_no_blob_columns_in_models(self):
        """Verify no BLOB columns exist in any model."""
        from sqlalchemy import LargeBinary
        from sqlalchemy.orm import class_mapper
        from backend.db.models import Task, Run, Step, Assertion, AssertionResult, Report

        models = [Task, Run, Step, Assertion, AssertionResult, Report]
        blob_columns = []

        for model in models:
            mapper = class_mapper(model)
            for column in mapper.columns:
                if isinstance(column.type, LargeBinary):
                    blob_columns.append(f"{model.__name__}.{column.name}")

        assert blob_columns == [], f"Found BLOB columns (should use file storage): {blob_columns}"

    def test_screenshot_directory_structure(self):
        """Screenshots are stored under output_dir/screenshots/task_id/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ScreenshotManager(tmpdir, "mytask")
            expected_dir = Path(tmpdir) / "screenshots" / "mytask"

            assert manager.screenshot_dir == expected_dir
            assert expected_dir.exists()
