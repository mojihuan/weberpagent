# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestPurseCenter(BaseCase, unittest.TestCase):
    """钱包管理|钱包中心"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purse_r.PurseCenterRequest()
        else:
            return purse_p.PurseCenterPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0recharge_the_product_wallet(self):
        """[充值]-对公转账支付"""
        case = self.common_operations(login='main')
        case.recharge_the_product_wallet()
        res = [lambda: self.pc.purse_wallet_order_list_assert(data='a', businessTypeStr='钱包充值', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_alipay_recharge(self):
        """[充值]-支付宝支付"""
        case = self.common_operations()
        case.alipay_recharge()
        res = [lambda: self.pc.purse_wallet_order_list_assert(businessTypeStr='钱包充值', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wechat_payment(self):
        """[充值]-微信支付"""
        case = self.common_operations()
        case.wechat_payment()
        res = [lambda: self.pc.purse_wallet_order_list_assert(businessTypeStr='钱包充值', createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
