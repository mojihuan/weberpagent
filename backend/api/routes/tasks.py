"""任务管理路由"""

from fastapi import APIRouter, HTTPException

from backend.api.schemas.index import Task, TaskCreate, TaskUpdate
from backend.storage.task_store import TaskStore

router = APIRouter(prefix="/tasks", tags=["tasks"])

task_store = TaskStore()


@router.get("", response_model=list[Task])
async def list_tasks():
    """获取任务列表"""
    return task_store.list()


@router.post("", response_model=Task)
async def create_task(task: TaskCreate):
    """创建任务"""
    return task_store.create(
        name=task.name,
        description=task.description,
        assertions=[a.model_dump() for a in task.assertions],
    )


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """获取任务详情"""
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskUpdate):
    """更新任务"""
    update_data = {k: v for k, v in task.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    updated = task_store.update(task_id, **update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    if not task_store.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted"}
