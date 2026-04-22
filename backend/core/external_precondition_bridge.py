"""Bridge module for webseleniumerp integration.

This module isolates all external project imports and provides
a clean API for operation code discovery and execution.
"""

import ast
import importlib
import sys
import logging
import inspect
import re
import asyncio
from datetime import datetime
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
_assertion_methods_cache: list[dict] | None = None

# Docstring-based method mapping state
_docstring_method_map: dict[str, dict[str, str]] | None = None
# Format: {class_name: {docstring_id: actual_method_name}}
_import_api_patched: bool = False

# LoginApi state for headers resolution
_login_api_instance = None
_login_api_error: str | None = None

# Assertion fields discovery state
_assertion_fields_cache: list[dict] | None = None
_assertion_fields_error: str | None = None


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
        else:
            _import_error = "WEBSERP_PATH not configured (optional feature)"
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
        else:
            _base_params_import_error = "WEBSERP_PATH not configured (optional feature)"
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
        else:
            _assertion_import_error = "WEBSERP_PATH not configured (optional feature)"
            return None, _assertion_import_error

    try:
        import common.base_assertions as _ba_mod
        _assertion_classes_cache = {}
        for _name in ('PcAssert', 'MgAssert', 'McAssert'):
            _cls = getattr(_ba_mod, _name, None)
            if _cls is not None:
                _assertion_classes_cache[_name] = _cls
        if not _assertion_classes_cache:
            raise ImportError("No assertion classes found in common.base_assertions")
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


# Common data option descriptions mapping
DATA_OPTION_DESCRIPTIONS = {
    'main': '主数据',
    'a': '配件数据',
    'b': '分店数据',
    'c': '仓库数据',
    'd': '其他数据',
}

# Keyword mappings for field description generation
KEYWORD_MAPPINGS: dict[str, str] = {
    'create': '创建',
    'update': '更新',
    'delete': '删除',
    'time': '时间',
    'date': '日期',
    'status': '状态',
    'str': '字符串',
    'num': '数量',
    'price': '价格',
    'amount': '金额',
    'order': '订单',
    'sale': '销售',
    'sales': '销售',
    'purchase': '采购',
    'inventory': '库存',
    'user': '用户',
    'name': '名称',
    'no': '编号',
    'id': 'ID',
    'type': '类型',
    'desc': '描述',
    'remark': '备注',
    'audit': '审核',
    'check': '检查',
    'express': '快递',
    'logistics': '物流',
    'warehouse': '仓库',
    'supplier': '供应商',
    'brand': '品牌',
    'model': '型号',
    'channel': '渠道',
    'business': '业务',
    'finish': '完成',
    'complete': '完成',
    'cancel': '取消',
    'total': '总计',
    'sum': '合计',
    'count': '计数',
    'return': '退货',
    'receive': '接收',
    'send': '发送',
    'delivery': '配送',
    'sign': '签收',
    'pay': '支付',
    'refund': '退款',
    'adjustment': '调整',
    'receipt': '收据',
    'bill': '账单',
    'account': '账户',
    'balance': '余额',
    'revenue': '收入',
    'income': '收益',
    'cost': '成本',
    'accessory': '配件',
    'quality': '质量',
    'repair': '维修',
    'batch': '批次',
    'settlement': '结算',
    'platform': '平台',
    'tenant': '租户',
    'help': '辅助',
    'shelf': '上架',
    'storage': '存储',
    'outbound': '出库',
    'inbound': '入库',
    'assign': '分配',
    'distributor': '配送员',
    'rider': '骑手',
    'consigner': '发货人',
    'operate': '操作',
    'nick': '昵称',
    'video': '视频',
    'image': '图片',
    'goods': '商品',
    'article': '物品',
    'state': '状态',
    'reason': '原因',
    'result': '结果',
    'recheck': '复核',
    'review': '审查',
    'expect': '预期',
    'guarantee': '保证',
    'final': '最终',
    'auto': '自动',
    'bid': '竞价',
    'auction': '拍卖',
    'appeal': '申诉',
    'first': '首次',
    'latest': '最新',
    'wait': '等待',
    'issue': '问题',
    'normal': '正常',
    'abnormal': '异常',
    'fineness': '成色',
    'imei': 'IMEI',
    'sku': 'SKU',
    'info': '信息',
    'detail': '详情',
    'list': '列表',
    'config': '配置',
    'timeout': '超时',
    'publish': '发布',
    'internal': '内部',
    'external': '外部',
    'qty': '数量',
}

