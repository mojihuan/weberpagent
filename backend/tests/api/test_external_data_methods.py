"""API integration tests for external data methods endpoint."""

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


class TestListDataMethods:
    """Tests for GET /api/external-data-methods endpoint."""

    def test_returns_503_when_module_unavailable(self, client):
        """Test GET /api/external-data-methods returns 503 when external module unavailable."""
        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_data_methods.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            response = client.get("/api/external-data-methods")

            assert response.status_code == 503
            # The detail is wrapped by the global exception handler
            data = response.json()
            # Check for the error message in the response
            assert "error" in data
            # The original detail dict is stringified in the error message
            assert "not available" in str(data).lower() or "503" in str(data)

    def test_returns_200_with_methods_when_available(self, client):
        """Test GET /api/external-data-methods returns correct response structure when available."""
        mock_methods = [
            {
                "name": "BaseParams",
                "methods": [
                    {
                        "name": "inventory_list_data",
                        "description": "Get inventory list",
                        "parameters": [
                            {"name": "i", "type": "int", "required": False, "default": "0"}
                        ]
                    }
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.get_data_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-data-methods")

            assert response.status_code == 200
            data = response.json()
            assert data["available"] is True
            assert data["total"] == 1
            assert len(data["classes"]) == 1
            assert data["classes"][0]["name"] == "BaseParams"
            assert len(data["classes"][0]["methods"]) == 1
            assert data["classes"][0]["methods"][0]["name"] == "inventory_list_data"

    def test_returns_grouped_classes_with_methods(self, client):
        """Test that methods are grouped by class name."""
        mock_methods = [
            {
                "name": "BaseParams",
                "methods": [
                    {"name": "method1", "description": "Method 1", "parameters": []},
                    {"name": "method2", "description": "Method 2", "parameters": []},
                ]
            },
            {
                "name": "InventoryParams",
                "methods": [
                    {"name": "method3", "description": "Method 3", "parameters": []},
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.get_data_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-data-methods")

            assert response.status_code == 200
            data = response.json()
            assert data["available"] is True
            assert data["total"] == 3
            assert len(data["classes"]) == 2
            # Check class names
            class_names = [c["name"] for c in data["classes"]]
            assert "BaseParams" in class_names
            assert "InventoryParams" in class_names

    def test_returns_total_count_across_all_classes(self, client):
        """Test that total count is sum of all methods across all classes."""
        mock_methods = [
            {
                "name": "ClassA",
                "methods": [
                    {"name": "m1", "description": "M1", "parameters": []},
                    {"name": "m2", "description": "M2", "parameters": []},
                ]
            },
            {
                "name": "ClassB",
                "methods": [
                    {"name": "m3", "description": "M3", "parameters": []},
                    {"name": "m4", "description": "M4", "parameters": []},
                    {"name": "m5", "description": "M5", "parameters": []},
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.get_data_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-data-methods")

            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 5  # 2 + 3 methods

    def test_parameters_include_required_and_default(self, client):
        """Test that parameters include required and default fields."""
        mock_methods = [
            {
                "name": "TestClass",
                "methods": [
                    {
                        "name": "test_method",
                        "description": "Test method",
                        "parameters": [
                            {"name": "required_param", "type": "str", "required": True, "default": None},
                            {"name": "optional_param", "type": "int", "required": False, "default": "10"},
                        ]
                    }
                ]
            }
        ]

        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.get_data_methods_grouped',
            return_value=mock_methods
        ):
            response = client.get("/api/external-data-methods")

            assert response.status_code == 200
            data = response.json()
            params = data["classes"][0]["methods"][0]["parameters"]
            assert len(params) == 2
            # Check required param
            assert params[0]["name"] == "required_param"
            assert params[0]["required"] is True
            assert params[0]["default"] is None
            # Check optional param
            assert params[1]["name"] == "optional_param"
            assert params[1]["required"] is False
            assert params[1]["default"] == "10"
