# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestSellAfterSalesHanding(BaseCase, unittest.TestCase):
    """商品销售|销售售后管理|销售售后处理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellAfterSalesHandlingRequest()
        else:
            return sell_p.SellAfterSalesHandlingPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sell_returned_spare_parts_after_sale_journey(self):
        """[销售售后处理]-仅退配件未收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations(login='main')
        case.sell_returned_spare_parts_after_sale_journey()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', saleTypeStr='仅退配件', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_returned_spare_parts_after_sale_journey_warehouse(self):
        """[销售售后处理]-仅退配件已收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sell_returned_spare_parts_after_sale_journey_warehouse()
        res = [lambda: self.pc.sell_after_sales_list_assert(saleTypeStr='仅退配件', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_after_sales_returns(self):
        """[销售售后处理]-退货-邮寄已收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sales_after_sales_returns()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', saleTypeStr='退货', createTime='now')]
        self.assert_all(*res)


class TestSellGoodsListing(BaseCase, unittest.TestCase):
    """商品销售|销售管理|销售上架"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellGoodsListingRequest()
        else:
            return sell_p.SellGoodsListingPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sell_goods_listing(self):
        """[添加物品]-销售上架"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations(login='main')
        case.sell_goods_listing()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(typeRes='上架', orderStateStr='未完结', shelfTime='now')]
        self.assert_all(*res)


