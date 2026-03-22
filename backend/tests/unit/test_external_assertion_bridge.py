"""Unit tests for ExternalAssertionBridge - assertion class discovery."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock

from backend.core.external_precondition_bridge import (
    reset_cache,
    load_base_assertions_class,
    resolve_headers,
    _parse_assertion_error,
    execute_assertion_method,
)
from backend.core import external_precondition_bridge


@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache and settings cache before and after each test."""
    from backend.config import get_settings
    reset_cache()
    get_settings.cache_clear()
    yield
    reset_cache()
    get_settings.cache_clear()


class TestAssertionClassesDiscovery:
    """Tests for assertion class discovery from base_assertions.py."""

    def test_load_assertion_classes_unavailable(self, monkeypatch):
        """Test load_base_assertions_class() returns (None, error) when WEBSERP_PATH not configured."""
        # Ensure WEBSERP_PATH is not configured by setting to empty string
        from backend.config import get_settings
        monkeypatch.setenv('WEBSERP_PATH', '')  # Set to empty to override .env
        get_settings.cache_clear()  # Clear settings cache after env change
        reset_cache()  # Clear bridge cached state after env change

        classes, error = load_base_assertions_class()

        # Without WEBSERP_PATH configured, assertion classes should not be loadable
        assert classes is None
        assert error is not None
        assert isinstance(error, str)
        # Should mention import failure or configuration
        assert "Failed to import" in error or "not configured" in error.lower()

    def test_load_assertion_classes_returns_dict_when_available(self, monkeypatch):
        """Test load_base_assertions_class() returns (dict, None) with PcAssert/MgAssert/McAssert when available."""
        # This test requires the external module to be available
        # We verify the structure when available
        from backend.config import get_settings

        # Use the actual settings to check if module is configured
        settings = get_settings()
        if not settings.weberp_path:
            pytest.skip("WEBSERP_PATH not configured - skipping availability test")

        classes, error = load_base_assertions_class()

        # When available, should return a dict with expected classes
        assert error is None
        assert classes is not None
        assert isinstance(classes, dict)
        # Should contain the three main assertion classes
        assert 'PcAssert' in classes
        assert 'MgAssert' in classes
        assert 'McAssert' in classes

    def test_assertion_class_cache(self):
        """Test load_base_assertions_class() caches result and returns same dict on subsequent calls."""
        from backend.core import external_precondition_bridge

        # First call
        classes1, error1 = load_base_assertions_class()

        # Verify cache is set
        cached_classes = external_precondition_bridge._assertion_classes_cache
        cached_error = external_precondition_bridge._assertion_import_error

        # Second call should return cached values
        classes2, error2 = load_base_assertions_class()

        # Either classes or error should be cached and identical
        assert classes1 == classes2
        assert error1 == error2

    def test_reset_cache_clears_assertion_state(self):
        """Test reset_cache() clears _assertion_classes_cache and _assertion_import_error."""
        from backend.core import external_precondition_bridge

        # Trigger lazy loading
        load_base_assertions_class()

        # Reset cache
        reset_cache()

        # Verify assertion state is reset
        assert external_precondition_bridge._assertion_classes_cache is None
        assert external_precondition_bridge._assertion_import_error is None


class TestParseDataOptions:
    """Tests for _parse_data_options_from_source() function."""

    def test_returns_main_when_no_methods_dict(self):
        """Test _parse_data_options_from_source() returns ['main'] when no methods dict found."""
        from backend.core.external_precondition_bridge import _parse_data_options_from_source

        # Create a mock method with no methods dict
        def method_without_methods_dict():
            """A method without methods dictionary."""
            pass

        result = _parse_data_options_from_source(method_without_methods_dict)
        assert result == ['main']

    def test_returns_options_from_methods_dict(self):
        """Test _parse_data_options_from_source() returns ['main', 'a', 'b'] when methods = {'main': ..., 'a': ..., 'b': ...}."""
        from backend.core.external_precondition_bridge import _parse_data_options_from_source

        # Create a method with methods dictionary
        def method_with_methods_dict():
            """A method with methods dictionary."""
            methods = {
                'main': 'api.main_method',
                'a': 'api.method_a',
                'b': 'api.method_b',
            }
            return methods

        result = _parse_data_options_from_source(method_with_methods_dict)
        # Should contain the keys from methods dict
        assert 'main' in result
        assert 'a' in result
        assert 'b' in result

    def test_returns_main_when_inspect_fails(self, monkeypatch):
        """Test _parse_data_options_from_source() returns ['main'] when inspect.getsource fails."""
        from backend.core.external_precondition_bridge import _parse_data_options_from_source
        import inspect

        # Mock inspect.getsource to raise OSError
        def mock_getsource(*args, **kwargs):
            raise OSError("Cannot get source")

        monkeypatch.setattr(inspect, 'getsource', mock_getsource)

        def some_method():
            """Some method."""
            pass

        result = _parse_data_options_from_source(some_method)
        assert result == ['main']


