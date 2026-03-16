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
    # 前置条件（JSON 字符串数组）
    preconditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 关系
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="task")
    assertions: Mapped[List["Assertion"]] = relationship(
        "Assertion", back_populates="task", cascade="all, delete-orphan"
    )


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
    assertion_results: Mapped[List["AssertionResult"]] = relationship(
        "AssertionResult", back_populates="run", cascade="all, delete-orphan"
    )


class Assertion(Base):
    """断言模型"""
    __tablename__ = "assertions"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    task_id: Mapped[str] = mapped_column(String(8), ForeignKey("tasks.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # url_contains, text_exists, no_errors
    expected: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string or plain text
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    task: Mapped["Task"] = relationship("Task", back_populates="assertions")
    results: Mapped[List["AssertionResult"]] = relationship("AssertionResult", back_populates="assertion")


class AssertionResult(Base):
    """断言结果模型"""
    __tablename__ = "assertion_results"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), nullable=False)
    assertion_id: Mapped[str] = mapped_column(String(8), ForeignKey("assertions.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # pass, fail
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # explanation
    actual_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # actual captured value
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    run: Mapped["Run"] = relationship("Run", back_populates="assertion_results")
    assertion: Mapped["Assertion"] = relationship("Assertion", back_populates="results")


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


class Report(Base):
    """报告模型"""
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(8), primary_key=True, default=generate_id)
    run_id: Mapped[str] = mapped_column(String(8), ForeignKey("runs.id"), unique=True, nullable=False)
    task_id: Mapped[str] = mapped_column(String(8), ForeignKey("tasks.id"), nullable=False)
    task_name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # success, failed
    total_steps: Mapped[int] = mapped_column(Integer, default=0)
    success_steps: Mapped[int] = mapped_column(Integer, default=0)
    failed_steps: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # 关系
    run: Mapped["Run"] = relationship("Run", backref="report", uselist=False)
