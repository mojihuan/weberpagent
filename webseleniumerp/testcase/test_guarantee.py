# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestGuaranteeOrderManage(BaseCase, unittest.TestCase):
    """保卖管理|订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return guarantee_r.GuaranteeOrderManageRequest()
        else:
            return guarantee_p.GuaranteeOrderManagePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0quick_guarantee_item_submission(self):
        """[快速保卖]-输入物品编号-提交"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations(login='main')
        case.quick_guarantee_item_submission()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quick_guarantee_item_submission_delivery(self):
        """[快速保卖]-输入物品编号-提交并发货-快递sf"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.quick_guarantee_item_submission_delivery()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quick_guarantee_item_submission_delivery_jd(self):
        """[快速保卖]-输入物品编号-提交并发货-快递jd"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.quick_guarantee_item_submission_delivery_jd()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quick_guarantee_item_submission_delivery_self_mail(self):
        """[快速保卖]-输入物品编号-提交并发货-快递自行邮寄"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.quick_guarantee_item_submission_delivery_self_mail()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fast_item_shipping_by_yourself(self):
        """[快速保卖]-输入物品编号-提交并发货-自己送货"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.fast_item_shipping_by_yourself()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待取件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ship_now_by_express_sf(self):
        """[立即发货]-快递sf"""
        self.pre.operations(data=['FA1', 'EA1'])
        case = self.common_operations()
        case.ship_now_by_express_sf()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待取件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ship_now_by_express_jd(self):
        """[立即发货]-快递jd"""
        self.pre.operations(data=['FA1', 'EA1'])
        case = self.common_operations()
        case.ship_now_by_express_jd()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ship_now_by_express_self_mail(self):
        """[立即发货]-快递自行邮寄"""
        self.pre.operations(data=['FA1', 'EA1'])
        case = self.common_operations()
        case.ship_now_by_express_self_mail()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ship_now_by_express_send_it_yourself(self):
        """[立即发货]-自己送货"""
        self.pre.operations(data=['FA1', 'EA1'])
        case = self.common_operations()
        case.ship_now_by_express_send_it_yourself()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quick_guarantee_cancel_the_order(self):
        """[取消订单]-取消订单"""
        self.pre.operations(data=['FA1', 'EA1', 'EA2'])
        case = self.common_operations()
        case.quick_guarantee_cancel_the_order()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fast_guarantee_reshipment(self):
        """[重新发货]-自己送改快递-重新发货"""
        self.pre.operations(data=['FA1', 'EA1', 'EA2'])
        case = self.common_operations()
        case.fast_guarantee_reshipment()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待取件')]
        self.assert_all(*res)


class TestGuaranteeReturnsManage(BaseCase, unittest.TestCase):
    """保卖管理|退货管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return guarantee_r.GuaranteeReturnsManageRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0cancel_returns_by_mail(self):
        """[待退货tab]-邮寄退货-取消退货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2'])
        case = self.common_operations(login='main')
        case.cancel_returns_by_mail()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_change_the_return_method_by_mail(self):
        """[待退货tab]-邮寄退货-更改退货方式"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2'])
        case = self.common_operations()
        case.change_the_return_method_by_mail()
        res = [lambda: self.pc.guarantee_returns_manage_assert(applyTime='now', logisticsTypeStr='快递', i=1)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_self_lifted_cancel_a_return(self):
        """[待取货tab]-自提退货-取消退货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB3'])
        case = self.common_operations()
        case.self_lifted_cancel_a_return()
        # res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='待退货')]
        # self.assert_all(*res)   todo 测试环境无法测试

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_change_the_return_method(self):
        """[待取货tab]-自提退货-更改退货方式"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB3'])
        case = self.common_operations()
        case.change_the_return_method()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_confirm_receipt(self):
        """[退货已出库tab]-确认收货"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2', 'CC1'])
        case = self.common_operations()
        case.confirm_receipt()
        res = [lambda: self.pc.guarantee_order_manage_assert(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)


class TestGuaranteeGoodsManage(BaseCase, unittest.TestCase):
    """保卖管理|商品管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return guarantee_r.GuaranteeGoodsManageRequest()
        else:
            return guarantee_p.GuaranteeGoodsManagePages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    @unittest.skip('')
    def test_0return_method_express(self):  # 缺api用例
        """[退货]-快递"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations(login='main')
        case.return_method_express()
        obj = cached('id')
        # res = [lambda: self.pc.guarantee_order_manage_assert(id=obj, statusStr='待销售')]
        # self.assert_all(*res)   todo 测试环境无法测试

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('')
    def test_return_method_self_lifted(self):  # 缺api用例
        """[退货]-自提"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.return_method_self_lifted()
        # res = [lambda: self.pc.guarantee_goods_manage_assert(signTime='now', statusStr='待销售')]
        # self.assert_all(*res)   todo 测试环境无法测试

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_bid_reference_price(self):
        """[销售]-竞价拍机-今日参考价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.sell_bid_reference_price()
        obj = cached('id')
        res = [lambda: self.pc.guarantee_goods_manage_assert(id=obj, statusStr='销售中', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_bid_self_pricing(self):
        """[销售]-竞价拍机-自主定价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.sell_bid_self_pricing()
        obj = cached('id')
        res = [lambda: self.pc.guarantee_goods_manage_assertt(id=obj, statusStr='销售中', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_bid_platform_pricing(self):
        """[销售]竞价拍机-平台定价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.sell_bid_platform_pricing()
        obj = cached('id')
        res = [lambda: self.pc.guarantee_goods_manage_assert(id=obj, statusStr='待平台确认', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_same_sale_reference_price(self):
        """[销售]-第三方同售-今日参考价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.sell_same_sale_reference_price()
        obj = cached('id')
        res = [lambda: self.pc.guarantee_goods_manage_assert(id=obj, statusStr='销售中', saleTypeStr='同售')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_self_same_sale_pricing(self):
        """[销售]-第三方同售-自主定价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.sell_self_same_sale_pricing()
        obj = cached('id')
        res = [lambda: self.pc.guarantee_goods_manage_assert(id=obj, statusStr='销售中', saleTypeStr='同售')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_same_sale_platform_pricing(self):
        """[销售]-第三方同售-平台定价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.sell_same_sale_platform_pricing()
        obj = cached('id')
        res = [lambda: self.pc.guarantee_goods_manage_assert(id=obj, statusStr='待平台确认', saleTypeStr='同售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cancel_the_sale(self):
        """[取消销售]-取消销售"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4'])
        case = self.common_operations()
        case.cancel_the_sale()
        obj = cached('id')
        res = [lambda: self.guarantee.goods_list(id=obj, statusStr='待销售', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_update_price(self):
        """[改价]-改价"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4'])
        case = self.common_operations()
        case.update_price()
        obj = cached('id')
        res = [lambda: self.guarantee.goods_list(id=obj, signTime='now', statusStr='销售中', saleTypeStr='竞价拍机')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
