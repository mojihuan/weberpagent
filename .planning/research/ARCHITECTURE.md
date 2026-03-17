# Architecture Research

**Domain:** AI-Driven UI Testing Platform
**Researched:** 2026-03-17 (updated for v0.3)
**Confidence:** HIGH (based on comprehensive codebase analysis and established patterns)

## Executive Summary

The aiDriveUITest platform follows a clean layered architecture with event-driven real-time updates. The current implementation has a solid foundation but requires targeted restructuring to achieve v0.1 stability. Key issues include: database schema lacking assertions support, frontend-backend type mismatches, and inconsistent API response formats.

**Recommended approach:** Incremental refactoring preserving the core architecture while fixing data flow issues and adding missing components.

---

## NEW: External Precondition Module Integration (v0.3)

### Integration Question

**Question:** How should webseleniumerp project be integrated?

**Options evaluated:**
1. Add to PYTHONPATH and import
2. Import by file path using importlib
3. Copy required files
4. Create a bridge/adapter module

**Recommendation:** Option 1 (Add to PYTHONPATH) + Option 4 (Create Bridge Module)

### webseleniumerp Architecture Analysis

```
webseleniumerp-master/
+-- common/
|   +-- base_prerequisites.py   # PreFront class with operations() method
|   +-- base_api.py             # BaseApi with headers, caching, random mixins
|   +-- import_api.py           # Generated: ImportApi aggregates all API classes
|   +-- import_request.py       # Generated: ImportRequest aggregates request methods
|   +-- base_random_mixin.py    # Random data generation
|   +-- base_url.py             # URL configuration
|   +-- log.py                  # Logging
|   +-- file_cache.py           # File caching
+-- config/
|   +-- settings.py             # DATA_PATHS - NOT IN GIT (generated locally)
|   +-- user_info.py            # INFO dict with account details
|   +-- conftest.py             # Selenium webdriver setup
+-- api/                        # API endpoint wrappers
+-- request/                    # Request method implementations
+-- pages/                      # Page object models
+-- testcase/                   # Test cases
```

### Critical Dependency: config/settings.py

**WARNING:** `config/settings.py` is in `.gitignore` and NOT in the repository.

This file defines `DATA_PATHS` which is imported by:
- `common/base_api.py`
- `common/base_prerequisites.py`
- `common/base_case.py`
- And many more files

**Solution:** Create a minimal `config/settings.py` template:

```python
# webseleniumerp/config/settings.py - MUST BE CREATED LOCALLY
DATA_PATHS = {
    'performance': 'close',  # 'open' or 'close'
    'auto_type': 'api',      # 'ui' or 'api'
    'chrome_driver': '',     # Only needed for UI mode
}
```

### PreFront Class Structure

```python
# common/base_prerequisites.py
class PreFront(CommonFront):
    def operations(self, data=None):
        # Operation codes mapped to request methods
        # Example operation codes:
        # FA1 - 新增采购单未付款入库
        # FA2 - 新增采购单未付款在路上
        # HC1 - 库存移交销售
        # ... 100+ operation codes

        operations = {
            'FA1': [self.request.purchase_add.new_purchase_order_unpaid_warehouse],
            'FA2': [self.request.purchase_add.new_purchase_order_unpaid_journey],
            'HC1': [self.request.inventory_list.inventory_transfer_sell_main],
            # ... many more
        }

        for key in data:
            self.execute_operations(operations, key)
```

### Recommended Integration Architecture

```
+------------------------------------------------------------------+
|                        Frontend (React + TypeScript)              |
|  ┌─────────────────────────────────────────────────────────┐    |
|  │  PreconditionEditor                                      │    |
|  │  - Operation code selector (dropdown: FA1, HC1, ...)     │    |
|  │  - Selected codes stored as list in precondition config   │    |
|  └─────────────────────────────────────────────────────────┘    |
+-------|----------------------------------------------------------+
        | REST API: GET /api/external-operations
+-------|----------------------------------------------------------+
|                        Backend (FastAPI + Python)                 |
|  ┌─────────────────────────────────────────────────────────┐    |
|  │  NEW: ExternalPreconditionBridge                         │    |
|  │  - configure_external_path(WEBSERP_PATH)                 │    |
|  │  - load_pre_front_class() -> PreFront                    │    |
|  │  - get_available_operations() -> dict[code, description] │    |
|  │  - execute_operations(codes) -> result                   │    |
|  └─────────────────────────────────────────────────────────┘    |
|                              |                                    |
|  ┌────────-------------------|-------------------------┐        |
|  │  PreconditionService (existing)                    |        |
|  │  - external_module_path (ERP_API_MODULE_PATH)      |        |
|  │  - execute_single() uses exec()                    |        |
|  │  - Generated code imports and uses external modules|        |
|  └------------------------------------------------------        |
+-------|----------------------------------------------------------+
        | sys.path.insert(0, WEBSERP_PATH)
+-------|----------------------------------------------------------+
|                        External: webseleniumerp                    |
|  ┌─────────────────────────────────────────────────────────┐    |
|  │  common/base_prerequisites.py -> PreFront               │    |
|  │  config/settings.py (must be created)                   │    |
|  │  config/user_info.py -> INFO                            │    |
|  └─────────────────────────────────────────────────────────┘    |
+------------------------------------------------------------------+
```