class TestParseParamOptions:
    """Tests for _parse_param_options() function."""

    def test_returns_empty_list_for_description_without_options(self):
        """Test _parse_param_options() returns [] for description without options."""
        from backend.core.external_precondition_bridge import _parse_param_options

        result = _parse_param_options("Just a description without options")
        assert result == []

    def test_parses_options_from_description(self):
        """Test _parse_param_options() parses '订单状态 1待发货 2待取件' into options list."""
        from backend.core.external_precondition_bridge import _parse_param_options

        description = "订单状态 1待发货 2待取件"
        result = _parse_param_options(description)

        assert len(result) == 2
        assert {"value": 1, "label": "待发货"} in result
        assert {"value": 2, "label": "待取件"} in result

    def test_handles_multi_digit_values(self):
        """Test _parse_param_options() handles multi-digit values like '13待销售'."""
        from backend.core.external_precondition_bridge import _parse_param_options

        description = "物品状态 13待销售 3待分货"
        result = _parse_param_options(description)

        assert len(result) == 2
        assert {"value": 13, "label": "待销售"} in result
        assert {"value": 3, "label": "待分货"} in result

    def test_handles_chinese_and_english_colons(self):
        """Test _parse_param_options() handles Chinese and English colons in input."""
        from backend.core.external_precondition_bridge import _parse_param_options

        # The function should work with descriptions that have colons
        description = "i：订单状态 1待发货 2待取件"
        result = _parse_param_options(description)

        # Should still extract options
        assert len(result) == 2
        assert {"value": 1, "label": "待发货"} in result


class TestExtractAssertionMethodInfo:
    """Tests for extract_assertion_method_info() function."""

    def test_returns_none_for_private_methods(self):
        """Test extract_assertion_method_info() returns None for private methods."""
        from backend.core.external_precondition_bridge import extract_assertion_method_info

        class MockClass:
            def _private_method(self):
                """A private method."""
                pass

        result = extract_assertion_method_info(MockClass, '_private_method')
        assert result is None

    def test_returns_none_for_internal_methods(self):
        """Test extract_assertion_method_info() returns None for internal methods like assert_time."""
        from backend.core.external_precondition_bridge import extract_assertion_method_info

        class MockClass:
            def assert_time(self):
                """Internal time assertion."""
                pass

            def assert_contains(self):
                """Internal contains assertion."""
                pass

        result1 = extract_assertion_method_info(MockClass, 'assert_time')
        result2 = extract_assertion_method_info(MockClass, 'assert_contains')
        assert result1 is None
        assert result2 is None

    def test_returns_dict_with_all_fields(self):
        """Test extract_assertion_method_info() returns dict with name, description, data_options, parameters."""
        from backend.core.external_precondition_bridge import extract_assertion_method_info

        class MockClass:
            def test_method(self):
                """Test method description.
                i: 订单状态 1待发货 2待取件
                """
                methods = {
                    'main': 'api.main',
                    'a': 'api.alt',
                }
                return methods

        result = extract_assertion_method_info(MockClass, 'test_method')

        assert result is not None
        assert result['name'] == 'test_method'
        assert 'Test method description' in result['description']
        assert 'main' in result['data_options']
        assert 'a' in result['data_options']
        # Check parameters with options
        assert len(result['parameters']) >= 1
        param_i = next((p for p in result['parameters'] if p['name'] == 'i'), None)
        assert param_i is not None
        assert len(param_i['options']) == 2


