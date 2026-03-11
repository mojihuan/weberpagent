# backend/agent_simple/form_filler/types.py
"""表单填写类型定义 - 占位文件"""

# TODO: 后续任务填充具体定义
from dataclasses import dataclass
from typing import Optional


@dataclass
class GeneratedCode:
    """生成的代码 - 占位"""
    code: str
    explanation: Optional[str] = None


@dataclass
class ReviewIssue:
    """审查问题 - 占位"""
    severity: str  # "error", "warning", "info"
    message: str
    line: Optional[int] = None


@dataclass
class ReviewResult:
    """审查结果 - 占位"""
    approved: bool
    issues: list[ReviewIssue]


@dataclass
class FillResult:
    """填写结果 - 占位"""
    success: bool
    message: str