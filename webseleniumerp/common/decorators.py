# coding: utf-8
import json
import os
import time
from selenium.webdriver.remote.webdriver import WebDriver
from functools import wraps
from common.base_url import URL
from common.mini_base_case import MiniBaseCase
from config.settings import DATA_PATHS

#
# def clear_browser_cache(driver: WebDriver, login_url: str = URL['web']['login']):
#     """ 清除浏览器缓存并跳转到登录页 """
#     try:
#         driver.delete_all_cookies()
#         driver.execute_script("window.localStorage.clear();")
#         driver.execute_script("window.sessionStorage.clear();")
#         driver.get(login_url)  # 跳转到登录页
#         print(f"✅ 浏览器缓存已清除，并跳转到登录页: {login_url}")
#     except Exception as e:
#         print(f"⚠️ 清除缓存或跳转失败: {e}")


def retry_with(clear_cache=False):
    """带重试机制的装饰器，用于自动化测试中失败自动重跑"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取配置
            auto_type = DATA_PATHS.get('auto_type', 'ui')
            api_only_mode = DATA_PATHS.get('api_only_mode', False)
            retry_enabled = DATA_PATHS.get('retry_enabled', True)  # 获取重试开关配置

            # 判断是否需要启用重试机制
            # 当 'auto_type': 'ui' 且 'api_only_mode': False 且 'retry_enabled': True 时启用重试
            # 其他情况不启用重试
            should_retry = (auto_type == 'ui' and not api_only_mode and retry_enabled)

            # 如果不需要重试，直接执行函数
            if not should_retry:
                return func(*args, **kwargs)

            # 需要重试的情况
            self_obj = args[0]
            max_retries = DATA_PATHS['tries']
            delay = DATA_PATHS['delay']

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"发生异常: {e}, 正在重试第 {attempt + 1} 次...")
                        if clear_cache and hasattr(self_obj, 'driver'):
                            try:
                                self_obj.driver.delete_all_cookies()
                            except:
                                pass  # 忽略清除缓存可能的异常
                        if hasattr(self_obj, 'driver'):
                            try:
                                self_obj.driver.refresh()
                            except:
                                pass  # 忽略刷新可能的异常
                        time.sleep(delay)
                    else:
                        raise
            return None

        return wrapper

    return decorator


def cached(key=None, filename='practical.json', cache_dir='cache_assert'):
    """用于缓存文件断言，从缓存文件中获取 ID 或指定键的值，或者返回整个数据字典

    Args:
        key: 缓存数据的键名，如果为 None 则返回整个数据字典
        filename: 缓存文件名，默认为 practical.json
        cache_dir: 缓存目录名称，默认为 cache_assert
    """
    from common.file_cache_manager import ParamCache

    # 使用统一的路径获取方法
    cache_file_path = ParamCache.get_cache_file_path(filename, cache_dir)

    try:
        with open(cache_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 如果没有指定 key，返回整个数据字典
        if key is None:
            return data

        # 否则返回指定 key 的值
        return data.get(key)
    except FileNotFoundError:
        print(f"⚠️ 缓存文件不存在：{cache_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"⚠️ 缓存文件格式错误：{cache_file_path}")
        return None
    except Exception as e:
        print(f"⚠️ 读取缓存文件出错：{e}")
        return None


def test_mode_handler(request_class, page_class):
    """小程序专用测试模式处理装饰器 - 统一管理版本"""

    def decorator(cls):
        auto = DATA_PATHS.get('auto_type', 'ui')
        is_api_mode = auto == 'api'

        # 动态设置基类
        if is_api_mode:
            cls.__bases__ = (MiniBaseCase, object)
        else:
            cls.__bases__ = (MiniBaseCase, page_class)

        # 保存原始setUp方法
        original_setUp = getattr(cls, 'setUp', None)

        def new_setUp(self):
            if is_api_mode:
                self.case = request_class()
            else:
                self.case = self
            if original_setUp:
                original_setUp(self)

        cls.setUp = new_setUp
        return cls

    return decorator



def capture_request_params(url_keywords=None, exclude_keywords=None):
    """
    装饰器：自动捕获并保存浏览器请求的 Payload 参数（只保存请求体）
    :param url_keywords: URL 包含的关键词列表（可选）
    :param exclude_keywords: 需要排除的 URL 关键词列表（可选）
    :return: 装饰器函数

    Example:
        @capture_request_params(
            url_keywords=['/api/'],
            exclude_keywords=['.css', '.js', '.png']
        )
        def test_0goods_received(self):
            # 测试代码...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 执行原始测试方法
            result = func(self, *args, **kwargs)

            # 执行完成后捕获 Payload 参数
            try:
                method_name = func.__name__
                if hasattr(self, 'capture_and_save_request_params'):
                    print(f"\n📥 开始捕获方法 {method_name} 的 Payload 参数...")
                    self.capture_and_save_request_params(
                        method_name=method_name,
                        url_keywords=url_keywords,
                        exclude_keywords=exclude_keywords
                    )
            except Exception as e:
                print(f"⚠️ 捕获 Payload 参数失败：{e}")

            return result

        return wrapper

    return decorator


if __name__ == '__main__':
    result = cached()
    print(json.dumps(result, indent=4, ensure_ascii=False))
