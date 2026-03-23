# coding: utf-8
from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(mg_r.IndexShippingRequest, mg_p.IndexShippingPages)
class TestAuctionIndex(MiniBaseCase):
    """首页"""

    # @BaseCase.auto('ui')
    # @BaseCase.author('Jack')
    # def test_0fast_submit_new_order(self):
    #     """[快速发货]-创建订单"""
    #     self.case.fast_submit_new_order()
    #     res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
    #     self.assert_all(*res)
    #
    # @BaseCase.auto('ui')
    # @BaseCase.author('Jack')
    # def test_auto_submit_new_order(self):
    #     """[精确发货]自动估价-创建订单"""
    #     self.case.auto_submit_new_order()
    #     res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
    #     self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0fast_submit_new_order(self):
        """[快速发货]-创建订单"""
        self.case.fast_submit_new_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_large_quantity_fast_submit_new_order(self):
        """[快速发货]-多数量-创建订单"""
        self.case.fast_submit_new_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_max_quantity_fast_submit_new_order(self):
        """[快速发货]-数量最大值-创建订单"""
        self.case.max_quantity_fast_submit_new_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_auto_submit_new_order(self):
        """[精确发货]自动估价-创建订单"""
        self.case.auto_submit_new_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_inspection_service_create_an_order(self):
        """[质检服务]创建订单"""
        self.case.quality_inspection_service_create_an_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)


