# coding: utf-8
from common.base_page import BasePage
from config.user_info import INFO


class LoginPages(BasePage):
    """登录"""

    def __init__(self, driver):
        super().__init__(driver)

    def login_main(self):
        self.get_load()
        self.wait_time()
        self.click(key='login_main_1', desc='密码登录', auto=False)
        self.input(key='login_main_2', text=INFO['main_account'], desc='请输入账号', auto=False)
        self.input(key='login_main_3', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='login_main_4', desc='登 录', auto=False)
        return self

    def login_special(self):
        self.get_load()
        self.wait_time()
        self.click(key='login_main_1', desc='密码登录', auto=False)
        self.input(key='login_main_2', text=INFO['special_account'], desc='请输入账号', auto=False)
        self.input(key='login_main_3', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='login_main_4', desc='登 录', auto=False)
        return self

    def login_platform(self):
        self.get_load()
        self.wait_time()
        self.click(key='login_main_1', desc='密码登录', auto=False)
        self.input(key='login_main_2', text=INFO['platform_account'], desc='请输入账号', auto=False)
        self.input(key='login_main_3', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='login_main_4', desc='登 录', auto=False)
        return self

    def login_idle(self):
        self.get_load()
        self.wait_time()
        self.click(key='login_main_1', desc='密码登录', auto=False)
        self.input(key='login_main_2', text=INFO['idle_account'], desc='请输入账号', auto=False)
        self.input(key='login_main_3', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='login_main_4', desc='登 录', auto=False)
        return self

    def login_vice(self):
        self.get_load()
        self.wait_time()
        self.click(key='login_main_1', desc='密码登录', auto=False)
        self.input(key='login_main_2', text=INFO['vice_account'], desc='请输入账号', auto=False)
        self.input(key='login_main_3', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='login_main_4', desc='登 录', auto=False)
        return self

    def login_super(self):
        self.get_load()
        self.wait_time()
        self.click(key='login_main_1', desc='密码登录', auto=False)
        self.input(key='login_main_2', text=INFO['super_admin_account'], desc='请输入账号', auto=False)
        self.input(key='login_main_3', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='login_main_4', desc='登 录', auto=False)
        return self
