import subprocess
import platform
import logging
import unittest
from common.base_api import BaseApi
from config.settings import DATA_PATHS
from common.base_dynamic_attr_mixin import DynamicAttrMixin


class MiniBaseCase(DynamicAttrMixin, unittest.TestCase, BaseApi):
    """测试用例基类，提供通用的前置条件方法"""

    DATA_PATHS = DATA_PATHS

    @classmethod
    def tearDownClass(cls):
        """基类清理方法"""
        # 判断如果不是API模式，则关闭微信开发者工具
        api_only_mode = DATA_PATHS.get('api_only_mode', False)
        if not api_only_mode:
            # 只在非API模式下关闭微信开发者工具
            cls._close_wechat_tools()
        super().tearDownClass()  # 现在可以安全调用父类方法

    @classmethod
    def _close_wechat_tools(cls):
        """关闭微信相关工具"""
        try:
            system = platform.system()
            if system == "Windows":
                # 关闭Windows下的微信开发者工具
                subprocess.run(["taskkill", "/f", "/im", "wechatdevtools.exe"],
                               capture_output=True, timeout=10)
                # 同时关闭可能的相关进程
                subprocess.run(["taskkill", "/f", "/im", "nw.exe"],
                               capture_output=True, timeout=10)

        except subprocess.TimeoutExpired:
            logging.warning("关闭微信开发者工具超时")
        except Exception as e:
            logging.warning(f"关闭微信开发者工具时出错: {e}")

    def common_operations_mini(self):

        # 获取实例化的页面对象
        access_page = self.get_instantiation()

        return access_page

    def get_instantiation(self):
        """子类必须重写该方法返回对应的页面实例"""
        raise NotImplementedError("请在子类中实现 get_instantiation 方法")
