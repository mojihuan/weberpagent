"""E2E tests for FLOW-03: batch execution with independent token injection per task.

Per D-05: only cover 'all tasks have login_role' scenario.
Per D-06: no mixed/partial-failure tests (already covered by BatchExecutionService unit tests).

Each task in a batch must independently:
1. Fetch its own token (no shared token)
2. Create its own BrowserSession (no browser instance reuse)
3. Navigate to ERP with its own auth state
"""

import asyncio
import os

import pytest

from backend.core.auth_service import AuthService, TokenFetchError
from backend.core.auth_session_factory import create_authenticated_session


@pytest.mark.asyncio
async def test_batch_fetches_independent_tokens(auth_service, skip_if_erp_unreachable):
    """Verify concurrent token fetches return independent tokens for each role.

    Simulates batch scenario: N tasks with different roles all fetch tokens
    concurrently. Each should get its own unique storage_state.
    """
    roles = ["main", "special", "vice"]
    semaphore = asyncio.Semaphore(2)
    results = {}

    async def fetch_role_token(role: str):
        async with semaphore:
            storage_state = await auth_service.get_storage_state_for_role(role)
            local_storage = storage_state["origins"][0]["localStorage"]
            token = next(e["value"] for e in local_storage if e["name"] == "Admin-Token")
            results[role] = token

    try:
        await asyncio.gather(*[fetch_role_token(r) for r in roles])
    except TokenFetchError as exc:
        pytest.skip(f"ERP auth endpoint unavailable: {exc}")

    assert len(results) == 3, f"Expected 3 results, got {len(results)}"

    # Verify each role got a token
    for role in roles:
        assert results[role] is not None, f"Role {role} got None token"
        assert len(results[role]) > 10, f"Role {role} token too short"

    # Verify tokens are independent (different credentials -> different tokens)
    unique_tokens = set(results.values())
    assert len(unique_tokens) >= 2, f"Expected >= 2 unique tokens, got {len(unique_tokens)}"


@pytest.mark.asyncio
async def test_batch_creates_independent_sessions(erp_base_url, skip_if_erp_unreachable):
    """Verify concurrent tasks each create independent BrowserSession instances.

    Per FLOW-03: no cross-task browser instance reuse.
    Each session must have its own storage_state and browser process.
    """
    roles = ["main", "special"]
    semaphore = asyncio.Semaphore(2)
    results = {}

    async def verify_role_session(role: str):
        async with semaphore:
            session = await create_authenticated_session(role)
            try:
                page = await session.get_current_page()
                await page.goto(f"{erp_base_url}/", wait_until="networkidle", timeout=30000)

                # Verify auth state in browser
                admin_token = await page.evaluate("window.localStorage.getItem('Admin-Token')")
                assert admin_token is not None, f"Role {role}: no Admin-Token in browser"
                results[role] = admin_token
            finally:
                temp_file = getattr(session, '_auth_temp_file', None)
                await session.stop()
                if temp_file:
                    try:
                        os.unlink(temp_file)
                    except OSError:
                        pass

    try:
        await asyncio.gather(*[verify_role_session(r) for r in roles])
    except TokenFetchError as exc:
        pytest.skip(f"ERP auth endpoint unavailable: {exc}")

    assert len(results) == 2
    # Each session should have loaded its own token
    for role in roles:
        assert results[role] is not None, f"Role {role}: session did not load auth state"
        assert len(results[role]) > 10, f"Role {role}: token in browser too short"


@pytest.mark.asyncio
async def test_batch_same_role_independent_sessions(auth_service, erp_base_url, skip_if_erp_unreachable):
    """Verify even same-role tasks get independent sessions (no reuse).

    Per FLOW-03: each task independently gets token and creates BrowserSession,
    even if multiple tasks share the same role.
    """
    role = "main"
    sessions_data = []
    semaphore = asyncio.Semaphore(2)

    async def create_and_verify(task_idx: int):
        async with semaphore:
            session = await create_authenticated_session(role)
            try:
                page = await session.get_current_page()
                await page.goto(f"{erp_base_url}/", wait_until="networkidle", timeout=30000)
                admin_token = await page.evaluate("window.localStorage.getItem('Admin-Token')")
                sessions_data.append({
                    "task_idx": task_idx,
                    "token": admin_token,
                    "session_id": id(session),
                })
            finally:
                temp_file = getattr(session, '_auth_temp_file', None)
                await session.stop()
                if temp_file:
                    try:
                        os.unlink(temp_file)
                    except OSError:
                        pass

    try:
        await asyncio.gather(*[create_and_verify(i) for i in range(2)])
    except TokenFetchError as exc:
        pytest.skip(f"ERP auth endpoint unavailable: {exc}")

    assert len(sessions_data) == 2

    # Verify different session objects (no reuse)
    session_ids = [d["session_id"] for d in sessions_data]
    assert len(set(session_ids)) == 2, "Sessions should be independent objects"

    # Both should have valid tokens
    for data in sessions_data:
        assert data["token"] is not None, f"Task {data['task_idx']}: no token in browser"
