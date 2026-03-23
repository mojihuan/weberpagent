# -*- coding: utf-8 -*-
import glob
import subprocess
import sys
import json
import os
import shutil
from urllib.parse import urlencode
import pandas as pd
from locust import HttpUser, task, between, SequentialTaskSet
from common.base_url import ENV, URL
import logging
import time
import copy
import uuid
import threading
from functools import wraps
import importlib
import inspect

""" Locust 性能测试封装类 """

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局 URL 映射表，用于存储装饰器注册的性能测试配置
PERFORMANCE_TEST_REGISTRY = {}


# 从设置中读取性能测试开关
def is_performance_enabled():
    """检查是否启用了性能测试"""
    try:
        from config.settings import DATA_PATHS
        return DATA_PATHS.get('performance', 'close') == 'open'
    except ImportError:
        return False


def performance_test(endpoint=None, method='POST', headers=None, timeout=60, auto_extract=True):
    """
    性能测试装饰器

    Args:
        endpoint (str): API 端点 URL，如果为 None 则自动从被装饰方法中提取
        method (str): HTTP 方法，默认 POST
        headers (dict): 请求头，默认为{"Content-Type": "application/json"}
        timeout (int): 超时时间，默认 60 秒
        auto_extract (bool): 是否自动从被装饰方法中提取 URL，默认 True
    """

    def decorator(func):
        # 检查是否启用了性能测试
        if not is_performance_enabled():
            # 如果未启用性能测试，返回原函数而不做任何装饰
            return func

        # 获取模块名和类名（从 func.__qualname 推断）
        qualname_parts = func.__qualname__.split('.')
        if len(qualname_parts) >= 2:
            class_name = qualname_parts[-2]
            method_name = func.__qualname__
        else:
            class_name = func.__self__.__class__.__name__ if hasattr(func, '__self__') else 'UnknownClass'
            method_name = func.__name__

        # 获取模块名（从 func.__module 获取）
        module_name = func.__module__

        # 如果启用自动提取且 endpoint 为 None，则延迟注册 URL
        if auto_extract and endpoint is None:
            # 将方法信息存储起来，稍后通过调用方法来获取真实 URL
            PERFORMANCE_TEST_REGISTRY[method_name] = {
                "module": module_name,
                "class": class_name,
                "method": method_name,
                "http_method": method,
                "headers": headers or {"Content-Type": "application/json"},
                "timeout": timeout,
                "auto_extract": True
            }
        else:
            # 手动指定了 endpoint，直接注册
            PERFORMANCE_TEST_REGISTRY[endpoint] = {
                "module": module_name,
                "class": class_name,
                "method": method_name,
                "http_method": method,
                "headers": headers or {"Content-Type": "application/json"},
                "timeout": timeout,
                "auto_extract": False,
                "manual_endpoint": endpoint
            }

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # 如果启用了自动提取且还没有注册真实 URL，则尝试获取
            if auto_extract and endpoint is None:
                try:
                    # 尝试从被调用的方法中获取真实的请求 URL
                    # 这里需要根据实际的实现方式来获取
                    instance = args[0] if args else None
                    if hasattr(instance, 'get_instantiation'):
                        api_instance = instance.get_instantiation()
                        # 这里需要根据你的具体实现来获取 URL
                        # 可能需要改进此部分以适应你的代码结构
                except Exception as e:
                    logger.warning(f"无法自动提取 URL: {e}")

            return result

        # 添加标记，表示这是一个性能测试方法
        wrapper.is_performance_test = True
        wrapper.performance_config = {
            "endpoint": endpoint,
            "method": method,
            "headers": headers or {"Content-Type": "application/json"},
            "timeout": timeout,
            "auto_extract": auto_extract
        }

        return wrapper

    return decorator