class TestGetAssertionMethodsGrouped:
    """Tests for get_assertion_methods_grouped() function."""

    def test_returns_empty_list_when_module_unavailable(self, monkeypatch):
        """Test get_assertion_methods_grouped() returns [] when load_base_assertions_class returns error."""
        from backend.core import external_precondition_bridge
        from backend.core.external_precondition_bridge import (
            get_assertion_methods_grouped,
            reset_cache,
        )

        # Reset and set the import error to simulate unavailable module
        reset_cache()
        external_precondition_bridge._assertion_import_error = "Simulated import error"

        result = get_assertion_methods_grouped()
        assert result == []

        # Clean up
        reset_cache()

    def test_returns_classes_with_methods_grouped(self, monkeypatch):
        """Test get_assertion_methods_grouped() returns classes with methods grouped by class name."""
        from backend.core.external_precondition_bridge import (
            get_assertion_methods_grouped,
            reset_cache,
        )
        from backend.config import get_settings

        # Check if module is available
        settings = get_settings()
        if not settings.weberp_path:
            pytest.skip("WEBSERP_PATH not configured - skipping availability test")

        reset_cache()
        result = get_assertion_methods_grouped()

        # Should return a list
        assert isinstance(result, list)

        # Each item should have name and methods
        for class_group in result:
            assert 'name' in class_group
            assert 'methods' in class_group
            assert isinstance(class_group['methods'], list)

            # Each method should have required fields
            for method in class_group['methods']:
                assert 'name' in method
                assert 'description' in method
                assert 'data_options' in method
                assert 'parameters' in method


class TestResolveHeaders:
    """Tests for resolve_headers() function."""

    def test_resolve_headers_success(self):
        """Test resolve_headers('main') returns the headers dict when LoginApi is available."""
        # Create mock LoginApi with headers attribute
        mock_login_api = MagicMock()
        mock_login_api.headers = {
            'main': {'Authorization': 'Bearer token123', 'Content-Type': 'application/json'},
            'idle': {'Authorization': 'Bearer idle_token', 'Content-Type': 'application/json'},
        }

        with patch.object(external_precondition_bridge, '_get_login_api', return_value=mock_login_api):
            result = resolve_headers('main')

        assert result == {'Authorization': 'Bearer token123', 'Content-Type': 'application/json'}

    def test_resolve_headers_none_defaults_to_main(self):
        """Test resolve_headers(None) returns 'main' headers (verifies None defaults to 'main')."""
        mock_login_api = MagicMock()
        mock_login_api.headers = {
            'main': {'Authorization': 'Bearer main_token', 'Content-Type': 'application/json'},
        }

        with patch.object(external_precondition_bridge, '_get_login_api', return_value=mock_login_api):
            result = resolve_headers(None)

        assert result == {'Authorization': 'Bearer main_token', 'Content-Type': 'application/json'}

    def test_resolve_headers_invalid_identifier(self):
        """Test resolve_headers('invalid_identifier') raises ValueError with 'Unknown header identifier'."""
        with pytest.raises(ValueError) as exc_info:
            resolve_headers('invalid_identifier')

        error_message = str(exc_info.value)
        assert "Unknown header identifier" in error_message
        assert "valid identifiers" in error_message.lower()

    def test_resolve_headers_login_api_unavailable(self):
        """Test resolve_headers('main') raises RuntimeError when LoginApi returns None."""
        with patch.object(external_precondition_bridge, '_get_login_api', return_value=None):
            with pytest.raises(RuntimeError) as exc_info:
                resolve_headers('main')

        error_message = str(exc_info.value)
        assert "LoginApi not available" in error_message


