"""Tests for async migration of blocking I/O operations.

Tests ASYNC-01 (save_screenshot uses asyncio.to_thread) and
ASYNC-02 (_execute_code_background uses asyncio.create_subprocess_exec).
"""

import asyncio
import base64
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.agent_service import AgentService
from backend.api.routes.runs_routes import _execute_code_background


class TestSaveScreenshotAsync:
    """Unit tests for save_screenshot async migration (ASYNC-01).

    Verifies that filepath.write_bytes is called via asyncio.to_thread
    instead of being called directly on the event loop.
    """

    @pytest.mark.asyncio
    async def test_calls_to_thread_with_write_bytes(self, tmp_path: Path) -> None:
        """save_screenshot must call asyncio.to_thread(filepath.write_bytes, screenshot_bytes).

        ASYNC-01: The blocking I/O write must be offloaded to a thread pool
        so the event loop is not blocked during screenshot saving.
        """
        service = AgentService(output_dir=str(tmp_path))
        screenshot_bytes = b"\x89PNG\r\n\x1a\n"  # minimal PNG header

        with patch("backend.core.agent_service.asyncio.to_thread", new=AsyncMock(return_value=None)) as mock_to_thread:
            result = await service.save_screenshot(screenshot_bytes, "run-1", 0)

            # Verify asyncio.to_thread was called with write_bytes and the bytes
            mock_to_thread.assert_called_once()
            call_args = mock_to_thread.call_args
            assert call_args[0][0].__name__ == "write_bytes", (
                "First arg to asyncio.to_thread should be filepath.write_bytes"
            )
            assert call_args[0][1] == screenshot_bytes, (
                "Second arg to asyncio.to_thread should be the screenshot bytes"
            )

    @pytest.mark.asyncio
    async def test_handles_base64_string_input(self, tmp_path: Path) -> None:
        """save_screenshot must decode base64 strings before passing to asyncio.to_thread.

        ASYNC-01: Base64 string input should be decoded to bytes first, then
        the decoded bytes should be passed to asyncio.to_thread.
        """
        service = AgentService(output_dir=str(tmp_path))
        raw_bytes = b"\x89PNG\r\n\x1a\nfake_image_data"
        b64_string = base64.b64encode(raw_bytes).decode("ascii")

        with patch("backend.core.agent_service.asyncio.to_thread", new=AsyncMock(return_value=None)) as mock_to_thread:
            result = await service.save_screenshot(b64_string, "run-2", 1)

            # Verify decoded bytes were passed to to_thread
            call_args = mock_to_thread.call_args
            assert call_args[0][1] == raw_bytes, (
                "Base64 string must be decoded before passing to asyncio.to_thread"
            )

    @pytest.mark.asyncio
    async def test_creates_directory_and_returns_path(self, tmp_path: Path) -> None:
        """save_screenshot must create the run screenshots directory and return the path string.

        ASYNC-01: Directory creation and path return must continue working after
        the async migration. The function should create the directory structure
        and return the string path to the saved file.
        """
        service = AgentService(output_dir=str(tmp_path))
        screenshot_bytes = b"\x89PNG\r\n\x1a\n"

        with patch("backend.core.agent_service.asyncio.to_thread", new=AsyncMock(return_value=None)):
            result = await service.save_screenshot(screenshot_bytes, "run-3", 2)

            # Verify directory was created
            expected_dir = tmp_path / "run-3" / "screenshots"
            assert expected_dir.exists(), "Screenshots directory must be created"

            # Verify return value is the correct path string
            expected_path = str(expected_dir / "step_2.png")
            assert result == expected_path, f"Expected {expected_path}, got {result}"


