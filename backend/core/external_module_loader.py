"""External module loading and caching.

Split from external_precondition_bridge.py per D-07.
Handles lazy-loading, path configuration, and class loading for external
webseleniumerp integration.
"""

import importlib
import sys
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Module-level singleton state
_pre_front_class = None
_import_error = None
_operations_cache: dict[str, str] | None = None
_modules_cache: list[dict] | None = None
_path_configured = False

# Data methods discovery state
_base_params_class = None
_base_params_import_error = None
_data_methods_cache: list[dict] | None = None

# Assertion classes discovery state
_assertion_classes_cache: dict[str, type] | None = None
_assertion_import_error: str | None = None
_assertion_methods_cache: list[dict] | None = None

# Docstring-based method mapping state
_docstring_method_map: dict[str, dict[str, str]] | None = None
_import_api_patched: bool = False

# LoginApi state for headers resolution
_login_api_instance = None
_login_api_error: str | None = None

# Assertion fields discovery state
_assertion_fields_cache: list[dict] | None = None
_assertion_fields_error: str | None = None


def _lazy_load(
    cache_var_name: str,
    error_var_name: str,
    import_fn: callable,
    display_name: str,
) -> tuple[Any, str | None]:
    """Generic lazy-load with module-level caching."""
    cache_val = globals().get(cache_var_name)
    if cache_val is not None:
        return cache_val, None

    error_val = globals().get(error_var_name)
    if error_val is not None:
        return None, error_val

    # Configure path if needed
    if not _path_configured:
        from backend.config import get_settings
        settings = get_settings()
        if settings.weberp_path:
            success, msg = configure_external_path(settings.weberp_path)
            if not success:
                globals()[error_var_name] = msg
                return None, msg
        else:
            msg = "WEBSERP_PATH not configured (optional feature)"
            globals()[error_var_name] = msg
            return None, msg

    try:
        loaded = import_fn()
        globals()[cache_var_name] = loaded
        return loaded, None
    except ImportError as e:
        err = (
            f"Failed to import {display_name}: {e}. "
            f"Ensure config/settings.py exists in webseleniumerp."
        )
        globals()[error_var_name] = err
        logger.error(err)
        return None, err
    except Exception as e:
        err = f"Unexpected error loading {display_name}: {e}"
        globals()[error_var_name] = err
        logger.error(err, exc_info=True)
        return None, err


def _error_result(message: str, error_type: str, **extra_fields) -> dict:
    """Create a standardized error result dict."""
    result = {"success": False, "error": message, "error_type": error_type}
    result.update(extra_fields)
    return result


def configure_external_path(weberp_path: str | None) -> tuple[bool, str]:
    """Configure external module path."""
    global _path_configured

    if not weberp_path:
        return True, "WEBSERP_PATH not configured (optional feature)"

    path = Path(weberp_path)
    if not path.exists():
        return False, f"WEBSERP_PATH does not exist: {weberp_path}"
    if not path.is_dir():
        return False, f"WEBSERP_PATH is not a directory: {weberp_path}"

    path_str = str(path.resolve())
    parent_dir = str(path.resolve().parent)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
        logger.info(f"Added to sys.path: {path_str}")
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        logger.info(f"Added to sys.path: {parent_dir}")

    _path_configured = True
    return True, f"Path configured: {weberp_path}"


def load_pre_front_class() -> tuple[type | None, str | None]:
    """Load PreFront class lazily."""
    def _import_pre_front() -> Any:
        from common.base_prerequisites import PreFront
        return PreFront

    result, err = _lazy_load(
        '_pre_front_class', '_import_error', _import_pre_front, 'PreFront',
    )
    if result is not None:
        logger.info("Successfully loaded PreFront class")
    return result, err


def is_available() -> bool:
    """Check if external module is available."""
    cls, _ = load_pre_front_class()
    return cls is not None


def load_base_params_class() -> tuple[type | None, str | None]:
    """Load base_params module class lazily."""
    def _import_base_params() -> Any:
        from common.base_params import BaseImport
        return BaseImport

    result, err = _lazy_load(
        '_base_params_class', '_base_params_import_error',
        _import_base_params, 'BaseImport',
    )
    if result is not None:
        logger.info("Successfully loaded BaseImport class")
    return result, err


def load_base_assertions_class() -> tuple[dict[str, type] | None, str | None]:
    """Load assertion classes lazily from common.base_assertions."""
    def _import_assertion_classes() -> Any:
        import common.base_assertions as _ba_mod
        classes_cache = {}
        for _name in ('PcAssert', 'MgAssert', 'McAssert'):
            _cls = getattr(_ba_mod, _name, None)
            if _cls is not None:
                classes_cache[_name] = _cls
        if not classes_cache:
            raise ImportError("No assertion classes found in common.base_assertions")
        return classes_cache

    result, err = _lazy_load(
        '_assertion_classes_cache', '_assertion_import_error',
        _import_assertion_classes, 'assertion classes',
    )
    if result is not None:
        logger.info("Successfully loaded assertion classes (PcAssert, MgAssert, McAssert)")
    return result, err


def reset_cache() -> None:
    """Reset all cached data (for testing)."""
    global _pre_front_class, _import_error, _operations_cache, _modules_cache, _path_configured
    global _base_params_class, _base_params_import_error, _data_methods_cache
    global _assertion_classes_cache, _assertion_import_error, _assertion_methods_cache
    global _login_api_instance, _login_api_error
    global _assertion_fields_cache, _assertion_fields_error
    global _docstring_method_map, _import_api_patched
    _pre_front_class = None
    _import_error = None
    _operations_cache = None
    _modules_cache = None
    _path_configured = False
    _base_params_class = None
    _base_params_import_error = None
    _data_methods_cache = None
    _assertion_classes_cache = None
    _assertion_import_error = None
    _assertion_methods_cache = None
    _login_api_instance = None
    _login_api_error = None
    _assertion_fields_cache = None
    _assertion_fields_error = None
    _docstring_method_map = None
    _import_api_patched = False

    # Clear common.* entries from sys.modules
    stale_modules = [k for k in sys.modules if k == "common" or k.startswith("common.")]
    for key in stale_modules:
        del sys.modules[key]

    # Also clear any api.* entries
    stale_api_modules = [k for k in sys.modules if k == "api" or k.startswith("api.")]
    for key in stale_api_modules:
        del sys.modules[key]
