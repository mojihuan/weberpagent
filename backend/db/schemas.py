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


class TaskResponse(TaskBase):
    """任务响应"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

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
