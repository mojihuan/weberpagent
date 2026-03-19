# Archived Test Files

**Archived:** 2026-03-19
**Reason:** These test files import modules that have been deleted or refactored out of the codebase.

## Files

| File | Reason for Archival |
|------|---------------------|
| test_agent.py | Imports `backend.agent_simple` (deleted) |
| test_agent_optimized.py | Imports `backend.agent_simple` (deleted) |
| test_code_generator.py | Imports deleted code generator module |
| test_code_optimizer.py | Imports deleted optimizer module |
| test_code_reviewer.py | Imports deleted reviewer module |
| test_dashboard_api.py | References old API structure |
| test_decision.py | Imports `backend.agent_simple.decision` (deleted) |
| test_delivery_form.py | Uses deprecated form filler pattern |
| test_executor.py | Imports deleted executor module |
| test_form_filler_integration.py | Uses deprecated integration pattern |
| test_login_e2e.py | Superseded by e2e/tests/ tests |
| test_memory.py | Imports deleted memory module |
| test_memory_integration.py | Imports deleted memory module |
| test_orchestrator.py | Imports deleted orchestrator module |
| test_perception.py | Imports `backend.agent_simple.perception` (deleted) |
| test_phase5_unit.py | Phase-specific test, no longer relevant |
| test_purchase_e2e.py | Superseded by e2e/tests/ tests |
| test_sandbox.py | Sandbox experiment file |

## Restoration

To restore any of these tests:
1. Update imports to use current module structure
2. Verify test logic is still relevant
3. Move file back to `backend/tests/` or appropriate subdirectory
