"""动态数据支持端到端集成测试 (Phase 7)

验证 DYN-01 到 DYN-04 所有需求：
- DYN-01: 随机数生成
- DYN-02: API 数据获取
- DYN-03: 跨步骤数据缓存
- DYN-04: 时间计算
"""

import pytest
from datetime import datetime, timedelta

from backend.core.precondition_service import PreconditionService


class TestDynamicDataGeneration:
    """DYN-01: 随机数生成端到端测试"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_sf_waybill_in_precondition(self, service):
        """测试 SF 物流单号在前置条件中生成"""
        code = "context['sf_no'] = sf_waybill()"
        result = await service.execute_single(code, 0)

        assert result.success is True
        sf_no = result.variables.get('sf_no')
        assert sf_no.startswith("SF")
        assert len(sf_no) == 14

    @pytest.mark.asyncio
    async def test_all_random_functions(self, service):
        """测试所有随机数生成函数"""
        code = '''
context['sf'] = sf_waybill()
context['phone'] = random_phone()
context['imei'] = random_imei()
context['serial'] = random_serial()
context['num'] = random_numbers(6)
'''
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('sf', '').startswith('SF')
        assert result.variables.get('phone', '').startswith('13')
        assert result.variables.get('imei', '').startswith('I')
        assert len(result.variables.get('serial', '')) == 8
        assert len(result.variables.get('num', '')) == 6

    @pytest.mark.asyncio
    async def test_random_uniqueness(self, service):
        """测试随机数唯一性"""
        code = "context['sf_list'] = [sf_waybill() for _ in range(10)]"
        result = await service.execute_single(code, 0)

        assert result.success is True
        sf_list = result.variables.get('sf_list', [])
        assert len(sf_list) == 10
        assert len(set(sf_list)) == 10  # 全部唯一


class TestTimeCalculation:
    """DYN-04: 时间计算端到端测试"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_time_now_current(self, service):
        """测试获取当前时间"""
        code = "context['now'] = time_now()"
        result = await service.execute_single(code, 0)

        assert result.success is True
        now_str = result.variables.get('now')
        parsed = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
        # 允许 2 秒误差
        assert abs((parsed - datetime.now()).total_seconds()) < 2

    @pytest.mark.asyncio
    async def test_time_offset_future(self, service):
        """测试未来时间偏移"""
        code = "context['future'] = time_now(60)"
        result = await service.execute_single(code, 0)

        assert result.success is True
        future_str = result.variables.get('future')
        parsed = datetime.strptime(future_str, "%Y-%m-%d %H:%M:%S")
        expected = datetime.now() + timedelta(minutes=60)
        assert abs((parsed - expected).total_seconds()) < 2

    @pytest.mark.asyncio
    async def test_time_offset_past(self, service):
        """测试过去时间偏移"""
        code = "context['past'] = time_now(-30)"
        result = await service.execute_single(code, 0)

        assert result.success is True
        past_str = result.variables.get('past')
        parsed = datetime.strptime(past_str, "%Y-%m-%d %H:%M:%S")
        expected = datetime.now() - timedelta(minutes=30)
        assert abs((parsed - expected).total_seconds()) < 2


class TestContextPersistence:
    """DYN-03: 跨步骤数据缓存测试"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_context_persistence_across_preconditions(self, service):
        """测试 context 在多个前置条件间持久化"""
        codes = [
            "context['order_no'] = sf_waybill()",
            "context['phone'] = random_phone()",
            "context['combined'] = context['order_no'] + '_' + context['phone']",
        ]
        success, results = await service.execute_all(codes)

        assert success is True
        ctx = service.get_context()
        assert ctx.get('order_no', '').startswith('SF')
        assert ctx.get('phone', '').startswith('13')
        assert ctx.get('combined') == f"{ctx['order_no']}_{ctx['phone']}"

    @pytest.mark.asyncio
    async def test_dynamic_data_substitution(self, service):
        """测试动态数据生成后进行变量替换"""
        # 生成动态数据
        code = "context['order_no'] = sf_waybill()"
        result = await service.execute_single(code, 0)
        assert result.success is True

        # 获取 context 并进行变量替换
        context = service.get_context()
        template = "请查询订单 {{order_no}} 的物流信息"
        substituted = PreconditionService.substitute_variables(template, context)

        assert "请查询订单 SF" in substituted
        assert len(substituted) == len("请查询订单 ") + 14 + len(" 的物流信息")


class TestApiDataIntegration:
    """DYN-02: API 数据获取集成测试"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_api_data_with_random(self, service, tmp_path):
        """测试 API 获取数据与随机数组合使用"""
        # 创建模拟 API 模块
        module_dir = tmp_path / "mock_api"
        module_dir.mkdir()
        api_file = module_dir / "order_api.py"
        api_file.write_text('''
class OrderApi:
    def get_order(self, order_no):
        return {"order_no": order_no, "status": "pending"}
''')
        (module_dir / "__init__.py").write_text("")

        service = PreconditionService(external_module_path=str(module_dir.parent))

        code = '''
from mock_api.order_api import OrderApi
api = OrderApi()
context['order_no'] = sf_waybill()
context['order'] = api.get_order(context['order_no'])
'''
        result = await service.execute_single(code, 0)

        assert result.success is True
        order = result.variables.get('order')
        assert order is not None
        assert order.get('order_no', '').startswith('SF')
        assert order.get('status') == 'pending'

    @pytest.mark.asyncio
    async def test_api_list_data_processing(self, service, tmp_path):
        """测试 API 返回列表数据处理"""
        module_dir = tmp_path / "list_data_api"
        module_dir.mkdir()
        api_file = module_dir / "list_api.py"
        api_file.write_text('''
class ListApi:
    def get_items(self):
        return [
            {"id": "ITEM-001", "name": "商品1"},
            {"id": "ITEM-002", "name": "商品2"},
            {"id": "ITEM-003", "name": "商品3"},
        ]
''')
        (module_dir / "__init__.py").write_text("")

        service = PreconditionService(external_module_path=str(module_dir.parent))

        code = '''
from list_data_api.list_api import ListApi
api = ListApi()
items = api.get_items()
context['first_item_id'] = items[0]['id']
context['item_count'] = len(items)
'''
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('first_item_id') == 'ITEM-001'
        assert result.variables.get('item_count') == 3
