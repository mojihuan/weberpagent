"""External assertion methods API routes.

Provides REST API for discovering available assertion methods
from external webseleniumerp project's base_assertions.py module.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.core.external_precondition_bridge import (
    is_available,
    get_unavailable_reason,
    get_assertion_methods_grouped,
    get_assertion_fields_grouped,
    execute_assertion_method,
)


router = APIRouter(prefix="/external-assertions", tags=["external-assertions"])

# Fixed headers identifiers (mapped to actual tokens at execution time)
HEADERS_OPTIONS = ["main", "idle", "vice", "special", "platform", "super", "camera"]

# Labels for headers options
HEADERS_LABELS = {
    "main": "主请求头",
    "idle": "空闲请求头",
    "vice": "副请求头",
    "special": "特殊请求头",
    "platform": "平台请求头",
    "super": "超级请求头",
    "camera": "摄像头请求头",
}


class ParameterOption(BaseModel):
    """Option value for a parameter."""
    value: int
    label: str


class DataOption(BaseModel):
    """Option for data selection."""
    value: str
    label: str


class HeadersOption(BaseModel):
    """Option for headers selection."""
    value: str
    label: str


class ParameterInfo(BaseModel):
    """Parameter with options."""
    name: str
    description: str
    options: list[ParameterOption] = []


class AssertionMethodInfo(BaseModel):
    """Single assertion method info."""
    name: str
    description: str
    data_options: list[DataOption]
    parameters: list[ParameterInfo]


class AssertionClassGroup(BaseModel):
    """Group of methods under a class name."""
    name: str
    methods: list[AssertionMethodInfo]


class AssertionMethodsResponse(BaseModel):
    """Response model for listing assertion methods."""
    available: bool
    headers_options: list[HeadersOption] = []
    classes: list[AssertionClassGroup] = []
    total: int = 0


class FieldInfo(BaseModel):
    """Single field info."""
    name: str
    path: str
    is_time_field: bool
    description: str


class FieldGroup(BaseModel):
    """Group of fields under a category."""
    name: str
    fields: list[FieldInfo]


class AssertionFieldsResponse(BaseModel):
    """Response model for listing assertion fields."""
    available: bool
    error: str | None = None
    groups: list[FieldGroup] = []
    total: int = 0


class FieldResult(BaseModel):
    """Single field assertion result."""
    name: str
    expected: str
    actual: str
    passed: bool
    comparison_type: str | None = None
    description: str | None = None


class AssertionExecuteRequest(BaseModel):
    """Request model for executing an assertion method."""
    class_name: str
    method_name: str
    data: str = 'main'
    api_params: dict = {}
    field_params: dict = {}
    # Backward compatibility
    headers: str | None = 'main'
    params: dict = {}


class AssertionExecuteResponse(BaseModel):
    """Response model for assertion execution."""
    success: bool
    passed: bool
    duration: float
    fields: list[FieldResult] = []
    error: str | None = None
    error_type: str | None = None


@router.get("/methods", response_model=AssertionMethodsResponse)
async def list_assertion_methods():
    """List all available assertion methods.

    Returns 503 if external module is not available.
    """
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External assertion module not available",
                "reason": get_unavailable_reason(),
                "fix": "Ensure WEBSERP_PATH is configured in .env and config/settings.py exists in webseleniumerp"
            }
        )

    classes = get_assertion_methods_grouped()
    total = sum(len(c["methods"]) for c in classes)

    # Build headers options with labels
    headers_with_labels = [
        HeadersOption(value=h, label=HEADERS_LABELS.get(h, h))
        for h in HEADERS_OPTIONS
    ]

    return AssertionMethodsResponse(
        available=True,
        headers_options=headers_with_labels,
        classes=[AssertionClassGroup(**c) for c in classes],
        total=total
    )


@router.get("/fields", response_model=AssertionFieldsResponse)
async def list_assertion_fields():
    """List all available assertion fields.

    Returns 503 if external module is not available.
    """
    result = get_assertion_fields_grouped()

    if not result['available']:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External assertion fields not available",
                "reason": result.get('error', 'Unknown error'),
                "fix": "Ensure WEBSERP_PATH is configured in .env"
            }
        )

    return AssertionFieldsResponse(
        available=True,
        groups=[FieldGroup(**g) for g in result['groups']],
        total=result['total']
    )
