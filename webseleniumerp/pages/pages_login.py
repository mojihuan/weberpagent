# coding: utf-8
from common.base_page import BasePage
from common.base_params import InitializeParams
from config.user_info import INFO


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []


class YIfRytREfFx(CommonPages):
    """登录"""

    def login_main(self):
        self.get_load()
        self.wait_time()
        self.click(key='y5obCIyqLPDEN', desc='密码登录', auto=False)
        self.input(key='D6BJxtdkN4J4n', text=INFO['main_account'], desc='请输入账号', auto=False)
        self.input(key='sRaM9ysLkMAwq', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='tybmCyx87usJG', desc='登 录', auto=False)
        return self

    def login_special(self):
        self.get_load()
        self.wait_time()
        self.click(key='y5obCIyqLPDEN', desc='密码登录', auto=False)
        self.input(key='D6BJxtdkN4J4n', text=INFO['special_account'], desc='请输入账号', auto=False)
        self.input(key='sRaM9ysLkMAwq', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='tybmCyx87usJG', desc='登 录', auto=False)
        return self

    def login_platform(self):
        self.get_load()
        self.wait_time()
        self.click(key='y5obCIyqLPDEN', desc='密码登录', auto=False)
        self.input(key='D6BJxtdkN4J4n', text=INFO['platform_account'], desc='请输入账号', auto=False)
        self.input(key='sRaM9ysLkMAwq', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='tybmCyx87usJG', desc='登 录', auto=False)
        return self

    def login_idle(self):
        self.get_load()
        self.wait_time()
        self.click(key='y5obCIyqLPDEN', desc='密码登录', auto=False)
        self.input(key='D6BJxtdkN4J4n', text=INFO['idle_account'], desc='请输入账号', auto=False)
        self.input(key='sRaM9ysLkMAwq', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='tybmCyx87usJG', desc='登 录', auto=False)
        return self

    def login_vice(self):
        self.get_load()
        self.wait_time()
        self.click(key='y5obCIyqLPDEN', desc='密码登录', auto=False)
        self.input(key='D6BJxtdkN4J4n', text=INFO['vice_account'], desc='请输入账号', auto=False)
        self.input(key='sRaM9ysLkMAwq', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='tybmCyx87usJG', desc='登 录', auto=False)
        return self

    def login_super(self):
        self.get_load()
        self.wait_time()
        self.click(key='y5obCIyqLPDEN', desc='密码登录', auto=False)
        self.input(key='D6BJxtdkN4J4n', text=INFO['super_admin_account'], desc='请输入账号', auto=False)
        self.input(key='sRaM9ysLkMAwq', text=INFO['password'], desc='请输入密码', auto=False)
        self.click(key='tybmCyx87usJG', desc='登 录', auto=False)
        return self
