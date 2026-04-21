"""Auth service — HTTP token acquisition.

Provides AuthService (module-level singleton) that:
1. Fetches ERP access tokens via HTTP POST to /auth/login

No browser instances required — purely HTTP-based token acquisition.
"""

import logging
from urllib.parse import urlparse

import httpx

from backend.config.settings import get_settings

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
    """HTTP-based ERP token acquisition.

    Provides methods to:
    - fetch_token: POST to ERP /auth/login and extract access_token
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
