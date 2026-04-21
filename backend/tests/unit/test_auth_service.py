"""Unit tests for AuthService — HTTP token fetch."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from backend.core.auth_service import AuthService, TokenFetchError


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