# Field grouping rules (regex pattern -> group name)
GROUP_RULES = [
    (r'^sale', '销售相关'),
    (r'^purchase', '采购相关'),
    (r'^inventory', '库存相关'),
    (r'^order', '订单相关'),
    (r'^accessoryOrderInfo\.', '配件订单嵌套'),
    (r'^sales', '销售相关'),
    (r'Time$|time$|Date$|date$', '时间字段'),
]


def _parse_data_options_from_source(method) -> list[dict]:
    """Extract data options from method source code with descriptions.

    Parses the methods = {...} dictionary to extract available keys
    and maps them to human-readable descriptions.

    Args:
        method: The method to parse

    Returns:
        List of data option dicts: [{"value": str, "label": str}, ...]
        e.g., [{"value": "main", "label": "主数据"}, {"value": "a", "label": "配件数据"}]
    """
    try:
        source = inspect.getsource(method)
    except (OSError, TypeError):
        return [{'value': 'main', 'label': DATA_OPTION_DESCRIPTIONS.get('main', 'main')}]  # Default fallback

    # Find methods = {...} pattern
    match = re.search(r"methods\s*=\s*\{([^}]+)\}", source, re.DOTALL)
    if not match:
        return [{'value': 'main', 'label': DATA_OPTION_DESCRIPTIONS.get('main', 'main')}]

    methods_dict_str = match.group(1)

    # Extract quoted keys from the dictionary
    keys = re.findall(r"['\"](\w+)['\"]\s*:", methods_dict_str)
    if not keys:
        return [{'value': 'main', 'label': DATA_OPTION_DESCRIPTIONS.get('main', 'main')}]

    # Map keys to options with descriptions
    options = []
    for key in keys:
        options.append({
            'value': key,
            'label': DATA_OPTION_DESCRIPTIONS.get(key, key)
        })
    return options


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


# Internal methods from BaseModuleAssert/BaseAssert that should not be exposed
INTERNAL_ASSERTION_METHODS = {
    '_get_cached_api', '_call_module_api',
    'assert_time', 'assert_contains', 'assert_equal',
    '_get_field_value', '_assert_api_response'
}


def _parse_docstring_params_with_options(docstring: str) -> list[dict]:
    """Parse parameter definitions with options from docstring.

    Handles format like:
        i: 订单状态 1待发货 2待取件
        j: 物品状态 13待销售 3待分货

    Returns:
        List of parameter dicts with name, description, and options
    """
    params = []
    if not docstring:
        return params

    lines = docstring.strip().split('\n')
    for line in lines[1:]:  # Skip first line (method description)
        line = line.strip()
        if not line:
            continue

        # Match pattern: "param_name: description" or "param_name： description"
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[：:]\s*(.+)$', line)
        if match:
            param_name = match.group(1)
            param_desc = match.group(2).strip()

            # Parse options from description
            options = _parse_param_options(param_desc)

            # If options found, extract just the description part
            if options:
                # Remove option patterns from description
                clean_desc = re.sub(r'\d+[^\d]+', '', param_desc).strip()
            else:
                clean_desc = param_desc

            params.append({
                "name": param_name,
                "description": clean_desc,
                "options": options
            })

    return params


def extract_assertion_method_info(cls: type, method_name: str) -> dict | None:
    """Extract assertion method information including data options and parameters.

    Args:
        cls: The class containing the method
        method_name: Name of the method to extract info from

    Returns:
        dict with name, description, data_options, and parameters, or None for filtered methods
    """
    # Skip private methods
    if method_name.startswith('_'):
        return None

    # Skip internal utility methods from BaseModuleAssert/BaseAssert
    if method_name in INTERNAL_ASSERTION_METHODS:
        return None

    method = getattr(cls, method_name, None)
    if method is None:
        return None

    # Extract description from docstring (first line)
    docstring = method.__doc__ or ""
    description = docstring.strip().split('\n')[0] if docstring.strip() else method_name

    # Extract data options from source code
    data_options = _parse_data_options_from_source(method)

    # Parse parameters from docstring (i/j/k with options)
    parameters = _parse_docstring_params_with_options(docstring)

    return {
        "name": method_name,
        "description": description,
        "data_options": data_options,
        "parameters": parameters
    }


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
        "docstring_id": description if description != method_name else None,
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


