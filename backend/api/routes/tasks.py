"""任务管理路由"""

import json as json_module
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from backend.api.helpers import _build_task_dict, raise_not_found
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.db.models import Task
from backend.db.schemas import TaskCreate, TaskUpdate, TaskResponse
from backend.db.repository import TaskRepository
from backend.utils.excel_template import generate_template
from backend.utils.excel_parser import parse_excel


router = APIRouter(prefix="/tasks", tags=["tasks"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


async def _validate_upload_file(file: UploadFile) -> bytes:
    """Validate upload file format and size. Returns file content bytes."""
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="仅支持 .xlsx 格式文件")
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="文件为空")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过 5MB")
    return content


def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


@router.get("/template")
async def download_template():
    """下载测试用例 Excel 模版"""
    buffer = generate_template()
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=task_template.xlsx"},
    )


@router.post("/import/preview")
async def import_preview(file: UploadFile = File(...)):
    """Preview parsed Excel rows with validation status before committing."""
    content = await _validate_upload_file(file)
    result = parse_excel(BytesIO(content))
    return {
        "rows": [
            {
                "row_number": row.row_number,
                "data": row.data,
                "errors": row.errors,
                "valid": len(row.errors) == 0,
            }
            for row in result.rows
        ],
        "total_rows": result.total_rows,
        "valid_count": sum(1 for r in result.rows if not r.errors),
        "error_count": sum(1 for r in result.rows if r.errors),
        "has_errors": result.has_errors,
    }


@router.post("/import/confirm")
async def import_confirm(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Re-parse Excel and batch create Tasks atomically.

    Uses async with db.begin() so any failure rolls back ALL inserts.
    """
    content = await _validate_upload_file(file)
    result = parse_excel(BytesIO(content))

    if result.has_errors:
        raise HTTPException(status_code=400, detail="文件包含无效行，无法导入。请返回检查数据")

    created_count = 0
    async with db.begin():
        for row in result.rows:
            task_data = dict(row.data)  # Copy because we mutate
            # Serialize preconditions to JSON string (same as TaskRepository.create)
            preconditions = task_data.get("preconditions")
            if preconditions is not None:
                task_data["preconditions"] = json_module.dumps(preconditions, ensure_ascii=False)
            # Map "assertions" key to "external_assertions" column
            assertions = task_data.pop("assertions", None)
            if assertions is not None:
                task_data["external_assertions"] = json_module.dumps(assertions, ensure_ascii=False)
            task = Task(**task_data, status="draft")
            db.add(task)
            created_count += 1
    # Transaction commits on block exit. Any exception rolls back all.

    return {"status": "success", "created_count": created_count}


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    repo: TaskRepository = Depends(get_task_repo),
):
    tasks = await repo.list()
    results = []
    for task in tasks:
        task_dict = _build_task_dict(task)
        results.append(TaskResponse.model_validate(task_dict))
    return results


@router.post("", response_model=TaskResponse)
async def create_task(
    data: TaskCreate,
    repo: TaskRepository = Depends(get_task_repo),
):
    return await repo.create(data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    repo: TaskRepository = Depends(get_task_repo),
):
    task = await repo.get(task_id)
    if not task:
        raise_not_found("Task", task_id)
    return TaskResponse.model_validate(_build_task_dict(task))


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    repo: TaskRepository = Depends(get_task_repo),
):
    if not data.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No update data provided")

    updated = await repo.update(task_id, data)
    if not updated:
        raise_not_found("Task", task_id)
    return updated


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    repo: TaskRepository = Depends(get_task_repo),
):
    if not await repo.delete(task_id):
        raise_not_found("Task", task_id)
    return {"status": "deleted"}
