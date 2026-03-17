"""随机数生成器单元测试"""

import pytest

from backend.core.random_generators import (
    random_imei,
    random_numbers,
    random_phone,
    random_serial,
    sf_waybill,
)


class TestSfWaybill:
    """SF 物流单号生成测试"""

    def test_sf_waybill_format(self):
        """测试 SF 单号格式：SF 开头，共 14 位"""
        result = sf_waybill()
        assert result.startswith("SF"), f"应以 SF 开头，实际: {result}"
        assert len(result) == 14, f"长度应为 14，实际: {len(result)}"
        # SF 后面的 12 位应该是字母和数字的组合
        suffix = result[2:]
        assert suffix.isalnum(), f"后缀应为字母数字，实际: {suffix}"

    def test_sf_waybill_uniqueness(self):
        """测试 SF 单号唯一性"""
        results = [sf_waybill() for _ in range(100)]
        unique_results = set(results)
        assert len(unique_results) == 100, "100 次生成应全部唯一"


class TestRandomPhone:
    """手机号生成测试"""

    def test_random_phone_format(self):
        """测试手机号格式：13 开头，共 11 位"""
        result = random_phone()
        assert result.startswith("13"), f"应以 13 开头，实际: {result}"
        assert len(result) == 11, f"长度应为 11，实际: {len(result)}"
        assert result.isdigit(), f"应为纯数字，实际: {result}"

    def test_random_phone_uniqueness(self):
        """测试手机号唯一性"""
        results = [random_phone() for _ in range(100)]
        unique_results = set(results)
        assert len(unique_results) >= 95, "100 次生成应有至少 95 个唯一值"


class TestRandomImei:
    """IMEI 生成测试"""

    def test_random_imei_format(self):
        """测试 IMEI 格式：I 开头，共 15 位"""
        result = random_imei()
        assert result.startswith("I"), f"应以 I 开头，实际: {result}"
        assert len(result) == 15, f"长度应为 15，实际: {len(result)}"
        assert result[1:].isdigit(), f"后 14 位应为纯数字，实际: {result}"


class TestRandomSerial:
    """序列号生成测试"""

    def test_random_serial_format(self):
        """测试序列号格式：8 位纯数字"""
        result = random_serial()
        assert len(result) == 8, f"长度应为 8，实际: {len(result)}"
        assert result.isdigit(), f"应为纯数字，实际: {result}"


class TestRandomNumbers:
    """指定长度随机数字测试"""

    def test_random_numbers_length(self):
        """测试指定长度生成"""
        for n in [1, 5, 10, 20]:
            result = random_numbers(n)
            assert len(result) == n, f"长度应为 {n}，实际: {len(result)}"
            assert result.isdigit(), f"应为纯数字，实际: {result}"

    def test_random_numbers_zero(self):
        """测试长度为 0"""
        result = random_numbers(0)
        assert result == "", f"长度为 0 应返回空字符串，实际: {result}"
