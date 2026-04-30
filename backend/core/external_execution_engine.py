"""External execution engine — assertion and data method execution.

Split from external_precondition_bridge.py per D-07.
Handles execution of assertion methods, data methods, operations,
and field discovery for external webseleniumerp integration.
"""

import ast
import asyncio
import inspect
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.core.precondition_service import ContextWrapper

import backend.core.external_module_loader as loader
from backend.core.external_method_discovery import (
    _build_docstring_method_map,
    _patch_import_api_aliases,
)

logger = logging.getLogger(__name__)


# Valid header identifiers matching LoginApi.headers keys
VALID_HEADER_IDENTIFIERS = {'main', 'idle', 'vice', 'special', 'platform', 'super', 'camera'}


def _get_login_api() -> Any:
    """Get or create LoginApi instance with caching."""
    def _import_login_api() -> Any:
        from api.api_login import LoginApi
        return LoginApi()

    result, _ = loader._lazy_load(
        '_login_api_instance', '_login_api_error',
        _import_login_api, 'LoginApi',
    )
    if result is not None:
        logger.info("Successfully created LoginApi instance for headers resolution")
    return result


def resolve_headers(identifier: str = 'main') -> dict:
    """Resolve header identifier to actual headers dict with auth tokens."""
    if identifier is None:
        identifier = 'main'

    if identifier not in VALID_HEADER_IDENTIFIERS:
        raise ValueError(
            f"Unknown header identifier: '{identifier}'. "
            f"Valid identifiers: {sorted(VALID_HEADER_IDENTIFIERS)}"
        )

    login_api = _get_login_api()
    if login_api is None:
        raise RuntimeError(
            "LoginApi not available. Ensure WEBSERP_PATH is configured and "
            "webseleniumerp project is accessible."
        )

    return login_api.headers.get(identifier, login_api.headers['main'])


def _parse_assertion_error(error_message: str) -> list[dict]:
    """Parse AssertionError message to extract field-level results."""
    field_results = []
    pattern = r"字段\s+['\"]([^'\"]+)['\"]\s+(预期值|预期包含):\s*['\"]([^'\"]*)['\"]\s*,\s*实际值:\s*['\"]([^'\"]*)['\"]"

    for match in re.finditer(pattern, error_message):
        field_name = match.group(1)
        comparison_type = match.group(2)
        expected = match.group(3)
        actual = match.group(4)
        field_results.append({
            'name': field_name,
            'expected': expected,
            'actual': actual,
            'passed': False,
            'comparison_type': 'equals' if comparison_type == '预期值' else 'contains'
        })
    if not field_results:
        field_results.append({
            'name': 'unknown',
            'expected': '',
            'actual': '',
            'passed': False,
            'description': error_message
        })
    return field_results


async def execute_assertion_method(
    class_name: str,
    method_name: str,
    headers: str | None = 'main',
    data: str = 'main',
    api_params: dict | None = None,
    field_params: dict | None = None,
    params: dict | None = None,
    timeout: float = 30.0
) -> dict:
    """Execute an assertion method with timeout protection."""
    import time
    start_time = time.time()

    if params and not field_params:
        field_params = params

    result = {
        'success': False,
        'passed': False,
        'fields': [],
        'error': None,
        'error_type': None,
        'duration': 0.0
    }
    classes_dict, error = loader.load_base_assertions_class()
    if error:
        result['error'] = error
        result['error_type'] = 'ImportError'
        result['duration'] = time.time() - start_time
        return result
    if class_name not in classes_dict:
        result['error'] = f"Assertion class '{class_name}' not found. Available: {list(classes_dict.keys())}"
        result['error_type'] = 'NotFoundError'
        result['duration'] = time.time() - start_time
        return result
    if headers and headers not in VALID_HEADER_IDENTIFIERS:
        result['error'] = f"Invalid headers identifier '{headers}'. Valid: {VALID_HEADER_IDENTIFIERS}"
        result['error_type'] = 'HeaderResolutionError'
        result['duration'] = time.time() - start_time
        return result
    try:
        assertion_class = classes_dict[class_name]
        assertion_instance = assertion_class()
        method = getattr(assertion_instance, method_name, None)
        if method is None:
            result['error'] = f"Method '{method_name}' not found in class '{class_name}'"
            result['error_type'] = 'NotFoundError'
            result['duration'] = time.time() - start_time
            return result
    except Exception as e:
        result['error'] = f"Failed to instantiate or access method: {e}"
        result['error_type'] = 'InstantiationError'
        result['duration'] = time.time() - start_time
        return result
    try:
        loop = asyncio.get_event_loop()
        merged_kwargs = {**(api_params or {}), **(field_params or {})}
        call_kwargs = _convert_now_values(merged_kwargs)
        call_kwargs['headers'] = headers
        call_kwargs['data'] = data
        logger.info(f"Calling {class_name}.{method_name} with kwargs: {list(call_kwargs.keys())}")
        await asyncio.wait_for(
            loop.run_in_executor(None, lambda: method(**call_kwargs)),
            timeout=timeout
        )
        result['success'] = True
        result['passed'] = True
        result['fields'] = []
    except asyncio.TimeoutError:
        result['error'] = f"Assertion execution timeout ({timeout}s)"
        result['error_type'] = 'TimeoutError'
    except AssertionError as e:
        result['success'] = True
        result['passed'] = False
        result['fields'] = _parse_assertion_error(str(e))
        result['error'] = str(e)
    except TypeError as e:
        logger.error(f"Parameter error in {class_name}.{method_name}: {e}", exc_info=True)
        result['error'] = f"Parameter error: {e}"
        result['error_type'] = 'ParameterError'
    except Exception as e:
        logger.error(f"Failed to execute assertion method: {e}", exc_info=True)
        result['error'] = str(e)
        result['error_type'] = 'ExecutionError'
    result['duration'] = time.time() - start_time
    return result


