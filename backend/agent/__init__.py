"""Agent 模块"""

# Note: UIBrowserAgent import commented out due to missing browser_use_adapter module
# This is a pre-existing issue tracked for future fix.

from .monitored_agent import MonitoredAgent
from .pre_submit_guard import PreSubmitGuard
from .prompts import CHINESE_ENHANCEMENT, LOGIN_TASK_PROMPT
from .stall_detector import StallDetector
from .task_progress_tracker import TaskProgressTracker

__all__ = [
    # "UIBrowserAgent",  # Commented out - missing dependency
    "CHINESE_ENHANCEMENT",
    "LOGIN_TASK_PROMPT",
    "MonitoredAgent",
    "PreSubmitGuard",
    "StallDetector",
    "TaskProgressTracker",
]
