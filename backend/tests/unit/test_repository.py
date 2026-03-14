"""Test stubs for repository methods.

These tests are skipped until the repository methods are implemented in plan 02-02.
"""

import pytest


@pytest.mark.skip(reason="RunRepository.get_steps will be implemented in plan 02-02")
def test_run_repository_get_steps():
    """RunRepository.get_steps() returns list of Step ordered by step_index.

    This test verifies:
    - RunRepository has get_steps method
    - Method accepts run_id parameter
    - Returns list of Step objects
    - Steps are ordered by step_index ascending
    - Returns empty list if run has no steps
    """
    pass
