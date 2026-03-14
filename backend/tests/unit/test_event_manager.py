# backend/tests/unit/test_event_manager.py
"""EventManager 单元测试 - 包含 SSE 心跳功能测试"""

import asyncio

import pytest

from backend.core.event_manager import EventManager


class TestEventManager:
    """EventManager 基础功能测试"""

    def test_init(self):
        """测试 EventManager 初始化"""
        manager = EventManager()
        assert manager._events == {}
        assert manager._subscribers == {}
        assert manager._status == {}

    def test_init_with_heartbeat_interval(self):
        """测试 EventManager 使用自定义心跳间隔初始化"""
        manager = EventManager(heartbeat_interval=10.0)
        assert manager._heartbeat_interval == 10.0

    def test_default_heartbeat_interval(self):
        """测试默认心跳间隔为 20 秒"""
        manager = EventManager()
        assert manager._heartbeat_interval == 20.0

    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self):
        """测试基本发布订阅功能"""
        manager = EventManager()
        run_id = "test-run-1"

        # 发布事件
        await manager.publish(run_id, "event: test\ndata: hello\n\n")

        # 订阅并接收事件
        events = []
        async for event in manager.subscribe(run_id):
            events.append(event)
            break  # 只取第一个事件

        assert len(events) == 1
        assert events[0] == "event: test\ndata: hello\n\n"

    @pytest.mark.asyncio
    async def test_set_status_and_is_finished(self):
        """测试状态设置和完成检查"""
        manager = EventManager()
        run_id = "test-run-2"

        assert not manager.is_finished(run_id)

        manager.set_status(run_id, "success")
        assert manager.is_finished(run_id)

        manager.set_status(run_id, "running")
        assert not manager.is_finished(run_id)

    @pytest.mark.asyncio
    async def test_cleanup(self):
        """测试资源清理"""
        manager = EventManager()
        run_id = "test-run-3"

        await manager.publish(run_id, "event: test\n\n")
        manager.set_status(run_id, "success")

        manager.cleanup(run_id)

        assert run_id not in manager._events
        assert run_id not in manager._status


class TestEventManagerHeartbeat:
    """EventManager SSE 心跳功能测试"""

    @pytest.mark.asyncio
    async def test_heartbeat_sent_periodically(self):
        """测试心跳任务周期性发送心跳注释

        心跳使用 SSE 注释格式 (:heartbeat)，EventSource 客户端会忽略。
        """
        manager = EventManager(heartbeat_interval=0.1)  # 100ms for testing
        run_id = "test-heartbeat-1"

        events = []
        subscription_task = None

        async def collect_events():
            nonlocal subscription_task
            async for event in manager.subscribe(run_id):
                if event is not None:
                    events.append(event)
                    if len(events) >= 2:  # 收集到至少 2 个心跳后停止
                        manager.set_status(run_id, "success")
                        break

        # 启动订阅
        subscription_task = asyncio.create_task(collect_events())

        # 等待足够时间让心跳发送
        await asyncio.sleep(0.35)  # 等待 3+ 个心跳周期

        # 设置完成状态以结束订阅
        manager.set_status(run_id, "success")

        # 等待订阅任务完成
        try:
            await asyncio.wait_for(subscription_task, timeout=1.0)
        except asyncio.TimeoutError:
            subscription_task.cancel()
            try:
                await subscription_task
            except asyncio.CancelledError:
                pass

        # 验证至少收到了心跳
        heartbeat_count = sum(1 for e in events if e == ":heartbeat\n\n")
        assert heartbeat_count >= 1, f"Expected at least 1 heartbeat, got {heartbeat_count}"

    @pytest.mark.asyncio
    async def test_heartbeat_stops_on_finish(self):
        """测试心跳任务在 run 完成时停止"""
        manager = EventManager(heartbeat_interval=0.1)
        run_id = "test-heartbeat-2"

        events = []

        async def collect_events():
            async for event in manager.subscribe(run_id):
                if event is not None:
                    events.append(event)

        # 启动订阅
        subscription_task = asyncio.create_task(collect_events())

        # 等待一个心跳周期
        await asyncio.sleep(0.15)

        # 设置完成状态
        manager.set_status(run_id, "success")

        # 等待订阅结束
        try:
            await asyncio.wait_for(subscription_task, timeout=1.0)
        except asyncio.TimeoutError:
            subscription_task.cancel()
            try:
                await subscription_task
            except asyncio.CancelledError:
                pass

        # 验证心跳任务已停止（检查 _heartbeat_tasks 是否清理）
        # 注意：由于 subscribe 退出时会清理，所以 run_id 不应该在 _heartbeat_tasks 中
        assert run_id not in manager._heartbeat_tasks

    @pytest.mark.asyncio
    async def test_heartbeat_task_cancelled_on_unsubscribe(self):
        """测试取消订阅时心跳任务被取消"""
        manager = EventManager(heartbeat_interval=0.1)
        run_id = "test-heartbeat-3"

        subscription_task = None

        async def subscribe_and_cancel():
            nonlocal subscription_task
            async for event in manager.subscribe(run_id):
                # 立即取消
                break

        # 启动订阅
        subscription_task = asyncio.create_task(subscribe_and_cancel())

        # 等待订阅完成
        try:
            await asyncio.wait_for(subscription_task, timeout=1.0)
        except asyncio.TimeoutError:
            subscription_task.cancel()
            try:
                await subscription_task
            except asyncio.CancelledError:
                pass

        # 验证心跳任务已清理
        assert run_id not in manager._heartbeat_tasks
