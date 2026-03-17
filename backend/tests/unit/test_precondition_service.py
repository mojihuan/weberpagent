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


class TestPreconditionServiceExternalModule:
    """外部模块加载测试"""

    @pytest.mark.asyncio
    async def test_load_external_module(self, tmp_path):
        """测试加载外部模块（PRE-03）"""
        # 创建临时模块
        module_dir = tmp_path / "test_api"
        module_dir.mkdir()
        api_file = module_dir / "test_api.py"
        api_file.write_text('''
class TestApi:
    def __init__(self):
        self.base_url = "http://test.com"

    def get_data(self):
        return {"status": "ok"}
''')
        # 添加 __init__.py
        (module_dir / "__init__.py").write_text("")

        service = PreconditionService(external_module_path=str(module_dir.parent))

        code = '''
from test_api.test_api import TestApi
api = TestApi()
context['api_result'] = api.get_data()
'''
        result = await service.execute_single(code, 0)

        assert result.success is True, f"Error: {result.error}"
        assert result.variables.get('api_result') == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_invalid_module_path(self):
        """测试无效模块路径"""
        service = PreconditionService(external_module_path="/nonexistent/path")
        valid, msg = service.validate_external_module_path()

        assert valid is False
        assert "不存在" in msg

    @pytest.mark.asyncio
    async def test_no_external_module_path(self):
        """测试未配置外部模块路径"""
        service = PreconditionService()
        valid, msg = service.validate_external_module_path()

        assert valid is True
        assert "未配置" in msg

    @pytest.mark.asyncio
    async def test_module_import_error(self, tmp_path):
        """测试模块导入错误"""
        module_dir = tmp_path / "broken_api"
        module_dir.mkdir()
        broken_file = module_dir / "broken.py"
        broken_file.write_text("import nonexistent_module")  # 故意导入不存在的模块
        (module_dir / "__init__.py").write_text("")

        service = PreconditionService(external_module_path=str(module_dir.parent))

        code = "from broken_api import broken"
        result = await service.execute_single(code, 0)

        assert result.success is False
        assert "执行错误" in result.error or "ModuleNotFoundError" in result.error

    @pytest.mark.asyncio
    async def test_context_with_external_api(self, tmp_path):
        """测试使用外部 API 并存储结果到 context"""
        module_dir = tmp_path / "erp_api"
        module_dir.mkdir()
        api_file = module_dir / "order_api.py"
        api_file.write_text('''
class OrderApi:
    def create_order(self, name):
        return {"id": "ORD-001", "name": name}
''')
        (module_dir / "__init__.py").write_text("")

        service = PreconditionService(external_module_path=str(module_dir.parent))

        code = '''
from erp_api.order_api import OrderApi
api = OrderApi()
order = api.create_order("测试订单")
context['order_id'] = order['id']
context['order_name'] = order['name']
'''
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('order_id') == "ORD-001"
        assert result.variables.get('order_name') == "测试订单"


class TestPreconditionServiceDynamicData:
    """动态数据集成测试 (Phase 7)"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_dynamic_data_sf_waybill(self, service):
        """测试 SF 物流单号生成 (DYN-01)"""
        code = "context['order_no'] = sf_waybill()"
        result = await service.execute_single(code, 0)

        assert result.success is True
        order_no = result.variables.get('order_no')
        assert order_no is not None
        assert order_no.startswith("SF")
        assert len(order_no) == 14

    @pytest.mark.asyncio
    async def test_dynamic_data_random_phone(self, service):
        """测试手机号生成 (DYN-01)"""
        code = "context['phone'] = random_phone()"
        result = await service.execute_single(code, 0)

        assert result.success is True
        phone = result.variables.get('phone')
        assert phone is not None
        assert phone.startswith("13")
        assert len(phone) == 11
        assert phone.isdigit()

    @pytest.mark.asyncio
    async def test_dynamic_data_random_imei(self, service):
        """测试 IMEI 生成 (DYN-01)"""
        code = "context['imei'] = random_imei()"
        result = await service.execute_single(code, 0)

        assert result.success is True
        imei = result.variables.get('imei')
        assert imei is not None
        assert imei.startswith("I")
        assert len(imei) == 15

    @pytest.mark.asyncio
    async def test_dynamic_data_time_now(self, service):
        """测试当前时间获取 (DYN-04)"""
        code = "context['current_time'] = time_now()"
        result = await service.execute_single(code, 0)

        assert result.success is True
        current_time = result.variables.get('current_time')
        assert current_time is not None
        # 验证格式可以解析
        from datetime import datetime
        parsed = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        assert isinstance(parsed, datetime)

    @pytest.mark.asyncio
    async def test_dynamic_data_time_offset(self, service):
        """测试时间偏移计算 (DYN-04)"""
        code = "context['future_time'] = time_now(30)"
        result = await service.execute_single(code, 0)

        assert result.success is True
        future_time = result.variables.get('future_time')
        assert future_time is not None

        from datetime import datetime, timedelta
        parsed = datetime.strptime(future_time, "%Y-%m-%d %H:%M:%S")
        expected = datetime.now() + timedelta(minutes=30)
        # 允许 2 秒误差
        assert abs((parsed - expected).total_seconds()) < 2

    @pytest.mark.asyncio
    async def test_dynamic_data_multiple_functions(self, service):
        """测试多个动态数据函数组合使用"""
        code = '''
context['order_no'] = sf_waybill()
context['phone'] = random_phone()
context['imei'] = random_imei()
context['time'] = time_now()
'''
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('order_no', '').startswith('SF')
        assert result.variables.get('phone', '').startswith('13')
        assert result.variables.get('imei', '').startswith('I')
        assert result.variables.get('time') is not None

    @pytest.mark.asyncio
    async def test_dynamic_data_substitution(self, service):
        """测试动态数据 + 变量替换 (DYN-03)"""
        # 先执行前置条件生成动态数据
        code = "context['order_no'] = sf_waybill()"
        result = await service.execute_single(code, 0)
        assert result.success is True

        # 获取 context 并进行变量替换
        context = service.get_context()
        text = "查询订单 {{order_no}}"
        substituted = PreconditionService.substitute_variables(text, context)

        assert substituted.startswith("查询订单 SF")
        assert len(substituted) == len("查询订单 ") + 14
