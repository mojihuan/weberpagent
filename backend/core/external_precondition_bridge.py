"""Bridge module for webseleniumerp integration.

This module isolates all external project imports and provides
a clean API for operation code discovery and execution.
"""

import sys
import logging
import inspect
import re
import asyncio
from pathlib import Path
from typing import Any, get_type_hints

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


def configure_external_path(weberp_path: str | None) -> tuple[bool, str]:
    """Configure external module path.

    Args:
        weberp_path: Path to webseleniumerp project root

    Returns:
        (success, message)
    """
    global _path_configured

    if not weberp_path:
        return True, "WEBSERP_PATH not configured (optional feature)"

    path = Path(weberp_path)
    if not path.exists():
        return False, f"WEBSERP_PATH does not exist: {weberp_path}"
    if not path.is_dir():
        return False, f"WEBSERP_PATH is not a directory: {weberp_path}"

    path_str = str(path.resolve())
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
        logger.info(f"Added to sys.path: {path_str}")

    _path_configured = True
    return True, f"Path configured: {weberp_path}"


def load_pre_front_class() -> tuple[type | None, str | None]:
    """Load PreFront class lazily.

    Returns:
        (class_or_none, error_or_none)
    """
    global _pre_front_class, _import_error

    if _pre_front_class is not None:
        return _pre_front_class, None

    if _import_error is not None:
        return None, _import_error

    # Configure path from settings if not already done
    if not _path_configured:
        from backend.config import get_settings
        settings = get_settings()
        if settings.weberp_path:
            success, msg = configure_external_path(settings.weberp_path)
            if not success:
                _import_error = msg
                return None, _import_error

    try:
        from common.base_prerequisites import PreFront
        _pre_front_class = PreFront
        logger.info("Successfully loaded PreFront class")
        return _pre_front_class, None
    except ImportError as e:
        _import_error = (
            f"Failed to import PreFront: {e}. "
            f"Ensure config/settings.py exists in webseleniumerp."
        )
        logger.error(_import_error)
        return None, _import_error
    except Exception as e:
        _import_error = f"Unexpected error loading PreFront: {e}"
        logger.error(_import_error, exc_info=True)
        return None, _import_error


def is_available() -> bool:
    """Check if external module is available."""
    cls, _ = load_pre_front_class()
    return cls is not None


def load_base_params_class() -> tuple[type | None, str | None]:
    """Load base_params module class lazily.

    Returns:
        (class_or_none, error_or_none)
    """
    global _base_params_class, _base_params_import_error

    if _base_params_class is not None:
        return _base_params_class, None

    if _base_params_import_error is not None:
        return None, _base_params_import_error

    # Configure path from settings if not already done
    if not _path_configured:
        from backend.config import get_settings
        settings = get_settings()
        if settings.weberp_path:
            success, msg = configure_external_path(settings.weberp_path)
            if not success:
                _base_params_import_error = msg
                return None, _base_params_import_error

    try:
        from common.base_params import BaseImport
        _base_params_class = BaseImport
        logger.info("Successfully loaded BaseImport class")
        return _base_params_class, None
    except ImportError as e:
        _base_params_import_error = (
            f"Failed to import BaseImport: {e}. "
            f"Ensure config/settings.py exists in webseleniumerp."
        )
        logger.error(_base_params_import_error)
        return None, _base_params_import_error
    except Exception as e:
        _base_params_import_error = f"Unexpected error loading BaseImport: {e}"
        logger.error(_base_params_import_error, exc_info=True)
        return None, _base_params_import_error


