# backend/tests/test_event_manager.py
import pytest
import asyncio
from backend.core.event_manager import EventManager


@pytest.fixture
def event_manager():
    return EventManager()


class TestEventManager:
    """EventManager 单元测试"""

    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self, event_manager):
        """测试发布和订阅事件"""
        run_id = "test-run-1"

        # 发布事件
        await event_manager.publish(run_id, "event: test\ndata: hello\n\n")

        # 订阅并获取事件
        events = []
        async for event in event_manager.subscribe(run_id):
            events.append(event)
            break  # 只获取一个事件

        assert len(events) == 1
        assert events[0] == "event: test\ndata: hello\n\n"

    @pytest.mark.asyncio
    async def test_multiple_events(self, event_manager):
        """测试多个事件 - 模拟实际场景：先订阅，后发布"""
        run_id = "test-run-2"
        collected_events: list[str] = []
        done = asyncio.Event()

        async def subscriber():
            async for event in event_manager.subscribe(run_id):
                if event is None:
                    break
                collected_events.append(event)
            done.set()

        # 启动订阅者
        sub_task = asyncio.create_task(subscriber())

        # 给订阅者一点时间启动
        await asyncio.sleep(0.01)

        # 发布多个事件
        await event_manager.publish(run_id, "event: started\ndata: 1\n\n")
        await event_manager.publish(run_id, "event: step\ndata: 2\n\n")
        await event_manager.publish(run_id, None)  # 结束信号

        # 等待订阅者完成
        await done.wait()
        sub_task.cancel()

        assert len(collected_events) == 2

    @pytest.mark.asyncio
    async def test_is_finished(self, event_manager):
        """测试执行状态检查"""
        run_id = "test-run-3"

        assert event_manager.is_finished(run_id) is False

        event_manager.set_status(run_id, "success")
        assert event_manager.is_finished(run_id) is True

        event_manager.set_status(run_id, "failed")
        assert event_manager.is_finished(run_id) is True

        event_manager.set_status(run_id, "running")
        assert event_manager.is_finished(run_id) is False

    @pytest.mark.asyncio
    async def test_reconnect_gets_history(self, event_manager):
        """测试重新连接获取历史事件"""
        run_id = "test-run-4"

        # 发布事件
        await event_manager.publish(run_id, "event: started\ndata: 1\n\n")
        await event_manager.publish(run_id, "event: step\ndata: 2\n\n")

        # 标记完成
        event_manager.set_status(run_id, "success")

        # 订阅应该获取历史事件
        events = []
        async for event in event_manager.subscribe(run_id):
            if event is None:
                break
            events.append(event)

        assert len(events) == 2

    @pytest.mark.asyncio
    async def test_cleanup(self, event_manager):
        """测试清理资源"""
        run_id = "test-run-5"

        await event_manager.publish(run_id, "event: test\ndata: 1\n\n")
        event_manager.cleanup(run_id)

        # 清理后历史应该为空
        events = event_manager._events.get(run_id, [])
        assert len(events) == 0
