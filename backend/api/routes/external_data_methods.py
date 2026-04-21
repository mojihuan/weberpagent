"""External data methods API routes.

Provides REST API for discovering available data query methods
from external webseleniumerp project's base_params.py module.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any

from backend.core.external_precondition_bridge import (
    is_available,
    get_unavailable_reason,
    get_data_methods_grouped,
    execute_data_method,
)


router = APIRouter(prefix="/external-data-methods", tags=["external-data-methods"])


class ParameterInfo(BaseModel):
    """Single method parameter info."""
    name: str
    type: str
    required: bool
    default: Optional[str] = None
    description: Optional[str] = None


class MethodInfo(BaseModel):
    """Single data method info."""
    name: str
    description: str
    parameters: list[ParameterInfo]
    docstring_id: Optional[str] = None  # Stable identifier from docstring first line


class ClassGroup(BaseModel):
    """Group of methods under a class name."""
    name: str
    methods: list[MethodInfo]


class DataMethodsResponse(BaseModel):
    """Response model for listing data methods."""
    available: bool
    classes: list[ClassGroup] = []
    total: int = 0
    error: Optional[str] = None


class ExecuteRequest(BaseModel):
    """Request model for executing a data method."""
    class_name: str
    method_name: str
    params: dict = {}


class ExecuteResponse(BaseModel):
    """Response model for method execution."""
    success: bool
    data: Optional[list[dict]] = None
    error: Optional[str] = None
    error_type: Optional[str] = None


@router.get("", response_model=DataMethodsResponse)
async def list_data_methods():
    """List all available data query methods.

    Returns 503 if external module is not available.
    """
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External data methods module not available",
                "reason": get_unavailable_reason(),
                "fix": "Ensure WEBSERP_PATH is configured in .env and config/settings.py exists in webseleniumerp"
            }
        )

    classes = get_data_methods_grouped()
    total = sum(len(c["methods"]) for c in classes)

    return DataMethodsResponse(
        available=True,
        classes=[ClassGroup(**c) for c in classes],
        total=total
    )


@router.post("/execute", response_model=ExecuteResponse)
async def execute_method(request: ExecuteRequest):
    """Execute a data method and return results.

    Returns 503 if external module is not available.
    Returns 200 with success=False and error field if execution fails.
    """
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External data methods module not available",
                "reason": get_unavailable_reason(),
                "fix": "Ensure WEBSERP_PATH is configured in .env and config/settings.py exists in webseleniumerp"
            }
        )

    result = await execute_data_method(
        request.class_name,
        request.method_name,
        request.params
    )

    return ExecuteResponse(**result)
