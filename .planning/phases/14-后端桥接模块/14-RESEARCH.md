# Phase 14: 后端桥接模块 - Research

**Researched:** 2026-03-17
**Domain:** External Module Integration / Python Bridge Pattern
**Confidence:** HIGH

## Summary

This phase creates the `ExternalPreconditionBridge` module that isolates all external project (webseleniumerp) imports and provides a clean API for operation code discovery and execution. The bridge uses `inspect.getsource` to parse operation codes at startup, caches them in memory, and provides both a REST API endpoint and integration hooks for the existing `PreconditionService`.

**Primary recommendation:** Use a singleton bridge module in `backend/core/external_precondition_bridge.py` that handles path configuration, source parsing, and operation execution. Return HTTP 503 with clear error messages when external module is not configured.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Parsing method**: Use `inspect.getsource` to parse `PreFront.operations()` method source code
- **Extracted content**: Operation codes (e.g., 'FA1', 'HC1') + module comments (e.g., '#配件管理|配件采购')
- **Caching strategy**: Load once at application startup and cache in memory; subsequent requests return cached results
- **Refresh mechanism**: Application restart required to refresh operation codes (acceptable tradeoff)
- **Integration approach**: `PreconditionService` directly calls bridge module's `execute_operations()` method
- **Generated code template**:
  ```python
  import sys
  sys.path.insert(0, '<WEBSERP_PATH>')

  from common.base_prerequisites import PreFront

  pre_front = PreFront()
  pre_front.operations(['FA1', 'HC1'])

  context['precondition_result'] = 'success'
  ```
- **Error response**: Return HTTP 503 Service Unavailable with clear error message

### Claude's Discretion
- Bridge module file location (`backend/core/` or `backend/services/`)
- Regex implementation details for source parsing
- Module grouping hierarchy (whether to support multi-level grouping)
- Whether to add operation code search/filter functionality

### Deferred Ideas (OUT OF SCOPE)
- Frontend operation code selector component - Phase 15
- Operation code search/filter functionality - Phase 15
- End-to-end validation testing - Phase 16
- Operation execution caching (avoid duplicate executions) - Future optimization

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| BRIDGE-01 | Create ExternalPreconditionBridge module to isolate external project imports | Bridge module pattern with lazy loading and error handling |
| BRIDGE-02 | Implement get_available_operations() returning operation code list with descriptions | Use `inspect.getsource` + regex parsing for operation codes |
| BRIDGE-03 | Provide `/api/external-operations` API endpoint | FastAPI router with Pydantic response model |
| BRIDGE-04 | Implement operation code execution integrated with PreconditionService | Bridge exposes `execute_operations()` callable |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python inspect | stdlib | Source code introspection | Native, no dependencies |
| Python re | stdlib | Regex pattern matching | Native, efficient for parsing |
| sys.path | stdlib | Dynamic module path management | Standard Python import mechanism |

### Supporting (Project Existing)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| FastAPI | 0.100+ | REST API endpoints | Creating `/api/external-operations` |
| Pydantic | 2.x | Request/Response models | Response schema validation |
| logging | stdlib | Error/warning logging | All bridge operations |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| inspect.getsource | importlib + AST | inspect simpler, AST more robust for complex parsing |
| Regex parsing | Full AST parsing | Regex sufficient for this use case, AST overkill |
| Runtime import | Static file read | Runtime import validates module actually works |

**No additional installation required** - all dependencies are Python stdlib or existing project dependencies.

## Architecture Patterns

### Recommended Project Structure

```
backend/
+-- core/
|   +-- external_precondition_bridge.py  # NEW: Bridge module (this phase)
|   +-- precondition_service.py          # Existing: Will integrate with bridge
+-- api/
|   +-- routes/
|   |   +-- external_operations.py       # NEW: REST API endpoint
+-- config/
|   +-- settings.py                      # Existing: Has weberp_path field
|   +-- validators.py                    # Existing: Has validate_weberp_path
```

### Pattern 1: Singleton Bridge with Lazy Loading

