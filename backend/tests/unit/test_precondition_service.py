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


class TestPreconditionServiceSubstitution:
    """变量替换测试"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    def test_substitute_variables_simple(self, service):
        """测试简单变量替换"""
        context = {'order_id': 'ORD-12345'}
        text = "查询订单 {{order_id}}"
        result = PreconditionService.substitute_variables(text, context)

        assert result == "查询订单 ORD-12345"

    def test_substitute_variables_multiple(self, service):
        """测试多个变量替换"""
        context = {'order_id': 'ORD-001', 'user_name': '张三'}
        text = "订单 {{order_id}} 的收件人是 {{user_name}}"
        result = PreconditionService.substitute_variables(text, context)

        assert result == "订单 ORD-001 的收件人是 张三"

    def test_substitute_variables_no_match(self, service):
        """测试无变量文本不处理"""
        context = {'order_id': 'ORD-001'}
        text = "普通文本没有变量"
        result = PreconditionService.substitute_variables(text, context)

        assert result == "普通文本没有变量"

    def test_substitute_variables_empty_text(self, service):
        """测试空文本"""
        context = {'order_id': 'ORD-001'}
        result = PreconditionService.substitute_variables("", context)
        assert result == ""

        result = PreconditionService.substitute_variables(None, context)
        assert result is None

    def test_substitute_variables_undefined_error(self, service):
        """测试未定义变量报错"""
        from jinja2 import UndefinedError

        context = {'order_id': 'ORD-001'}
        text = "订单 {{undefined_var}}"

        with pytest.raises(UndefinedError):
            PreconditionService.substitute_variables(text, context)

    def test_substitute_variables_with_dict_access(self, service):
        """测试字典属性访问（Jinja2 特性）"""
        context = {'order': {'id': 'ORD-001', 'name': '测试订单'}}
        text = "订单 ID: {{order.id}}, 名称: {{order.name}}"
        result = PreconditionService.substitute_variables(text, context)

        assert result == "订单 ID: ORD-001, 名称: 测试订单"

    @pytest.mark.asyncio
    async def test_full_flow_with_substitution(self, service):
        """测试完整流程：执行前置条件 + 变量替换（PRE-04）"""
        # 执行前置条件设置变量
        code1 = "context['order_id'] = 'ORD-99999'"
        code2 = "context['user_name'] = '测试用户'"

        result1 = await service.execute_single(code1, 0)
        result2 = await service.execute_single(code2, 1)

        assert result1.success is True
        assert result2.success is True

        # 获取 context 并进行变量替换
        context = service.get_context()
        text = "查询订单 {{order_id}}，验证收件人是 {{user_name}}"
        substituted = PreconditionService.substitute_variables(text, context)

        assert substituted == "查询订单 ORD-99999，验证收件人是 测试用户"