def extract_real_urls_from_methods():
    """
    从已注册的方法中提取真实的 URL
    需要在适当的时候调用此函数
    """
    for key, config in PERFORMANCE_TEST_REGISTRY.items():
        if config.get("auto_extract", False):
            try:
                # 动态导入模块和类
                module = __import__(config['module'], fromlist=[config['class']])

                cls = getattr(module, config['class'])

                # 创建实例并获取真实 URL
                instance = cls()

                # 获取方法并尝试调用以获得真实 URL
                method_obj = getattr(instance, config['method'])

                # 从方法中提取真实 URL 的逻辑
                # 这取决于你的方法是如何实现的
                real_url = get_url_from_method(method_obj)

                if real_url:
                    # 将自动提取的 URL 注册到映射表中
                    PERFORMANCE_TEST_REGISTRY[real_url] = config
                    # 移除原来的方法名为 key 的条目
                    del PERFORMANCE_TEST_REGISTRY[key]

            except Exception as e:
                logger.error(f"提取 URL 失败：{e}")


def get_url_from_method(method_func):
    """
    从方法中提取 URL，需要根据你的具体实现调整
    """
    try:
        # 如果方法有特殊的属性来存储 URL
        if hasattr(method_func, '__self__'):
            instance = method_func.__self__
            # 根据你的实现方式来获取 URL
            # 这里只是一个示例，需要根据实际情况调整
            if hasattr(instance, 'urls'):
                # 需要确定哪个 URL 与这个方法关联
                # 可能需要在方法上添加注解或特殊属性来指定 URL
                pass
    except Exception as e:
        logger.error(f"获取 URL 失败：{e}")
    return None


def get_performance_tests():
    """获取所有注册的性能测试配置"""
    return PERFORMANCE_TEST_REGISTRY


def dynamic_method_call(call_string):
    """
    动态调用方法，支持参数传递
    Args:
        call_string: 格式为 "module.class.method" 或 "package.module.class.method"
        *args: 传递给方法的位置参数
        **kwargs: 传递给方法的关键字参数
    """
    parts = call_string.split('.')
    print('---par:', parts)

    if len(parts) < 3:
        raise ValueError(
            f"字符串格式错误，应为 'module.class.method' 或 'package.module.class.method' 格式，当前为：{call_string}")

    # 处理不同长度的调用字符串
    if len(parts) == 3:
        # 格式：module.class.method
        module_name, class_name, method_name = parts
    elif len(parts) >= 4:
        # 格式：package.module.class.method 或更复杂的路径
        module_name = '.'.join(parts[:-2])  # 重组模块路径
        class_name = parts[-2]
        method_name = parts[-1]
    else:
        raise ValueError(
            f"字符串格式错误，应为 'module.class.method' 或 'package.module.class.method' 格式，当前为：{call_string}")

    # 特殊处理：如果模块名是 common.base_params 且类名以 Request 结尾
    # 这通常意味着应该从 request 模块中查找
    # 同时处理 IndexShippingRequest 和 PersonalSalesServiceRequest
    if module_name == 'common.base_params' and (class_name.endswith('Request')):
        # 尝试从对应的 request 子模块中查找
        # 例如：PurchaseAddRequest -> request.request_purchase
        if class_name.startswith('Purchase'):
            module_name = 'request.request_purchase'
        elif class_name.startswith('Sell'):
            module_name = 'request.request_sell'
        elif class_name.startswith('Fulfillment'):
            module_name = 'request.request_fulfillment'
        elif class_name.startswith('Quality'):
            module_name = 'request.request_quality'
        elif class_name.startswith('Help'):
            module_name = 'request.request_help'
        elif class_name.startswith('Send'):
            module_name = 'request.request_send'
        elif class_name.startswith('Purse'):
            module_name = 'request.request_purse'
        elif class_name.startswith('Platform'):
            module_name = 'request.request_platform'
        elif class_name.startswith('Message'):
            module_name = 'request.request_message'
        elif class_name.startswith('Guarantee'):
            module_name = 'request.request_guarantee'
        elif class_name.startswith('Finance'):
            module_name = 'request.request_finance'
        elif class_name.startswith('Inventory'):
            module_name = 'request.request_inventory'
        elif class_name.startswith('Login'):
            module_name = 'request.request_login'
        elif class_name.startswith('Repair'):
            module_name = 'request.request_repair'
        elif class_name.startswith('Camera'):
            module_name = 'request.request_camera'
        elif class_name.startswith('Attachment'):
            module_name = 'request.request_attachment'
        elif class_name.startswith('Auction'):
            module_name = 'request.request_auction'
        elif class_name.startswith('Bidding'):
            module_name = 'request.request_bidding'
        elif class_name.startswith('Trafficker'):
            module_name = 'request.request_trafficker'
        else:
            # 无法推断，保持原模块名
            pass

    try:
        # 动态导入模块
        module = importlib.import_module(module_name)

        # 获取类
        target_class = getattr(module, class_name)

    except (ImportError, AttributeError) as e:
        # 如果从原模块找不到类，尝试从 request 模块查找
        # 这主要用于处理像 PurchaseAddRequest 这样的类
        if class_name.endswith('Request'):
            try:
                # 构建 request 模块路径
                # 根据类名自动推断模块
                base_name = class_name.replace('Request', '')
                # 尝试不同的命名模式
                possible_modules = [
                    f'request.request_{base_name.lower()}',
                    f'request.api_{base_name.lower()}',
                ]
                for request_module_name in possible_modules:
                    try:
                        print(f"尝试从 {request_module_name} 导入 {class_name}")
                        module = importlib.import_module(request_module_name)
                        target_class = getattr(module, class_name)
                        module_name = request_module_name  # 更新模块名用于后续错误信息
                        break
                    except (ImportError, AttributeError):
                        continue
                else:
                    # 所有尝试都失败
                    raise AttributeError(f"在所有可能的 request 模块中均未找到类 {class_name}")

            except Exception as retry_error:
                raise AttributeError(
                    f"locust_use 模块 {module_name} 及所有可能的 request 子模块中均不存在类 {class_name}: {e}"
                )
        else:
            raise AttributeError(
                f"locust_use 模块 {module_name} 中不存在类 {class_name} 或方法 {method_name}: {e}"
            )

    try:
        # 实例化类
        instance = target_class()

        # 获取并调用方法
        method = getattr(instance, method_name)

        if callable(method):
            # 如果方法可调用，执行方法，固定入参，不执行 http 请求，只生成数据
            result = method(nocheck=True)
            return result
        else:
            # 如果是属性，直接返回值
            return method
    except AttributeError as e:
        raise AttributeError(
            f"locust_use 模块 {module_name} 中的类 {class_name} 不存在方法 {method_name}: {e}"
        )

    except Exception as e:
        raise Exception(f"locust_use 调用过程中发生错误：{e}")


