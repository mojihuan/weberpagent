"""Unit tests for AuthService — HTTP token fetch + storage_state construction."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from backend.core.auth_service import AuthService, TokenFetchError, auth_service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_response(
    status_code: int = 200,
    json_data: dict | None = None,
    text: str = "",
) -> MagicMock:
    """Create a mock httpx.Response."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.text = text or json.dumps(json_data or {})
    resp.json.return_value = json_data or {}
    resp.raise_for_status.side_effect = (
        None
        if status_code < 400
        else httpx.HTTPStatusError(
            message=f"HTTP {status_code}",
            request=MagicMock(),
            response=resp,
        )
    )
    return resp


# ---------------------------------------------------------------------------
# fetch_token tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_token_success():
    """fetch_token returns access_token on successful ERP login."""
    service = AuthService()
    mock_resp = _make_response(
        json_data={"data": {"access_token": "test-jwt-token", "expires_in": 720}},
    )

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_resp)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        token = await service.fetch_token("Y59800075", "secret", role="main")

    assert token == "test-jwt-token"
    mock_client.post.assert_awaited_once()
    call_args = mock_client.post.call_args
    assert "/auth/login" in call_args.args[0] or "/auth/login" in call_args.kwargs.get("url", call_args.args[0])


@pytest.mark.asyncio
async def test_fetch_token_timeout():
    """fetch_token raises TokenFetchError on timeout (>10s)."""
    service = AuthService()

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(TokenFetchError) as exc_info:
            await service.fetch_token("Y59800075", "secret", role="main")

    error_msg = str(exc_info.value)
    assert "main" in error_msg
    assert "超时" in error_msg


@pytest.mark.asyncio
async def test_fetch_token_non_200():
    """fetch_token raises TokenFetchError on non-200 HTTP status."""
    service = AuthService()
    mock_resp = _make_response(status_code=401, text="Unauthorized")

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_resp)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(TokenFetchError) as exc_info:
            await service.fetch_token("Y59800075", "secret", role="main")

    error_msg = str(exc_info.value)
    assert "401" in error_msg


@pytest.mark.asyncio
async def test_fetch_token_missing_data():
    """fetch_token raises TokenFetchError when response lacks data/access_token."""
    service = AuthService()
    mock_resp = _make_response(json_data={"code": 500})

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_resp)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(TokenFetchError) as exc_info:
            await service.fetch_token("Y59800075", "secret", role="main")

    error_msg = str(exc_info.value)
    assert "响应格式异常" in error_msg


# ---------------------------------------------------------------------------
# build_storage_state tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_build_storage_state():
    """build_storage_state returns Playwright storage_state dict with Admin-Token."""
    service = AuthService()

    mock_settings = MagicMock()
    mock_settings.erp_base_url = "https://erptest.epbox.cn/epbox_erp"

    with patch("backend.core.auth_service.get_settings", return_value=mock_settings):
        result = service.build_storage_state("my-jwt")

    assert result["cookies"] == []
    assert len(result["origins"]) == 1
    origin = result["origins"][0]
    assert origin["origin"] == "https://erptest.epbox.cn"
    local_storage = origin["localStorage"]
    assert {"name": "Admin-Token", "value": "my-jwt"} in local_storage
    assert {"name": "Admin-Expires-In", "value": "720"} in local_storage


# ---------------------------------------------------------------------------
# get_storage_state_for_role tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_storage_state_for_role():
    """get_storage_state_for_role combines AccountService + fetch_token + build_storage_state."""
    service = AuthService()

    mock_account_info = MagicMock()
    mock_account_info.account = "Y59800075"
    mock_account_info.password = "secret"
    mock_account_info.role = "main"

    mock_settings = MagicMock()
    mock_settings.erp_base_url = "https://erptest.epbox.cn/epbox_erp"

    with (
        patch.object(service, "fetch_token", new_callable=AsyncMock, return_value="role-jwt") as mock_fetch,
        patch("backend.core.auth_service.account_service") as mock_acct,
        patch("backend.core.auth_service.get_settings", return_value=mock_settings),
    ):
        mock_acct.resolve.return_value = mock_account_info
        result = await service.get_storage_state_for_role("main")

    mock_acct.resolve.assert_called_once_with("main")
    mock_fetch.assert_awaited_once_with("Y59800075", "secret", role="main")
    assert result["origins"][0]["localStorage"][0]["name"] == "Admin-Token"
    assert result["origins"][0]["localStorage"][0]["value"] == "role-jwt"


