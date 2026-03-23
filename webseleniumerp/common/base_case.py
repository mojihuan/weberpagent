# coding: utf-8
from datetime import date, timedelta
from config.settings import DATA_PATHS
from config.conftest import TestConfig
from common.decorators import retry_with
from common.base_prerequisites import PreFront
from common.base_url import URL
from common.base_dynamic_attr_mixin import DynamicAttrMixin


class BaseCase(TestConfig, DynamicAttrMixin):
    """
    BaseCase 是所有测试用例的基础类，提供通用的 setUp/tearDown 方法、日期获取、操作执行、断言初始化等功能。
    """
    retry_with = staticmethod(retry_with)  # 将 retry_with 添加为静态方法
    DATA_PATHS = DATA_PATHS

    @classmethod
    def setUpClass(cls):
        """
        在所有测试方法执行前调用，用于初始化 WebDriver。
        :return: None
        """
        super().setup_webdriver()

    @classmethod
    def tearDownClass(cls):
        """
        在所有测试方法执行后调用，用于关闭 WebDriver。
        :return: None
        """
        super().teardown_webdriver()

    def get_today_str(self, days=0, use_dash=False):
        """
        获取当前日期并格式化为字符串（YYYYMMDD）。
        :param days: 天数偏移量，默认为0（当天），正数表示未来日期，负数表示过去日期
        :param use_dash: 是否使用短横线分隔符，默认为False（不使用）
        :return: 格式化后的日期字符串
        """
        target_date = date.today() + timedelta(days=days)
        if use_dash:
            return target_date.strftime("%Y-%m-%d")
        else:
            return target_date.strftime("%Y%m%d")

    def clear_browser_cache(self, url=None):
        """清除浏览器缓存并打开指定页面"""
        # 只根据auto_type判断是否跳过浏览器缓存清除
        auto_type = DATA_PATHS.get('auto_type', 'ui')
        if auto_type == 'api':
            print("💡 当前为API模式，跳过浏览器缓存清除")
            return
        if url is None:
            url = URL.get('web', {}).get('login', 'about:blank')
        try:
            # 只在必要时清除特定缓存
            self.driver.delete_all_cookies()
            # 可选：只在特定条件下清除Storage
            # 例如，检查当前URL是否为登录页，避免在data: URL上操作
            current_url = self.driver.current_url
            if not current_url.startswith('data:'):
                try:
                    self.driver.execute_script("window.localStorage.clear();")
                    self.driver.execute_script("window.sessionStorage.clear();")
                except Exception as storage_error:
                    if "Storage is disabled" not in str(storage_error):
                        raise

            self.driver.get(url)
            print(f"✅ 浏览器缓存已清除，并跳转到页面: {url}")
        except Exception as e:
            print(f"⚠️ 清除缓存或跳转失败: {e}")

    def common_operations(self, **kwargs):
        """
        通用的操作执行逻辑
        Args:
            **kwargs: 传递给操作函数的关键字参数，支持以下特殊参数：
                - login (str, optional): 登录账号标识，如果有则先执行登录操作
        Returns:  object: 操作完成后返回的页面对象
        Raises: NotImplementedError: 当子类没有实现 get_instantiation 方法时抛出
        Example:
            # 执行登录操作
            self.common_operations(login='main')
        """
        login_param = kwargs.pop('login', None)

        # 检查是否为API模式
        auto_type = DATA_PATHS.get('auto_type', 'ui')

        # 只有在UI模式下才执行登录操作
        if auto_type != 'api' and login_param:
            # 初始化主登录页面
            from common.import_page import ImportPage
            main = PreFront()
            setattr(main, 'page', ImportPage(self.driver))

            # 执行登录操作
            main.login_operations()
            main.page.common_login(login_param)

        # 获取实例化的页面对象
        access_page = self.get_instantiation()

        return access_page

    def common_operations_mini(self):

        # 获取实例化的页面对象
        access_page = self.get_instantiation()

        return access_page

    def get_instantiation(self):
        """子类必须重写该方法返回对应的页面实例"""
        raise NotImplementedError("请在子类中实现 get_instantiation 方法")
