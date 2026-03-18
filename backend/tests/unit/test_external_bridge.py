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
    _pre_front_class,
    _operations_cache,
    _modules_cache,
    _base_params_class,
    _base_params_import_error,
    _data_methods_cache,
)


@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache before and after each test."""
    reset_cache()
    yield
    reset_cache()


class TestExternalPreconditionBridgeBasics:
    """Basic bridge module tests."""

    def test_bridge_module_exists(self):
        """Test that bridge module can be imported."""
        import backend.core.external_precondition_bridge as bridge
        assert bridge is not None

    def test_is_available_returns_false_when_not_configured(self):
        """Test is_available() returns False when PreFront cannot be loaded."""
        # Without WEBSERP_PATH configured, PreFront should not be loadable
        result = is_available()
        assert result is False

    def test_get_unavailable_reason_returns_message(self):
        """Test get_unavailable_reason() returns string when unavailable."""
        reason = get_unavailable_reason()
        assert reason is not None
        assert isinstance(reason, str)
        # Should mention import failure or configuration
        assert "Failed to import" in reason or "not configured" in reason.lower()

    def test_get_operations_grouped_returns_empty_when_unavailable(self):
        """Test get_operations_grouped() returns empty list when external module not available."""
        operations = get_operations_grouped()
        assert operations == []

    def test_get_available_operations_returns_empty_when_unavailable(self):
        """Test get_available_operations() returns empty dict when unavailable."""
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

    def test_operations_cached_after_first_parse(self):
        """Test that operations are cached after first parse (when available)."""
        # This test verifies caching behavior
        # Since external module is not available, cache should be set to empty
        result1 = get_operations_grouped()
        result2 = get_operations_grouped()

        # Both should return same empty result (cached)
        assert result1 == result2 == []


class TestDataMethodsDiscovery:
    """Tests for data method discovery from base_params.py."""

    def test_load_base_params_class_unavailable(self):
        """Test load_base_params_class() returns (None, error) when module unavailable."""
        cls, error = load_base_params_class()

        # Without WEBSERP_PATH configured, base_params should not be loadable
        assert cls is None
        assert error is not None
        assert isinstance(error, str)
        # Should mention import failure or configuration
        assert "Failed to import" in error or "not configured" in error.lower()

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
