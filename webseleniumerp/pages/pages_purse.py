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


class PurseCenterPages(CommonPages):
    """钱包管理|钱包中心"""


    def menu_manage(self):
        """菜单"""
        (self.scroll('purse_wallet_manage_menu', desc='钱包管理')
         .step(key='purse_wallet_manage_menu', desc='钱包管理')
         .step(key='purse_wallet_center_menu', desc='钱包中心')
         .wait())
        return self

    @reset_after_execution
    @doc(p_recharge_the_product_wallet)
    def recharge_the_product_wallet(self):
        """[流程]充值按钮-对公转账支付"""
        self.menu_manage()
        (self.step(key='top_up', desc='充值')
         .step(key='top_up_amount', value='124', action='input', desc='充值金额')
         .step(key='public_transfer', desc='对公转账支付')
         .step(key='wallet_top_up_and_upload_images', value=self.file_path('img'), action='upload', desc='上传文件')
         .scroll('immediate_payment', desc='立即支付')
         .step(key='barter_verify', desc='立即支付')
         .wait())
        return self

    @reset_after_execution
    @doc(p_alipay_recharge)
    def alipay_recharge(self):
        self.menu_manage()
        (self.step(key='top_up', desc='充值')
         .step(key='alipay_payment', desc='支付宝支付')
         .step(key='barter_verify', desc='立即支付')
         .step(key='i_have_paid', desc='我已支付')
         .wait())
        return self

    @reset_after_execution
    @doc(p_wechat_payment)
    def wechat_payment(self):
        self.menu_manage()
        (self.step(key='top_up', desc='充值')
         .step(key='wechat_payment', desc='微信支付')
         .step(key='barter_verify', desc='立即支付')
         .step(key='i_have_paid', desc='我已支付')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_approval)
    def platform_approval(self):
        (self.step(key='platform_manage_menu', desc='平台管理')
         .step(key='platform_order_manage_menu', desc='订单管理')
         .step(key='platform_order_review_menu', desc='订单审核')
         .step(key='order_examine', desc='审核')
         .step(key='audit_opinion', value=self.serial, action='input', desc='审核说明')
         .step(key='review_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_audit_rejection)
    def platform_audit_rejection(self):
        (self.step(key='platform_manage_menu', desc='平台管理')
         .step(key='platform_order_manage_menu', desc='订单管理')
         .step(key='platform_order_review_menu', desc='订单审核')
         .step(key='order_examine', desc='审核')
         .step(key='turn_down', desc='未通过')
         .step(key='audit_opinion', value=self.serial, action='input', desc='审核说明')
         .step(key='review_confirmation', desc='确认')
         .wait())
        return self

