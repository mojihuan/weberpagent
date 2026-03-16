"""Pydantic 请求/响应模型"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# === Task Schemas ===

class TaskBase(BaseModel):
    """任务基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    target_url: str = Field(default="", max_length=500)
    max_steps: int = Field(default=10, ge=1, le=100)
    preconditions: Optional[List[str]] = Field(default=None, description="前置条件代码列表")


class TaskCreate(TaskBase):
    """创建任务请求"""
    pass


class TaskUpdate(BaseModel):
    """更新任务请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    target_url: Optional[str] = Field(None, max_length=500)
    max_steps: Optional[int] = Field(None, ge=1, le=100)
    status: Optional[str] = Field(None, pattern="^(draft|ready)$")
    preconditions: Optional[List[str]] = Field(None, description="前置条件代码列表")


class TaskResponse(TaskBase):
    """任务响应"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    preconditions: Optional[List[str]] = None

    class Config:
        from_attributes = True


# === Run Schemas ===

class RunCreate(BaseModel):
    """创建执行请求"""
    task_id: str


class RunResponse(BaseModel):
    """执行响应"""
    id: str
    task_id: str
    status: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime
    # 额外字段（列表页需要）
    task_name: Optional[str] = None
    steps_count: int = 0

    class Config:
        from_attributes = True


# === Step Schemas ===

class StepResponse(BaseModel):
    """步骤响应"""
    id: str
    run_id: str
    step_index: int
    action: str
    reasoning: Optional[str] = None
    screenshot_url: Optional[str] = None  # 前端访问 URL
    status: str
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# === SSE Event Schemas ===

class SSEStartedEvent(BaseModel):
    """SSE started 事件"""
    run_id: str
    task_id: str
    task_name: str


class SSEStepEvent(BaseModel):
    """SSE step 事件"""
    index: int
    action: str
    reasoning: Optional[str] = None
    screenshot_url: Optional[str] = None
    status: str
    duration_ms: Optional[int] = None


class SSEFinishedEvent(BaseModel):
    """SSE finished 事件"""
    status: str  # success, failed, stopped
    total_steps: int
    duration_ms: int


class SSEErrorEvent(BaseModel):
    """SSE error 事件"""
    error: str


# === Report Schemas ===

class ReportResponse(BaseModel):
    """报告响应"""
    id: str
    run_id: str
    task_id: str
    task_name: str
    status: str  # success, failed
    total_steps: int
    success_steps: int
    failed_steps: int
    duration_ms: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReportDetailResponse(ReportResponse):
    """报告详情响应（包含 steps 和 assertion_results）"""
    steps: List[StepResponse] = []
    assertion_results: List["AssertionResultResponse"] = []


class ReportListParams(BaseModel):
    """报告列表查询参数"""
    status: Optional[str] = None  # success, failed, all
    date: Optional[str] = None
    page: int = 1
    page_size: int = 10


# === Assertion Schemas ===


class AssertionResponse(BaseModel):
    """断言响应"""
    id: str
    task_id: str
    name: str
    type: str  # url_contains, text_exists, no_errors
    expected: str
    created_at: datetime

    class Config:
        from_attributes = True


class AssertionCreate(BaseModel):
    """创建断言请求"""
    name: str = Field(..., min_length=1, max_length=200)
    type: str = Field(..., pattern="^(url_contains|text_exists|no_errors)$")
    expected: str = Field(..., min_length=1)


# === AssertionResult Schemas ===


class AssertionResultResponse(BaseModel):
    """断言结果响应"""
    id: str
    run_id: str
    assertion_id: str
    status: str  # pass, fail
    message: Optional[str] = None
    actual_value: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
