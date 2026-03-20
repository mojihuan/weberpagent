"""API integration tests for external assertion methods endpoint."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.api.main import app
from backend.core import external_precondition_bridge


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset bridge cache before and after each test."""
    external_precondition_bridge.reset_cache()
    yield
    external_precondition_bridge.reset_cache()


class TestListAssertionMethods:
    """Tests for GET /api/external-assertions/methods endpoint."""

    def test_list_assertion_methods_returns_503_when_unavailable(self, client):
        """Test GET /api/external-assertions/methods returns 503 when external module unavailable."""
        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_assertions.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            response = client.get("/api/external-assertions/methods")

            assert response.status_code == 503
            # The detail is wrapped by the global exception handler
            data = response.json()
            # Check for the error message in the response
            assert "error" in data
            # The original detail dict is stringified in the error message
            assert "not available" in str(data).lower() or "503" in str(data)

    def test_list_assertion_methods_returns_200_with_methods_when_available(self, client):
        """Test GET /api/external-assertions/methods returns correct response structure when available."""
        mock_methods = [
            {
                "name": "PcAssert",
                "methods": [
                    {
                        "name": "attachment_inventory_list_assert",
                        "description": "Get inventory list assertion",
                        "data_options": [
                            {"value": "main", "label": "主数据"},
                            {"value": "a", "label": "配件数据"},
                            {"value": "b", "label": "分店数据"}
                        ],
                        "parameters": [
                            {"name": "i", "description": "Status", "options": [{"value": 1, "label": "Pending"}]}
                        ]
                    }
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_assertions.get_assertion_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-assertions/methods")

            assert response.status_code == 200
            data = response.json()
            assert data["available"] is True
            assert data["total"] == 1
            assert len(data["classes"]) == 1
            assert data["classes"][0]["name"] == "PcAssert"
            assert len(data["classes"][0]["methods"]) == 1
            assert data["classes"][0]["methods"][0]["name"] == "attachment_inventory_list_assert"

    def test_list_assertion_methods_includes_headers_options(self, client):
        """Test that response includes headers_options field with 7 identifiers."""
        mock_methods = [
            {
                "name": "PcAssert",
                "methods": [
                    {
                        "name": "test_assert",
                        "description": "Test assertion",
                        "data_options": [{"value": "main", "label": "主数据"}],
                        "parameters": []
                    }
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_assertions.get_assertion_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-assertions/methods")

            assert response.status_code == 200
            data = response.json()
            assert "headers_options" in data
            assert len(data["headers_options"]) == 7
            # headers_options now returns list of {value, label} objects
            assert data["headers_options"][0] == {"value": "main", "label": "主请求头"}
            assert data["headers_options"][1] == {"value": "idle", "label": "空闲请求头"}

    def test_list_assertion_methods_returns_total_count(self, client):
        """Test that total count is sum of all methods across all classes."""
        mock_methods = [
            {
                "name": "PcAssert",
                "methods": [
                    {"name": "m1", "description": "M1", "data_options": [{"value": "main", "label": "主数据"}], "parameters": []},
                    {"name": "m2", "description": "M2", "data_options": [{"value": "main", "label": "主数据"}], "parameters": []},
                ]
            },
            {
                "name": "MgAssert",
                "methods": [
                    {"name": "m3", "description": "M3", "data_options": [{"value": "main", "label": "主数据"}], "parameters": []},
                    {"name": "m4", "description": "M4", "data_options": [{"value": "main", "label": "主数据"}], "parameters": []},
                    {"name": "m5", "description": "M5", "data_options": [{"value": "main", "label": "主数据"}], "parameters": []},
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_assertions.get_assertion_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-assertions/methods")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 5  # 2 + 3 methods

    def test_endpoint_registered_in_app(self, client):
        """Test that /api/external-assertions/methods is accessible (not 404)."""
        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_assertions.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            response = client.get("/api/external-assertions/methods")
            # Should get 503, not 404 (proves route is registered)
            assert response.status_code == 503
            assert response.status_code != 404


class TestAssertionMethodDataOptions:
    """Tests for data_options field in assertion methods."""

    def test_data_options_field_present(self, client):
        """Test that each method includes data_options field with value/label pairs."""
        mock_methods = [
            {
                "name": "PcAssert",
                "methods": [
                    {
                        "name": "test_assert",
                        "description": "Test",
                        "data_options": [
                            {"value": "main", "label": "主数据"},
                            {"value": "a", "label": "配件数据"},
                            {"value": "b", "label": "分店数据"},
                            {"value": "c", "label": "仓库数据"}
                        ],
                        "parameters": []
                    }
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_assertions.get_assertion_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-assertions/methods")

            assert response.status_code == 200
            data = response.json()
            method = data["classes"][0]["methods"][0]
            assert "data_options" in method
            # Check that data_options is list of {value, label} objects
            assert len(method["data_options"]) == 4
            assert method["data_options"][0] == {"value": "main", "label": "主数据"}

    def test_parameters_include_options(self, client):
        """Test that parameters include options field with value/label pairs."""
        mock_methods = [
            {
                "name": "PcAssert",
                "methods": [
                    {
                        "name": "test_assert",
                        "description": "Test",
                        "data_options": [{"value": "main", "label": "主数据"}],
                        "parameters": [
                            {
                                "name": "i",
                                "description": "Order Status",
                                "options": [
                                    {"value": 1, "label": "Pending"},
                                    {"value": 2, "label": "Completed"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_assertions.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_assertions.get_assertion_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-assertions/methods")

            assert response.status_code == 200
            data = response.json()
            params = data["classes"][0]["methods"][0]["parameters"]
            assert len(params) == 1
            assert params[0]["name"] == "i"
            assert params[0]["description"] == "Order Status"
            assert len(params[0]["options"]) == 2
            assert params[0]["options"][0] == {"value": 1, "label": "Pending"}
            assert params[0]["options"][1] == {"value": 2, "label": "Completed"}
