"""任务管理路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db, init_db, Task
 from backend.db.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.db.repository import TaskRepository


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    repo: TaskRepository = Depends(get_db),
):
    return await repo.list()


@router.post("", response_model=TaskResponse)
async def create_task(
    data: TaskCreate,
    repo: TaskRepository = Depends(get_db),
):
    return await repo.create(data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    repo: TaskRepository = Depends(get_db),
):
    task = await repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    repo: TaskRepository = Depends(get_db),
):
    if not data.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No update data provided")

    updated = await repo.update(task_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    repo: TaskRepository = Depends(get_db),
):
    if not await repo.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted"}
