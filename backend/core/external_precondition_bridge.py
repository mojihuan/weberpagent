"""Backward-compatible re-exports — use specific sub-modules directly.

Split per D-07: loading in external_module_loader.py, discovery in
external_method_discovery.py, execution in external_execution_engine.py.
"""

from backend.core.external_module_loader import (  # noqa: F401
    configure_external_path, load_pre_front_class, is_available,
    load_base_params_class, load_base_assertions_class, reset_cache,
)
from backend.core.external_method_discovery import (  # noqa: F401
    extract_assertion_method_info, extract_method_info,
    discover_class_methods, get_data_methods_grouped,
    get_assertion_methods_grouped,
)
from backend.core.external_execution_engine import (  # noqa: F401
    execute_assertion_method, execute_all_assertions, execute_data_method,
    execute_operations, require_external_available, get_available_operations,
    get_operations_grouped, generate_precondition_code, resolve_headers,
    get_assertion_fields_grouped, parse_assertions_field_py,
)
