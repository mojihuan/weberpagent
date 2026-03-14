---
phase: 01-foundation-fixes
plan: 04
subsystem: llm
tags: [determinism, temperature, configuration, tdd]
dependency_graph:
  requires: [01-01]
  provides: [deterministic-llm]
  affects: [backend/llm/factory.py, backend/api/routes/runs.py]
tech_stack:
  added: []
  patterns: [centralized-settings, tdd]
key_files:
  created:
    - backend/tests/unit/test_llm_config.py
    - backend/tests/integration/test_agent_service.py
  modified:
    - backend/llm/factory.py
    - backend/api/routes/runs.py
decisions:
  - temperature=0.0 for deterministic LLM output
  - centralized Settings for all LLM configuration
metrics:
  duration: 4 min
  tasks: 4
  tests: 7
  files: 4
  completed_date: "2026-03-14"
---

# Phase 1 Plan 4: LLM Deterministic Configuration Summary

## One-liner

Configured LLM for deterministic test execution with temperature=0.0 and centralized Settings integration.

## What Was Done

### Task 1: Update create_llm() default temperature to 0.0

Changed the default temperature in `backend/llm/factory.py` from 0.1 to 0.0 for deterministic output. Updated the docstring to clarify the purpose.

### Task 2: Update get_llm_config() to use centralized Settings

Replaced `os.getenv()` calls in `backend/api/routes/runs.py` with `get_settings()` to use the centralized Settings class. The function now reads from `Settings.llm_model`, `Settings.llm_base_url`, `Settings.llm_temperature`, and `Settings.dashscope_api_key`/`Settings.openai_api_key`.

### Task 3: Create unit tests for LLM configuration

Created `backend/tests/unit/test_llm_config.py` with 5 test cases:
- `test_create_llm_temperature_default`: verifies temperature=0.0 is the default
- `test_create_llm_temperature_from_config`: respects provided temperature
- `test_get_llm_config_uses_settings`: uses centralized Settings
- `test_get_llm_config_temperature_zero`: returns temperature=0.0
- `test_get_llm_config_prefers_dashscope_key`: prefers DashScope API key

### Task 4: Create integration test for AgentService LLM configuration

Created `backend/tests/integration/test_agent_service.py` with 2 test cases:
- `test_agent_service_uses_llm_config`: passes LLM config to create_llm
- `test_agent_service_default_temperature`: uses create_llm defaults

## Key Decisions

1. **temperature=0.0 for determinism**: Using temperature=0 significantly improves predictability even though 100% reproducibility isn't guaranteed due to GPU non-determinism.

2. **Centralized Settings**: All LLM configuration now flows through the centralized Settings class, providing a single source of truth.

## Deviations from Plan

None - plan executed exactly as written.

## Verification Results

All 7 tests pass:
- 2 tests for create_llm() temperature handling
- 3 tests for get_llm_config() Settings integration
- 2 integration tests for AgentService LLM config flow

## Commits

| Commit | Message |
|--------|---------|
| 69406b9 | test(01-04): add failing test for create_llm default temperature |
| a2d0987 | feat(01-04): update get_llm_config to use centralized Settings |
| dbb5550 | test(01-04): add unit and integration tests for LLM configuration |

## Self-Check: PASSED

- [x] backend/llm/factory.py contains `temperature.*0.0`
- [x] backend/api/routes/runs.py contains `get_settings`
- [x] All tests pass
- [x] All commits exist