async def execute_all_assertions(
    assertions: list[dict],
    context: 'ContextWrapper',
    timeout_per_assertion: float = 30.0
) -> dict:
    """Execute multiple assertions in sequence and store results in context."""
    context.reset_assertion_tracking()

    results = []

    for index, assertion_config in enumerate(assertions):
        class_name = assertion_config.get('class_name') or assertion_config.get('className')
        method_name = assertion_config.get('method_name') or assertion_config.get('methodName')
        headers = assertion_config.get('headers', 'main')
        data = assertion_config.get('data', 'main')
        api_params = assertion_config.get('api_params', {})
        field_params = assertion_config.get('field_params', {})
        params = assertion_config.get('params', {})

        logger.info(
            f"Executing assertion {index + 1}/{len(assertions)}: "
            f"{class_name}.{method_name}"
        )

        try:
            result = await execute_assertion_method(
                class_name=class_name,
                method_name=method_name,
                headers=headers,
                data=data,
                api_params=api_params,
                field_params=field_params,
                params=params,
                timeout=timeout_per_assertion
            )
        except Exception as e:
            logger.error(f"Unexpected error in assertion {index}: {e}", exc_info=True)
            result = loader._error_result(
                str(e), 'UnexpectedError',
                passed=False, duration=0.0,
                field_results=[], method=method_name, class_name=class_name,
            )

        result['method'] = method_name
        result['class_name'] = class_name

        context.store_assertion_result(index, result)
        results.append(result)

        if result.get('passed'):
            logger.info(f"Assertion {index} passed")
        elif result.get('error_type'):
            logger.warning(f"Assertion {index} error: {result.get('error_type')}")
        else:
            logger.warning(f"Assertion {index} failed: {result.get('error')}")

    summary = context.get_assertion_results_summary()
    summary['results'] = results

    logger.info(
        f"Assertion execution complete: {summary['passed']}/{summary['total']} passed, "
        f"{summary['failed']} failed, {summary['errors']} errors"
    )

    return summary


async def _execute_sync_with_timeout(method: callable, kwargs: dict, timeout: float) -> dict:
    """Execute a synchronous method in thread pool with timeout protection."""
    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: method(**kwargs)),
            timeout=timeout
        )
        return {"success": True, "data": result}
    except asyncio.TimeoutError:
        return loader._error_result(f"Execution timeout ({timeout}s)", "TimeoutError")
    except TypeError as e:
        return loader._error_result(f"Parameter error: {e}", "ParameterError")
    except Exception as e:
        logger.error(f"Failed to execute method: {e}", exc_info=True)
        return loader._error_result(str(e), "ExecutionError")


