# coding: utf-8
import unittest

from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(mc_r.BiddingCameraRequest, None)
class TestBiddingCamera(MiniBaseCase):
    """竞拍"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0bidding_offer(self):
        """[竞拍]暗拍-出价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2', 'DD4'])
        self.wait_until_next_five_minute()
        self.case.bidding_offer()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.bidding_camera_assert(headers='camera', data='a', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_modify_the_price(self):
        """[竞拍]暗拍-修改价格"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2', 'DD4', '@BA2'])
        self.wait_default()
        self.case.modify_the_price()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.bidding_camera_assert(headers='camera', data='a', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_auction_bidding(self):
        """[竞拍]直拍-出价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2'])
        self.wait_until_next_five_minute()
        self.case.direct_auction_bidding()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.bidding_camera_assert(headers='camera', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_auction_price_change(self):
        """[竞拍]直拍-改价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        self.wait_default()
        self.case.direct_auction_price_change()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.bidding_camera_assert(headers='camera', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)


@test_mode_handler(mc_r.BiddingMyRequest, None)
class TestBiddingMy(MiniBaseCase):
    """我的"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_straight_shot_change_to_self_pickup(self):
        """[待发货]直拍-改自提"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        self.wait_for_five_minutes()
        self.case.straight_shot_change_to_self_pickup()
        obj = cached('articlesNo')
        res = [lambda: self.pc.bidding_my_assert(headers='camera', i=3, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @unittest.skip('没按最新的数据排序，测不了')
    def test_direct_shot_change_to_mailing(self):
        """[待收货]直拍-改邮寄"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1'])
        self.case.direct_shot_change_to_mailing()
        obj = cached('articlesNo')
        res = [lambda: self.pc.bidding_my_assert(headers='camera', i=2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shot_confirm_receipt(self):
        """[待收货]直拍-确认收货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1'])
        self.case.direct_shot_confirm_receipt()
        obj = cached('articlesNo')
        res = [lambda: self.pc.bidding_my_assert(headers='camera', i=4, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shooting_apply_for_after_sales(self):
        """[已收货]直拍-申请售后"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1'])
        self.case.direct_shooting_apply_for_after_sales()
        res = [lambda: self.pc.camera_after_sales_order_assert(headers='camera', applyTime='now', afterDesc='售后', afterStatusStr='线上审核', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_auction_receives_the_difference(self):
        """[可补差]直拍-接收补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF1'])
        self.case.direct_auction_receives_the_difference()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[5], headers='camera', id=obj, afterStatus=5)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shot_refuses_to_make_up_for_the_difference(self):
        """[可补差]直拍-拒绝补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF1'])
        self.case.direct_shot_refuses_to_make_up_for_the_difference()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[7], headers='camera', id=obj, afterStatus=7)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shooting_ends_after_sales(self):
        """[可补差]直拍-结束售后"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF1'])

        self.case.direct_shooting_ends_after_sales()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(i=4, headers='camera', id=obj, articlesStatus=4)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shot_go_shipping(self):
        """[待寄回]直拍-去发货-预约上门"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2'])
        self.case.direct_shot_go_shipping()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(id=obj, afterStatus=10, buyerReturnModeStr='预约上门', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shooting_to_ship_logistics(self):
        """[待寄回]直拍-去发货-自叫物流"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2'])
        self.case.direct_shooting_to_ship_logistics()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(id=obj, afterStatus=10, buyerReturnModeStr='自叫物流', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shot_to_ship_by_yourself(self):
        """[待寄回]直拍-去发货-自行送货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2'])
        self.case.direct_shot_to_ship_by_yourself()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(id=obj, afterStatus=10, buyerReturnModeStr='自行送货', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shot_re_inspection_receive_the_spread(self):
        """[可补差]-直拍-复检审核-接收补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB4', 'CF3', 'CB7', 'CB8', 'CF4'])
        self.case.direct_shot_re_inspection_receive_the_spread()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[5], headers='camera', id=obj, afterStatus=5)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shot_re_inspection_rejection_price(self):
        """[可补差]-直拍-复检审核-拒绝补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB4', 'CF3', 'CB7', 'CB8', 'CF4'])
        self.case.direct_shot_re_inspection_rejection_price()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[7], headers='camera', id=obj, afterStatus=7)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_shooting_re_inspection_ends_after_sales(self):
        """[可补差]-直拍-复检审核-结束售后"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5'])
        self.case.direct_shooting_re_inspection_ends_after_sales()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[9], headers='camera', id=obj, afterStatus=9)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_straight_shot_i_want_to_appeal(self):
        """[待申诉]-直拍-我要申诉"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5'])
        self.case.straight_shot_i_want_to_appeal()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[4], headers='camera', id=obj, afterStatus=4)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_appeal_and_end_after_sales(self):
        """[待申诉]-直拍-结束售后"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5'])
        self.case.pending_appeal_and_end_after_sales()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[4], headers='camera', id=obj, afterStatus=4)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_platform_review_receive_the_spread(self):
        """[可补差]-直拍-平台申诉通过-接收补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC2'])
        self.case.direct_platform_review_receive_the_spread()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[5], headers='camera', id=obj, afterStatus=5)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_platform_review_no_rejection_price(self):
        """[可补差]-直拍-平台申诉通过-拒绝补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC2'])
        self.case.direct_platform_review_no_rejection_price()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[7], headers='camera', id=obj, afterStatus=7)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_platform_review_ends_after_sales(self):
        """[可补差]-直拍-平台申诉通过-结束售后"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC2'])
        self.case.direct_platform_review_ends_after_sales()
        obj = cached('id')
        res = [lambda: self.pc.bidding_my_assert(data='c', i=[9], headers='camera', id=obj, afterStatus=9)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_platform_review_go_shipping(self):
        """[待寄回]-直拍-平台申诉通过-去发货-预约上门"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1'])
        self.case.direct_platform_review_go_shipping()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(id=obj, afterStatus=10, buyerReturnModeStr='预约上门', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_platform_review_self_proclaimed_logistics(self):
        """[待寄回]-直拍-平台申诉通过-去发货-自叫物流"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1'])
        self.case.direct_platform_review_self_proclaimed_logistics()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(id=obj, afterStatus=10, buyerReturnModeStr='自叫物流', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_direct_platform_review_mail_it_yourself(self):
        """[待寄回]-直拍-平台申诉通过-去发货-自行送货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1'])
        self.case.direct_platform_review_mail_it_yourself()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(id=obj, afterStatus=10, buyerReturnModeStr='自行送货', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
