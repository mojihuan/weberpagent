"""scroll_table_and_input tool for horizontally scrolling table cell location and input.

Per D-01: Specialized tool design for ERP table scenarios.
Per D-06: Uses Tools.action decorator for browser-use 0.2+ API.
Per D-07: Returns descriptive errors, lets Agent handle failures.
"""
import logging
from typing import Optional

from pydantic import BaseModel
from browser_use.browser.session import BrowserSession
from browser_use.tools.service import Tools

logger = logging.getLogger(__name__)


class ScrollTableInputParams(BaseModel):
    """Parameters for scroll_table_and_input tool (kept for backward compatibility)."""

    table_selector: str
    row_identifier: str
    column_header: str
    input_value: str


async def scroll_table_and_input(
    table_selector: str,
    row_identifier: str,
    column_header: str,
    input_value: str,
    browser_session: Optional[BrowserSession] = None,
) -> str:
    """Locate cell in horizontally scrolling table and input value.

    Per D-03 smart scroll logic with auto-detection:
    1. Find table (auto-detect if generic selector provided)
    2. Match column_header against table headers to find column index
    3. Match row_identifier against row text to find target row
    4. Scroll horizontally if needed
    5. Find input element in target cell
    6. Input value

    Args:
        table_selector: CSS selector for the table (or generic, will auto-detect)
        row_identifier: Text content to identify the target row
        column_header: Text content of the column header
        input_value: Value to input into the cell
        browser_session: Browser session from browser-use (injected)

    Returns:
        Success message or descriptive error (per D-07)
    """
    if not browser_session:
        return "错误: 没有可用的浏览器会话"

    try:
        page = await browser_session.get_current_page()
        if not page:
            return "错误: 无法获取当前页面"

        # Step 1: Locate table (with auto-detection)
        table = None

        # Try specific selector first
        if table_selector not in ["div", "table", ""]:
            table = await page.query_selector(table_selector)

        # Auto-detect: find table containing the row_identifier
        if not table:
            logger.info(f"Auto-detecting table containing '{row_identifier}'...")
            tables = await page.query_selector_all("table, .ant-table, [role='grid'], .el-table")

            for t in tables:
                text = await t.text_content()
                if text and row_identifier in text:
                    table = t
                    logger.info(f"Found table containing '{row_identifier}'")
                    break

        # Fallback: find any element with horizontal scroll containing the row
        if not table:
            logger.info("Trying scrollable container detection...")
            scrollable = await page.query_selector_all("[style*='overflow']")
            for el in scrollable:
                text = await el.text_content()
                if text and row_identifier in text:
                    table = el
                    logger.info(f"Found scrollable container containing '{row_identifier}'")
                    break

        if not table:
            return f"错误: 找不到包含 '{row_identifier}' 的表格。请确保表格可见且包含目标行。"

        # Step 2: Find column by header text
        # Try th first, then look for header row
        headers = await table.query_selector_all("th")
        if not headers:
            # Try finding headers in first row
            first_row = await table.query_selector("tr")
            if first_row:
                headers = await first_row.query_selector_all("td, th")

        target_col_index = None
        for i, header in enumerate(headers):
            header_text = await header.text_content()
            if header_text and column_header in header_text.strip():
                target_col_index = i
                logger.info(f"Found column '{column_header}' at index {i}")
                break

        if target_col_index is None:
            # List available columns for debugging
            available = []
            for h in headers:
                t = await h.text_content()
                if t:
                    available.append(t.strip())
            return f"错误: 找不到列 '{column_header}'。可用列: {', '.join(available[:10])}"

        # Step 3: Find row by identifier text
        rows = await table.query_selector_all("tr")
        if not rows:
            # For non-table elements, try finding row-like elements
            rows = await table.query_selector_all("[role='row'], .ant-table-row, tr")

        target_row = None
        for row in rows:
            row_text = await row.text_content()
            if row_text and row_identifier in row_text:
                target_row = row
                logger.info(f"Found row containing '{row_identifier}'")
                break

        if target_row is None:
            return f"错误: 找不到包含 '{row_identifier}' 的行"

        # Step 4 & 5: Get target cell and scroll into view
        target_cell = await target_row.query_selector(
            f"td:nth-child({target_col_index + 1}), [role='gridcell']:nth-child({target_col_index + 1})"
        )
        if not target_cell:
            return f"错误: 无法定位到第 {target_col_index + 1} 列的单元格"

        # Scroll cell into view (per D-03)
        await target_cell.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)  # Wait for scroll animation

        # Step 6: Find input element in cell
        input_element = await target_cell.query_selector("input, textarea, [contenteditable='true']")
        if not input_element:
            # Check if cell itself is editable
            is_editable = await target_cell.get_attribute("contenteditable")
            if is_editable == "true":
                input_element = target_cell
            else:
                return "错误: 目标单元格中没有找到输入框，请检查该列是否可编辑"

        # Step 7: Input value
        await input_element.focus()
        await input_element.fill("")  # Clear existing value
        await page.wait_for_timeout(50)
        await input_element.type(input_value)
        await page.wait_for_timeout(100)  # Wait for React/Vue to process

        logger.info(
            f"scroll_table_and_input success: column='{column_header}', "
            f"row='{row_identifier}', value='{input_value}'"
        )

        return f"成功: 在列 '{column_header}' 的行 '{row_identifier}' 中输入了值: {input_value}"

    except Exception as e:
        logger.error(f"scroll_table_and_input failed: {e}", exc_info=True)
        return f"错误: 操作失败 - {str(e)}"


def create_tools_with_scroll_table() -> Tools:
    """Create Tools instance with scroll_table_and_input action registered.

    Per D-06: Uses Tools.action decorator pattern for browser-use 0.2+ API.
    Call this before creating Agent instance to get tools with custom action.

    Returns:
        Tools instance with scroll_table_and_input action registered.
    """
    tools = Tools()

    @tools.action(
        "在水平滚动表格中定位单元格并输入值。自动检测包含目标行的表格，自动滚动到目标列。"
        "适用于 ERP 系统中需要操作水平滚动表格内输入字段的场景。"
        "参数: table_selector(表格选择器，可填'table'或任意值自动检测), "
        "row_identifier(行内的唯一文本，如商品编号), "
        "column_header(列标题文本，如'销售金额'), "
        "input_value(要输入的值)"
    )
    async def scroll_table_and_input_action(
        table_selector: str,
        row_identifier: str,
        column_header: str,
        input_value: str,
        browser_session: BrowserSession = None,
    ) -> str:
        return await scroll_table_and_input(
            table_selector=table_selector,
            row_identifier=row_identifier,
            column_header=column_header,
            input_value=input_value,
            browser_session=browser_session,
        )

    logger.info("scroll_table_and_input tool registered with browser-use Tools")
    return tools


# Keep old function name for backward compatibility
def register_scroll_table_tool(registry=None) -> Tools:
    """Register scroll_table_and_input tool with browser-use.

    Per D-06: Uses Tools.action decorator pattern for browser-use 0.2+ API.

    Args:
        registry: Ignored (kept for backward compatibility).

    Returns:
        Tools instance with scroll_table_and_input action registered.
    """
    return create_tools_with_scroll_table()
