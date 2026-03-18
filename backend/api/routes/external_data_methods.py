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
)


router = APIRouter(prefix="/external-data-methods", tags=["external-data-methods"])


class ParameterInfo(BaseModel):
    """Single method parameter info."""
    name: str
    type: str
    required: bool
    default: Optional[str] = None


class MethodInfo(BaseModel):
    """Single data method info."""
    name: str
    description: str
    parameters: list[ParameterInfo]


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