**What:** Module-level singleton that loads external class on first access

**When to use:** External module loading that may fail and needs caching

**Example:**
```python
# backend/core/external_precondition_bridge.py
import sys
import logging
import inspect
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Module-level cache (singleton state)
_pre_front_class = None
_import_error = None
_operations_cache: dict[str, str] | None = None
_modules_cache: list[dict] | None = None


def configure_external_path(weberp_path: str) -> tuple[bool, str]:
    """Add webseleniumerp to sys.path if not already present."""
    path = Path(weberp_path)
    if not path.exists():
        return False, f"Path does not exist: {weberp_path}"
    if not path.is_dir():
        return False, f"Path is not a directory: {weberp_path}"

    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
        logger.info(f"Added webseleniumerp to sys.path: {path_str}")

    return True, f"Path configured: {weberp_path}"


def load_pre_front_class() -> tuple[type | None, str | None]:
    """Load PreFront class from webseleniumerp.

    Returns:
        (class_or_none, error_or_none)
    """
    global _pre_front_class, _import_error

    if _pre_front_class is not None:
        return _pre_front_class, None

    if _import_error is not None:
        return None, _import_error

    try:
        from common.base_prerequisites import PreFront
        _pre_front_class = PreFront
        logger.info("Successfully loaded PreFront class")
        return _pre_front_class, None
    except ImportError as e:
        _import_error = f"Failed to import PreFront: {e}"
        logger.error(_import_error)
        return None, _import_error
    except Exception as e:
        _import_error = f"Unexpected error loading PreFront: {e}"
        logger.error(_import_error, exc_info=True)
        return None, _import_error


def is_available() -> bool:
    """Check if external module is available."""
    cls, err = load_pre_front_class()
    return cls is not None


def get_unavailable_reason() -> str | None:
    """Get reason why external module is unavailable."""
    cls, err = load_pre_front_class()
    if cls is not None:
        return None
    return err or "External module not configured"
```

### Pattern 2: Source Code Parsing for Operation Discovery

**What:** Use `inspect.getsource` to read method source, parse with regex

**When to use:** Discover available operations without executing code

**Example:**
```python
# Source: Python stdlib inspect module
# Pattern: r"'([A-Z0-9@]+)':\s*\["

def _parse_operations_from_source() -> tuple[dict[str, str], list[dict]]:
    """Parse operation codes and module groupings from source.

    Returns:
        (operations_dict, modules_list)
    """
    global _operations_cache, _modules_cache

    if _operations_cache is not None and _modules_cache is not None:
        return _operations_cache, _modules_cache

    PreFront, error = load_pre_front_class()
    if error:
        _operations_cache = {}
        _modules_cache = []
        return _operations_cache, _modules_cache

    try:
        source = inspect.getsource(PreFront.operations)
    except (OSError, TypeError) as e:
        logger.error(f"Failed to get source: {e}")
        _operations_cache = {}
        _modules_cache = []
        return _operations_cache, _modules_cache

    operations = {}
    modules_dict: dict[str, list] = {}  # module_name -> operations

    lines = source.split('\n')
    current_module = "未分组"

    for line in lines:
        stripped = line.strip()

        # Parse module comments: # 配件管理|配件采购|新增采购
        if stripped.startswith('#') and '|' in stripped:
            parts = stripped[1:].strip().split('|')
            if len(parts) >= 2:
                current_module = f"{parts[0]} - {parts[1]}"
            elif len(parts) == 1:
                current_module = parts[0]

        # Parse operation codes: 'FA1': [self.request...]
        elif "'" in stripped and "': [" in stripped:
            match = re.search(r"'([A-Z0-9@]+)'", stripped)
            if match:
                code = match.group(1)
                # Extract description from comment or use code
                desc_match = re.search(r"#\s*(.+)$", stripped)
                description = desc_match.group(1) if desc_match else code
                operations[code] = description

                # Add to module grouping
                if current_module not in modules_dict:
                    modules_dict[current_module] = []
                modules_dict[current_module].append({
                    "code": code,
                    "description": description
                })

    _operations_cache = operations
    _modules_cache = [
        {"name": name, "operations": ops}
        for name, ops in modules_dict.items()
    ]

    return _operations_cache, _modules_cache


def get_available_operations() -> dict[str, str]:
    """Get dictionary of available operation codes and descriptions."""
    operations, _ = _parse_operations_from_source()
    return operations


def get_operations_grouped() -> list[dict]:
    """Get operations grouped by module."""
    _, modules = _parse_operations_from_source()
    return modules
```

### Pattern 3: API Response Schema

**What:** Pydantic models for consistent API responses

**Example:**
```python
# backend/api/routes/external_operations.py
from pydantic import BaseModel
from typing import Optional

class OperationItem(BaseModel):
    code: str
    description: str

class ModuleGroup(BaseModel):
    name: str
    operations: list[OperationItem]

class OperationsResponse(BaseModel):
    available: bool
    modules: list[ModuleGroup] = []
    total: int = 0
    error: Optional[str] = None

class ExecuteRequest(BaseModel):
    operation_codes: list[str]

class ExecuteResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None
```

### Pattern 4: FastAPI Route with 503 Response

**What:** Return HTTP 503 when external module unavailable

**Example:**
```python
# backend/api/routes/external_operations.py
from fastapi import APIRouter, HTTPException

from backend.core.external_precondition_bridge import (
    is_available,
    get_unavailable_reason,
    get_operations_grouped,
)

router = APIRouter(prefix="/external-operations", tags=["external-operations"])


@router.get("", response_model=OperationsResponse)
async def list_operations():
    """List all available precondition operation codes."""
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External precondition module not available",
                "reason": get_unavailable_reason(),
                "fix": "Ensure WEBSERP_PATH is configured in .env and the path is valid"
            }
        )

    modules = get_operations_grouped()
    total = sum(len(m["operations"]) for m in modules)

    return OperationsResponse(
        available=True,
        modules=[ModuleGroup(**m) for m in modules],
        total=total
    )
```

### Anti-Patterns to Avoid

- **Direct Import Without Bridge**: Never import from `common.base_prerequisites` outside the bridge module. This creates tight coupling and scattered error handling.
- **Executing External Code at Import Time**: Do not execute `PreFront()` at module load - only load the class. Instantiate only when executing operations.
- **Ignoring Missing config/settings.py**: The external project requires `config/settings.py` which is in `.gitignore`. Document this requirement clearly.
- **Assuming sys.path Persistence**: sys.path modifications should be idempotent - check before adding.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Source code parsing | Custom tokenizer | `inspect.getsource` + `re` | stdlib, well-tested, handles edge cases |
| Module caching | Custom cache dict | Module-level globals | Python module singleton pattern is sufficient |
| Path validation | Custom file checks | `pathlib.Path.exists()` | Cross-platform, handles edge cases |
| API error responses | Custom error dict | HTTPException + Pydantic | FastAPI standard pattern |

**Key insight:** The bridge pattern is simple - isolate imports, cache results, handle errors. Do not over-engineer.

## Common Pitfalls

### Pitfall 1: Circular Import on Bridge Import
**What goes wrong:** Importing bridge in multiple places at startup causes circular dependencies
**Why it happens:** Bridge imports settings, other modules import bridge
**How to avoid:** Bridge should only import from `config.settings` via `get_settings()` at function call time, not at module level
**Warning signs:** `ImportError: cannot import name 'X' from partially initialized module`

### Pitfall 2: Missing External config/settings.py
**What goes wrong:** ImportError when loading PreFront because config/settings.py doesn't exist
**Why it happens:** The file is in `.gitignore` of the external project
**How to avoid:** Bridge should catch ImportError and return clear message: "Create config/settings.py in webseleniumerp with DATA_PATHS configuration"
**Warning signs:** `ModuleNotFoundError: No module named 'config.settings'`

### Pitfall 3: Stale Cache After External Module Update
**What goes wrong:** New operation codes not visible after updating webseleniumerp
**Why it happens:** Operations cached at startup, not refreshed
**How to avoid:** Document that application restart is required; add `/api/external-operations/refresh` endpoint if needed in future
**Warning signs:** Operation code shown in external project but not in API response

### Pitfall 4: sys.path Pollution
**What goes wrong:** Adding path multiple times, path order issues
**Why it happens:** Calling `configure_external_path` multiple times
**How to avoid:** Always check `if path_str not in sys.path` before inserting
**Warning signs:** Unexpected import behavior, wrong module loaded

### Pitfall 5: Regex Not Matching All Operation Codes
**What goes wrong:** Some operation codes not parsed correctly
**Why it happens:** Edge cases in source formatting (e.g., '@1' codes, multi-line definitions)
**How to avoid:** Test regex against actual source; handle '@' prefix in pattern: `r"'([A-Z0-9@]+)':\s*\["`
**Warning signs:** Total count doesn't match expected

## Code Examples

### Bridge Module Full Template

```python
# backend/core/external_precondition_bridge.py
"""Bridge module for webseleniumerp integration.

This module isolates all external project imports and provides
a clean API for operation code discovery and execution.
"""

import sys
import logging
import inspect
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Module-level singleton state
_pre_front_class = None
_import_error = None
_operations_cache: dict[str, str] | None = None
_modules_cache: list[dict] | None = None
_path_configured = False


def configure_external_path(weberp_path: str | None) -> tuple[bool, str]:
    """Configure external module path.

    Args:
        weberp_path: Path to webseleniumerp project root

    Returns:
        (success, message)
    """
    global _path_configured

    if not weberp_path:
        return True, "WEBSERP_PATH not configured (optional feature)"

    path = Path(weberp_path)
    if not path.exists():
        return False, f"WEBSERP_PATH does not exist: {weberp_path}"
    if not path.is_dir():
        return False, f"WEBSERP_PATH is not a directory: {weberp_path}"

    path_str = str(path.resolve())
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
        logger.info(f"Added to sys.path: {path_str}")

    _path_configured = True
    return True, f"Path configured: {weberp_path}"


def load_pre_front_class() -> tuple[type | None, str | None]:
    """Load PreFront class lazily.

    Returns:
        (class_or_none, error_or_none)
    """
    global _pre_front_class, _import_error

    if _pre_front_class is not None:
        return _pre_front_class, None

    if _import_error is not None:
        return None, _import_error

    try:
        from common.base_prerequisites import PreFront
        _pre_front_class = PreFront
        logger.info("Successfully loaded PreFront class")
        return _pre_front_class, None
    except ImportError as e:
        _import_error = f"Failed to import PreFront: {e}. " \
                       f"Ensure config/settings.py exists in webseleniumerp."
        logger.error(_import_error)
        return None, _import_error
    except Exception as e:
        _import_error = f"Unexpected error loading PreFront: {e}"
        logger.error(_import_error, exc_info=True)
        return None, _import_error


def is_available() -> bool:
    """Check if external module is available."""
    cls, _ = load_pre_front_class()
    return cls is not None


def get_unavailable_reason() -> str | None:
    """Get reason why external module is unavailable."""
    cls, err = load_pre_front_class()
    if cls is not None:
        return None
    return err or "External module not configured"


def _parse_operations_from_source() -> tuple[dict[str, str], list[dict]]:
    """Parse operations from source code."""
    global _operations_cache, _modules_cache

    if _operations_cache is not None and _modules_cache is not None:
        return _operations_cache, _modules_cache

    PreFront, error = load_pre_front_class()
    if error:
        _operations_cache = {}
        _modules_cache = []
        return _operations_cache, _modules_cache

    try:
        source = inspect.getsource(PreFront.operations)
    except (OSError, TypeError) as e:
        logger.error(f"Failed to get source: {e}")
        _operations_cache = {}
        _modules_cache = []
        return _operations_cache, _modules_cache

    operations = {}
    modules_dict: dict[str, list] = {}

    lines = source.split('\n')
    current_module = "未分组"

    for line in lines:
        stripped = line.strip()

        # Module comment: # 配件管理|配件采购|新增采购
        if stripped.startswith('#') and '|' in stripped:
            parts = stripped[1:].strip().split('|')
            if len(parts) >= 2:
                current_module = f"{parts[0]} - {parts[1]}"
            else:
                current_module = parts[0] if parts else "未分组"

        # Operation code: 'FA1': [self.request...]
        elif "'" in stripped and "': [" in stripped:
            match = re.search(r"'([A-Z0-9@]+)'", stripped)
            if match:
                code = match.group(1)
                desc_match = re.search(r"#\s*(.+)$", stripped)
                description = desc_match.group(1) if desc_match else code
                operations[code] = description

                if current_module not in modules_dict:
                    modules_dict[current_module] = []
                modules_dict[current_module].append({
                    "code": code,
                    "description": description
                })

    _operations_cache = operations
    _modules_cache = [
        {"name": name, "operations": ops}
        for name, ops in modules_dict.items()
    ]

    return _operations_cache, _modules_cache


def get_available_operations() -> dict[str, str]:
    """Get all available operation codes with descriptions."""
    operations, _ = _parse_operations_from_source()
    return operations


def get_operations_grouped() -> list[dict]:
    """Get operations grouped by module."""
    _, modules = _parse_operations_from_source()
    return modules


def generate_precondition_code(operation_codes: list[str], weberp_path: str) -> str:
    """Generate precondition code for selected operation codes.

    Args:
        operation_codes: List of operation codes to execute
        weberp_path: Path to webseleniumerp for sys.path

    Returns:
        Python code string for PreconditionService
    """
    codes_str = ", ".join(f"'{c}'" for c in operation_codes)
    return f'''import sys
sys.path.insert(0, '{weberp_path}')

from common.base_prerequisites import PreFront

pre_front = PreFront()
pre_front.operations([{codes_str}])

context['precondition_result'] = 'success'
'''


def execute_operations(operation_codes: list[str]) -> tuple[bool, str, dict[str, Any]]:
    """Execute precondition operations directly.

    Args:
        operation_codes: List of operation codes to execute

    Returns:
        (success, message, context_data)
    """
    PreFront, error = load_pre_front_class()
    if error:
        return False, error, {}

    try:
        pre_front = PreFront()
        pre_front.operations(operation_codes)
        return True, f"Executed operations: {operation_codes}", {}
    except Exception as e:
        logger.error(f"Failed to execute operations: {e}", exc_info=True)
        return False, str(e), {}


def reset_cache():
    """Reset all cached data (for testing)."""
    global _pre_front_class, _import_error, _operations_cache, _modules_cache, _path_configured
    _pre_front_class = None
    _import_error = None
    _operations_cache = None
    _modules_cache = None
    _path_configured = False
```