### New Component: ExternalPreconditionBridge

```python
# backend/core/external_precondition_bridge.py
"""Bridge module for webseleniumerp integration"""

import sys
import logging
import inspect
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Module-level cache for loaded classes
_pre_front_class = None
_import_error = None


def configure_external_path(webe_erp_path: str) -> tuple[bool, str]:
    """Add webseleniumerp to sys.path if not already present.

    Args:
        webe_erp_path: Path to webseleniumerp project root

    Returns:
        (success, message)
    """
    path = Path(webe_erp_path)
    if not path.exists():
        return False, f"Path does not exist: {webe_erp_path}"
    if not path.is_dir():
        return False, f"Path is not a directory: {webe_erp_path}"

    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
        logger.info(f"Added webseleniumerp to sys.path: {path_str}")

    return True, f"Path configured: {webe_erp_path}"


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


def get_available_operations() -> dict[str, str]:
    """Get dictionary of available operation codes and their descriptions.

    Returns:
        Dict mapping operation codes (e.g., 'FA1') to descriptions
    """
    PreFront, error = load_pre_front_class()
    if error:
        return {}

    try:
        # Parse operation codes from the method source
        # The operations() method contains dict like: 'FA1': [self.request...]
        source = inspect.getsource(PreFront.operations)
        pattern = r"'([A-Z0-9@]+)':\s*\["
        matches = re.findall(pattern, source)

        # Map codes to Chinese descriptions (from comments in source)
        # This maps the operation codes to their human-readable descriptions
        descriptions = _parse_operation_descriptions(source)

        return {code: descriptions.get(code, code) for code in matches}
    except Exception as e:
        logger.error(f"Failed to get operations: {e}")
        return {}


def _parse_operation_descriptions(source: str) -> dict[str, str]:
    """Parse operation descriptions from source code comments."""
    # Extract comment lines like: # 配件管理|配件采购|新增采购
    # Then find the operation codes that follow
    descriptions = {}

    lines = source.split('\n')
    current_comment = ""

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') and not stripped.startswith('# '):
            # Module comment like: # 配件管理|配件采购|新增采购
            current_comment = stripped[1:].strip()
        elif "'" in stripped and "': [" in stripped:
            # Operation line like: 'FA1': [self.request...],
            match = re.search(r"'([A-Z0-9@]+)'", stripped)
            if match and current_comment:
                code = match.group(1)
                descriptions[code] = current_comment
                current_comment = ""

    return descriptions


def execute_operations(operation_codes: list[str]) -> tuple[bool, str, dict[str, Any]]:
    """Execute precondition operations.

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
```

### Generated Precondition Code Pattern

When user selects operation codes, generate code for PreconditionService:

```python
# This is what gets passed to PreconditionService.execute_single()
import sys
sys.path.insert(0, '/Users/huhu/project/webseleniumerp-master')

from common.base_prerequisites import PreFront

pre_front = PreFront()
pre_front.operations(['FA1', 'HC1'])

# Store result in context for later use
context['precondition_result'] = 'success'
```

### Configuration Requirements

```env
# .env
# Path to webseleniumerp project root
WEBSERP_PATH=/Users/huhu/project/webseleniumerp-master

# Existing config (for ERP API module)
ERP_API_MODULE_PATH=/path/to/erp/api/module
```

### API Endpoint Addition

```python
# backend/api/routes/external_operations.py (NEW)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.external_precondition_bridge import (
    configure_external_path,
    get_available_operations,
)

router = APIRouter(prefix="/external-operations", tags=["external-operations"])


class OperationsResponse(BaseModel):
    operations: dict[str, str]
    total: int


@router.get("", response_model=OperationsResponse)
async def list_operations():
    """List all available precondition operation codes."""
    operations = get_available_operations()
    if not operations:
        raise HTTPException(
            status_code=503,
            detail="External precondition module not configured or failed to load"
        )
    return OperationsResponse(operations=operations, total=len(operations))
```

### Anti-Patterns to Avoid for External Integration

#### Anti-Pattern 1: Direct Import Without Bridge

**BAD:**
```python
# Scattered throughout codebase
from common.base_prerequisites import PreFront
```

**Why bad:** No centralized error handling, hard to test, tight coupling.

**Instead:** Use the bridge module for all external imports.

#### Anti-Pattern 2: Copying Files

**BAD:** Copying files from webseleniumerp into weberpagent.

