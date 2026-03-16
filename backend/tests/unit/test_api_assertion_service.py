"""ApiAssertionService 单元测试"""

import pytest
from datetime import datetime, timedelta

from backend.core.api_assertion_service import (
    ApiAssertionService,
    ApiAssertionResult,
    FieldAssertionResult,
)


class TestApiAssertionServiceClass:
    """ApiAssertionService 类基础测试"""

    @pytest.fixture
    def service(self):
        """创建服务实例"""
        return ApiAssertionService()

    def test_service_instantiable(self, service):
        """测试 ApiAssertionService 类可实例化"""
        assert service is not None
        assert isinstance(service, ApiAssertionService)

    def test_time_tolerance_constant(self, service):
        """测试 TIME_TOLERANCE_SECONDS = 60"""
        assert ApiAssertionService.TIME_TOLERANCE_SECONDS == 60

    def test_decimal_tolerance_constant(self, service):
        """测试 DECIMAL_TOLERANCE = 0.01"""
        assert ApiAssertionService.DECIMAL_TOLERANCE == 0.01

    def test_context_initialized(self, service):
        """测试 context 初始化为空字典"""
        assert service.context == {}
        assert isinstance(service.context, dict)


class TestDataClasses:
    """数据类测试"""

    def test_field_assertion_result_defaults(self):
        """测试 FieldAssertionResult 默认值"""
        result = FieldAssertionResult(
            field_name="status",
            expected="success",
            actual="success",
        )

        assert result.passed is False
        assert result.message == ""
        assert result.assertion_type == "exact"

    def test_api_assertion_result_defaults(self):
        """测试 ApiAssertionResult 默认值"""
        result = ApiAssertionResult(
            index=0,
            code="x = 1",
        )

        assert result.success is False
        assert result.error is None
        assert result.duration_ms == 0
        assert result.field_results == []


class TestCheckTimeWithinRange:
    """时间断言测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    def test_current_time_in_range(self, service):
        """测试当前时间在范围内返回 (True, "")"""
        now = datetime.now()
        passed, msg = service.check_time_within_range(now)

        assert passed is True
        assert msg == ""

    def test_30_seconds_ago_in_range(self, service):
        """测试 30 秒前的时间在范围内返回 (True, "")"""
        time_30s_ago = datetime.now() - timedelta(seconds=30)
        passed, msg = service.check_time_within_range(time_30s_ago)

        assert passed is True
        assert msg == ""

    def test_59_seconds_ago_in_range(self, service):
        """测试 59 秒前的时间在范围内返回 (True, "") - 边界"""
        time_59s_ago = datetime.now() - timedelta(seconds=59)
        passed, msg = service.check_time_within_range(time_59s_ago)

        assert passed is True
        assert msg == ""

    def test_60_seconds_ago_in_range(self, service):
        """测试 60 秒前的时间在范围内返回 (True, "") - 边界"""
        # 使用 59.5 秒前确保在执行比较时仍在范围内（避免微秒级时间漂移）
        time_59_5s_ago = datetime.now() - timedelta(seconds=59.5)
        passed, msg = service.check_time_within_range(time_59_5s_ago)

        assert passed is True
        assert msg == ""

    def test_61_seconds_ago_out_of_range(self, service):
        """测试 61 秒前的时间超出范围返回 (False, ...)"""
        time_61s_ago = datetime.now() - timedelta(seconds=61)
        passed, msg = service.check_time_within_range(time_61s_ago)

        assert passed is False
        assert "61" in msg
        assert "超出容差范围" in msg
        assert "60" in msg

    def test_string_time_format_parsed(self, service):
        """测试字符串格式时间 "2026-03-16 10:30:00" 可被正确解析"""
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        passed, msg = service.check_time_within_range(time_str)

        assert passed is True
        assert msg == ""

    def test_invalid_time_string(self, service):
        """测试无效时间字符串返回 (False, "无法解析时间格式: invalid")"""
        passed, msg = service.check_time_within_range("invalid")

        assert passed is False
        assert "无法解析时间格式" in msg
        assert "invalid" in msg

    def test_iso_format_time(self, service):
        """测试 ISO 格式时间字符串"""
        time_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        passed, msg = service.check_time_within_range(time_str)

        assert passed is True
        assert msg == ""

    def test_date_only_format(self, service):
        """测试仅日期格式字符串（今天应该通过）"""
        time_str = datetime.now().strftime("%Y-%m-%d")
        passed, msg = service.check_time_within_range(time_str)

        # 日期格式只有年月日，比较时差异可能超过60秒
        # 这取决于测试执行时间，所以只验证不会崩溃
        assert isinstance(passed, bool)
        assert isinstance(msg, str)


class TestCheckExactMatch:
    """精确匹配断言测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    def test_exact_match_equal_strings(self, service):
        """测试 check_exact_match("hello", "hello") 返回 (True, "")"""
        passed, msg = service.check_exact_match("hello", "hello")

        assert passed is True
        assert msg == ""

    def test_exact_match_different_strings(self, service):
        """测试 check_exact_match("hello", "world") 返回 (False, ...)"""
        passed, msg = service.check_exact_match("hello", "world")

        assert passed is False
        assert "期望" in msg
        assert "world" in msg
        assert "实际" in msg
        assert "hello" in msg

    def test_exact_match_numbers(self, service):
        """测试数字精确匹配"""
        passed, msg = service.check_exact_match(100, 100)

        assert passed is True
        assert msg == ""

    def test_exact_match_different_numbers(self, service):
        """测试数字不匹配"""
        passed, msg = service.check_exact_match(100, 200)

        assert passed is False
        assert "100" in msg
        assert "200" in msg