def _build_docstring_method_map() -> dict[str, dict[str, str]]:
    """Build mapping from docstring IDs to actual method names.

    Scans all classes in common.base_params and maps the first line
    of each public method's docstring to the method name.

    Returns:
        Dict mapping class_name -> {docstring_id: method_name}
        e.g. {'PcImport': {'配件管理|配件库存|库存列表': 'CtRBRcFNn2LnUPfJF5Yhu', ...}}
    """
    global _docstring_method_map

    if _docstring_method_map is not None:
        return _docstring_method_map

    cls, error = load_base_params_class()
    if error:
        _docstring_method_map = {}
        return _docstring_method_map

    try:
        import common.base_params as base_params_module

        result: dict[str, dict[str, str]] = {}
        for class_name, obj in inspect.getmembers(base_params_module, predicate=inspect.isclass):
            if obj.__module__ != 'common.base_params':
                continue

            class_map: dict[str, str] = {}
            for method_name in dir(obj):
                if method_name.startswith('_'):
                    continue
                method = getattr(obj, method_name, None)
                if not callable(method):
                    continue

                docstring = method.__doc__ or ""
                first_line = docstring.strip().split('\n')[0] if docstring.strip() else ""
                if first_line:
                    class_map[first_line] = method_name

            if class_map:
                result[class_name] = class_map

        _docstring_method_map = result
        return _docstring_method_map
    except Exception as e:
        logger.error(f"Failed to build docstring method map: {e}", exc_info=True)
        _docstring_method_map = {}
        return _docstring_method_map


def _remap_stale_module_map_classes(ImportApi):
    """Fix _module_map entries whose class names are stale after upstream obfuscation.

    Upstream webseleniumerp periodically obfuscates all API class names.
    The _module_map still holds human-readable class names (e.g.
    'InventoryListApi') that no longer exist in their modules. This function
    remaps each entry to the actual class by sorted positional matching:
    old keys and actual classes are both sorted, then mapped 1:1.

    This is safe because the module file paths are stable across obfuscation
    passes and the number of classes per module matches the number of
    _module_map entries.
    """
    from collections import defaultdict

    entries_by_module = defaultdict(list)
    for key, (mod_path, cls_name) in list(ImportApi._module_map.items()):
        entries_by_module[mod_path].append((key, cls_name))

    updated_count = 0
    for mod_path, entries in entries_by_module.items():
        try:
            mod = importlib.import_module(mod_path)
            actual_classes = sorted([
                name for name in dir(mod)
                if not name.startswith('_')
                and isinstance(getattr(mod, name, None), type)
                and name != 'BaseApi'
            ])
        except Exception:
            continue

        entries_sorted = sorted(entries, key=lambda x: x[0])
        for i, (old_key, old_cls_name) in enumerate(entries_sorted):
            if i < len(actual_classes):
                new_cls_name = actual_classes[i]
                if new_cls_name != old_cls_name:
                    ImportApi._module_map[old_key] = (mod_path, new_cls_name)
                    updated_count += 1

    if updated_count:
        logger.info(f"Remapped {updated_count} stale _module_map class names")


def _scan_module_for_get_data_attrs(module) -> set[str]:
    """Scan a module's classes for obfuscated _get_data/_get_cached_api attributes.

    Returns the set of obfuscated api_attr names found in method source code.
    """
    attrs = set()
    for class_name, obj in inspect.getmembers(module, predicate=inspect.isclass):
        if obj.__module__ != module.__name__:
            continue
        for method_name in dir(obj):
            if method_name.startswith('_'):
                continue
            method = getattr(obj, method_name, None)
            if not callable(method):
                continue
            try:
                source = inspect.getsource(method)
            except (OSError, TypeError):
                continue

            # Match _get_data('...') and _get_cached_api('...')
            for pattern in (r"_get_data\('(\w+)'", r"_get_cached_api\('(\w+)'"):
                for match in re.finditer(pattern, source):
                    attrs.add(match.group(1))
    return attrs


