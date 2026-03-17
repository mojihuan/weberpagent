"""时间计算工具单元测试"""

import pytest
from datetime import datetime, timedelta
from backend.core.time_utils import time_now


class TestTimeNow:
    """time_now 函数测试"""

    def test_time_now_format(self):
        """测试返回格式为 '%Y-%m-%d %H:%M:%S'"""
        result = time_now()
        # 验证格式：尝试解析
        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        assert isinstance(parsed, datetime)

    def test_time_now_current(self):
        """测试无偏移时返回当前时间"""
        before = datetime.now()
        result = time_now()
        after = datetime.now()

        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

        # 结果应在调用前后之间（允许 1 秒误差）
        assert before - timedelta(seconds=1) <= parsed <= after + timedelta(seconds=1)

    def test_time_now_future(self):
        """测试正偏移返回未来时间"""
        offset = 30
        result = time_now(offset)
        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

        expected = datetime.now() + timedelta(minutes=offset)
        # 允许 1 秒误差
        assert abs((parsed - expected).total_seconds()) < 1

    def test_time_now_past(self):
        """测试负偏移返回过去时间"""
        offset = -15
        result = time_now(offset)
        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

        expected = datetime.now() + timedelta(minutes=offset)
        # 允许 1 秒误差
        assert abs((parsed - expected).total_seconds()) < 1

    def test_time_now_zero_offset(self):
        """测试偏移为 0 等同于无偏移"""
        result_default = time_now()
        result_zero = time_now(0)

        # 两个调用应在同一秒内
        parsed_default = datetime.strptime(result_default, "%Y-%m-%d %H:%M:%S")
        parsed_zero = datetime.strptime(result_zero, "%Y-%m-%d %H:%M:%S")

        assert abs((parsed_default - parsed_zero).total_seconds()) < 1

    def test_time_now_large_offset(self):
        """测试大偏移值"""
        # 测试 1440 分钟 = 24 小时 = 1 天
        result = time_now(1440)
        parsed = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

        expected = datetime.now() + timedelta(days=1)
        # 允许 1 秒误差
        assert abs((parsed - expected).total_seconds()) < 1