def load_base_assertions_class() -> tuple[dict[str, type] | None, str | None]:
    """Load assertion classes lazily from common.base_assertions.

    Returns:
        (dict mapping class names to classes, error_or_none)
    """
    global _assertion_classes_cache, _assertion_import_error

    if _assertion_classes_cache is not None:
        return _assertion_classes_cache, None

    if _assertion_import_error is not None:
        return None, _assertion_import_error

    # Configure path from settings if not already done
    if not _path_configured:
        from backend.config import get_settings
        settings = get_settings()
        if settings.weberp_path:
            success, msg = configure_external_path(settings.weberp_path)
            if not success:
                _assertion_import_error = msg
                return None, _assertion_import_error

    try:
        from common.base_assertions import PcAssert, MgAssert, McAssert
        _assertion_classes_cache = {
            'PcAssert': PcAssert,
            'MgAssert': MgAssert,
            'McAssert': McAssert
        }
        logger.info("Successfully loaded assertion classes (PcAssert, MgAssert, McAssert)")
        return _assertion_classes_cache, None
    except ImportError as e:
        _assertion_import_error = (
            f"Failed to import assertion classes: {e}. "
            f"Ensure config/settings.py exists in webseleniumerp."
        )
        logger.error(_assertion_import_error)
        return None, _assertion_import_error
    except Exception as e:
        _assertion_import_error = f"Unexpected error loading assertion classes: {e}"
        logger.error(_assertion_import_error, exc_info=True)
        return None, _assertion_import_error


def _parse_docstring_params(docstring: str) -> list[dict]:
    """Parse parameter definitions from docstring.

    Handles format like:
        i：库存状态 2库存中 1待入库 3已出库
        j：物品状态 13待销售 3待分货...

    Returns:
        List of parameter dicts with name, description
    """
    params = []
    if not docstring:
        return params

    lines = docstring.strip().split('\n')
    for line in lines[1:]:  # Skip first line (method description)
        line = line.strip()
        if not line:
            continue

        # Match pattern: "param_name：description" or "param_name: description"
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[：:]\s*(.+)$', line)
        if match:
            param_name = match.group(1)
            param_desc = match.group(2).strip()
            params.append({
                "name": param_name,
                "type": "int",  # These are typically integers for API parameters
                "required": False,  # Docstring params are usually optional kwargs
                "default": None,
                "description": param_desc
            })

    return params


def _parse_data_options_from_source(method) -> list[str]:
    """Extract data options from method source code.

    Parses the methods = {...} dictionary to extract available keys.

    Args:
        method: The method to parse

    Returns:
        List of available data options (e.g., ['main', 'a', 'b'])
    """
    try:
        source = inspect.getsource(method)
    except (OSError, TypeError):
        return ['main']  # Default fallback

    # Find methods = {...} pattern
    match = re.search(r"methods\s*=\s*\{([^}]+)\}", source, re.DOTALL)
    if not match:
        return ['main']

    methods_dict_str = match.group(1)

    # Extract quoted keys from the dictionary
    keys = re.findall(r"['\"](\w+)['\"]\s*:", methods_dict_str)
    return keys if keys else ['main']


def _parse_param_options(description: str) -> list[dict]:
    """Parse option values from parameter description.

    Parses formats like:
        i: 订单状态 1待发货 2待取件
        j: 物品状态 13待销售 3待分货

    Args:
        description: Parameter description string

    Returns:
        List of option dicts: [{"value": int, "label": str}, ...]
    """
    options = []

    # Pattern: digit followed by non-digit text
    # Matches: "1待发货" -> (1, "待发货")
    pattern = r'(\d+)([^\d]+)'

    for match in re.finditer(pattern, description):
        value = int(match.group(1))
        label = match.group(2).strip()
        if label:
            options.append({"value": value, "label": label})

    return options


