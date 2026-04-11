import time
import unittest
from functools import wraps
from common.base_prerequisites import PreFront
from common.base_assertions import PcAssert
from common.import_api import ImportApi
from common.import_request import ImportRequest
from config.settings import DATA_PATHS


class DynamicAttrMixin:
    """
    动态属性混入类，提供动态获取断言实例和前置条件实例的功能
    """
    DATA_PATHS = DATA_PATHS

    def __getattr__(self, item):
        """
        动态获取断言实例、前置条件实例和后置条件实例。如果属性不存在，则根据映射创建对应的实例。
        :param item: 属性名
        :return: 对应的断言模块实例、前置条件实例或后置条件实例
        """
        assert_mapping = {
            'pc': PcAssert,
        }

        # 检查是否是前置条件模块（以 'pre' 开头）
        if item.startswith('pre'):
            # 定义前置条件映射
            front_classes = {
                'pre': PreFront,
            }
            if item in front_classes:
                # 创建并设置前置条件实例
                setattr(self, item, front_classes[item]())
                return getattr(self, item)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

        # 检查是否是后置条件模块（以 'post_' 开头）
        if item.startswith('post_'):
            # 定义后置条件映射
            post_classes = {
                'post_request': ImportRequest,
                'post_api': ImportApi,
            }
            if item in post_classes:
                # 创建并设置后置条件实例
                setattr(self, item, post_classes[item]())
                return getattr(self, item)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

        # 处理断言映射
        if item in assert_mapping:
            cls = assert_mapping[item]
            instance = cls()
            setattr(self, item, instance)
            return instance

        # 如果都不是，抛出 AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    @staticmethod
    def auto(auto_name):
        """
        根据配置决定是否跳过UI自动化用例
        Args: name (str): 测试用例类型标识，用于区分API用例和UI用例
        Returns: function: 装饰器函数
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func._is_api_test = True
                api_only_mode = DATA_PATHS.get('api_only_mode', False)
                # 只有在api_only_mode为True时才执行跳过逻辑
                if api_only_mode:
                    if auto_name == 'ui':
                        raise unittest.SkipTest("忽略自动化用例")
                    return func(*args, **kwargs)
                elif not api_only_mode:
                    if auto_name == 'api':
                        raise unittest.SkipTest("忽略自动化用例")
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def author(name):
        """用于作者命名"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @property
    def auto_type(self):
        """获取自动化测试类型"""
        return self.DATA_PATHS.get('auto_type', 'ui')

    def assert_all(self, *res):
        """
        执行多个断言并收集所有失败的断言信息
        Args:
            *res: 可变参数，传入多个lambda函数或可调用对象，每个代表一个断言操作
        异常处理:
            - 只捕获AssertionError类型的异常，其他异常会正常抛出
            - 每个失败的断言都会记录其序号和具体的错误信息
            - 所有错误信息会按行连接成一个字符串后抛出
        """
        errors = []
        for i, assertion in enumerate(res):
            try:
                assertion()
            except AssertionError as e:
                errors.append(f"Assertion {i + 1} failed: {str(e)}")
        if errors:
            raise AssertionError("\n".join(errors))
