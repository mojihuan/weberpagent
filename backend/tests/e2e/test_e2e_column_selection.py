"""E2E test for DEPTH-05: Agent correctly selects sales amount column.

Validates that Phase 94 (DOM patch column header injection + td depth protection)
and Phase 95 (Section 9 cross-positioning rewrite) jointly solve column misidentification.
"""

import asyncio

import pytest

from backend.tests.e2e.conftest import _has_api_key

# Polling defaults
_POLL_INTERVAL = 5
_POLL_TIMEOUT = 360  # 6 minutes -- increased from 300s for login + navigate + fill

# Terminal run statuses
_TERMINAL_STATUSES = ("success", "failed", "stopped")


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
        print(f"[DEPTH-05] Polling run {run_id}... status={status}")

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
# DEPTH-05: Column selection verification
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _has_api_key(), reason="DASHSCOPE_API_KEY not configured")
@pytest.mark.asyncio
async def test_e2e_column_selection_sales_amount(api_client):
    """DEPTH-05: Verify Agent selects sales amount column (not profit column).

    Creates a task targeting the sales outbound page, asking the Agent to find
    a specific row by IMEI and fill the sales amount with 150. Verifies that:
    - Agent reasoning shows awareness of "销售金额" (sales amount column)
    - Agent never mentions "利润" (profit column) in reasoning
    - Either an input action with value 150 exists, or the run succeeded
    """
    # Step 1: Create task
    task_payload = {
        "name": "E2E列选择验证-销售金额",
        "description": (
            "在销售出库页面，找到 I01784004409597 所在行，"
            "将销售金额填写为 150。"
            "注意区分销售金额列和利润列。"
        ),
        "target_url": "",
        "max_steps": 20,
        "login_role": "main",
    }
    task_resp = await api_client.post("/api/tasks", json=task_payload)
    assert task_resp.status_code == 200, f"POST /api/tasks failed: {task_resp.text}"
    task_data = task_resp.json()
    task_id = task_data["id"]
    print(f"[DEPTH-05] Step 1: Created task {task_id}")

    # Step 2: Trigger run
    run_resp = await api_client.post("/api/runs", params={"task_id": task_id})
    assert run_resp.status_code == 200, f"POST /api/runs failed: {run_resp.text}"
    run_data = run_resp.json()
    run_id = run_data["id"]
    print(f"[DEPTH-05] Step 2: Created run {run_id}")

    # Step 3: Poll for completion
    final_run = await _poll_run_completion(api_client, run_id)
    assert final_run["status"] in ("success", "failed"), (
        f"Run ended with unexpected status '{final_run['status']}'. "
        f"Expected 'success' or 'failed'."
    )
    print(f"[DEPTH-05] Step 3: Run completed with status={final_run['status']}")

    # Step 4: Fetch report with step data
    report_resp = await api_client.get(f"/api/reports/{run_id}")
    assert report_resp.status_code == 200, (
        f"GET /api/reports/{run_id} returned {report_resp.status_code}: {report_resp.text}"
    )
    report_data = report_resp.json()
    steps = report_data.get("steps", [])
    print(f"[DEPTH-05] Step 4: Report retrieved with {len(steps)} steps")

    # Step 5: Verify column selection evidence
    reasoning_texts = [s.get("reasoning", "") or "" for s in steps]
    actions = [s.get("action", "") or "" for s in steps]

    # 5a: At least one step should mention "销售金额" in reasoning
    has_sales_amount_awareness = any("销售金额" in r for r in reasoning_texts)

    # 5b: An input action with value "150" should exist
    has_value_150_input = any("150" in a and "input" in a.lower() for a in actions)

    # 5c: No evidence of repeatedly clicking profit column (利润)
    #     Only count steps where "利润" appears alongside failure context
    profit_clicks = [r for r in reasoning_texts if "利润" in r]

    # PRIMARY: Agent shows awareness of sales amount column
    assert has_sales_amount_awareness, (
        "No step reasoning mentions '销售金额' -- "
        "Agent may not be using column annotations. "
        f"All reasoning: {reasoning_texts}"
    )

    # CRITICAL: Agent did NOT click the profit column repeatedly
    assert len(profit_clicks) == 0, (
        f"Agent reasoning mentions '利润' in {len(profit_clicks)} steps: "
        f"{profit_clicks} -- column selection may still be broken"
    )

    # SECONDARY: Value 150 was input (strong signal but Agent may use evaluate JS)
    if not has_value_150_input:
        if final_run["status"] != "success":
            pytest.fail(
                "Run failed and no input action with value 150 found -- "
                "Agent likely did not fill the sales amount correctly"
            )
        # If run succeeded without explicit input_text("150"), Agent used alternative method

    # Diagnostic output
    print(f"[DEPTH-05] Run completed: status={final_run['status']}, steps={len(steps)}")
    for i, s in enumerate(steps):
        action_preview = (s.get("action") or "")[:80]
        reasoning_preview = (s.get("reasoning") or "")[:80]
        print(f"  Step {i}: action={action_preview}...")
        print(f"          reasoning={reasoning_preview}...")

    # Cleanup: delete created task to avoid data pollution
    try:
        await api_client.delete(f"/api/tasks/{task_id}")
    except Exception:
        pass  # Non-critical cleanup
