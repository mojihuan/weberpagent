"""Standard API response format module.

Provides consistent response structure for all API endpoints.
All responses have a 'success' field (boolean).
Successful responses have 'data' field.
Error responses have 'error' object with code, message, request_id.
"""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel
import uuid


T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Error response body"""
    code: str
    message: str
    request_id: str
    stack: Optional[str] = None


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None
    meta: Optional[dict] = None


def success_response(data: Any, meta: dict = None) -> dict:
    """Create success response.

    Args:
        data: The response data
        meta: Optional metadata (pagination, totals, etc.)

    Returns:
        Dict with success=True and data field
    """
    return {"success": True, "data": data, "meta": meta}


def error_response(
    code: str,
    message: str,
    request_id: str = None,
    status_code: int = 400,
    stack: str = None
) -> tuple[dict, int]:
    """Create error response with status code.

    Args:
        code: Error code (e.g., NOT_FOUND, VALIDATION_ERROR)
        message: Human-readable error message
        request_id: Optional request ID for debugging (auto-generated if not provided)
        status_code: HTTP status code (default 400)
        stack: Optional stack trace for debugging

    Returns:
        Tuple of (error dict, status code)
    """
    error_body = {
        "code": code,
        "message": message,
        "request_id": request_id or str(uuid.uuid4()),
    }
    if stack is not None:
        error_body["stack"] = stack

    return {
        "success": False,
        "error": error_body
    }, status_code


class ErrorCodes:
    """Standard error code constants"""
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