def extract_method_info(cls: type, method_name: str) -> dict | None:
    """Extract method information including parameters with types.

    Args:
        cls: The class containing the method
        method_name: Name of the method to extract info from

    Returns:
        dict with name, description, and parameters, or None for private methods
    """
    # Skip private methods
    if method_name.startswith('_'):
        return None

    # Skip internal utility methods from BaseApi that shouldn't be called directly
    INTERNAL_METHODS = {
        'get_handle_response', 'request_handle', 'get_page_num',
        'get_response_data', 'get_token', 'get_cached_tokens',
        'set_cached_tokens', 'get_page_params', 'process_params',
        'process_and_check_params', 'check_unsupported_params',
        'compare_json', 'get_file_and_class_name', 'get_formatted_datetime',
        'get_current_time', 'get_the_date', 'get_current_timestamp_ms',
        'save_to_cache', 'load_from_cache', 'save_json_file', 'load_json_file',
        'generate_hourly_sessions', 'generate_five_minute_sessions',
        'wait_until_next_five_minute', 'wait_for_five_minutes', 'wait_default',
        'get_nested_field', '_get_nested_field',
        'handle_api_error', 'clear_pkl_files'
    }
    if method_name in INTERNAL_METHODS:
        return None

    method = getattr(cls, method_name, None)
    if method is None:
        return None

    try:
        sig = inspect.signature(method)
        type_hints = get_type_hints(method)
    except (ValueError, TypeError) as e:
        logger.warning(f"Cannot get signature for {method_name}: {e}")
        return None

    # Extract description from docstring (first line)
    docstring = method.__doc__ or ""
    description = docstring.strip().split('\n')[0] if docstring.strip() else method_name

    parameters = []
    existing_param_names = set()

    for param_name, param in sig.parameters.items():
        # Skip 'self' parameter
        if param_name == 'self':
            continue

        # Skip *args and **kwargs (VAR_POSITIONAL and VAR_KEYWORD)
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        existing_param_names.add(param_name)

        # Determine type
        param_type = type_hints.get(param_name, Any)
        type_str = getattr(param_type, '__name__', str(param_type))
        if type_str.startswith('typing.'):
            type_str = str(param_type).replace('typing.', '')

        # Determine if required and default value
        has_default = param.default != inspect.Parameter.empty
        parameters.append({
            "name": param_name,
            "type": type_str,
            "required": not has_default,
            "default": repr(param.default) if has_default else None
        })

    # Parse additional kwargs parameters from docstring
    docstring_params = _parse_docstring_params(docstring)
    for param in docstring_params:
        if param["name"] not in existing_param_names:
            parameters.append(param)

    return {
        "name": method_name,
        "description": description,
        "parameters": parameters
    }


def discover_class_methods(cls: type) -> list[dict]:
    """Discover all public methods in a class.

    Args:
        cls: The class to scan for methods

    Returns:
        List of method info dicts
    """
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_'):
            method_info = extract_method_info(cls, name)
            if method_info is not None:
                methods.append(method_info)
    return methods


def get_data_methods_grouped() -> list[dict]:
    """Get data methods grouped by class name.

    Returns:
        List of class groups with their methods
    """
    global _data_methods_cache

    if _data_methods_cache is not None:
        return _data_methods_cache

    # Load base_params module
    cls, error = load_base_params_class()
    if error:
        _data_methods_cache = []
        return _data_methods_cache

    try:
        # Import the base_params module to scan for all classes
        import common.base_params as base_params_module

        classes = []
        for name, obj in inspect.getmembers(base_params_module, predicate=inspect.isclass):
            # Skip imported classes (only include classes defined in the module)
            if obj.__module__ != 'common.base_params':
                continue

            # Discover methods for this class
            methods = discover_class_methods(obj)
            if methods:  # Only include classes with public methods
                classes.append({
                    "name": name,
                    "methods": methods
                })

        _data_methods_cache = classes
        return _data_methods_cache
    except Exception as e:
        logger.error(f"Failed to scan base_params module: {e}", exc_info=True)
        _data_methods_cache = []
        return _data_methods_cache


async def execute_data_method(
    class_name: str,
    method_name: str,
    params: dict,
    timeout: float = 30.0
) -> dict:
    """Execute a data method with timeout protection.

    Args:
        class_name: Name of the class in base_params module
        method_name: Name of the method to execute
        params: Dictionary of parameters to pass to the method
        timeout: Maximum execution time in seconds

    Returns:
        dict with success, data/error, and error_type fields
    """
    # Load the class
    cls, error = load_base_params_class()
    if error:
        return {
            "success": False,
            "error": error,
            "error_type": "ImportError"
        }

    # Get the class by name
    try:
        target_class = None
        for name, obj in inspect.getmembers(
            inspect.getmodule(cls),
            predicate=inspect.isclass
        ):
            if name == class_name:
                target_class = obj
                break

        if target_class is None:
            return {
                "success": False,
                "error": f"Class '{class_name}' not found in base_params module",
                "error_type": "NotFoundError"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to find class: {e}",
            "error_type": "SystemError"
        }

    # Get the method
    try:
        instance = target_class()
        method = getattr(instance, method_name, None)
        if method is None:
            return {
                "success": False,
                "error": f"Method '{method_name}' not found in class '{class_name}'",
                "error_type": "NotFoundError"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to instantiate class: {e}",
            "error_type": "InstantiationError"
        }

    # Execute with timeout
    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: method(**params)),
            timeout=timeout
        )
        return {
            "success": True,
            "data": result
        }
    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": f"Execution timeout ({timeout}s)",
            "error_type": "TimeoutError"
        }
    except TypeError as e:
        return {
            "success": False,
            "error": f"Parameter error: {e}",
            "error_type": "ParameterError"
        }
    except Exception as e:
        logger.error(f"Failed to execute method: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "error_type": "ExecutionError"
        }