class PerformanceTestMixin:
    """性能测试混入类，提供性能测试相关方法"""

    def __new__(cls, *args, **kwargs):
        # 检查是否启用了性能测试，如果没有启用则返回一个普通对象
        if not is_performance_enabled():
            # 如果没有启用性能测试，创建一个基本对象而不应用混入类的功能
            class BasicObject:
                pass

            return object.__new__(BasicObject)
        return super().__new__(cls)

    def run_specific_performance_test(self, method_name, concurrency=10, duration=60):
        """
        运行特定方法的性能测试
        """
        # 首先检查性能测试是否启用
        if not is_performance_enabled():
            logger.info("性能测试未启用，跳过性能测试执行")
            return None

        # 首先尝试从方法名获取注册的配置
        config = None
        for key, cfg in PERFORMANCE_TEST_REGISTRY.items():
            if cfg.get('method') == method_name or key == method_name:
                config = cfg
                break

        if not config:
            raise ValueError(f"No performance test registered for method: {method_name}")

        # 获取真实的 API 实例来获取 URL
        api_instance = self.get_instantiation()

        # 根据方法名称映射到对应的 URL（这需要根据你的实际实现来调整）
        url_mapping = {
            'new_purchase_order_unpaid_journey': 'item_new_purchase_order',
        }

        url_key = url_mapping.get(method_name.split('.')[-1], '')
        if hasattr(api_instance, 'urls') and url_key in api_instance.urls:
            real_endpoint = api_instance.urls[url_key]
        else:
            # 如果找不到映射，使用配置中的 endpoint
            real_endpoint = config.get('manual_endpoint', method_name)

        # 构建 API 配置
        api_config = [{
            "endpoint": real_endpoint,
            "method": config.get("http_method", "POST"),
            "headers": config.get("headers", {"Content-Type": "application/json"}),
            "timeout": config.get("timeout", 60),
            "name": f"Performance Test - {real_endpoint}",
            "data": {}
        }]

        # 运行性能测试
        return LocustPerformanceTest.run_performance_test(
            api_configs=api_config,
            users=concurrency,
            spawn_rate=min(concurrency, 10),
            run_time=f"{duration}s",
            headless=True
        )


