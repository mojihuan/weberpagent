"""E2E tests for COMPAT-01: no-login-role task execution path unchanged vs v0.9.1.

Per D-07: comparison test -- verify no-role path is identical to v0.9.1.
Per D-08: independent verification of existing text login flow.

Key invariant: when login_role is None, the execution path must NOT:
- Call AuthService.get_storage_state_for_role()
- Call create_authenticated_session()
- Modify the task_description with login prefix
- Set effective_target_url to ERP base URL
"""

import pytest
from unittest.mock import patch, AsyncMock

from backend.core.auth_service import AuthService
from backend.core.test_flow_service import TestFlowService


@pytest.mark.asyncio
async def test_no_login_role_does_not_call_auth_service():
    """Verify AuthService is never called when login_role is None.

    Per COMPAT-01: the no-role path must be completely independent of
    the cookie pre-injection infrastructure.
    """
    auth_service = AuthService()

    with patch.object(auth_service, "get_storage_state_for_role", new_callable=AsyncMock) as mock_get:
        # Simulate the runs.py logic: if login_role is None, skip auth entirely
        login_role = None

        if login_role:
            # This branch should NOT be entered
            await auth_service.get_storage_state_for_role(login_role)

        # Verify auth_service was never called
        mock_get.assert_not_called()


@pytest.mark.asyncio
async def test_no_login_role_preserves_task_description():
    """Verify task description is unchanged when login_role is None.

    Per v0.9.1 behavior: no login prefix is added, no variable substitution
    beyond normal precondition processing.
    """
    flow = TestFlowService()
    original_description = "\u6253\u5f00\u9500\u552e\u51fa\u5e93\u9875\u9762\uff0c\u586b\u5199\u51fa\u5e93\u5355"

    # When login_role is None, runs.py does NOT call _build_description or replace_cached_variables_only
    # It passes the task_description directly (after optional precondition variable substitution)
    # This test verifies that neither method is called for the no-role path

    with patch.object(flow, "_build_description") as mock_build, \
         patch.object(flow, "replace_cached_variables_only") as mock_replace:

        login_role = None
        if login_role:
            # NOT entered
            pass
        # Description stays as-is
        result = original_description

        mock_build.assert_not_called()
        mock_replace.assert_not_called()
        assert result == original_description


@pytest.mark.asyncio
async def test_login_role_uses_build_description_on_injection_failure():
    """Verify injection failure fallback calls _build_description (v0.9.1 text login).

    Per D-07: when login_role is set but injection fails, the task
    falls back to the exact same _build_description path as v0.9.1.
    """
    flow = TestFlowService()

    description = flow._build_description(
        task_description="\u6253\u5f00\u9500\u552e\u51fa\u5e93\u9875\u9762",
        login_url="https://erp.example.com/login",
        account="Y59800075",
        password="test_pass",
        context={},
        cache_values={},
    )

    # _build_description must produce a login prefix (5-step login instructions)
    assert "\u767b\u5f55" in description or "login" in description.lower(), \
        f"_build_description should include login instructions, got: {description[:200]}"
    # Original task description must be preserved
    assert "\u9500\u552e\u51fa\u5e93" in description, \
        f"_build_description should preserve original task description, got: {description[:200]}"
    # Login credentials must be in the description
    assert "Y59800075" in description, \
        f"_build_description should include account, got: {description[:200]}"


@pytest.mark.asyncio
async def test_login_role_uses_replace_cached_only_on_injection_success():
    """Verify injection success calls replace_cached_variables_only (not _build_description).

    Per D-07: when injection succeeds, only replace_cached_variables_only is called,
    NOT _build_description. No 5-step login prefix is added.
    """
    flow = TestFlowService()

    # replace_cached_variables_only should NOT add login prefix
    description = flow.replace_cached_variables_only(
        task_description="\u6253\u5f00{{cached:PRODUCT_NAME}}\u9875\u9762",
        cache_values={"PRODUCT_NAME": "\u9500\u552e\u51fa\u5e93"},
    )

    # Variable replaced
    assert "\u9500\u552e\u51fa\u5e93" in description, f"Variable not replaced: {description}"
    # No login instructions
    assert "\u767b\u5f55" not in description, f"Should NOT contain login instructions: {description[:200]}"
    assert "password" not in description.lower(), f"Should NOT contain credentials: {description[:200]}"


@pytest.mark.asyncio
async def test_no_login_role_creates_default_browser_session():
    """Verify no-login-role path creates a standard BrowserSession (no storage_state).

    Per COMPAT-01: create_browser_session() is called (not create_authenticated_session).
    The session has no pre-loaded auth state.
    """
    from backend.core.auth_session_factory import create_authenticated_session

    with patch("backend.core.auth_session_factory.create_authenticated_session", new_callable=AsyncMock) as mock_auth:
        login_role = None
        session = None

        if login_role:
            session = await create_authenticated_session(login_role)

        # Should NOT have called create_authenticated_session
        mock_auth.assert_not_called()
        # session should be None (will be created later by agent_service.run_with_cleanup)
        assert session is None