def _match_attr_to_module_map(attr_name: str, ImportApi) -> bool:
    """Try to add an obfuscated attr to _module_map by matching method names.

    Handles two patterns:
    - base_params: type_map = {'main': ('METHOD', 'header'), ...}
    - base_assertions: methods = {'main': api.METHOD, ...} or api.METHOD refs

    Returns True if the attr was added to _module_map.
    """
    # Search all loaded modules for the source containing this attr
    for mod_name, mod in list(sys.modules.items()):
        if not mod_name.startswith(('common.', 'api.')):
            continue
        for class_name, obj in inspect.getmembers(mod, predicate=inspect.isclass):
            if obj.__module__ != mod.__name__:
                continue
            for method_name in dir(obj):
                if method_name.startswith('_'):
                    continue
                method = getattr(obj, method_name, None)
                if not callable(method):
                    continue
                try:
                    source = inspect.getsource(method)
                except (OSError, TypeError):
                    continue

                if f"'{attr_name}'" not in source:
                    continue

                # Pattern 1: type_map = {'key': ('METHOD', 'header'), ...}
                type_map_methods = set(re.findall(
                    r"'(\w+)',\s*'(?:main|idle|vice|special|platform|super|camera)'\)",
                    source
                ))

                # Pattern 2: api.METHOD references (assertion pattern)
                api_method_refs = set(re.findall(r'api\.(\w+)', source))

                # Combine both pattern results
                probe_methods = type_map_methods | api_method_refs
                if not probe_methods:
                    continue

                # Find matching _module_map entry
                for map_key, (mod_path, cls_name) in ImportApi._module_map.items():
                    try:
                        api_mod = importlib.import_module(mod_path)
                        api_cls = getattr(api_mod, cls_name)
                        api_methods = set(
                            m for m in dir(api_cls) if not m.startswith('_')
                        )
                        if probe_methods & api_methods:
                            ImportApi._module_map[attr_name] = (mod_path, cls_name)
                            return True
                    except Exception:
                        continue
    return False


def _patch_import_api_aliases():
    """Add obfuscated api_attr aliases to ImportApi._module_map.

    Three-phase patching:
    1. Remap stale human-readable class names to current obfuscated names
       (upstream periodically re-obfuscates all API class names).
    2. Scan base_params methods to extract obfuscated _get_data arguments,
       then match them to _module_map entries by checking if the API class
       has methods matching the type_map values.
    3. Scan base_assertions methods for _get_cached_api arguments using the
       same matching strategy.

    The type_map values are obfuscated method names unique to each API class,
    making this matching reliable once the stale class names are fixed.
    """
    global _import_api_patched
    if _import_api_patched:
        return

    cls, error = load_base_params_class()
    if error:
        return

    try:
        import common.base_params as bp_module
        from common.import_api import ImportApi

        # Phase 1: Fix stale class names in _module_map
        _remap_stale_module_map_classes(ImportApi)

        # Phase 2: Add obfuscated api_attr aliases from base_params
        for class_name, obj in inspect.getmembers(bp_module, predicate=inspect.isclass):
            if obj.__module__ != bp_module.__name__:
                continue
            for method_name in dir(obj):
                if method_name.startswith('_'):
                    continue
                method = getattr(obj, method_name, None)
                if not callable(method):
                    continue
                try:
                    source = inspect.getsource(method)
                except (OSError, TypeError):
                    continue

                # Extract _get_data first arg
                get_data_match = re.search(r"_get_data\('(\w+)'", source)
                if not get_data_match:
                    continue
                obfuscated_api_attr = get_data_match.group(1)

                # Skip if already a valid _module_map key
                if obfuscated_api_attr in ImportApi._module_map:
                    continue

                # Extract type_map method names for matching
                type_map_methods = set(re.findall(
                    r"'(\w+)',\s*'(?:main|idle|vice|special|platform|super|camera)'\)",
                    source
                ))

                # Find matching _module_map entry by checking API class methods
                for map_key, (mod_path, cls_name) in ImportApi._module_map.items():
                    try:
                        mod = importlib.import_module(mod_path)
                        api_cls = getattr(mod, cls_name)
                        api_methods = set(m for m in dir(api_cls) if not m.startswith('_'))
                        if type_map_methods & api_methods:  # intersection
                            ImportApi._module_map[obfuscated_api_attr] = (mod_path, cls_name)
                            break
                    except Exception:
                        continue

        # Phase 3: Add obfuscated api_attr aliases from base_assertions
        try:
            import common.base_assertions as ba_module
            ba_attrs = _scan_module_for_get_data_attrs(ba_module)
            for attr in ba_attrs:
                if attr not in ImportApi._module_map:
                    _match_attr_to_module_map(attr, ImportApi)
        except ImportError:
            logger.debug("base_assertions not available, skipping assertion alias patching")

        _import_api_patched = True
    except Exception as e:
        logger.error(f"Failed to patch ImportApi aliases: {e}", exc_info=True)