async def execute_data_method(
    class_name: str,
    method_name: str,
    params: dict,
    timeout: float = 30.0
) -> dict:
    """Execute a data method with timeout protection."""
    cls, error = loader.load_base_params_class()
    if error:
        return loader._error_result(error, "ImportError")

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
            return loader._error_result(
                f"Class '{class_name}' not found in base_params module",
                "NotFoundError",
            )
    except Exception as e:
        return loader._error_result(f"Failed to find class: {e}", "SystemError")

    try:
        instance = target_class()
        method = getattr(instance, method_name, None)

        if method is None:
            docstring_map = _build_docstring_method_map()
            class_map = docstring_map.get(class_name, {})
            actual_name = class_map.get(method_name)

            if actual_name:
                logger.info(
                    f"Docstring match: '{method_name}' -> method '{actual_name}'"
                )
                method = getattr(instance, actual_name, None)
                if method is not None:
                    method_name = actual_name

        if method is None:
            docstring_map = _build_docstring_method_map()
            class_map = docstring_map.get(class_name, {})
            available = [
                f"'{doc_id}' -> {name}"
                for doc_id, name in sorted(class_map.items())
            ]
            available_str = ', '.join(available[:20])
            return loader._error_result(
                f"Method '{method_name}' not found in class '{class_name}'. "
                f"Available methods: {available_str}",
                "NotFoundError",
            )
    except Exception as e:
        return loader._error_result(f"Failed to instantiate class: {e}", "InstantiationError")

    _patch_import_api_aliases()

    return await _execute_sync_with_timeout(method, params, timeout)


def get_unavailable_reason() -> str | None:
    """Get reason why external module is unavailable."""
    cls, err = loader.load_pre_front_class()
    if cls is not None:
        return None
    return err or "External module not configured"


def require_external_available() -> None:
    """Raise HTTPException 503 if external module is not available."""
    if not loader.is_available():
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail=f"External module not available: {get_unavailable_reason()}"
        )


def _parse_operations_from_source() -> tuple[dict[str, str], list[dict]]:
    """Parse operations from source code."""
    if loader._operations_cache is not None and loader._modules_cache is not None:
        return loader._operations_cache, loader._modules_cache

    PreFront, error = loader.load_pre_front_class()
    if error:
        loader._operations_cache = {}
        loader._modules_cache = []
        return loader._operations_cache, loader._modules_cache

    try:
        source = inspect.getsource(PreFront.operations)
    except (OSError, TypeError) as e:
        logger.error(f"Failed to get source: {e}")
        loader._operations_cache = {}
        loader._modules_cache = []
        return loader._operations_cache, loader._modules_cache

    operations = {}
    modules_dict: dict[str, list] = {}

    lines = source.split('\n')
    current_module = "未分组"

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('#') and '|' in stripped:
            parts = stripped[1:].strip().split('|')
            if len(parts) >= 2:
                current_module = f"{parts[0]} - {parts[1]}"
            else:
                current_module = parts[0] if parts else "未分组"

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

    loader._operations_cache = operations
    loader._modules_cache = [
        {"name": name, "operations": ops}
        for name, ops in modules_dict.items()
    ]

    return loader._operations_cache, loader._modules_cache


def get_available_operations() -> dict[str, str]:
    """Get all available operation codes with descriptions."""
    operations, _ = _parse_operations_from_source()
    return operations


def get_operations_grouped() -> list[dict]:
    """Get operations grouped by module."""
    _, modules = _parse_operations_from_source()
    return modules


def generate_precondition_code(operation_codes: list[str], weberp_path: str) -> str:
    """Generate precondition code for selected operation codes."""
    codes_str = ", ".join(f"'{c}'" for c in operation_codes)
    return f'''import sys
sys.path.insert(0, '{weberp_path}')

from common.base_prerequisites import PreFront

pre_front = PreFront()
pre_front.operations([{codes_str}])

context['precondition_result'] = 'success'
'''


def execute_operations(operation_codes: list[str]) -> tuple[bool, str, dict[str, Any]]:
    """Execute precondition operations directly."""
    PreFront, error = loader.load_pre_front_class()
    if error:
        return False, error, {}

    try:
        pre_front = PreFront()
        pre_front.operations(operation_codes)
        return True, f"Executed operations: {operation_codes}", {}
    except Exception as e:
        logger.error(f"Failed to execute operations: {e}", exc_info=True)
        return False, str(e), {}


# =============================================================================
# Field Discovery functions
# =============================================================================

def _get_assertions_field_path() -> str | None:
    """Get path to base_assertions_field.py from settings."""
    from backend.config import get_settings
    settings = get_settings()
    if not settings.weberp_path:
        return None
    return str(Path(settings.weberp_path) / "common" / "base_assertions_field.py")


class ParamDictVisitor(ast.NodeVisitor):
    """Extract the param dictionary from assertive_field method."""

    def __init__(self) -> None:
        self.param_dict = None

    def visit_FunctionDef(self, node: ast.AST) -> None:
        if node.name == 'assertive_field':
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == 'param':
                            self.param_dict = child.value
        self.generic_visit(node)


def split_camel_case(name: str) -> list[str]:
    """Split camelCase name into words."""
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', name)
    return [w.lower() for w in words]


def infer_field_group(field_name: str) -> str:
    """Infer field group from name using naming patterns."""
    from backend.core.external_method_discovery import GROUP_RULES
    for pattern, group in GROUP_RULES:
        if re.search(pattern, field_name):
            return group
    return '通用字段'


