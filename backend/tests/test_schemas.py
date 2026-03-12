"""测试 Pydantic 数据模型"""

import pytest
from datetime import datetime
from backend.api.schemas.index import Task, Run, Step, Assertion, RunResult


def test_assertion_creation():
    """测试断言模型创建"""
    assertion = Assertion(name="URL检查", type="url_contains", expected="/dashboard")
    assert assertion.name == "URL检查"
    assert assertion.type == "url_contains"
    assert assertion.expected == "/dashboard"


def test_task_creation():
    """测试任务模型创建"""
    task = Task(
        id="test-123",
        name="登录测试",
        description="测试登录功能",
        assertions=[
            Assertion(name="URL检查", type="url_contains", expected="/dashboard")
        ],
    )
    assert task.id == "test-123"
    assert task.name == "登录测试"
    assert len(task.assertions) == 1


def test_step_creation():
    """测试步骤模型创建"""
    step = Step(
        step=1,
        action="click",
        reasoning="点击登录按钮",
        screenshot="/screenshots/1.png",
    )
    assert step.step == 1
    assert step.action == "click"


def test_run_result_creation():
    """测试执行结果模型创建"""
    result = RunResult(
        success=True,
        ai_assertion={"passed": True},
        code_assertion={"passed": True},
        duration_seconds=10.5,
        total_steps=5,
    )
    assert result.success is True
    assert result.total_steps == 5


def test_run_creation():
    """测试执行记录模型创建"""
    run = Run(
        id="run-123",
        task_id="task-123",
        status="pending",
        steps=[],
    )
    assert run.id == "run-123"
    assert run.status == "pending"
