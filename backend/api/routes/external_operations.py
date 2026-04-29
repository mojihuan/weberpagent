"""External operations API routes.

Provides REST API for discovering available precondition operation codes
from external webseleniumerp project.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.config import get_settings
from backend.core.external_precondition_bridge import (
    require_external_available,
    get_operations_grouped,
    generate_precondition_code,
)


router = APIRouter(prefix="/external-operations", tags=["external-operations"])


# Pydantic response models
class OperationItem(BaseModel):
    """Single operation code with description."""
    code: str
    description: str


class ModuleGroup(BaseModel):
    """Group of operations under a module name."""
    name: str
    operations: list[OperationItem]


class OperationsResponse(BaseModel):
    """Response model for listing available operations."""
    available: bool
    modules: list[ModuleGroup] = []
    total: int = 0
    error: Optional[str] = None


class GenerateRequest(BaseModel):
    """Request model for generating precondition code."""
    operation_codes: list[str]


class GenerateResponse(BaseModel):
    """Response model for generated precondition code."""
    code: str


@router.get("", response_model=OperationsResponse)
async def list_operations():
    """List all available precondition operation codes.

    Returns 503 if external module is not available.
    """
    require_external_available()

    modules = get_operations_grouped()
    total = sum(len(m["operations"]) for m in modules)

    return OperationsResponse(
        available=True,
        modules=[ModuleGroup(**m) for m in modules],
        total=total
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """Generate precondition code for selected operation codes."""
    require_external_available()

    settings = get_settings()
    if not settings.weberp_path:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "WEBSERP_PATH not configured",
                "fix": "Add WEBSERP_PATH to your .env file"
            }
        )

    code = generate_precondition_code(request.operation_codes, settings.weberp_path)
    return GenerateResponse(code=code)
