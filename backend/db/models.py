"""SQLAlchemy ORM 模型"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.database import Base


def generate_id() -> str:
    """生成 8 位 ID"""
    return uuid.uuid4().hex[:8]


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_url: Mapped[str] = mapped_column(String(500), default="")
    max_steps: Mapped[int] = mapped_column(Integer, default=10)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, ready
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="task")


class Run(Base):
    """执行记录模型"""
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    task_id: Mapped[str] = mapped_column(String(8), ForeignKey("tasks.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, success, failed, stopped
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    task: Mapped["Task"] = relationship("Task", back_populates="runs")
    steps: Mapped[List["Step"]] = relationship("Step", back_populates="run", order_by="Step.step_index")


class Step(Base):
    """执行步骤模型"""
    __tablename__ = "steps"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), nullable=False)
    step_index: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failed
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    run: Mapped["Run"] = relationship("Run", back_populates="steps")