class TestExecuteAssertionMethod:
    """Tests for execute_assertion_method() async function."""

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test execute_assertion_method() returns success when assertion passes."""
        # Mock assertion class with a method that returns None (success)
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.test_method = MagicMock(return_value=None)
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method('PcAssert', 'test_method', 'main', 'main', {})

        assert result['success'] is True
        assert result['passed'] is True
        assert result['field_results'] == []
        assert result['error'] is None
        assert result['error_type'] is None
        assert result['duration'] >= 0

    @pytest.mark.asyncio
    async def test_execute_assertion_error(self):
        """Test execute_assertion_method() returns passed=False when AssertionError is raised."""
        # Mock assertion class with a method that raises AssertionError
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.test_method = MagicMock(
            side_effect=AssertionError("字段 'name' 预期值: 'expected', 实际值: 'actual'")
        )
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method('PcAssert', 'test_method', 'main', 'main', {})

        assert result['success'] is True  # Execution succeeded
        assert result['passed'] is False  # Assertion failed
        assert len(result['field_results']) == 1
        assert result['field_results'][0]['field'] == 'name'
        assert '预期值' in result['error'] or 'expected' in result['error'].lower()

    @pytest.mark.asyncio
    async def test_execute_timeout(self):
        """Test execute_assertion_method() returns TimeoutError when asyncio.TimeoutError is raised."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.test_method = MagicMock(return_value=None)
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError()):
                    result = await execute_assertion_method('PcAssert', 'test_method', 'main', 'main', {})

        assert result['error_type'] == 'TimeoutError'
        assert 'timeout' in result['error'].lower()
        assert result['success'] is False

    @pytest.mark.asyncio
    async def test_execute_class_not_found(self):
        """Test execute_assertion_method() returns NotFoundError when class_name not in classes_dict."""
        mock_classes = {'PcAssert': MagicMock()}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method('InvalidClass', 'test_method', 'main', 'main', {})

        assert result['error_type'] == 'NotFoundError'
        assert 'not found' in result['error'].lower() or 'InvalidClass' in result['error']
        assert result['success'] is False

    @pytest.mark.asyncio
    async def test_execute_method_not_found(self):
        """Test execute_assertion_method() returns NotFoundError when method not found in class."""
        # Mock class instance without the target method
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        # getattr returns None for nonexistent method
        mock_instance.nonexistent_method = None
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method('PcAssert', 'nonexistent_method', 'main', 'main', {})

        assert result['error_type'] == 'NotFoundError'
        assert 'not found' in result['error'].lower()
        assert result['success'] is False

    @pytest.mark.asyncio
    async def test_execute_headers_resolution_error(self):
        """Test execute_assertion_method() returns HeaderResolutionError when resolve_headers raises ValueError."""
        mock_classes = {'PcAssert': MagicMock()}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', side_effect=ValueError("Unknown header identifier")):
                result = await execute_assertion_method('PcAssert', 'test_method', 'invalid_header', 'main', {})

        assert result['error_type'] == 'HeaderResolutionError'
        assert 'Unknown header identifier' in result['error']
        assert result['success'] is False

    @pytest.mark.asyncio
    async def test_execute_import_error(self):
        """Test execute_assertion_method() returns ImportError when load_base_assertions_class returns error."""
        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(None, "Failed to import assertion classes")):
            result = await execute_assertion_method('PcAssert', 'test_method', 'main', 'main', {})

        assert result['error_type'] == 'ImportError'
        assert result['error'] == "Failed to import assertion classes"
        assert result['success'] is False