@test_mode_handler(mg_r.PersonalSalesServiceRequest, None)
class TestAuctionMy(MiniBaseCase):
    """我的"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0sales_out_warehouse(self):
        """[待销售]-今日参考价-销售物品"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        self.case.sales_out_warehouse()
        res = [lambda: self.pc.platform_virtual_inventory_list_assert(headers='super', i=3, statusStr='销售中', signTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_self_pricing_selling_items(self):
        """[待销售]-自主定价-销售物品"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        self.case.self_pricing_selling_items()
        res = [lambda: self.pc.platform_virtual_inventory_list_assert(headers='super', i=3, statusStr='销售中', signTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_together_xy_sell_items(self):
        """[待销售]-平台定价-销售物品"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        self.case.together_xy_sell_items()
        res = [lambda: self.pc.platform_virtual_inventory_list_assert(headers='super', i=5, statusStr='待平台确认', signTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sales_re_inspection(self):
        """[待销售]-复检"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        self.case.sales_re_inspection()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='b', statusStr='待审核', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_express_easy_return(self):
        """[待销售]-快递退货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        self.case.express_easy_return()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_self_pickup_returns(self):
        """[待销售]-自提退货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        self.case.self_pickup_returns()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=2, logisticsTypeStr='自提', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sell_no_quality_check_return(self):
        """[待销售]-无需质检-退货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4', '@AB8'])
        self.case.sell_no_quality_check_return()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_cancel_the_sale(self):
        """[销售中]-取消销售"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4'])
        self.case.cancel_the_sale()
        obj = cached('id')
        res = [lambda: self.pc.auction_my_assert(j=1, i=2, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_price_change_during_sales(self):
        """[销售中]-改价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4'])
        self.case.case.price_change_during_sales()
        obj = cached('id')
        obj_2 = cached('upbeatPrice')
        res = [lambda: self.pc.auction_my_assert(j=1, i=3, id=obj, upbeatPrice=obj_2)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_platform_cancel_the_sale(self):
        """[待平台确认]-取消销售"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4'])
        self.case.platform_cancel_the_sale()
        obj = cached('id')
        res = [lambda: self.pc.auction_my_assert(j=1, i=2, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_change_the_return_method(self):
        """[退货中]-自提改快递-更改退货方式"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB3'])
        self.case.change_the_return_method()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_cancel_the_return(self):
        """[退货中]-取消退货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB3'])
        self.case.cancel_the_return()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=5, updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_confirm_receipt(self):
        """[退货已出库]-确认收货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2', 'CC1'])
        self.case.confirm_receipt()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='b', i=4, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_offer_confirms_sale(self):
        """[报价确认]-确认销售"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4', 'CD1', 'DA1'])
        self.case.offer_confirms_sale()
        res = [lambda: self.pc.platform_virtual_inventory_list_assert(headers='super', signTime='now', statusStr='销售待出库')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_shipped_immediately_sf(self):
        """[待发货]-立即发货-顺丰快递邮寄发货"""
        self.pre.operations(data=['@AA1'])
        self.case.shipped_immediately_sf()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_shipped_immediately_own(self):
        """[待发货]-立即发货-自行邮寄-顺丰发货"""
        self.pre.operations(data=['@AA1'])
        self.case.shipped_immediately_own()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_deliver_it_yourself(self):
        """[待发货]-立即发货-自己送货"""
        self.pre.operations(data=['@AA1'])
        self.case.deliver_it_yourself()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_shipped_immediately_sf_the_next_day(self):
        """[待发货]-立即发货-顺丰快递邮寄-次日发货"""
        self.pre.operations(data=['@AA1'])
        self.case.shipped_immediately_sf_the_next_day()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_shipped_immediately_no_shipping_address(self):
        """[待发货]-立即发货-顺丰快递邮寄-无收货地址"""
        self.pre.operations(data=['@AA1'])
        self.case.shipped_immediately_no_shipping_address()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_cancel_the_order(self):
        """[待发货]-取消订单"""
        self.pre.operations(data=['@AA1'])
        self.case.cancel_the_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(data='b', i=6, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_pickup_cancel_the_order(self):
        """[待取件]-取消订单"""
        self.pre.operations(data=['@AA1', '@AB6'])
        self.case.pending_pickup_cancel_the_order()
        obj = cached('id')
        res = [lambda: self.pc.auction_my_assert(data='b', i=6, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_receipt_cancel_the_order(self):
        """[待收货]-取消订单"""
        self.pre.operations(data=['@AA1', '@AB5'])
        self.case.pending_receipt_cancel_the_order()
        obj = cached('id')
        res = [lambda: self.pc.auction_my_assert(data='b', i=6, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_receipt_of_reshipment_by_sf_logistics(self):
        """[待收货]-重新发货-顺丰快递"""
        self.pre.operations(data=['@AA1', '@AB5'])
        self.case.pending_receipt_of_reshipment_by_sf_logistics()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_receipt_reshipment_self_mailing(self):
        """[待收货]-重新发货-自行邮寄"""
        self.pre.operations(data=['@AA1', '@AB5'])
        self.case.pending_receipt_reshipment_self_mailing()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_receipt_reshipment_deliver_it_yourself(self):
        """[待收货]-重新发货-自己送"""
        self.pre.operations(data=['@AA1', '@AB5'])
        self.case.pending_receipt_reshipment_deliver_it_yourself()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0quality_shipped_immediately_sf(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄发货"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_shipped_immediately_sf()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_shipped_immediately_own(self):
        """[待发货]-质检服务-立即发货-自行邮寄-顺丰发货"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_shipped_immediately_own()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_deliver_it_yourself(self):
        """[待发货]-质检服务-立即发货-自己送货"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_deliver_it_yourself()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_shipped_immediately_sf_the_next_day(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄-次日发货"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_shipped_immediately_sf_the_next_day()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_shipped_immediately_no_address(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄-无发货地址"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_shipped_immediately_no_address()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='自己送货/自取', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_shipped_immediately_no_shipping_address(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄-无收货地址"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_shipped_immediately_no_shipping_address()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=2, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_cancel_the_order(self):
        """[待发货]-质检服务-取消订单"""
        self.pre.operations(data=['@AA2'])
        self.case.quality_cancel_the_order()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=6, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_pending_pickup_cancel_the_order(self):
        """[待取件]-质检服务-取消订单"""
        self.pre.operations(data=['@AA2', '@AB7'])
        self.case.quality_pending_pickup_cancel_the_order()
        res = [lambda: self.fulfillment.order_manage(data='b', i=6, receiptNum=0, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_pending_receipt_cancel_the_order(self):
        """[待收货]-质检服务-取消订单"""
        self.pre.operations(data=['@AA2', '@AB1'])
        self.case.quality_pending_receipt_cancel_the_order()
        res = [lambda: self.fulfillment.order_manage(data='b', i=6, receiptNum=0, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_pending_receipt_of_reshipment_by_sf_logistics(self):
        """[待收货]-质检服务-重新发货-顺丰快递"""
        self.pre.operations(data=['@AA2', '@AB1'])
        self.case.quality_pending_receipt_of_reshipment_by_sf_logistics()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_pending_receipt_reshipment_self_mailing(self):
        """[待收货]-质检服务-重新发货-自行邮寄"""
        self.pre.operations(data=['@AA2', '@AB1'])
        self.case.quality_pending_receipt_reshipment_self_mailing()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_pending_receipt_reshipment_deliver_it_yourself(self):
        """[待收货]-质检服务-重新发货-自己送"""
        self.pre.operations(data=['@AA2', '@AB1'])
        self.case.quality_pending_receipt_reshipment_deliver_it_yourself()
        res = [lambda: self.pc.fulfillment_order_manage_assert(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_inspection_completed_express_return(self):
        """[质检完成]-质检服务-快递退货"""
        self.pre.operations(data=['@AA2', '@AB1', 'CA1', 'CB1', 'CB2'])
        self.case.quality_inspection_completed_express_return()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_self_pickup_returns(self):
        """[质检完成]-质检服务-自提退货"""
        self.pre.operations(data=['@AA2', '@AB1', 'CA1', 'CB1', 'CB2'])
        self.case.quality_self_pickup_returns()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=2, logisticsTypeStr='自提', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_sales_re_inspection(self):
        """[质检完成]-质检服务-复检"""
        self.pre.operations(data=['@AA2', '@AB1', 'CA1', 'CB1', 'CB2'])
        self.case.quality_sales_re_inspection()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='b', statusStr='待审核', applyTime='now')]
        self.assert_all(*res)
