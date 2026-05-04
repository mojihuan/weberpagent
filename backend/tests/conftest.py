"""Shared pytest configuration and fixtures."""

import pytest

# Prevent pytest from collecting test files in outputs/, _backup/, node_modules/
# These directories may contain generated Playwright test files that would
# be incorrectly collected by pytest discovery.
collect_ignore_glob = ["outputs/*", "_backup/*", "node_modules/*"]
