"""Tests for assertion execution functions in external_precondition_bridge."""

import pytest
from unittest.mock import patch, MagicMock

from backend.core.external_precondition_bridge import (
    resolve_headers,
    VALID_HEADER_IDENTIFIERS,
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
