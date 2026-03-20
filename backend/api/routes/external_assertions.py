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
)


router = APIRouter(prefix="/external-assertions", tags=["external-assertions"])

# Fixed headers identifiers (mapped to actual tokens at execution time)
HEADERS_OPTIONS = ["main", "idle", "vice", "special", "platform", "super", "camera"]


class ParameterOption(BaseModel):
    """Option value for a parameter."""
    value: int
    label: str


class DataOption(BaseModel):
    """Option for data selection."""
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
    headers_options: list[str] = []
    classes: list[AssertionClassGroup] = []
    total: int = 0


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

    return AssertionMethodsResponse(
        available=True,
        headers_options=HEADERS_OPTIONS,
        classes=[AssertionClassGroup(**c) for c in classes],
        total=total
    )
