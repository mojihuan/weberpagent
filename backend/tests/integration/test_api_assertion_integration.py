"""ApiAssertionService 集成测试"""

import pytest
from datetime import datetime, timedelta

from backend.core.api_assertion_service import ApiAssertionService


class TestApiAssertionIntegration:
    """接口断言集成测试"""

    @pytest.mark.asyncio
    async def test_api_assertion_full_flow(self):
        """完整的接口断言流程"""
        service = ApiAssertionService()
        service.context = {"order_id": "12345"}

        # 模拟完整的断言代码
        assertions = [
            # 精确匹配
            "assert context['order_id'] == '12345'",
            # 时间断言
            "from datetime import datetime; assert_time(datetime.now())",
            # 包含匹配
            "assert_contains('hello world', 'world')",
            # 小数近似
            "assert_decimal(100.005, 100.0, 0.01)",
        ]

        results = await service.execute_all(assertions)

        assert len(results) == 4
        assert all(r.success for r in results)

    @pytest.mark.asyncio
    async def test_api_assertion_with_external_module_mock(self, tmp_path):
        """外部模块加载测试"""
        # 创建临时模块
        module_dir = tmp_path / "test_api"
        module_dir.mkdir()
        (module_dir / "__init__.py").write_text("")
        (module_dir / "mock_api.py").write_text("""
class MockApi:
    def get_order(self, order_id):
        return {"id": order_id, "status": "success"}
""")

        service = ApiAssertionService(external_module_path=str(module_dir))

        # 使用外部模块
        code = """
from mock_api import MockApi
api = MockApi()
result = api.get_order('12345')
context['api_result'] = result
"""
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert service.context.get("api_result") == {"id": "12345", "status": "success"}

    @pytest.mark.asyncio
    async def test_api_assertion_mixed_results(self):
        """混合通过和失败的断言"""
        service = ApiAssertionService()

        assertions = [
            "x = 1 + 1",  # 通过
            "assert False",  # 失败
            "y = 2 + 2",  # 通过
            "raise Exception('error')",  # 失败
        ]

        results = await service.execute_all(assertions)

        assert len(results) == 4
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True
        assert results[3].success is False

    @pytest.mark.asyncio
    async def test_api_assertion_with_variable_substitution(self):
        """变量替换集成测试"""
        service = ApiAssertionService()
        service.context = {
            "expected_status": "success",
            "expected_amount": 100.00,
        }

        # 变量替换在代码中生效
        code1 = "status = '{{expected_status}}'; assert status == 'success'"
        code2 = "amount = {{expected_amount}}; assert amount == 100.0"

        result1 = await service.execute_single(code1, 0)
        result2 = await service.execute_single(code2, 1)

        assert result1.success is True
        assert result2.success is True

    @pytest.mark.asyncio
    async def test_api_assertion_time_scenarios(self):
        """时间断言场景测试"""
        service = ApiAssertionService()

        now = datetime.now()
        time_30s_ago = now - timedelta(seconds=30)

        assertions = [
            # 当前时间应该在范围内
            f"assert_time('{now.strftime('%Y-%m-%d %H:%M:%S')}')",
            # 30秒前应该在范围内
            f"assert_time('{time_30s_ago.strftime('%Y-%m-%d %H:%M:%S')}')",
        ]

        results = await service.execute_all(assertions)

        assert len(results) == 2
        assert all(r.success for r in results)

        # 测试超出范围的时间 - assert_time 返回 False，assert False 会失败
        time_2min_ago = now - timedelta(seconds=120)
        result = await service.execute_single(
            f"result = assert_time('{time_2min_ago.strftime('%Y-%m-%d %H:%M:%S')}'); assert result is False", 0
        )
        # 应该成功，因为 assert_time 对超出范围的时间返回 False
        assert result.success is True

    @pytest.mark.asyncio
    async def test_api_assertion_data_scenarios(self):
        """数据断言场景测试"""
        service = ApiAssertionService()

        assertions = [
            # 精确匹配
            "assert assert_exact('success', 'success')",
            "assert assert_exact(100, 100)",
            # 包含匹配
            "assert assert_contains('Order #12345 created', '12345')",
            "assert assert_contains('订单创建成功', '成功')",
            # 小数近似
            "assert assert_decimal(100.005, 100.0, 0.01)",
            "assert assert_decimal(-50.005, -50.0, 0.01)",
        ]

        results = await service.execute_all(assertions)

        assert len(results) == 6
        assert all(r.success for r in results)