def get_assertion_methods_grouped() -> list[dict]:
    """Get assertion methods grouped by class name.

    Returns:
        List of class groups with their methods
    """
    global _assertion_methods_cache

    if _assertion_methods_cache is not None:
        return _assertion_methods_cache

    # Load assertion classes
    classes_dict, error = load_base_assertions_class()
    if error:
        _assertion_methods_cache = []
        return _assertion_methods_cache

    try:
        classes = []
        for name in ['PcAssert', 'MgAssert', 'McAssert']:
            if name in classes_dict:
                cls = classes_dict[name]
                # Discover methods for this class
                methods = []
                for method_name in dir(cls):
                    if not method_name.startswith('_'):
                        method_info = extract_assertion_method_info(cls, method_name)
                        if method_info is not None:
                            methods.append(method_info)

                if methods:  # Only include classes with public methods
                    classes.append({
                        "name": name,
                        "methods": methods
                    })

        _assertion_methods_cache = classes
        return _assertion_methods_cache
    except Exception as e:
        logger.error(f"Failed to scan base_assertions module: {e}", exc_info=True)
        _assertion_methods_cache = []
        return _assertion_methods_cache


def _get_login_api():
    """Get or create LoginApi instance with caching.

    Returns:
        LoginApi instance or None if unavailable
    """
    global _login_api_instance, _login_api_error

    if _login_api_instance is not None:
        return _login_api_instance

    if _login_api_error is not None:
        return None

    # Ensure path is configured
    if not _path_configured:
        from backend.config import get_settings
        settings = get_settings()
        if settings.weberp_path:
            configure_external_path(settings.weberp_path)
        else:
            _login_api_error = "WEBSERP_PATH not configured (optional feature)"
            return None

    try:
        from api.api_login import LoginApi
        _login_api_instance = LoginApi()
        logger.info("Successfully created LoginApi instance for headers resolution")
        return _login_api_instance
    except ImportError as e:
        _login_api_error = f"Failed to import LoginApi: {e}"
        logger.error(_login_api_error)
        return None
    except Exception as e:
        _login_api_error = f"Failed to create LoginApi: {e}"
        logger.error(_login_api_error, exc_info=True)
        return None


# Valid header identifiers matching LoginApi.headers keys
VALID_HEADER_IDENTIFIERS = {'main', 'idle', 'vice', 'special', 'platform', 'super', 'camera'}


def resolve_headers(identifier: str = 'main') -> dict:
    """Resolve header identifier to actual headers dict with auth tokens.

    Args:
        identifier: Header identifier string ('main', 'idle', 'vice', 'special',
                   'platform', 'super', 'camera'). Defaults to 'main'.

    Returns:
        dict: Headers dict with 'Authorization' and 'Content-Type' keys

    Raises:
        ValueError: If identifier is not a valid header identifier
        RuntimeError: If LoginApi is not available
    """
    # Default to 'main' if None
    if identifier is None:
        identifier = 'main'

    # Validate identifier
    if identifier not in VALID_HEADER_IDENTIFIERS:
        raise ValueError(
            f"Unknown header identifier: '{identifier}'. "
            f"Valid identifiers: {sorted(VALID_HEADER_IDENTIFIERS)}"
        )

    # Get LoginApi instance
    login_api = _get_login_api()
    if login_api is None:
        raise RuntimeError(
            "LoginApi not available. Ensure WEBSERP_PATH is configured and "
            "webseleniumerp project is accessible."
        )

    # Return resolved headers
    return login_api.headers.get(identifier, login_api.headers['main'])


