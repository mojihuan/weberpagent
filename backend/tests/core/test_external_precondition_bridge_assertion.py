"""Tests for assertion execution functions in external_precondition_bridge."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from backend.core.external_precondition_bridge import (
    resolve_headers,
    VALID_HEADER_IDENTIFIERS,
    execute_assertion_method,
    _parse_assertion_error,
)


class TestResolveHeaders:
    """Tests for resolve_headers() function."""

    def test_resolve_headers_main_returns_dict_with_authorization(self):
        """resolve_headers('main') returns dict with Authorization key."""
        with patch('backend.core.external_precondition_bridge._get_login_api') as mock_get_api:
            mock_api = MagicMock()
            mock_api.headers = {
                'main': {'Authorization': 'Bearer token123', 'Content-Type': 'application/json'},
                'idle': {},
            }
            mock_get_api.return_value = mock_api

            result = resolve_headers('main')

            assert 'Authorization' in result
            assert result['Authorization'] == 'Bearer token123'

    def test_resolve_headers_invalid_identifier_raises_valueerror(self):
        """resolve_headers with invalid identifier raises ValueError."""
        with patch('backend.core.external_precondition_bridge._get_login_api') as mock_get_api:
            mock_api = MagicMock()
            mock_api.headers = {'main': {}}
            mock_get_api.return_value = mock_api

            with pytest.raises(ValueError) as exc_info:
                resolve_headers('invalid_identifier')

            assert "Unknown header identifier" in str(exc_info.value)
            assert "invalid_identifier" in str(exc_info.value)

    def test_resolve_headers_none_returns_default_main(self):
        """resolve_headers(None) returns 'main' headers as default."""
        with patch('backend.core.external_precondition_bridge._get_login_api') as mock_get_api:
            mock_api = MagicMock()
            mock_api.headers = {
                'main': {'Authorization': 'Bearer main_token'},
                'idle': {'Authorization': 'Bearer idle_token'},
            }
            mock_get_api.return_value = mock_api

            result = resolve_headers(None)

            assert result['Authorization'] == 'Bearer main_token'

    def test_resolve_headers_login_api_unavailable_raises_runtimeerror(self):
        """resolve_headers raises RuntimeError when LoginApi is not available."""
        with patch('backend.core.external_precondition_bridge._get_login_api') as mock_get_api:
            mock_get_api.return_value = None

            with pytest.raises(RuntimeError) as exc_info:
                resolve_headers('main')

            assert "LoginApi not available" in str(exc_info.value)

    def test_resolve_headers_all_valid_identifiers(self):
        """resolve_headers works for all valid identifiers."""
        with patch('backend.core.external_precondition_bridge._get_login_api') as mock_get_api:
            mock_api = MagicMock()
            mock_api.headers = {
                identifier: {'Authorization': f'Bearer {identifier}_token'}
                for identifier in VALID_HEADER_IDENTIFIERS
            }
            mock_get_api.return_value = mock_api

            for identifier in VALID_HEADER_IDENTIFIERS:
                result = resolve_headers(identifier)
                assert f'{identifier}_token' in result['Authorization']


class TestExecuteAssertionMethod:
    """Tests for execute_assertion_method() function."""

    @pytest.mark.asyncio
    async def test_returns_success_when_assertion_passes(self):
        """execute_assertion_method returns success=True when assertion passes."""
        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            with patch('backend.core.external_precondition_bridge.resolve_headers') as mock_resolve:
                mock_load.return_value = ({'PcAssert': MagicMock}, None)
                mock_resolve.return_value = {'Authorization': 'Bearer token'}

                with patch('backend.core.external_precondition_bridge.asyncio.get_event_loop') as mock_loop:
                    mock_loop.return_value.run_in_executor = MagicMock(return_value=asyncio.Future())
                    mock_loop.return_value.run_in_executor.return_value.set_result(None)

                    # Use wait_for mock that doesn't timeout
                    with patch('backend.core.external_precondition_bridge.asyncio.wait_for') as mock_wait:
                        mock_wait.return_value = None

                        result = await execute_assertion_method('PcAssert', 'test_assert')

                        assert result['success'] is True
                        assert result['passed'] is True

    @pytest.mark.asyncio
    async def test_catches_assertion_error_and_returns_field_results(self):
        """execute_assertion_method catches AssertionError and extracts field results."""
        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            with patch('backend.core.external_precondition_bridge.resolve_headers') as mock_resolve:
                mock_load.return_value = ({'PcAssert': MagicMock}, None)
                mock_resolve.return_value = {'Authorization': 'Bearer token'}

                # Create assertion method that raises AssertionError
                async def raise_assertion_error(*args, **kwargs):
                    raise AssertionError("字段 'status' 预期值: '已发货', 实际值: '待发货'")

                with patch('backend.core.external_precondition_bridge.asyncio.wait_for', side_effect=raise_assertion_error):
                    result = await execute_assertion_method('PcAssert', 'test_assert')

                    assert result['success'] is True  # Execution succeeded
                    assert result['passed'] is False  # Assertion failed
                    assert len(result['field_results']) > 0

    @pytest.mark.asyncio
    async def test_returns_timeout_error_when_exceeds_timeout(self):
        """execute_assertion_method returns TimeoutError when execution exceeds timeout."""
        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            with patch('backend.core.external_precondition_bridge.resolve_headers') as mock_resolve:
                mock_load.return_value = ({'PcAssert': MagicMock}, None)
                mock_resolve.return_value = {'Authorization': 'Bearer token'}

                with patch('backend.core.external_precondition_bridge.asyncio.wait_for') as mock_wait:
                    mock_wait.side_effect = asyncio.TimeoutError()

                    result = await execute_assertion_method('PcAssert', 'test_assert', timeout=1.0)

                    assert result['success'] is False
                    assert result['error_type'] == 'TimeoutError'
                    assert 'timeout' in result['error'].lower()

    @pytest.mark.asyncio
    async def test_returns_import_error_when_class_not_found(self):
        """execute_assertion_method returns ImportError when assertion class not found."""
        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            mock_load.return_value = (None, "Failed to import assertion classes")

            result = await execute_assertion_method('PcAssert', 'test_assert')

            assert result['success'] is False
            assert result['error_type'] == 'ImportError'

    @pytest.mark.asyncio
    async def test_resolves_headers_before_calling_assertion(self):
        """execute_assertion_method resolves headers identifier before calling assertion."""
        mock_class = MagicMock
        mock_instance = MagicMock()
        mock_method = MagicMock(return_value=True)
        mock_instance.test_assert = mock_method
        mock_class.return_value = mock_instance

        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            with patch('backend.core.external_precondition_bridge.resolve_headers') as mock_resolve:
                mock_load.return_value = ({'PcAssert': mock_class}, None)
                mock_resolve.return_value = {'Authorization': 'Bearer resolved_token'}

                with patch('backend.core.external_precondition_bridge.asyncio.wait_for') as mock_wait:
                    mock_wait.return_value = None

                    await execute_assertion_method('PcAssert', 'test_assert', headers='vice')

                    mock_resolve.assert_called_once_with('vice')


class TestParseAssertionError:
    """Tests for _parse_assertion_error() function."""

    def test_parses_field_comparison_message(self):
        """Parses standard field comparison error message."""
        message = "字段 'status' 预期值: '已发货', 实际值: '待发货'"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert results[0]['field'] == 'status'
        assert results[0]['expected'] == '已发货'
        assert results[0]['actual'] == '待发货'
        assert results[0]['passed'] is False

    def test_parses_contains_comparison_message(self):
        """Parses 'contains' comparison error message."""
        message = "字段 'name' 预期包含: '张', 实际值: '李四'"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert results[0]['field'] == 'name'
        assert results[0]['comparison_type'] == 'contains'

    def test_returns_fallback_for_unparseable_message(self):
        """Returns fallback result for unparseable message."""
        message = "Some random error message"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert results[0]['field'] == 'unknown'
        assert results[0]['description'] == message
