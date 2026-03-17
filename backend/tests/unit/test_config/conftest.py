"""Shared fixtures for config validation tests."""
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def mock_valid_weberp_path(tmp_path: Path) -> Path:
    """Create a mock webseleniumerp directory with all required files."""
    weberp_dir = tmp_path / "webseleniumerp"
    weberp_dir.mkdir()

    # Create base_prerequisites.py
    (weberp_dir / "base_prerequisites.py").write_text(
        "# Mock base_prerequisites.py\n"
        "class BasePrerequisites:\n"
        "    pass\n"
    )

    # Create config/settings.py
    config_dir = weberp_dir / "config"
    config_dir.mkdir()
    (config_dir / "settings.py").write_text(
        "# Mock config/settings.py\n"
        "DATA_PATHS = {}\n"
    )

    return weberp_dir


@pytest.fixture
def mock_weberp_missing_base_prereq(tmp_path: Path) -> Path:
    """Create a mock webseleniumerp directory without base_prerequisites.py."""
    weberp_dir = tmp_path / "webseleniumerp"
    weberp_dir.mkdir()

    # Create config/settings.py only
    config_dir = weberp_dir / "config"
    config_dir.mkdir()
    (config_dir / "settings.py").write_text("DATA_PATHS = {}")

    return weberp_dir


@pytest.fixture
def mock_weberp_missing_config(tmp_path: Path) -> Path:
    """Create a mock webseleniumerp directory without config/settings.py."""
    weberp_dir = tmp_path / "webseleniumerp"
    weberp_dir.mkdir()

    # Create base_prerequisites.py only
    (weberp_dir / "base_prerequisites.py").write_text(
        "class BasePrerequisites:\n    pass\n"
    )

    return weberp_dir


@pytest.fixture
def mock_weberp_unimportable(tmp_path: Path) -> Path:
    """Create a mock webseleniumerp directory with invalid base_prerequisites.py."""
    weberp_dir = tmp_path / "webseleniumerp"
    weberp_dir.mkdir()

    # Create syntactically invalid base_prerequisites.py
    (weberp_dir / "base_prerequisites.py").write_text(
        "this is not valid python syntax !!!\n"
    )

    # Create config/settings.py
    config_dir = weberp_dir / "config"
    config_dir.mkdir()
    (config_dir / "settings.py").write_text("DATA_PATHS = {}")

    return weberp_dir