**Why bad:**
- Divergence: Changes to webseleniumerp won't be reflected
- Maintenance burden: Two codebases to maintain
- Import conflicts: May break internal imports

**Instead:** Import from the external project via sys.path.

#### Anti-Pattern 3: Ignoring the Missing settings.py

**BAD:** Assuming config/settings.py exists in the external project.

**Why bad:** It's in .gitignore and won't be present after cloning.

**Instead:** Create a setup script or document the required configuration.

### Integration Checklist

- [ ] Add `WEBSERP_PATH` to environment configuration
- [ ] Create `backend/core/external_precondition_bridge.py`
- [ ] Create `backend/api/routes/external_operations.py` endpoint
- [ ] Add `config/settings.py` template to webseleniumerp
- [ ] Update frontend to add operation code selector
- [ ] Document setup requirements in README

---

## Current Architecture Assessment

### System Overview (Current)

```
+-------------------------------------------------------------------------+
|                        PRESENTATION LAYER (React)                        |
+-------------------------------------------------------------------------+
|  +----------+  +----------+  +----------+  +----------+  +----------+  |
|  |Dashboard |  |  Tasks   |  |   Runs   |  | Reports  |  | Monitor  |  |
|  +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+-----+  |
|       |             |             |             |             |         |
|  +----+-------------+-------------+-------------+-------------+----+   |
|  |                    API Client + SSE Hook                         |   |
|  +-------------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
|                          API LAYER (FastAPI)                             |
+-------------------------------------------------------------------------+
|  +----------+  +----------+  +----------+  +----------+                 |
|  |  /tasks  |  |  /runs   |  |/reports  |  |/dashboard|                 |
|  +----+-----+  +----+-----+  +----+-----+  +----+-----+                 |
|       |             |             |             |                        |
+-------+-------------+-------------+-------------+------------------------+
|                         SERVICE LAYER                                    |
+-------------------------------------------------------------------------+
|  +---------------+  +----------------+  +-----------------+             |
|  | AgentService  |  |  EventManager  |  | PreconditionSvc |             |
|  | (browser-use) |  |  (SSE pub-sub) |  | (exec() runner) |             |
|  +-------+-------+  +-------+--------+  +-----------------+             |
|          |                  |                                           |
+----------+------------------+-------------------------------------------+
|                           DATA LAYER                                     |
+-------------------------------------------------------------------------+
|  +------------+  +------------+  +------------+  +------------+         |
|  |TaskRepo    |  |RunRepo     |  |StepRepo    |  |ReportRepo  |         |
|  +------+-----+  +------+-----+  +------+-----+  +------+-----+         |
|         +-------------+-------------+-------------+                      |
|                              |                                           |
|                    +---------+---------+                                 |
|                    |   SQLite + ORM    |                                 |
|                    +-------------------+                                 |
+-------------------------------------------------------------------------+
|                      EXTERNAL INTEGRATION                                |
+-------------------------------------------------------------------------+
|  +----------------+  +----------------+  +----------------+             |
|  | Browser-Use    |  |  LLM Provider  |  |   Playwright   |             |
|  | (Agent Engine) |  | (Qwen/OpenAI)  |  |   (Browser)    |             |
|  +----------------+  +----------------+  +----------------+             |
|  +----------------+                                                    |
|  | webseleniumerp |  <-- NEW: External precondition module              |
|  | (PreFront)     |                                                    |
|  +----------------+                                                    |
+-------------------------------------------------------------------------+
```

### Current Component Responsibilities

| Component | Responsibility | Status |
|-----------|----------------|--------|
| **Frontend Pages** | UI rendering, user interaction | Works but has type mismatches |
| **API Client** | HTTP communication, error handling | Functional, needs response transform |
| **useRunStream Hook** | SSE connection management | Works correctly |
| **FastAPI Routes** | Request handling, validation | Functional, inconsistent responses |
| **AgentService** | Browser-Use orchestration | Works correctly |
| **EventManager** | SSE pub-sub distribution | Works correctly |
| **PreconditionService** | Execute Python code via exec() | Works correctly |
| **Repositories** | Data access abstraction | Missing some methods |
| **LLM Factory** | LLM instance creation | Works, uses archived code |

## Identified Architecture Issues

### Issue 1: Database Schema Gaps

**Problem:** Current schema lacks:
- Assertion configuration (types: URL check, text exists, no errors)
- Assertion results per run/step
- Task configuration storage (target_url underutilized)

**Impact:** Assertions mentioned in requirements but no database support

**Fix:**
```sql
-- Add to schema
CREATE TABLE assertions (
    id TEXT PRIMARY KEY,
    task_id TEXT REFERENCES tasks(id),
    type TEXT NOT NULL,  -- url_check, text_exists, no_errors
    config JSON NOT NULL,
    enabled BOOLEAN DEFAULT true
);

CREATE TABLE assertion_results (
    id TEXT PRIMARY KEY,
    run_id TEXT REFERENCES runs(id),
    assertion_id TEXT REFERENCES assertions(id),
    passed BOOLEAN NOT NULL,
    actual_value TEXT,
    error_message TEXT
);
```

