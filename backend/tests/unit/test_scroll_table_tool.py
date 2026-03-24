"""Unit tests for scroll_table_and_input tool."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestScrollTableInputParams:
    """Tests for ScrollTableInputParams model."""

    def test_params_model_has_required_fields(self):
        """Verify model has all 4 required fields (D-02)."""
        from backend.agent.tools.scroll_table_tool import ScrollTableInputParams

        params = ScrollTableInputParams(
            table_selector="table.data-table",
            row_identifier="IMEI: 12345",
            column_header="销售金额",
            input_value="100.00",
        )
        assert params.table_selector == "table.data-table"
        assert params.row_identifier == "IMEI: 12345"
        assert params.column_header == "销售金额"
        assert params.input_value == "100.00"

    def test_params_model_requires_all_fields(self):
        """Verify all fields are required."""
        from backend.agent.tools.scroll_table_tool import ScrollTableInputParams

        with pytest.raises(Exception):  # ValidationError
            ScrollTableInputParams()  # Missing all required fields


class TestScrollTableAndInput:
    """Tests for scroll_table_and_input tool function."""

    @pytest.fixture
    def mock_browser_session(self):
        """Create mock browser session with page."""
        session = MagicMock()
        page = AsyncMock()

        # Mock table element
        table = AsyncMock()
        table.query_selector_all = AsyncMock(return_value=[])
        table.query_selector = AsyncMock(return_value=None)

        page.query_selector = AsyncMock(return_value=table)
        page.evaluate = AsyncMock(return_value=None)

        session.get_current_page = AsyncMock(return_value=page)
        return session

    @pytest.mark.asyncio
    async def test_missing_table_returns_error(self, mock_browser_session):
        """Tool returns error when table not found (D-07)."""
        from backend.agent.tools.scroll_table_tool import (
            ScrollTableInputParams,
            scroll_table_and_input,
        )

        mock_browser_session.get_current_page.return_value.query_selector = AsyncMock(
            return_value=None
        )

        params = ScrollTableInputParams(
            table_selector="table.nonexistent",
            row_identifier="test",
            column_header="test",
            input_value="test",
        )

        result = await scroll_table_and_input(params, mock_browser_session)
        assert "错误" in result or "error" in result.lower()

    @pytest.mark.asyncio
    async def test_missing_column_returns_error(self, mock_browser_session):
        """Tool returns error when column header not found (D-07)."""
        from backend.agent.tools.scroll_table_tool import (
            ScrollTableInputParams,
            scroll_table_and_input,
        )

        page = await mock_browser_session.get_current_page()
        table = await page.query_selector("table")
        table.query_selector_all = AsyncMock(return_value=[])  # No headers

        params = ScrollTableInputParams(
            table_selector="table",
            row_identifier="test",
            column_header="不存在的列",
            input_value="test",
        )

        result = await scroll_table_and_input(params, mock_browser_session)
        assert "列" in result or "column" in result.lower()

    @pytest.mark.asyncio
    async def test_missing_row_returns_error(self, mock_browser_session):
        """Tool returns error when row not found (D-07)."""
        from backend.agent.tools.scroll_table_tool import (
            ScrollTableInputParams,
            scroll_table_and_input,
        )

        page = await mock_browser_session.get_current_page()
        table = await page.query_selector("table")

        # Mock headers with target column
        header = AsyncMock()
        header.text_content = AsyncMock(return_value="销售金额")

        table.query_selector_all = AsyncMock(
            side_effect=[
                [header],  # headers
                [],  # rows - empty
            ]
        )

        params = ScrollTableInputParams(
            table_selector="table",
            row_identifier="不存在的行",
            column_header="销售金额",
            input_value="test",
        )

        result = await scroll_table_and_input(params, mock_browser_session)
        assert "行" in result or "row" in result.lower()

    @pytest.mark.asyncio
    async def test_missing_input_returns_error(self, mock_browser_session):
        """Tool returns error when no input element in cell (D-07)."""
        from backend.agent.tools.scroll_table_tool import (
            ScrollTableInputParams,
            scroll_table_and_input,
        )

        page = await mock_browser_session.get_current_page()
        table = await page.query_selector("table")

        # Mock header
        header = AsyncMock()
        header.text_content = AsyncMock(return_value="销售金额")

        # Mock row with text
        row = AsyncMock()
        row.text_content = AsyncMock(return_value="IMEI: 12345")

        # Mock cell without input
        cell = AsyncMock()
        cell.query_selector = AsyncMock(return_value=None)  # No input
        row.query_selector = AsyncMock(return_value=cell)

        table.query_selector_all = AsyncMock(
            side_effect=[
                [header],  # headers
                [row],  # rows
            ]
        )

        params = ScrollTableInputParams(
            table_selector="table",
            row_identifier="IMEI: 12345",
            column_header="销售金额",
            input_value="100.00",
        )

        result = await scroll_table_and_input(params, mock_browser_session)
        assert "输入" in result or "input" in result.lower()


class TestToolRegistration:
    """Tests for tool registration with browser-use registry."""

    def test_register_scroll_table_tool_function_exists(self):
        """Verify register_scroll_table_tool function exists."""
        from backend.agent.tools.scroll_table_tool import register_scroll_table_tool

        assert callable(register_scroll_table_tool)