class LocustTaskSet(SequentialTaskSet):
    """顺序执行的任务集"""

    def on_start(self):
        """任务开始时的初始化操作"""
        # 检查性能测试是否启用
        if not is_performance_enabled():
            logger.info("性能测试未启用，跳过初始化")
            return

        # 每个用户开始时也清空一次数据（额外保障）
        try:
            from common.base_random_mixin import BaseRandomMixin
            BaseRandomMixin.clear_generated_data()
            time.sleep(0.1)
        except:
            pass

        # 从环境变量获取 API 配置
        api_config_str = os.getenv('LOCUST_API_CONFIG')
        if api_config_str:
            try:
                self.api_config = json.loads(api_config_str)
            except json.JSONDecodeError:
                self.api_config = []
        else:
            self.api_config = []

        # 初始化请求计数器
        self.request_count = 0
        # 每个接口最多执行 10 次，避免无限循环
        self.max_requests = max(len(self.api_config) * 10, 100)

    def on_stop(self):
        """任务结束时的清理操作"""
        logger.info(f"任务结束，总请求次数：{self.request_count}")
        # 清空生成的数据
        try:
            from common.base_random_mixin import BaseRandomMixin
            BaseRandomMixin.clear_generated_data()
        except Exception as e:
            logger.error(f"清理数据失败：{e}")

    @task(1)
    def execute_requests(self):
        """执行配置的 API 请求"""
        # 检查性能测试是否启用
        if not is_performance_enabled():
            logger.info("性能测试未启用，跳过请求执行")
            return

        # 检查是否超过最大请求次数，如果超过则中断任务
        if self.request_count >= self.max_requests:
            logger.info(f"已达到最大请求次数 {self.max_requests}，结束任务")
            self.interrupt(reschedule=False)
            return

        for api in self.api_config:
            # 处理 URL（修复问号问题）
            url = api.get('endpoint', '').rstrip('?')
            data = api.get('data')
            if '.' in str(data):
                data = dynamic_method_call(data)
            logger.info(f'{url}处理前-data: {data}, type:{type(data)}')

            # 添加额外的日志来检查 IMEI 是否唯一
            if isinstance(data, dict) and 'purchaseOrdersArticlesDTOList' in data:
                for item in data['purchaseOrdersArticlesDTOList']:
                    outer_imei = item.get('imei')
                    inner_imei = item.get('purchaseArticlesInfoDTO', {}).get('imei')
                    if outer_imei and inner_imei:
                        logger.info(
                            f"外层 IMEI: {outer_imei}, 内层 IMEI: {inner_imei}, 是否相同：{outer_imei == inner_imei}")

            # 特殊处理：如果 data 是空字符串或 None，转换为{}
            if data is None or (isinstance(data, str) and data.strip() == ''):
                data = {}

            # 修复：如果 data 是字符串，尝试转换为字典
            original_data_str = None
            if isinstance(data, str):
                original_data_str = data
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON 解析错误：{e}, 原始数据：{original_data_str}")
                    continue

            if api.get('method') == 'GET' and data:
                query_string = urlencode(data)
                url = f"{url}?{query_string}" if '?' not in url else f"{url}&{query_string}"

            # 关键修改：为每个请求生成新的唯一数据
            print('-----', self._is_url_in_request(url), isinstance(data, dict))
            if isinstance(data, dict):
                data = self._generate_unique_data(data, url)

            # 确定使用 json 参数还是 data 参数
            use_json = None
            use_data = None

            if api.get('method') in ['POST', 'PUT', 'PATCH']:
                # 对于 POST/PUT/PATCH 请求，使用 json 参数发送 JSON 数据，如果原始数据是字符串，我们使用原始字符串以确保引号正确
                if original_data_str and isinstance(data, dict):
                    use_data = json.dumps(data)
                else:
                    use_json = data
            else:
                # 对于 GET/DELETE 等请求，使用 data 参数（如果是 GET 则已处理为 URL 参数）
                use_data = data if api.get('method') != 'GET' else None

            logger.info(f'{url}方式{api.get("method")}处理后:{use_data}, json: {use_json}, type-json:{type(use_json)},'
                        f'请求头:{api.get("headers")}')

            # 执行 API 请求
            with self.client.request(
                    method=api.get('method', 'GET'),
                    url=url,
                    json=use_json,
                    data=use_data,
                    headers=api.get('headers', {"Content-Type": "application/json"}),
                    catch_response=True,
                    timeout=api.get('timeout', 60),
                    name=api.get('name', 'Unnamed Request')
            ) as response:
                # 打印响应信息
                try:
                    response_data = response.json() if response.content else {}
                    logger.info(f"返回：{response_data}")
                    if isinstance(response_data, dict) and response_data.get('code') != 200:
                        logger.info(f"接口地址{url}请求错误：code={response_data.get('code')}")
                except:
                    logger.info(f"响应文本：{response.text}")

                # 处理响应结果
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"请求失败，状态码：{response.status_code}")

            # 增加请求计数
            self.request_count += 1

    def _generate_unique_data(self, data, url=None):
        """
        为数据生成唯一标识，确保每次请求的数据都是唯一的
        """
        # 检查性能测试是否启用
        if not is_performance_enabled():
            return data

        # 深拷贝数据以避免修改原始数据
        new_data = copy.deepcopy(data)

        # 递归处理数据中的所有 IMEI 相关字段
        new_data = self._ensure_unique_imei_recursive(new_data)

        # 应用参数生成器
        new_data = self._get_param_generator(new_data, url)
        return new_data

    def _ensure_unique_imei_recursive(self, obj):
        """
        递归遍历对象，确保所有 IMEI 相关字段都是唯一的
        """
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                if self._is_imei_field(key):
                    # 生成新的唯一 IMEI
                    new_dict[key] = self._generate_unique_imei()
                elif isinstance(value, (dict, list)):
                    new_dict[key] = self._ensure_unique_imei_recursive(value)
                else:
                    new_dict[key] = value
            return new_dict
        elif isinstance(obj, list):
            return [self._ensure_unique_imei_recursive(item) for item in obj]
        else:
            return obj

    def _is_imei_field(self, key):
        """
        判断字段名是否与 IMEI 相关
        """
        key_lower = key.lower()
        return 'imei' in key_lower

    def _generate_unique_imei(self):
        """
        生成唯一的 IMEI 号
        """
        # 检查性能测试是否启用
        if not is_performance_enabled():
            return "default_imei"

        # 使用线程本地存储确保每个线程有独立的 IMEI 集合
        if not hasattr(self, '_thread_local'):
            self._thread_local = threading.local()

        if not hasattr(self._thread_local, '_used_imies'):
            self._thread_local._used_imies = set()

        # 生成基于时间戳和 UUID 的 IMEI
        timestamp_part = str(int(time.time() * 1000000))[-10:]
        unique_part = str(uuid.uuid4()).replace('-', '')[:8].upper()
        thread_id = str(threading.current_thread().ident)[-4:]

        # 组合生成唯一 IMEI
        base_imei = f"I{timestamp_part}{unique_part}{thread_id}"

        # 确保唯一性
        counter = 0
        new_imei = base_imei
        while new_imei in self._thread_local._used_imies:
            counter += 1
            new_imei = f"{base_imei}{counter:04d}"

        self._thread_local._used_imies.add(new_imei)
        return new_imei

    def _get_param_generator(self, data, url):
        """
        根据 URL 获取对应的参数生成器方法
        :param url: 接口 URL
        :return: 参数生成方法或 None
        """
        # 检查性能测试是否启用
        if not is_performance_enabled():
            return data

        # 使用全局注册的性能测试配置
        if url in PERFORMANCE_TEST_REGISTRY:
            mapping = PERFORMANCE_TEST_REGISTRY[url]
            print('--执行的参数生成方法内容:', mapping)
            try:
                # 动态导入模块
                module = __import__(mapping['module'], fromlist=[mapping['class']])
                # 获取类
                cls = getattr(module, mapping['class'])
                # 创建实例
                instance = cls()

                # 获取方法并执行
                method_obj = getattr(instance, mapping['method'])

                # 如果方法需要参数，这里需要特殊处理
                # 由于我们是在 Locust 环境中，需要创建一个临时实例来调用方法
                try:
                    if callable(method_obj):
                        # 尝试调用方法 - 传入 nocheck=True 避免触发 HTTP 请求
                        # 关键修改：确保方法不会触发嵌套的性能测试
                        sig = inspect.signature(method_obj)
                        params = sig.parameters

                        # 如果方法接受 nocheck 参数，则传入 True 以避免执行 HTTP 请求
                        if 'nocheck' in params:
                            result = method_obj(nocheck=True)
                        else:
                            # 如果不接受 nocheck 参数，直接调用（期望方法内部不会产生副作用）
                            result = method_obj()

                        print('--resu:', result)
                        return result
                except Exception as e:
                    logger.error(f"执行参数生成方法时出错：{e}")
                    return data

            except (ImportError, AttributeError) as e:
                logger.error(f"无法导入参数生成器：{e}")
                return data
        return data

    def _is_url_in_request(self, target_url):
        """
        检查目标 URL 是否存在于 URL['request'] 的嵌套字典结构中
        :param target_url: 要检查的目标 URL
        :return: 如果存在返回 True，否则返回 False
        """
        if not target_url or not isinstance(URL.get('request'), dict):
            return False

        # 遍历 URL['request'] 的所有层级，查找目标 URL
        def search_nested_dict(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    if search_nested_dict(value):
                        return True
                elif isinstance(value, str) and value == target_url:
                    return True
            return False

        return search_nested_dict(URL['request'])


class LocustPerformanceTest(HttpUser):
    """
    Locust 性能测试主类
    """
    # 设置用户等待时间 - 修改为合理的值，避免请求过于频繁
    wait_time = between(1, 3)

    # 设置主机地址
    host = ENV

    # 注册任务集
    tasks = [LocustTaskSet]

    @staticmethod
    def clean_performance_directory():
        """
        清理 performance 目录下的所有文件
        """
        # 检查性能测试是否启用
        if not is_performance_enabled():
            return

        try:
            # 获取 performance 目录路径
            report_path = os.path.dirname(os.path.abspath(__file__)).replace('common', 'performance')
            report_path = os.path.abspath(report_path)

            # 确保目录存在
            if not os.path.exists(report_path):
                os.makedirs(report_path)
                print(f"创建 performance 目录：{report_path}")
                return

            # 删除目录下的所有文件和子目录
            for filename in os.listdir(report_path):
                file_path = os.path.join(report_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        print(f"已删除文件：{file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"已删除目录：{file_path}")
                except Exception as e:
                    print(f"删除 {file_path} 失败：{e}")

            print(f"已清理 performance 目录：{report_path}")
        except Exception as e:
            print(f"清理 performance 目录时出错：{e}")

    @staticmethod
    def run_performance_test(
            api_configs,
            users=0,
            spawn_rate=0,
            run_time="60s",
            host=None,
            headless=True
    ):
        """
        执行性能测试
        """
        # 检查性能测试是否启用
        if not is_performance_enabled():
            logger.info("性能测试未启用，跳过性能测试执行")
            return None

        # 在每次测试前清空所有生成的数据记录
        try:
            from common.base_random_mixin import BaseRandomMixin
            BaseRandomMixin.clear_generated_data()
            time.sleep(0.2)
        except Exception as e:
            print(f"清空生成数据时出错：{e}")

        """
        执行性能测试

        Args:
            api_configs (list): API 配置列表，每个配置应包含:
                - endpoint (str): 接口地址
                - method (str): 请求方法 (GET/POST/PUT/DELETE)
                - data (dict, optional): 请求数据
                - headers (dict, optional): 请求头
                - timeout (int, optional): 超时时间，默认 60 秒
            users (int): 并发用户数
            spawn_rate (int): 每秒启动用户数
            run_time (str): 运行时间，例如 "60s", "5m", "1h"
            host (str): 目标主机地址
            headless (bool): 是否无头模式运行

        Returns:
            subprocess.CompletedProcess: 执行结果
        """
        # 在每次运行前清理 performance 目录
        # LocustPerformanceTest.clean_performance_directory()

        # 构建 API 配置 JSON
        api_config_json = json.dumps(api_configs)
        # 构建命令
        cmd = [sys.executable, "-m", "locust"]
        cmd.extend(["-f", os.path.abspath(__file__)])
        cmd.extend(["--users", str(users)])
        cmd.extend(["--spawn-rate", str(spawn_rate)])

        if host:
            cmd.extend(["--host", host])
        elif ENV:
            cmd.extend(["--host", ENV])

        cmd.extend(["--run-time", run_time])
        cmd.extend(["--loglevel", "INFO"])

        if headless:
            cmd.append("--headless")

        # 获取当前项目的根目录
        report_path = os.path.dirname(os.path.abspath(__file__)).replace('common', 'performance')
        new_report_path_csv = os.path.join(report_path,
                                           f"{api_configs[0]['report_name'] if 'report_name' in api_configs[0] else 'performance_test'}")
        cmd.extend(["--csv", new_report_path_csv])
        print(f"执行命令：{' '.join(cmd)}")

        # 在生成新报告前，先删除旧的报告文件
        stats_file = f"{new_report_path_csv}_stats.csv"
        failures_file = f"{new_report_path_csv}_failures.csv"
        exceptions_file = f"{new_report_path_csv}_exceptions.csv"

        for file in [stats_file, failures_file, exceptions_file]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"已删除旧报告文件：{file}")
                except Exception as e:
                    print(f"删除旧报告文件 {file} 失败：{e}")

        try:
            # 设置环境变量传递 API 配置
            env = os.environ.copy()
            env['LOCUST_API_CONFIG'] = api_config_json

            # 执行命令，使用二进制模式避免编码问题
            result = subprocess.run(
                cmd,
                capture_output=True,
                env=env,
                check=True
            )

            # 手动解码输出内容，使用多种编码方式尝试
            def safe_decode(data):
                if not data:
                    return ""
                try:
                    return data.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        return data.decode('gbk')
                    except UnicodeDecodeError:
                        return data.decode('utf-8', errors='ignore')

            stdout_text = safe_decode(result.stdout)
            stderr_text = safe_decode(result.stderr)

            print("STDOUT:", stdout_text)
            if stderr_text:
                print("STDERR:", stderr_text)

            return result
        except subprocess.CalledProcessError as e:
            stderr_text = e.stderr.decode('utf-8', errors='ignore') if e.stderr else ""
            print(f"执行性能测试时出错：{e}")
            print(f"错误输出：{stderr_text}")
            return None
        except Exception as e:
            print(f"执行性能测试时发生异常：{e}")
            return None

    @staticmethod
    def merge_csv_reports():
        """
        合并所有 CSV 报告到一个文件中
        """
        # 检查性能测试是否启用
        if not is_performance_enabled():
            return

        # 获取报告目录
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'performance')
        report_path = os.path.abspath(report_path)

        # 查找所有 stats.csv 文件
        csv_files = glob.glob(os.path.join(report_path, "*_stats.csv"))

        if not csv_files:
            print("未找到任何 CSV 报告文件")
            return

        # 读取所有 CSV 文件并合并
        merged_data = []
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                # 添加来源文件列
                df['source_file'] = os.path.basename(file)
                merged_data.append(df)
            except Exception as e:
                print(f"读取文件 {file} 时出错：{e}")

        if merged_data:
            # 合并所有数据
            merged_df = pd.concat(merged_data, ignore_index=True)

            # 数值列保留两位小数
            numeric_columns = merged_df.select_dtypes(include=['float64']).columns
            merged_df[numeric_columns] = merged_df[numeric_columns].round(2)

            # 保存合并后的文件
            output_file = os.path.join(report_path, "merged_stats_report.csv")
            merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"合并报告已保存到：{output_file}")

            # 同时生成一个 Excel 文件以便更好地查看
            output_excel = os.path.join(report_path, "merged_stats_report.xlsx")
            merged_df.to_excel(output_excel, index=False)
            print(f"合并报告 Excel 版本已保存到：{output_excel}")
        else:
            print("没有数据可以合并")
