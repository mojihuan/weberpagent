# Coding Conventions

**Analysis Date:** 2026-03-14

## Programming Languages

**Backend (Python):**
- Python 3.11+ (ES2022 equivalent)
- Type hints used throughout
- Async/await patterns for I/O operations

**Frontend (TypeScript/React):**
- TypeScript with strict mode
- React 18 with functional components
- Hooks-based architecture

## Naming Patterns

### Python Backend

**Files:**
- Snake case: `agent_service.py`, `database.py`
- Descriptive names: `task_store.py`, `event_manager.py`

**Classes:**
- PascalCase: `AgentService`, `TaskStore`
- Clear domain indication

**Functions/Methods:**
- Snake case: `save_screenshot`, `run_with_streaming`
- Action-oriented names
- Async functions prefixed with `async def`

**Variables:**
- Snake case: `output_dir`, `llm_config`
- Clear, descriptive names
- Type hints always used

**Constants:**
- UPPER_SNAKE_CASE: `API_BASE`

### Frontend TypeScript

**Files:**
- PascalCase for components: `Button.tsx`, `TaskList.tsx`
- Index files: `index.ts`
- Barrel exports for shared utilities

**Interfaces/Types:**
- PascalCase: `Task`, `Run`, `DashboardStats`
- Descriptive names with clear purpose
- Optional properties marked with `?`

**React Components:**
- PascalCase: `Button`, `TaskModal`
- Destructured props
- Type props interface with `Props` suffix

**Functions/Methods:**
- camelCase: `fetchTasks`, `toggleSelect`
- Hook names: `useTasks`, `useDashboard`
- Event handlers: `onSubmit`, `onCancel`

**Variables:**
- camelCase: `filteredTasks`, `selectedIds`
- Clear, descriptive names

**Constants:**
- UPPER_SNAKE_CASE: `API_BASE`

## Code Style

### Python

**Line Length:**
- Maximum 100 characters (Ruff configuration)
- No hard limit enforcement in practice

**Imports:**
```python
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field
```
- Standard library first
- Third-party second
- Local modules last
- Relative imports for local modules

**Docstrings:**
- Triple quotes for all modules, classes, and functions
- Brief description
- Args and Returns sections for functions
- Examples for complex methods

**Type Hints:**
```python
async def save_screenshot(
    self,
    screenshot_data: Union[bytes, str],
    run_id: str,
    step_index: int
) -> str:
```
- Always used
- `Optional[X]` for nullable values
- `Union[X, Y]` for multiple types

### TypeScript

**Line Length:**
- No explicit limit, but maintain readability

**Imports:**
```typescript
import { useState, useCallback, useEffect, useMemo } from 'react'
import type { Task } from '../types'
import { tasksApi } from '../api/tasks'
```
- React imports first
- Relative imports for local modules
- Type imports with `type` keyword

**Spacing:**
- 2-space indentation
- No semicolons
- Curly braces on same line for statements
- JSX consistent with Prettier

**Component Structure:**
```typescript
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary'
  children: ReactNode
}

export function Button({ variant = 'primary', children, className = '', ...props }: ButtonProps) {
  // Implementation
}
```

## Error Handling

### Python

**Logging:**
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"[{run_id}] Creating LLM: config={llm_config}")
logger.warning(f"[{run_id}] base64 decode failed: {e}")
```
- Structured logging with context
- Different log levels appropriately used
- Context information in brackets

**Exception Handling:**
```python
try:
    screenshot_bytes = base64.b64decode(screenshot_data)
except Exception as e:
    logger.warning(f"[{run_id}] base64 decode failed: {e}")
    screenshot_bytes = screenshot_data.encode('utf-8')
```
- Specific exception types when possible
- Logging with context
- Graceful degradation

**API Response Errors:**
```python
if !response.ok:
    throw new ApiError(response.status, `API Error: ${response.status}`)
```

### TypeScript

**Error Boundaries:**
- Not implemented yet - opportunity for improvement

**Async Error Handling:**
```typescript
try {
  const data = await tasksApi.list({
    status: filters.status,
    search: filters.search,
  })
  setTasks(data)
} catch (error) {
  console.error('Failed to fetch tasks:', error)
}
```
- Try/catch for async operations
- Error logging with context
- User-friendly error messages not yet implemented

## Input Validation

### Python

**Pydantic Models:**
```python
class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    target_url: str = Field(default="", max_length=500)
    max_steps: int = Field(default=10, ge=1, le=100)
```
- Field validation with constraints
- Default values for optional fields
- Type safety enforced

### TypeScript

**Runtime Validation:**
```typescript
interface Filters {
  search: string
  status: 'all' | 'draft' | 'ready'
  sortBy: 'updated_at' | 'name' | 'created_at'
  sortOrder: 'asc' | 'desc'
}
```
- Type-level constraints
- No runtime validation yet - opportunity
- Literal types for fixed values

## Comments

### Python
- Comprehensive docstrings
- Inline comments for complex logic
- Chinese comments for business logic

### TypeScript
- Minimal comments - code should be self-explanatory
- Type definitions well-documented
- No JSDoc currently - opportunity for improvement

## Function Design

### Python
- Functions typically < 50 lines
- Single responsibility principle
- Async functions for I/O
- Clear input/output contracts

### TypeScript
- Small, focused functions
- useCallback/useMemo for performance
- Clear separation of concerns
- No deep nesting (>4 levels)

## Module Design

### Python
- Clear module boundaries
- Dependency injection where appropriate
- Factory pattern for LLM creation
- Service layer for business logic

### TypeScript
- Feature-based organization
- Shared utilities in `components/shared`
- API clients in dedicated modules
- Hooks for state management

## Architecture Patterns

### Backend
- Repository pattern for data access
- Service layer for business logic
- Event-driven architecture with callbacks
- Dependency injection for LLM providers

### Frontend
- Component-based architecture
- Custom hooks for state
- API client abstraction
- Type-safe interfaces

---

*Convention analysis: 2026-03-14*