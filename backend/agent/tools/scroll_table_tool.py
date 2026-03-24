"""scroll_table_and_input tool for horizontally scrolling table cell location and input.

Per D-01: Specialized tool design for ERP table scenarios.
Per D-06: Uses @registry.action decorator for browser-use integration.
Per D-07: Returns descriptive errors, lets Agent handle failures.
"""
import logging
from typing import Optional

from pydantic import BaseModel
from browser_use.browser.session import BrowserSession

logger = logging.getLogger(__name__)


class ScrollTableInputParams(BaseModel):
    """Parameters for scroll_table_and_input tool (per D-02)."""

    table_selector: str
    row_identifier: str
    column_header: str
    input_value: str


async def scroll_table_and_input(
    params: ScrollTableInputParams,
    browser_session: Optional[BrowserSession] = None,
) -> str:
    """Locate cell in horizontally scrolling table and input value.

    Per D-03 smart scroll logic:
    1. Use table_selector to locate table element
    2. Match column_header against table headers to find column index
    3. Match row_identifier against row text to find target row
    4. Check if target column is in visible area
    5. If not visible, scroll horizontally until column is visible
    6. Find input element in target cell
    7. Input value into the input element

    Args:
        params: ScrollTableInputParams with table_selector, row_identifier, column_header, input_value
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

        # Step 1: Locate table
        table = await page.query_selector(params.table_selector)
        if not table:
            return f"错误: 找不到表格 '{params.table_selector}'"

        # Step 2: Find column by header text
        headers = await table.query_selector_all("th")
        target_col_index = None

        for i, header in enumerate(headers):
            header_text = await header.text_content()
            if header_text and params.column_header in header_text.strip():
                target_col_index = i
                break

        if target_col_index is None:
            return f"错误: 找不到列 '{params.column_header}'"

        # Step 3: Find row by identifier text
        rows = await table.query_selector_all("tr")
        target_row = None

        for row in rows:
            row_text = await row.text_content()
            if row_text and params.row_identifier in row_text:
                target_row = row
                break

        if target_row is None:
            return f"错误: 找不到包含 '{params.row_identifier}' 的行"

        # Step 4 & 5: Get target cell and scroll into view
        target_cell = await target_row.query_selector(
            f"td:nth-child({target_col_index + 1})"
        )
        if not target_cell:
            return f"错误: 无法定位到第 {target_col_index + 1} 列的单元格"

        # Scroll cell into view (per D-03, using scrollIntoViewIfNeeded pattern)
        await target_cell.scroll_into_view_if_needed()
        await page.wait_for_timeout(100)  # Brief pause for scroll animation

        # Step 6: Find input element in cell
        input_element = await target_cell.query_selector("input, textarea")
        if not input_element:
            return "错误: 目标单元格中没有找到输入框"

        # Step 7: Input value
        await input_element.focus()
        await input_element.fill("")  # Clear existing value
        await input_element.type(params.input_value)

        logger.info(
            f"scroll_table_and_input success: column='{params.column_header}', "
            f"row='{params.row_identifier}', value='{params.input_value}'"
        )

        return f"成功: 在列 '{params.column_header}' 的行 '{params.row_identifier}' 中输入了值: {params.input_value}"

    except Exception as e:
        logger.error(f"scroll_table_and_input failed: {e}")
        return f"错误: 操作失败 - {str(e)}"


def register_scroll_table_tool(registry=None) -> None:
    """Register scroll_table_and_input tool with browser-use registry.

    Per D-06: Uses registry.action decorator pattern.
    Call this before creating Agent instance to make tool available.

    Args:
        registry: Optional browser-use registry. If None, uses default global registry.
    """
    from browser_use.tools.registry import registry as default_registry

    target_registry = registry or default_registry

    @target_registry.action(
        "在水平滚动表格中定位单元格并输入值。当目标列不在可视区域时自动水平滚动。"
        "适用于 ERP 系统中需要操作水平滚动表格内输入字段的场景。"
        "参数: table_selector(表格选择器), row_identifier(行内文本), column_header(列标题), input_value(输入值)",
        param_model=ScrollTableInputParams,
    )
    async def scroll_table_and_input_wrapper(
        params: ScrollTableInputParams,
        browser_session: BrowserSession,
    ) -> str:
        return await scroll_table_and_input(params, browser_session)

    logger.info("scroll_table_and_input tool registered with browser-use registry")