### Issue 2: Frontend-Backend Type Mismatch

**Problem:**
- Backend uses `step_index`, frontend expects `index`
- Backend uses `screenshot_path`, frontend expects `screenshot` URL
- Date formats inconsistent (ISO string vs datetime objects)

**Current Transform (frontend/src/api/reports.ts):**
```typescript
function transformStep(step: StepApiResponse): Step {
  return {
    index: step.step_index,        // Rename
    screenshot: step.screenshot_url || '',  // Transform
    // ...
  }
}
```

**Fix Options:**
1. **Backend-first (recommended):** Standardize backend response to match frontend expectations
2. **Frontend transform layer:** Keep current approach but document mapping explicitly

### Issue 3: Inconsistent API Response Format

**Problem:**
- Some endpoints return direct objects (`/tasks/{id}`)
- Others return wrapped objects (`/reports` returns `{reports: [], total: number}`)
- No consistent error response structure

**Recommended Standard:**
```typescript
// All list endpoints
interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}

// All single item endpoints
interface ItemResponse<T> {
  data: T;
}

// All errors
interface ErrorResponse {
  error: string;
  detail?: string;
  code?: string;
}
```

### Issue 4: Missing Run-Steps Relationship in Repository

**Problem:** `RunRepository` has `get_steps()` called but not defined

**Location:** `backend/api/routes/runs.py:141`
```python
steps = await run_repo.get_steps(run_id)  # Method doesn't exist
```

**Fix:** Add to RunRepository or use StepRepository

### Issue 5: Hardcoded API Base URL

**Problem:** `API_BASE = 'http://localhost:8080/api'` hardcoded in multiple frontend files

**Files affected:**
- `frontend/src/api/client.ts:1`
- `frontend/src/api/runs.ts:5`
- `frontend/src/hooks/useRunStream.ts:5`

**Fix:** Use environment variable
```typescript
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'
```

## Recommended Architecture (v0.1 Target)

### Target System Overview

```
+-------------------------------------------------------------------------+
|                        PRESENTATION LAYER (React)                        |
+-------------------------------------------------------------------------+
|  +------------------------------------------------------------------+   |
|  |                         Pages                                     |   |
|  |  Dashboard | Tasks | TaskDetail | RunMonitor | Reports | Report  |   |
|  +------------------------------------------------------------------+   |
|                              |                                           |
|  +------------------------------------------------------------------+   |
|  |                         Hooks                                     |   |
|  |  useTasks | useDashboard | useRunStream | useReports              |   |
|  +------------------------------------------------------------------+   |
|                              |                                           |
|  +------------------------------------------------------------------+   |
|  |                       API Layer                                   |   |
|  |  client.ts | tasks.ts | runs.ts | reports.ts | dashboard.ts       |   |
|  +------------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
|                          API LAYER (FastAPI)                             |
+-------------------------------------------------------------------------+
|  +------------------------------------------------------------------+   |
|  |                       Routes (backend/api/routes/)                |   |
|  |  tasks.py | runs.py | reports.py | dashboard.py | external_ops.py |   |
|  +------------------------------------------------------------------+   |
|                              |                                           |
|  +------------------------------------------------------------------+   |
|  |                       Schemas (backend/db/schemas.py)             |   |
|  |  Request/Response validation with Pydantic                        |   |
|  +------------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
|                         SERVICE LAYER                                    |
+-------------------------------------------------------------------------+
|  +-------------+  +-------------+  +-------------+  +-------------+    |
|  |AgentService |  |EventManager |  |PrecondSvc   |  |ReportService|    |
|  +-------------+  +-------------+  +-------------+  +-------------+    |
|  +-------------+  +-------------+                                     |
|  |ExternalPrec-|  |ApiAssertSvc |  <-- NEW/Updated for v0.3           |
|  |onditionBrdg |  |             |                                     |
|  +-------------+  +-------------+                                     |
+-------------------------------------------------------------------------+
|                           DATA LAYER                                     |
+-------------------------------------------------------------------------+
|  +------------------------------------------------------------------+   |
|  |              Repositories (backend/db/repository.py)              |   |
|  |  TaskRepo | RunRepo | StepRepo | ReportRepo | AssertionRepo       |   |
|  +------------------------------------------------------------------+   |
|                              |                                           |
|  +------------------------------------------------------------------+   |
|  |                  Models (backend/db/models.py)                    |   |
|  |  Task | Run | Step | Report | Assertion | AssertionResult         |   |
|  +------------------------------------------------------------------+   |
|                              |                                           |
|                    +---------+---------+                                 |
|                    |   SQLite + ORM    |                                 |
|                    +-------------------+                                 |
+-------------------------------------------------------------------------+
|                      EXTERNAL INTEGRATION                                |
+-------------------------------------------------------------------------+
|  +----------------+  +----------------+  +----------------+             |
|  | Browser-Use    |  |  LLM Provider  |  |   Playwright   |             |
|  | Agent Engine   |  | Qwen/OpenAI    |  |   Browser      |             |
|  +----------------+  +----------------+  +----------------+             |
|  +----------------+                                                    |
|  | webseleniumerp |  <-- External precondition module via sys.path     |
|  | (PreFront)     |                                                    |
|  +----------------+                                                    |
+-------------------------------------------------------------------------+
```

