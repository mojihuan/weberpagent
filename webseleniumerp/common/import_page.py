# coding: utf-8
from pages.pages_login import LoginPages


class ImportPage:
    def __init__(self, driver):
        self.driver = driver
        self.login = LoginPages(self.driver)  # 登录

    def execute_operation(self, operation_mapping, operation):
        for op, method in operation_mapping.items():
            if op == operation:
                method()
                break

    # 登录管理
    def common_login(self, operation):
        operation_mapping = {
            'main': self.login.login_main,  # 登录
            'vice': self.login.login_vice,
            'special': self.login.login_special,
            'platform': self.login.login_platform,
            'idle': self.login.login_idle,
            'super': self.login.login_super,
            'load': self.login.get_load,  # 浏览器地址
        }
        self.execute_operation(operation_mapping, operation)
