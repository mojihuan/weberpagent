# backend/core/event_manager.py
"""SSE 事件管理器 - 管理执行事件的发布和订阅"""

import asyncio
from collections import defaultdict
from typing import AsyncGenerator


class EventManager:
    """
    管理执行事件的发布和订阅

    - 存储事件历史，支持重新连接
    - 支持多个并发订阅者
    - 自动清理完成的执行
    """

    def __init__(self):
        # run_id -> 事件列表
        self._events: dict[str, list[str | None]] = defaultdict(list)
        # run_id -> 订阅者队列列表
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)
        # run_id -> 执行状态
        self._status: dict[str, str] = {}

    async def publish(self, run_id: str, event: str | None) -> None:
        """
        发布事件到指定 run

        Args:
            run_id: 执行 ID
            event: SSE 事件字符串，None 表示执行结束
        """
        # 存储事件历史
        if event is not None:
            self._events[run_id].append(event)

        # 通知所有订阅者
        for queue in self._subscribers.get(run_id, []):
            await queue.put(event)

    async def subscribe(self, run_id: str) -> AsyncGenerator[str | None, None]:
        """
        订阅 run 的事件流

        Args:
            run_id: 执行 ID

        Yields:
            SSE 事件字符串，None 表示流结束
        """
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        self._subscribers[run_id].append(queue)

        try:
            # 先发送历史事件
            for event in self._events.get(run_id, []):
                yield event

            # 如果已经完成，直接结束
            if self.is_finished(run_id):
                return

            # 等待新事件
            while True:
                event = await queue.get()
                yield event
                if event is None:  # 结束信号
                    break
        finally:
            # 移除订阅者
            if queue in self._subscribers[run_id]:
                self._subscribers[run_id].remove(queue)

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


# 全局单例
event_manager = EventManager()
