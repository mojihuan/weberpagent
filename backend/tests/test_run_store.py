"""测试执行记录存储"""

import tempfile
import pytest
from backend.storage.run_store import RunStore
from backend.api.schemas.index import Step, RunResult


@pytest.fixture
def temp_store():
    """使用临时目录的存储"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = RunStore(data_dir=tmpdir)
        yield store


def test_create_run(temp_store):
    """测试创建执行记录"""
    run = temp_store.create(task_id="task-123")
    assert run.id
    assert run.task_id == "task-123"
    assert run.status == "pending"


def test_update_run_status(temp_store):
    """测试更新执行状态"""
    run = temp_store.create(task_id="task-123")
    updated = temp_store.update_status(run.id, "running")
    assert updated is not None
    assert updated.status == "running"


def test_add_step(temp_store):
    """测试添加步骤"""
    run = temp_store.create(task_id="task-123")
    step = Step(step=1, action="click", reasoning="点击按钮")
    # Call add_step method to add step to run
    updated_run = temp_store.add_step(run.id, step)
    # Get the Run object and access updated steps
    assert updated_run is not None
    # Check that steps is a list of Step objects
    assert isinstance(updated_run.steps, list)
    assert len(updated_run.steps) == 1
    # Verify the step object has correct data
    assert updated_run.steps[0].step == 1
    assert updated_run.steps[0].action == "click"


    assert updated_run.steps[0].reasoning == "点击按钮"


def test_get_runs_by_task(temp_store):
    """测试按任务 ID 获取执行记录"""
    temp_store.create(task_id="task-1")
    temp_store.create(task_id="task-1")
    temp_store.create(task_id="task-2")
    runs = temp_store.list_by_task("task-1")
    assert len(runs) == 2


def test_set_result(temp_store):
    """测试设置执行结果"""
    run = temp_store.create(task_id="task-123")
    result = RunResult(
        success=True,
        ai_assertion={"passed": True},
        code_assertion={"passed": True},
        duration_seconds=10.5,
        total_steps=5,
    )
    updated = temp_store.set_result(run.id, result)
    assert updated is not None
    assert updated.result is not None
    assert updated.result.success is True


def test_delete_run(temp_store):
    """测试删除执行记录"""
    run = temp_store.create(task_id="task-123")
    assert temp_store.delete(run.id) is True
    assert temp_store.get(run.id) is None