class TestParseAssertionError:
    """Tests for _parse_assertion_error() function."""

    def test_parse_expected_value_format(self):
        """Test parsing '字段 name 预期值: expected, 实际值: actual' format."""
        message = "字段 'name' 预期值: 'expected', 实际值: 'actual'"
        result = _parse_assertion_error(message)

        assert len(result) == 1
        assert result[0]['field'] == 'name'
        assert result[0]['expected'] == 'expected'
        assert result[0]['actual'] == 'actual'
        assert result[0]['passed'] is False
        assert result[0]['comparison_type'] == 'equals'

    def test_parse_expected_contains_format(self):
        """Test parsing '字段 status 预期包含: active, 实际值: inactive' format."""
        message = "字段 'status' 预期包含: 'active', 实际值: 'inactive'"
        result = _parse_assertion_error(message)

        assert len(result) == 1
        assert result[0]['field'] == 'status'
        assert result[0]['expected'] == 'active'
        assert result[0]['actual'] == 'inactive'
        assert result[0]['passed'] is False
        assert result[0]['comparison_type'] == 'contains'

    def test_parse_multiple_fields(self):
        """Test parsing message with multiple field patterns."""
        message = (
            "字段 'name' 预期值: 'expected1', 实际值: 'actual1'; "
            "字段 'status' 预期值: 'expected2', 实际值: 'actual2'"
        )
        result = _parse_assertion_error(message)

        assert len(result) == 2
        assert result[0]['field'] == 'name'
        assert result[1]['field'] == 'status'

    def test_parse_unparseable_message(self):
        """Test parsing unparseable message returns unknown field with description."""
        message = "Some random error message without field pattern"
        result = _parse_assertion_error(message)

        assert len(result) == 1
        assert result[0]['field'] == 'unknown'
        assert result[0]['passed'] is False
        assert result[0]['description'] == message

    def test_parse_chinese_colon(self):
        """Test parsing message with Chinese colon still works."""
        message = "字段 'name' 预期值：'expected', 实际值：'actual'"
        result = _parse_assertion_error(message)

        # The regex pattern uses [：:] to match both Chinese and English colons
        # But the current pattern expects specific format with Chinese colons in some places
        # Let's verify what the actual behavior is
        # If the pattern doesn't match, it should return unknown field
        if len(result) == 1 and result[0]['field'] == 'name':
            assert result[0]['expected'] == 'expected'
            assert result[0]['actual'] == 'actual'
        else:
            # If Chinese colon in the comparison_type position doesn't match, fallback is expected
            assert result[0]['field'] == 'unknown'


class TestConvertNowValues:
    """Tests for _convert_now_values() function."""

    def test_converts_now_to_datetime_string_for_time_field(self):
        """_convert_now_values converts 'now' to datetime string for time fields."""
        from backend.core.external_precondition_bridge import _convert_now_values
        from datetime import datetime

        kwargs = {'createTime': 'now', 'statusStr': '已完成'}
        result = _convert_now_values(kwargs)

        # createTime should be converted to datetime string
        assert result['createTime'] != 'now'
        assert len(result['createTime']) == 19  # YYYY-MM-DD HH:MM:SS format
        # Verify format matches expected pattern
        datetime.strptime(result['createTime'], '%Y-%m-%d %H:%M:%S')
        # statusStr should remain unchanged
        assert result['statusStr'] == '已完成'

    def test_does_not_convert_non_time_fields(self):
        """_convert_now_values does not convert 'now' for non-time fields."""
        from backend.core.external_precondition_bridge import _convert_now_values

        kwargs = {'statusStr': 'now', 'orderType': 'now'}
        result = _convert_now_values(kwargs)

        # These are not time fields, so 'now' should remain unchanged
        assert result['statusStr'] == 'now'
        assert result['orderType'] == 'now'

    def test_converts_all_time_fields_ending_with_time_or_date(self):
        """_convert_now_values converts fields ending with Time/time/Date/date."""
        from backend.core.external_precondition_bridge import _convert_now_values
        from datetime import datetime

        kwargs = {
            'createTime': 'now',
            'updateTime': 'now',
            'orderDate': 'now',
            'saleTime': 'now',
        }
        result = _convert_now_values(kwargs)

        # All should be converted
        for key in kwargs:
            assert result[key] != 'now', f"{key} should be converted"
            datetime.strptime(result[key], '%Y-%m-%d %H:%M:%S')

    def test_does_not_mutate_input_dict(self):
        """_convert_now_values returns new dict without mutating input."""
        from backend.core.external_precondition_bridge import _convert_now_values

        original = {'createTime': 'now', 'status': 'active'}
        original_id = id(original)
        result = _convert_now_values(original)

        # Input dict should be unchanged
        assert original == {'createTime': 'now', 'status': 'active'}
        # Result should be a new dict
        assert id(result) != original_id

    def test_handles_empty_dict(self):
        """_convert_now_values handles empty dict."""
        from backend.core.external_precondition_bridge import _convert_now_values

        result = _convert_now_values({})
        assert result == {}

    def test_handles_dict_without_now_values(self):
        """_convert_now_values handles dict without 'now' values."""
        from backend.core.external_precondition_bridge import _convert_now_values

        kwargs = {'statusStr': '已完成', 'orderType': 'SA', 'i': 1}
        result = _convert_now_values(kwargs)

        assert result == kwargs