def _parse_assertion_error(error_message: str) -> list[dict]:
    """Parse AssertionError message to extract field-level results.

    Args:
        error_message: The AssertionError message string
    Returns:
        List of field result dicts with name, expected, actual, passed
    """
    import re

    field_results = []
    # Pattern for: 字段 'fieldName' 预期值: 'expected', 实际值: 'actual'
    # or: 字段 'fieldName' 预期包含: 'expected', 实际值: 'actual'
    # More robust pattern that handles various quote styles and spacing
    pattern = r"字段\s+['\"]([^'\"]+)['\"]\s+(预期值|预期包含):\s*['\"]([^'\"]*)['\"]\s*,\s*实际值:\s*['\"]([^'\"]*)['\"]"

    for match in re.finditer(pattern, error_message):
        field_name = match.group(1)
        comparison_type = match.group(2)  # '预期值' or '预期包含'
        expected = match.group(3)
        actual = match.group(4)
        field_results.append({
            'name': field_name,
            'expected': expected,
            'actual': actual,
            'passed': False,  # If in error message, it failed
            'comparison_type': 'equals' if comparison_type == '预期值' else 'contains'
        })
    # If no fields parsed, create a single entry with the full message
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
    """Execute an assertion method with timeout protection.

    Supports three-layer parameter structure:
    - data: Data method selector ('main', 'a', 'b', etc.)
    - api_params: API filter parameters (i, j, k, etc.)
    - field_params: Field validation parameters (statusStr, createTime, etc.)

    Args:
        class_name: Name of the assertion class ('PcAssert', 'MgAssert', 'McAssert')
        method_name: Name of the assertion method (e.g., 'attachment_inventory_list_assert')
        headers: Header identifier string ('main', 'idle', 'vice', etc.)
        data: Data method selector ('main', 'a', 'b', etc.)
        api_params: API filter parameters (i, j, k, etc.)
        field_params: Field validation parameters
        params: Legacy parameter - acts as field_params fallback for backward compatibility
        timeout: Maximum execution time in seconds (default: 30.0)

    Returns:
        dict with:
            - success: bool - True if assertion passed (no AssertionError)
            - passed: bool - True if validation succeeded
            - fields: list - Field-level validation results (renamed from field_results)
            - error: str | None - Error message if execution failed
            - error_type: str | None - Error type (TimeoutError, ImportError, etc.)
            - duration: float - Execution time in seconds
    """
    import time
    start_time = time.time()

    # Backward compatibility: params acts as field_params fallback (D-06)
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
    # Load assertion classes
    classes_dict, error = load_base_assertions_class()
    if error:
        result['error'] = error
        result['error_type'] = 'ImportError'
        result['duration'] = time.time() - start_time
        return result
    # Get the target class
    if class_name not in classes_dict:
        result['error'] = f"Assertion class '{class_name}' not found. Available: {list(classes_dict.keys())}"
        result['error_type'] = 'NotFoundError'
        result['duration'] = time.time() - start_time
        return result
    # Validate headers identifier (but don't resolve - assertion method handles that)
    if headers and headers not in VALID_HEADER_IDENTIFIERS:
        result['error'] = f"Invalid headers identifier '{headers}'. Valid: {VALID_HEADER_IDENTIFIERS}"
        result['error_type'] = 'HeaderResolutionError'
        result['duration'] = time.time() - start_time
        return result
    # Create assertion instance and get method
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
    # Execute with timeout
    try:
        loop = asyncio.get_event_loop()
        # Merge api_params and field_params (D-01)
        merged_kwargs = {**(api_params or {}), **(field_params or {})}
        # Convert "now" values to datetime strings (D-02, D-03)
        call_kwargs = _convert_now_values(merged_kwargs)
        # Add headers (as identifier string, not resolved dict) and data
        # The assertion method's _process_headers will resolve the identifier
        call_kwargs['headers'] = headers
        call_kwargs['data'] = data
        # Debug logging
        logger.info(f"Calling {class_name}.{method_name} with kwargs: {list(call_kwargs.keys())}")
        # Execute in thread pool with timeout
        await asyncio.wait_for(
            loop.run_in_executor(None, lambda: method(**call_kwargs)),
            timeout=timeout
        )
        # If we get here, assertion passed
        result['success'] = True
        result['passed'] = True
        result['fields'] = []
    except asyncio.TimeoutError:
        result['error'] = f"Assertion execution timeout ({timeout}s)"
        result['error_type'] = 'TimeoutError'
    except AssertionError as e:
        # Assertion failed - parse field results from error message
        result['success'] = True  # Execution succeeded, assertion failed
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
    """Execute multiple assertions in sequence and store results in context.

    This function implements non-fail-fast behavior: all assertions execute
    regardless of individual failures, and results are collected for reporting.

    Args:
        assertions: List of assertion configs, each with:
                   - class_name: str (e.g., 'PcAssert')
                   - method_name: str (e.g., 'attachment_inventory_list_assert')
                   - headers: str (e.g., 'main')
                   - data: str (e.g., 'main')
                   - params: dict (i, j, k, etc.)
        context: ContextWrapper instance for storing results
        timeout_per_assertion: Timeout for each assertion in seconds

    Returns:
        dict with:
            - total: int - Total assertions executed
            - passed: int - Assertions that passed
            - failed: int - Assertions that failed (AssertionError)
            - errors: int - Assertions with execution errors
            - results: list - Individual assertion results
    """
    # Reset context assertion tracking for clean state
    context.reset_assertion_tracking()

    results = []

    for index, assertion_config in enumerate(assertions):
        # Support both snake_case (backend) and camelCase (frontend) field names
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
            # Catch any unexpected errors to ensure non-fail-fast
            logger.error(f"Unexpected error in assertion {index}: {e}", exc_info=True)
            result = {
                'success': False,
                'passed': False,
                'error': str(e),
                'error_type': 'UnexpectedError',
                'duration': 0.0,
                'field_results': [],
                'method': method_name,
                'class_name': class_name
            }

        # Enrich result with metadata
        result['method'] = method_name
        result['class_name'] = class_name

        # Store in context
        context.store_assertion_result(index, result)
        results.append(result)

        # Log result
        if result.get('passed'):
            logger.info(f"Assertion {index} passed")
        elif result.get('error_type'):
            logger.warning(f"Assertion {index} error: {result.get('error_type')}")
        else:
            logger.warning(f"Assertion {index} failed: {result.get('error')}")

    # Get final summary from context
    summary = context.get_assertion_results_summary()
    summary['results'] = results

    logger.info(
        f"Assertion execution complete: {summary['passed']}/{summary['total']} passed, "
        f"{summary['failed']} failed, {summary['errors']} errors"
    )

    return summary


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

        # D-02: Docstring-based fallback for stable method names
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
            # D-03: Build helpful error with available methods
            docstring_map = _build_docstring_method_map()
            class_map = docstring_map.get(class_name, {})
            available = [
                f"'{doc_id}' -> {name}"
                for doc_id, name in sorted(class_map.items())
            ]
            available_str = ', '.join(available[:20])
            return {
                "success": False,
                "error": (
                    f"Method '{method_name}' not found in class '{class_name}'. "
                    f"Available methods: {available_str}"
                ),
                "error_type": "NotFoundError"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to instantiate class: {e}",
            "error_type": "InstantiationError"
        }

    # Patch ImportApi aliases before execution (fixes _get_data internal failure)
    _patch_import_api_aliases()

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

    # Clear common.* entries from sys.modules so that stale modules from
    # webseleniumerp or test-created mocks do not persist across tests.
    # This is safe because reset_cache() invalidates all cached state, and
    # any subsequent load_* call will re-import fresh modules if needed.
    stale_modules = [k for k in sys.modules if k == "common" or k.startswith("common.")]
    for key in stale_modules:
        del sys.modules[key]

    # Also clear any api.* entries that may have been imported from
    # webseleniumerp (e.g. api.api_login used by _get_login_api).
    stale_api_modules = [k for k in sys.modules if k == "api" or k.startswith("api.")]
    for key in stale_api_modules:
        del sys.modules[key]


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

    def __init__(self):
        self.param_dict = None

    def visit_FunctionDef(self, node):
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
    for pattern, group in GROUP_RULES:
        if re.search(pattern, field_name):
            return group
    return '通用字段'


