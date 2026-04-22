"""Unit tests for ExternalPreconditionBridge module."""

import pytest

from backend.core.external_precondition_bridge import (
    is_available,
    get_unavailable_reason,
    get_available_operations,
    get_operations_grouped,
    generate_precondition_code,
    reset_cache,
    load_base_params_class,
    extract_method_info,
    discover_class_methods,
    get_data_methods_grouped,
    _pre_front_class,
    _operations_cache,
    _modules_cache,
    _base_params_class,
    _base_params_import_error,
    _data_methods_cache,
    _build_docstring_method_map,
    _patch_import_api_aliases,
)


@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache and settings cache before and after each test."""
    from backend.config import get_settings
    reset_cache()
    get_settings.cache_clear()
    yield
    reset_cache()
    get_settings.cache_clear()


class TestExternalPreconditionBridgeBasics:
    """Basic bridge module tests."""

    def test_bridge_module_exists(self):
        """Test that bridge module can be imported."""
        import backend.core.external_precondition_bridge as bridge
        assert bridge is not None

    def test_is_available_returns_false_when_not_configured(self, monkeypatch):
        """Test is_available() returns False when PreFront cannot be loaded."""
        # Ensure WEBSERP_PATH is not configured by setting to empty string
        # Note: pydantic-settings reads from .env file, so delenv doesn't work
        from backend.config import get_settings
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        get_settings.cache_clear()  # Clear settings cache after env change
        reset_cache()  # Clear bridge cached state after env change
        result = is_available()
        assert result is False

    def test_get_unavailable_reason_returns_message(self, monkeypatch):
        """Test get_unavailable_reason() returns string when unavailable."""
        # Ensure WEBSERP_PATH is not configured by setting to empty string
        from backend.config import get_settings
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        get_settings.cache_clear()  # Clear settings cache after env change
        reset_cache()  # Clear bridge cached state after env change
        reason = get_unavailable_reason()
        assert reason is not None
        assert isinstance(reason, str)
        # Should mention import failure or configuration
        assert "Failed to import" in reason or "not configured" in reason.lower()

    def test_get_operations_grouped_returns_empty_when_unavailable(self, monkeypatch):
        """Test get_operations_grouped() returns empty list when external module not available."""
        # Ensure WEBSERP_PATH is not configured by setting to empty string
        from backend.config import get_settings
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        get_settings.cache_clear()  # Clear settings cache after env change
        reset_cache()  # Clear bridge cached state after env change
        operations = get_operations_grouped()
        assert operations == []

    def test_get_available_operations_returns_empty_when_unavailable(self, monkeypatch):
        """Test get_available_operations() returns empty dict when unavailable."""
        # Ensure WEBSERP_PATH is not configured by setting to empty string
        from backend.config import get_settings
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        get_settings.cache_clear()  # Clear settings cache after env change
        reset_cache()  # Clear bridge cached state after env change
        operations = get_available_operations()
        assert operations == {}


class TestExternalPreconditionBridgeCodeGeneration:
    """Code generation tests."""

    def test_generate_precondition_code_format(self):
        """Test generated code contains required elements."""
        codes = ['FA1', 'HC1']
        weberp_path = '/test/path'
        code = generate_precondition_code(codes, weberp_path)

        assert "sys.path.insert(0, '/test/path')" in code
        assert "from common.base_prerequisites import PreFront" in code
        assert "pre_front = PreFront()" in code
        assert "pre_front.operations(['FA1', 'HC1'])" in code
        assert "context['precondition_result'] = 'success'" in code

    def test_generate_precondition_code_single_operation(self):
        """Test generated code with single operation code."""
        codes = ['FA1']
        weberp_path = '/another/path'
        code = generate_precondition_code(codes, weberp_path)

        assert "sys.path.insert(0, '/another/path')" in code
        assert "pre_front.operations(['FA1'])" in code

    def test_generate_precondition_code_with_special_characters_in_path(self):
        """Test generated code handles paths with special characters."""
        codes = ['FA1']
        weberp_path = '/path/with spaces/and-dashes'
        code = generate_precondition_code(codes, weberp_path)

        # Path should be included as-is in the generated code
        assert weberp_path in code


class TestExternalPreconditionBridgeCache:
    """Cache management tests."""

    def test_reset_cache_clears_all_state(self):
        """Test reset_cache() clears singleton state."""
        from backend.core import external_precondition_bridge

        # Call some functions to potentially populate cache
        is_available()
        get_operations_grouped()

        # Reset cache
        reset_cache()

        # Verify state is reset
        assert external_precondition_bridge._pre_front_class is None
        assert external_precondition_bridge._import_error is None
        assert external_precondition_bridge._operations_cache is None
        assert external_precondition_bridge._modules_cache is None
        assert external_precondition_bridge._path_configured is False


class TestDataMethodsDiscovery:
    """Tests for data method discovery from base_params.py."""

    def test_load_base_params_class_caches_result(self):
        """Test load_base_params_class() caches result and returns same instance."""
        from backend.core import external_precondition_bridge

        # First call
        cls1, error1 = load_base_params_class()

        # Verify cache is set
        cached_class = external_precondition_bridge._base_params_class
        cached_error = external_precondition_bridge._base_params_import_error

        # Second call should return cached values
        cls2, error2 = load_base_params_class()

        # Either class or error should be cached
        assert cls1 == cls2
        assert error1 == error2

    def test_reset_cache_clears_base_params_state(self):
        """Test reset_cache() clears base_params related singleton state."""
        from backend.core import external_precondition_bridge

        # Trigger lazy loading
        load_base_params_class()

        # Reset cache
        reset_cache()

        # Verify base_params state is reset
        assert external_precondition_bridge._base_params_class is None
        assert external_precondition_bridge._base_params_import_error is None
        assert external_precondition_bridge._data_methods_cache is None


class TestExtractMethodInfo:
    """Tests for extract_method_info function."""

    def test_extract_method_info_skips_private_methods(self):
        """Test extract_method_info() returns None for private methods."""
        class MockClass:
            def _private_method(self):
                pass

        result = extract_method_info(MockClass, '_private_method')
        assert result is None

    def test_extract_method_info_returns_correct_structure(self):
        """Test extract_method_info() returns dict with name, description, parameters."""
        class MockClass:
            def public_method(self):
                """This is a test method."""
                pass

        result = extract_method_info(MockClass, 'public_method')

        assert result is not None
        assert result['name'] == 'public_method'
        assert 'description' in result
        assert 'parameters' in result
        assert isinstance(result['parameters'], list)

    def test_extract_method_info_extracts_parameters_with_types(self):
        """Test extract_method_info() extracts parameters with type hints."""
        class MockClass:
            def method_with_params(self, i: int, j: str, k: float):
                """Method with parameters."""
                pass

        result = extract_method_info(MockClass, 'method_with_params')

        assert result is not None
        params = result['parameters']
        assert len(params) == 3

        # Check first parameter
        assert params[0]['name'] == 'i'
        assert params[0]['type'] == 'int'
        assert params[0]['required'] is True
        assert params[0]['default'] is None

        # Check second parameter
        assert params[1]['name'] == 'j'
        assert params[1]['type'] == 'str'

    def test_extract_method_info_required_flag_no_default(self):
        """Test parameters without default are marked as required."""
        class MockClass:
            def method(self, required_param, optional_param=10):
                """Method with mixed params."""
                pass

        result = extract_method_info(MockClass, 'method')

        assert result is not None
        params = result['parameters']
        assert len(params) == 2

        # required_param has no default
        assert params[0]['name'] == 'required_param'
        assert params[0]['required'] is True
        assert params[0]['default'] is None

        # optional_param has default
        assert params[1]['name'] == 'optional_param'
        assert params[1]['required'] is False
        assert params[1]['default'] == '10'

    def test_extract_method_info_description_from_docstring(self):
        """Test description is extracted from docstring first line."""
        class MockClass:
            def documented_method(self):
                """Get inventory list data.
                This is a longer description.
                """
                pass

        result = extract_method_info(MockClass, 'documented_method')

        assert result is not None
        assert 'Get inventory list data' in result['description']

    def test_extract_method_info_description_fallback_to_name(self):
        """Test description falls back to method name when no docstring."""
        class MockClass:
            def undocumented_method(self):
                pass

        result = extract_method_info(MockClass, 'undocumented_method')

        assert result is not None
        assert result['description'] == 'undocumented_method'


class TestDiscoverClassMethods:
    """Tests for discover_class_methods function."""

    def test_discover_class_methods_returns_list_of_method_info(self):
        """Test discover_class_methods() returns list of method info dicts."""
        class MockClass:
            def method_one(self):
                """First method."""
                pass

            def method_two(self, i: int = 0):
                """Second method."""
                pass

            def _private_method(self):
                """Should be skipped."""
                pass

        result = discover_class_methods(MockClass)

        assert isinstance(result, list)
        assert len(result) == 2  # Only public methods

        # Check that both public methods are included
        method_names = [m['name'] for m in result]
        assert 'method_one' in method_names
        assert 'method_two' in method_names
        assert '_private_method' not in method_names

    def test_discover_class_methods_includes_parameters(self):
        """Test discover_class_methods() includes parameter info."""
        class MockClass:
            def method_with_params(self, i: int, j: str = "default"):
                """Method with params."""
                pass

        result = discover_class_methods(MockClass)

        assert len(result) == 1
        method_info = result[0]
        assert method_info['name'] == 'method_with_params'
        assert len(method_info['parameters']) == 2


class TestGetDataMethodsGrouped:
    """Tests for get_data_methods_grouped function."""

    def test_get_data_methods_grouped_populates_cache(self):
        """Test cache is populated after first call to get_data_methods_grouped()."""
        from backend.core import external_precondition_bridge

        # First call
        get_data_methods_grouped()

        # Verify cache is populated (even if empty due to unavailable module)
        cache = external_precondition_bridge._data_methods_cache
        assert cache is not None  # Cache is set (may be empty list)

    def test_get_data_methods_grouped_returns_cached_result(self):
        """Test subsequent calls return cached result without re-scanning."""
        from backend.core import external_precondition_bridge

        # First call populates cache
        result1 = get_data_methods_grouped()

        # Manually set cache to a different value to verify it's used
        external_precondition_bridge._data_methods_cache = [{"name": "CachedClass", "methods": []}]

        # Second call should return the manually set cache
        result2 = get_data_methods_grouped()

        assert result2 == [{"name": "CachedClass", "methods": []}]

    def test_get_data_methods_grouped_structure(self):
        """Test get_data_methods_grouped() returns correct structure when available."""
        # This test verifies the structure when module is available
        # Since module is unavailable, we verify the empty case
        result = get_data_methods_grouped()

        assert isinstance(result, list)
        # When unavailable, result is empty list
        for item in result:
            assert 'name' in item
            assert 'methods' in item
            assert isinstance(item['methods'], list)


class TestDocstringMethodMap:
    """Tests for _build_docstring_method_map()."""

    def test_builds_mapping_from_class_methods(self):
        """Docstring first line maps to method name."""
        from unittest.mock import MagicMock, patch
        from backend.core.external_precondition_bridge import _build_docstring_method_map, reset_cache

        # Create mock class with methods that have docstrings
        mock_method = MagicMock()
        mock_method.__doc__ = "库存管理|库存列表"
        mock_method.__module__ = 'common.base_params'

        MockPcImport = type('PcImport', (), {
            '__module__': 'common.base_params',
            '__doc__': None,
            'UYV6mZaVwDk4HHhyuWRRp': mock_method,
        })

        mock_module = MagicMock()
        mock_module.PcImport = MockPcImport

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(MagicMock, None)), \
             patch.dict('sys.modules', {'common.base_params': mock_module}), \
             patch('inspect.getmembers', return_value=[('PcImport', MockPcImport)]):
            result = _build_docstring_method_map()
            assert 'PcImport' in result
            assert result['PcImport']['库存管理|库存列表'] == 'UYV6mZaVwDk4HHhyuWRRp'

    def test_returns_empty_when_module_unavailable(self):
        """Returns empty dict when base_params cannot be loaded."""
        from backend.core.external_precondition_bridge import _build_docstring_method_map, reset_cache
        from unittest.mock import patch

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(None, "Module not available")):
            result = _build_docstring_method_map()
            assert result == {}

    def test_caches_result(self):
        """Second call returns cached result without re-scanning."""
        from backend.core import external_precondition_bridge
        from unittest.mock import patch, MagicMock

        # First call populates cache
        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(None, "unavailable")):
            result1 = _build_docstring_method_map()

        # Manually set cache
        external_precondition_bridge._docstring_method_map = {'TestClass': {'test_id': 'test_method'}}

        result2 = _build_docstring_method_map()
        assert result2 == {'TestClass': {'test_id': 'test_method'}}


class TestImportApiAliasPatching:
    """Tests for _patch_import_api_aliases() heuristic validation."""

    def test_patch_adds_obfuscated_aliases(self):
        """Obfuscated api_attr gets added as alias in _module_map."""
        from backend.core.external_precondition_bridge import _patch_import_api_aliases
        from unittest.mock import patch, MagicMock
        from backend.core import external_precondition_bridge

        # Create mock PcImport method with obfuscated _get_data call
        mock_method = MagicMock()
        mock_method.__module__ = 'common.base_params'
        mock_method.__doc__ = "库存管理|库存列表"

        MockPcImport = type('PcImport', (), {
            '__module__': 'common.base_params',
            '__doc__': None,
            'UYV6mZaVwDk4HHhyuWRRp': mock_method,
        })

        mock_module = MagicMock(__name__='common.base_params')
        mock_module.PcImport = MockPcImport

        # Mock API class that has matching method
        MockApiClass = type('InventoryListApi', (), {
            '__module__': 'api.api_inventory',
            'I8TzeuUVWOYr': MagicMock(),  # matches type_map value
        })

        mock_api_module = MagicMock()
        mock_api_module.InventoryListApi = MockApiClass

        mock_module_map = {
            'inventory_list': ('api.api_inventory', 'InventoryListApi'),
        }

        # Build a mock ImportApi class with the _module_map attribute
        MockImportApi = type('ImportApi', (), {
            '_module_map': mock_module_map,
            '_initialized': {},
        })

        mock_import_api_module = MagicMock(__name__='common.import_api')
        mock_import_api_module.ImportApi = MockImportApi

        # common package stub -- must expose sub-modules as attributes
        # so that 'import common.base_params' resolves to our mock
        mock_common = MagicMock()
        mock_common.base_params = mock_module
        mock_common.import_api = mock_import_api_module

        external_precondition_bridge._import_api_patched = False

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(MagicMock, None)), \
             patch.dict('sys.modules', {
                 'common': mock_common,
                 'common.base_params': mock_module,
                 'common.import_api': mock_import_api_module,
             }), \
             patch('inspect.getmembers', return_value=[('PcImport', MockPcImport)]), \
             patch('inspect.getsource', return_value="self._get_data('UYV6mZaVwDk4HHhyuWRRp', data, {'main': ('I8TzeuUVWOYr', 'main')})"), \
             patch('importlib.import_module', return_value=mock_api_module):
            _patch_import_api_aliases()
            assert 'UYV6mZaVwDk4HHhyuWRRp' in mock_module_map
            assert mock_module_map['UYV6mZaVwDk4HHhyuWRRp'] == ('api.api_inventory', 'InventoryListApi')

    def test_patch_is_idempotent(self):
        """Calling twice does not duplicate entries."""
        from unittest.mock import patch
        from backend.core.external_precondition_bridge import _patch_import_api_aliases
        from backend.core import external_precondition_bridge

        external_precondition_bridge._import_api_patched = True
        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(None, "skip")):
            _patch_import_api_aliases()
        # Should return early without touching _module_map
        assert external_precondition_bridge._import_api_patched is True

    def test_patch_skips_existing_keys(self):
        """api_attr names already in _module_map are not re-processed."""
        from backend.core.external_precondition_bridge import _patch_import_api_aliases
        from unittest.mock import patch, MagicMock
        from backend.core import external_precondition_bridge

        # api_attr that already exists as a key (snake_case, not obfuscated)
        mock_method = MagicMock()
        MockPcImport = type('PcImport', (), {
            '__module__': 'common.base_params',
            '__doc__': None,
            'existing_method': mock_method,
        })

        mock_module = MagicMock(__name__='common.base_params')
        mock_module.PcImport = MockPcImport

        mock_module_map = {
            'existing_method': ('api.api_test', 'TestApi'),
        }

        MockImportApi = type('ImportApi', (), {
            '_module_map': mock_module_map,
            '_initialized': {},
        })
        mock_import_api_module = MagicMock(__name__='common.import_api')
        mock_import_api_module.ImportApi = MockImportApi

        mock_common = MagicMock()
        mock_common.base_params = mock_module
        mock_common.import_api = mock_import_api_module

        external_precondition_bridge._import_api_patched = False

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(MagicMock, None)), \
             patch.dict('sys.modules', {
                 'common': mock_common,
                 'common.base_params': mock_module,
                 'common.import_api': mock_import_api_module,
             }), \
             patch('inspect.getmembers', return_value=[('PcImport', MockPcImport)]), \
             patch('inspect.getsource', return_value="self._get_data('existing_method', data, {'main': ('X', 'main')})"), \
             patch('importlib.import_module', return_value=MagicMock()):
            _patch_import_api_aliases()
            # Should not add a duplicate entry
            assert list(mock_module_map.keys()).count('existing_method') == 1


class TestDocstringFallback:
    """Tests for docstring-based fallback in execute_data_method()."""

    def test_docstring_id_resolves_to_method(self):
        """Docstring ID resolves to correct obfuscated method name."""
        from backend.core.external_precondition_bridge import execute_data_method
        from unittest.mock import patch, MagicMock
        import asyncio

        class MockInstance:
            """Instance where docstring ID is not an attribute but obfuscated name is."""
            def __getattr__(self, name):
                if name == '库存管理|库存列表':
                    raise AttributeError(name)
                raise AttributeError(name)

        mock_instance = MockInstance()
        mock_instance.UYV6mZaVwDk4HHhyuWRRp = MagicMock(return_value=[{"id": 1}])

        mock_class = MagicMock(return_value=mock_instance)

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(MagicMock, None)), \
             patch('inspect.getmembers', return_value=[('PcImport', mock_class)]), \
             patch('inspect.getmodule', return_value=MagicMock()), \
             patch('inspect.isclass', return_value=True), \
             patch('backend.core.external_precondition_bridge._build_docstring_method_map',
                   return_value={'PcImport': {'库存管理|库存列表': 'UYV6mZaVwDk4HHhyuWRRp'}}), \
             patch('backend.core.external_precondition_bridge._patch_import_api_aliases'):
            result = asyncio.run(execute_data_method('PcImport', '库存管理|库存列表', {}))
            assert result['success'] is True
            assert result['data'] == [{"id": 1}]

    def test_obfuscated_name_backward_compat(self):
        """Old obfuscated name still works directly."""
        from backend.core.external_precondition_bridge import execute_data_method
        from unittest.mock import patch, MagicMock
        import asyncio

        mock_instance = MagicMock()
        mock_instance.UYV6mZaVwDk4HHhyuWRRp = MagicMock(return_value=[{"id": 1}])
        mock_class = MagicMock(return_value=mock_instance)

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(MagicMock, None)), \
             patch('inspect.getmembers', return_value=[('PcImport', mock_class)]), \
             patch('inspect.getmodule', return_value=MagicMock()), \
             patch('inspect.isclass', return_value=True), \
             patch('backend.core.external_precondition_bridge._patch_import_api_aliases'):
            result = asyncio.run(execute_data_method('PcImport', 'UYV6mZaVwDk4HHhyuWRRp', {}))
            assert result['success'] is True

    def test_unknown_method_returns_available_list(self):
        """Unknown method returns error with available methods list."""
        from backend.core.external_precondition_bridge import execute_data_method
        from unittest.mock import patch, MagicMock
        import asyncio

        class MockInstance:
            """Instance where no method exists for unknown or docstring names."""
            def __getattr__(self, name):
                raise AttributeError(name)

        mock_instance = MockInstance()
        mock_class = MagicMock(return_value=mock_instance)

        with patch('backend.core.external_precondition_bridge.load_base_params_class',
                   return_value=(MagicMock, None)), \
             patch('inspect.getmembers', return_value=[('PcImport', mock_class)]), \
             patch('inspect.getmodule', return_value=MagicMock()), \
             patch('inspect.isclass', return_value=True), \
             patch('backend.core.external_precondition_bridge._build_docstring_method_map',
                   return_value={'PcImport': {'库存管理|库存列表': 'UYV6mZaVwDk4HHhyuWRRp'}}):
            result = asyncio.run(execute_data_method('PcImport', 'nonexistent_method', {}))
            assert result['success'] is False
            assert result['error_type'] == 'NotFoundError'
            assert '库存管理|库存列表' in result['error']


class TestDataMethodCacheReset:
    """Tests that new caches are properly reset."""

    def test_reset_clears_docstring_method_map(self):
        """reset_cache() clears _docstring_method_map."""
        from backend.core import external_precondition_bridge

        external_precondition_bridge._docstring_method_map = {'test': {'id': 'method'}}
        external_precondition_bridge.reset_cache()
        assert external_precondition_bridge._docstring_method_map is None

    def test_reset_clears_import_api_patched(self):
        """reset_cache() resets _import_api_patched flag."""
        from backend.core import external_precondition_bridge

        external_precondition_bridge._import_api_patched = True
        external_precondition_bridge.reset_cache()
        assert external_precondition_bridge._import_api_patched is False
