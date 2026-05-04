# backend/core/event_manager.py
"""SSE 事件管理器 - 管理执行事件的发布和订阅"""

import asyncio
import logging
from collections import defaultdict
from typing import AsyncGenerator

logger = logging.getLogger(__name__)


class EventManager:
    """
    管理执行事件的发布和订阅

    - 存储事件历史，支持重新连接
    - 支持多个并发订阅者
    - 自动清理完成的执行
    - 支持 SSE 心跳以保持连接活跃
    """

    def __init__(self, heartbeat_interval: float = 20.0):
        """
        初始化 EventManager

        Args:
            heartbeat_interval: 心跳间隔（秒），默认 20 秒
        """
        # run_id -> 事件列表
        self._events: dict[str, list[str | None]] = defaultdict(list)
        # run_id -> 订阅者队列列表
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)
        # run_id -> 执行状态
        self._status: dict[str, str] = {}
        # 心跳间隔（秒）
        self._heartbeat_interval = heartbeat_interval
        # run_id -> 心跳任务
        self._heartbeat_tasks: dict[str, asyncio.Task] = {}

    async def publish(self, run_id: str, event: str | None) -> None:
        """
        发布事件到指定 run

        Per-queue exception isolation: a failing queue does not prevent
        other subscribers from receiving the event.

        Args:
            run_id: 执行 ID
            event: SSE 事件字符串，None 表示执行结束
        """
        # 存储事件历史
        if event is not None:
            self._events[run_id].append(event)

        # 通知所有订阅者（隔离每个 queue 的异常）
        for queue in self._subscribers.get(run_id, []):
            try:
                await queue.put(event)
            except Exception:
                logger.warning(f"[{run_id}] Failed to put event to subscriber queue, skipping")

    async def _send_heartbeat(self, run_id: str) -> None:
        """
        后台任务：周期性发送心跳注释

        SSE 注释格式 (:heartbeat) 会被 EventSource 客户端忽略，
        用于保持连接活跃。

        Args:
            run_id: 执行 ID
        """
        while not self.is_finished(run_id):
            await asyncio.sleep(self._heartbeat_interval)
            if not self.is_finished(run_id):
                # 发布心跳注释到所有订阅者
                for queue in self._subscribers.get(run_id, []):
                    await queue.put(":heartbeat\n\n")

    async def subscribe(self, run_id: str) -> AsyncGenerator[str | None, None]:
        """
        订阅 run 的事件流（带心跳支持）

        Args:
            run_id: 执行 ID

        Yields:
            SSE 事件字符串（包括心跳注释），None 表示流结束
        """
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        self._subscribers[run_id].append(queue)

        # 启动心跳任务（先取消同一 run_id 的旧 task，防止 task 泄漏）
        existing_task = self._heartbeat_tasks.get(run_id)
        if existing_task is not None and not existing_task.done():
            existing_task.cancel()
            try:
                await existing_task
            except asyncio.CancelledError:
                pass
        heartbeat_task = asyncio.create_task(self._send_heartbeat(run_id))
        self._heartbeat_tasks[run_id] = heartbeat_task

        try:
            # 先发送历史事件
            for event in self._events.get(run_id, []):
                yield event

            # 如果已经完成，直接结束
            if self.is_finished(run_id):
                return

            # 等待新事件（包括心跳）
            while True:
                event = await queue.get()
                yield event
                if event is None:  # 结束信号
                    break
        finally:
            # 移除订阅者
            if queue in self._subscribers[run_id]:
                self._subscribers[run_id].remove(queue)

            # 取消心跳任务
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass

            # 清理心跳任务引用
            if run_id in self._heartbeat_tasks:
                del self._heartbeat_tasks[run_id]

    def set_status(self, run_id: str, status: str) -> None:
        """
        设置执行状态

        Args:
            run_id: 执行 ID
            status: 状态 (running, success, failed, stopped)
        """
        self._status[run_id] = status

    def is_finished(self, run_id: str) -> bool:
        """
        检查执行是否已结束

        Args:
            run_id: 执行 ID

        Returns:
            True 如果执行已成功或失败
        """
        return self._status.get(run_id) in ("success", "failed", "stopped")

    def cleanup(self, run_id: str) -> None:
        """
        清理执行资源

        Args:
            run_id: 执行 ID
        """
        if run_id in self._events:
            del self._events[run_id]
        if run_id in self._subscribers:
            del self._subscribers[run_id]
        if run_id in self._status:
            del self._status[run_id]
        if run_id in self._heartbeat_tasks:
            del self._heartbeat_tasks[run_id]


# 全局单例
event_manager = EventManager()
