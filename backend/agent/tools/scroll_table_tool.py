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

    Uses JavaScript execution via browser-use Page.evaluate() for all DOM operations.

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

        # 使用 page.evaluate 执行 JavaScript 完成所有操作
        # JavaScript 必须是 (...args) => 格式
        js_code = """(tableSelector, rowIdentifier, columnHeader, inputValue) => {
            // Step 1: Find table (auto-detect if generic selector)
            let table = null;
            const specificSelectors = ['table', '.ant-table', '.el-table', '[role="grid"]'];

            if (tableSelector && !specificSelectors.includes(tableSelector)) {
                // Try specific selector first
                table = document.querySelector(tableSelector);
            }

            if (!table) {
                // Auto-detect: find table containing rowIdentifier text
                for (const sel of specificSelectors) {
                    const tables = document.querySelectorAll(sel);
                    for (const t of tables) {
                        if (t.textContent.includes(rowIdentifier)) {
                            table = t;
                            break;
                        }
                    }
                    if (table) break;
                }
            }

            if (!table) {
                return { error: '找不到包含目标文本的表格' };
            }

            // Step 2: Find column by header text
            const headers = table.querySelectorAll('th');
            let targetColIndex = -1;

            for (let i = 0; i < headers.length; i++) {
                const headerText = headers[i].textContent.trim();
                if (headerText.includes(columnHeader)) {
                    targetColIndex = i;
                    break;
                }
            }

            if (targetColIndex === -1) {
                // Try to find column in table header row (some tables use tr > td for headers)
                const headerRows = table.querySelectorAll('thead tr, tr:first-child');
                for (const row of headerRows) {
                    const cells = row.querySelectorAll('th, td');
                    for (let i = 0; i < cells.length; i++) {
                        if (cells[i].textContent.trim().includes(columnHeader)) {
                            targetColIndex = i;
                            break;
                        }
                    }
                    if (targetColIndex !== -1) break;
                }
            }

            if (targetColIndex === -1) {
                return { error: `找不到列 '${columnHeader}'` };
            }

            // Step 3: Find row by identifier text
            const rows = table.querySelectorAll('tbody tr, tr');
            let targetRow = null;

            for (const row of rows) {
                if (row.textContent.includes(rowIdentifier)) {
                    targetRow = row;
                    break;
                }
            }

            if (!targetRow) {
                return { error: `找不到包含 '${rowIdentifier}' 的行` };
            }

            // Step 4: Get target cell
            const cells = targetRow.querySelectorAll('td');
            if (targetColIndex >= cells.length) {
                return { error: `列索引 ${targetColIndex} 超出范围` };
            }

            const targetCell = cells[targetColIndex];

            // Step 5: Find scrollable container and scroll
            let scrollContainer = table;

            // 查找可滚动的容器（可能是表格的父元素）
            let parent = table.parentElement;
            while (parent) {
                const style = window.getComputedStyle(parent);
                if (style.overflowX === 'auto' || style.overflowX === 'scroll' ||
                    parent.scrollWidth > parent.clientWidth) {
                    scrollContainer = parent;
                    break;
                }
                parent = parent.parentElement;
            }

            // Step 6: Scroll target cell into view
            targetCell.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });

            // Step 7: Find input element in cell
            const inputElement = targetCell.querySelector('input, textarea');
            if (!inputElement) {
                return { error: '目标单元格中没有找到输入框' };
            }

            // Step 8: Input value
            inputElement.focus();
            inputElement.value = '';

            // Simulate typing
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            nativeInputValueSetter.call(inputElement, inputValue);

            // Trigger events for React/Vue
            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            inputElement.dispatchEvent(new Event('change', { bubbles: true }));

            return {
                success: true,
                message: `成功: 在列 '${columnHeader}' 的行 '${rowIdentifier}' 中输入了值: ${inputValue}`
            };
        }"""

        result_str = await page.evaluate(js_code, table_selector, row_identifier, column_header, input_value)

        # 解析结果
        import json
        try:
            result = json.loads(result_str) if result_str else {}
        except json.JSONDecodeError:
            return f"错误: JavaScript 执行返回无效结果: {result_str}"

        if result.get('error'):
            return f"错误: {result['error']}"
        elif result.get('success'):
            logger.info(f"scroll_table_and_input success: {result['message']}")
            return result['message']
        else:
            return f"错误: 未知结果: {result_str}"

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


# Keep old function name for backward compatibility, but it now returns Tools instance
def register_scroll_table_tool(registry=None) -> Tools:
    """Register scroll_table_and_input tool with browser-use.

    Per D-06: Uses Tools.action decorator pattern for browser-use 0.2+ API.

    Args:
        registry: Ignored (kept for backward compatibility).

    Returns:
        Tools instance with scroll_table_and_input action registered.
    """
    return create_tools_with_scroll_table()
