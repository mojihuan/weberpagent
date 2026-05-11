"""External method discovery and reflection.

Split from external_precondition_bridge.py per D-07.
Handles method discovery, docstring parsing, and class scanning for
external webseleniumerp integration.
"""

import ast
import importlib
import inspect
import json
import re
import logging
from pathlib import Path
from typing import Any

import backend.core.external_module_loader as loader

logger = logging.getLogger(__name__)


def _parse_docstring_params(docstring: str) -> list[dict]:
    """Parse parameter definitions from docstring."""
    params = []
    if not docstring:
        return params

    lines = docstring.strip().split('\n')
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[：:]\s*(.+)$', line)
        if match:
            param_name = match.group(1)
            param_desc = match.group(2).strip()
            params.append({
                "name": param_name,
                "type": "int",
                "required": False,
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
    'create': '创建', 'update': '更新', 'delete': '删除',
    'time': '时间', 'date': '日期', 'status': '状态',
    'str': '字符串', 'num': '数量', 'price': '价格',
    'amount': '金额', 'order': '订单', 'sale': '销售',
    'sales': '销售', 'purchase': '采购', 'inventory': '库存',
    'user': '用户', 'name': '名称', 'no': '编号',
    'id': 'ID', 'type': '类型', 'desc': '描述',
    'remark': '备注', 'audit': '审核', 'check': '检查',
    'express': '快递', 'logistics': '物流', 'warehouse': '仓库',
    'supplier': '供应商', 'brand': '品牌', 'model': '型号',
    'channel': '渠道', 'business': '业务', 'finish': '完成',
    'complete': '完成', 'cancel': '取消', 'total': '总计',
    'sum': '合计', 'count': '计数', 'return': '退货',
    'receive': '接收', 'send': '发送', 'delivery': '配送',
    'sign': '签收', 'pay': '支付', 'refund': '退款',
    'adjustment': '调整', 'receipt': '收据', 'bill': '账单',
    'account': '账户', 'balance': '余额', 'revenue': '收入',
    'income': '收益', 'cost': '成本', 'accessory': '配件',
    'quality': '质量', 'repair': '维修', 'batch': '批次',
    'settlement': '结算', 'platform': '平台', 'tenant': '租户',
    'help': '辅助', 'shelf': '上架', 'storage': '存储',
    'outbound': '出库', 'inbound': '入库', 'assign': '分配',
    'distributor': '配送员', 'rider': '骑手', 'consigner': '发货人',
    'operate': '操作', 'nick': '昵称', 'video': '视频',
    'image': '图片', 'goods': '商品', 'article': '物品',
    'state': '状态', 'reason': '原因', 'result': '结果',
    'recheck': '复核', 'review': '审查', 'expect': '预期',
    'guarantee': '保证', 'final': '最终', 'auto': '自动',
    'bid': '竞价', 'auction': '拍卖', 'appeal': '申诉',
    'first': '首次', 'latest': '最新', 'wait': '等待',
    'issue': '问题', 'normal': '正常', 'abnormal': '异常',
    'fineness': '成色', 'imei': 'IMEI', 'sku': 'SKU',
    'info': '信息', 'detail': '详情', 'list': '列表',
    'config': '配置', 'timeout': '超时', 'publish': '发布',
    'internal': '内部', 'external': '外部', 'qty': '数量',
}

# Field grouping rules
GROUP_RULES = [
    (r'^sale', '销售相关'),
    (r'^purchase', '采购相关'),
    (r'^inventory', '库存相关'),
    (r'^order', '订单相关'),
    (r'^accessoryOrderInfo\.', '配件订单嵌套'),
    (r'^sales', '销售相关'),
    (r'Time$|time$|Date$|date$', '时间字段'),
]


def _parse_data_options_from_source(method: Any) -> list[dict]:
    """Extract data options from method source code with descriptions."""
    try:
        source = inspect.getsource(method)
    except (OSError, TypeError):
        return [{'value': 'main', 'label': DATA_OPTION_DESCRIPTIONS.get('main', 'main')}]

    match = re.search(r"methods\s*=\s*\{([^}]+)\}", source, re.DOTALL)
    if not match:
        return [{'value': 'main', 'label': DATA_OPTION_DESCRIPTIONS.get('main', 'main')}]

    methods_dict_str = match.group(1)
    keys = re.findall(r"['\"](\w+)['\"]\s*:", methods_dict_str)
    if not keys:
        return [{'value': 'main', 'label': DATA_OPTION_DESCRIPTIONS.get('main', 'main')}]

    options = []
    for key in keys:
        options.append({
            'value': key,
            'label': DATA_OPTION_DESCRIPTIONS.get(key, key)
        })
    return options


def _parse_param_options(description: str) -> list[dict]:
    """Parse option values from parameter description."""
    options = []
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
    """Parse parameter definitions with options from docstring."""
    params = []
    if not docstring:
        return params

    lines = docstring.strip().split('\n')
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[：:]\s*(.+)$', line)
        if match:
            param_name = match.group(1)
            param_desc = match.group(2).strip()

            options = _parse_param_options(param_desc)

            if options:
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
    """Extract assertion method information including data options and parameters."""
    if method_name.startswith('_'):
        return None

    if method_name in INTERNAL_ASSERTION_METHODS:
        return None

    method = getattr(cls, method_name, None)
    if method is None:
        return None

    docstring = method.__doc__ or ""
    description = docstring.strip().split('\n')[0] if docstring.strip() else method_name

    data_options = _parse_data_options_from_source(method)
    parameters = _parse_docstring_params_with_options(docstring)

    return {
        "name": method_name,
        "description": description,
        "data_options": data_options,
        "parameters": parameters
    }


def extract_method_info(cls: type, method_name: str) -> dict | None:
    """Extract method information including parameters with types."""
    from typing import get_type_hints

    if method_name.startswith('_'):
        return None

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

    docstring = method.__doc__ or ""
    description = docstring.strip().split('\n')[0] if docstring.strip() else method_name

    parameters = []
    existing_param_names = set()

    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        existing_param_names.add(param_name)

        param_type = type_hints.get(param_name, Any)
        type_str = getattr(param_type, '__name__', str(param_type))
        if type_str.startswith('typing.'):
            type_str = str(param_type).replace('typing.', '')

        has_default = param.default != inspect.Parameter.empty
        parameters.append({
            "name": param_name,
            "type": type_str,
            "required": not has_default,
            "default": repr(param.default) if has_default else None
        })

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
    """Discover all public methods in a class."""
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_'):
            method_info = extract_method_info(cls, name)
            if method_info is not None:
                methods.append(method_info)
    return methods


def get_data_methods_grouped() -> list[dict]:
    """Get data methods grouped by class name."""
    if loader._data_methods_cache is not None:
        return loader._data_methods_cache

    cls, error = loader.load_base_params_class()
    if error:
        loader._data_methods_cache = []
        return loader._data_methods_cache

    try:
        import common.base_params as base_params_module

        classes = []
        for name, obj in inspect.getmembers(base_params_module, predicate=inspect.isclass):
            if obj.__module__ != 'common.base_params':
                continue

            methods = discover_class_methods(obj)
            if methods:
                classes.append({
                    "name": name,
                    "methods": methods
                })

        loader._data_methods_cache = classes
        return loader._data_methods_cache
    except Exception as e:
        logger.error(f"Failed to scan base_params module: {e}", exc_info=True)
        loader._data_methods_cache = []
        return loader._data_methods_cache


def _build_docstring_method_map() -> dict[str, dict[str, str]]:
    """Build mapping from docstring IDs to actual method names."""
    if loader._docstring_method_map is not None:
        return loader._docstring_method_map

    cls, error = loader.load_base_params_class()
    if error:
        loader._docstring_method_map = {}
        return loader._docstring_method_map

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

        loader._docstring_method_map = result
        return loader._docstring_method_map
    except Exception as e:
        logger.error(f"Failed to build docstring method map: {e}", exc_info=True)
        loader._docstring_method_map = {}
        return loader._docstring_method_map


def _remap_stale_module_map_classes(ImportApi: Any) -> None:
    """Fix _module_map entries whose class names are stale after upstream obfuscation."""
    from collections import defaultdict

    entries_by_module = defaultdict(list)
    for key, value in list(ImportApi._module_map.items()):
        if isinstance(value, tuple):
            mod_path, cls_name = value
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


def _scan_module_for_get_data_attrs(module: Any) -> set[str]:
    """Scan a module's classes for obfuscated _get_data/_get_cached_api attributes."""
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

            for pattern in (r"_get_data\('(\w+)'", r"_get_cached_api\('(\w+)'"):
                for match in re.finditer(pattern, source):
                    attrs.add(match.group(1))
    return attrs


def _find_module_map_match(
    attr_name: str, source: str, ImportApi: Any,
) -> tuple[str, str] | None:
    """Try to find a matching _module_map entry for attr_name.

    Returns (mod_path, cls_name) if a match is found, None otherwise.
    """
    type_map_methods = set(re.findall(
        r"'(\w+)',\s*'(?:main|idle|vice|special|platform|super|camera)'\)",
        source
    ))
    api_method_refs = set(re.findall(r'api\.(\w+)', source))
    probe_methods = type_map_methods | api_method_refs
    if not probe_methods:
        return None

    for map_key, (mod_path, cls_name) in ImportApi._module_map.items():
        try:
            api_mod = importlib.import_module(mod_path)
            api_cls = getattr(api_mod, cls_name)
            api_methods = set(m for m in dir(api_cls) if not m.startswith('_'))
            if probe_methods & api_methods:
                return mod_path, cls_name
        except Exception:
            continue
    return None


def _scan_class_method_for_attr(
    attr_name: str, obj: type, ImportApi: Any,
) -> tuple[str, str] | None:
    """Scan a class for a method containing attr_name and resolve via _module_map."""
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
        return _find_module_map_match(attr_name, source, ImportApi)
    return None


def _match_attr_to_module_map(attr_name: str, ImportApi: Any) -> bool:
    """Try to add an obfuscated attr to _module_map by matching method names."""
    import sys as _sys

    for mod_name, mod in list(_sys.modules.items()):
        if not mod_name.startswith(('common.', 'api.')):
            continue
        for class_name, obj in inspect.getmembers(mod, predicate=inspect.isclass):
            if obj.__module__ != mod.__name__:
                continue
            match = _scan_class_method_for_attr(attr_name, obj, ImportApi)
            if match:
                mod_path, cls_name = match
                ImportApi._module_map[attr_name] = (mod_path, cls_name)
                return True
    return False


def _try_patch_alias_for_method(
    method_name: str, method: Any, ImportApi: Any,
) -> None:
    """Try to patch ImportApi._module_map with an obfuscated alias for a method."""
    try:
        source = inspect.getsource(method)
    except (OSError, TypeError):
        return

    get_data_match = re.search(r"_get_data\('(\w+)'", source)
    if not get_data_match:
        return
    obfuscated_api_attr = get_data_match.group(1)
    if obfuscated_api_attr in ImportApi._module_map:
        return

    type_map_methods = set(re.findall(
        r"'(\w+)',\s*'(?:main|idle|vice|special|platform|super|camera)'\)",
        source
    ))

    for map_key, (mod_path, cls_name) in ImportApi._module_map.items():
        try:
            mod = importlib.import_module(mod_path)
            api_cls = getattr(mod, cls_name)
            api_methods = set(m for m in dir(api_cls) if not m.startswith('_'))
            if type_map_methods & api_methods:
                ImportApi._module_map[obfuscated_api_attr] = (mod_path, cls_name)
                break
        except Exception:
            continue


_CACHE_VERSION = 1


def _cache_file_path() -> Path | None:
    """Return path to .module_map_cache.json next to weberp_path."""
    from backend.config import get_settings
    weberp_path = get_settings().weberp_path
    if not weberp_path:
        return None
    return Path(weberp_path) / ".module_map_cache.json"


def _load_cached_module_map() -> dict[str, tuple[str, str]] | None:
    """Load cached _module_map from JSON file. Returns None if cache missing/invalid."""
    cache_path = _cache_file_path()
    if cache_path is None or not cache_path.exists():
        return None
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        if data.get("version") != _CACHE_VERSION:
            return None
        entries = data.get("entries", {})
        return {k: tuple(v) for k, v in entries.items()}
    except Exception as e:
        logger.debug(f"Failed to load module_map cache: {e}")
        return None


def _save_cached_module_map(module_map: dict) -> None:
    """Save _module_map to JSON cache file."""
    cache_path = _cache_file_path()
    if cache_path is None:
        return
    try:
        entries = {}
        for k, v in module_map.items():
            if isinstance(v, tuple):
                entries[k] = list(v)
            elif isinstance(v, type):
                entries[k] = [v.__module__, v.__name__]
        data = {"version": _CACHE_VERSION, "entries": entries}
        cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        logger.info(f"Saved module_map cache ({len(entries)} entries) to {cache_path}")
    except Exception as e:
        logger.warning(f"Failed to save module_map cache: {e}")


def _patch_import_api_aliases() -> None:
    """Add obfuscated api_attr aliases to ImportApi._module_map.

    Three-phase patching:
    1. Remap stale human-readable class names
    2. Scan base_params methods for obfuscated _get_data arguments
    3. Scan base_assertions methods for _get_cached_api arguments
    """
    if loader._import_api_patched:
        return

    cls, error = loader.load_base_params_class()
    if error:
        return

    try:
        import common.base_params as bp_module
        from common.import_api import ImportApi

        # 尝试从缓存加载（跳过耗时的源码扫描）
        cached = _load_cached_module_map()
        if cached is not None:
            ImportApi._module_map.update(cached)
            logger.info(f"Loaded module_map cache ({len(cached)} entries)")
            loader._import_api_patched = True
            return

        # 缓存未命中：执行完整扫描
        _remap_stale_module_map_classes(ImportApi)

        for class_name, obj in inspect.getmembers(bp_module, predicate=inspect.isclass):
            if obj.__module__ != bp_module.__name__:
                continue
            for method_name in dir(obj):
                if method_name.startswith('_'):
                    continue
                method = getattr(obj, method_name, None)
                if not callable(method):
                    continue
                _try_patch_alias_for_method(method_name, method, ImportApi)

        try:
            import common.base_assertions as ba_module
            ba_attrs = _scan_module_for_get_data_attrs(ba_module)
            for attr in ba_attrs:
                if attr not in ImportApi._module_map:
                    _match_attr_to_module_map(attr, ImportApi)
        except ImportError:
            logger.debug("base_assertions not available, skipping assertion alias patching")

        # 扫描完成，保存缓存
        _save_cached_module_map(ImportApi._module_map)
        loader._import_api_patched = True
    except Exception as e:
        logger.error(f"Failed to patch ImportApi aliases: {e}", exc_info=True)


def _scan_class_for_attr_match(cls: type) -> list[dict]:
    """Scan a class for public assertion methods."""
    methods = []
    for method_name in dir(cls):
        if method_name.startswith('_'):
            continue
        method_info = extract_assertion_method_info(cls, method_name)
        if method_info is not None:
            methods.append(method_info)
    return methods


def get_assertion_methods_grouped() -> list[dict]:
    """Get assertion methods grouped by class name."""
    if loader._assertion_methods_cache is not None:
        return loader._assertion_methods_cache

    classes_dict, error = loader.load_base_assertions_class()
    if error:
        loader._assertion_methods_cache = []
        return loader._assertion_methods_cache

    try:
        classes = []
        for name in ['PcAssert', 'MgAssert', 'McAssert']:
            if name not in classes_dict:
                continue
            methods = _scan_class_for_attr_match(classes_dict[name])
            if methods:
                classes.append({
                    "name": name,
                    "methods": methods
                })

        loader._assertion_methods_cache = classes
        return loader._assertion_methods_cache
    except Exception as e:
        logger.error(f"Failed to scan base_assertions module: {e}", exc_info=True)
        loader._assertion_methods_cache = []
        return loader._assertion_methods_cache