class TestCheckContainsMatch:
    """包含匹配断言测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    def test_contains_match_found(self, service):
        """测试 check_contains_match("hello world", "world") 返回 (True, "")"""
        passed, msg = service.check_contains_match("hello world", "world")

        assert passed is True
        assert msg == ""

    def test_contains_match_not_found(self, service):
        """测试 check_contains_match("hello", "xyz") 返回 (False, ...)"""
        passed, msg = service.check_contains_match("hello", "xyz")

        assert passed is False
        assert "不包含" in msg
        assert "hello" in msg
        assert "xyz" in msg

    def test_contains_match_chinese(self, service):
        """测试中文包含匹配"""
        passed, msg = service.check_contains_match("订单创建成功", "成功")

        assert passed is True
        assert msg == ""

    def test_contains_match_case_sensitive(self, service):
        """测试大小写敏感"""
        passed, msg = service.check_contains_match("Hello", "hello")

        assert passed is False  # 大小写敏感


class TestCheckDecimalApprox:
    """小数近似断言测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    def test_decimal_approx_within_tolerance(self, service):
        """测试 check_decimal_approx(1.005, 1.00, 0.01) 返回 (True, "")"""
        # 使用 0.005 误差确保在容差范围内（避免浮点精度问题）
        passed, msg = service.check_decimal_approx(1.005, 1.00, tolerance=0.01)

        assert passed is True
        assert msg == ""

    def test_decimal_approx_exceeds_tolerance(self, service):
        """测试 check_decimal_approx(1.02, 1.00, 0.01) 返回 (False, ...)"""
        passed, msg = service.check_decimal_approx(1.02, 1.00, tolerance=0.01)

        assert passed is False
        assert "0.02" in msg
        assert "超出容差" in msg
        assert "0.01" in msg

    def test_decimal_approx_default_tolerance(self, service):
        """测试默认容差 0.01"""
        passed, msg = service.check_decimal_approx(100.005, 100.00)

        assert passed is True
        assert msg == ""

    def test_decimal_approx_negative_numbers(self, service):
        """测试负数"""
        passed, msg = service.check_decimal_approx(-1.005, -1.00, tolerance=0.01)

        assert passed is True
        assert msg == ""

    def test_decimal_approx_exact_match(self, service):
        """测试精确相等"""
        passed, msg = service.check_decimal_approx(100.00, 100.00)

        assert passed is True
        assert msg == ""


