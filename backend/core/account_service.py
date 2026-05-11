"""Account service — resolves ERP role names to login credentials.

Provides AccountService (module-level singleton) that maps role names to
account/password pairs from user_info.py INFO dict, and composes login URL
from settings.erp_base_url.
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AccountInfo:
    """Immutable login credentials for a role."""

    account: str
    password: str
    role: str


class AccountService:
    """Resolves role names to ERP login credentials.

    Uses a static ROLE_MAP that maps role names to (account_field, password_field)
    tuples. The field names are keys into the user_info.py INFO dict.
    """

    ROLE_MAP: dict[str, tuple[str, str]] = {
        "main": ("main_account", "password"),  # api_login.py:78
        "special": ("special_account", "password"),  # api_login.py:90
        "vice": ("vice_account", "password"),  # api_login.py:84
        "camera": ("camera_account", "password"),  # api_login.py:114
        "platform": ("platform_account", "password"),  # api_login.py:102
        "super": ("super_admin_account", "super_admin_password"),  # api_login.py:108
        "idle": ("idle_account", "password"),  # api_login.py:96
    }

    def __init__(self, config: dict[str, str] | None = None) -> None:
        self._config = config
        self._loaded = config is not None

    def _ensure_loaded(self) -> None:
        """Lazily load config on first resolve, after sys.path is ready."""
        if self._loaded:
            return
        import sys
        from backend.config import get_settings
        settings = get_settings()
        weberp_path = settings.weberp_path
        if weberp_path:
            from pathlib import Path
            # Need the parent directory so Python can find the 'webseleniumerp' package
            parent_dir = str(Path(weberp_path).resolve().parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
                logger.info(f"Added to sys.path: {parent_dir}")
        self._config = self._load_config()
        logger.info(f"Loaded config with {len(self._config)} keys: {list(self._config.keys())[:5]}...")
        self._loaded = True

    @staticmethod
    def _load_config() -> dict[str, str]:
        """Lazy-load USER_INFO dict from webseleniumerp."""
        try:
            try:
                from webseleniumerp.config.user_data import USER_INFO

                return dict(USER_INFO)
            except ImportError:
                from webseleniumerp.config.user_info import INFO

                return dict(INFO)
        except ImportError as e:
            logger.warning(f"webseleniumerp.config.user_info not available: {e}")
            return {}
        except Exception as e:
            logger.warning(f"Failed to load user_info: {type(e).__name__}: {e}")
            return {}

    def resolve(self, role: str) -> AccountInfo:
        """Resolve a role name to an AccountInfo with credentials.

        Raises:
            ValueError: If role is unknown or config field is missing/empty.
        """
        self._ensure_loaded()
        if role not in self.ROLE_MAP:
            available = ", ".join(sorted(self.ROLE_MAP.keys()))
            raise ValueError(f"unknown role: '{role}'. available roles: {available}")

        account_field, password_field = self.ROLE_MAP[role]
        account = self._config.get(account_field, "")
        password = self._config.get(password_field, "")

        if not account:
            raise ValueError(
                f"role '{role}' account config missing: field '{account_field}' not found"
            )

        return AccountInfo(account=account, password=password, role=role)

    def get_login_url(self) -> str:
        """Return login URL composed from settings.erp_base_url + '/login'."""
        from backend.config import get_settings

        settings = get_settings()
        base = settings.erp_base_url.rstrip("/")
        return f"{base}/login"


account_service = AccountService()