def generate_field_description(field_name: str) -> str:
    """Generate Chinese description from field name."""
    words = split_camel_case(field_name)
    translated = []
    for word in words:
        if word in KEYWORD_MAPPINGS:
            translated.append(KEYWORD_MAPPINGS[word])
        else:
            translated.append(word.capitalize())

    return ''.join(translated) if translated else field_name


def _is_time_field(field_name: str, default_node) -> bool:
    """Check if field is a time field based on name suffix or default value.

    Args:
        field_name: The field name to check
        default_node: AST node for the default value

    Returns:
        True if field is a time field
    """
    # Primary: Check AST for get_formatted_datetime call
    if isinstance(default_node, ast.Call):
        if isinstance(default_node.func, ast.Attribute):
            if default_node.func.attr == 'get_formatted_datetime':
                return True

    # Fallback: Suffix matching
    return field_name.endswith(('Time', 'time', 'Date', 'date'))


def _convert_now_values(kwargs: dict) -> dict:
    """Convert 'now' values to formatted datetime strings for time fields.

    Supported formats:
    - 'now' → current time
    - 'now-2m' → 2 minutes ago
    - 'now+5m' → 5 minutes from now
    - 'now-1h' → 1 hour ago
    - 'now+30s' → 30 seconds from now

    Args:
        kwargs: Parameter dictionary to process

    Returns:
        New dict with 'now' values converted to datetime strings (YYYY-MM-DD HH:mm:ss)
    """
    import re
    result = {}
    for key, value in kwargs.items():
        if _is_time_field(key, default_node=None) and isinstance(value, str) and value.startswith('now'):
            # Parse 'now' with optional offset: now, now-2m, now+5m, now-1h, now+30s
            match = re.match(r'^now([+-])(\d+)([smhd])?$', value)
            if match:
                # Calculate offset
                sign = 1 if match.group(1) == '+' else -1
                amount = int(match.group(2))
                unit = match.group(3) or 'm'  # default to minutes

                from datetime import timedelta
                offset = timedelta(
                    seconds=sign * amount * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
                )
                result[key] = (datetime.now() + offset).strftime('%Y-%m-%d %H:%M:%S')
            elif value == 'now':
                result[key] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                result[key] = value  # Pass through if doesn't match pattern
        else:
            result[key] = value
    return result


