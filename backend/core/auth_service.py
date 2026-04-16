"""Auth service — HTTP token acquisition and Playwright storage_state construction.

Provides AuthService (module-level singleton) that:
1. Fetches ERP access tokens via HTTP POST to /auth/login
2. Constructs Playwright-compatible storage_state dicts with localStorage entries
3. Combines AccountService resolution with token fetch for role-based auth

No browser instances required — purely HTTP-based token acquisition.
"""

import logging
from typing import Any
from urllib.parse import urlparse

import httpx

from backend.config.settings import get_settings
from backend.core.account_service import account_service

logger = logging.getLogger(__name__)


class TokenFetchError(Exception):
    """Raised when ERP token acquisition fails.

    Contains the role name and human-readable reason for diagnostics.
    """

    def __init__(self, role: str, reason: str) -> None:
        self.role = role
        self.reason = reason
        super().__init__(f"Token 获取失败 [role={role}]: {reason}")

    def __str__(self) -> str:
        return f"Token 获取失败 [role={self.role}]: {self.reason}"


class AuthService:
    """HTTP-based ERP token acquisition and storage_state construction.

    Provides methods to:
    - fetch_token: POST to ERP /auth/login and extract access_token
    - build_storage_state: construct Playwright storage_state dict with localStorage
    - get_storage_state_for_role: combine AccountService + fetch + build
    """

    def __init__(self) -> None:
        """Initialize AuthService. Settings are read lazily per call."""
        pass

    async def fetch_token(
        self,
        account: str,
        password: str,
        role: str = "",
    ) -> str:
        """Fetch access_token from ERP via HTTP POST.

        Args:
            account: ERP username.
            password: ERP password.
            role: Role name for error messages.

        Returns:
            The access_token string from ERP login response.

        Raises:
            TokenFetchError: On timeout, HTTP error, or malformed response.
        """
        settings = get_settings()
        login_url = f"{settings.erp_base_url.rstrip('/')}/auth/login"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    login_url,
                    json={"username": account, "password": password},
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code != 200:
                    raise TokenFetchError(
                        role=role,
                        reason=f"HTTP {response.status_code}: {response.text[:200]}",
                    )

                data = response.json()
                token = data["data"]["access_token"]

                logger.info(
                    f"Token 获取成功: role={role}, token={token[:20]}..."
                )
                return token

        except httpx.TimeoutException:
            raise TokenFetchError(
                role=role,
                reason="请求超时 (>10s)",
            )
        except TokenFetchError:
            raise
        except (KeyError, TypeError):
            raise TokenFetchError(
                role=role,
                reason=f"响应格式异常: {response.text[:200]}",
            )

    def build_storage_state(self, token: str) -> dict[str, Any]:
        """Construct Playwright storage_state dict from access_token.

        Creates a storage_state with empty cookies and localStorage entries
        for Admin-Token and Admin-Expires-In, targeting the ERP origin.

        Args:
            token: JWT access_token string.

        Returns:
            Playwright-compatible storage_state dict.
        """
        settings = get_settings()
        origin = self._extract_origin(settings.erp_base_url)

        return {
            "cookies": [],
            "origins": [
                {
                    "origin": origin,
                    "localStorage": [
                        {"name": "Admin-Token", "value": token},
                        {"name": "Admin-Expires-In", "value": "720"},
                    ],
                }
            ],
        }

    async def get_storage_state_for_role(
        self, role: str
    ) -> dict[str, Any]:
        """Get storage_state for a role by resolving credentials and fetching token.

        Combines AccountService.resolve() to get credentials,
        fetch_token() to get access_token, and build_storage_state()
        to construct the Playwright storage_state dict.

        Args:
            role: ERP role name (e.g. "main", "special", "vice").

        Returns:
            Playwright-compatible storage_state dict.

        Raises:
            TokenFetchError: If token acquisition fails.
            ValueError: If role is unknown to AccountService.
        """
        account_info = account_service.resolve(role)
        token = await self.fetch_token(
            account_info.account,
            account_info.password,
            role=role,
        )
        return self.build_storage_state(token)

    @staticmethod
    def _extract_origin(url: str) -> str:
        """Extract origin (scheme + netloc) from a URL, stripping path.

        Args:
            url: Full URL, e.g. "https://erptest.epbox.cn/epbox_erp"

        Returns:
            Origin string, e.g. "https://erptest.epbox.cn"
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"


auth_service = AuthService()  # module-level singleton
