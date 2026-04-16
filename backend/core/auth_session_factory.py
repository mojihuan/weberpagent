"""Authenticated session factory — creates pre-authenticated BrowserSession instances.

Provides create_authenticated_session(role) that acquires an ERP auth token via
AuthService, constructs a Playwright storage_state dict, and creates a BrowserSession
with auth pre-loaded so the browser starts already logged in.

Raises TokenFetchError if token acquisition fails. The caller (Phase 80) handles
fallback to the existing text-based login flow.
"""

import logging

from browser_use import BrowserSession
from browser_use.browser.profile import ViewportSize

from backend.core.agent_service import SERVER_BROWSER_ARGS
from backend.core.auth_service import auth_service

logger = logging.getLogger(__name__)


async def create_authenticated_session(role: str) -> BrowserSession:
    """Create a pre-authenticated BrowserSession for the given role.

    Acquires an ERP access token via HTTP, constructs a Playwright
    storage_state dict with localStorage entries (Admin-Token, Admin-Expires-In),
    and creates a BrowserSession with auth pre-loaded.

    The browser will have ERP auth cookies pre-loaded so it starts already
    logged in, skipping the 5-step text-based login flow.

    Args:
        role: ERP role name (e.g. "main", "special", "vice").

    Returns:
        BrowserSession with ERP auth pre-loaded.

    Raises:
        TokenFetchError: If token acquisition fails (timeout, HTTP error,
            malformed response). The caller should handle fallback.
    """
    storage_state = await auth_service.get_storage_state_for_role(role)

    session = BrowserSession(
        storage_state=storage_state,
        headless=True,
        args=SERVER_BROWSER_ARGS,
        viewport=ViewportSize(width=1920, height=1080),
    )

    logger.info(f"已创建认证浏览器会话: role={role}")
    return session
