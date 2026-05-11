# Auto-Execute Precondition Operations

**Date:** 2026-05-10
**Status:** Approved

## Problem

When test cases are imported via Excel, precondition code like:

```python
context['preconditions'] = ['FA1', 'HC1']
```

Only stores the operation codes in the context dict. The actual `PreFront().operations()` call is never made. This means ERP operations (e.g., creating purchase orders, sales outbound) are never executed, and subsequent `get_data()` calls return stale data with the same IMEIs every time.

The front-end OperationCodeSelector generates correct code (via `/generate` API), but Excel import bypasses this and the user writes the shorthand directly.

## Solution

Auto-detect `context['preconditions']` in `PreconditionService.execute_single()` after `exec()` completes. If present and not yet executed, call `execute_operations()` automatically.

## Design

### Flow

1. `exec(code, env)` runs user precondition code as before
2. After exec, check `context.get('preconditions')`:
   - If it's a `list[str]` and `context.get('_operations_executed')` is not `True`
   - Call `execute_operations(codes)` which invokes `PreFront().operations(codes)`
3. Set `context['_operations_executed'] = True` to prevent re-execution
4. Remove `preconditions` key from context to avoid polluting downstream data

### File Change

**`backend/core/precondition_service.py`** — `execute_single()` method:

After the `exec()` call succeeds and before taking the variable snapshot, insert the auto-detection logic:

```python
# Auto-execute precondition operation codes
op_codes = self.context.get('preconditions')
if isinstance(op_codes, list) and not self.context.get('_operations_executed'):
    from backend.core.external_execution_engine import execute_operations
    success, error, _ = execute_operations(op_codes)
    if not success:
        raise RuntimeError(f"Precondition operations failed: {error}")
    self.context['_operations_executed'] = True
```

### Error Handling

- `execute_operations()` failure raises `RuntimeError`, caught by existing `except Exception` in `execute_single()`
- Timeout: existing 30s per-precondition timeout covers the operation execution
- Idempotency: `_operations_executed` flag prevents re-execution if user writes multiple precondition blocks with the same pattern

### Backward Compatibility

- Front-end generated code (via OperationCodeSelector) already calls `PreFront().operations()` directly — no `context['preconditions']` key is set, so auto-detection is skipped
- Precondition code without operation codes is unaffected
- No changes to Excel parser, API routes, or front-end

## Testing

- Unit test: `execute_single()` with `context['preconditions'] = ['FA1']` triggers `execute_operations()`
- Unit test: `_operations_executed` flag prevents double execution
- Unit test: failure in `execute_operations()` propagates as precondition failure
- Unit test: existing code pattern (no `preconditions` key) is unaffected
