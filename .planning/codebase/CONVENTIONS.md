# Coding Conventions

**Analysis Date:** 2026-04-03

## Programming Languages

**Backend (Python):**
- Python 3.11+
- Type hints used throughout
- Async/await patterns for I/O operations
- Immutability preferred (return new objects, never mutate)

**Frontend (TypeScript/React):**
- TypeScript with strict mode
- React 19 with functional components
- Hooks-based architecture

## Naming Patterns

### Python Backend

**Files:**
- Snake case: `agent_service.py`, `event_manager.py`, `run_logger.py`
- Descriptive names indicating purpose

**Classes:**
- PascalCase: `MonitoredAgent`, `AgentService`, `StallDetector`
- PascalCase: `PreSubmitGuard`, `TaskProgressTracker`, `ContextWrapper`

**Functions/Methods:**
- snake_case: `create_llm`, `run_with_streaming`, `execute_single`
- `async def` for async functions
- Action-oriented names

**Variables:**
- snake_case: `run_id`, `llm_config`, `step_index`, `target_url`
- Descriptive and clear

**Constants:**
- SCREAMING_SNAKE_CASE: `SERVER_BROWSER_ARGS`, `RETRYABLE_ERRORS`

### Frontend TypeScript

**Files:**
- PascalCase for components: `RunMonitor.tsx`, `StepTimeline.tsx`
- camelCase for utilities: `useSSE.ts`, `useTasks.ts`

**Interfaces/Types:**
- PascalCase: `Task`, `Run`, `Step`, `TimelineItem`
- Optional properties marked with `?`

**React Components:**
- PascalCase: `RunMonitor`, `StepTimeline`
- Props interface with `Props` suffix when needed

## Code Style

### Python

**Line Length:**
- Maximum 100 characters (Ruff configuration)

**Imports:**
```python
# Standard library
import asyncio
import json
import logging
from typing import Any, Callable

# Third-party
from fastapi import APIRouter, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

# Local modules
from backend.core.agent_service import AgentService
from backend.agent.monitored_agent import MonitoredAgent
```

**Type Hints:**
```python
async def run_with_streaming(
    self,
    task: str,
    run_id: str,
    on_step: Callable[[int, str, str, str | None], Any],
    max_steps: int = 10,
    llm_config: dict | None = None,
    target_url: str | None = None,
) -> Any:
```

### TypeScript

**Imports:**
```typescript
import { useState, useEffect } from 'react'
import type { Task, Run, Step } from '../types'
import { tasksApi } from '../api/tasks'
```

## Immutability Patterns

**CRITICAL: Always return new objects, never mutate:**

```python
# WRONG: Mutation
def update_status(run, new_status):
    run.status = new_status  # MUTATION!
    return run

# CORRECT: Return new object
def update_status(run, new_status):
    return {
        **run,
        status: new_status
    }
```

**Frozen dataclasses for detector results:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class StallResult:
    should_intervene: bool
    message: str
```

## Error Handling

**Python:**
```python
logger = logging.getLogger(__name__)

try:
    result = await precondition_service.execute_single(code, i)
except asyncio.TimeoutError:
    result.error = f"执行超时（超过 {timeout} 秒）"
except SyntaxError as e:
    result.error = f"语法错误: {e.msg} (行 {e.lineno})"
except Exception as e:
    result.error = f"执行错误: {str(e)}"
```

**Fault-tolerant detectors:**
```python
# Detectors wrapped in try/except for non-blocking behavior
try:
    stall_result = self._stall_detector.check(...)
    if stall_result.should_intervene:
        self._pending_interventions.append(stall_result.message)
except Exception as e:
    logger.error(f"[monitor] Detector error (non-blocking): {e}")
```

## Input Validation

**Pydantic Models:**
```python
class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    max_steps: int = Field(default=10, ge=1, le=100)
```

## Function Design

**Size:** < 50 lines typical, < 100 lines max
**Parameters:** < 6 parameters, use config objects if more needed
**Return Values:** Always return explicit values

## Module Design

**Backend:**
- `backend/api/routes/` - HTTP endpoints
- `backend/core/` - Business logic services
- `backend/agent/` - Agent/detector implementations
- `backend/db/` - Data access layer
- `backend/utils/` - Utilities

**Plugin Pattern for Detectors:**
```python
class MonitoredAgent(Agent):
    def __init__(
        self,
        *,
        stall_detector: StallDetector | None = None,
        pre_submit_guard: PreSubmitGuard | None = None,
        task_progress_tracker: TaskProgressTracker | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._stall_detector = stall_detector or StallDetector()
        # ...
```

## Comments

**Chinese comments for business logic:**
```python
# 前置条件执行结束
# === External Assertions End ===
```

**Docstrings for public APIs:**
```python
async def run_with_streaming(
    self,
    task: str,
    run_id: str,
    on_step: Callable,
    max_steps: int = 10,
    llm_config: dict | None = None,
    target_url: str | None = None,
) -> Any:
    """Execute task with streaming callback.

    Args:
        task: Natural language task description
        run_id: Execution ID for logging
        on_step: Async callback for step updates
        max_steps: Maximum execution steps
        llm_config: LLM configuration
        target_url: Target URL to navigate to before execution
    """
```

---

*Convention analysis: 2026-04-03*
