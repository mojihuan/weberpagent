"""Authenticated session factory — creates pre-authenticated BrowserSession instances.

Provides create_authenticated_session(role) that acquires an ERP auth token via
AuthService, constructs a Playwright storage_state dict, and creates a BrowserSession
with auth pre-loaded so the browser starts already logged in.

Uses a temp JSON file workaround because browser-use 0.12.2's
StorageStateWatchdog._load_storage_state() calls os.path.exists(str(load_path))
which silently fails when storage_state is a dict (returns False, skips loading).

Raises TokenFetchError if token acquisition fails. The caller (Phase 80) handles
fallback to the existing text-based login flow.
"""

import json
import logging
import os
import tempfile

from browser_use import BrowserSession
from browser_use.browser.profile import ViewportSize

from backend.core.agent_service import SERVER_BROWSER_ARGS
from backend.core.auth_service import auth_service

logger = logging.getLogger(__name__)


async def create_authenticated_session(role: str) -> BrowserSession:
    """Create a pre-authenticated BrowserSession for the given role.

    Acquires an ERP access token via HTTP, constructs a Playwright
    storage_state dict with localStorage entries (Admin-Token, Admin-Expires-In),
    writes it to a temp JSON file, and creates a BrowserSession with the file
    path so browser-use can properly load it.

    The browser will have ERP auth cookies pre-loaded so it starts already
    logged in, skipping the 5-step text-based login flow.

    The temp file path is stored as session._auth_temp_file for caller cleanup.

    Args:
        role: ERP role name (e.g. "main", "special", "vice").

    Returns:
        BrowserSession with ERP auth pre-loaded. Caller should clean up
        the temp file via session._auth_temp_file after stopping the session.

    Raises:
        TokenFetchError: If token acquisition fails (timeout, HTTP error,
            malformed response). The caller should handle fallback.
    """
    storage_state = await auth_service.get_storage_state_for_role(role)

    # Write storage_state dict to temp JSON file (browser-use _load_storage_state
    # only works with file paths, not dicts -- see StorageStateWatchdog._load_storage_state)
    tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False, prefix=f'auth_state_{role}_'
    )
    try:
        json.dump(storage_state, tmp)
        tmp.close()
    except Exception:
        tmp.close()
        os.unlink(tmp.name)
        raise

    session = BrowserSession(
        storage_state=tmp.name,
        user_data_dir=None,
        headless=True,
        args=SERVER_BROWSER_ARGS,
        viewport=ViewportSize(width=1920, height=1080),
    )
    session._auth_temp_file = tmp.name  # track for cleanup
    logger.info(f"已创建认证浏览器会话: role={role}, temp_state={tmp.name}")
    return session