def generate_field_description(field_name: str) -> str:
    """Generate Chinese description from field name."""
    from backend.core.external_method_discovery import KEYWORD_MAPPINGS
    words = split_camel_case(field_name)
    translated = []
    for word in words:
        if word in KEYWORD_MAPPINGS:
            translated.append(KEYWORD_MAPPINGS[word])
        else:
            translated.append(word.capitalize())

    return ''.join(translated) if translated else field_name


def _is_time_field(field_name: str, default_node: Any) -> bool:
    """Check if field is a time field based on name suffix or default value."""
    if isinstance(default_node, ast.Call):
        if isinstance(default_node.func, ast.Attribute):
            if default_node.func.attr == 'get_formatted_datetime':
                return True

    return field_name.endswith(('Time', 'time', 'Date', 'date'))


def _convert_now_values(kwargs: dict) -> dict:
    """Convert 'now' values to formatted datetime strings for time fields."""
    result = {}
    for key, value in kwargs.items():
        if _is_time_field(key, default_node=None) and isinstance(value, str) and value.startswith('now'):
            match = re.match(r'^now([+-])(\d+)([smhd])?$', value)
            if match:
                sign = 1 if match.group(1) == '+' else -1
                amount = int(match.group(2))
                unit = match.group(3) or 'm'

                from datetime import timedelta
                offset = timedelta(
                    seconds=sign * amount * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
                )
                result[key] = (datetime.now() + offset).strftime('%Y-%m-%d %H:%M:%S')
            elif value == 'now':
                result[key] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                result[key] = value
        else:
            result[key] = value
    return result


def parse_assertions_field_py(file_path: str) -> list[dict]:
    """Parse base_assertions_field.py and extract all fields."""
    source_code = Path(file_path).read_text(encoding='utf-8')
    tree = ast.parse(source_code)

    visitor = ParamDictVisitor()
    visitor.visit(tree)

    if visitor.param_dict is None:
        return []

    fields = []
    for key, value in zip(visitor.param_dict.keys, visitor.param_dict.values):
        if isinstance(key, ast.Constant) and isinstance(value, ast.Tuple):
            field_name = key.value
            path_node = value.elts[0]
            default_node = value.elts[1]

            if isinstance(path_node, ast.Constant):
                path = path_node.value
            else:
                path = field_name

            is_time = _is_time_field(field_name, default_node)

            fields.append({
                'name': field_name,
                'path': path,
                'is_time_field': is_time,
                'group': infer_field_group(field_name),
                'description': generate_field_description(field_name)
            })

    return fields


def _group_fields(fields: list[dict]) -> list[dict]:
    """Group fields by their group property."""
    groups_dict: dict[str, list] = {}
    for field in fields:
        group_name = field['group']
        if group_name not in groups_dict:
            groups_dict[group_name] = []
        groups_dict[group_name].append({
            'name': field['name'],
            'path': field['path'],
            'is_time_field': field['is_time_field'],
            'description': field['description']
        })

    return [
        {'name': name, 'fields': fields_list}
        for name, fields_list in sorted(groups_dict.items())
    ]


def get_assertion_fields_grouped() -> dict:
    """Get assertion fields grouped by category."""
    if loader._assertion_fields_cache is not None:
        return {
            'available': True,
            'groups': _group_fields(loader._assertion_fields_cache),
            'total': len(loader._assertion_fields_cache)
        }

    if loader._assertion_fields_error is not None:
        return {
            'available': False,
            'error': loader._assertion_fields_error,
            'groups': [],
            'total': 0
        }

    file_path = _get_assertions_field_path()
    if file_path is None:
        loader._assertion_fields_error = "WEBSERP_PATH not configured"
        return {
            'available': False,
            'error': loader._assertion_fields_error,
            'groups': [],
            'total': 0
        }

    if not Path(file_path).exists():
        loader._assertion_fields_error = f"File not found: {file_path}"
        return {
            'available': False,
            'error': loader._assertion_fields_error,
            'groups': [],
            'total': 0
        }

    try:
        loader._assertion_fields_cache = parse_assertions_field_py(file_path)
        return {
            'available': True,
            'groups': _group_fields(loader._assertion_fields_cache),
            'total': len(loader._assertion_fields_cache)
        }
    except Exception as e:
        loader._assertion_fields_error = f"Failed to parse fields: {e}"
        logger.error(loader._assertion_fields_error, exc_info=True)
        return {
            'available': False,
            'error': loader._assertion_fields_error,
            'groups': [],
            'total': 0
        }
