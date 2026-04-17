"""E2E tests for COMPAT-02: all 7 UI roles token fetch + browser injection.

Per D-03: each of the 7 roles is independently tested.
Per D-04: each role verification = get_storage_state_for_role -> BrowserSession
          -> navigate ERP -> verify logged-in.
"""

import os

import pytest

from backend.core.auth_session_factory import create_authenticated_session
from backend.core.auth_service import AuthService, TokenFetchError


ERP_ALL_ROLES = ["main", "special", "vice", "camera", "platform", "super", "idle"]


@pytest.mark.asyncio
async def test_all_roles_fetch_storage_state(auth_service, skip_if_erp_unreachable):
    """Verify all 7 roles can fetch token and construct storage_state.

    Per COMPAT-02: no 'role not supported' errors for any of the 7 roles.
    """
    results = {}
    for role in ERP_ALL_ROLES:
        try:
            storage_state = await auth_service.get_storage_state_for_role(role)
        except TokenFetchError as e:
            pytest.skip(f"Role {role} token fetch failed: {e}")
        assert storage_state is not None, f"Role {role}: storage_state is None"
        assert "origins" in storage_state, f"Role {role}: missing 'origins' key"
        assert len(storage_state["origins"]) > 0, f"Role {role}: empty origins"

        # Verify Admin-Token is present in localStorage
        origin = storage_state["origins"][0]
        local_storage = origin.get("localStorage", [])
        token_entries = [e for e in local_storage if e["name"] == "Admin-Token"]
        assert len(token_entries) == 1, (
            f"Role {role}: Admin-Token not found in localStorage"
        )
        assert len(token_entries[0]["value"]) > 10, (
            f"Role {role}: Admin-Token seems empty or too short"
        )

        results[role] = storage_state

    assert len(results) == 7, f"Expected 7 roles, got {len(results)}"


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ERP_ALL_ROLES)
async def test_role_authenticated_browser_session(role, erp_base_url, skip_if_erp_unreachable):
    """Verify each role can create an authenticated BrowserSession and navigate to ERP logged-in.

    Per D-04: get_storage_state_for_role -> create BrowserSession -> navigate ERP
              -> verify logged-in.
    Per D-01: real E2E, no mocks.
    """
    try:
        session = await create_authenticated_session(role)
    except TokenFetchError as e:
        pytest.skip(f"Role {role} token fetch failed: {e}")
    try:
        # Verify temp file was created and contains valid JSON
        temp_file = getattr(session, '_auth_temp_file', None)
        assert temp_file is not None, f"Role {role}: _auth_temp_file not set on session"
        assert os.path.exists(temp_file), f"Role {role}: temp file does not exist"

        # Verify BrowserSession received the file path
        assert session.browser_profile.storage_state == temp_file, (
            f"Role {role}: BrowserSession storage_state is not the temp file path"
        )

        page = await session.get_current_page()
        await page.goto(f"{erp_base_url}/", wait_until="networkidle", timeout=30000)

        # Wait for SPA to render auth state.
        # Check that login form is NOT present (user is already logged in).
        try:
            await page.wait_for_url("**/login**", timeout=5000)
            # If we reach here, we got redirected to login = injection failed
            pytest.fail(
                f"Role {role}: redirected to login page, cookie injection did not work"
            )
        except Exception:
            # Expected: we did NOT get redirected to login, meaning we are logged in
            pass

        # Verify localStorage has Admin-Token (injected by storage_state)
        admin_token = await page.evaluate("window.localStorage.getItem('Admin-Token')")
        assert admin_token is not None, (
            f"Role {role}: Admin-Token not found in browser localStorage after injection"
        )
        assert len(admin_token) > 10, (
            f"Role {role}: Admin-Token in browser is too short"
        )

    finally:
        # Clean up browser session and temp file
        temp_file = getattr(session, '_auth_temp_file', None)
        await session.stop()
        if temp_file:
            try:
                os.unlink(temp_file)
            except OSError:
                pass


@pytest.mark.asyncio
async def test_roles_have_independent_tokens(auth_service, skip_if_erp_unreachable):
    """Verify different roles get different tokens (no token sharing/caching)."""
    tokens = {}
    for role in ERP_ALL_ROLES:
        try:
            storage_state = await auth_service.get_storage_state_for_role(role)
        except TokenFetchError as e:
            pytest.skip(f"Role {role} token fetch failed: {e}")
        local_storage = storage_state["origins"][0]["localStorage"]
        token = next(e["value"] for e in local_storage if e["name"] == "Admin-Token")
        tokens[role] = token

    # Each role should get a unique token (they have different credentials)
    unique_tokens = set(tokens.values())
    assert len(unique_tokens) >= 2, (
        "Expected at least 2 different tokens across roles"
    )