def get_unavailable_reason() -> str | None:
    """Get reason why external module is unavailable."""
    cls, err = load_pre_front_class()
    if cls is not None:
        return None
    return err or "External module not configured"


def _parse_operations_from_source() -> tuple[dict[str, str], list[dict]]:
    """Parse operations from source code.

    Returns:
        (operations_dict, modules_list)
    """
    global _operations_cache, _modules_cache

    if _operations_cache is not None and _modules_cache is not None:
        return _operations_cache, _modules_cache

    PreFront, error = load_pre_front_class()
    if error:
        _operations_cache = {}
        _modules_cache = []
        return _operations_cache, _modules_cache

    try:
        source = inspect.getsource(PreFront.operations)
    except (OSError, TypeError) as e:
        logger.error(f"Failed to get source: {e}")
        _operations_cache = {}
        _modules_cache = []
        return _operations_cache, _modules_cache

    operations = {}
    modules_dict: dict[str, list] = {}

    lines = source.split('\n')
    current_module = "未分组"

    for line in lines:
        stripped = line.strip()

        # Module comment: # 配件管理|配件采购|新增采购
        if stripped.startswith('#') and '|' in stripped:
            parts = stripped[1:].strip().split('|')
            if len(parts) >= 2:
                current_module = f"{parts[0]} - {parts[1]}"
            else:
                current_module = parts[0] if parts else "未分组"

        # Operation code: 'FA1': [self.request...]
        elif "'" in stripped and "': [" in stripped:
            match = re.search(r"'([A-Z0-9@]+)'", stripped)
            if match:
                code = match.group(1)
                desc_match = re.search(r"#\s*(.+)$", stripped)
                description = desc_match.group(1) if desc_match else code
                operations[code] = description

                if current_module not in modules_dict:
                    modules_dict[current_module] = []
                modules_dict[current_module].append({
                    "code": code,
                    "description": description
                })

    _operations_cache = operations
    _modules_cache = [
        {"name": name, "operations": ops}
        for name, ops in modules_dict.items()
    ]

    return _operations_cache, _modules_cache


def get_available_operations() -> dict[str, str]:
    """Get all available operation codes with descriptions."""
    operations, _ = _parse_operations_from_source()
    return operations


def get_operations_grouped() -> list[dict]:
    """Get operations grouped by module."""
    _, modules = _parse_operations_from_source()
    return modules


def generate_precondition_code(operation_codes: list[str], weberp_path: str) -> str:
    """Generate precondition code for selected operation codes.

    Args:
        operation_codes: List of operation codes to execute
        weberp_path: Path to webseleniumerp for sys.path

    Returns:
        Python code string for PreconditionService
    """
    codes_str = ", ".join(f"'{c}'" for c in operation_codes)
    return f'''import sys
sys.path.insert(0, '{weberp_path}')

from common.base_prerequisites import PreFront

pre_front = PreFront()
pre_front.operations([{codes_str}])

context['precondition_result'] = 'success'
'''


def execute_operations(operation_codes: list[str]) -> tuple[bool, str, dict[str, Any]]:
    """Execute precondition operations directly.

    Args:
        operation_codes: List of operation codes to execute

    Returns:
        (success, message, context_data)
    """
    PreFront, error = load_pre_front_class()
    if error:
        return False, error, {}

    try:
        pre_front = PreFront()
        pre_front.operations(operation_codes)
        return True, f"Executed operations: {operation_codes}", {}
    except Exception as e:
        logger.error(f"Failed to execute operations: {e}", exc_info=True)
        return False, str(e), {}


def reset_cache():
    """Reset all cached data (for testing)."""
    global _pre_front_class, _import_error, _operations_cache, _modules_cache, _path_configured
    global _base_params_class, _base_params_import_error, _data_methods_cache
    global _assertion_classes_cache, _assertion_import_error
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
