"""Unit tests for AccountService — role-based ERP credential resolution.

Tests cover ACCT-01 (resolve returns AccountInfo), ACCT-02 (resolve raises
on unknown/missing/empty), and ACCT-03 (get_login_url from settings).
"""

from unittest.mock import patch

import pytest

from backend.core.account_service import AccountInfo, AccountService


# ---------------------------------------------------------------------------
# Task 1: AccountInfo frozen dataclass + ROLE_MAP + resolve()
# ---------------------------------------------------------------------------


def test_account_info_is_frozen():
    """AccountInfo is frozen — assigning to a field raises FrozenInstanceError."""
    info = AccountInfo(account="a", password="p", role="r")
    with pytest.raises(AttributeError, match="cannot assign"):
        info.account = "b"  # type: ignore[misc]


def test_account_info_is_hashable():
    """Frozen dataclass is hashable — can be used in sets/dicts."""
    info = AccountInfo(account="a", password="p", role="r")
    assert isinstance(hash(info), int)


def test_account_info_fields():
    """AccountInfo has exactly 3 fields: account, password, role."""
    info = AccountInfo(account="a", password="p", role="r")
    assert info.account == "a"
    assert info.password == "p"
    assert info.role == "r"


def test_role_map_has_seven_ui_roles():
    """ROLE_MAP contains exactly 7 UI login roles."""
    expected = {"main", "special", "vice", "camera", "platform", "super", "idle"}
    assert set(AccountService.ROLE_MAP.keys()) == expected


def test_role_map_excludes_bot():
    """bot role is excluded — it uses phone/wechatId login, not UI form."""
    assert "bot" not in AccountService.ROLE_MAP


def test_resolve_main_account():
    """resolve('main') returns correct AccountInfo from config."""
    config = {"main_account": "Y59800075", "password": "Aa123456"}
    svc = AccountService(config=config)
    result = svc.resolve("main")
    assert result == AccountInfo(account="Y59800075", password="Aa123456", role="main")


def test_resolve_super_uses_super_admin_password():
    """resolve('super') uses super_admin_password, not password."""
    config = {"super_admin_account": "admin", "super_admin_password": "admin@*erp2025"}
    svc = AccountService(config=config)
    result = svc.resolve("super")
    assert result.password == "admin@*erp2025"
    assert result.account == "admin"


def test_resolve_platform_uses_password_not_super():
    """resolve('platform') uses password field, NOT super_admin_password."""
    config = {"platform_account": "1531503140", "password": "Aa123456"}
    svc = AccountService(config=config)
    result = svc.resolve("platform")
    assert result.password == "Aa123456"
    assert result.account == "1531503140"


def test_resolve_all_seven_roles():
    """All 7 UI roles resolve successfully with appropriate config."""
    config = {
        "main_account": "M",
        "special_account": "S",
        "vice_account": "V",
        "camera_account": "C",
        "platform_account": "P",
        "super_admin_account": "SA",
        "idle_account": "I",
        "password": "pw",
        "super_admin_password": "sapw",
    }
    svc = AccountService(config=config)
    expected = {
        "main": ("M", "pw"),
        "special": ("S", "pw"),
        "vice": ("V", "pw"),
        "camera": ("C", "pw"),
        "platform": ("P", "pw"),
        "super": ("SA", "sapw"),
        "idle": ("I", "pw"),
    }
    for role, (acct, pw) in expected.items():
        result = svc.resolve(role)
        assert result.account == acct, f"role={role}"
        assert result.password == pw, f"role={role}"
        assert result.role == role


def test_resolve_raises_on_unknown_role():
    """resolve('nonexistent') raises ValueError listing all 7 roles."""
    svc = AccountService(config={"password": "x"})
    with pytest.raises(ValueError, match="nonexistent") as exc_info:
        svc.resolve("nonexistent")
    msg = str(exc_info.value)
    for role in ["main", "special", "vice", "camera", "platform", "super", "idle"]:
        assert role in msg, f"error message should list role '{role}'"


def test_resolve_raises_on_missing_account_field():
    """resolve raises ValueError when config lacks the account field for a role."""
    svc = AccountService(config={"password": "x"})  # no main_account key
    with pytest.raises(ValueError, match="main_account"):
        svc.resolve("main")


def test_resolve_raises_on_empty_account():
    """resolve raises ValueError when account field is empty string."""
    svc = AccountService(config={"main_account": "", "password": "x"})
    with pytest.raises(ValueError, match="main_account"):
        svc.resolve("main")


# ---------------------------------------------------------------------------
# Task 2: get_login_url() + settings integration (ACCT-03)
# ---------------------------------------------------------------------------


def test_get_login_url():
    """get_login_url() returns base_url + '/login'."""
    svc = AccountService(config={"main_account": "a", "password": "p"})
    with patch("backend.config.get_settings") as mock:
        mock.return_value.erp_base_url = "https://erptest.epbox.cn/epbox_erp"
        assert svc.get_login_url() == "https://erptest.epbox.cn/epbox_erp/login"


def test_get_login_url_strips_trailing_slash():
    """get_login_url() strips trailing slash to avoid double-slash."""
    svc = AccountService(config={"main_account": "a", "password": "p"})
    with patch("backend.config.get_settings") as mock:
        mock.return_value.erp_base_url = "https://erptest.epbox.cn/epbox_erp/"
        assert svc.get_login_url() == "https://erptest.epbox.cn/epbox_erp/login"


def test_get_login_url_empty_base():
    """get_login_url() with empty base_url returns '/login'."""
    svc = AccountService(config={"main_account": "a", "password": "p"})
    with patch("backend.config.get_settings") as mock:
        mock.return_value.erp_base_url = ""
        assert svc.get_login_url() == "/login"
