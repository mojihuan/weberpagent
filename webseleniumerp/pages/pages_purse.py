# coding: utf-8
import os

from common.base_params import InitializeParams
from config.settings import DATA_PATHS
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.import_desc import *


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'img': os.path.join(DATA_PATHS['excel'], 'img.jpg')
        }

    def menu(self, menu_type, key):
        """获取元素"""
        menu_mapping = {
            'main': self.elem_positioning['positioning'],
        }
        if menu_type in menu_mapping:
            return self.exc(lambda: menu_mapping[menu_type][key])
        else:
            raise ValueError(f"menu not found: {menu_type}")


class N7Vx2u7PEoa(CommonPages):
    """钱包管理|钱包中心"""


    def menu_manage(self):
        """菜单"""
        (self.scroll('purse_wallet_manage_menu', desc='钱包管理')
         .step(key='AurQ1nowhIFaI', desc='钱包管理')
         .step(key='BC4V5O9i5o0eX', desc='钱包中心')
         .wait())
        return self

    @reset_after_execution
    @doc(JxIyyg72fjeXbmTdyUr7)
    def JxIyyg72fjeXbmTdyUr7(self):
        """[流程]充值按钮-对公转账支付"""
        self.menu_manage()
        (self.step(key='y3onGibXwI8zR', desc='充值')
         .step(key='Udl0b6w0OkM20', value='124', action='input', desc='充值金额')
         .step(key='EtLCXBYKRsnxk', desc='对公转账支付')
         .step(key='iiym33CEVIx5m', value=self.file_path('img'), action='upload', desc='上传文件')
         .scroll('immediate_payment', desc='立即支付')
         .step(key='Bd73ruusMcTZk', desc='立即支付')
         .wait())
        return self

    @reset_after_execution
    @doc(ItN5k8HledkZ9VtTetAA)
    def ItN5k8HledkZ9VtTetAA(self):
        self.menu_manage()
        (self.step(key='VjKCcBR8ghY8u', desc='充值')
         .step(key='Tr8BcBrV7wZjn', desc='支付宝支付')
         .step(key='xOjyQCwe77M6o', desc='立即支付')
         .step(key='FxbFOshiuIljG', desc='我已支付')
         .wait())
        return self

    @reset_after_execution
    @doc(a05NJAdkRNkHL45jPTjg)
    def a05NJAdkRNkHL45jPTjg(self):
        self.menu_manage()
        (self.step(key='TvV2jHOFm63OK', desc='充值')
         .step(key='C28t5TsM5HJPV', desc='微信支付')
         .step(key='F8hWygJQ3vDtO', desc='立即支付')
         .step(key='v8DJ04BYwdqcA', desc='我已支付')
         .wait())
        return self

