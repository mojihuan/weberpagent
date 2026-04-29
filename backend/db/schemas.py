"""Pydantic 请求/响应模型"""

import json
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# === Task Schemas ===

class TaskBase(BaseModel):
    """任务基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    target_url: str = Field(default="", max_length=500)
    max_steps: int = Field(default=10, ge=1, le=100)
    preconditions: Optional[List[str]] = Field(default=None, description="前置条件代码列表")
    assertions: Optional[List[dict[str, Any]]] = Field(default=None, description="业务断言配置列表")
    login_role: Optional[str] = Field(default=None, max_length=20, description="登录角色")


class TaskCreate(TaskBase):
    """创建任务请求"""
    pass


class TaskUpdate(BaseModel):
    """更新任务请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    target_url: Optional[str] = Field(None, max_length=500)
    max_steps: Optional[int] = Field(None, ge=1, le=100)
    status: Optional[str] = Field(None, pattern="^(draft|ready|success)$")
    preconditions: Optional[List[str]] = Field(None, description="前置条件代码列表")
    assertions: Optional[List[dict[str, Any]]] = Field(None, description="业务断言配置列表")
    login_role: Optional[str] = Field(None, max_length=20)


class TaskResponse(BaseModel):
    """任务响应 - 不继承 TaskBase 以避免访问 ORM 关系字段"""
    id: str
    name: str
    description: str
    target_url: str = ""
    max_steps: int = 10
    status: str
    created_at: datetime
    updated_at: datetime
    preconditions: Optional[List[str]] = None
    assertions: Optional[List[dict[str, Any]]] = None
    login_role: Optional[str] = None
    has_code: bool = False
    latest_run_id: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def from_orm_model(cls, data):
        """从 ORM 模型转换，处理 JSON 字段和避免访问关系字段."""
        if hasattr(data, 'external_assertions'):
            # 从 ORM 模型转换
            result = {
                'id': data.id,
                'name': data.name,
                'description': data.description,
                'target_url': data.target_url,
                'max_steps': data.max_steps,
                'status': data.status,
                'created_at': data.created_at,
                'updated_at': data.updated_at,
                'preconditions': data.preconditions,
                'assertions': data.external_assertions,  # 从 external_assertions 读取
                'login_role': data.login_role,
            }
            return result
        return data

    @field_validator('preconditions', 'assertions', mode='before')
    @classmethod
    def deserialize_json_list(cls, v):
        """Deserialize JSON string to list if needed."""
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return None

    model_config = ConfigDict(from_attributes=True)


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
    # 外部断言执行摘要（Phase 25）
    external_assertion_summary: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


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
    step_stats: Optional[dict[str, Any]] = None  # Phase 41, LOG-02
    created_at: datetime

    @field_validator('step_stats', mode='before')
    @classmethod
    def deserialize_step_stats(cls, v):
        """Deserialize JSON string to dict if needed."""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return None

    model_config = ConfigDict(from_attributes=True)


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
    step_stats: Optional[dict[str, Any]] = None  # Phase 41, LOG-02


class SSEFinishedEvent(BaseModel):
    """SSE finished 事件"""
    status: str  # success, failed, stopped
    total_steps: int
    duration_ms: int


class SSEErrorEvent(BaseModel):
    """SSE error 事件"""
    error: str


class SSEPreconditionEvent(BaseModel):
    """SSE precondition 事件"""
    index: int
    code: str
    status: str  # running, success, failed
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    variables: Optional[dict[str, Any]] = None  # 设置的变量


class SSEAssertionEvent(BaseModel):
    """SSE assertion 事件 — UI 断言评估完成后推送"""
    assertion_id: str
    assertion_name: str
    assertion_type: str
    status: str  # pass, fail
    message: Optional[str] = None
    actual_value: Optional[str] = None
    field_results: Optional[list[dict[str, Any]]] = None


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

    model_config = ConfigDict(from_attributes=True)


class ReportDetailResponse(ReportResponse):
    """报告详情响应（包含 steps 和 assertion_results）"""
    steps: List[StepResponse] = []
    assertion_results: List["AssertionResultResponse"] = []
    ui_assertion_results: Optional[List["AssertionResultResponse"]] = None
    pass_rate: Optional[str] = None
    precondition_results: Optional[List[SSEPreconditionEvent]] = None
    timeline_items: Optional[List[dict[str, Any]]] = None  # Phase 59: unified timeline


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


# === Batch Schemas ===

class BatchCreateRequest(BaseModel):
    """批量执行创建请求"""
    task_ids: List[str] = Field(..., min_length=1, max_length=50)
    concurrency: int = Field(default=2, ge=1, le=4)


class BatchRunSummary(BaseModel):
    """批量执行中的 Run 摘要"""
    id: str
    task_id: str
    task_name: Optional[str] = None
    status: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BatchResponse(BaseModel):
    """批量执行响应"""
    id: str
    concurrency: int
    status: str
    created_at: datetime
    finished_at: Optional[datetime] = None
    runs: Optional[List[BatchRunSummary]] = None

    model_config = ConfigDict(from_attributes=True)
