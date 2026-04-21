"""Tests for assertion execution functions in external_precondition_bridge."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from backend.core.external_precondition_bridge import (
    resolve_headers,
    VALID_HEADER_IDENTIFIERS,
    execute_assertion_method,
    _parse_assertion_error,
    execute_all_assertions,
)
from backend.core.precondition_service import ContextWrapper


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
            mock_load.return_value = ({'PcAssert': MagicMock}, None)

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
            mock_load.return_value = ({'PcAssert': MagicMock}, None)

            # Create assertion method that raises AssertionError
            async def raise_assertion_error(*args, **kwargs):
                raise AssertionError("字段 'status' 预期值: '已发货', 实际值: '待发货'")

            with patch('backend.core.external_precondition_bridge.asyncio.wait_for', side_effect=raise_assertion_error):
                result = await execute_assertion_method('PcAssert', 'test_assert')

                assert result['success'] is True  # Execution succeeded
                assert result['passed'] is False  # Assertion failed
                assert len(result['fields']) > 0  # Uses 'fields' per ROADMAP API Contract

    @pytest.mark.asyncio
    async def test_returns_timeout_error_when_exceeds_timeout(self):
        """execute_assertion_method returns TimeoutError when execution exceeds timeout."""
        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            mock_load.return_value = ({'PcAssert': MagicMock}, None)

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
    async def test_passes_headers_identifier_to_assertion(self):
        """execute_assertion_method passes headers as identifier string to assertion method."""
        # Use a real class so getattr returns the actual method
        call_record = {}

        class FakeAssert:
            def test_assert(self, **kwargs):
                call_record.update(kwargs)
                return None

        fake_class = FakeAssert

        with patch('backend.core.external_precondition_bridge.load_base_assertions_class') as mock_load:
            mock_load.return_value = ({'PcAssert': fake_class}, None)

            # Mock asyncio.get_event_loop to return a loop where run_in_executor
            # calls the function synchronously
            with patch('backend.core.external_precondition_bridge.asyncio.get_event_loop') as mock_get_loop:
                mock_loop = MagicMock()
                mock_get_loop.return_value = mock_loop

                async def fake_wait_for(coro_or_future, timeout=None):
                    pass

                mock_loop.run_in_executor = MagicMock(
                    return_value=asyncio.Future()
                )
                mock_loop.run_in_executor.return_value.set_result(None)

                with patch('backend.core.external_precondition_bridge.asyncio.wait_for', side_effect=fake_wait_for):
                    await execute_assertion_method('PcAssert', 'test_assert', headers='vice')

        # Execute the captured lambda to verify headers was passed correctly
        assert mock_loop.run_in_executor.call_count == 1
        executor_arg, lambda_fn = mock_loop.run_in_executor.call_args[0]
        assert executor_arg is None
        lambda_fn()
        assert call_record.get('headers') == 'vice'


class TestParseAssertionError:
    """Tests for _parse_assertion_error() function."""

    def test_parses_field_comparison_message(self):
        """Parses standard field comparison error message."""
        message = "字段 'status' 预期值: '已发货', 实际值: '待发货'"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert results[0]['name'] == 'status'  # Uses 'name' per ROADMAP API Contract
        assert results[0]['expected'] == '已发货'
        assert results[0]['actual'] == '待发货'
        assert results[0]['passed'] is False

    def test_parses_contains_comparison_message(self):
        """Parses 'contains' comparison error message."""
        message = "字段 'name' 预期包含: '张', 实际值: '李四'"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert results[0]['name'] == 'name'  # Uses 'name' per ROADMAP API Contract
        assert results[0]['comparison_type'] == 'contains'

    def test_returns_fallback_for_unparseable_message(self):
        """Returns fallback result for unparseable message."""
        message = "Some random error message"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert results[0]['name'] == 'unknown'  # Uses 'name' per ROADMAP API Contract
        assert results[0]['description'] == message

    def test_returns_name_not_field(self):
        """_parse_assertion_error returns 'name' key (not 'field') per ROADMAP API Contract."""
        message = "字段 'statusStr' 预期值: '已完成', 实际值: '进行中'"
        results = _parse_assertion_error(message)

        assert len(results) == 1
        assert 'name' in results[0]
        assert results[0]['name'] == 'statusStr'
        # 'field' key should NOT exist (deprecated in favor of 'name')
        assert 'field' not in results[0]


class TestExecuteAllAssertions:
    """Tests for execute_all_assertions() function."""

    @pytest.mark.asyncio
    async def test_executes_multiple_assertions_in_sequence(self):
        """execute_all_assertions executes multiple assertions in sequence."""
        context = ContextWrapper()
        assertions = [
            {
                'class_name': 'PcAssert',
                'method_name': 'assert_1',
                'headers': 'main',
                'data': 'main',
                'params': {}
            },
            {
                'class_name': 'PcAssert',
                'method_name': 'assert_2',
                'headers': 'main',
                'data': 'main',
                'params': {}
            }
        ]

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.return_value = {
                'success': True,
                'passed': True,
                'fields': [],
                'duration': 0.1,
                'error': None,
                'error_type': None
            }

            result = await execute_all_assertions(assertions, context)

            assert mock_exec.call_count == 2
            assert result['total'] == 2

    @pytest.mark.asyncio
    async def test_stores_results_in_context_via_store_assertion_result(self):
        """execute_all_assertions stores results in context via store_assertion_result."""
        context = ContextWrapper()
        assertions = [
            {'class_name': 'PcAssert', 'method_name': 'test', 'headers': 'main', 'data': 'main', 'params': {}}
        ]

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.return_value = {
                'success': True,
                'passed': True,
                'fields': [],
                'duration': 0.1
            }

            await execute_all_assertions(assertions, context)

            assert 'assertion_result_0' in context._data
            assert context['assertion_result_0']['passed'] is True

    @pytest.mark.asyncio
    async def test_continues_even_if_one_assertion_fails(self):
        """execute_all_assertions continues even if one assertion fails (non-fail-fast)."""
        context = ContextWrapper()
        assertions = [
            {'class_name': 'PcAssert', 'method_name': 'pass', 'headers': 'main', 'data': 'main', 'params': {}},
            {'class_name': 'PcAssert', 'method_name': 'fail', 'headers': 'main', 'data': 'main', 'params': {}},
            {'class_name': 'PcAssert', 'method_name': 'pass2', 'headers': 'main', 'data': 'main', 'params': {}}
        ]

        call_count = 0

        async def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                return {
                    'success': True,
                    'passed': False,
                    'fields': [{'name': 'x', 'expected': 'a', 'actual': 'b'}],
                    'duration': 0.1,
                    'error': 'Assertion failed'
                }
            return {
                'success': True,
                'passed': True,
                'fields': [],
                'duration': 0.1
            }

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.side_effect = side_effect

            result = await execute_all_assertions(assertions, context)

            # All 3 should have been executed
            assert mock_exec.call_count == 3
            assert result['total'] == 3
            assert result['passed'] == 2
            assert result['failed'] == 1

    @pytest.mark.asyncio
    async def test_returns_summary_with_total_passed_failed_errors(self):
        """execute_all_assertions returns summary with total/passed/failed/errors."""
        context = ContextWrapper()
        assertions = [
            {'class_name': 'PcAssert', 'method_name': 'pass', 'headers': 'main', 'data': 'main', 'params': {}},
            {'class_name': 'PcAssert', 'method_name': 'fail', 'headers': 'main', 'data': 'main', 'params': {}},
            {'class_name': 'PcAssert', 'method_name': 'error', 'headers': 'main', 'data': 'main', 'params': {}}
        ]

        call_count = 0

        async def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return {'success': True, 'passed': True, 'fields': [], 'duration': 0.1}
            elif call_count == 2:
                return {'success': True, 'passed': False, 'fields': [], 'duration': 0.1}
            else:
                return {'success': False, 'passed': False, 'error_type': 'TimeoutError', 'fields': [], 'duration': 30.0}

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.side_effect = side_effect

            result = await execute_all_assertions(assertions, context)

            assert 'total' in result
            assert 'passed' in result
            assert 'failed' in result
            assert 'errors' in result
            assert result['total'] == 3
            assert result['passed'] == 1
            assert result['failed'] == 1
            assert result['errors'] == 1

    @pytest.mark.asyncio
    async def test_handles_empty_assertion_list_gracefully(self):
        """execute_all_assertions handles empty assertion list gracefully."""
        context = ContextWrapper()
        assertions = []

        result = await execute_all_assertions(assertions, context)

        assert result['total'] == 0
        assert result['passed'] == 0
        assert result['failed'] == 0
        assert result['errors'] == 0
        assert result['results'] == []

    @pytest.mark.asyncio
    async def test_catches_unexpected_errors_and_continues(self):
        """execute_all_assertions catches unexpected errors and continues."""
        context = ContextWrapper()
        assertions = [
            {'class_name': 'PcAssert', 'method_name': 'crash', 'headers': 'main', 'data': 'main', 'params': {}},
            {'class_name': 'PcAssert', 'method_name': 'pass', 'headers': 'main', 'data': 'main', 'params': {}}
        ]

        call_count = 0

        async def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("Unexpected crash!")
            return {'success': True, 'passed': True, 'fields': [], 'duration': 0.1}

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.side_effect = side_effect

            result = await execute_all_assertions(assertions, context)

            # Both assertions should have been attempted
            assert mock_exec.call_count == 2
            assert result['errors'] == 1  # First one had unexpected error
            assert result['passed'] == 1  # Second one passed


class TestExecuteAllAssertionsThreeLayerParams:
    """Tests for three-layer parameter passing in execute_all_assertions."""

    @pytest.mark.asyncio
    async def test_passes_api_params_to_execute_assertion_method(self):
        """execute_all_assertions passes api_params to execute_assertion_method."""
        context = ContextWrapper()
        assertions = [{
            'class_name': 'PcAssert',
            'method_name': 'test',
            'headers': 'main',
            'data': 'main',
            'api_params': {'i': 1, 'j': 2},
        }]

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.return_value = {'success': True, 'passed': True, 'fields': [], 'duration': 0.1}
            await execute_all_assertions(assertions, context)

            # Verify api_params was passed
            call_kwargs = mock_exec.call_args[1]
            assert call_kwargs['api_params'] == {'i': 1, 'j': 2}

    @pytest.mark.asyncio
    async def test_passes_field_params_to_execute_assertion_method(self):
        """execute_all_assertions passes field_params to execute_assertion_method."""
        context = ContextWrapper()
        assertions = [{
            'class_name': 'PcAssert',
            'method_name': 'test',
            'headers': 'main',
            'data': 'main',
            'field_params': {'saleTime': 'now', 'salesOrder': 'SA'},
        }]

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.return_value = {'success': True, 'passed': True, 'fields': [], 'duration': 0.1}
            await execute_all_assertions(assertions, context)

            # Verify field_params was passed
            call_kwargs = mock_exec.call_args[1]
            assert call_kwargs['field_params'] == {'saleTime': 'now', 'salesOrder': 'SA'}

    @pytest.mark.asyncio
    async def test_passes_all_three_layers_simultaneously(self):
        """execute_all_assertions passes api_params, field_params, and params together."""
        context = ContextWrapper()
        assertions = [{
            'class_name': 'PcAssert',
            'method_name': 'test',
            'headers': 'main',
            'data': 'main',
            'api_params': {'i': 1, 'j': 2},
            'field_params': {'saleTime': 'now', 'salesOrder': 'SA'},
            'params': {'extra': 'value'},
        }]

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.return_value = {'success': True, 'passed': True, 'fields': [], 'duration': 0.1}
            await execute_all_assertions(assertions, context)

            # Verify all three layers were passed correctly
            call_kwargs = mock_exec.call_args[1]
            assert call_kwargs['api_params'] == {'i': 1, 'j': 2}
            assert call_kwargs['field_params'] == {'saleTime': 'now', 'salesOrder': 'SA'}
            assert call_kwargs['params'] == {'extra': 'value'}

    @pytest.mark.asyncio
    async def test_backward_compat_with_only_params(self):
        """execute_all_assertions works with old configs using only params."""
        context = ContextWrapper()
        assertions = [{
            'class_name': 'PcAssert',
            'method_name': 'test',
            'headers': 'main',
            'data': 'main',
            'params': {'i': 1, 'j': 2},
        }]

        with patch('backend.core.external_precondition_bridge.execute_assertion_method') as mock_exec:
            mock_exec.return_value = {'success': True, 'passed': True, 'fields': [], 'duration': 0.1}
            await execute_all_assertions(assertions, context)

            # Verify params is still passed for backward compatibility
            call_kwargs = mock_exec.call_args[1]
            assert call_kwargs['params'] == {'i': 1, 'j': 2}
            # api_params and field_params should default to empty dicts
            assert call_kwargs['api_params'] == {}
            assert call_kwargs['field_params'] == {}
