"""前置条件到 UI 测试的完整流程测试"""

import pytest
import asyncio
import tempfile
import json

from backend.core.precondition_service import PreconditionService


class TestPreconditionFlow:
    """前置条件完整流程测试"""

    @pytest.mark.asyncio
    async def test_precondition_to_ui_flow(self):
        """测试前置条件执行并传递变量到 UI 步骤（PRE-04 集成测试）"""
        # 模拟前置条件
        preconditions = [
            "context['order_id'] = 'ORD-INTEGRATION-001'",
            "context['status'] = 'pending'",
        ]

        service = PreconditionService()

        # 执行所有前置条件
        success, results = await service.execute_all(preconditions)

        assert success is True
        assert len(results) == 2

        # 获取 context
        context = service.get_context()
        assert context['order_id'] == 'ORD-INTEGRATION-001'
        assert context['status'] == 'pending'

        # 模拟 UI 步骤描述的变量替换
        ui_description = "在订单页面搜索 {{order_id}}，验证状态为 {{status}}"
        substituted = PreconditionService.substitute_variables(ui_description, context)

        assert substituted == "在订单页面搜索 ORD-INTEGRATION-001，验证状态为 pending"

    @pytest.mark.asyncio
    async def test_precondition_failure_stops_flow(self):
        """测试前置条件失败时停止流程"""
        preconditions = [
            "context['a'] = 1",
            "raise Exception('故意失败')",
            "context['b'] = 2",  # 不应该执行
        ]

        service = PreconditionService()
        success, results = await service.execute_all(preconditions)

        assert success is False
        assert len(results) == 2  # 第三个不执行
        assert results[0].success is True
        assert results[1].success is False
        assert 'b' not in service.get_context()

    @pytest.mark.asyncio
    async def test_precondition_with_external_module_flow(self, tmp_path):
        """测试使用外部模块的完整流程"""
        # 创建模拟 API 模块
        module_dir = tmp_path / "mock_erp"
        module_dir.mkdir()
        api_file = module_dir / "mock_api.py"
        api_file.write_text('''
class MockOrderApi:
    def create_order(self, name):
        return {"id": "MOCK-001", "name": name, "status": "created"}
''')
        (module_dir / "__init__.py").write_text("")

        # 创建服务并配置外部模块路径
        service = PreconditionService(external_module_path=str(module_dir.parent))

        # 执行使用外部模块的前置条件
        preconditions = [
            '''
from mock_erp.mock_api import MockOrderApi
api = MockOrderApi()
order = api.create_order("集成测试订单")
context['order_id'] = order['id']
context['order_name'] = order['name']
''',
        ]

        success, results = await service.execute_all(preconditions)

        assert success is True
        context = service.get_context()
        assert context['order_id'] == "MOCK-001"
        assert context['order_name'] == "集成测试订单"

        # 验证变量替换
        ui_step = "验证订单 {{order_id}} 的名称为 {{order_name}}"
        substituted = PreconditionService.substitute_variables(ui_step, context)
        assert substituted == "验证订单 MOCK-001 的名称为 集成测试订单"

    @pytest.mark.asyncio
    async def test_variable_not_defined_error(self):
        """测试引用未定义变量的错误"""
        service = PreconditionService()

        # 不设置任何变量
        context = service.get_context()

        # 尝试替换未定义的变量
        from jinja2 import UndefinedError
        with pytest.raises(UndefinedError):
            PreconditionService.substitute_variables("{{undefined_var}}", context)

    @pytest.mark.asyncio
    async def test_precondition_context_persistence(self):
        """测试 context 在多次执行间正确持久化"""
        service = PreconditionService()

        # 第一次执行
        await service.execute_single("context['step1'] = 'value1'", 0)

        # 第二次执行引用第一次的值
        await service.execute_single("context['step2'] = context['step1'] + '_extended'", 1)

        context = service.get_context()
        assert context['step1'] == 'value1'
        assert context['step2'] == 'value1_extended'
