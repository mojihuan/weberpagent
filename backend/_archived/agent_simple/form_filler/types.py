"""表单填写类型定义"""

from pydantic import BaseModel, Field


class GeneratedCode(BaseModel):
    """生成的代码"""
    code: str = Field(description="Playwright 代码片段")
    description: str = Field(description="代码功能描述")
    field_values: dict = Field(default_factory=dict, description="生成的字段值")


class ReviewIssue(BaseModel):
    """审查问题"""
    severity: str = Field(description="严重级别: CRITICAL/HIGH/MEDIUM/LOW")
    line: int | None = Field(default=None, description="行号")
    message: str = Field(description="问题描述")


class ReviewResult(BaseModel):
    """代码审查结果"""
    approved: bool = Field(description="是否通过审查")
    issues: list[ReviewIssue] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class FillResult(BaseModel):
    """表单填写结果"""
    success: bool = Field(description="是否成功")
    screenshot: str | None = Field(default=None, description="验证截图路径")
    code: str | None = Field(default=None, description="最终执行的代码")
    error: str | None = Field(default=None, description="错误信息")