def parse_assertions_field_py(file_path: str) -> list[dict]:
    """Parse base_assertions_field.py and extract all fields.

    Args:
        file_path: Path to base_assertions_field.py

    Returns:
        List of field info dicts with name, path, is_time_field, group, description
    """
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

            # Extract path (first element of tuple)
            if isinstance(path_node, ast.Constant):
                path = path_node.value
            else:
                path = field_name

            # Check if time field
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
    """Get assertion fields grouped by category.

    Returns:
        dict with available, groups, and total fields
    """
    global _assertion_fields_cache, _assertion_fields_error

    if _assertion_fields_cache is not None:
        return {
            'available': True,
            'groups': _group_fields(_assertion_fields_cache),
            'total': len(_assertion_fields_cache)
        }

    if _assertion_fields_error is not None:
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }

    # Get file path
    file_path = _get_assertions_field_path()
    if file_path is None:
        _assertion_fields_error = "WEBSERP_PATH not configured"
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }

    if not Path(file_path).exists():
        _assertion_fields_error = f"File not found: {file_path}"
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }

    try:
        _assertion_fields_cache = parse_assertions_field_py(file_path)
        return {
            'available': True,
            'groups': _group_fields(_assertion_fields_cache),
            'total': len(_assertion_fields_cache)
        }
    except Exception as e:
        _assertion_fields_error = f"Failed to parse fields: {e}"
        logger.error(_assertion_fields_error, exc_info=True)
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }
