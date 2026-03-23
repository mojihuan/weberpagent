# Phase 23: Backend Assertion Discovery - Research

**Researched:** 2026-03-20
**Domain:** Python introspection, external module discovery, API endpoint design
**Confidence:** HIGH (existing patterns from Phase 17, codebase analysis complete)

## Summary

Phase 23 implements a discovery API that scans `webseleniumerp/common/base_assertions.py` and exposes assertion methods via `GET /external-assertions/methods`. The implementation follows the exact pattern established in Phase 17 for data method discovery (`/external-data-methods`).

Key findings:
1. **Reuse existing bridge pattern** - The `external_precondition_bridge.py` already has all necessary infrastructure (lazy loading, caching, method discovery). We add assertion-specific functions alongside existing data method functions.
2. **Assertion method structure** - All assertion methods follow a consistent signature: `def xxx_assert(self, headers=None, data='main', **kwargs)` with a `methods` dictionary mapping data options to API methods.
3. **Headers are fixed** - The `headers` parameter accepts a fixed set of identifiers: `main`, `idle`, `vice`, `special`, `platform`, `super`, `camera`. These map to actual authentication tokens at execution time (Phase 25).
4. **Data options extraction** - Parse the `methods` dictionary from source code to extract available `data` parameter options (`main`, `a`, `b`, etc.).
5. **i/j/k parameter parsing** - Extend existing `_parse_docstring_params()` to also extract option values (e.g., `i: 订单状态 1待发货 2待取件`).

**Primary recommendation:** Extend `external_precondition_bridge.py` with assertion loading functions following the exact pattern as data method functions.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**data parameter discovery strategy**
- **Parse method**: Scan method source code, extract `methods = {...}` dictionary keys
- **Implementation**: Use `inspect.getsource()` + regex matching `methods = \{[^}]+\}` to extract key names
- **Example**: `methods = {'main': ..., 'a': ..., 'b': ...}` -> extract `['main', 'a', 'b']`
- **Cache**: Cache together with method signature

**headers parameter handling**
- **Phase 23 responsibility**: Only return available identifier list `['main', 'idle', 'vice', 'special', 'platform', 'super', 'camera']`
- **Token resolution**: Deferred to Phase 25 execution, handled by ExternalAssertionBridge calling ImportApi.headers
- **Hardcoded list**: headers identifiers are fixed, no discovery from external modules needed

**i/j/k parameter parsing depth**
- **Full parsing**: Parse option descriptions from docstring into structured data
- **Parse format**: `i: 订单状态 1待发货 2待取件` ->
  ```json
  {
    "name": "i",
    "description": "订单状态",
    "options": [
      {"value": 1, "label": "待发货"},
      {"value": 2, "label": "待取件"}
    ]
  }
  ```
- **Regex pattern**: `(\d+)([^\d]+)` match digit + description combinations

**error handling strategy**
- **WEBSERP_PATH not configured**: Return HTTP 503 Service Unavailable + clear error message
- **External module load failure**: HTTP 503 + detailed error (missing file/import error)
- **Response format**:
  ```json
  {
    "detail": "WEBSERP_PATH not configured. Set WEBSERP_PATH in .env file."
  }
  ```

**API response structure**
- **Reuse Phase 17 format**: Consistent with `/external-data-methods` structure
- **Response example**:
  ```json
  {
    "available": true,
    "headers_options": ["main", "idle", "vice", "special", "platform", "super", "camera"],
    "classes": [
      {
        "name": "PcAssert",
        "methods": [
          {
            "name": "attachment_inventory_list_assert",
            "description": "配件管理|配件库存|库存列表",
            "data_options": ["main", "a", "b"],
            "parameters": [
              {"name": "i", "description": "库存状态", "options": [{"value": 2, "label": "库存中"}, {"value": 1, "label": "待入库"}]}
            ]
          }
        ]
      }
    ],
    "total": 83
  }
  ```

**cache strategy**
- **Method signature**: Cache at startup, subsequent requests return cached result
- **Refresh mechanism**: Requires application restart to refresh method list (consistent with Phase 17)
- **No refresh endpoint**: Keep backend simple

**search/filter functionality**
- **Backend does not implement search**: Returns all classes and methods, frontend implements search/filter
- **No filtering by class name**: Returns all PcAssert/MgAssert/McAssert classes
- **80+ methods all returned**: Frontend can group by class name + search box filtering

### Claude's Discretion

- Bridge module specific file location (extend existing `external_precondition_bridge.py` or create new file)
- `data` parameter parsing regex implementation details
- `i/j/k` option value parsing edge cases (e.g., when no option description present)
- Internal method filtering rules (e.g., `get_handle_response` and similar methods should not be exposed)

### Deferred Ideas (OUT OF SCOPE)

- Frontend assertion selector component - Phase 24
- Headers identifier to actual token resolution - Phase 25
- Assertion execution engine - Phase 25
- Assertion results stored in context - Phase 25
- E2E testing - Phase 26
- Unit test coverage - Phase 27
- Cache refresh endpoint - Future optimization
- Search/filter by class name/method name - Frontend implementation
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DISC-01 | System scans base_assertions.py for PcAssert/MgAssert/McAssert assertion methods | `load_base_assertions_class()` function + `discover_class_methods()` pattern from existing bridge |
| DISC-02 | Assertion methods grouped by class name (PcAssert ~80, MgAssert 1, McAssert 2) | `get_assertion_methods_grouped()` following `get_data_methods_grouped()` pattern |
| DISC-03 | Extract `data` parameter options (main/a/b/c etc.) as dropdown | `_parse_data_options_from_source()` - new function using regex to extract `methods` dict keys |
| DISC-04 | Parse method docstring for `i/j/k` parameter descriptions and options | Extend `_parse_docstring_params()` to parse option values using `(\d+)([^\d]+)` pattern |
| DISC-05 | Provide API endpoint `GET /external-assertions/methods` | New route file `external_assertions.py` following `external_data_methods.py` pattern |
</phase_requirements>

## Standard Stack

### Core (No New Dependencies)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| inspect | stdlib | Introspection for method discovery | Already used in bridge module |
| re | stdlib | Regex for parsing methods dict and options | Already used in bridge module |
| FastAPI | 0.135.1+ | REST API framework | Existing backend framework |
| Pydantic | 2.4.0+ | Response models | Already used in routes |

### Supporting (Existing - Reuse)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| asyncio | stdlib | Async execution wrapper | For timeout-protected execution (Phase 25) |
| logging | stdlib | Error logging | Already used throughout bridge |

### No New Packages Required

All functionality uses Python standard library and existing project dependencies. The assertion discovery reuses the exact same infrastructure as data method discovery from Phase 17.

**Installation:**
No new packages needed. All dependencies already installed.

## Architecture Patterns

### Recommended Project Structure

```
backend/
  core/
    external_precondition_bridge.py   # EXTEND: Add assertion loading functions
  api/
    routes/
      external_assertions.py          # NEW: Assertion discovery API route
      external_data_methods.py        # EXISTING: Reference pattern
```

### Pattern 1: Lazy Class Loading with Caching

**What:** Load external classes lazily and cache for subsequent calls

**When to use:** All external module imports (PreFront, BaseImport,Assert classes)

**Example:**
```python
# Source: backend/core/external_precondition_bridge.py (existing pattern)
_assertion_classes_cache: dict[str, type] | None = None
_assertion_import_error: str | None = None

def load_base_assertions_class() -> tuple[type | None, str | None]:
    """Load assertion classes lazily.

    Returns:
        (class_or_none, error_or_none)
    """
    global _assertion_classes_cache, _assertion_import_error

    if _assertion_classes_cache is not None:
        return _assertion_classes_cache, None

    if _assertion_import_error is not None:
        return None, _assertion_import_error

    # Configure path from settings if not already done
    if not _path_configured:
        from backend.config import get_settings
        settings = get_settings()
        if settings.weberp_path:
            success, msg = configure_external_path(settings.weberp_path)
            if not success:
                _assertion_import_error = msg
                return None, _assertion_import_error

    try:
        from common.base_assertions import PcAssert, MgAssert, McAssert
        _assertion_classes_cache = {
            'PcAssert': PcAssert,
            'MgAssert': MgAssert,
            'McAssert': McAssert
        }
        logger.info("Successfully loaded assertion classes")
        return _assertion_classes_cache, None
    except ImportError as e:
        _assertion_import_error = (
            f"Failed to import assertion classes: {e}. "
            f"Ensure config/settings.py exists in webseleniumerp."
        )
        logger.error(_assertion_import_error)
        return None, _assertion_import_error
    except Exception as e:
        _assertion_import_error = f"Unexpected error loading assertion classes: {e}"
        logger.error(_assertion_import_error, exc_info=True)
        return None, _assertion_import_error
```

### Pattern 2: Source Code Parsing for Data Options

**What:** Extract `methods` dictionary keys from method source code

**When to use:** When discovering available `data` parameter options

**Example:**
```python
# Source: NEW - backend/core/external_precondition_bridge.py
def _parse_data_options_from_source(method) -> list[str]:
    """Extract data options from method source code.

    Parses the methods = {...} dictionary to extract available keys.

    Args:
        method: The method to parse

    Returns:
        List of available data options (e.g., ['main', 'a', 'b'])
    """
    try:
        source = inspect.getsource(method)
    except (OSError, TypeError):
        return ['main']  # Default fallback

    # Find methods = {...} pattern
    match = re.search(r"methods\s*=\s*\{([^}]+)\}", source, re.DOTALL)
    if not match:
        return ['main']

    methods_dict_str = match.group(1)

    # Extract quoted keys from the dictionary
    keys = re.findall(r"['\"](\w+)['\"]\s*:", methods_dict_str)
    return keys if keys else ['main']
```

### Pattern 3: Extended Docstring Parsing for Options

**What:** Parse i/j/k parameter options from docstrings

**When to use:** When discovering parameter options with value labels

**Example:**
```python
# Source: Extended from existing _parse_docstring_params()
def _parse_param_options(description: str) -> list[dict]:
    """Parse option values from parameter description.

    Parses formats like:
        i: 订单状态 1待发货 2待取件
        j: 物品状态 13待销售 3待分货

    Returns:
        List of option dicts: [{"value": 1, "label": "待发货"}, ...]
    """
    options = []

    # Pattern: digit followed by non-digit text
    # Matches: "1待发货" -> (1, "待发货")
    pattern = r'(\d+)([^\d]+)'

    for match in re.finditer(pattern, description):
        value = int(match.group(1))
        label = match.group(2).strip()
        if label:
            options.append({"value": value, "label": label})

    return options
```

### Pattern 4: API Route with 503 Handling

**What:** Return 503 Service Unavailable when external module not configured

**When to use:** All external module API endpoints

**Example:**
```python
# Source: backend/api/routes/external_assertions.py (based on external_data_methods.py)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.core.external_precondition_bridge import (
    is_available,
    get_unavailable_reason,
    get_assertion_methods_grouped,
)


router = APIRouter(prefix="/external-assertions", tags=["external-assertions"])


class ParameterOption(BaseModel):
    """Option value for a parameter."""
    value: int
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
    data_options: list[str]
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
        headers_options=["main", "idle", "vice", "special", "platform", "super", "camera"],
        classes=[AssertionClassGroup(**c) for c in classes],
        total=total
    )
```

### Anti-Patterns to Avoid

- **Direct import without bridge**: `from common.base_assertions import PcAssert` scattered in code
  - Why bad: No centralized error handling, hard to test, tight coupling
  - Use bridge module for all external imports

- **Assuming settings.py exists**: The `config/settings.py` in webseleniumerp is in `.gitignore`
  - Why bad: Import will fail silently without clear error message
  - Check availability first, return 503 with clear fix instructions

- **Parsing methods dict with eval()**: Using `eval()` to parse the dictionary
  - Why bad: Security risk, can execute arbitrary code
  - Use regex to extract keys safely

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Lazy loading with caching | Custom singleton pattern | Existing `load_base_params_class()` pattern | Already tested, handles errors |
| Method discovery | Custom reflection code | Existing `discover_class_methods()` | Already handles private method filtering |
| Docstring parsing | Custom parser | Existing `_parse_docstring_params()` + extend | Handles Chinese colon, existing pattern |
| API error responses | Custom error format | Existing 503 pattern from `external_data_methods.py` | Consistent frontend error handling |

**Key insight:** The assertion discovery is a nearly identical use case to data method discovery. Copy the existing patterns, extend only where needed (data options parsing, parameter options).

## Common Pitfalls

### Pitfall 1: Missing config/settings.py in External Project

**What goes wrong:** Import fails with cryptic `ImportError: No module named 'config.settings'`

**Why it happens:** `webseleniumerp/config/settings.py` is in `.gitignore` and must be created locally

**How to avoid:**
1. Check import availability in `is_available()`
2. Return clear error message: "Ensure config/settings.py exists in webseleniumerp"
3. Include fix suggestion in 503 response

**Warning signs:**
- Generic "External module not available" without specific cause
- Users cannot diagnose the issue

### Pitfall 2: Data Options Defaulting to Empty List

**What goes wrong:** Frontend dropdown shows no options when source parsing fails

**Why it happens:** Regex fails to match, method has no `methods` dictionary, or `inspect.getsource()` fails

**How to avoid:**
1. Always return `['main']` as default (every assertion method has at least 'main')
2. Log warning when regex fails
3. Test with various method structures

**Warning signs:**
- Empty dropdown in frontend
- Assertion execution fails with "不支持的方法"

### Pitfall 3: Internal Methods Exposed in API

**What goes wrong:** Methods like `_get_cached_api`, `_call_module_api` appear in API response

**Why it happens:** Only checking `if name.startswith('_')` misses inherited internal methods

**How to avoid:**
1. Extend `INTERNAL_METHODS` set in `extract_method_info()`
2. Add: `_get_cached_api`, `_call_module_api`, `assert_time`, `assert_contains`, `assert_equal`
3. Filter by checking both name pattern and method origin

**Warning signs:**
- API returns 90+ methods instead of expected 83
- Frontend shows internal utility methods

### Pitfall 4: Option Parsing Fails on Complex Descriptions

**What goes wrong:** Parameter options not parsed when description has unusual format

**Why it happens:** Regex `(\d+)([^\d]+)` assumes simple digit+text pattern

**How to avoid:**
1. Handle edge cases: no options, only description
2. Return empty options list when parsing fails (not an error)
3. Support both Chinese `:` and English `:` colon

**Warning signs:**
- Options dropdown empty when it should have values
- Inconsistent option parsing across methods

### Pitfall 5: Cache Not Cleared Between Tests

**What goes wrong:** Tests pass in isolation but fail when run together due to stale cache

**Why it happens:** Module-level singletons persist across test runs

**How to avoid:**
1. Call `reset_cache()` in test fixtures
2. Add assertion-specific reset in `reset_cache()`
3. Document that server restart is needed for production cache clear

**Warning signs:**
- Tests pass individually but fail in suite
- Method list doesn't update after external module changes

## Code Examples

### Complete Assertion Method Info Extraction

```python
# Source: backend/core/external_precondition_bridge.py (extended)
def extract_assertion_method_info(cls: type, method_name: str) -> dict | None:
    """Extract assertion method information including data options and parameters.

    Args:
        cls: The class containing the method
        method_name: Name of the method to extract info from

    Returns:
        dict with name, description, data_options, and parameters, or None for filtered methods
    """
    # Skip private methods
    if method_name.startswith('_'):
        return None

    # Skip internal utility methods from BaseModuleAssert/BaseAssert
    INTERNAL_ASSERTION_METHODS = {
        '_get_cached_api', '_call_module_api',
        'assert_time', 'assert_contains', 'assert_equal', '_get_field_value',
        '_assert_api_response'  # Internal method in BaseAssert
    }
    if method_name in INTERNAL_ASSERTION_METHODS:
        return None

    method = getattr(cls, method_name, None)
    if method is None:
        return None

    # Extract description from docstring (first line)
    docstring = method.__doc__ or ""
    description = docstring.strip().split('\n')[0] if docstring.strip() else method_name

    # Extract data options from source code
    data_options = _parse_data_options_from_source(method)

    # Parse parameters from docstring (i/j/k with options)
    parameters = _parse_docstring_params_with_options(docstring)

    return {
        "name": method_name,
        "description": description,
        "data_options": data_options,
        "parameters": parameters
    }


def _parse_docstring_params_with_options(docstring: str) -> list[dict]:
    """Parse parameter definitions with options from docstring.

    Handles format like:
        i: 订单状态 1待发货 2待取件
        j: 物品状态 13待销售 3待分货

    Returns:
        List of parameter dicts with name, description, and options
    """
    params = []
    if not docstring:
        return params

    lines = docstring.strip().split('\n')
    for line in lines[1:]:  # Skip first line (method description)
        line = line.strip()
        if not line:
            continue

        # Match pattern: "param_name: description" or "param_name： description"
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[：:]\s*(.+)$', line)
        if match:
            param_name = match.group(1)
            param_desc = match.group(2).strip()

            # Parse options from description
            options = _parse_param_options(param_desc)

            # If options found, extract just the description part
            if options:
                # Remove option patterns from description
                clean_desc = re.sub(r'\d+[^\d]+', '', param_desc).strip()
            else:
                clean_desc = param_desc

            params.append({
                "name": param_name,
                "description": clean_desc,
                "options": options
            })

    return params
```

