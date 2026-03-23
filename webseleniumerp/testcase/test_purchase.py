# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *
from config.constant import CON
from config.user_info import INFO


class TestPurchaseAdd(BaseCase, unittest.TestCase):
    """商品采购|采购管理|新增采购单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseAddRequest()
        else:
            return purchase_p.PurchaseAddPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_purchase_order_unpaid_journey(self):
        """[新增]-苹果手机-未付款在路上-单个物品创建采购单"""
        case = self.common_operations(login='main')
        case.new_purchase_order_unpaid_journey()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_purchase_order_unpaid_warehouse(self):
        """[新增]-苹果手机-未付款入库-单个物品创建采购单"""
        case = self.common_operations()
        case.new_purchase_order_unpaid_warehouse()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_purchase_order_has_not_been_shipped(self):
        """[新增]-苹果手机-未付款未发货-单个物品创建采购单"""
        case = self.common_operations()
        case.new_purchase_order_has_not_been_shipped()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='未发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_create_batch_order(self):
        """[新增]-苹果手机-已付款已到货-多个物品创建采购单"""
        case = self.common_operations()
        case.create_batch_order()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_purchase_order_paid_warehouse(self):
        """[新增]-苹果手机-已付款已到货-单个物品创建采购单"""
        case = self.common_operations()
        case.new_purchase_order_paid_warehouse()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_purchase_order(self):
        """[导入]-采购物品导入-创建采购单"""
        case = self.common_operations()
        case.import_purchase_order()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_transfer_import_create_a_purchase_order(self):
        """[导入]-转转导入-创建采购单"""
        case = self.common_operations()
        case.transfer_import_create_a_purchase_order()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_and_adjust_price(self):
        """[批量调价]-调价后创建采购单"""
        case = self.common_operations()
        case.import_and_adjust_price()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_create_and_transfer_order(self):
        """[新增]-已付款入库-创建采购单-入库并移交订单原因是质检"""
        case = self.common_operations()
        case.create_and_transfer_order()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)


class TestPurchaseAddTwo(TestPurchaseAdd):
    """商品采购|采购管理|新增采购单"""

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_create_with_new_supplier(self):
        """[+-创建供应商]-选择供应商生成采购单"""
        case = self.common_operations(login='idle')
        case.create_with_new_supplier()
        res = [lambda: self.pc.purchase_order_list_assert(headers='idle', purchaseTime='now', payStateStr='部分付款', stateStr='已收货')]
        self.assert_all(*res)


class TestPurchaseAfterSaleList(BaseCase, unittest.TestCase):
    """商品采购|采购售后管理|采购售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseAfterSaleListRequest()
        else:
            return purchase_p.PurchaseAfterSaleListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0purchase_barter_route(self):
        """[采购售后中tab]-换货-在途"""
        self.pre.operations(data=['FA1', 'HC6', 'HG1'])
        case = self.common_operations(login='main')
        case.purchase_barter_route()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购换货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_barter_warehousing(self):
        """[采购售后中tab]-换货-直接入库"""
        self.pre.operations(data=['FA1', 'HC6', 'HG1'])
        case = self.common_operations()
        case.purchase_barter_warehousing()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购换货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_refund_single(self):
        """[采购售后中tab]-退货退款-未结算"""
        self.pre.operations(data=['FA1', 'HC6', 'HG1'])
        case = self.common_operations()
        case.purchase_refund_single()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购退货退款')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_refuse_route(self):
        """[采购售后中tab]-拒退退回-在途"""
        self.pre.operations(data=['FA1', 'HC6', 'HG1'])
        case = self.common_operations()
        case.purchase_refuse_route()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购拒退')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_refuse_warehousing(self):
        """[采购售后中tab]-拒退退回-入库"""
        self.pre.operations(data=['FA1', 'HC6', 'HG1'])
        case = self.common_operations()
        case.purchase_refuse_warehousing()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购拒退')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', imei=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_supplier_id(self):
        """[搜索]-supplier_id查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_supplier_id()
        obj = cached('supplierId')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', supplierId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_platform_articles_no(self):
        """[搜索]-platform_articles_no查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_platform_articles_no()
        obj = cached('platformArticlesNo')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', platformArticlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_sale_state(self):
        """[搜索]-sale_state查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_sale_state()
        obj = cached('saleState')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleState=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_sale_no(self):
        """[搜索]-sale_no查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_sale_no()
        obj = cached('saleNo')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_logistics_no(self):
        """[搜索]-logistics_no查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_date(self):
        """[搜索]-date查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_date()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_sale_no(self):
        """[搜索]-售后订单号查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_sale_no()
        obj = cached('saleNo')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_after_list_search_by_logistics_no(self):
        """[搜索]-出库物流单号查询"""
        case = self.common_operations()
        case.purchase_after_list_search_by_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', logisticsNo=obj)]
        self.assert_all(*res)


class TestPurchaseAwaitAfterSaleList(BaseCase, unittest.TestCase):
    """商品采购|采购售后管理|待售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseAwaitAfterSaleListRequest()
        else:
            return purchase_p.PurchaseAwaitAfterSaleListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0cancel_purchase_after_sale(self):
        """[取消售后]-确认取消"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations(login='main')
        case.cancel_purchase_after_sale()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_refund_difference_not_settled(self):
        """[售后操作]-采购补差-未结算确认"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.purchase_refund_difference_not_settled()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购退差价')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_refund_difference_settled(self):
        """[售后操作]-采购补差-已结算确认"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.purchase_refund_difference_settled()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购退差价')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_delivery(self):
        """[售后操作]-售后出库-普通快递-无"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_delivery()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购售后中')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_outbound_return_refund_unsettled(self):
        """[售后操作]-售后出库-普通快递-退货退款-未结算"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_outbound_return_refund_unsettled()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购退货退款')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_outbound_return_refund_settled(self):
        """[售后操作]-售后出库-普通快递-退货退款-已结算"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_outbound_return_refund_settled()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购退货退款')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_delivery_refusal_to_return_in_transit(self):
        """[售后操作]-售后出库-普通快递-拒退退回-在途"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_delivery_refusal_to_return_in_transit()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购拒退')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_outbound_refuse_to_return_warehousing(self):
        """[售后操作]-售后出库-普通快递-拒退退回-直接入库"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_outbound_refuse_to_return_warehousing()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购拒退')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_delivery_exchange_in_transit(self):
        """[售后操作]-售后出库-普通快递-换货-在途"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_delivery_exchange_in_transit()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购换货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_after_sales_outbound_replacement_warehousing(self):
        """[售后操作]-售后出库-普通快递-换货-直接入库"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.after_sales_outbound_replacement_warehousing()
        res = [lambda: self.pc.purchase_after_sales_list_assert(createTime='now', saleStateStr='采购换货')]
        self.assert_all(*res)