class TestExecuteCodeAsyncSubprocess:
    """Unit tests for _execute_code_background async subprocess migration (ASYNC-02).

    Verifies that subprocess.run is replaced with asyncio.create_subprocess_exec,
    stdout/stderr are decoded from bytes, timeout kills the process, and cleanup
    still happens in the finally block.
    """

    @pytest.mark.asyncio
    async def test_calls_create_subprocess_exec(self) -> None:
        """_execute_code_background must use asyncio.create_subprocess_exec instead of subprocess.run.

        ASYNC-02: The blocking subprocess.run must be replaced with
        asyncio.create_subprocess_exec for non-blocking subprocess execution.
        """
        run_id = "test-run-sub-1"
        test_file_path = "/tmp/test_file.py"
        test_file_dir = "/tmp"

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"stdout output", b""))

        with patch("backend.api.routes.runs_routes._code_execution_semaphore") as mock_sem, \
             patch("backend.api.routes.runs_routes._build_login_credentials", new=AsyncMock(return_value={})), \
             patch("backend.api.routes.runs_routes._write_test_support_files", return_value=(Path("/tmp/conftest.py"), None)), \
             patch("backend.api.routes.runs_routes.asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_proc)) as mock_create, \
             patch("backend.api.routes.runs_routes.asyncio.wait_for", new=AsyncMock(return_value=(b"stdout output", b""))) as mock_wait, \
             patch("backend.api.routes.runs_routes.async_session") as mock_session, \
             patch("backend.api.routes.runs_routes.silent_execute"):

            mock_sem.__aenter__ = AsyncMock(return_value=None)
            mock_sem.__aexit__ = AsyncMock(return_value=None)

            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            mock_run_repo = AsyncMock()
            mock_task_repo = AsyncMock()
            with patch("backend.api.routes.runs_routes.RunRepository", return_value=mock_run_repo), \
                 patch("backend.api.routes.runs_routes.TaskRepository", return_value=mock_task_repo):
                await _execute_code_background(
                    run_id=run_id,
                    test_file_path=test_file_path,
                    login_role="admin",
                    task_id="task-1",
                )

            # Verify create_subprocess_exec was called with correct args
            mock_create.assert_called_once()
            call_args = mock_create.call_args
            assert call_args[0][0] == "uv", "Command must be 'uv'"
            assert call_args[0][1] == "run", "Second arg must be 'run'"
            assert call_args[0][2] == "pytest", "Third arg must be 'pytest'"
            assert call_args[0][3] == test_file_path, "Fourth arg must be the test file path"

    @pytest.mark.asyncio
    async def test_success_updates_run_status(self) -> None:
        """On successful subprocess (returncode=0), run status must be updated to 'success'.

        ASYNC-02: When pytest completes with returncode 0, the run status
        must be set to 'success' via RunRepository.
        """
        run_id = "test-run-success"
        test_file_path = "/tmp/test_success.py"

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"1 passed", b""))

        with patch("backend.api.routes.runs_routes._code_execution_semaphore") as mock_sem, \
             patch("backend.api.routes.runs_routes._build_login_credentials", new=AsyncMock(return_value={})), \
             patch("backend.api.routes.runs_routes._write_test_support_files", return_value=(Path("/tmp/conftest.py"), None)), \
             patch("backend.api.routes.runs_routes.asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_proc)), \
             patch("backend.api.routes.runs_routes.asyncio.wait_for", new=AsyncMock(return_value=(b"1 passed", b""))), \
             patch("backend.api.routes.runs_routes.async_session") as mock_session, \
             patch("backend.api.routes.runs_routes.silent_execute"):

            mock_sem.__aenter__ = AsyncMock(return_value=None)
            mock_sem.__aexit__ = AsyncMock(return_value=None)

            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            mock_run_repo = AsyncMock()
            mock_task_repo = AsyncMock()
            with patch("backend.api.routes.runs_routes.RunRepository", return_value=mock_run_repo), \
                 patch("backend.api.routes.runs_routes.TaskRepository", return_value=mock_task_repo):
                await _execute_code_background(
                    run_id=run_id,
                    test_file_path=test_file_path,
                    login_role="admin",
                    task_id="task-1",
                )

            mock_run_repo.update_status.assert_called_once_with(run_id, "success")

    @pytest.mark.asyncio
    async def test_failure_updates_run_status(self) -> None:
        """On failed subprocess (returncode!=0), run status must be updated to 'failed'.

        ASYNC-02: When pytest completes with non-zero returncode, the run status
        must be set to 'failed' via RunRepository.
        """
        run_id = "test-run-fail"
        test_file_path = "/tmp/test_fail.py"

        mock_proc = AsyncMock()
        mock_proc.returncode = 1
        mock_proc.communicate = AsyncMock(return_value=(b"", b"1 failed"))

        with patch("backend.api.routes.runs_routes._code_execution_semaphore") as mock_sem, \
             patch("backend.api.routes.runs_routes._build_login_credentials", new=AsyncMock(return_value={})), \
             patch("backend.api.routes.runs_routes._write_test_support_files", return_value=(Path("/tmp/conftest.py"), None)), \
             patch("backend.api.routes.runs_routes.asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_proc)), \
             patch("backend.api.routes.runs_routes.asyncio.wait_for", new=AsyncMock(return_value=(b"", b"1 failed"))), \
             patch("backend.api.routes.runs_routes.async_session") as mock_session, \
             patch("backend.api.routes.runs_routes.silent_execute"):

            mock_sem.__aenter__ = AsyncMock(return_value=None)
            mock_sem.__aexit__ = AsyncMock(return_value=None)

            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            mock_run_repo = AsyncMock()
            with patch("backend.api.routes.runs_routes.RunRepository", return_value=mock_run_repo):
                await _execute_code_background(
                    run_id=run_id,
                    test_file_path=test_file_path,
                    login_role="admin",
                    task_id="task-1",
                )

            mock_run_repo.update_status.assert_called_once_with(run_id, "failed")

    @pytest.mark.asyncio
    async def test_timeout_kills_process_and_waits(self) -> None:
        """On asyncio.TimeoutError, proc.kill() then proc.wait() must be called.

        ASYNC-02: When the subprocess exceeds the timeout, the process must be
        killed and waited for before handling the error gracefully.
        """
        run_id = "test-run-timeout"
        test_file_path = "/tmp/test_timeout.py"

        mock_proc = AsyncMock()
        mock_proc.kill = MagicMock()
        mock_proc.wait = AsyncMock()

        async def raise_timeout(*args, **kwargs):
            raise asyncio.TimeoutError()

        with patch("backend.api.routes.runs_routes._code_execution_semaphore") as mock_sem, \
             patch("backend.api.routes.runs_routes._build_login_credentials", new=AsyncMock(return_value={})), \
             patch("backend.api.routes.runs_routes._write_test_support_files", return_value=(Path("/tmp/conftest.py"), None)), \
             patch("backend.api.routes.runs_routes.asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_proc)), \
             patch("backend.api.routes.runs_routes.asyncio.wait_for", side_effect=raise_timeout), \
             patch("backend.api.routes.runs_routes.async_session") as mock_session, \
             patch("backend.api.routes.runs_routes.non_blocking_execute", new=AsyncMock()) as mock_non_block, \
             patch("backend.api.routes.runs_routes.silent_execute"):

            mock_sem.__aenter__ = AsyncMock(return_value=None)
            mock_sem.__aexit__ = AsyncMock(return_value=None)

            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            await _execute_code_background(
                run_id=run_id,
                test_file_path=test_file_path,
                login_role="admin",
                task_id="task-1",
            )

            # Verify kill was called on the process
            mock_proc.kill.assert_called_once()
            # Verify wait was called after kill
            mock_proc.wait.assert_called_once()

    @pytest.mark.asyncio
    async def test_stdout_stderr_decoded_from_bytes(self) -> None:
        """stdout and stderr must be decoded from bytes before logging.

        ASYNC-02: asyncio.create_subprocess_exec returns bytes for stdout/stderr,
        unlike subprocess.run with text=True. The code must decode them.
        """
        run_id = "test-run-decode"
        test_file_path = "/tmp/test_decode.py"

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        # Return bytes, not strings
        stdout_bytes = "1 passed in 0.5s".encode("utf-8")
        stderr_bytes = "warning message".encode("utf-8")
        mock_proc.communicate = AsyncMock(return_value=(stdout_bytes, stderr_bytes))

        with patch("backend.api.routes.runs_routes._code_execution_semaphore") as mock_sem, \
             patch("backend.api.routes.runs_routes._build_login_credentials", new=AsyncMock(return_value={})), \
             patch("backend.api.routes.runs_routes._write_test_support_files", return_value=(Path("/tmp/conftest.py"), None)), \
             patch("backend.api.routes.runs_routes.asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_proc)), \
             patch("backend.api.routes.runs_routes.asyncio.wait_for", new=AsyncMock(return_value=(stdout_bytes, stderr_bytes))), \
             patch("backend.api.routes.runs_routes.async_session") as mock_session, \
             patch("backend.api.routes.runs_routes.silent_execute"), \
             patch("backend.api.routes.runs_routes.logger") as mock_logger:

            mock_sem.__aenter__ = AsyncMock(return_value=None)
            mock_sem.__aexit__ = AsyncMock(return_value=None)

            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            mock_run_repo = AsyncMock()
            mock_task_repo = AsyncMock()
            with patch("backend.api.routes.runs_routes.RunRepository", return_value=mock_run_repo), \
                 patch("backend.api.routes.runs_routes.TaskRepository", return_value=mock_task_repo):
                await _execute_code_background(
                    run_id=run_id,
                    test_file_path=test_file_path,
                    login_role="admin",
                    task_id="task-1",
                )

            # Verify that logger.info was called with decoded stdout string (not bytes)
            info_calls = [str(call) for call in mock_logger.info.call_args_list]
            stdout_logged = any("1 passed in 0.5s" in call for call in info_calls)
            assert stdout_logged, "stdout must be decoded from bytes to string before logging"

            # Verify that logger.warning was called with decoded stderr string
            warning_calls = [str(call) for call in mock_logger.warning.call_args_list]
            stderr_logged = any("warning message" in call for call in warning_calls)
            assert stderr_logged, "stderr must be decoded from bytes to string before logging"

    @pytest.mark.asyncio
    async def test_finally_cleans_up_active_dict_and_support_files(self) -> None:
        """finally block must clean up _active_code_execution dict and support files.

        ASYNC-02: Regardless of success or failure, the _active_code_execution
        dict entry must be removed and support files (conftest.py) must be deleted.
        """
        run_id = "test-run-cleanup"
        test_file_path = "/tmp/test_cleanup.py"
        test_file_dir = "/tmp"

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"passed", b""))

        with patch("backend.api.routes.runs_routes._code_execution_semaphore") as mock_sem, \
             patch("backend.api.routes.runs_routes._build_login_credentials", new=AsyncMock(return_value={})), \
             patch("backend.api.routes.runs_routes._write_test_support_files", return_value=(Path("/tmp/conftest.py"), None)), \
             patch("backend.api.routes.runs_routes.asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_proc)), \
             patch("backend.api.routes.runs_routes.asyncio.wait_for", new=AsyncMock(return_value=(b"passed", b""))), \
             patch("backend.api.routes.runs_routes.async_session") as mock_session, \
             patch("backend.api.routes.runs_routes._active_code_execution", {}) as active_dict, \
             patch("backend.api.routes.runs_routes.silent_execute") as mock_silent:

            mock_sem.__aenter__ = AsyncMock(return_value=None)
            mock_sem.__aexit__ = AsyncMock(return_value=None)

            mock_session_instance = AsyncMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)
            mock_session.return_value = mock_session_instance

            mock_run_repo = AsyncMock()
            mock_task_repo = AsyncMock()
            with patch("backend.api.routes.runs_routes.RunRepository", return_value=mock_run_repo), \
                 patch("backend.api.routes.runs_routes.TaskRepository", return_value=mock_task_repo):
                await _execute_code_background(
                    run_id=run_id,
                    test_file_path=test_file_path,
                    login_role="admin",
                    task_id="task-1",
                )

            # Verify _active_code_execution was cleaned up
            assert run_id not in active_dict, (
                "run_id must be removed from _active_code_execution in finally block"
            )

            # Verify silent_execute was called for file cleanup
            assert mock_silent.call_count >= 1, (
                "silent_execute must be called to clean up support files"
            )
