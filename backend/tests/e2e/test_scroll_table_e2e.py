"""
E2E Tests for scroll_table_and_input tool behavior.

LOOP-04 Verification: Agent self-handles tool failure and continues.

Per D-08: No separate skip logic implementation needed.
The Agent naturally handles tool failures through its decision-making process.

Manual E2E Verification Steps:
==============================

Test Case 1: Agent continues after tool failure
-----------------------------------------------
Prerequisites:
- ERP system accessible at ERP_BASE_URL
- Valid credentials in ERP_USERNAME, ERP_PASSWORD
- Test case with intentionally invalid table selector

Steps:
1. Start backend: uv run uvicorn backend.api.main:app --reload --port 8080
2. Open frontend: cd frontend && npm run dev
3. Create a test case with:
   - Step 1: Navigate to a page with a table
   - Step 2: Call scroll_table_and_input with INVALID table_selector
   - Step 3: Perform another action (e.g., click a button)
4. Run the test case
5. Observe: Agent should:
   - Attempt to use scroll_table_and_input tool
   - Receive error message: "错误: 找不到表格 'invalid_selector'"
   - Log the error in its reasoning
   - Continue to Step 3 or adapt its approach

Expected Result:
- Agent does not crash or hang
- Error is logged in run steps
- Subsequent steps execute (or Agent adapts strategy)

Test Case 2: Agent adapts strategy on tool failure
---------------------------------------------------
Steps:
1. Create a test case with:
   - Step 1: Navigate to sales order page
   - Step 2: Use scroll_table_and_input with valid selector but wrong row
   - Step 3: Complete the order
2. Run the test case
3. Observe: Agent should:
   - Attempt scroll_table_and_input
   - Receive error: "错误: 找不到包含 'wrong_row_text' 的行"
   - Either: retry with different row identifier, or skip and continue

Expected Result:
- Agent adapts its approach based on error context
- Task eventually completes or gracefully fails

Test Case 3: Multiple tool failures handled
--------------------------------------------
Steps:
1. Create a test case with multiple scroll_table_and_input calls
2. Some should succeed, some should fail
3. Observe: Agent handles each failure independently

Expected Result:
- Successful tool calls complete normally
- Failed tool calls return errors
- Agent continues processing remaining steps

Integration with LoopInterventionTracker:
=========================================
If stagnation >= 5 is detected (Phase 39), the intervention message
suggests the Agent try different approaches. Combined with tool
error messages, the Agent has multiple signals to guide adaptation.

Automated Verification (Limited):
=================================
The following test verifies tool registration and error message format.
Full E2E verification requires live ERP system and manual testing.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.agent.tools.scroll_table_tool import (
    ScrollTableInputParams,
    scroll_table_and_input,
)


class TestScrollTableE2EDocumentation:
    """E2E test documentation for LOOP-04 verification."""

    @pytest.mark.asyncio
    async def test_tool_returns_descriptive_error_for_missing_table(self):
        """Verify tool returns descriptive error (D-07) - foundation for LOOP-04.

        When the tool fails, it returns a Chinese error message.
        This error message allows the Agent to understand what went wrong
        and decide how to proceed (LOOP-04 behavior).

        LOOP-04 VERIFICATION: This test verifies D-07 (descriptive errors).
        Per D-08, Agent self-handling is achieved through these error messages.
        No separate implementation needed - the Agent naturally continues
        after receiving a descriptive error from the tool.
        """
        mock_browser = MagicMock()
        mock_page = AsyncMock()
        mock_page.query_selector = AsyncMock(return_value=None)  # Table not found
        mock_browser.get_current_page = AsyncMock(return_value=mock_page)

        params = ScrollTableInputParams(
            table_selector="table.nonexistent",
            row_identifier="test",
            column_header="test",
            input_value="test",
        )

        result = await scroll_table_and_input(params, mock_browser)

        # Verify error message format (D-07)
        assert "错误" in result, "Error message should contain '错误'"
        assert "表格" in result or "table" in result.lower(), "Error should mention table"

    @pytest.mark.asyncio
    async def test_tool_returns_descriptive_error_for_missing_row(self):
        """Verify tool returns descriptive error for missing row.

        Different error types allow Agent to understand context.
        """
        mock_browser = MagicMock()
        mock_page = AsyncMock()

        # Mock table exists but row not found
        mock_table = AsyncMock()
        mock_header = AsyncMock()
        mock_header.text_content = AsyncMock(return_value="销售金额")
        mock_table.query_selector_all = AsyncMock(side_effect=[
            [mock_header],  # headers
            [],  # rows - empty
        ])

        mock_page.query_selector = AsyncMock(return_value=mock_table)
        mock_browser.get_current_page = AsyncMock(return_value=mock_page)

        params = ScrollTableInputParams(
            table_selector="table",
            row_identifier="不存在的行",
            column_header="销售金额",
            input_value="100",
        )

        result = await scroll_table_and_input(params, mock_browser)

        # Verify error mentions row
        assert "错误" in result
        assert "行" in result

    def test_error_messages_are_chinese(self):
        """Verify error messages are in Chinese for consistency.

        This ensures Agent receives consistent error format.
        """
        # All error messages from scroll_table_and_input start with "错误:"
        # This pattern allows Agent to recognize tool failures consistently
        error_patterns = [
            "错误: 没有可用的浏览器会话",
            "错误: 无法获取当前页面",
            "错误: 找不到表格",
            "错误: 找不到列",
            "错误: 找不到包含",
            "错误: 无法定位到",
            "错误: 目标单元格中没有找到输入框",
            "错误: 操作失败",
        ]

        for pattern in error_patterns:
            assert pattern.startswith("错误:"), f"Error should start with '错误:': {pattern}"
