# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestL886KE2N(BaseCase, unittest.TestCase):
    """钱包管理|钱包中心"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purse_r.PNng2wLCAK()
        else:
            return purse_p.N7Vx2u7PEoa(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0JxIyyg72fjeXbmTdyUr7(self):
        """[充值]-对公转账支付"""
        case = self.common_operations(login='main')
        case.JxIyyg72fjeXbmTdyUr7()
        res = [lambda: self.pc.dHWcCR(data='a', businessTypeStr='钱包充值', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ItN5k8HledkZ9VtTetAA(self):
        """[充值]-支付宝支付"""
        case = self.common_operations()
        case.ItN5k8HledkZ9VtTetAA()
        res = [lambda: self.pc.dHWcCR(businessTypeStr='钱包充值', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_a05NJAdkRNkHL45jPTjg(self):
        """[充值]-微信支付"""
        case = self.common_operations()
        case.a05NJAdkRNkHL45jPTjg()
        res = [lambda: self.pc.dHWcCR(businessTypeStr='钱包充值', createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
