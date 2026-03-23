# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestCameraAfterSalesOrders(BaseCase, unittest.TestCase):
    """拍机管理|售后管理|售后订单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return camera_r.CameraAfterSalesOrdersRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0pending_end_of_after_sales(self):
        """[待处理]-结束售后"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2'])
        case = self.common_operations(login='camera')
        case.pending_end_of_after_sales()
        obj = cached('id')
        res = [lambda: self.pc.camera_after_sales_order_assert(headers='camera', afterStatusStr='主动取消', id=obj)]
        self.assert_all(*res)


class TestAListOfAirportVisits(BaseCase, unittest.TestCase):
    """拍机管理|拍机场次列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return camera_r.AListOfAirportVisitsRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    @unittest.skip('')
    def test_0direct_auction_bidding_modify_the_price(self):
        """[竞拍中]-直拍-修改价格"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        case = self.common_operations(login='camera')
        case.direct_auction_bidding_modify_the_price()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.camera_list_of_airport_visits_assert(headers='camera', data='a', articlesNo=obj, bidPrice=obj_2)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('')
    def test_secret_shot_bidding_modify_the_price(self):
        """[竞拍中]-暗拍-修改价格"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2', 'DD4', '@BA2'])
        case = self.common_operations()
        case.secret_shot_bidding_modify_the_price()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.camera_list_of_airport_visits_assert(headers='camera', data='a', articlesNo=obj, bidPrice=obj_2)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
