# coding: utf-8
from datetime import datetime, timedelta
from common.import_api import ImportApi
from common.log import Log


class BaseAssert:
    """
    BaseAssert 是所有断言类的基础类，提供通用的断言方法。
    """

    def __init__(self):
        self.api = ImportApi()

    def assert_time(self, res, desc):
        """
        断言时间是否在当前时间 ±1 分钟范围内。
        :param res: 实际时间字符串（格式：YYYY-MM-DD HH:MM:SS）
        :param desc: 时间描述信息
        :return: None
        """
        Log().log_save('--进入方法_assert_time---')
        res_dt = datetime.strptime(res, "%Y-%m-%d %H:%M:%S")
        now_dt = datetime.now()
        # 正确的±1分钟范围应该是基于当前真实时间
        min_dt = now_dt - timedelta(minutes=1)
        max_dt = now_dt + timedelta(minutes=1)
        assert min_dt <= res_dt <= max_dt, \
            f"预期时间在 [{min_dt.strftime('%Y-%m-%d %H:%M:%S')}, {max_dt.strftime('%Y-%m-%d %H:%M:%S')}] " \
            f"范围内，实际时间为: {res_dt.strftime('%Y-%m-%d %H:%M:%S')} ({desc})"

    def assert_contains(self, expect, res, field_name="", error_msg=""):
        """
        断言结果中是否包含预期内容（模糊匹配）。
        :param expect: 预期内容
        :param res: 实际结果
        :param field_name: 字段名
        :param error_msg: 自定义错误信息（可选）
        :return: None
        """
        Log().log_save('--进入方法_assert_contains---')
        str_expect = str(expect) if expect is not None else None
        str_res = str(res) if res is not None else ""

        # 打印字段比较信息，断言失败时添加 ❌ 符号
        if field_name:
            if str_expect is not None and str_expect != "":
                match_success = str_expect in str_res
            else:
                match_success = str_expect == str_res
            status_symbol = "" if match_success else " ❌"
            print(f"字段 '{field_name}' 比较: 预期='{str_expect}', 实际='{str_res}'{status_symbol}")

        if str_expect is not None:
            if str_expect == "":
                assert str_res == "", error_msg or f"字段 '{field_name}' 预期为: '{str_expect}', 实际值: '{str_res}'"
            else:
                assert str_expect in str_res, error_msg or f"字段 '{field_name}' 预期包含: '{str_expect}', 实际值: '{str_res}'"
        else:
            assert str_expect == str(
                res), error_msg or f"字段 '{field_name}' 预期值: '{str_expect}', 实际值: '{str_res}'"

    def assert_equal(self, expect, res, field_name="", error_msg=""):
        """
        精确断言两个值是否相等，特别适用于整型数字的精确匹配。
        :param expect: 预期值
        :param res: 实际值
        :param field_name: 字段名
        :param error_msg: 自定义错误信息（可选）
        :return: None
        """
        Log().log_save('--进入方法_assert_equal---')
        # 打印字段比较信息，断言失败时添加 ❌ 符号
        if field_name:
            match_success = expect == res
            status_symbol = "" if match_success else " ❌"
            print(f"字段 '{field_name}' 比较: 预期='{expect}', 实际='{res}'{status_symbol}")

        assert expect == res, error_msg or f"字段 '{field_name}' 预期值: '{expect}', 实际值: '{res}'"

    def _get_field_value(self, data, key_path):
        """
        通用字段值提取方法，支持嵌套字典和数组
        :param data: 数据源
        :param key_path: 点号分隔的键路径，如 'saleOrderInfo.salePaymentStatus'
        :return: 对应的值或None
        """
        keys = key_path.split('.')
        current = data

        for i, key in enumerate(keys):
            if isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    return None
            elif isinstance(current, list):
                if key.isdigit():  # 数组索引
                    index = int(key)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        return None
                else:  # 数组中字典的字段
                    if len(current) > 0:
                        current = current[0]
                        if isinstance(current, dict) and key in current:
                            current = current[key]
                        else:
                            return None
                    else:
                        return None
            else:
                return None

        return current

    def _print_result(self, result, actual_res):
        """
        全局打印结果方法
        :param result: 预期结果
        :param actual_res: 实际结果
        :return: None
        """
        # print('响应数据：', result, actual_res)

    def _is_numeric_string(self, s):
        """
        检查字符串是否为纯数字（允许一个小数点）
        :param s: 待检查的字符串
        :return: bool 是否为纯数字字符串
        """
        if not isinstance(s, str):
            return False
        # 允许一个负号开头
        if s.startswith('-'):
            s = s[1:]
        # 检查是否为数字（最多一个小数点）
        return s.replace('.', '', 1).isdigit() and s.count('.') <= 1

    def _extract_actual_value(self, actual_res, key):
        """
        提取实际值的辅助方法
        :param actual_res: 实际响应结果
        :param key: 字段键名
        :return: 实际值
        """
        actual_value = None
        if isinstance(actual_res, dict):
            # 如果 actual_res 是字典
            if '.' in key and key not in actual_res:
                # 处理嵌套字段(如: 'user.name'格式)
                actual_value = self._get_field_value(actual_res, key)
            else:
                actual_value = actual_res.get(key)
        elif isinstance(actual_res, (list, tuple)) and len(actual_res) > 0:
            # 如果 actual_res 是非空列表或元组
            if isinstance(actual_res[0], dict):
                if '.' in key and key not in actual_res[0]:
                    # 处理嵌套字段
                    actual_value = self._get_field_value(actual_res[0], key)
                else:
                    actual_value = actual_res[0].get(key)
            else:
                # 如果列表第一个元素不是字典，直接使用该元素（适用于只有一个值的情况）
                actual_value = actual_res[0]
        elif isinstance(actual_res, str) and hasattr(self, 'result') and len(self.result) == 1:
            # 如果 actual_res 是字符串，且只期望一个结果
            actual_value = actual_res
        else:
            raise TypeError(f"无法处理的数据结构: {type(actual_res)}")
        return actual_value

    def _compare_values(self, expected, actual, field_name):
        """
        统一的值比较方法，根据类型自动选择比较策略
        :param expected: 预期值
        :param actual: 实际值
        :param field_name: 字段名
        :return: 比较结果字符串
        """
        # 时间字段特殊处理
        if self._is_time_field(field_name):
            return self._compare_time_values(expected, actual, field_name)
        # None值处理
        if expected is None:
            return self._compare_none_values(actual, field_name)
        # 根据类型组合进行处理
        return self._compare_by_types(expected, actual, field_name)

    def _is_time_field(self, field_name):
        """判断是否为时间字段"""
        return field_name.endswith('Time') or field_name.endswith('time')

    def _compare_time_values(self, expected, actual, field_name):
        """处理时间字段比较"""
        if actual and expected:
            try:
                self.assert_time(actual, field_name)
                # 成功时的打印信息
                comparison_result = f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
                print(comparison_result)
                return comparison_result
            except AssertionError as e:
                # 失败时的处理
                comparison_result = f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}' ❌"
                print(comparison_result)
                raise  # 重新抛出异常以确保断言失败被正确处理
        else:
            # 时间字段为空时的处理
            match_success = (expected is None and actual is None) or (expected == actual)
            status_symbol = "" if match_success else " ❌"
            comparison_result = f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'{status_symbol}"
            print(comparison_result)
            if not match_success:
                self.assert_contains(expected, actual, field_name,
                                     f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
            return comparison_result

    def _compare_none_values(self, actual, field_name):
        """处理None值比较"""
        match_success = actual is None
        status_symbol = "" if match_success else " ❌"
        comparison_result = f"字段 '{field_name}' 比较: 预期='None', 实际='{actual}'{status_symbol}"
        if not match_success:
            raise AssertionError(f"字段 '{field_name}' 预期为None，实际'{actual}'")
        return comparison_result

    def _compare_by_types(self, expected, actual, field_name):
        """根据数据类型进行比较"""
        # 数值类型比较
        if self._is_both_numeric(expected, actual):
            return self._compare_numeric_values(expected, actual, field_name)
        elif isinstance(expected, str) and isinstance(actual, (int, float)):
            return self._compare_str_to_num(expected, actual, field_name)
        elif isinstance(expected, (int, float)) and isinstance(actual, str):
            return self._compare_num_to_str(expected, actual, field_name)
        elif isinstance(expected, str) and isinstance(actual, str):
            return self._compare_string_values(expected, actual, field_name)
        elif actual is not None:
            # 其他情况使用模糊匹配
            return self._compare_fuzzy_values(expected, actual, field_name)
        else:
            # 找不到对应值的情况
            raise KeyError(f"无法找到键 '{field_name}' 对应的值")

    def _is_both_numeric(self, val1, val2):
        """判断两个值是否都为数值类型"""
        return ((isinstance(val1, (int, float)) and isinstance(val2, (int, float))) or
                (isinstance(val1, str) and self._is_numeric_string(val1) and
                 isinstance(val2, str) and self._is_numeric_string(val2)))

    def _compare_numeric_values(self, expected, actual, field_name):
        """处理数值类型比较"""
        # 如果两个都是纯数字字符串，则进行数值精确比较
        if isinstance(expected, str) and isinstance(actual, str) and self._is_numeric_string(
                expected) and self._is_numeric_string(actual):
            try:
                # 转换为数值进行比较
                if '.' in expected or '.' in actual or isinstance(expected, float) or isinstance(actual, float):
                    num_expected = float(expected)
                    num_actual = float(actual)
                else:
                    num_expected = int(expected)
                    num_actual = int(actual)

                self.assert_equal(num_expected, num_actual, field_name,
                                  f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
                return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
            except AssertionError:
                raise
        else:
            try:
                self.assert_equal(expected, actual, field_name,
                                  f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
                return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
            except AssertionError:
                raise

    def _compare_str_to_num(self, expected, actual, field_name):
        """处理字符串数字与数值类型的比较"""
        try:
            # 尝试将字符串转换为数值进行精确比较
            if '.' in str(expected):
                converted_value = float(expected)
            else:
                converted_value = int(expected)
            self.assert_equal(converted_value, actual, field_name,
                              f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
            return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
        except (ValueError, AssertionError):
            raise

    def _compare_num_to_str(self, expected, actual, field_name):
        """处理数值与字符串类型的比较"""
        try:
            # 将数值转换为字符串进行比较
            if isinstance(expected, float) and expected.is_integer():
                str_value = str(int(expected))
            else:
                str_value = str(expected)
            self.assert_equal(str_value, actual, field_name,
                              f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
            return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
        except AssertionError:
            raise

    def _compare_string_values(self, expected, actual, field_name):
        """处理字符串与字符串比较"""
        # 如果两个都是纯数字字符串，则进行数值精确比较
        if self._is_numeric_string(expected) and self._is_numeric_string(actual):
            try:
                # 转换为数值进行比较
                if '.' in expected or '.' in actual:
                    num_expected = float(expected)
                    num_actual = float(actual)
                else:
                    num_expected = int(expected)
                    num_actual = int(actual)

                self.assert_equal(num_expected, num_actual, field_name,
                                  f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
                return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
            except AssertionError:
                raise
        else:
            # 非纯数字字符串使用模糊匹配
            try:
                self.assert_contains(expected, actual, field_name,
                                     f"字段 '{field_name}' 预期包含: '{expected}'，实际: '{actual}'")
                return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
            except AssertionError:
                raise

    def _compare_fuzzy_values(self, expected, actual, field_name):
        """处理其他字符串模糊匹配"""
        try:
            self.assert_contains(expected, actual, field_name,
                                 f"字段 '{field_name}' 预期: '{expected}'，实际: '{actual}'")
            return f"字段 '{field_name}' 比较: 预期='{expected}', 实际='{actual}'"
        except AssertionError:
            raise

    def base_action(self, result, actual_res):
        """
        断言基础方法，用于比较预期结果和实际结果
        Args:
            result (dict): 预期结果字典，键为字段名，值为预期值
            actual_res (dict/list/tuple/str): 实际响应结果
        Raises:
            TypeError: 当无法处理actual_res的数据结构时抛出
            AssertionError: 当断言失败时抛出
            KeyError: 当无法找到对应键时抛出
        """
        self._print_result(result, actual_res)
        self.result = result  # 保存result供_extract_actual_value使用
        comparison_results = []
        for key, value in result.items():
            # 提取实际值
            actual_value = self._extract_actual_value(actual_res, key)
            try:
                # 使用统一比较方法处理比较
                comparison_result = self._compare_values(value, actual_value, key)
                comparison_results.append(comparison_result)
                # print(comparison_result)
            except AssertionError as e:
                comparison_result = f"字段 '{key}' 比较: 预期='{value}', 实际='{actual_value}' ❌"
                comparison_results.append(comparison_result)
                # print(comparison_result)
                raise
            except KeyError as e:
                comparison_result = f"字段 '{key}' 比较: 预期='{value}', 实际='{actual_value}' ❌"
                comparison_results.append(comparison_result)
                # print(comparison_result)
                raise

    def _validate_fields(self, validator_func, actual_res, **kwargs):
        """
        通用字段验证方法
        Args:
            validator_func: 验证函数(如 AttachmentRes().inventory_list)
            actual_res: 实际响应结果
            **kwargs: 需要验证的字段键值对
        """
        errors = []
        for field_name, expected_value in kwargs.items():
            try:
                single_field_kwargs = {field_name: expected_value}
                result = validator_func(**single_field_kwargs)
                self.base_action(result, actual_res)
            except AssertionError as e:
                errors.append(str(e))
            except Exception as e:
                errors.append(f"验证字段 '{field_name}' 时发生错误: {str(e)}")
        if errors:
            raise AssertionError("\n".join(errors))
        return True

    def _process_headers(self, obj, headers, header_mapping=None):
        """
        通用header处理方法
        Args:
            obj: API对象
            headers: 传入的header标识
            header_mapping: 自定义header映射关系，格式为 {标识: header_key}
        Returns:
            处理后的header
        """
        if header_mapping is None:
            # 默认映射关系
            header_mapping = {
                'main': 'main',
                'idle': 'idle',
                'vice': 'vice',
                'special': 'special',
                'platform': 'platform',
                'super': 'super',
                'camera': 'camera',
            }

        if headers is None:
            return obj.headers['main']
        elif headers in header_mapping:
            header_key = header_mapping[headers]
            return obj.headers[header_key]
        else:
            return headers  # 如果不匹配任何规则，直接返回原值

    def _assert_api_response(self, api_attr, methods_map, validator, headers=None, method='list', **kwargs):
        """
        通用API响应断言方法
        :param api_attr: API属性名
        :param methods_map: 方法映射字典
        :param validator: 验证器
        :param headers: 请求头
        :param method: 方法名
        :param kwargs: 验证字段参数，也可以包含其他传递给API方法的参数（如i参数）
        :return: 验证结果
        """
        if not kwargs:
            return True

        # 分离验证字段参数和其他参数
        validation_kwargs = {}
        api_call_kwargs = {}

        # 定义可能传递给API方法的特殊参数
        special_params = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','headers']  # 添加所有可能的特殊参数
        for key, value in kwargs.items():
            if key in special_params:
                api_call_kwargs[key] = value
            else:
                validation_kwargs[key] = value

        try:
            obj = getattr(self.api, api_attr)
        except AttributeError:
            # 如果self.api中没有该属性，抛出异常
            raise AttributeError(
                f"'ImportApi' object has no attribute '{api_attr}'")

        if method not in methods_map:
            raise ValueError(f"不支持的方法: {method}, 支持的方法: {list(methods_map.keys())}")

        # 将headers参数和其他参数一起传递给API方法
        api_params = {'headers': self._process_headers(obj, headers)}
        api_params.update(api_call_kwargs)

        actual_res = methods_map[method](**api_params)
        return self._validate_fields(validator, actual_res, **validation_kwargs)