## Recommended Project Structure

### Backend Structure (Recommended)

```
backend/
+-- api/
|   +-- __init__.py
|   +-- main.py              # FastAPI app entry, middleware setup
|   +-- routes/
|   |   +-- __init__.py
|   |   +-- tasks.py         # Task CRUD endpoints
|   |   +-- runs.py          # Run execution endpoints
|   |   +-- reports.py       # Report endpoints
|   |   +-- dashboard.py     # Dashboard stats endpoints
|   |   +-- external_operations.py  # NEW: External precondition operations
|   +-- deps.py              # Dependency injection helpers (NEW)
+-- core/
|   +-- __init__.py
|   +-- agent_service.py     # Browser-Use orchestration
|   +-- event_manager.py     # SSE event management
|   +-- precondition_service.py  # Precondition execution (exec())
|   +-- external_precondition_bridge.py  # NEW: Bridge to webseleniumerp
|   +-- api_assertion_service.py  # API assertion execution
|   +-- report_service.py    # Report generation (NEW)
+-- db/
|   +-- __init__.py
|   +-- database.py          # SQLAlchemy async setup
|   +-- models.py            # ORM models
|   +-- schemas.py           # Pydantic schemas
|   +-- repository.py        # Data access layer
+-- llm/
|   +-- __init__.py
|   +-- base.py              # LLM interface
|   +-- factory.py           # LLM creation
|   +-- config.py            # LLM configuration
|   +-- openai.py            # OpenAI-compatible implementation
+-- config/
|   +-- __init__.py
|   +-- settings.py          # Environment config (NEW)
+-- tests/
|   +-- ...                  # Test files
+-- data/
    +-- database.db          # SQLite database
    +-- screenshots/         # Screenshot storage
```

### Frontend Structure (Recommended)

```
frontend/src/
+-- api/
|   +-- client.ts            # Base fetch wrapper, error handling
|   +-- tasks.ts             # Task API calls
|   +-- runs.ts              # Run API calls
|   +-- reports.ts           # Report API calls
|   +-- dashboard.ts         # Dashboard API calls
|   +-- external_operations.ts  # NEW: External operations API
|   +-- types.ts             # API response types (NEW)
+-- components/
|   +-- shared/              # Reusable components
|   +-- Dashboard/           # Dashboard-specific
|   +-- TaskList/            # Task list components
|   +-- TaskDetail/          # Task detail components
|   +-- TaskModal/           # Task form modal
|   +-- RunMonitor/          # Run monitoring components
|   +-- Report/              # Report components
|   +-- PreconditionEditor/  # NEW: Precondition editing with operation selector
+-- hooks/
|   +-- useTasks.ts          # Task queries (TanStack Query)
|   +-- useRunStream.ts      # SSE streaming hook
|   +-- useReports.ts        # Report queries
|   +-- useDashboard.ts      # Dashboard data
|   +-- useExternalOperations.ts  # NEW: External operations hook
+-- pages/
|   +-- Dashboard.tsx
|   +-- Tasks.tsx
|   +-- TaskDetail.tsx
|   +-- RunList.tsx
|   +-- RunMonitor.tsx
|   +-- Reports.tsx
|   +-- ReportDetail.tsx
+-- types/
|   +-- index.ts             # Domain types
+-- utils/
|   +-- transforms.ts        # API response transforms (NEW)
+-- config/
|   +-- env.ts               # Environment config (NEW)
+-- App.tsx
+-- main.tsx
```

### Structure Rationale

