"""Unit tests for API response format module"""

import pytest
from backend.api.response import (
    ApiResponse,
    ErrorResponse,
    success_response,
    error_response,
    ErrorCodes,
)


def test_success_response_structure():
    """Success response has success=true and data field"""
    result = success_response({"id": 1, "name": "test"})
    assert result["success"] is True
    assert result["data"]["id"] == 1
    assert result["meta"] is None


def test_success_response_with_meta():
    """Success response can include meta field"""
    result = success_response([1, 2, 3], {"total": 3, "page": 1})
    assert result["meta"]["total"] == 3


def test_error_response_structure():
    """Error response has success=false and error object"""
    result, status = error_response("NOT_FOUND", "Item not found")
    assert result["success"] is False
    assert result["error"]["code"] == "NOT_FOUND"
    assert result["error"]["message"] == "Item not found"
    assert "request_id" in result["error"]
    assert status == 400


def test_error_response_with_custom_status():
    """Error response can have custom status code"""
    result, status = error_response("NOT_FOUND", "Not found", status_code=404)
    assert status == 404


def test_error_response_with_stack():
    """Error response can include stack trace"""
    result, _ = error_response("INTERNAL_ERROR", "Error", stack="Traceback...")
    assert result["error"]["stack"] == "Traceback..."


def test_error_response_request_id_provided():
    """Error response uses provided request_id"""
    result, _ = error_response("ERROR", "msg", request_id="custom-id")
    assert result["error"]["request_id"] == "custom-id"


def test_api_response_model_validates_success_required():
    """ApiResponse model validates success field is required"""
    # Valid with success=True
    response = ApiResponse(success=True, data={"test": "value"})
    assert response.success is True

    # Valid with success=False
    response = ApiResponse(success=False, error={"code": "ERR", "message": "Error"})
    assert response.success is False


def test_meta_field_optional():
    """Meta field is optional in success responses"""
    result = success_response({"id": 1})
    assert result["meta"] is None

    result_with_meta = success_response({"id": 1}, {"page": 1})
    assert result_with_meta["meta"]["page"] == 1


def test_error_codes_constants():
    """Error code constants are defined"""
    assert ErrorCodes.NOT_FOUND == "NOT_FOUND"
    assert ErrorCodes.VALIDATION_ERROR == "VALIDATION_ERROR"
    assert ErrorCodes.INTERNAL_ERROR == "INTERNAL_ERROR"
    assert ErrorCodes.BAD_REQUEST == "BAD_REQUEST"
