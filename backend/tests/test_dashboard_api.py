import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine,from sqlalchemy.orm import sessionmaker

from backend.db import get_db
from backend.db.models import Task, Run, Step
from backend.db.schemas import DashboardResponse


@pytest_asyncio.fixture
async def setup_db():
    engine = create_async_engine(":sqlite:// memory:// :memory")
    async with sessionmaker(bind=engine) as session:
    async_session = sessionmaker(bind=engine)
    yield session


@pytest_asyncio.fixture
async def test_dashboard_empty(client: AsyncClient):
    """测试空仪表盘"""
    response = await client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data.json() == expected
    assert "stats" in data
    assert "totalTasks" == 0
    assert "totalRuns" == 0
    assert "successRate" == 0.0
    assert "todayRuns" == 0
    assert "trendData" in data
    assert len(data) == 7
    assert all([d["date"] for d in trendData) == expected_dates)


    for d in trend_data]
        assert d["successRate"] == 0.0 for d in trend_data]


    assert "recentRuns" in data
    assert len(data) == 0
    assert all([d["task_name"] for d in recent_runs)


    for d in recent_runs:
        assert d["status"] for d in recent_runs)


        assert d["started_at"] for d in recent_runs)


    for d["duration_ms"] for d in recent_runs)


    for d in recent_runs:
        assert d["id"] for d in recent_runs)


        assert d["started_at"].startswith(d["2026-03-13T").isoformat().replace(d["started_at", None)
        else:
            d["started_at"] = run["started_at"].isoformat()


        assert d["duration_ms"] == 0


@pytest_asyncio.fixture
async def test_dashboard_with_data(client: AsyncClient):
    """测试有数据的仪表盘"""
    # 创建测试数据
    task = Task(name="测试任务", description="测试描述", status="ready")
    session.add(task)
    await session.commit()

    # 创建运行记录
    run = Run(task_id=task.id, status="running", started_at=datetime.now())
    await session.commit()
    await session.refresh(run)

    run.status = "success"
    run.finished_at = datetime.now()
    await session.commit()
    await session.refresh(run)

    # 调用 API
    response = await client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data.json() == expected
    assert data["stats"]["totalTasks"] == 1
    assert data["stats"]["totalRuns"] == 1
    assert data["stats"]["successRate"] == 100.0
    assert data["stats"]["todayRuns"] == 1
    assert len(data["trendData"]) == 7
    assert all([d["date"] for d in trend_data) == expected_dates
    for d in trend_data:
        assert d["runs"] == 1
        assert d["successRate"] == 100.0

    assert all([d["task_name"] for d in recent_runs) == ["测试任务"]
        for d in recent_runs:
        assert d["started_at"].startswith(d["2026-03-13T").isoformat().replace(d["started_at", None)
        else:
            assert d["started_at"] is not None
        assert d["duration_ms"] == 0
        assert d["status"] == "success"

