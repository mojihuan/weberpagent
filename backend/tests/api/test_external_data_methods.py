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


class TestExecuteDataMethodFunction:
    """Tests for execute_data_method() function in bridge module."""

    def test_returns_error_dict_when_class_not_found(self, reset_cache):
        """Should return error dict when class not found."""
        from backend.core.external_precondition_bridge import execute_data_method
        import asyncio

        with patch.object(
            external_precondition_bridge,
            'load_base_params_class',
            return_value=(None, "Module not available")
        ):
            result = asyncio.run(execute_data_method("UnknownClass", "some_method", {}))

            assert result["success"] is False
            assert "error" in result
            assert result["error_type"] == "ImportError"

    def test_returns_error_dict_when_method_not_found(self, reset_cache):
        """Should return error dict when method not found."""
        from backend.core.external_precondition_bridge import execute_data_method
        import asyncio

        # Mock a class without the requested method
        mock_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.unknown_method = None  # Method doesn't exist
        mock_class.return_value = mock_instance

        with patch.object(
            external_precondition_bridge,
            'load_base_params_class',
            return_value=(MagicMock, None)
        ):
            with patch('inspect.getmembers', return_value=[("BaseParams", mock_class)]):
                with patch('inspect.getmodule', return_value=MagicMock()):
                    with patch('inspect.isclass', return_value=True):
                        result = asyncio.run(execute_data_method("BaseParams", "unknown_method", {}))

                        assert result["success"] is False
                        assert "not found" in result["error"].lower()
                        assert result["error_type"] == "NotFoundError"

    def test_returns_success_dict_with_data_when_method_executes(self, reset_cache):
        """Should return success dict with data when method executes successfully."""
        from backend.core.external_precondition_bridge import execute_data_method
        import asyncio

        # Create a mock class with a method that returns data
        mock_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.test_method = MagicMock(return_value=[{"id": 1, "name": "test"}])
        mock_class.return_value = mock_instance

        with patch.object(
            external_precondition_bridge,
            'load_base_params_class',
            return_value=(MagicMock, None)
        ):
            with patch('inspect.getmembers', return_value=[("TestClass", mock_class)]):
                with patch('inspect.getmodule', return_value=MagicMock()):
                    with patch('inspect.isclass', return_value=True):
                        # Run async function
                        result = asyncio.run(execute_data_method("TestClass", "test_method", {}))

                        assert result["success"] is True
                        assert "data" in result
                        assert result["data"] == [{"id": 1, "name": "test"}]

    def test_returns_timeout_error(self, reset_cache):
        """Should return timeout error when execution exceeds timeout."""
        from backend.core.external_precondition_bridge import execute_data_method
        import asyncio
        import time

        # Create a mock class with a slow method
        mock_class = MagicMock()
        mock_instance = MagicMock()

        def slow_method(**kwargs):
            time.sleep(2)  # Sleep for 2 seconds
            return [{"id": 1}]

        mock_instance.slow_method = slow_method
        mock_class.return_value = mock_instance

        with patch.object(
            external_precondition_bridge,
            'load_base_params_class',
            return_value=(MagicMock, None)
        ):
            with patch('inspect.getmembers', return_value=[("TestClass", mock_class)]):
                with patch('inspect.getmodule', return_value=MagicMock()):
                    with patch('inspect.isclass', return_value=True):
                        # Run with 0.5 second timeout
                        result = asyncio.run(execute_data_method("TestClass", "slow_method", {}, timeout=0.5))

                        assert result["success"] is False
                        assert "timeout" in result["error"].lower()
                        assert result["error_type"] == "TimeoutError"

    def test_returns_parameter_error(self, reset_cache):
        """Should return parameter error when params type conversion fails."""
        from backend.core.external_precondition_bridge import execute_data_method
        import asyncio

        # Create a mock class with a method that requires specific types
        mock_class = MagicMock()
        mock_instance = MagicMock()

        def strict_method(i: int, **kwargs):
            return [{"id": i}]

        mock_instance.strict_method = strict_method
        mock_class.return_value = mock_instance

        with patch.object(
            external_precondition_bridge,
            'load_base_params_class',
            return_value=(MagicMock, None)
        ):
            with patch('inspect.getmembers', return_value=[("TestClass", mock_class)]):
                with patch('inspect.getmodule', return_value=MagicMock()):
                    with patch('inspect.isclass', return_value=True):
                        # Pass invalid params - this should raise TypeError when calling method
                        mock_instance.strict_method = MagicMock(side_effect=TypeError("'i' must be integer"))
                        result = asyncio.run(execute_data_method("TestClass", "strict_method", {"i": "not_a_number"}))

                        assert result["success"] is False
                        assert "parameter error" in result["error"].lower()
                        assert result["error_type"] == "ParameterError"

    def test_returns_execution_error(self, reset_cache):
        """Should return execution error when method raises exception."""
        from backend.core.external_precondition_bridge import execute_data_method
        import asyncio

        # Create a mock class with a method that raises exception
        mock_class = MagicMock()
        mock_instance = MagicMock()
        mock_instance.failing_method = MagicMock(side_effect=ValueError("Database connection failed"))
        mock_class.return_value = mock_instance

        with patch.object(
            external_precondition_bridge,
            'load_base_params_class',
            return_value=(MagicMock, None)
        ):
            with patch('inspect.getmembers', return_value=[("TestClass", mock_class)]):
                with patch('inspect.getmodule', return_value=MagicMock()):
                    with patch('inspect.isclass', return_value=True):
                        result = asyncio.run(execute_data_method("TestClass", "failing_method", {}))

                        assert result["success"] is False
                        assert "database connection failed" in result["error"].lower()
                        assert result["error_type"] == "ExecutionError"