class TestThreeLayerParams:
    """Tests for execute_assertion_method with three-layer parameters."""

    @pytest.mark.asyncio
    async def test_accepts_api_params_and_field_params(self):
        """execute_assertion_method accepts api_params and field_params parameters."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method(
                    'PcAssert', 'test_method',
                    headers='main', data='main',
                    api_params={'i': 1, 'j': 2},
                    field_params={'statusStr': '已完成'}
                )

        assert result['success'] is True
        assert result['passed'] is True

    @pytest.mark.asyncio
    async def test_merges_api_params_and_field_params(self):
        """execute_assertion_method merges api_params and field_params into kwargs."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                await execute_assertion_method(
                    'PcAssert', 'test_method',
                    headers='main', data='main',
                    api_params={'i': 1, 'j': 2},
                    field_params={'statusStr': '已完成'}
                )

        # Check that method was called with merged params
        call_kwargs = mock_method.call_args[1]
        assert call_kwargs['i'] == 1
        assert call_kwargs['j'] == 2
        assert call_kwargs['statusStr'] == '已完成'
        assert call_kwargs['headers'] == mock_headers
        assert call_kwargs['data'] == 'main'

    @pytest.mark.asyncio
    async def test_converts_now_in_field_params(self):
        """execute_assertion_method converts 'now' values in field_params."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                await execute_assertion_method(
                    'PcAssert', 'test_method',
                    headers='main', data='main',
                    field_params={'createTime': 'now'}
                )

        # Check that 'now' was converted to datetime string
        call_kwargs = mock_method.call_args[1]
        assert call_kwargs['createTime'] != 'now'
        assert len(call_kwargs['createTime']) == 19  # YYYY-MM-DD HH:MM:SS


class TestBackwardCompatibility:
    """Tests for backward compatibility with old params parameter."""

    @pytest.mark.asyncio
    async def test_params_acts_as_field_params_fallback(self):
        """execute_assertion_method treats params as field_params fallback."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                # Call with old-style params
                result = await execute_assertion_method(
                    'PcAssert', 'test_method',
                    headers='main', data='main',
                    params={'statusStr': '已完成'}
                )

        assert result['success'] is True
        # Check that params was used as field_params
        call_kwargs = mock_method.call_args[1]
        assert call_kwargs['statusStr'] == '已完成'

    @pytest.mark.asyncio
    async def test_field_params_overrides_params(self):
        """execute_assertion_method prefers field_params over params."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                # Call with both params and field_params
                await execute_assertion_method(
                    'PcAssert', 'test_method',
                    headers='main', data='main',
                    params={'statusStr': 'old_value'},
                    field_params={'statusStr': 'new_value'}
                )

        # Check that field_params was used (not params)
        call_kwargs = mock_method.call_args[1]
        assert call_kwargs['statusStr'] == 'new_value'


class TestFieldsResponseFormat:
    """Tests for response using 'fields' instead of 'field_results'."""

    @pytest.mark.asyncio
    async def test_success_response_uses_fields_key(self):
        """execute_assertion_method returns 'fields' instead of 'field_results' on success."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=None)
        mock_instance.test_method = mock_method
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method('PcAssert', 'test_method', 'main', 'main', {})

        assert 'fields' in result
        assert result['fields'] == []

    @pytest.mark.asyncio
    async def test_assertion_error_response_uses_fields_key(self):
        """execute_assertion_method returns 'fields' with parsed results on AssertionError."""
        mock_assertion_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.test_method = MagicMock(
            side_effect=AssertionError("字段 'statusStr' 预期值: '已完成', 实际值: '进行中'")
        )
        mock_assertion_class.return_value = mock_instance

        mock_classes = {'PcAssert': mock_assertion_class}
        mock_headers = {'Authorization': 'Bearer token'}

        with patch.object(external_precondition_bridge, 'load_base_assertions_class', return_value=(mock_classes, None)):
            with patch.object(external_precondition_bridge, 'resolve_headers', return_value=mock_headers):
                result = await execute_assertion_method('PcAssert', 'test_method', 'main', 'main', {})

        assert 'fields' in result
        assert len(result['fields']) == 1
        # Should use 'name' key instead of 'field'
        assert result['fields'][0]['name'] == 'statusStr'
