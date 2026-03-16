"""PreconditionService 单元测试"""

import pytest
import asyncio

from backend.core.precondition_service import PreconditionService, PreconditionResult


class TestPreconditionService:
    """PreconditionService 测试"""

    @pytest.fixture
    def service(self):
        """创建服务实例"""
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_execute_simple_code(self, service):
        """测试执行简单代码"""
        code = "x = 1 + 1"
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.error is None
        assert result.duration_ms >= 0  # May be 0 for very fast execution

    @pytest.mark.asyncio
    async def test_execute_with_context(self, service):
        """测试通过 context 存储变量"""
        code = "context['order_id'] = 'ORD-12345'"
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('order_id') == 'ORD-12345'
        assert service.get_context().get('order_id') == 'ORD-12345'

    @pytest.mark.asyncio
    async def test_execute_without_browser(self, service):
        """测试执行不启动浏览器（PRE-02）"""
        # 这是一个纯 Python 代码执行测试
        # 验证不依赖任何浏览器相关模块
        code = """
import json
data = json.loads('{"name": "test"}')
context['parsed_name'] = data['name']
"""
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('parsed_name') == 'test'

    @pytest.mark.asyncio
    async def test_syntax_error(self, service):
        """测试语法错误处理"""
        code = "if True"  # 缺少冒号
        result = await service.execute_single(code, 0)

        assert result.success is False
        assert "语法错误" in result.error

    @pytest.mark.asyncio
    async def test_runtime_error(self, service):
        """测试运行时错误处理"""
        code = "1 / 0"
        result = await service.execute_single(code, 0)

        assert result.success is False
        assert "执行错误" in result.error

    @pytest.mark.asyncio
    async def test_timeout_control(self, service):
        """测试超时控制（PRE-02）"""
        code = "import time; time.sleep(5)"
        result = await service.execute_single(code, 0, timeout=1.0)

        assert result.success is False
        assert "超时" in result.error

    @pytest.mark.asyncio
    async def test_execute_all_success(self, service):
        """测试批量执行全部成功"""
        codes = [
            "context['a'] = 1",
            "context['b'] = 2",
        ]
        success, results = await service.execute_all(codes)

        assert success is True
        assert len(results) == 2
        assert all(r.success for r in results)

    @pytest.mark.asyncio
    async def test_execute_all_stop_on_failure(self, service):
        """测试批量执行失败时停止"""
        codes = [
            "context['a'] = 1",
            "raise Exception('fail')",
            "context['b'] = 2",  # 不应该执行
        ]
        success, results = await service.execute_all(codes)

        assert success is False
        assert len(results) == 2  # 第三个不应该执行
        assert results[0].success is True
        assert results[1].success is False

    @pytest.mark.asyncio
    async def test_context_persistence(self, service):
        """测试 context 在多次执行间持久化"""
        await service.execute_single("context['x'] = 1", 0)
        await service.execute_single("context['y'] = context['x'] + 1", 1)

        ctx = service.get_context()
        assert ctx['x'] == 1
        assert ctx['y'] == 2

    @pytest.mark.asyncio
    async def test_empty_code_skipped(self, service):
        """测试空代码被跳过"""
        codes = ["", "  ", "context['a'] = 1"]
        success, results = await service.execute_all(codes)

        assert success is True
        assert len(results) == 1  # 只有第三个被执行
