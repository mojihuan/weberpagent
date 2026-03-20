"""Unit tests for ExternalAssertionBridge - assertion class discovery."""

import pytest

from backend.core.external_precondition_bridge import (
    reset_cache,
    load_base_assertions_class,
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
