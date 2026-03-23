import minium
import time
import os
import sys
import pyperclip

from config.settings import DATA_PATHS

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from common.base_random_mixin import BaseRandomMixin


class BaseMinium(minium.MiniTest, BaseRandomMixin):
    """基于minium框架的基础测试类，提供通用的测试前置和后置操作"""

    # 类变量，标记是否已导航
    _has_navigated = False

    def setUp(self):
        # 测试前置操作：仅在首次启动时导航到主页
        self.logger.info(f"开始执行测试用例: {self._testMethodName}")

        # 使用类变量标记是否已导航
        if not getattr(BaseMinium, '_has_navigated', False):
            try:
                # 首次启动导航到主页
                self.app.navigate_to("/pages/mainPage/index?")
                # 增加智能等待
                self.wait_for_page_ready()
                # 标记已导航
                BaseMinium._has_navigated = True
            except Exception as e:
                self.logger.warning(f"导航失败: {e}，重新启动应用并导航到主页")
                # 如果导航失败则重新启动应用并导航到主页
                self.app.relaunch("/pages/mainPage/index?")
                # 重启后需要更长的等待时间
                self.wait_for_page_ready()
                # 标记已导航
                BaseMinium._has_navigated = True

    def tearDown(self):
        """测试后置操作：清理测试环境"""
        self.logger.info(f"测试用例执行完毕: {self._testMethodName}")
        # 可选：在每个测试结束后添加一些清理操作
        try:
            # 清理可能存在的弹窗或临时状态
            # 这里可以根据实际需要添加清理代码
            pass
        except Exception as e:
            self.logger.warning(f"测试后置清理操作出现异常: {e}")

    def _log_element_error(self, selector=None, xpath=None, inner_text=None, error_msg=""):
        """
        记录元素定位错误的详细信息
        Args:
            selector (str, optional): 元素选择器
            xpath (str, optional): 元素xpath表达式
            inner_text (str, optional): 元素文本内容
            error_msg (str): 错误信息
        """
        error_details = []
        if selector:
            error_details.append(f"selector='{selector}'")
        if xpath:
            error_details.append(f"xpath='{xpath}'")
        if inner_text:
            error_details.append(f"inner_text='{inner_text}'")

        error_info = ", ".join(error_details)
        self.logger.error(f"元素定位失败 [{error_info}]: {error_msg}")

    def _try_locate_element(self, selector=None, xpath=None, inner_text=None):
        """
        尝试定位元素的核心逻辑
        Args:
            selector (str, optional): 元素选择器
            xpath (str, optional): 元素xpath表达式
            inner_text (str, optional): 元素文本内容

        Returns:
            tuple: (element_is_exists, element) 元素是否存在和元素对象
        """
        element_is_exists = False
        element = None

        try:
            # 尝试使用 selector 定位元素
            if selector:
                element_is_exists = self.page.element_is_exists(selector)
                if element_is_exists:
                    element = self.page.get_element(selector)

            # 如果 selector 定位失败，尝试使用 xpath 定位元素
            if not element_is_exists and xpath:
                element_is_exists = self.page.element_is_exists(xpath=xpath)
                if element_is_exists:
                    element = self.page.get_element_by_xpath(xpath)

            # 如果 xpath 定位失败，尝试使用 inner_text 定位元素
            if not element_is_exists and inner_text:
                # 注意：使用 inner_text 定位元素时无法预先检查元素是否存在
                element = self.page.get_element_by_xpath("//*", inner_text=inner_text)

        except Exception as e:
            self._log_element_error(selector, xpath, inner_text, str(e))
            # 重新抛出异常供上层处理
            raise

        return element_is_exists, element

    def _find_element(self, selector=None, xpath=None, inner_text=None, timeout=10, force_wait=None):
        """
        通用元素查找方法，支持多种定位方式
        Args:
            selector (str, optional): 元素选择器
            xpath (str, optional): 元素xpath表达式
            inner_text (str, optional): 元素文本内容
            timeout (int): 等待元素出现的超时时间（秒），默认为10秒
            force_wait (int): 强制等待时间（秒）
        Returns:
            Element: 页面元素对象

        Raises:
            TimeoutError: 元素定位超时时抛出
            ElementNotFoundError: 元素未找到时抛出
        """
        # 每次查找元素前强制等待指定时间
        forced_time = DATA_PATHS.get('forced_time', force_wait)  # 如果配置中没有forced_time，则使用force_wait
        # 增强容错处理：当 forced_time 和 force_wait 都为 None 时，默认设为 0
        actual_wait = float(forced_time) if forced_time is not None and forced_time != '' else (force_wait or 0)

        if actual_wait > 0:
            time.sleep(actual_wait)

        # 如果设置了超时时间，则等待元素出现
        if timeout > 0:
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # 首先检查页面是否加载完成
                    if hasattr(self.page, 'is_ready') and not self.page.is_ready():
                        time.sleep(0.5)
                        continue

                    element_is_exists, element = self._try_locate_element(selector, xpath, inner_text)
                    if element_is_exists or element:  # element存在表示通过inner_text找到了元素
                        break
                except Exception as e:
                    # 记录异常但继续等待
                    time.sleep(0.5)
            else:
                # 超时仍未找到元素
                error_msg = f"在{timeout}秒内未找到元素"
                self._log_element_error(selector, xpath, inner_text, error_msg)
                raise TimeoutError(error_msg)
        else:
            # 不等待，直接查找元素
            _, element = self._try_locate_element(selector, xpath, inner_text)

        if not element:
            error_msg = "未能找到元素"
            self._log_element_error(selector, xpath, inner_text, error_msg)
            raise ElementNotFoundError(error_msg)

        return element

    def input(self, selector=None, xpath=None, inner_text=None, text=None, desc=None):
        """
        安全地输入文本到指定元素，支持多种定位方式
        Args:
            selector (str, optional): 元素选择器
            xpath (str, optional): 元素xpath表达式
            inner_text (str, optional): 元素文本内容
            text (str): 需要输入的文本内容
            desc (str, optional): 操作描述信息
        """
        element = self._find_element(selector, xpath, inner_text)
        element.input(text)

    def elem(self, selector=None, xpath=None, inner_text=None, desc=None, tap=True, force=False):
        """
        安全地获取页面元素，支持多种定位方式，默认执行点击操作
        Args:
            selector (str, optional): 元素选择器
            xpath (str, optional): 元素xpath表达式
            inner_text (str, optional): 元素文本内容
            desc (str, optional): 元素描述信息
            tap (bool): 是否执行点击操作，默认为True
            force (bool): 是否强制点击，默认为False
        Returns:
            Element: 页面元素对象
        """
        element = self._find_element(selector, xpath, inner_text)
        # 默认执行点击操作，除非显式设置tap=False
        if tap:
            if force:
                element.tap(force=True)
            else:
                element.tap()
        return element

    def _load_locators_from_module(self, module_name, locator_names):
        """
        从指定模块加载定位器
        Args:
            module_name (str): 模块名
            locator_names (list): 定位器名称列表
        Returns:
            dict: 包含定位器的字典
        """
        # 动态导入模块
        module_parts = module_name.split('.')
        module = __import__(module_parts[0])
        for part in module_parts[1:]:
            module = getattr(module, part)

        # 创建定位器字典
        locators = {name: getattr(module, name) for name in locator_names}
        self.logger.info(f"Total locators loaded from {module_name}: {len(locators)}")
        return locators

    def wait(self, seconds=1):
        """
        等待指定时间
        Args:
            seconds (int): 等待时间（秒），默认为1秒
        """
        self.page.wait_for(seconds)

    def wait_for_page_ready(self, timeout=10):
        """
        等待页面加载完成，增加更智能的检查机制
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 多重检查确保页面真正就绪
                if (hasattr(self.page, 'is_ready') and self.page.is_ready() and
                        self.page.element_is_exists("page")):  # 检查页面根元素是否存在
                    # 额外的小等待确保渲染完成
                    time.sleep(0.1)
                    return True
            except:
                pass
            time.sleep(0.2)
        return False

    def back(self, times=1):
        """
        多次返回操作
        Args:
            times (int): 返回次数，默认为1次
        Returns:
            self: 支持链式调用
        """
        for _ in range(times):
            self.app.navigate_back()
        return self

    def mg_locator(self, locator_name):
        """
        获取元素定位器
        :param locator_name: 定位器名称
        :return: 定位器对象
        """
        if not hasattr(self, '_locators'):
            from common import mini_element_positioning
            self._locators = mini_element_positioning
        return getattr(self._locators, locator_name)

    def copy(self, value):
        """
        将指定值复制到剪贴板
        :param value: 要复制到剪贴板的值
        :return: 返回自身实例以支持链式调用
        """
        pyperclip.copy(str(value))
        return self


class ElementNotFoundError(Exception):
    """元素未找到异常"""
    pass
