"""测试任务存储"""

import os
import tempfile
import pytest
from backend.storage.task_store import TaskStore
from backend.api.schemas.index import Task, Assertion


@pytest.fixture
def temp_store():
    """使用临时目录的存储"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = TaskStore(data_dir=tmpdir)
        yield store


def test_create_task(temp_store):
    """测试创建任务"""
    task = temp_store.create(
        name="登录测试",
        description="测试登录功能",
        assertions=[Assertion(name="URL", type="url_contains", expected="/dashboard")],
    )
    assert task.id
    assert task.name == "登录测试"


def test_get_task(temp_store):
    """测试获取任务"""
    created = temp_store.create(name="测试", description="描述")
    found = temp_store.get(created.id)
    assert found is not None
    assert found.id == created.id


def test_list_tasks(temp_store):
    """测试列出任务"""
    temp_store.create(name="任务1", description="描述1")
    temp_store.create(name="任务2", description="描述2")
    tasks = temp_store.list()
    assert len(tasks) == 2


def test_update_task(temp_store):
    """测试更新任务"""
    created = temp_store.create(name="原名称", description="原描述")
    updated = temp_store.update(created.id, name="新名称")
    assert updated is not None
    assert updated.name == "新名称"


def test_delete_task(temp_store):
    """测试删除任务"""
    created = temp_store.create(name="测试", description="描述")
    assert temp_store.delete(created.id) is True
    assert temp_store.get(created.id) is None
