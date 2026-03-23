# coding: utf-8
import os

import gevent.monkey
import asyncio
import sys
from common.base_url import URL
from config.settings import DATA_PATHS

if DATA_PATHS['performance'] == 'close':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    gevent.monkey.patch_all()

import threading
import inspect
import json
import pyperclip
import requests
import random
import time
from common.log import Log
from common.file_cache import FileCache
from common.base_random_mixin import BaseRandomMixin
from datetime import datetime, timedelta
from functools import wraps


class BaseApi(BaseRandomMixin):
    """
    BaseApi 是所有 API 接口类的基础类，提供通用的数据生成、请求处理、响应解析等功能。
    """
    # 用于确保时间戳唯一性的类变量
    _last_timestamp = 0
    _timestamp_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {}  # 存储 HTTP 请求头信息
        self.sum = random.choice([1, 2])  # 随机选择1或2
        self.cache = FileCache()  # 初始化缓存对象
        self._headers = None  # 延迟加载
        self.urls = URL['api']  # 接口请求地址

    @property
    def headers(self):
        """
        获取请求头信息，使用延迟加载机制
        避免在初始化时产生循环依赖问题
        只有在首次访问时才会实例化 LoginApi 来获取 headers
        """
        if self._headers is None:
            from api.api_login import LoginApi
            self._headers = LoginApi().headers
        return self._headers

    @headers.setter
    def headers(self, value):
        """
        设置请求头信息
        :param value: 要设置的 headers 值
        """
        self._headers = value

    def get_formatted_datetime(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
        """
        获取当前时间，并支持增加指定年、月、日、时、分、秒数
        :param years: 要增加的年数（默认为 0）
        :param months: 要增加的月数（默认为 0）
        :param days: 要增加的天数（默认为 0）
        :param hours: 要增加的小时数（默认为 0）
        :param minutes: 要增加的分钟数（默认为 0）
        :param seconds: 要增加的秒数（默认为 0）
        :return: 格式化后的时间字符串
        """
        from dateutil.relativedelta import relativedelta
        current_time = datetime.now()
        adjusted_time = current_time + relativedelta(
            years=years,
            months=months,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
        return adjusted_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_current_time(self, hours=0, minutes=0, seconds=0):
        """
        获取当前时间的时分秒部分，支持增加指定小时、分钟和秒数
        :param hours: 要增加的小时数（默认为 0）
        :param minutes: 要增加的分钟数（默认为 0）
        :param seconds: 要增加的秒数（默认为 0）
        :return: 格式化后的时间字符串，格式为 HH:MM:SS
        """
        current_time = datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return current_time.strftime("%H:%M:%S")

    def get_the_date(self, days=0):
        """
        获取当前日期，并支持增加指定天数
        :param days: 要增加的天数（默认为 0）
        :return: 格式化后的日期字符串（仅年月日）
        """
        current_time = datetime.now() + timedelta(days=days)
        return current_time.strftime("%Y-%m-%d")

    def get_current_timestamp_ms(self):
        """
        获取当前时间戳（毫秒级），确保在高并发下唯一性
        :return: 整型时间戳
        """
        with self._timestamp_lock:
            # 使用更高精度的时间戳
            current_timestamp = int(datetime.now().timestamp() * 1000000)  # 微秒级
            # 确保时间戳递增
            if current_timestamp <= self._last_timestamp:
                current_timestamp = self._last_timestamp + 1

            self._last_timestamp = current_timestamp
            return current_timestamp

    def get_response_data(self, response, key, default_value=None, allow_empty=False, index=None):
        """
        从接口响应中提取指定字段的值
        :param response: 接口响应对象
        :param key: 要提取的字段名，如果是空字符串且响应是列表，则直接返回列表
        :param default_value: 若字段不存在时返回的默认值
        :param allow_empty: 是否允许空字符串/列表
        :param index: 当值为列表时，获取指定索引位置的值，默认为 None（不使用索引）
        :return: 提取到的值或默认值
        """
        try:
            if response:
                data = response.json()

                # 新增：如果 key 为空且响应数据是列表，直接返回
                if key == '' and isinstance(data, list):
                    return data if allow_empty or len(data) > 0 else default_value

                if isinstance(data, dict):
                    value = data.get(key)
                    if value is None:
                        return default_value

                    if index is not None and isinstance(value, list):
                        try:
                            print('--', 0 <= index, index < len(value), index == -1)
                            return [value[index]] if (0 <= index < len(value) or index == -1) else default_value
                        except (TypeError, IndexError):
                            return default_value

                    if isinstance(value, (list, str)) and not allow_empty:
                        return value if len(value) > 0 else default_value
                    return value
        except Exception as e:
            print(f"获取响应数据失败：{e}")
        return default_value

    def get_page_num(self, response):
        """
        根据接口返回内容计算总页码数量
        :param response: 接口响应对象
        :return: 总页码数 或 None
        """
        try:
            if response.status_code != 200:
                return None
            res = response.json()
            if res['total'] > 10:
                return int(res['total'] / 10) + 1
            else:
                return None
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None

    def _get_nested_field(self, data, field_path):
        """
        从嵌套字典结构中根据路径提取字段值
        :param data: 字典数据源
        :param field_path: 字段路径，用 '.' 分隔层级
        :return: 提取到的值 或 None
        """
        fields = field_path.split('.')
        current = data
        for field in fields:
            if isinstance(current, dict) and field in current:
                current = current[field]
            else:
                return None
        return current

    def get_token(self, response):
        """
        从登录响应中提取 token 值
        :param response: 登录接口响应对象
        :return: token 值 或 None
        """
        res = response.json()
        if 'data' in res:
            data = res['data']
            if isinstance(data, dict) and data:
                return data.get("access_token")
        return None

    def get_handle_response(self, response):
        """
        处理并返回接口原始响应数据
        """
        # 获取调用栈信息，跳过 _make_request 层
        caller_frame = inspect.currentframe().f_back.f_back  # 跳过 _make_request
        caller_name = caller_frame.f_code.co_name
        api_info = f"[{caller_name}] "

        try:
            # 定义状态码消息映射
            status_messages = {
                200: ("✅", "接口请求成功"),
                201: ("✅", "资源创建成功"),
                204: ("✅", "请求成功，无返回内容"),
                400: ("❌", "请求参数错误"),
                401: ("❌", "未授权访问"),
                403: ("❌", "禁止访问"),
                404: ("❌", "请求资源不存在"),
                500: ("❌", "服务器内部错误")
            }

            # 尝试解析JSON响应
            result = response.json() if response.content else None

            # 检查是否为预定义的状态码
            if response.status_code in status_messages:
                emoji, message = status_messages[response.status_code]
                print(f"{emoji} {api_info}{message} {response.status_code}")

                if response.status_code == 204:
                    return None
                else:
                    print(f"返回值: {result}")
                    return result
            # 检查是否为客户端错误 (4xx)
            elif 400 <= response.status_code < 500:
                print(f"❌ {api_info}客户端错误，状态码: {response.status_code}")
                print(f"错误信息: {result}")
                return result
            # 检查是否为服务器错误 (5xx)
            elif 500 <= response.status_code < 600:
                print(f"❌ {api_info}服务器错误，状态码: {response.status_code}")
                print(f"错误信息: {result}")
                return result
            # 未知状态码
            else:
                print(f"⚠️ {api_info}未知状态码: {response.status_code}")
                print(f"返回值: {result}")
                return result

        except json.JSONDecodeError:
            # 处理非JSON响应
            text_content = response.text
            if response.status_code == 200:
                print(f"✅ {api_info}接口请求成功（非JSON响应）")
                print(f"响应内容: {text_content}")
            else:
                print(f"❌ {api_info}请求失败，状态码: {response.status_code}")
                print(f"响应内容: {text_content}")
            return {"status_code": response.status_code, "content": text_content}
        except Exception as e:
            print(f"❌ {api_info}处理响应时发生异常: {e}")
            return None

    def _get_field_copy_value(self, method_name, header_key, field_name, index=0, copy_to_clipboard=True,
                              **method_kwargs):
        """
        通过指定方法获取数据，并从中提取字段值，可选复制到剪贴板
        :param method_name: 方法名称（字符串）
        :param header_key: 请求头中的键
        :param field_name: 字段路径（支持多级嵌套）
        :param index: 数据索引，默认为0（第一条数据）
        :param copy_to_clipboard: 是否复制到剪贴板
        :param method_kwargs: 传递给目标方法的额外参数
        :return: 提取到的字段值
        """
        method = getattr(self, method_name)

        # 特殊处理 headers 参数，避免冲突
        headers = self.headers[header_key]

        # 如果 method_kwargs 中包含 headers，则合并参数
        if 'headers' in method_kwargs:
            actual_headers = method_kwargs.pop('headers')
            res = method(headers=actual_headers, **method_kwargs)
        else:
            res = method(headers=headers, **method_kwargs)

        if field_name is None and res is None:
            return None
        if isinstance(res, list):
            if len(res) > 0:
                if index < len(res):
                    data = res[index]  # 使用指定索引获取数据
                else:
                    raise IndexError(f"索引 {index} 超出数据范围，数据长度为 {len(res)}")
            else:
                raise ValueError("列表为空，无法获取字段值")
        elif isinstance(res, dict):
            data = res
        else:
            raise TypeError("不支持的数据类型，期望为 dict 或 list")

        fields = field_name.split('.')
        value = data
        for field in fields:
            if isinstance(value, dict):
                value = value.get(field)
            elif isinstance(value, list) and value and isinstance(value[0], (dict, list)):
                value = value[0]
                value = value.get(field) if isinstance(value, dict) else None
            else:
                value = None
                break

        if value is None:
            raise KeyError(f"字段路径 {field_name} 不存在于数据中")

        if copy_to_clipboard and value is not None:
            try:
                pyperclip.copy(str(value))
            except Exception as e:
                print(f"复制到剪贴板失败: {e}")

        return value

    def get_cached_tokens(self):
        """
        从缓存中获取已保存的认证信息
        :return: 缓存中的 auth_data 数据 或 None
        """
        self.cache.clear_expired()
        serialized_data = self.cache.get('auth_data')
        return serialized_data or None

    def set_cached_tokens(self, data):
        """
        将认证信息写入缓存
        :param data: 要缓存的数据
        :return: None
        """
        self.cache.clear_expired()
        self.cache.set('auth_data', data, expire=3600)

    def get_page_params(self, num=1, size=10):
        """
        构造分页参数
        :param num: 页码（从1开始）
        :param size: 每页记录数
        :return: 包含 pageNum 和 pageSize 的字典
        """
        # 确保页码和每页大小都是正整数
        num = max(1, int(num))
        size = max(1, int(size))

        # 设置每页大小的上限，防止请求过多数据导致接口出错
        MAX_PAGE_SIZE = 1000  # 可根据实际接口限制调整
        size = min(size, MAX_PAGE_SIZE)

        return {'pageNum': num, 'pageSize': size}

    def request_handle(self, method, url, headers, data=None, report_name=None, stress=''):
        """
        发起 HTTP 请求并处理异常
        :param method: 请求方法（get/post/put/delete/patch）
        :param url: 请求地址
        :param headers: 请求头
        :param data: 请求体数据（可选）
        :param report_name: 性能测试报告文件名
        :return: 响应对象 或 抛出异常
        """
        # 根据配置参数决定是否打印请求信息
        if DATA_PATHS.get('print_request', False):
            print(f"请求地址: {url}")
            print(f"请求方法: {method}")
            print(f"请求头: {headers}")
            if data:
                # 如果data是字符串且可能是JSON格式，则尝试美化输出
                try:
                    # 尝试解析为JSON然后再格式化输出，避免中文显示为Unicode转义序列
                    parsed_data = json.loads(data)
                    formatted_data = json.dumps(parsed_data, ensure_ascii=False, indent=2)
                    print(f"请求参数: {formatted_data}")
                except json.JSONDecodeError:
                    # 如果不是有效的JSON，则直接输出原数据
                    print(f"请求参数: {data}")

        def make_request():
            try:
                timeout = 60  # 统一设置超时时间

                # 创建请求方法映射
                request_methods = {
                    'get': lambda: requests.get(url, headers=headers, timeout=timeout),
                    'post': lambda: requests.post(url, headers=headers, data=data, timeout=timeout,
                                                  proxies={'http': '', 'https': ''}),
                    'put': lambda: requests.put(url, headers=headers, data=data, timeout=timeout),
                    'delete': lambda: requests.delete(url, headers=headers, data=data, timeout=timeout),
                    'patch': lambda: requests.patch(url, headers=headers, data=data, timeout=timeout)
                }

                # 检查方法是否支持
                if method.lower() not in request_methods:
                    raise ValueError(f"不支持的HTTP方法: {method}")

                # 执行请求
                response = request_methods[method.lower()]()

                # 性能测试 - 只在明确需要时执行
                if (DATA_PATHS.get('performance') == 'open' and
                        '/auth/login' not in url and  # 只在特定条件下执行
                        not DATA_PATHS.get('auto_type') == 'ui'
                ):  # UI模式下不执行性能测试

                    # 执行性能测试
                    api_config = [{
                        "endpoint": url,
                        "name": url,
                        "report_name": url.replace('https://erptest.epbox.cn/epbox_erp', '').replace('/', '_'),
                        "method": method.upper(),
                        "data": stress,
                        "headers": headers,
                        "timeout": timeout
                    }]

                    try:
                        from common.locust_use import LocustPerformanceTest
                        LocustPerformanceTest.run_performance_test(
                            api_configs=api_config,
                            users=DATA_PATHS.get('performance_user'),
                            spawn_rate=DATA_PATHS.get('performance_spawn_rate'),
                            run_time=DATA_PATHS.get('performance_run_time'),
                        )
                        LocustPerformanceTest.merge_csv_reports()
                    except ImportError as e:
                        print(f"无法导入性能测试模块: {e}")
                        print("跳过性能测试，继续执行请求")

                # 检查响应状态码和内容（仅在错误时记录日志，减少I/O操作）
                if response and response.status_code not in [200, 201, 204]:
                    Log.log_save(f"接口地址{url}请求失败: 状态码 {response.status_code}", type='error')
                elif response:
                    try:
                        ary = response.json() if response.content else {}
                        if isinstance(ary, dict) and ary.get('code') not in [200, None]:
                            Log.log_save(f"接口地址{url}请求错误: code={ary.get('code')}", type='error')
                    except Exception:
                        pass  # 忽略JSON解析错误

                return response

            except Exception as e:
                Log.log_save(f"接口地址{url}请求错误: {e}", type='error')
                raise

        return self.handle_api_error(make_request)

    def handle_api_error(self, func):
        """
        统一处理接口请求过程中的异常并记录日志
        :param func: 待执行的函数
        :return: 函数执行结果 或 抛出异常
        """
        exception_handlers = {
            KeyError: "【配置缺失】找不到指定的请求地址或字段，请检查配置文件",
            ConnectionError: "【网络连接失败】请检查网络状态或服务器是否可用",
            TimeoutError: "【请求超时】服务器无响应，请检查接口稳定性或增加超时时间",
            json.JSONDecodeError: "【响应解析失败】返回内容不是合法的 JSON 格式",
        }
        try:
            return func()
        except Exception as e:
            exception_type = type(e)
            if exception_type in exception_handlers:
                msg = exception_handlers[exception_type]
                print(f"{msg}- {str(e)}")
            else:
                print(f"【接口异常】发生未知错误: {str(e)}")
            raise

    def check_unsupported_params(self, provided_params, supported_params, method_name):
        """
        检查是否有不支持的参数，如果有则抛出异常
        :param provided_params: 提供的参数列表
        :param supported_params: 支持的参数集合
        :param method_name: 方法名称
        """
        unsupported_params = set(provided_params) - supported_params
        if unsupported_params:
            raise ValueError(f"Method '{method_name}' 断言参数名填写错误 {unsupported_params}")

    def process_params(self, kwargs, param):
        """
        处理参数映射
        :param kwargs: 输入参数
        :param param: 参数映射字典，格式为 {internal_key: (external_key, value_processor)}
        :return: (data, supported_params)
        """
        data = {}
        supported_params = set()
        for internal_key, (external_key, value_processor) in param.items():
            if kwargs.get(internal_key) is not None:
                supported_params.add(internal_key)
                value = kwargs[internal_key]
                if value_processor:
                    if callable(value_processor):
                        value = value_processor(
                            value) if value_processor.__name__ != 'get_formatted_datetime' else self.get_formatted_datetime()
                    else:
                        value = value_processor
                # 检查是否为嵌套字段（包含点号）
                if '.' in external_key and isinstance(value, list) and len(value) > 0:
                    print('--', external_key)
                    processed_values = []
                    for item in value:
                        if isinstance(item, dict):
                            nested_value = self._get_nested_field(item, external_key)
                            if nested_value is not None:
                                processed_values.append(nested_value)
                        else:
                            processed_values.append(item)
                    data[external_key] = processed_values
                else:
                    data[external_key] = value
        return data, supported_params

    def process_and_check_params(self, kwargs, param_mapping, method_name):
        """
        处理参数并检查不支持的参数
        :param kwargs: 输入参数
        :param param_mapping: 参数映射
        :param method_name: 方法名
        :return: 处理后的数据
        """
        data, supported_params = self.process_params(kwargs, param_mapping)
        self.check_unsupported_params(kwargs.keys(), supported_params, method_name)
        return data

    def timing_decorator(func):
        """
        装饰器：用于统计接口请求时间
        此装饰器用于包装接口请求方法，自动计算并打印方法执行的时间。
        如果执行时间大于等于1秒，则以秒为单位显示；否则以毫秒为单位显示。
        Args:
            func: 被装饰的函数
        Returns:
            被装饰函数的执行结果
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            # 执行原始函数
            result = func(self, *args, **kwargs)
            end_time = time.time()
            request_time = end_time - start_time
            # 自动选择合适的单位
            if request_time >= 1.0:
                print(f"接口请求耗时: {request_time:.4f} 秒")
            else:
                print(f"接口请求耗时: {request_time * 1000:.2f} 毫秒")
            return result

        return wrapper

    def save_to_cache(self, key, value, cache_dir='cache_assert', filename="parameter_data.json", timestamp=True):
        """
        将数据保存到缓存文件
        :param key: 缓存键值，建议使用测试用例名称或唯一标识
        :param value: 需要保存的值，如obj的值
        :param cache_dir: 缓存目录，默认为cache
        :param filename: 缓存文件名，默认为parameter_data.json
        :param timestamp: 是否添加时间戳
        """
        import os
        from datetime import datetime

        # 创建缓存目录
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        cache_file = f"{cache_dir}/{filename}"
        cache_data = {
            'value': value,
            'timestamp': datetime.now().isoformat() if timestamp else None
        }
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"已保存 {key} 到缓存: {value}")

    def load_from_cache(self, cache_dir='cache_assert', filename="parameter_data.json"):
        """
        从缓存文件加载数据
        :param cache_dir: 缓存目录，默认为cache
        :param filename: 缓存文件名，默认为parameter_data.json
        :return: 缓存的数据，如果不存在则返回None
        """
        import os

        cache_file = f"{cache_dir}/{filename}"
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                return cache_data['value']
        return None

    def get_file_and_class_name(self):
        """
        获取调用该方法的类名和方法名
        :return: (class_name, method_name) - 调用者的类名和方法名
        """
        # 获取调用栈
        frame = inspect.currentframe()
        try:
            # 获取调用者的帧
            caller_frame = frame.f_back

            # 获取调用者的方法名
            caller_method_name = caller_frame.f_code.co_name

            # 获取调用者所在的文件名
            caller_filename = caller_frame.f_code.co_filename
            # 获取项目根目录
            project_root = os.path.dirname(os.path.abspath(__file__)).replace('common', '')
            file_name = caller_filename.replace(project_root, '').replace('.py', '').replace('\\', '.')

            # 获取调用者所在的类实例
            caller_self = caller_frame.f_locals.get('self')
            if caller_self:
                caller_class_name = caller_self.__class__.__name__
            else:
                # 如果不是实例方法，尝试获取类名
                caller_class_name = None
                # 检查是否是类方法
                if 'cls' in caller_frame.f_locals:
                    caller_cls = caller_frame.f_locals['cls']
                    if hasattr(caller_cls, '__name__'):
                        caller_class_name = caller_cls.__name__

            return file_name, caller_class_name, caller_method_name
        finally:
            # 避免循环引用
            del frame

    def generate_hourly_sessions(self):
        """暗拍直拍专用：生成每小时一场的场次配置列表（09:00:00 到 23:59:59）"""
        sessions = []
        # 只循环 9 到 23 点，共 15 场
        for hour in range(9, 24):
            start_time = f"{self.get_the_date()} {hour:02d}:00:00"
            end_time = f"{self.get_the_date()} {hour:02d}:59:59"
            show_time = f"{self.get_the_date()} {hour:02d}:30:00"

            sessions.append({
                "name": "场次" + self.serial,
                "showTime": show_time,
                "startTime": start_time,
                "endTime": end_time
            })
        return sessions

    def generate_five_minute_sessions(self, count=1):
        """暗拍直拍专用：
        生成每5分钟一场的场次配置列表
        :param count: 生成场次数量，默认为1
        :return: 包含开始时间和结束时间的场次列表
        """
        sessions = []
        for i in range(count):
            # 获取当前时间
            current_time = datetime.now()
            # 计算当前分钟数
            current_minute = current_time.minute
            # 计算下一个5分钟间隔的时间
            # 例如：如果当前是14:23，则计算到14:25（向上取到最近的5的倍数）
            next_five_minute = ((current_minute // 5) + 1) * 5
            if next_five_minute >= 60:
                # 如果分钟数超过或等于60，需要跳到下个小时
                next_five_minute = 0
                current_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            else:
                # 设置到下一个5分钟间隔
                current_time = current_time.replace(minute=next_five_minute, second=0, microsecond=0)

            # 如果是第一个场次，使用计算的时间；后续场次按5分钟递增
            start_time = current_time + timedelta(minutes=5 * i)
            end_time = start_time + timedelta(minutes=5)

            sessions.append({
                "name": f"场次{self.serial}{i + 1}",
                "showTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "startTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            })

        # 整个方法执行完成后额外等待10秒
        time.sleep(10)
        return sessions

    def wait_until_next_five_minute(self):
        """等待到下一个5分钟整数时刻，复用现有的时间逻辑，并额外多等N秒"""
        current_time = datetime.now()
        current_minute = current_time.minute
        # 使用与生成场次相同的时间计算逻辑
        next_five_minute = ((current_minute // 5) + 1) * 5
        if next_five_minute >= 60:
            next_five_minute = 0
            current_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            current_time = current_time.replace(minute=next_five_minute, second=0, microsecond=0)

        start_time = current_time
        wait_seconds = (start_time - datetime.now()).total_seconds()

        # 额外多等N秒
        extra_wait_seconds = 20
        total_wait_seconds = wait_seconds + extra_wait_seconds

        if total_wait_seconds > 0:
            print(
                f"等待 {total_wait_seconds:.2f} 秒直到下一个5分钟整数时刻: {start_time.strftime('%H:%M:%S')} (额外多等5秒)")
            time.sleep(total_wait_seconds)

    def save_json_file(self, data, filename):
        """
        将数据保存为 JSON 文件
        :param data: 要保存的数据（通常是字典或列表）
        :param filename: 保存的文件名
        """
        try:
            # 获取当前工作目录
            current_path = os.getcwd()
            file_path = os.path.join(current_path, filename)

            # 将数据写入 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"数据已成功保存到 {file_path}")
        except Exception as e:
            print(f"保存文件时发生错误: {e}")

    def wait_for_five_minutes(self):
        """
        强制等待分钟，加秒缓冲时间
        """
        base_wait = 5 * 60
        buffer = 10  # 额外时间
        wait_time = base_wait + buffer
        print(f"开始强制等待 ({wait_time}秒)...")
        time.sleep(wait_time)
        print("等待完成")

    def wait_default(self):
        """
        强制等待秒
        """
        wait_time = 3
        print(f"开始强制等待 ({wait_time}秒)...")
        time.sleep(wait_time)
        print("等待完成")

    @staticmethod
    def load_json_file(file_name):
        """
        加载单个JSON文件
        :param file_name: JSON文件名（不含路径）
        :return: JSON文件内容（字典或列表）
        """
        file_path = os.path.join(os.path.dirname(__file__), 'json', file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)