class TestPurchaseGoodsReceived(BaseCase, unittest.TestCase):
    """商品采购|采购售后管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseGoodsReceivedRequest()
        else:
            return purchase_p.PurchaseGoodsReceivedPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0goods_received(self):
        """[接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC7'])
        case = self.common_operations(login='special')
        case.goods_received()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_goods_received(self):
        """[扫码精确接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC7'])
        case = self.common_operations()
        case.scan_goods_received()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_imei(self):
        """[搜索]-IMEI查询"""
        case = self.common_operations()
        case.search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.purchase_items_to_be_received_assert(imei=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_by_date(self):
        """[搜索]-移交时间查询"""
        case = self.common_operations()
        case.search_by_date()
        res = [lambda: self.pc.purchase_items_to_be_received_assert(deliveryTime='now')]
        self.assert_all(*res)


class TestPurchaseOrderList(BaseCase, unittest.TestCase):
    """商品采购|采购管理|采购订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseOrderListRequest()
        else:
            return purchase_p.PurchaseOrderListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_purchase_order_refund(self):
        """[采购单号]-售后处理-采购仅退款"""
        self.pre.operations(data=['FA2'])
        case = self.common_operations(login='main')
        case.new_purchase_order_refund()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_logistics_delivery(self):
        """[物流发货]-发货"""
        self.pre.operations(data=['FA4'])
        case = self.common_operations()
        case.logistics_delivery()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_items_shipping(self):
        """[物流发货]-导入物品-发货"""
        self.pre.operations(data=['FA4'])
        case = self.common_operations(login='main')
        case.import_items_shipping()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_receive_goods(self):
        """[收货]-签收入库"""
        self.pre.operations(data=['FA2'])
        case = self.common_operations()
        case.receive_goods()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_purchase_number(self):
        """[搜索]-采购单号查询"""
        case = self.common_operations()
        case.order_list_search_by_purchase_number()
        obj = cached('orderNo')
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_supplier(self):
        """[搜索]-供应商查询"""
        case = self.common_operations()
        case.order_list_search_by_supplier()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', supplierId=INFO['main_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_order_state(self):
        """[搜索]-订单状态查询"""
        type_ary = DICT_DATA['g']
        for item in type_ary:
            case = self.common_operations()
            case.order_list_search_by_order_state(item['key'], item['val'])
            obj = cached('stateStr')
            res = [lambda: self.pc.purchase_order_list_assert(i=item['key'], stateStr=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.order_list_search_by_imei()
        obj = cached('articlesNoList')
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', articlesNoList=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_logistics_no(self):
        """[搜索]-物流单号查询"""
        case = self.common_operations()
        case.order_list_search_by_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_pay_state(self):
        """[搜索]-付款状态查询"""
        type_ary = DICT_DATA['b']
        for item in type_ary:
            case = self.common_operations(item['key'], item['val'])
            case.order_list_search_by_pay_state()
            obj = cached('payStateStr')
            res = [lambda: self.pc.purchase_order_list_assert(j=item['key'], payStateStr=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_purchase_uid(self):
        """[搜索]-采购账号查询"""
        case = self.common_operations()
        case.order_list_search_by_purchase_uid()
        obj = cached('purchaseUserId')
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', purchaseUserId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_uid(self):
        """[搜索]-采购人查询"""
        case = self.common_operations()
        case.order_list_search_by_uid()
        obj = cached('userId')
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', userId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_list_search_by_date(self):
        """[搜索]-日期查询"""
        case = self.common_operations()
        case.order_list_search_by_date()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now')]
        self.assert_all(*res)


class TestPurchaseSupplierManage(BaseCase, unittest.TestCase):
    """商品采购|供应商管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseSupplierManageRequest()
        else:
            return purchase_p.PurchaseSupplierManagePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_supplier(self):
        """[新增]-平台拍货-默认付款状态"""
        case = self.common_operations(login='idle')
        case.new_supplier()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_edit_supplier(self):
        """[编辑]-修改信息保存"""
        case = self.common_operations()
        case.edit_supplier()
        res = [lambda: self.pc.purchase_supplier_manage_assert(headers='idle', updateTime='now')]
        self.assert_all(*res)


class TestPurchaseWorkOrder(BaseCase, unittest.TestCase):
    """商品采购|采购管理|采购工单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseWorkOrderRequest()
        else:
            return purchase_p.PurchaseWorkOrderPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0work_order_add(self):
        """[创建采购工单]"""
        case = self.common_operations(login='main')
        case.work_order_add()
        res = [lambda: self.pc.purchase_work_order_assert(stateStr='待开始', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_work_order_edit(self):
        """[修改采购工单]"""
        self.pre.operations(data=['FC1'])
        case = self.common_operations()
        case.work_order_edit()
        res = [lambda: self.pc.purchase_work_order_assert(stateStr='待开始', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_work_order_to_start_the_task(self):
        """[开始任务]"""
        self.pre.operations(data=['FC1'])
        # case = self.common_operations()
        # case.work_order_to_start_the_task()
        # res = [lambda: self.pc.purchase_work_order_assert(stateStr='进行中', updateTime='now')]
        # self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_work_order_ends_the_task(self):
        """[结束任务]"""
        self.pre.operations(data=['FC1', 'FC2'])
        case = self.common_operations()
        case.work_order_ends_the_task()
        res = [lambda: self.pc.purchase_work_order_assert(stateStr='已结束', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_work_order_resumes_tasks(self):
        """[恢复任务]"""
        self.pre.operations(data=['FC1', 'FC2', 'FC3'])
        case = self.common_operations()
        case.work_order_resumes_tasks()
        res = [lambda: self.pc.purchase_work_order_assert(stateStr='进行中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_work_order_del(self):
        """[删除采购工单]"""
        self.pre.operations(data=['FC1'])
        case = self.common_operations()
        case.work_order_del()


class TestPurchaseUnSendOrder(BaseCase, unittest.TestCase):
    """商品采购|采购管理|未发货订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseUnsendListRequest()
        else:
            return purchase_p.PurchaseUnsendListPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0order_export(self):
        """[导出]-导出"""
        case = self.common_operations(login='main')
        case.order_export()
        res = [lambda: self.pc.system_export_list_assert(name='未发货物品列表导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unsend_order_by_supplier(self):
        """[搜索]-供应商查询"""
        case = self.common_operations()
        case.unsend_order_by_supplier()
        res = [lambda: self.pc.purchase_un_shipped_order_list_assert(createTime='now', supplierName=INFO['main_supplier_name'])]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unsend_order_by_platform_order_no(self):
        """[搜索]-平台订单号查询"""
        case = self.common_operations()
        case.unsend_order_by_platform_order_no()
        obj = cached('platformOrderNo')
        res = [lambda: self.pc.purchase_un_shipped_order_list_assert(createTime='now', platformOrderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unsend_order_by_platform_articles_no(self):
        """[搜索]-平台物品编号查询"""
        case = self.common_operations()
        case.unsend_order_by_platform_articles_no()
        obj = cached('platformArticlesNo')
        res = [lambda: self.pc.purchase_un_shipped_order_list_assert(createTime='now', platformArticlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unsend_order_by_platform_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.unsend_order_by_platform_imei()
        obj = cached('imei')
        res = [lambda: self.pc.purchase_un_shipped_order_list_assert(createTime='now', imei=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unsend_order_by_platform_date(self):
        """[搜索]-date查询"""
        case = self.common_operations()
        case.unsend_order_by_platform_date()
        res = [lambda: self.pc.purchase_un_shipped_order_list_assert(createTime='now')]
        self.assert_all(*res)


class TestPurchaseArrivalList(BaseCase, unittest.TestCase):
    """商品采购|采购管理|到货通知单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.PurchaseArrivalListRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0arrival_list_by_supplier(self):
        """[搜索]-供应商查询"""
        case = self.common_operations(login='main')
        case.arrival_list_by_supplier()
        obj = cached('supplierId')
        res = [lambda: self.pc.purchase_arrival_notices_assert(purchaseTime='now', supplierId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_arrival_list_by_platform_logistics_no(self):
        """[搜索]-物流单号查询"""
        case = self.common_operations()
        case.arrival_list_by_platform_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.purchase_arrival_notices_assert(purchaseTime='now', logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_arrival_list_by_platform_order_no(self):
        """[搜索]-采购单号查询"""
        case = self.common_operations()
        case.arrival_list_by_platform_order_no()
        obj = cached('orderNo')
        res = [lambda: self.pc.purchase_arrival_notices_assert(purchaseTime='now', orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_arrival_list_by_platform_date(self):
        """[搜索]-date查询"""
        case = self.common_operations()
        case.arrival_list_by_platform_date()
        res = [lambda: self.pc.purchase_un_shipped_order_list_assert(purchaseTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