### API Route Template

```python
# backend/api/routes/external_operations.py
"""External operations API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.config import get_settings
from backend.core.external_precondition_bridge import (
    is_available,
    get_unavailable_reason,
    get_operations_grouped,
    generate_precondition_code,
)

router = APIRouter(prefix="/external-operations", tags=["external-operations"])


class OperationItem(BaseModel):
    code: str
    description: str


class ModuleGroup(BaseModel):
    name: str
    operations: list[OperationItem]


class OperationsResponse(BaseModel):
    available: bool
    modules: list[ModuleGroup] = []
    total: int = 0
    error: Optional[str] = None


class GenerateRequest(BaseModel):
    operation_codes: list[str]


class GenerateResponse(BaseModel):
    code: str


@router.get("", response_model=OperationsResponse)
async def list_operations():
    """List all available precondition operation codes.

    Returns 503 if external module is not available.
    """
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External precondition module not available",
                "reason": get_unavailable_reason(),
                "fix": "Ensure WEBSERP_PATH is configured in .env and config/settings.py exists in webseleniumerp"
            }
        )

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
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail=get_unavailable_reason()
        )

    settings = get_settings()
    if not settings.weberp_path:
        raise HTTPException(
            status_code=503,
            detail="WEBSERP_PATH not configured"
        )

    code = generate_precondition_code(request.operation_codes, settings.weberp_path)
    return GenerateResponse(code=code)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Import external modules directly | Bridge module pattern | v0.3 | Isolated imports, centralized error handling |
| Execute code to discover operations | Parse source with inspect | v0.3 | Safer, no side effects |
| No caching | Startup caching | v0.3 | Faster responses |

**Deprecated/outdated:**
- None for this phase (new feature)

## Open Questions

1. **Should bridge be in `backend/core/` or `backend/services/`?**
   - Current pattern: `backend/core/` contains service-like modules (PreconditionService, AgentService)
   - Recommendation: Use `backend/core/external_precondition_bridge.py` for consistency

2. **Should we support multi-level module grouping?**
   - Source format: `# 配件管理|配件采购|新增采购` (3 levels)
   - Current plan: Flatten to 2 levels `配件管理 - 配件采购`
   - Alternative: Support nested structure if frontend needs it
   - Recommendation: Start with 2-level grouping, extend if needed

