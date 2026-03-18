"""API integration tests for external operations endpoint."""

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
def reset_bridge_cache():
    """Reset bridge cache before and after each test."""
    external_precondition_bridge.reset_cache()
    yield
    external_precondition_bridge.reset_cache()


class TestListOperations:
    """Tests for GET /api/external-operations endpoint."""

    def test_list_operations_returns_503_when_unavailable(self, client):
        """Test GET /api/external-operations returns 503 when external module unavailable."""
        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_operations.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            response = client.get("/api/external-operations")

            assert response.status_code == 503
            # The detail is wrapped by the global exception handler
            data = response.json()
            # Check for the error message in the response
            assert "error" in data
            # The original detail dict is stringified in the error message
            assert "not available" in str(data).lower() or "503" in str(data)

    def test_list_operations_returns_operations_when_available(self, client):
        """Test GET /api/external-operations returns correct response structure when available."""
        mock_modules = [
            {
                "name": "Test Module",
                "operations": [{"code": "T1", "description": "Test op"}]
            }
        ]

        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_operations.get_operations_grouped',
            return_value=mock_modules
        ):
            response = client.get("/api/external-operations")

            assert response.status_code == 200
            data = response.json()
            assert data["available"] is True
            assert data["total"] == 1
            assert len(data["modules"]) == 1
            assert data["modules"][0]["name"] == "Test Module"
            assert data["modules"][0]["operations"][0]["code"] == "T1"


class TestGenerateCode:
    """Tests for POST /api/external-operations/generate endpoint."""

    def test_generate_code_returns_code(self, client):
        """Test POST /api/external-operations/generate returns generated code."""
        mock_settings = MagicMock()
        mock_settings.weberp_path = "/test/path"

        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_operations.get_settings',
            return_value=mock_settings
        ):
            response = client.post(
                "/api/external-operations/generate",
                json={"operation_codes": ["FA1"]}
            )

            assert response.status_code == 200
            data = response.json()
            assert "code" in data
            assert "sys.path.insert" in data["code"]
            assert "FA1" in data["code"]

    def test_generate_code_returns_503_when_unavailable(self, client):
        """Test POST /api/external-operations/generate returns 503 when unavailable."""
        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_operations.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            response = client.post(
                "/api/external-operations/generate",
                json={"operation_codes": ["FA1"]}
            )

            assert response.status_code == 503

    def test_generate_code_returns_503_when_weberp_path_not_configured(self, client):
        """Test POST /api/external-operations/generate returns 503 when weberp_path is None."""
        mock_settings = MagicMock()
        mock_settings.weberp_path = None

        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_operations.get_settings',
            return_value=mock_settings
        ):
            response = client.post(
                "/api/external-operations/generate",
                json={"operation_codes": ["FA1"]}
            )

            assert response.status_code == 503

    def test_generate_code_validates_operation_codes_required(self, client):
        """Test POST /api/external-operations/generate validates operation_codes is required."""
        mock_settings = MagicMock()
        mock_settings.weberp_path = "/test/path"

        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=True
        ), patch(
            'backend.api.routes.external_operations.get_settings',
            return_value=mock_settings
        ):
            # Missing operation_codes field - FastAPI wraps validation errors with our handler
            response = client.post("/api/external-operations/generate", json={})
            # Our validation_exception_handler returns 400 for RequestValidationError
            assert response.status_code == 400
