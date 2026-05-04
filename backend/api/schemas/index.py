"""Pydantic 数据模型定义"""

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field


class Assertion(BaseModel):
    """断言模型"""

    name: str = Field(..., description="断言名称")
    type: Literal["url_contains", "text_exists", "no_errors", "element_exists"] = Field(
        ..., description="断言类型"
    )
    expected: str | bool = Field(..., description="期望值")


class Task(BaseModel):
    """任务模型"""

    id: str = Field(..., description="任务 ID")
    name: str = Field(..., description="任务名称")
    description: str = Field(..., description="自然语言任务描述")
    target_url: str = Field(default="", description="目标 URL")
    max_steps: int = Field(default=10, description="最大执行步数")
    status: Literal["draft", "ready"] = Field(default="draft", description="任务状态")
    assertions: list[Assertion] = Field(default_factory=list, description="断言列表")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")


class Step(BaseModel):
    """执行步骤模型"""

    step: int = Field(..., description="步骤编号")
    action: str = Field(..., description="动作类型")
    reasoning: str = Field(default="", description="AI 推理")
    screenshot: str | None = Field(default=None, description="截图路径")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class RunResult(BaseModel):
    """执行结果模型"""

    success: bool = Field(..., description="是否成功")
    ai_assertion: dict[str, Any] = Field(default_factory=dict, description="AI 断言结果")
    code_assertion: dict[str, Any] = Field(default_factory=dict, description="代码断言结果")
    duration_seconds: float = Field(..., description="执行时长")
    total_steps: int = Field(..., description="总步数")


class Run(BaseModel):
    """执行记录模型"""

    id: str = Field(..., description="执行 ID")
    task_id: str = Field(..., description="关联任务 ID")
    status: Literal["pending", "running", "completed", "failed"] = Field(
        default="pending", description="执行状态"
    )
    steps: list[Step] = Field(default_factory=list, description="执行步骤")
    result: RunResult | None = Field(default=None, description="执行结果")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    started_at: datetime | None = Field(default=None, description="开始时间")
    completed_at: datetime | None = Field(default=None, description="完成时间")


class TaskCreate(BaseModel):
    """创建任务请求模型"""

    name: str
    description: str
    assertions: list[Assertion] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """更新任务请求模型"""

    name: str | None = None
    description: str | None = None
    assertions: list[Assertion] | None = None
