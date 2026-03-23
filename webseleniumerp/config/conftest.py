# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from config.settings import DATA_PATHS


class TestConfig:
    driver = None  # 添加类变量

    @classmethod
    def should_run_headless(cls):
        """
        根据全局配置决定是否以无头模式运行浏览器
        当 auto_type='api' 时启用无头模式
        :return: bool 是否启用无头模式
        """
        auto_type = DATA_PATHS.get('auto_type', 'ui')
        return auto_type == 'api'

    @classmethod
    def setup_webdriver(cls):
        options = Options()
        # 根据配置决定是否启用无头模式
        if cls.should_run_headless():
            options.add_argument('--headless=new')  # 启用新的无头模式
        options.add_argument('--disable-gpu')  # 禁用 GPU 加速（某些系统需要）
        options.add_argument('--no-sandbox')  # 在 CI 环境中推荐设置
        options.add_argument('--disable-dev-shm-usage')  # 防止崩溃
        options.add_argument("--use-fake-device-for-media-stream")  # 模拟虚拟设备用于媒体流
        options.add_argument("--use-fake-ui-for-media-stream")  # 使用虚拟的用户界面来模拟媒体流权限提示
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument("--disable-application-cache")
        prefs = {
            "profile.default_content_setting_values.media_stream_mic": 1,  # 麦克风
            "profile.default_content_setting_values.media_stream_camera": 1  # 摄像头
        }
        options.add_argument("--use-fake-device-for-media-stream")  # 虚拟摄像头
        options.add_argument("--use-fake-ui-for-media-stream")  # 模拟 UI
        options.add_experimental_option('prefs', prefs)
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.add_argument("--disable-application-cache")
        # 启用网络日志
        options.set_capability('goog:loggingPrefs', {
            'performance': 'ALL',
            'browser': 'ALL'
        })
        # 手动指定 ChromeDriver 路径
        service = ChromeService(executable_path=DATA_PATHS['chrome_driver'])
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.execute_cdp_cmd('Network.enable', {})
        cls.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        cls.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
        cls.driver.delete_all_cookies()

        # 手动指定 ChromeDriver 路径
        cls.driver.implicitly_wait(1)  # 隐式等待
        cls.driver.maximize_window()  # 最大化窗口

    @classmethod
    def get_driver(cls):
        return cls.driver

    @classmethod
    def teardown_webdriver(cls):
        if cls.driver:
            cls.driver.quit()
