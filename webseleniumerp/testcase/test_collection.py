# coding: utf-8
from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(collection_r.L9OPe7bpsb, None)
class TestL16aU13Q(MiniBaseCase):
    """bot速收小程序|估价"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0NlMCdnlfaAys36F8lpXa(self):
        """[估价]"""
        self.case.NlMCdnlfaAys36F8lpXa()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_hFO4xZGpC9IyEEtPv313(self):
        """[提交换钱]-创建订单"""
        self.case.hFO4xZGpC9IyEEtPv313()
        res = [lambda: self.pc.wEEUyb(orderTime='now', systemOrderStateStr='待用户到店', valuationNo=cached('i'))]
        self.assert_all(*res)
