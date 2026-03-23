# coding: utf-8
from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(me_r.HelpOneClickHelpRequest, None)
class TestTraffickerHelp(MiniBaseCase):
    """首页|帮卖"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0execute_one_click_help(self):
        """[一键帮卖]-从库存添加-我要帮卖"""
        self.pre.operations(data=['FA1', 'GA1'])
        self.case.execute_one_click_help()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_guaranteed_sale_buyout(self):
        """[一键帮卖]-从库存添加-我要保卖买断"""
        self.pre.operations(data=['FA1', 'GA1'])
        self.case.guaranteed_sale_buyout()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_guaranteed_sales_and_profit_sharing(self):
        """[一键帮卖]-从库存添加-我要保卖分润"""
        self.pre.operations(data=['FA1', 'GA1'])
        self.case.guaranteed_sales_and_profit_sharing()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0express_delivery_is_easy_to_ship(self):
        """[发货]快递易发货"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        self.case.express_delivery_is_easy_to_ship()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_self_mailing(self):
        """[发货]自行邮寄发货"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        self.case.self_mailing()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_deliver_it_yourself(self):
        """[发货]自己送发货"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        self.case.deliver_it_yourself()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_inspection_retirement(self):
        """[待质检]-申请退机"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1'])
        self.case.quality_inspection_retirement()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_confirmation_request_to_withdraw(self):
        """[待确认]-申请退机"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA9', 'GA6', 'HA1', 'GB1'])
        self.case.pending_confirmation_request_to_withdraw()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_negotiate_a_refund_request(self):
        """[待议价]-申请退机"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA9', 'GA6', 'HA1', 'GB1', 'GA12'])
        self.case.negotiate_a_refund_request()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_for_sale_request_to_withdraw(self):
        """[待议价]-申请退机"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GB1'])
        self.case.for_sale_request_to_withdraw()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    def test_pending_negotiation_confirm_the_guaranteed_sale(self):
        """[待议价]-确认保卖"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_negotiation_confirm_the_guarantee_of_sale(self):
        """[待确认]-申请议价"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA9', 'GA6', 'HA1', 'GB1'])
        self.case.negotiation_confirm_the_guarantee_of_sale()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待议价', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pending_departure_cancel_the_departure(self):
        """[待退机]-取消退机"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA9', 'GA6', 'HA1', 'GB1'])
        self.case.pending_departure_cancel_the_departure()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待确认', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_manual_sign_in_during_exit(self):
        """[退机中]-手动签收"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8', 'GB2'])
        self.case.manual_sign_in_during_exit()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='已退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_logistics_signing_during_retirement(self):
        """[退机中]-物流签收入库"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8', 'GB3'])
        self.case.logistics_signing_during_retirement()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)


@test_mode_handler(me_r.InventoryCountRequest, None)
class TestTraffickerInventory(MiniBaseCase):
    """首页|库存"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0individual_item_counting(self):
        """[流程]新建盘点-提交盘点-完成盘点"""
        self.case.individual_item_counting()
        res = [lambda: self.pc.inventory_count_assert(updateTime='now', stockNo='PD')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0handover_for_quality_inspection(self):
        """[流程]移交物品-移交质检"""
        self.pre.operations(data=['FA1'])

        self.case.handover_for_quality_inspection()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_handover_for_maintenance(self):
        """[流程]移交物品-移交维修"""
        self.pre.operations(data=['FA1'])

        self.case.handover_for_maintenance()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_transfer_for_repair(self):
        """[流程]移交物品-移交送修"""
        self.pre.operations(data=['FA1'])

        self.case.transfer_for_repair()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_transfer_for_sales(self):
        """[流程]移交物品-移交销售"""
        self.pre.operations(data=['FA1'])

        self.case.transfer_for_sales()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_transfer_for_purchasing_after_sales(self):
        """[流程]移交物品-移交采购售后"""
        self.pre.operations(data=['FA1'])

        self.case.transfer_for_purchasing_after_sales()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_transfer_for_stock(self):
        """[流程]移交物品-移交库存"""
        self.pre.operations(data=['FA1'])

        self.case.transfer_for_stock()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0sign_in_warehouse(self):
        """[流程]签收入库"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sign_in_warehouse_in_quality(self):
        """[流程]签收入库-移交质检"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse_in_quality()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sign_in_warehouse_in_repair(self):
        """[流程]签收入库-移交维修"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse_in_repair()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sign_in_warehouse_in_send(self):
        """[流程]签收入库-移交送修"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse_in_send()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sign_in_warehouse_in_sell(self):
        """[流程]签收入库-移交销售"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse_in_sell()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sign_in_warehouse_in_purchase(self):
        """[流程]签收入库-移交采购"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse_in_purchase()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sign_in_warehouse_in_inventory(self):
        """[流程]签收入库-移交库存"""
        self.pre.operations(data=['FA2'])
        self.case.sign_in_warehouse_in_inventory()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0receive_items_in_sell(self):
        """[流程]销售-接收物品"""
        self.pre.operations(data=['FA1', 'HC8'])
        self.case.receive_items_in_sell()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0sign_into_the_library(self):
        """[流程]签收入库"""
        self.pre.operations(data=['FA2'])
        self.case.sign_into_the_library()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now')]
        self.assert_all(*res)


@test_mode_handler(me_r.PurchaseItemRequest, None)
class TestTraffickerPurchase(MiniBaseCase):
    """首页|采购"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_add_smartwatch_arrived_unpaid(self):
        """[流程]新增采购单-智能手表-已到货-未付款"""
        self.case.add_smartwatch_arrived_unpaid()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_add_mobile_handover_repair(self):
        """[流程]新增采购单-手机-已到货-未付款-入库移交维修"""
        self.case.add_mobile_handover_repair()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0purchase_orders(self):
        """[流程]采购入库"""
        self.pre.operations(data=['FA2'])
        self.case.purchase_orders()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_purchase_orders_in_quality(self):
        """[流程]采购入库-移交质检"""
        self.pre.operations(data=['FA2'])
        self.case.purchase_orders_in_quality()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now')]
        self.assert_all(*res)


@test_mode_handler(me_r.QualityItemRequest, None)
class TestTraffickerQuality(MiniBaseCase):
    """首页|质检"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0submit_the_quality_inspection_results(self):
        """[流程]提交质检结果"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        self.case.submit_the_quality_inspection_results()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_fast_quality_inspection(self):
        """[流程]快速质检-提交质检结果"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        self.case.fast_quality_inspection()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_new_quality_inspection_form(self):
        """[流程]新增质检单"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        self.case.new_quality_inspection_form()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_quality_complete_purchase_warehousing(self):
        """[流程]先质检后入库"""
        self.pre.operations(data=['KA1', 'HC3', 'LA1'])
        self.case.quality_complete_purchase_warehousing()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)


@test_mode_handler(me_r.RepairItemRequest, None)
class TestTraffickerRepair(MiniBaseCase):
    """首页|维修"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0repair_items_in_repair(self):
        """[流程]物品维修-移交维修"""
        self.pre.operations(data=['FA1', 'HC5'])
        self.case.repair_items_in_repair()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


@test_mode_handler(me_r.SellItemRequest, None)
class TestTraffickerSell(MiniBaseCase):
    """首页|销售"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0partial_receipt_of_sales_outbound(self):
        """[流程]销售出库-部分收款"""
        self.pre.operations(data=['FA1', 'HC1'])
        self.case.partial_receipt_of_sales_outbound()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sales_out_of_the_warehouse_in_full(self):
        """[流程]销售出库-全款收款"""
        self.pre.operations(data=['FA1', 'HC1'])
        self.case.sales_out_of_the_warehouse_in_full()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sales_outbound_add_accessories(self):
        """[流程]销售出库-全款收款-赠送配件"""
        self.pre.operations(data=['FA1', 'HC1'])
        self.case.sales_outbound_add_accessories()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sales_outbound_new_customer(self):
        """[流程]销售出库-未收款-新增销售客户"""
        self.pre.operations(data=['FA1', 'HC1'])
        self.case.sales_outbound_new_customer()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_sales_outbound_express_easy(self):
        """[流程]销售出库-未收款-快递易"""
        self.pre.operations(data=['FA1', 'HC1'])
        self.case.sales_outbound_express_easy()
        res = [lambda: self.pc.sell_sale_item_list_assert(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)