3. **Should generated code include context variable assignment?**
   - Yes - `context['precondition_result'] = 'success'` helps subsequent steps verify precondition ran
   - Already locked in CONTEXT.md

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest + pytest-asyncio |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/unit/test_external_precondition_bridge.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| BRIDGE-01 | Bridge module isolates external imports | unit | `pytest tests/unit/test_external_bridge.py::test_isolate_imports -v` | Wave 0 |
| BRIDGE-01 | Lazy loading with caching | unit | `pytest tests/unit/test_external_bridge.py::test_lazy_loading -v` | Wave 0 |
| BRIDGE-02 | Parse operation codes from source | unit | `pytest tests/unit/test_external_bridge.py::test_parse_operations -v` | Wave 0 |
| BRIDGE-02 | Group operations by module | unit | `pytest tests/unit/test_external_bridge.py::test_grouped_operations -v` | Wave 0 |
| BRIDGE-03 | API returns operations | integration | `pytest tests/integration/test_external_operations_api.py::test_list_operations -v` | Wave 0 |
| BRIDGE-03 | API returns 503 when unavailable | integration | `pytest tests/integration/test_external_operations_api.py::test_503_when_unavailable -v` | Wave 0 |
| BRIDGE-04 | Generate precondition code | unit | `pytest tests/unit/test_external_bridge.py::test_generate_code -v` | Wave 0 |
| BRIDGE-04 | Execute operations | unit | `pytest tests/unit/test_external_bridge.py::test_execute_operations -v` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_external_precondition_bridge.py -v`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** Full test suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_external_precondition_bridge.py` - Unit tests for bridge module
- [ ] `backend/tests/integration/test_external_operations_api.py` - API endpoint tests
- [ ] Mock PreFront class for testing without external dependency

*(If no gaps: "None - existing test infrastructure covers all phase requirements")*

## Sources

### Primary (HIGH confidence)
- Python stdlib `inspect` module - Source introspection
- Python stdlib `re` module - Regex parsing
- `.planning/research/ARCHITECTURE.md` - ExternalPreconditionBridge design
- `backend/core/precondition_service.py` - Integration pattern reference
- `backend/api/routes/runs.py` - API route pattern reference

### Secondary (MEDIUM confidence)
- `.planning/phases/14-后端桥接模块/14-CONTEXT.md` - User decisions and constraints
- `backend/config/settings.py` - Configuration pattern reference
- `backend/db/schemas.py` - Pydantic response model patterns

### Tertiary (LOW confidence)
- None - All findings verified against codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All Python stdlib, no external dependencies
- Architecture: HIGH - Based on existing project patterns and ARCHITECTURE.md
- Pitfalls: HIGH - Common Python import and caching patterns

**Research date:** 2026-03-17
**Valid until:** 90 days (stable Python patterns)
