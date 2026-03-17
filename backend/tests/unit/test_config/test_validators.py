"""Unit tests for WEBSERP_PATH validation."""
import sys
from pathlib import Path

import pytest

from backend.config.validators import validate_weberp_path


class TestValidateWeberpPath:
    """Tests for validate_weberp_path function."""

    def test_validate_valid_path(
        self, mock_valid_weberp_path: Path, capsys
    ):
        """Valid path with all files passes validation."""
        # Should not raise any exception
        validate_weberp_path(str(mock_valid_weberp_path))

        # No error output
        captured = capsys.readouterr()
        assert "[CONFIG ERROR]" not in captured.out

    def test_validate_nonexistent_directory(self, tmp_path: Path, capsys):
        """Non-existent directory causes SystemExit."""
        nonexistent = tmp_path / "nonexistent"

        with pytest.raises(SystemExit) as exc_info:
            validate_weberp_path(str(nonexistent))

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "[CONFIG ERROR]" in captured.out
        assert "directory not found" in captured.out

    def test_validate_missing_base_prerequisites(
        self, mock_weberp_missing_base_prereq: Path, capsys
    ):
        """Missing base_prerequisites.py causes SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            validate_weberp_path(str(mock_weberp_missing_base_prereq))

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "[CONFIG ERROR]" in captured.out
        assert "base_prerequisites.py not found" in captured.out

    def test_validate_missing_config_settings(
        self, mock_weberp_missing_config: Path, capsys
    ):
        """Missing config/settings.py causes SystemExit with template."""
        with pytest.raises(SystemExit) as exc_info:
            validate_weberp_path(str(mock_weberp_missing_config))

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "[CONFIG ERROR]" in captured.out
        assert "config/settings.py not found" in captured.out
        assert "DATA_PATHS" in captured.out  # Template included

    def test_validate_unimportable_module(
        self, mock_weberp_unimportable: Path, capsys
    ):
        """Unimportable base_prerequisites.py causes SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            validate_weberp_path(str(mock_weberp_unimportable))

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "[CONFIG ERROR]" in captured.out
        assert "Cannot import" in captured.out
