"""PreconditionService 单元测试"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from backend.core.precondition_service import (
    PreconditionService,
    PreconditionResult,
    ContextWrapper,
    DataMethodError,
    execute_data_method_sync,
)


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

    # --- List index access tests (Task 1) ---

    def test_substitute_variables_list_index(self, service):
        """Test list index access like {{items[0]}}."""
        context = {'items': ['first', 'second', 'third']}
        text = "First item: {{items[0]}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "First item: first"

    def test_substitute_variables_list_index_with_attribute(self, service):
        """Test list index with attribute access like {{items[0].name}}."""
        context = {
            'items': [
                {'name': 'Product A', 'price': 100},
                {'name': 'Product B', 'price': 200}
            ]
        }
        text = "Product: {{items[0].name}}, Price: {{items[0].price}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "Product: Product A, Price: 100"

    def test_substitute_variables_list_third_element(self, service):
        """Test {{items[2]}} with list of length 3 returns third element."""
        context = {'items': ['first', 'second', 'third']}
        text = "Third item: {{items[2]}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "Third item: third"

    def test_substitute_variables_list_index_out_of_range(self, service):
        """Test index out of range raises error."""
        from jinja2 import UndefinedError

        context = {'items': ['only_one']}
        text = "Missing: {{items[5]}}"

        with pytest.raises((UndefinedError, IndexError)):
            PreconditionService.substitute_variables(text, context)

    # --- Nested path and empty container tests (Task 2) ---

    def test_substitute_variables_nested_path(self, service):
        """Test deeply nested field paths like {{data.level1.level2}}."""
        context = {
            'data': {
                'level1': {
                    'level2': 'deep_value',
                    'sibling': 'other'
                }
            }
        }
        text = "Value: {{data.level1.level2}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "Value: deep_value"

    def test_substitute_variables_three_level_nesting(self, service):
        """Test 3-level nested paths."""
        context = {
            'response': {
                'data': {
                    'order': {
                        'id': 'ORD-123',
                        'items': [{'name': 'item1'}]
                    }
                }
            }
        }
        text = "Order: {{response.data.order.id}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "Order: ORD-123"

    def test_substitute_variables_empty_list_iteration(self, service):
        """Test empty list in context."""
        context = {'items': []}
        # Accessing empty list directly should work
        text = "Items: {{items}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "Items: []"

    def test_substitute_variables_none_value(self, service):
        """Test None value renders as 'None' string."""
        context = {'value': None}
        text = "Value: {{value}}"
        result = PreconditionService.substitute_variables(text, context)
        assert result == "Value: None"

    def test_substitute_variables_missing_nested_key(self, service):
        """Test missing key in nested path raises UndefinedError."""
        from jinja2 import UndefinedError

        context = {'data': {'level1': {}}}
        text = "Value: {{data.level1.missing_key}}"

        with pytest.raises(UndefinedError):
            PreconditionService.substitute_variables(text, context)

    # --- Special character handling tests (Task 3) ---

    def test_substitute_variables_with_quotes(self, service):
        """Test variable value containing quotes."""
        context = {'text': 'He said "Hello"'}
        result = PreconditionService.substitute_variables("Message: {{text}}", context)
        assert result == 'Message: He said "Hello"'

    def test_substitute_variables_with_newlines(self, service):
        """Test variable value containing newlines."""
        context = {'multiline': 'Line 1\nLine 2\nLine 3'}
        result = PreconditionService.substitute_variables("Content: {{multiline}}", context)
        assert result == 'Content: Line 1\nLine 2\nLine 3'

    def test_substitute_variables_with_unicode(self, service):
        """Test variable value with unicode characters."""
        context = {'chinese': '中文测试', 'emoji': 'test'}
        result = PreconditionService.substitute_variables("Text: {{chinese}}", context)
        assert result == 'Text: 中文测试'

    def test_substitute_variables_with_special_chars(self, service):
        """Test variable value with special regex characters."""
        context = {'pattern': '$10.00 (50% off) [special]'}
        result = PreconditionService.substitute_variables("Price: {{pattern}}", context)
        assert result == 'Price: $10.00 (50% off) [special]'

    def test_substitute_variables_with_html_content(self, service):
        """Test variable value with HTML is not escaped."""
        context = {'html': '<div class="test">content</div>'}
        result = PreconditionService.substitute_variables("HTML: {{html}}", context)
        assert result == 'HTML: <div class="test">content</div>'


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


class TestPreconditionServiceBridgeIntegration:
    """Tests for executing bridge-generated precondition code (BRIDGE-04)"""

    @pytest.fixture
    def service(self):
        return PreconditionService()

    @pytest.mark.asyncio
    async def test_execute_bridge_generated_code_pattern(self, service):
        """Test that bridge-generated code pattern executes correctly.

        This simulates the code generated by generate_precondition_code().
        Note: Without actual webseleniumerp project, we test the pattern, not real imports.
        """
        # Simulate bridge-generated code (without actual PreFront import)
        code = '''
# Simulated bridge-generated code structure
context['precondition_result'] = 'success'
context['operations_executed'] = ['FA1', 'HC1']
'''
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.variables.get('precondition_result') == 'success'
        assert result.variables.get('operations_executed') == ['FA1', 'HC1']

    @pytest.mark.asyncio
    async def test_execute_code_with_sys_path_pattern(self, service, tmp_path):
        """Test sys.path.insert pattern works in execution environment.

        This verifies the bridge code pattern of adding paths to sys.path.
        """
        # Create a test module
        test_module = tmp_path / "test_mod"
        test_module.mkdir()
        (test_module / "__init__.py").write_text("")
        (test_module / "submod.py").write_text("VALUE = 'test_value_123'")

        # Code mimicking bridge-generated pattern
        code = f'''
import sys
sys.path.insert(0, '{tmp_path}')
from test_mod.submod import VALUE
context['imported_value'] = VALUE
'''
        result = await service.execute_single(code, 0)

        assert result.success is True, f"Error: {result.error}"
        assert result.variables.get('imported_value') == 'test_value_123'

    @pytest.mark.asyncio
    async def test_context_precondition_result_set(self, service):
        """Test that context['precondition_result'] = 'success' works."""
        code = "context['precondition_result'] = 'success'"
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert service.get_context().get('precondition_result') == 'success'

    @pytest.mark.asyncio
    async def test_import_error_handling(self, service):
        """Test that import errors are caught and reported."""
        code = "from nonexistent_module import Something"
        result = await service.execute_single(code, 0)

        assert result.success is False
        assert "执行错误" in result.error or "ModuleNotFoundError" in result.error or "No module named" in result.error

    @pytest.mark.asyncio
    async def test_complex_precondition_code_pattern(self, service, tmp_path):
        """Test complete bridge-generated code pattern with mock module.

        This tests the full pattern: sys.path -> import -> instantiate -> call method -> set context.
        """
        # Create mock PreFront-like module
        mock_module = tmp_path / "common"
        mock_module.mkdir()
        (mock_module / "__init__.py").write_text("")
        (mock_module / "base_prerequisites.py").write_text('''
class PreFront:
    def __init__(self):
        self.executed_operations = []

    def operations(self, codes):
        self.executed_operations = codes
        return self
''')

        code = f'''
import sys
sys.path.insert(0, '{tmp_path}')

from common.base_prerequisites import PreFront

pre_front = PreFront()
pre_front.operations(['FA1', 'HC1'])

context['precondition_result'] = 'success'
context['executed_ops'] = pre_front.executed_operations
'''
        result = await service.execute_single(code, 0)

        assert result.success is True, f"Error: {result.error}"
        assert result.variables.get('precondition_result') == 'success'
        assert result.variables.get('executed_ops') == ['FA1', 'HC1']


class TestContextWrapper:
    """Tests for ContextWrapper class."""

    @pytest.fixture
    def wrapper(self):
        return ContextWrapper()

    # --- get_data() tests ---

    def test_get_data_returns_data_on_success(self, wrapper):
        """Test get_data() returns data when execution succeeds."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": True, "data": [{"id": 1}]}
        ):
            result = wrapper.get_data("BaseParams", "inventory_list_data", i=2, j=3)
            assert result == [{"id": 1}]

    def test_get_data_raises_on_import_error(self, wrapper):
        """Test get_data() raises DataMethodError on ImportError."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": False, "error": "Module not found", "error_type": "ImportError"}
        ):
            with pytest.raises(DataMethodError) as exc_info:
                wrapper.get_data("BaseParams", "some_method")
            # error_type not in message, but class.method should be
            assert "ImportError" not in str(exc_info.value)
            assert "BaseParams.some_method" in str(exc_info.value)
            assert "Module not found" in str(exc_info.value)

    def test_get_data_raises_on_not_found_error(self, wrapper):
        """Test get_data() raises DataMethodError on NotFoundError."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": False, "error": "Method not found", "error_type": "NotFoundError"}
        ):
            with pytest.raises(DataMethodError) as exc_info:
                wrapper.get_data("BaseParams", "unknown_method")
            assert "BaseParams.unknown_method" in str(exc_info.value)
            assert "Method not found" in str(exc_info.value)

    def test_get_data_raises_on_timeout_error(self, wrapper):
        """Test get_data() raises DataMethodError on TimeoutError."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": False, "error": "Execution timeout (30.0s)", "error_type": "TimeoutError"}
        ):
            with pytest.raises(DataMethodError) as exc_info:
                wrapper.get_data("BaseParams", "slow_method")
            assert "BaseParams.slow_method" in str(exc_info.value)
            assert "timeout" in str(exc_info.value)

    def test_get_data_raises_on_parameter_error(self, wrapper):
        """Test get_data() raises DataMethodError on ParameterError."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": False, "error": "Parameter error: 'i' must be integer", "error_type": "ParameterError"}
        ):
            with pytest.raises(DataMethodError) as exc_info:
                wrapper.get_data("BaseParams", "inventory_data", i="invalid")
            assert "BaseParams.inventory_data" in str(exc_info.value)
            assert "Parameter error" in str(exc_info.value)

    def test_get_data_raises_on_execution_error(self, wrapper):
        """Test get_data() raises DataMethodError on ExecutionError."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": False, "error": "Database connection failed", "error_type": "ExecutionError"}
        ):
            with pytest.raises(DataMethodError) as exc_info:
                wrapper.get_data("BaseParams", "failing_method")
            assert "BaseParams.failing_method" in str(exc_info.value)
            assert "Database connection failed" in str(exc_info.value)

    def test_get_data_error_message_includes_params(self, wrapper):
        """Test DataMethodError includes full method signature with params."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": False, "error": "Failed", "error_type": "ExecutionError"}
        ):
            with pytest.raises(DataMethodError) as exc_info:
                wrapper.get_data("BaseParams", "inventory_data", i=2, j=13)
            # Verify format: "BaseParams.inventory_data(i=2, j=13) failed: Failed"
            assert "BaseParams.inventory_data" in str(exc_info.value)
            assert "i=2" in str(exc_info.value)
            assert "j=13" in str(exc_info.value)
            assert "failed: Failed" in str(exc_info.value)

    def test_get_data_passes_params_correctly(self, wrapper):
        """Test get_data() passes **params correctly to execute_data_method_sync."""
        with patch(
            'backend.core.precondition_service.execute_data_method_sync',
            return_value={"success": True, "data": "result"}
        ) as mock_execute:
            wrapper.get_data("TestClass", "test_method", i=2, j=3, name="test")
            mock_execute.assert_called_once_with("TestClass", "test_method", {"i": 2, "j": 3, "name": "test"})

    # --- Dict-like interface tests ---

    def test_getitem_returns_value(self, wrapper):
        """Test __getitem__ returns value for existing key."""
        wrapper._data['order_id'] = 'ORD-123'
        assert wrapper['order_id'] == 'ORD-123'

    def test_getitem_raises_keyerror(self, wrapper):
        """Test __getitem__ raises KeyError for missing key."""
        with pytest.raises(KeyError):
            _ = wrapper['nonexistent']

    def test_setitem_stores_value(self, wrapper):
        """Test __setitem__ stores value correctly."""
        wrapper['user_name'] = 'test_user'
        assert wrapper._data['user_name'] == 'test_user'

    def test_contains_returns_correct_bool(self, wrapper):
        """Test __contains__ returns True for existing, False for missing."""
        wrapper['key'] = 'value'
        assert 'key' in wrapper
        assert 'missing' not in wrapper

    def test_get_returns_value_or_default(self, wrapper):
        """Test get() returns value or default."""
        wrapper['existing'] = 'value'
        assert wrapper.get('existing') == 'value'
        assert wrapper.get('missing') is None
        assert wrapper.get('missing', 'default') == 'default'

    def test_keys_returns_dict_keys_view(self, wrapper):
        """Test keys() returns dict_keys view."""
        wrapper['a'] = 1
        wrapper['b'] = 2
        keys = wrapper.keys()
        assert 'a' in keys
        assert 'b' in keys
        assert len(keys) == 2

    def test_to_dict_returns_copy(self, wrapper):
        """Test to_dict() returns a copy, not reference."""
        wrapper['data'] = {'nested': 'value'}
        copy = wrapper.to_dict()
        assert copy == {'data': {'nested': 'value'}}
        # Modify copy should not affect original
        copy['data']['nested'] = 'modified'
        assert wrapper._data['data']['nested'] == 'value'
        copy['new_key'] = 'new_value'
        assert 'new_key' not in wrapper._data