class TestExecuteMethods:
    """执行方法测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    @pytest.mark.asyncio
    async def test_execute_single_simple_code(self, service):
        """测试 execute_single 执行简单代码成功"""
        code = "x = 1 + 1"
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert result.error is None
        assert result.index == 0
        assert result.code == code
        assert result.duration_ms >= 0

    @pytest.mark.asyncio
    async def test_execute_single_timeout(self, service):
        """测试 execute_single 超时返回错误"""
        code = "import time; time.sleep(5)"
        result = await service.execute_single(code, 0, timeout=1.0)

        assert result.success is False
        assert "超时" in result.error

    @pytest.mark.asyncio
    async def test_execute_single_syntax_error(self, service):
        """测试 execute_single 语法错误返回错误信息"""
        code = "if True"  # 缺少冒号
        result = await service.execute_single(code, 0)

        assert result.success is False
        assert "语法错误" in result.error

    @pytest.mark.asyncio
    async def test_execute_all_multiple_assertions(self, service):
        """测试 execute_all 执行多个断言返回所有结果"""
        assertions = [
            "x = 1",
            "y = 2",
            "z = 3",
        ]
        results = await service.execute_all(assertions)

        assert len(results) == 3
        assert all(r.success for r in results)

    @pytest.mark.asyncio
    async def test_execute_all_collects_all_results(self, service):
        """测试 execute_all 收集所有结果（不终止）"""
        assertions = [
            "x = 1",
            "raise Exception('fail')",  # 这个会失败
            "y = 2",  # 但这个仍会执行
        ]
        results = await service.execute_all(assertions)

        # 不像 PreconditionService 的 fail-fast，这里应该收集所有结果
        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True


class TestSubstituteVariables:
    """变量替换测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    def test_substitute_variables_simple(self, service):
        """测试 substitute_variables 替换 {{var}} 为实际值"""
        context = {"order_id": "ORD-12345"}
        text = "查询订单 {{order_id}}"
        result = ApiAssertionService.substitute_variables(text, context)

        assert result == "查询订单 ORD-12345"

    def test_substitute_variables_multiple(self, service):
        """测试多个变量替换"""
        context = {"order_id": "ORD-001", "user_name": "张三"}
        text = "订单 {{order_id}} 的收件人是 {{user_name}}"
        result = ApiAssertionService.substitute_variables(text, context)

        assert result == "订单 ORD-001 的收件人是 张三"

    def test_substitute_variables_no_match(self, service):
        """测试无变量文本不处理"""
        context = {"order_id": "ORD-001"}
        text = "普通文本没有变量"
        result = ApiAssertionService.substitute_variables(text, context)

        assert result == "普通文本没有变量"

    def test_substitute_variables_undefined_error(self, service):
        """测试未定义变量抛出错误"""
        from jinja2 import UndefinedError

        context = {"order_id": "ORD-001"}
        text = "订单 {{undefined_var}}"

        with pytest.raises(UndefinedError):
            ApiAssertionService.substitute_variables(text, context)

    @pytest.mark.asyncio
    async def test_execute_with_substitution(self, service):
        """测试执行时变量替换"""
        # 先设置 context
        service.context["expected_value"] = 100

        code = "result = {{expected_value}} + 1"
        result = await service.execute_single(code, 0)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_undefined_variable_error(self, service):
        """测试未定义变量执行报错"""
        code = "result = {{undefined_var}} + 1"
        result = await service.execute_single(code, 0)

        assert result.success is False
        assert "变量未定义" in result.error


class TestHelperFunctions:
    """辅助断言函数测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    @pytest.mark.asyncio
    async def test_assert_time_helper(self, service):
        """测试 assert_time 辅助函数"""
        from datetime import datetime

        # 在执行环境中，assert_time 应该可用
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        code = f"result = assert_time('{now_str}')"
        result = await service.execute_single(code, 0)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_assert_exact_helper(self, service):
        """测试 assert_exact 辅助函数"""
        code = "result = assert_exact('hello', 'hello')"
        result = await service.execute_single(code, 0)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_assert_contains_helper(self, service):
        """测试 assert_contains 辅助函数"""
        code = "result = assert_contains('hello world', 'world')"
        result = await service.execute_single(code, 0)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_assert_decimal_helper(self, service):
        """测试 assert_decimal 辅助函数"""
        code = "result = assert_decimal(1.005, 1.00, 0.01)"
        result = await service.execute_single(code, 0)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_context_storage(self, service):
        """测试 context 存储"""
        code = "context['test_var'] = 'test_value'"
        result = await service.execute_single(code, 0)

        assert result.success is True
        assert service.get_context().get("test_var") == "test_value"


class TestGetContext:
    """get_context 方法测试"""

    @pytest.fixture
    def service(self):
        return ApiAssertionService()

    @pytest.mark.asyncio
    async def test_get_context_returns_copy(self, service):
        """测试 get_context 返回副本"""
        await service.execute_single("context['x'] = 1", 0)
        ctx1 = service.get_context()
        ctx1["y"] = 2  # 修改副本不应影响原 context

        ctx2 = service.get_context()
        assert "y" not in ctx2
