---
phase: 132-后端异步与状态
plan: 01
status: complete
requirements:
  - ASYNC-01
  - ASYNC-02
---

# Plan 01: 阻塞操作异步迁移

## Summary

Migrated two blocking I/O operations to async patterns: `save_screenshot` now uses `asyncio.to_thread` for file writes (ASYNC-01), and `_execute_code_background` now uses `asyncio.create_subprocess_exec` instead of `subprocess.run` (ASYNC-02). Both changes prevent event loop blocking during I/O-heavy operations.

## Changes

- **`backend/core/agent_service.py`**: Replaced `filepath.write_bytes(screenshot_bytes)` with `await asyncio.to_thread(filepath.write_bytes, screenshot_bytes)` in `save_screenshot` method
- **`backend/api/routes/runs_routes.py`**: Replaced `subprocess.run` with `asyncio.create_subprocess_exec` + `asyncio.wait_for`, removed `import subprocess`, added `proc.kill()` + `await proc.wait()` timeout cleanup, added `stdout.decode()` / `stderr.decode()` for byte decoding
- **`backend/tests/test_async_blocking.py`**: Added 9 test cases in 2 classes covering both async migrations

## Test Results

- 9/9 new tests pass (3 ASYNC-01 + 6 ASYNC-02)
- 34/34 total tests pass (no regressions)
- `uv run pytest backend/tests/ -v --timeout=30` -- all green

## Verification

Acceptance criteria confirmed:
- `agent_service.py` contains `await asyncio.to_thread(filepath.write_bytes, screenshot_bytes)`
- `runs_routes.py` contains `asyncio.create_subprocess_exec` and does NOT contain `subprocess.run`
- `runs_routes.py` does NOT contain `import subprocess`
- `runs_routes.py` contains `proc.kill()` followed by `await proc.wait()` for timeout cleanup
- `runs_routes.py` contains `stdout.decode()` and `stderr.decode()`
- All existing + new tests pass

## Deviations from Plan

None - plan executed exactly as written.