class TestExecuteDataMethodSync:
    """Tests for execute_data_method_sync function."""

    def test_no_running_loop_uses_asyncio_run(self):
        """Test uses asyncio.run() when no event loop is running."""
        with patch(
            'backend.core.precondition_service.execute_data_method',
            return_value={"success": True, "data": [{"id": 1}]}
        ) as mock_execute:
            result = execute_data_method_sync("TestClass", "test_method", {"i": 2})

            assert result == {"success": True, "data": [{"id": 1}]}
            mock_execute.assert_called_once_with("TestClass", "test_method", {"i": 2})

    @pytest.mark.asyncio
    async def test_with_running_loop_uses_nest_asyncio(self):
        """Test uses nest_asyncio when event loop is already running."""
        with patch(
            'backend.core.precondition_service.execute_data_method',
            return_value={"success": True, "data": "result"}
        ) as mock_execute:
            # We're inside an async test, so there's a running loop
            result = execute_data_method_sync("TestClass", "test_method", {})

            assert result == {"success": True, "data": "result"}
            mock_execute.assert_called_once_with("TestClass", "test_method", {})

    def test_result_passthrough(self):
        """Test result from execute_data_method is passed through unchanged."""
        expected = {"success": False, "error": "Some error", "error_type": "ExecutionError"}
        with patch(
            'backend.core.precondition_service.execute_data_method',
            return_value=expected
        ):
            result = execute_data_method_sync("Class", "method", {"p": 1})
            assert result is expected

    def test_params_passed_correctly(self):
        """Test params dict is passed correctly to execute_data_method."""
        with patch(
            'backend.core.precondition_service.execute_data_method',
            return_value={"success": True, "data": None}
        ) as mock_execute:
            params = {"i": 2, "j": 13, "name": "test"}
            execute_data_method_sync("BaseParams", "inventory_data", params)

            mock_execute.assert_called_once_with("BaseParams", "inventory_data", params)
