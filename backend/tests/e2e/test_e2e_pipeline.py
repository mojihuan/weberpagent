"""End-to-end pipeline tests.

Validates three E2E requirements:
- E2E-01: Natural language -> AI execution -> report pipeline completes
- E2E-02: context.get_data() with docstring method mapping works
- E2E-03: PcAssert external assertion executes and returns pass/fail result
"""

import asyncio

import pytest

from backend.tests.e2e.conftest import _has_api_key, _has_weberp_path

# Polling defaults
_POLL_INTERVAL = 5
_POLL_TIMEOUT = 300

# Terminal run statuses (per D-06, success or failed are both acceptable)
_TERMINAL_STATUSES = ("success", "failed", "stopped")
_ACCEPTABLE_STATUSES = ("success", "failed")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

async def _poll_run_completion(client, run_id: str) -> dict:
    """Poll GET /api/runs/{run_id} until terminal status or timeout.

    Returns the final run JSON on terminal status.
    Raises TimeoutError if the run does not complete within _POLL_TIMEOUT.
    """
    loop = asyncio.get_event_loop()
    deadline = loop.time() + _POLL_TIMEOUT

    while True:
        resp = await client.get(f"/api/runs/{run_id}")
        assert resp.status_code == 200, f"GET /api/runs/{run_id} returned {resp.status_code}"
        data = resp.json()
        status = data.get("status", "unknown")
        print(f"[E2E] Polling run {run_id}... status={status}")

        if status in _TERMINAL_STATUSES:
            return data

        remaining = deadline - loop.time()
        if remaining <= 0:
            raise TimeoutError(
                f"Run {run_id} did not reach terminal status within {_POLL_TIMEOUT}s. "
                f"Last status: {status}"
            )
        await asyncio.sleep(min(_POLL_INTERVAL, remaining))


# ---------------------------------------------------------------------------
# E2E-02: Precondition only (fast ~5s)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _has_weberp_path(), reason="WEBSERP_PATH not configured")
@pytest.mark.asyncio
async def test_e2e_precondition_only():
    """E2E-02: Verify context.get_data() with docstring method mapping."""
    from backend.core.external_precondition_bridge import execute_data_method

    result = await execute_data_method("PcImport", "库存管理|库存列表", {})
    assert result["success"], f"Data method failed: {result.get('error')}"
    assert result["data"] is not None


# ---------------------------------------------------------------------------
# E2E-03: Assertion only (fast ~10s)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _has_weberp_path(), reason="WEBSERP_PATH not configured")
@pytest.mark.asyncio
async def test_e2e_assertion_only():
    """E2E-03: Verify PcAssert assertion execution."""
    from backend.core.external_precondition_bridge import (
        execute_assertion_method,
        load_base_assertions_class,
    )

    classes_dict, error = load_base_assertions_class()
    if error or "PcAssert" not in classes_dict:
        pytest.skip(f"PcAssert not available: {error}")

    # Find first public non-internal method on PcAssert
    pc_assert_cls = classes_dict["PcAssert"]
    INTERNAL = {
        "_get_cached_api", "_call_module_api",
        "assert_time", "assert_contains", "assert_equal",
        "_get_field_value", "_assert_api_response",
    }
    method_name = None
    for name in dir(pc_assert_cls):
        if name.startswith("_") or name in INTERNAL:
            continue
        if callable(getattr(pc_assert_cls, name)):
            method_name = name
            break

    if method_name is None:
        pytest.skip("No public PcAssert methods found")

    result = await execute_assertion_method(
        class_name="PcAssert",
        method_name=method_name,
        headers="main",
        data="main",
    )
    # Per D-06: passed OR assertion-failed (AssertionError) is OK.
    # Only ImportError/ExecutionError indicates a broken chain.
    assert result["error_type"] not in ("ImportError", "ExecutionError"), (
        f"Assertion execution failed with: {result.get('error')}"
    )