- **api/**: Separate API layer for clear data fetching boundaries
- **components/**: Feature-based organization with shared components
- **hooks/**: TanStack Query hooks abstract data fetching from UI
- **types/**: Central type definitions matching backend schemas
- **utils/transforms.ts**: Single location for API-to-domain mapping

## Data Flow Patterns

### Test Execution Flow

```
User Clicks "Run"
    |
    v
+-----------------+
|  Frontend       |  POST /api/runs?task_id=xxx
|  createRun()    |----------------------------+
+-----------------+                            |
                                               v
                        +----------------------+
                        |  FastAPI /runs       |
                        |  1. Create Run       |
                        |  2. Queue background |
                        |  3. Return RunResponse|
                        +----------+-----------+
                                   |
    +------------------------------+-----------------------------+
    |                    Background Task                          |
    |  +-------------------------------------------------------+  |
    |  |  1. Update Run status -> "running"                    |  |
    |  |  2. Publish SSE "started" event                       |  |
    |  |  3. Execute preconditions (if configured)             |  |
    |  |     - ExternalPreconditionBridge.execute_operations() |  |
    |  |     - Or exec() user-provided code                    |  |
    |  |  4. Create Browser-Use Agent with LLM                 |  |
    |  |  5. For each step:                                    |  |
    |  |     a. Agent executes action                          |  |
    |  |     b. Callback captures action/reasoning/screenshot  |  |
    |  |     c. Save Step to database                          |  |
    |  |     d. Publish SSE "step" event                       |  |
    |  |  6. Execute API assertions (if configured)            |  |
    |  |  7. Update Run status -> "success"/"failed"           |  |
    |  |  8. Create Report                                     |  |
    |  |  9. Publish SSE "finished" event                      |  |
    |  +-------------------------------------------------------+  |
    +--------------------------------------------------------------+
                                   |
                                   v
                        +----------------------+
                        |  Frontend SSE        |
                        |  useRunStream        |
                        |  Real-time UI updates|
                        +----------------------+
```

### State Management Pattern

```
+-----------------------------------------------------------------+
|                    React Query Cache                             |
|  +-----------+  +-----------+  +-----------+  +-----------+   |
|  |  tasks    |  |   runs    |  |  reports  |  | dashboard |   |
|  +-----+-----+  +-----+-----+  +-----+-----+  +-----+-----+   |
+-------|--------------|--------------|--------------|-----------+
        |              |              |              |
        v              v              v              v
+-----------------------------------------------------------------+
|                      Hooks Layer                                 |
|  useTasks()   useRunStream()  useReports()  useDashboard()      |
|  useExternalOperations()  <-- NEW                              |
+-----------------------------------------------------------------+
        |              |              |              |
        v              v              v              v
+-----------------------------------------------------------------+
|                      Components                                  |
|  Pages consume hooks, react to state changes automatically      |
+-----------------------------------------------------------------+
```

## Key Architectural Patterns

### Pattern 1: Repository Pattern for Data Access

**What:** Abstract database operations behind repository interfaces

**When to use:** Always - isolates business logic from data access

**Implementation:**
```python
# backend/db/repository.py
class RunRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_id: str) -> Run:
        run = Run(task_id=task_id, status="pending")
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_with_steps(self, run_id: str) -> Optional[Run]:
        """NEW: Get run with all steps loaded"""
        stmt = select(Run).where(Run.id == run_id).options(
            selectinload(Run.steps)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
```

### Pattern 2: SSE Event Manager (Pub-Sub)

**What:** In-memory event distribution for real-time updates

**When to use:** Real-time status updates from background tasks

**Current Implementation (works well):**
```python
# backend/core/event_manager.py
class EventManager:
    def __init__(self):
        self._events: dict[str, list[str]] = defaultdict(list)
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)

    async def publish(self, run_id: str, event: str | None):
        if event:
            self._events[run_id].append(event)
        for queue in self._subscribers.get(run_id, []):
            await queue.put(event)

    async def subscribe(self, run_id: str) -> AsyncGenerator[str, None]:
        queue = asyncio.Queue()
        self._subscribers[run_id].append(queue)
        # Replay history first
        for event in self._events.get(run_id, []):
            yield event
        # Then stream new events
        while True:
            event = await queue.get()
            yield event
            if event is None:
                break
```

**Trade-offs:**
- (+) Simple, no external dependencies
- (+) History replay for reconnection
- (-) Memory grows with concurrent runs
- (-) Lost on server restart (acceptable for v0.1)

### Pattern 3: Background Tasks with FastAPI

**What:** Use FastAPI BackgroundTasks for async execution

**When to use:** Long-running operations (AI agent execution)

**Implementation:**
```python
# backend/api/routes/runs.py
@router.post("", response_model=RunResponse)
async def create_run(
    task_id: str,
    background_tasks: BackgroundTasks,
    task_repo: TaskRepository = Depends(get_task_repo),
    run_repo: RunRepository = Depends(get_run_repo),
):
    task = await task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    run = await run_repo.create(task_id=task_id)

    # Queue background execution
    background_tasks.add_task(
        run_agent_background,
        run.id,
        task.name,
        task.description,
        task.max_steps,
    )

    return run  # Return immediately, execution continues in background
```

### Pattern 4: Type Transformation Layer

**What:** Transform API responses to frontend domain types

**When to use:** Backend naming conventions differ from frontend expectations

**Implementation:**
```typescript
// frontend/src/utils/transforms.ts
export function transformStep(api: StepApiResponse): Step {
  return {
    index: api.step_index,
    action: api.action,
    reasoning: api.reasoning,
    screenshot: api.screenshot_url
      ? `${API_BASE}${api.screenshot_url}`
      : '',
    status: api.status as 'success' | 'failed',
    error: api.error || undefined,
    duration_ms: api.duration_ms,
  }
}
```

### Pattern 5: Bridge Module for External Dependencies (NEW)

**What:** Create a dedicated bridge module to isolate external project imports

**When to use:** Integrating external Python projects that aren't installable packages

**Implementation:**
```python
# backend/core/external_precondition_bridge.py
# See full implementation in the v0.3 section above
```

**Trade-offs:**
- (+) Centralized error handling for import failures
- (+) Caching of loaded classes for performance
- (+) Clear interface for type hints
- (+) Easy to mock for testing
- (-) Additional layer of indirection

## Anti-Patterns to Avoid

### Anti-Pattern 1: Direct Database Access in Routes

**What people do:**
```python
@router.get("/runs/{run_id}")
async def get_run(run_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Run).where(Run.id == run_id))
    return result.scalar_one_or_none()
```

**Why it's wrong:**
- Business logic leaks into route handlers
- Hard to test, hard to reuse
- No single source of truth for queries

**Do this instead:**
```python
@router.get("/runs/{run_id}")
async def get_run(
    run_id: str,
    run_repo: RunRepository = Depends(get_run_repo),
):
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
```

### Anti-Pattern 2: Hardcoded URLs and Configuration

**What people do:**
```typescript
const response = await fetch('http://localhost:8080/api/tasks')
```

**Why it's wrong:**
- Breaks in production
- No environment-specific configuration
- Scattered magic values

**Do this instead:**
```typescript
// frontend/src/config/env.ts
export const config = {
  apiBase: import.meta.env.VITE_API_BASE || 'http://localhost:8080/api',
}

// frontend/src/api/client.ts
import { config } from '../config/env'

export async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${config.apiBase}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  // ...
}
```

### Anti-Pattern 3: Inconsistent Error Handling

**What people do:**
```python
# Sometimes HTTPException
raise HTTPException(status_code=404, detail="Not found")

# Sometimes return error dict
return {"error": "Not found"}

# Sometimes let exception propagate
```

**Why it's wrong:**
- Frontend can't handle errors consistently
- Mixed response formats

**Do this instead:**
```python
# Always use HTTPException with consistent format
from fastapi import HTTPException

@router.get("/runs/{run_id}")
async def get_run(run_id: str, run_repo: RunRepository = Depends(get_run_repo)):
    run = await run_repo.get(run_id)
    if not run:
        raise HTTPException(
            status_code=404,
            detail={"error": "RUN_NOT_FOUND", "message": f"Run {run_id} not found"}
        )
    return run
```

### Anti-Pattern 4: Missing Database Migrations

**What people do:** Modify models.py and manually alter SQLite

**Why it's wrong:**
- No version control for schema changes
- Can't rollback
- Team members have inconsistent schemas

**Do this instead:**
```bash
# Add Alembic for v0.2+
alembic init migrations
alembic revision --autogenerate -m "Add assertions tables"
alembic upgrade head
```

**Note:** For v0.1, since SQLite allows schema flexibility, we can add tables without migrations. Plan for Alembic in v0.2.

## Database Schema Recommendations

### Current Schema (Keep)

```python
# backend/db/models.py - EXISTING
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str]  # 8-char UUID
    name: Mapped[str]
    description: Mapped[str]
    target_url: Mapped[str]  # Currently underutilized
    max_steps: Mapped[int]
    status: Mapped[str]  # draft, ready
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    runs: Mapped[List["Run"]]

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str]
    task_id: Mapped[str]
    status: Mapped[str]  # pending, running, success, failed, stopped
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]
    created_at: Mapped[datetime]
    steps: Mapped[List["Step"]]

class Step(Base):
    __tablename__ = "steps"
    id: Mapped[str]
    run_id: Mapped[str]
    step_index: Mapped[int]
    action: Mapped[str]
    reasoning: Mapped[str | None]
    screenshot_path: Mapped[str | None]
    status: Mapped[str]
    error: Mapped[str | None]
    duration_ms: Mapped[int | None]

class Report(Base):
    __tablename__ = "reports"
    id: Mapped[str]
    run_id: Mapped[str]
    task_id: Mapped[str]
    task_name: Mapped[str]
    status: Mapped[str]
    total_steps: Mapped[int]
    success_steps: Mapped[int]
    failed_steps: Mapped[int]
    duration_ms: Mapped[int]
```

### Recommended Additions (v0.1)

```python
# NEW: Assertion configuration per task
class Assertion(Base):
    __tablename__ = "assertions"
    id: Mapped[str]
    task_id: Mapped[str]  # FK to tasks
    type: Mapped[str]  # url_check, text_exists, no_errors, custom
    config: Mapped[str]  # JSON string with type-specific config
    enabled: Mapped[bool] = True
    created_at: Mapped[datetime]

    # Relationships
    task: Mapped["Task"] = relationship(back_populates="assertions")

# NEW: Assertion results per run
class AssertionResult(Base):
    __tablename__ = "assertion_results"
    id: Mapped[str]
    run_id: Mapped[str]  # FK to runs
    assertion_id: Mapped[str]  # FK to assertions
    passed: Mapped[bool]
    actual_value: Mapped[str | None]
    error_message: Mapped[str | None]
    created_at: Mapped[datetime]

    # Relationships
    run: Mapped["Run"] = relationship(back_populates="assertion_results")
    assertion: Mapped["Assertion"] = relationship()
```

### Repository Methods to Add

```python
# Add to RunRepository
async def get_steps(self, run_id: str) -> List[Step]:
    """Get all steps for a run"""
    stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
    result = await self.session.execute(stmt)
    return list(result.scalars())

async def get_with_steps(self, run_id: str) -> Optional[Run]:
    """Get run with steps loaded"""
    stmt = select(Run).where(Run.id == run_id).options(selectinload(Run.steps))
    result = await self.session.execute(stmt)
    return result.scalar_one_or_none()

# Add TaskRepository for assertions
async def get_assertions(self, task_id: str) -> List[Assertion]:
    """Get all assertions for a task"""
    stmt = select(Assertion).where(Assertion.task_id == task_id, Assertion.enabled == True)
    result = await self.session.execute(stmt)
    return list(result.scalars())
```

## Build Order for v0.3 External Precondition Integration

Based on dependency analysis, recommended implementation order:

### Phase 1: Configuration (Day 1)
1. **Add WEBSERP_PATH to environment** - Backend `config/settings.py`
2. **Create config/settings.py template for webseleniumerp** - Document required setup

### Phase 2: Backend Bridge (Day 1-2)
3. **Create ExternalPreconditionBridge** - `backend/core/external_precondition_bridge.py`
4. **Add API endpoint** - `backend/api/routes/external_operations.py`
5. **Wire into PreconditionService** - Generate code that uses bridge

### Phase 3: Frontend Integration (Day 2-3)
6. **Add useExternalOperations hook** - Fetch available operations
7. **Create OperationCodeSelector component** - Dropdown with operation codes
8. **Update PreconditionEditor** - Add operation code selector UI
9. **Test end-to-end flow** - Select operations, run test

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| **0-10 concurrent users** | Current architecture is sufficient. SQLite handles this load. |
| **10-100 concurrent users** | Add connection pooling, consider PostgreSQL migration. |
| **100+ concurrent users** | Move SSE to Redis pub/sub, add load balancer, separate services. |

### Scaling Priorities

1. **First bottleneck:** SQLite write concurrency
   - **Fix:** Migrate to PostgreSQL with connection pool

2. **Second bottleneck:** EventManager memory
   - **Fix:** Move to Redis pub/sub for event distribution

3. **Third bottleneck:** Screenshot storage
   - **Fix:** Move to S3/MinIO object storage

**Note:** v0.1 targets single-user local development. Scaling considerations are for v0.2+.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **Browser-Use** | Python library import | Core agent engine, well-isolated |
| **Qwen/OpenAI LLM** | HTTP via OpenAI SDK | Compatible API, configure via env |
| **Playwright** | Browser-Use dependency | Automatic browser management |
| **webseleniumerp** | sys.path + Bridge module | External precondition module (v0.3) |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Frontend <-> API | REST + SSE | Keep REST synchronous, SSE for streaming |
| API <-> Services | Direct function calls | Services are stateless, injected |
| Services <-> Repositories | Async method calls | All DB access through repositories |
| Services <-> External | Async HTTP | LLM calls are the main external dependency |
| Bridge <-> webseleniumerp | sys.path + import | External project loaded dynamically |

## Sources

- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices) - HIGH confidence
- [Async APIs with FastAPI: Patterns, Pitfalls & Best Practices](https://shiladityamajumder.medium.com/async-apis-with-fastapi-patterns-pitfalls-best-practices-2d72b2b66f25) - HIGH confidence
- [Real-Time Streaming with FastAPI](https://medium.com/@bhagyarana80/real-time-streaming-with-fastapi-simply-90287fe2228b) - HIGH confidence
- [FastAPI Patterns for Real-Time APIs](https://medium.com/@hadiyolworld007/fastapi-patterns-for-real-time-apis-a169aac97b44) - MEDIUM confidence
- Browser-Use Documentation - HIGH confidence (from codebase analysis)
- SQLAlchemy 2.0 Async Documentation - HIGH confidence
- webseleniumerp source code analysis - HIGH confidence (direct code review)

---

*Architecture research for: AI-Driven UI Testing Platform*
*Researched: 2026-03-17 (updated for v0.3 external precondition integration)*