class TestExecuteDataMethod:
    """Tests for POST /api/external-data-methods/execute endpoint."""

    def test_returns_503_when_module_unavailable(self, client):
        """Should return 503 when WEBSERP_PATH not configured."""
        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_data_methods.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            response = client.post(
                "/api/external-data-methods/execute",
                json={
                    "class_name": "BaseParams",
                    "method_name": "inventory_list_data",
                    "params": {}
                }
            )

            assert response.status_code == 503
            data = response.json()
            # The error is wrapped by the global exception handler
            assert "error" in data or "detail" in data

            # Check for 503 or "not available" in response
            assert "not available" in str(data).lower() or "503" in str(data)

    def test_returns_200_with_error_when_class_not_found(self, client, reset_cache):
        """Should return 200 with error when class not found."""
        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.execute_data_method',
            return_value={
                "success": False,
                "error": "Class 'UnknownClass' not found",
                "error_type": "NotFoundError"
            }
        ):
            response = client.post(
                "/api/external-data-methods/execute",
                json={
                    "class_name": "UnknownClass",
                    "method_name": "some_method",
                    "params": {}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "not found" in data["error"].lower()
            assert data["error_type"] == "NotFoundError"

    def test_returns_200_with_error_when_method_not_found(self, client, reset_cache):
        """Should return 200 with error when method not found."""
        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.execute_data_method',
            return_value={
                "success": False,
                "error": "Method 'unknown_method' not found",
                "error_type": "NotFoundError"
            }
        ):
            response = client.post(
                "/api/external-data-methods/execute",
                json={
                    "class_name": "BaseParams",
                    "method_name": "unknown_method",
                    "params": {}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "not found" in data["error"].lower()

    def test_returns_200_with_data_when_success(self, client, reset_cache):
        """Should return 200 with data when method executes successfully."""
        mock_data = [
            {"imei": "123456789012345", "name": "Product A"},
            {"imei": "123456789012346", "name": "Product B"}
        ]

        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.execute_data_method',
            return_value={
                "success": True,
                "data": mock_data
            }
        ):
            response = client.post(
                "/api/external-data-methods/execute",
                json={
                    "class_name": "BaseParams",
                    "method_name": "inventory_list_data",
                    "params": {"i": 0, "j": 10}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"] == mock_data
            assert data["error"] is None
            assert data["error_type"] is None

    def test_returns_200_with_timeout_error(self, client, reset_cache):
        """Should return 200 with timeout error when execution times out."""
        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.execute_data_method',
            return_value={
                "success": False,
                "error": "Execution timeout (30.0s)",
                "error_type": "TimeoutError"
            }
        ):
            response = client.post(
                "/api/external-data-methods/execute",
                json={
                    "class_name": "BaseParams",
                    "method_name": "slow_method",
                    "params": {}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "timeout" in data["error"].lower()
            assert data["error_type"] == "TimeoutError"

    def test_returns_200_with_parameter_error(self, client, reset_cache):
        """Should return 200 with parameter error when params invalid."""
        with patch(
            'backend.api.routes.external_data_methods.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_data_methods.execute_data_method',
            return_value={
                "success": False,
                "error": "Parameter error: 'i' must be integer",
                "error_type": "ParameterError"
            }
        ):
            response = client.post(
                "/api/external-data-methods/execute",
                json={
                    "class_name": "BaseParams",
                    "method_name": "inventory_list_data",
                    "params": {"i": "not_a_number"}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "parameter error" in data["error"].lower()
            assert data["error_type"] == "ParameterError"
