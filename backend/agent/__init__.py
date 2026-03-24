"""Agent 模块"""

# Note: UIBrowserAgent import commented out due to missing browser_use_adapter module
# This is a pre-existing issue tracked for future fix.

from .prompts import CHINESE_ENHANCEMENT, LOGIN_TASK_PROMPT
from .tools import register_scroll_table_tool, ScrollTableInputParams

__all__ = [
    # "UIBrowserAgent",  # Commented out - missing dependency
    "CHINESE_ENHANCEMENT",
    "LOGIN_TASK_PROMPT",
    "register_scroll_table_tool",
    "ScrollTableInputParams",
]