# ---------------------------------------------------------------------------
# E2E-01 + E2E-02 + E2E-03: Full pipeline (slow ~2-5 min)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _has_api_key(), reason="DASHSCOPE_API_KEY not configured")
@pytest.mark.asyncio
async def test_e2e_full_pipeline(api_client):
    """E2E-01 + E2E-02 + E2E-03: Full pipeline verification.

    Creates a task with precondition + assertion, triggers a run,
    polls to completion, and verifies the report exists.
    """
    # Step 1: Discover an assertion method name via the API
    methods_resp = await api_client.get("/api/external-assertions/methods")
    if methods_resp.status_code == 503:
        pytest.skip("WEBSERP_PATH not configured (external assertions unavailable)")

    assert methods_resp.status_code == 200
    methods_data = methods_resp.json()
    assertion_method_name = None

    for cls_group in methods_data.get("classes", []):
        if cls_group["name"] == "PcAssert":
            methods_list = cls_group.get("methods", [])
            # Prefer method with description matching inventory
            for m in methods_list:
                if "库存" in m.get("description", ""):
                    assertion_method_name = m["name"]
                    break
            # Fallback to first available
            if assertion_method_name is None and methods_list:
                assertion_method_name = methods_list[0]["name"]
            break

    if assertion_method_name is None:
        pytest.skip("No PcAssert methods available via API")

    # Step 2: Create task with precondition + assertion
    task_payload = {
        "name": "E2E可用性验证-库存列表",
        "description": "查看ERP首页，确认页面正常加载",
        "target_url": "",
        "max_steps": 3,
        "login_role": "main",
        "preconditions": [
            "data = context.get_data('PcImport', '库存管理|库存列表')\ncontext['inv_data'] = data"
        ],
        "assertions": [
            {
                "class_name": "PcAssert",
                "method_name": assertion_method_name,
                "headers": "main",
                "data": "main",
            }
        ],
    }

    task_resp = await api_client.post("/api/tasks", json=task_payload)
    assert task_resp.status_code == 200, f"POST /api/tasks failed: {task_resp.text}"
    task_data = task_resp.json()
    task_id = task_data["id"]
    print(f"[E2E] Step 1: Created task {task_id}")

    # Step 3: Create run
    run_resp = await api_client.post("/api/runs", params={"task_id": task_id})
    assert run_resp.status_code == 200, f"POST /api/runs failed: {run_resp.text}"
    run_data = run_resp.json()
    run_id = run_data["id"]
    print(f"[E2E] Step 2: Created run {run_id}")

    # Step 4: Poll for completion
    final_run = await _poll_run_completion(api_client, run_id)
    final_status = final_run.get("status", "unknown")
    steps_count = final_run.get("steps_count", 0)
    print(f"[E2E] Step 3: Run completed with status={final_status}, steps={steps_count}")

    # Step 5: Verify run completed (E2E-01, per D-06)
    assert final_status in _ACCEPTABLE_STATUSES, (
        f"Run ended with unexpected status '{final_status}'. Expected one of {_ACCEPTABLE_STATUSES}."
    )

    # Step 6: Verify report exists (E2E-01)
    report_resp = await api_client.get(f"/api/reports/{run_id}")
    assert report_resp.status_code == 200, (
        f"GET /api/reports/{run_id} returned {report_resp.status_code}: {report_resp.text}"
    )
    report_data = report_resp.json()
    report_id = report_data.get("id")
    assert report_id is not None, "Report response missing 'id' field"
    assert report_data.get("run_id") == run_id, "Report run_id mismatch"
    print(f"[E2E] Step 4: Report retrieved, id={report_id}")

    # Step 7: Diagnostic info about preconditions (E2E-02)
    if steps_count == 0 and final_status == "failed":
        print("[E2E] WARNING: Run failed with 0 steps -- may have failed at precondition stage")

    # Step 8: Diagnostic info about assertions (E2E-03)
    ext_summary = final_run.get("external_assertion_summary")
    if ext_summary:
        print(
            f"[E2E] External assertions: "
            f"{ext_summary.get('passed', '?')}/{ext_summary.get('total', '?')} passed"
        )
    else:
        print("[E2E] No external assertion summary in run response")
