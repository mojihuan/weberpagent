"""数据库操作封装"""

import json
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.db.models import Task, Run, Step, Report, AssertionResult, PreconditionResult, Batch
from backend.db.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    """任务仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _serialize_preconditions(self, preconditions: List[str] | None) -> str | None:
        """Serialize preconditions list to JSON string."""
        if preconditions is None:
            return None
        return json.dumps(preconditions, ensure_ascii=False)

    def _deserialize_preconditions(self, preconditions: str | None) -> List[str] | None:
        """Deserialize preconditions JSON string to list."""
        if preconditions is None:
            return None
        return json.loads(preconditions)

    async def create(self, data: TaskCreate) -> Task:
        task_data = data.model_dump()
        if task_data.get("preconditions") is not None:
            task_data["preconditions"] = self._serialize_preconditions(task_data["preconditions"])
        # assertions (业务断言配置) 存储到 external_assertions 字段
        # Task.assertions 是 SQLAlchemy 关系字段，不能直接赋值
        assertions_val = task_data.pop("assertions", None)
        if assertions_val is not None:
            task_data["external_assertions"] = json.dumps(
                assertions_val, ensure_ascii=False
            )
        task = Task(**task_data)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: str) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id).options(
            selectinload(Task.assertions), selectinload(Task.runs)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, status: Optional[str] = None) -> List[Task]:
        stmt = select(Task).options(selectinload(Task.assertions), selectinload(Task.runs))
        if status:
            stmt = stmt.where(Task.status == status)
        stmt = stmt.order_by(Task.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def update(self, task_id: str, data: TaskUpdate) -> Optional[Task]:
        task = await self.session.get(Task, task_id)
        if not task:
            return None
        update_data = data.model_dump(exclude_unset=True)
        if "preconditions" in update_data and update_data["preconditions"] is not None:
            update_data["preconditions"] = self._serialize_preconditions(update_data["preconditions"])
        # assertions (业务断言配置) 存储到 external_assertions 字段
        if "assertions" in update_data and update_data["assertions"] is not None:
            update_data["external_assertions"] = json.dumps(
                update_data["assertions"], ensure_ascii=False
            )
            del update_data["assertions"]
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: str) -> bool:
        task = await self.get(task_id)
        if not task:
            return False

        # 先删除关联的 runs（会级联删除 steps、reports、assertion_results）
        from sqlalchemy import delete as sql_delete
        await self.session.execute(sql_delete(Run).where(Run.task_id == task_id))
        await self.session.execute(sql_delete(Report).where(Report.task_id == task_id))

        await self.session.delete(task)
        await self.session.commit()
        return True


class RunRepository:
    """执行记录仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_id: str) -> Run:
        run = Run(task_id=task_id, status="pending")
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get(self, run_id: str) -> Optional[Run]:
        return await self.session.get(Run, run_id)

    async def get_with_task(self, run_id: str) -> Optional[Run]:
        """获取执行记录及其关联的任务（包含断言）"""
        stmt = (
            select(Run)
            .where(Run.id == run_id)
            .options(
                selectinload(Run.task).selectinload(Task.assertions)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, task_id: Optional[str] = None) -> List[Run]:
        stmt = select(Run)
        if task_id:
            stmt = stmt.where(Run.task_id == task_id)
        stmt = stmt.order_by(Run.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def list_with_details(self) -> List[Run]:
        """获取执行列表，包含任务名称和步骤数"""
        stmt = (
            select(Run)
            .options(
                selectinload(Run.task),
                selectinload(Run.steps),
            )
            .order_by(Run.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def update_status(self, run_id: str, status: str) -> Optional[Run]:
        run = await self.get(run_id)
        if not run:
            return None
        run.status = status
        if status == "running":
            run.started_at = datetime.now()
        elif status in ("success", "failed", "stopped"):
            run.finished_at = datetime.now()
        await self.session.commit()
        return run

    async def update_generated_code_path(self, run_id: str, path: str) -> None:
        """更新生成代码路径 (Phase 82, CODE-01)"""
        run = await self.get(run_id)
        if run:
            run.generated_code_path = path
            await self.session.commit()

    async def update_healing_status(
        self,
        run_id: str,
        status: str,
        attempts: int,
        error: str | None = None,
        code_path: str | None = None,
        error_category: str = "",
    ) -> None:
        """更新自愈状态 (Phase 85, HEAL-03)"""
        run = await self.get(run_id)
        if run:
            run.healing_status = status
            run.healing_attempts = attempts
            run.healing_error = error
            run.healing_error_category = error_category
            if code_path is not None:
                run.generated_code_path = code_path
            await self.session.commit()

    async def add_step(self, run_id: str, step_data: dict) -> Step:
        """Add a step to a run.

        Args:
            run_id: The run ID
            step_data: Dict with step fields. Required: step_index, action, status.
                      Optional: reasoning, screenshot_path, error, duration_ms,
                      loop_intervention (JSON string, Phase 39 LOG-01).

        Returns:
            The created Step instance
        """
        step = Step(run_id=run_id, **step_data)
        self.session.add(step)
        await self.session.commit()
        await self.session.refresh(step)
        return step

    async def get_steps(self, run_id: str) -> List[Step]:
        """Get all steps for a run, ordered by step_index."""
        stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
        result = await self.session.execute(stmt)
        return list(result.scalars())


class StepRepository:
    """步骤仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, step_id: str) -> Optional[Step]:
        return await self.session.get(Step, step_id)

    async def list_by_run(self, run_id: str) -> List[Step]:
        stmt = select(Step).where(Step.run_id == run_id).order_by(Step.step_index)
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def get_by_index(self, run_id: str, step_index: int) -> Optional[Step]:
        stmt = select(Step).where(Step.run_id == run_id, Step.step_index == step_index)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class ReportRepository:
    """报告仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        run_id: str,
        task_id: str,
        task_name: str,
        status: str,
        total_steps: int,
        success_steps: int,
        failed_steps: int,
        duration_ms: int,
    ) -> Report:
        report = Report(
            run_id=run_id,
            task_id=task_id,
            task_name=task_name,
            status=status,
            total_steps=total_steps,
            success_steps=success_steps,
            failed_steps=failed_steps,
            duration_ms=duration_ms,
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def get(self, report_id: str) -> Optional[Report]:
        return await self.session.get(Report, report_id)

    async def get_by_run_id(self, run_id: str) -> Optional[Report]:
        stmt = select(Report).where(Report.run_id == run_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        status: Optional[str] = None,
        date: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[List[Report], int]:
        stmt = select(Report)

        # 状态筛选
        if status and status != "all":
            stmt = stmt.where(Report.status == status)

        # 日期筛选
        if date:
            now = datetime.now()
            if date == "today":
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date == "7days":
                start = now - timedelta(days=7)
            elif date == "30days":
                start = now - timedelta(days=30)
            else:
                start = None

            if start:
                stmt = stmt.where(Report.created_at >= start)

        # 统计总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(count_stmt)).scalar()

        # 分页
        stmt = stmt.order_by(Report.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.session.execute(stmt)
        reports = list(result.scalars())

        return reports, total


class AssertionResultRepository:
    """断言结果仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        run_id: str,
        assertion_id: str,
        status: str,
        message: str | None = None,
        actual_value: str | None = None,
        sequence_number: int | None = None,
    ) -> AssertionResult:
        """Create and persist assertion result."""
        result = AssertionResult(
            run_id=run_id,
            assertion_id=assertion_id,
            status=status,
            message=message,
            actual_value=actual_value,
            sequence_number=sequence_number,
        )
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def list_by_run(self, run_id: str) -> List[AssertionResult]:
        """List all assertion results for a run."""
        stmt = (
            select(AssertionResult)
            .where(AssertionResult.run_id == run_id)
            .options(selectinload(AssertionResult.assertion))
            .order_by(AssertionResult.created_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def update_sequence_number(self, result_id: str, sequence_number: int) -> None:
        """Update sequence_number on an existing AssertionResult."""
        from sqlalchemy import update
        stmt = (
            update(AssertionResult)
            .where(AssertionResult.id == result_id)
            .values(sequence_number=sequence_number)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_with_sequence(
        self,
        run_id: str,
        assertion_id: str,
        status: str,
        message: str | None = None,
        actual_value: str | None = None,
        sequence_number: int | None = None,
    ) -> AssertionResult:
        """Create assertion result with optional sequence_number."""
        result = AssertionResult(
            run_id=run_id,
            assertion_id=assertion_id,
            status=status,
            message=message,
            actual_value=actual_value,
            sequence_number=sequence_number,
        )
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result


class PreconditionResultRepository:
    """前置条件结果仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        run_id: str,
        sequence_number: int,
        index: int,
        code: str,
        status: str,
        error: str | None = None,
        duration_ms: int | None = None,
        variables: str | None = None,
    ) -> PreconditionResult:
        result = PreconditionResult(
            run_id=run_id,
            sequence_number=sequence_number,
            index=index,
            code=code,
            status=status,
            error=error,
            duration_ms=duration_ms,
            variables=variables,
        )
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def list_by_run(self, run_id: str) -> List[PreconditionResult]:
        stmt = (
            select(PreconditionResult)
            .where(PreconditionResult.run_id == run_id)
            .order_by(PreconditionResult.sequence_number)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())


class BatchRepository:
    """批量执行批次仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, concurrency: int = 2) -> Batch:
        batch = Batch(concurrency=concurrency, status="pending")
        self.session.add(batch)
        await self.session.commit()
        await self.session.refresh(batch)
        return batch

    async def get(self, batch_id: str) -> Optional[Batch]:
        return await self.session.get(Batch, batch_id)

    async def get_with_runs(self, batch_id: str) -> Optional[Batch]:
        stmt = (
            select(Batch)
            .where(Batch.id == batch_id)
            .options(selectinload(Batch.runs).selectinload(Run.task))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(self, batch_id: str, status: str, finished_at: Optional[datetime] = None) -> Optional[Batch]:
        batch = await self.get(batch_id)
        if not batch:
            return None
        batch.status = status
        if finished_at:
            batch.finished_at = finished_at
        await self.session.commit()
        return batch

    async def list_runs_by_batch(self, batch_id: str) -> List[Run]:
        stmt = (
            select(Run)
            .where(Run.batch_id == batch_id)
            .options(selectinload(Run.task))
            .order_by(Run.created_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())