### Complete API Route File

```python
# Source: backend/api/routes/external_assertions.py (NEW FILE)
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


class ParameterOption(BaseModel):
    """Option value for a parameter."""
    value: int
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
    data_options: list[str]
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
        headers_options=["main", "idle", "vice", "special", "platform", "super", "camera"],
        classes=[AssertionClassGroup(**c) for c in classes],
        total=total
    )
```

### Registering the Route in main.py

```python
# Source: backend/api/main.py (add to existing imports and includes)
from backend.api.routes import external_assertions

app.include_router(external_assertions.router, prefix="/api")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom assertion discovery | Reuse data method pattern | Phase 23 | 50% less code, proven patterns |
| Parse full methods dict with eval | Regex extraction of keys | Phase 23 | Safer parsing, no code execution |
| Hardcode data options | Parse from source code | Phase 23 | Dynamic discovery, always accurate |
| Separate error responses | Consistent 503 with fix hint | Phase 23 | Better UX, easier debugging |

**Deprecated/outdated:**
- `eval()` for parsing: Use regex instead for security
- Hardcoded method lists: Use introspection for accuracy

## Open Questions

1. **Should `get_handle_response` and similar inherited methods be filtered?**
   - What we know: These are defined in `BaseApi` and inherited by assertion classes
   - What's unclear: Whether they could be called as assertions (unlikely based on naming)
   - Recommendation: Add to `INTERNAL_METHODS` set, filter by naming convention

2. **What if a method has no docstring for i/j/k parameters?**
   - What we know: Most methods have docstrings, but some may not
   - What's unclear: How to handle missing parameter documentation
   - Recommendation: Return empty parameters list (not an error), frontend can show generic input

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/unit/test_external_precondition_bridge.py -x -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DISC-01 | Scan base_assertions.py for assertion methods | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_load_assertion_classes -xvs` | Wave 0 |
| DISC-02 | Group methods by class name | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_get_assertion_methods_grouped -xvs` | Wave 0 |
| DISC-03 | Extract data parameter options | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_parse_data_options -xvs` | Wave 0 |
| DISC-04 | Parse i/j/k parameter descriptions | unit | `uv run pytest backend/tests/unit/test_external_assertion_bridge.py::test_parse_param_options -xvs` | Wave 0 |
| DISC-05 | API endpoint returns assertion methods | integration | `uv run pytest backend/tests/api/test_external_assertions_api.py -xvs` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_external_assertion_bridge.py -x`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_external_assertion_bridge.py` - Unit tests for assertion discovery functions
- [ ] `backend/tests/api/test_external_assertions_api.py` - Integration tests for API endpoint
- [ ] Extend `reset_cache()` in bridge module to clear assertion caches

*(If no gaps: "None - existing test infrastructure covers all phase requirements")*

## Sources

### Primary (HIGH confidence)
- `/Users/huhu/project/weberpagent/backend/core/external_precondition_bridge.py` - Existing pattern for lazy loading, caching, method discovery
- `/Users/huhu/project/weberpagent/backend/api/routes/external_data_methods.py` - API route pattern, 503 handling, response models
- `/Users/huhu/project/webseleniumerp-master/common/base_assertions.py` - Assertion class structure (PcAssert, MgAssert, McAssert)
- `/Users/huhu/project/webseleniumerp-master/common/base_assert.py` - BaseAssert base class with utility methods

### Secondary (MEDIUM confidence)
- `.planning/research/ARCHITECTURE.md` - Bridge module pattern, integration architecture
- `.planning/research/PITFALLS.md` - Assertion integration pitfalls A1-A5
- `.planning/research/STACK.md` - Assertion method structure, execution flow

### Tertiary (LOW confidence)
- None - All research based on direct codebase analysis

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new dependencies, existing patterns
- Architecture: HIGH - Follows Phase 17 pattern exactly
- Pitfalls: HIGH - Documented in PITFALLS.md with specific scenarios

**Research date:** 2026-03-20
**Valid until:** 30 days (stable patterns, no external API changes expected)