# ---------------------------------------------------------------------------
# _extract_origin tests
# ---------------------------------------------------------------------------


def test_extract_origin_strips_path():
    """_extract_origin removes path from URL."""
    result = AuthService._extract_origin("https://erptest.epbox.cn/epbox_erp")
    assert result == "https://erptest.epbox.cn"


def test_extract_origin_no_path():
    """_extract_origin returns URL unchanged when no path."""
    result = AuthService._extract_origin("https://erp.example.com")
    assert result == "https://erp.example.com"


# ---------------------------------------------------------------------------
# create_authenticated_session tests (auth_session_factory)
# ---------------------------------------------------------------------------


SAMPLE_STORAGE_STATE = {
    "cookies": [],
    "origins": [
        {
            "origin": "https://erptest.epbox.cn",
            "localStorage": [
                {"name": "Admin-Token", "value": "test-jwt"},
                {"name": "Admin-Expires-In", "value": "720"},
            ],
        }
    ],
}


@pytest.mark.asyncio
async def test_create_authenticated_session_success():
    """create_authenticated_session writes storage_state to temp file and passes path."""
    mock_session = MagicMock()

    with (
        patch(
            "backend.core.auth_session_factory.auth_service"
        ) as mock_auth_svc,
        patch(
            "backend.core.auth_session_factory.BrowserSession",
            return_value=mock_session,
        ) as mock_bs_cls,
    ):
        mock_auth_svc.get_storage_state_for_role = AsyncMock(
            return_value=SAMPLE_STORAGE_STATE
        )

        from backend.core.auth_session_factory import create_authenticated_session

        result = await create_authenticated_session("main")

    assert result is mock_session
    mock_auth_svc.get_storage_state_for_role.assert_awaited_once_with("main")
    mock_bs_cls.assert_called_once()
    call_kwargs = mock_bs_cls.call_args.kwargs

    # storage_state is now a temp file path (string), not a dict
    storage_state_path = call_kwargs["storage_state"]
    assert isinstance(storage_state_path, str)
    assert storage_state_path.endswith(".json")
    assert "auth_state_main_" in storage_state_path

    # Verify the temp file contains the correct storage_state JSON
    import os
    assert os.path.exists(storage_state_path)
    with open(storage_state_path) as f:
        loaded = json.load(f)
    assert loaded == SAMPLE_STORAGE_STATE

    # Clean up temp file
    os.unlink(storage_state_path)


@pytest.mark.asyncio
async def test_create_authenticated_session_preserves_browser_args():
    """create_authenticated_session uses SERVER_BROWSER_ARGS and ViewportSize."""
    mock_session = MagicMock()

    with (
        patch(
            "backend.core.auth_session_factory.auth_service"
        ) as mock_auth_svc,
        patch(
            "backend.core.auth_session_factory.BrowserSession",
            return_value=mock_session,
        ) as mock_bs_cls,
        patch(
            "backend.core.auth_session_factory.SERVER_BROWSER_ARGS",
            ["--no-sandbox", "--disable-gpu"],
        ),
    ):
        mock_auth_svc.get_storage_state_for_role = AsyncMock(
            return_value=SAMPLE_STORAGE_STATE
        )

        from backend.core.auth_session_factory import create_authenticated_session

        await create_authenticated_session("main")

    call_kwargs = mock_bs_cls.call_args.kwargs
    assert call_kwargs["args"] == ["--no-sandbox", "--disable-gpu"]
    viewport = call_kwargs["viewport"]
    assert viewport.width == 1920
    assert viewport.height == 1080


@pytest.mark.asyncio
async def test_create_authenticated_session_auth_failure():
    """create_authenticated_session propagates TokenFetchError (no catch)."""
    from backend.core.auth_service import TokenFetchError

    with patch(
        "backend.core.auth_session_factory.auth_service"
    ) as mock_auth_svc:
        mock_auth_svc.get_storage_state_for_role = AsyncMock(
            side_effect=TokenFetchError(role="main", reason="请求超时 (>10s)")
        )

        from backend.core.auth_session_factory import create_authenticated_session

        with pytest.raises(TokenFetchError) as exc_info:
            await create_authenticated_session("main")

    assert "main" in str(exc_info.value)
