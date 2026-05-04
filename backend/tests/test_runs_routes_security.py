"""Security tests for path traversal protection in runs_routes.py.

Tests CORR-02: _validate_code_path must be called in get_run_report and
execute_run_code endpoints, not just get_run_code.
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from backend.api.routes.runs_routes import _validate_code_path


class TestValidateCodePath:
    """Unit tests for _validate_code_path function."""

    def test_rejects_traversal(self, tmp_path: Path) -> None:
        """Path traversal sequences like ../../ must be rejected with 403.

        Simulates a path that resolves outside the outputs/ root directory.
        """
        outputs_root = tmp_path / "outputs"
        outputs_root.mkdir()
        outside_path = tmp_path / "etc" / "passwd"

        with patch("backend.api.routes.runs_routes.Path") as mock_path_cls:
            def path_constructor(arg: str = ".") -> MagicMock:
                mock = MagicMock(spec=Path)
                if arg == "outputs":
                    mock.resolve.return_value = outputs_root
                else:
                    # Simulates traversal: resolves outside outputs/
                    mock.resolve.return_value = outside_path
                    mock.__str__ = lambda _: str(outside_path)
                    mock.exists.return_value = True
                return mock

            mock_path_cls.side_effect = path_constructor

            with pytest.raises(HTTPException) as exc_info:
                _validate_code_path("outputs/../../etc/passwd")
            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "非法文件路径"

    def test_rejects_absolute_path(self, tmp_path: Path) -> None:
        """Absolute paths outside outputs/ must be rejected with 403."""
        outputs_root = tmp_path / "outputs"
        outputs_root.mkdir()
        absolute_path = Path("/etc/shadow")

        with patch("backend.api.routes.runs_routes.Path") as mock_path_cls:
            def path_constructor(arg: str = ".") -> MagicMock:
                mock = MagicMock(spec=Path)
                if arg == "outputs":
                    mock.resolve.return_value = outputs_root
                else:
                    mock.resolve.return_value = absolute_path
                    mock.__str__ = lambda _: str(absolute_path)
                    mock.exists.return_value = True
                return mock

            mock_path_cls.side_effect = path_constructor

            with pytest.raises(HTTPException) as exc_info:
                _validate_code_path("/etc/shadow")
            assert exc_info.value.status_code == 403
            assert exc_info.value.detail == "非法文件路径"

    def test_rejects_nonexistent(self, tmp_path: Path) -> None:
        """Paths to nonexistent files must be rejected with 404."""
        outputs_root = tmp_path / "outputs"
        outputs_root.mkdir()
        nonexistent = outputs_root / "nonexistent.py"

        with patch("backend.api.routes.runs_routes.Path") as mock_path_cls:
            def path_constructor(arg: str = ".") -> MagicMock:
                mock = MagicMock(spec=Path)
                if arg == "outputs":
                    mock.resolve.return_value = outputs_root
                else:
                    mock.resolve.return_value = nonexistent
                    mock.__str__ = lambda _: str(nonexistent)
                    mock.exists.return_value = False
                return mock

            mock_path_cls.side_effect = path_constructor

            with pytest.raises(HTTPException) as exc_info:
                _validate_code_path(str(nonexistent))
            assert exc_info.value.status_code == 404
            assert exc_info.value.detail == "代码文件不存在"

    def test_accepts_valid_path(self, tmp_path: Path) -> None:
        """Valid paths under outputs/ that exist should return the resolved Path."""
        outputs_root = tmp_path / "outputs"
        outputs_root.mkdir()
        valid_file = outputs_root / "test_file.py"
        valid_file.write_text("# test", encoding="utf-8")

        with patch("backend.api.routes.runs_routes.Path") as mock_path_cls:
            def path_constructor(arg: str = ".") -> MagicMock:
                mock = MagicMock(spec=Path)
                if arg == "outputs":
                    mock.resolve.return_value = outputs_root
                else:
                    mock.resolve.return_value = valid_file
                    mock.__str__ = lambda _: str(valid_file)
                    mock.exists.return_value = True
                return mock

            mock_path_cls.side_effect = path_constructor

            result = _validate_code_path(str(valid_file))
            assert str(result) == str(valid_file)


class TestEndpointPathValidation:
    """Integration tests ensuring endpoints call _validate_code_path."""

    @pytest.mark.asyncio
    async def test_execute_run_code_validates_before_background(self) -> None:
        """execute_run_code must validate path BEFORE adding background task.

        If path is malicious, 403 must be returned to client immediately,
        NOT deferred to background task where it would silently fail.
        """
        mock_run = MagicMock()
        mock_run.id = "test-run-id"
        mock_run.generated_code_path = "outputs/../../etc/passwd"

        mock_run_with_task = MagicMock()
        mock_task = MagicMock()
        mock_task.id = "test-task-id"
        mock_task.login_role = "admin"
        mock_run_with_task.task = mock_task

        mock_run_repo = AsyncMock()
        mock_run_repo.get.return_value = mock_run

        from backend.api.routes.runs_routes import execute_run_code

        with patch("backend.api.routes.runs_routes._validate_code_path",
                   side_effect=HTTPException(status_code=403, detail="非法文件路径")), \
             patch("backend.api.routes.runs_routes.async_session") as mock_session:
            mock_session_cm = AsyncMock()
            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=AsyncMock())
            mock_session_instance.__aexit__ = AsyncMock(return_value=False)
            mock_session.return_value = mock_session_instance

            # Set up get_with_task to return run with task
            mock_inner_repo = AsyncMock()
            mock_inner_repo.get_with_task.return_value = mock_run_with_task
            with patch("backend.api.routes.runs_routes.RunRepository",
                       return_value=mock_inner_repo):
                with pytest.raises(HTTPException) as exc_info:
                    await execute_run_code(
                        run_id="test-run-id",
                        background_tasks=MagicMock(),
                        run_repo=mock_run_repo,
                    )
                assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_get_run_report_validates_before_serve(self) -> None:
        """get_run_report must validate path before serving the report file.

        If path is malicious, 403 must be returned, not the file content.
        """
        mock_run = MagicMock()
        mock_run.id = "test-run-id"
        mock_run.generated_code_path = "outputs/../../etc/passwd"

        mock_run_repo = AsyncMock()
        mock_run_repo.get.return_value = mock_run

        from backend.api.routes.runs_routes import get_run_report

        with patch("backend.api.routes.runs_routes._validate_code_path",
                   side_effect=HTTPException(status_code=403, detail="非法文件路径")):
            with pytest.raises(HTTPException) as exc_info:
                await get_run_report(
                    run_id="test-run-id",
                    run_repo=mock_run_repo,
                )
            assert exc_info.value.status_code == 403
