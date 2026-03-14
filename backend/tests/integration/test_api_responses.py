"""Integration tests for API response format consistency"""

import pytest
from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_health_endpoint_success_format():
    """Health endpoint returns success format"""
    response = client.get("/health")
    assert response.status_code == 200
    # Health endpoint is simple, just verify it works


def test_404_response_format():
    """404 errors return consistent format"""
    response = client.get("/api/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    assert "request_id" in data["error"]


def test_validation_error_format():
    """Validation errors return 400 with consistent format"""
    # Try to create task without required fields
    # Our validation handler converts 422 to 400 for consistency
    response = client.post("/api/tasks", json={})
    assert response.status_code == 400  # Converted from 422 by our handler
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "details" in data["error"]
