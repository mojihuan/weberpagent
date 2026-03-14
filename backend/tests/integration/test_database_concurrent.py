import pytest
import asyncio
import time
import uuid
from backend.db.database import async_session, engine
from backend.db.models import Task
from sqlalchemy import select


@pytest.mark.asyncio
async def test_concurrent_writes_dont_block():
    """Multiple concurrent writes complete without blocking"""
    # Use UUIDs to avoid conflicts with existing data
    test_ids = [f"concurrent-test-{uuid.uuid4()}" for _ in range(5)]

    async def create_task(task_id: str, i: int):
        async with async_session() as session:
            task = Task(
                id=task_id,
                name=f"Concurrent Task {i}",
                description=f"Test task {i}",
                status="draft",
            )
            session.add(task)
            await session.commit()
            return task.id

    # Create 5 tasks concurrently
    start = time.time()
    tasks = [create_task(test_ids[i], i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    assert len(results) == 5, "All tasks should be created"
    assert elapsed < 5.0, "Should complete quickly (<5s) if not blocking"


@pytest.mark.asyncio
async def test_concurrent_reads_work():
    """Multiple concurrent reads work correctly"""
    async def read_tasks():
        async with async_session() as session:
            result = await session.execute(select(Task))
            return result.scalars().all()

    # Run 10 concurrent reads
    tasks = [read_tasks() for _ in range(10)]
    results = await asyncio.gather(*tasks)

    assert len(results) == 10, "All reads should complete"


@pytest.fixture(autouse=True)
async def cleanup_concurrent_test_tasks():
    """Clean up test tasks after each test using UUID pattern"""
    yield
    async with async_session() as session:
        # Delete all tasks matching our test pattern
        result = await session.execute(
            select(Task).where(Task.id.like("concurrent-test-%"))
        )
        tasks = result.scalars().all()
        for task in tasks:
            await session.delete(task)
        await session.commit()