class TestPurchaseGoodsReceived(BaseCase, unittest.TestCase):
    """商品销售|销售管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellWaitReceivedRequest()
        else:
            return sell_p.SellGoodsReceivedPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0goods_received(self):
        """[接收]-全部物品接收"""
        self.pre.operations(data=['FA1', 'HC8'])
        case = self.common_operations(login='special')
        case.goods_received()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_goods_received(self):
        """[扫码精确接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC8'])
        case = self.common_operations()
        case.scan_goods_received()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wait_received_one_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.wait_received_one_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.sell_goods_received_assert(imei=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wait_received_one_search_by_date(self):
        """[搜索]-date查询"""
        case = self.common_operations()
        case.wait_received_one_search_by_date()
        res = [lambda: self.pc.sell_goods_received_assert(deliveryTime='now')]
        self.assert_all(*res)


class TestSellMiddleItemList(BaseCase, unittest.TestCase):
    """商品销售|销售管理|销售中物品列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellMiddleItemListRequest()
        else:
            return sell_p.SellMiddleItemListPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0edit_sale_info_import(self):
        """[全部tab]销售类型上架-修改销售信息-导入添加物品修改"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations(login='main')
        case.edit_sale_info_import()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_edit_status_info_not_received(self):
        """[全部tab]-销售类型上架-修改销售状态-普通快递-未收款-确认销售"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.edit_status_info_not_received()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_edit_status_info_pay(self):
        """[全部tab]-销售类型上架-修改销售状态-普通快递-已收款-确认销售"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.edit_status_info_pay()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_on_and_off_shelves(self):
        """[全部tab]-销售类型上架-下架-确认下架"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.on_and_off_shelves()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bulk_shakedown(self):
        """[销售中tab]-销售类型上架-批量下架-确认下架"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.bulk_shakedown()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_presale_confirm_the_sale(self):
        """[销售中tab]-销售类型预售-更改销售状态-确认销售"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.presale_confirm_the_sale()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_and_delivery_of_goods(self):
        """[销售中tab]-销售类型铺货-铺货退回"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.sales_and_delivery_of_goods()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_goods_out_of_the_warehouse(self):
        """[销售中tab]-销售类型铺货-铺货销售出库"""
        self.pre.operations(data=['FA1', 'HC1', 'IB1'])
        case = self.common_operations()
        case.sell_goods_out_of_the_warehouse()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_search_in_sale_type(self):
        """[搜索]-销售类型查询"""
        case = self.common_operations()
        case.sell_search_in_sale_type()
        obj = cached('saleType')
        res = [lambda: self.pc.sell_list_of_items_for_sale_assert(saleType=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_search_in_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.sell_search_in_imei()
        obj = cached('imei')
        res = [lambda: self.pc.sell_list_of_items_for_sale_assert(imei=obj, i=1)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_search_in_supplier_id(self):
        """[搜索]-销售客户查询"""
        case = self.common_operations()
        case.sell_search_in_supplier_id()
        obj = cached('saleSupplierId')
        res = [lambda: self.pc.sell_list_of_items_for_sale_assert(saleSupplierId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_search_in_belong_type(self):
        """[搜索]-平台物品编号查询"""
        case = self.common_operations()
        case.sell_search_in_belong_type()
        obj = cached('belongType')
        res = [lambda: self.pc.sell_list_of_items_for_sale_assert(belongType=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_search_in_user_id(self):
        """[搜索]-销售人员查询"""
        case = self.common_operations()
        case.sell_search_in_user_id()
        obj = cached('userId')
        res = [lambda: self.pc.sell_list_of_items_for_sale_assert(userId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_search_in_date(self):
        """[搜索]-上架/出库查询"""
        case = self.common_operations()
        case.sell_search_in_date()
        res = [lambda: self.pc.sell_list_of_items_for_sale_assert(shelfTime='now')]
        self.assert_all(*res)


class TestSellSaleItem(BaseCase, unittest.TestCase):
    """商品销售|销售管理|待销售物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellSaleItemRequest()
        else:
            return sell_p.SellSaleItemPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sell_advance_sale(self):
        """销售预售出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations(login='main')
        case.sell_advance_sale()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='预售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_get_out(self):
        """[出库]-销售出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sell_get_out()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_distribution(self):
        """[出库]-销售铺货出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sell_distribution()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='铺货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_listing(self):
        """[上架]-销售上架"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sell_listing()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wait_sell_articles_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.wait_sell_articles_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.sell_items_for_sale_assert(imei=obj)]
        self.assert_all(*res)


class TestSellingOrderList(BaseCase, unittest.TestCase):
    """商品销售|销售管理|销售中订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellingOrderListRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0selling_order_search_by_batch_no(self):
        """[搜索]-销售中单号查询"""
        case = self.common_operations(login='main')
        case.selling_order_search_by_batch_no()
        obj = cached('batchNo')
        res = [lambda: self.pc.sell_order_list_for_sale_assert(batchNo=obj, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_selling_order_search_by_type(self):
        """[搜索]-销售类型查询"""
        case = self.common_operations()
        case.selling_order_search_by_type()
        obj = cached('type')
        res = [lambda: self.pc.sell_order_list_for_sale_assert(type=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_selling_order_search_by_sale_supplier_id(self):
        """[搜索]-销售客户查询"""
        case = self.common_operations()
        case.selling_order_search_by_sale_supplier_id()
        obj = cached('saleSupplierId')
        res = [lambda: self.pc.sell_order_list_for_sale_assert(saleSupplierId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_selling_order_search_by_sale_user_id(self):
        """[搜索]-销售人员查询"""
        case = self.common_operations()
        case.selling_order_search_by_sale_user_id()
        obj = cached('saleUserId')
        res = [lambda: self.pc.sell_order_list_for_sale_assert(saleUserId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_selling_order_search_by_sale_date(self):
        """[搜索]-上架/出库时间查询"""
        case = self.common_operations()
        case.selling_order_search_by_sale_date()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_selling_order_search_by_logistics_no(self):
        """[搜索]-物流单号查询"""
        case = self.common_operations()
        case.selling_order_search_by_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.sell_order_list_for_sale_assert(logisticsNo=obj)]
        self.assert_all(*res)


class TestSellSaleOrderList(BaseCase, unittest.TestCase):
    """商品销售|销售管理|已销售订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellSaleOrderListRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0search_by_order_no(self):
        """[搜索]-销售单号查询"""
        case = self.common_operations()
        case.search_by_order_no()
        obj = cached('orderNo')
        res = [lambda: self.pc.sell_sold_order_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_state(self):
        """[搜索]-销售单号查询"""
        case = self.common_operations()
        case.search_by_state()
        obj = cached('status')
        res = [lambda: self.pc.sell_sold_order_assert(status=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_search_by_sale_supplier_id(self):
        """[搜索]-销售客户查询"""
        case = self.common_operations()
        case.search_by_sale_supplier_id()
        obj = cached('saleSupplierId')
        res = [lambda: self.pc.sell_sold_order_assert(saleSupplierId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_sale_user_id(self):
        """[搜索]-销售人员查询"""
        case = self.common_operations()
        case.search_by_sale_user_id()
        obj = cached('saleUserId')
        res = [lambda: self.pc.sell_sold_order_assert(saleUserId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_search_by_date(self):
        """[搜索]-销售时间查询"""
        case = self.common_operations()
        case.order_search_by_date()
        res = [lambda: self.pc.sell_sold_order_assert(saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_search_by_out_date(self):
        """[搜索]-出库时间查询"""
        case = self.common_operations()
        case.order_search_by_out_date()
        res = [lambda: self.pc.sell_sold_order_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_search_by_logistics_no(self):
        """[搜索]-物流单号查询"""
        case = self.common_operations()
        case.order_search_by_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.sell_sold_order_assert(logisticsNo=obj)]
        self.assert_all(*res)


class TestSellSaleItemList(BaseCase, unittest.TestCase):
    """商品销售|销售管理|已销售物品列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellSaleItemListRequest()
        else:
            return sell_p.SellSaleItemListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sell_refund_difference(self):
        """[销售售后]-销售售后处理-调价"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations(login='main')
        case.sell_refund_difference()
        res = [lambda: self.pc.sell_after_sales_list_assert(saleTime='now', saleTypeStr='调价', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_return_only_parts_route(self):
        """[销售售后]-销售售后处理-仅退配件未收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sell_return_only_parts_route()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_return_only_parts_warehousing(self):
        """[销售售后]-销售售后处理-仅退配件已收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sell_return_only_parts_warehousing()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_return_goods_route(self):
        """[销售售后]-销售售后处理-退货-邮寄未收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sell_return_goods_route()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_return_goods_warehousing(self):
        """[销售售后]-销售售后处理-退货-邮寄已收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sell_return_goods_warehousing()
        res = [lambda: self.pc.sell_after_sales_list_assert(saleTime='now', saleTypeStr='仅退款', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_are_refunded_only(self):
        """[销售售后]-销售售后处理-仅退款"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.sales_are_refunded_only()
        res = [lambda: self.pc.sell_after_sales_list_assert(saleTime='now', saleTypeStr='仅退款', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_sale_no(self):
        """[搜索]-销售单号查询"""
        case = self.common_operations()
        case.search_by_sale_no()
        obj = cached('salesOrder')
        res = [lambda: self.pc.sell_sale_item_list_assert(salesOrder=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.sell_sale_item_list_assert(imei=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_category_id(self):
        """[搜索]-品类查询"""
        case = self.common_operations()
        case.search_by_category_id()
        obj = cached('categoryId')
        res = [lambda: self.pc.sell_sale_item_list_assert(belongType=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_brand(self):
        """[搜索]-品牌查询"""
        case = self.common_operations()
        case.search_by_brand()
        res = [lambda: self.pc.sell_sale_item_list_assert(brandId=1)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_model(self):
        """[搜索]-型号查询"""
        case = self.common_operations()
        case.search_by_model()
        obj = cached('modelId')
        res = [lambda: self.pc.sell_sale_item_list_assert(modelId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_supplier_id(self):
        """[搜索]-供应商查询"""
        case = self.common_operations()
        case.search_by_supplier_id()
        obj = cached('supplierId')
        res = [lambda: self.pc.sell_sale_item_list_assert(supplierId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_sale_supplier_id(self):
        """[搜索]-销售客户查询"""
        case = self.common_operations()
        case.search_by_sale_supplier_id()
        obj = cached('clientId')
        res = [lambda: self.pc.sell_sale_item_list_assert(clientId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_status(self):
        """[搜索]-收款状态查询"""
        case = self.common_operations()
        case.search_by_status()
        obj = cached('status')
        res = [lambda: self.pc.sell_sale_item_list_assert(status=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_status(self):
        """[搜索]-收款状态查询"""
        case = self.common_operations()
        case.search_by_status()
        obj = cached('status')
        res = [lambda: self.pc.sell_sale_item_list_assert(status=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_platform_no(self):
        """[搜索]-平台物品编号查询"""
        case = self.common_operations()
        case.search_by_platform_no()
        obj = cached('platformNo')
        res = [lambda: self.pc.sell_sale_item_list_assert(platformNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_sell_platform_no(self):
        """[搜索]-平台销售单号查询"""
        case = self.common_operations()
        case.search_by_sell_platform_no()
        obj = cached('sellPlatformOrderNo')
        res = [lambda: self.pc.sell_sale_item_list_assert(sellPlatformOrderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_sell_date(self):
        """[搜索]-销售时间查询"""
        case = self.common_operations()
        case.search_by_sell_date()
        res = [lambda: self.pc.sell_sale_item_list_assert(saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_user_id(self):
        """[搜索]-销售时间查询"""
        case = self.common_operations()
        case.search_by_user_id()
        obj = cached('userId')
        res = [lambda: self.pc.sell_sale_item_list_assert(userId=obj)]
        self.assert_all(*res)


class TestSellSalesList(BaseCase, unittest.TestCase):
    """商品销售|销售售后管理|销售售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellSalesListRequest()
        else:
            return sell_p.SellSalesListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sell_after_sale_barter(self):
        """[更新售后状态]-换货-普通快递-确认出库"""
        self.pre.operations(data=['FA1', 'FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations(login='main')
        case.sell_after_sale_barter()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='换货', articlesStatusStr='待分货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_attachment(self):
        """[更新售后状态]-仅退配件-确认入库"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA3'])
        case = self.common_operations()
        case.sell_after_sale_attachment()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='仅退配件', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_repair(self):
        """[更新售后状态]-返修-普通快递-确认出库"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_repair()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='返修', articlesStatusStr='已销售', )]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_refund(self):
        """[更新售后状态]-退货退款-无平台售后罚款"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_refund()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='退货退款', articlesStatusStr='待分货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_refusal_return(self):
        """[更新售后状态]-拒退退回-普通快递-确认出库"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_refusal_return()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='拒退退回', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_articles_no(self):
        """[搜索]-IMEI搜索"""
        case = self.common_operations()
        case.sell_after_sale_by_articles_no()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_platform_articles_no(self):
        """[搜索]-平台物品编号搜索"""
        case = self.common_operations()
        case.sell_after_sale_by_platform_articles_no()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_sale_order_no(self):
        """[搜索]-销售售后单号搜索"""
        case = self.common_operations()
        case.sell_after_sale_by_sale_order_no()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_sale_user_id(self):
        """[搜索]-销售客户搜索"""
        case = self.common_operations()
        case.sell_after_sale_by_sale_user_id()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_sale_type(self):
        """[搜索]-售后类型搜索"""
        case = self.common_operations()
        case.sell_after_sale_by_sale_type()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_create_time(self):
        """[搜索]-销售时间搜索"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_by_create_time()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_return_type(self):
        """[搜索]-退回方式搜索"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_by_return_type()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_by_is_sale_channel(self):
        """[搜索]-退回方式搜索"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_by_is_sale_channel()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)


class TestSellCustomManage(BaseCase, unittest.TestCase):
    """商品销售|客户管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellCustomManageRequest()
        else:
            return None


class TestSellStatics(BaseCase, unittest.TestCase):
    """商品销售|数据统计"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.SellStaticsRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_sell_statics_search_by_sale_custom(self):
        """[搜索]-销售客户搜索"""
        case = self.common_operations()
        case.sell_statics_search_by_sale_custom()
        obj = cached('saleSupplierId')
        res = [lambda: self.pc.sell_statics_assert(saleSupplierId=obj, i=obj)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
