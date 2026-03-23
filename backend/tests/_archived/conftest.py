"""Disable pytest collection for archived tests.

This conftest.py file prevents pytest from collecting tests in this directory.
The tests here import deleted modules and are kept for historical reference only.
"""

import pytest

# Collect no tests from this directory
collect_ignore_glob = ["*.py"]


def pytest_collection_modifyitems(config, items):
    """Remove any items that might have been collected from this directory."""
    items[:] = [item for item in items if "_archived" not in str(item.fspath)]
