# coding: utf-8
from common.base_assert import BaseAssert
from common.base_assertions_field import AssertionsRes


class BaseModuleAssert(BaseAssert):
    """通用断言模块基类"""

    def __init__(self):
        super().__init__()
        self._api_cache = {}

    def _get_cached_api(self, path):
        """获取缓存的API对象path"""
        cache_key = path

        if cache_key not in self._api_cache:
            parts = path.split('.')
            current = self.api

            for part in parts:
                current = getattr(current, part)
            self._api_cache[cache_key] = current
        return self._api_cache[cache_key]

    def _call_module_api(self, module_name, api_methods, headers=None, data='main', **kwargs):
        """
        通用API调用方法
        Args:
            module_name: 模块名称
            api_methods: API方法字典
            headers: 请求头
            method: 调用方法
            **kwargs: 其他参数
        """
        return self._assert_api_response(
            module_name,
            api_methods,
            AssertionsRes().assertive_field if hasattr(AssertionsRes(),
                                                       'assertive_field') else AssertionsRes.assertive_field,
            headers,
            data,
            **kwargs
        )


class PcAssert(BaseModuleAssert):
    """公共断言"""

    def attachment_inventory_list_assert(self, data='main', **kwargs):
        """配件管理|配件库存|库存列表"""
        api = self._get_cached_api('attachment_inventory_list')
        methods = {
            'main': api.attachment_inventory_list,  # 库存列表
            'a': api.inventory_detail,  # 物品详情
            'b': api.inventory_purchase_info,  # 物品详情 采购信息
            'c': api.inventory_sell_info,  # 物品详情 销售信息
            'd': api.inventory_log_info,  # 物品详情 操作日志
        }
        return self._call_module_api('attachment_inventory_list', methods, data=data, **kwargs)

    def attachment_sales_list_assert(self, data='main', **kwargs):
        """配件管理|配件销售|销售列表"""
        api = self._get_cached_api('attachment_sales_list')
        methods = {
            'main': api.sales_list,  # 销售列表
            'a': api.sales_details  # 销售详情
        }
        return self._call_module_api('attachment_sales_list', methods, data=data, **kwargs)

    def attachment_purchase_list_assert(self, data='main', **kwargs):
        """配件管理|配件采购|采购列表"""
        api = self._get_cached_api('attachment_purchase_list')
        methods = {
            'main': api.purchase_list,  # 采购列表
            'a': api.purchase_list_detail  # 采购详情
        }
        return self._call_module_api('attachment_purchase_list', methods, data=data, **kwargs)

    def attachment_purchase_sales_list_assert(self, data='main', **kwargs):
        """配件管理|配件采购|采购售后列表"""
        api = self._get_cached_api('attachment_purchase_sales_list')
        methods = {
            'main': api.purchase_sales_list,  # 采购售后列表
            'a': api.purchase_sales_list_detail  # 采购售后详情
        }
        return self._call_module_api('attachment_purchase_sales_list', methods, data=data, **kwargs)

    def attachment_after_sales_list_assert(self, data='main', **kwargs):
        """配件管理|配件销售|销售售后列表"""
        api = self._get_cached_api('attachment_after_sales_list')
        methods = {
            'main': api.after_sales_list,  # 销售售后列表
            'a': api.after_sales_list_detail  # 销售售后详情
        }
        return self._call_module_api('attachment_after_sales_list', methods, data=data, **kwargs)

    def attachment_sorting_list_assert(self, data='main', **kwargs):
        """配件管理|入库管理|分拣列表"""
        api = self._get_cached_api('attachment_sorting_list')
        methods = {
            'main': api.sorting_list,  # 分拣列表
            'a': api.package_video  # 包裹视频
        }
        return self._call_module_api('attachment_sorting_list', methods, data=data, **kwargs)

    def attachment_new_arrival_assert(self, data='main', **kwargs):
        """配件管理|入库管理|新到货入库"""
        api = self._get_cached_api('attachment_new_arrival')
        methods = {
            'main': api.new_arrival_list,  # 新到货入库列表
        }
        return self._call_module_api('attachment_new_arrival', methods, data=data, **kwargs)

    def attachment_warehouse_allocation_assert(self, data='main', **kwargs):
        """配件管理|配件库存|库存调拨"""
        api = self._get_cached_api('attachment_warehouse_allocation')
        methods = {
            'main': api.warehouse_allocation,  # 调拨列表
            'a': api.inventory_transfer_details_list  # 调拨详情
        }
        return self._call_module_api('attachment_warehouse_allocation', methods, data=data, **kwargs)

    def attachment_handover_records_assert(self, data='main', **kwargs):
        """配件管理|移交接收管理|移交记录"""
        api = self._get_cached_api('attachment_handover_records')
        methods = {
            'main': api.handover_records_list,  # 移交记录列表
            'a': api.handover_records_details,  # 移交记录详情
        }
        return self._call_module_api('attachment_handover_records', methods, data=data, **kwargs)

    def attachment_hand_over_the_list_of_items_assert(self, data='main', **kwargs):
        """配件管理|移交接收管理|移交物品"""
        api = self._get_cached_api('attachment_hand_over_the_list_of_items')
        methods = {
            'main': api.hand_over_the_list_of_items,  # 移交物品列表
        }
        return self._call_module_api('attachment_hand_over_the_list_of_items', methods, data=data, **kwargs)

    def attachment_receive_items_assert(self, data='main', **kwargs):
        """配件管理|移交接收管理|接收物品"""
        api = self._get_cached_api('attachment_receive_items')
        methods = {
            'main': api.handover_order_received_list,  # 移交单接收列表
            'a': api.item_received_list,  # 物品接收列表
        }
        return self._call_module_api('attachment_receive_items', methods, data=data, **kwargs)

    def attachment_gift_details_assert(self, data='main', **kwargs):
        """配件管理|配件统计|赠送明细"""
        api = self._get_cached_api('attachment_gift_details')
        methods = {
            'main': api.gift_details_list,  # 赠送明细列表
        }
        return self._call_module_api('attachment_gift_details', methods, data=data, **kwargs)

    def attachment_old_warehouse_assert(self, data='main', **kwargs):
        """配件管理|入库管理|旧配件入库"""
        api = self._get_cached_api('attachment_old_warehouse')
        methods = {
            'main': api.accessories_inventory_list,  # 旧配件入库列表
            'a': api.accessories_inventory_detail  # 旧配件入库详情
        }
        return self._call_module_api('attachment_old_warehouse', methods, data=data, **kwargs)

    def attachment_sales_details_assert(self, data='main', **kwargs):
        """配件管理|配件统计|销售明细"""
        api = self._get_cached_api('attachment_sales_details')
        methods = {
            'main': api.statics_detail,  # 销售明细列表
        }
        return self._call_module_api('attachment_sales_details', methods, data=data, **kwargs)

    def attachment_maintenance_assert(self, data='main', **kwargs):
        """配件管理|配件维护"""
        api = self._get_cached_api('attachment_maintenance')
        methods = {
            'main': api.maintenance_list,  # 配件维护列表
        }
        return self._call_module_api('attachment_maintenance', methods, data=data, **kwargs)

    def finance_account_list_assert(self, data='main', **kwargs):
        """财务管理|资金账户|账户列表"""
        api = self._get_cached_api('finance_account_list')
        methods = {
            'main': api.account_list,  # 账户列表
            'a': api.account_statistics  # 账户统计
        }
        return self._call_module_api('finance_account_list', methods, data=data, **kwargs)

    def finance_transaction_details_assert(self, data='main', **kwargs):
        """财务管理|资金账户|交易明细"""
        api = self._get_cached_api('finance_transaction_details')
        methods = {
            'main': api.transaction_details,  # 交易明细列表
        }
        return self._call_module_api('finance_transaction_details', methods, data=data, **kwargs)

    def finance_payment_settlement_assert(self, data='main', **kwargs):
        """财务管理|业务记账|付款结算单"""
        api = self._get_cached_api('finance_payment_settlement')
        methods = {
            'main': api.payment_settlement,  # 付款结算单列表
        }
        return self._call_module_api('finance_payment_settlement', methods, data=data, **kwargs)

    def finance_collection_and_settlement_assert(self, data='main', **kwargs):
        """财务管理|业务记账|收款结算单"""
        api = self._get_cached_api('finance_collection_and_settlement')
        methods = {
            'main': api.collection_and_settlement,  # 收款结算单列表
        }
        return self._call_module_api('finance_collection_and_settlement', methods, data=data, **kwargs)

    def finance_bill_review_assert(self, data='main', **kwargs):
        """财务管理|业务记账|账单审核
        i：1应付 2应收
        """
        api = self._get_cached_api('finance_bill_review')
        methods = {
            'main': api.payable_bill,  # 应付账单列表
        }
        return self._call_module_api('finance_bill_review', methods, data=data, **kwargs)

    def finance_cost_income_adjustment_assert(self, data='main', **kwargs):
        """财务管理|成本收入调整"""
        api = self._get_cached_api('finance_cost_income_adjustment')
        methods = {
            'main': api.cost_income_adjustment,  # 单据列表
            'a': api.document_list_details,  # 单据列表详情
            'b': api.list_of_items  # 物品列表
        }
        return self._call_module_api('finance_cost_income_adjustment', methods, data=data, **kwargs)

    def finance_daily_expenditure_assert(self, data='main', **kwargs):
        """财务管理|业务记账|日常支出"""
        api = self._get_cached_api('finance_daily_expenditure')
        methods = {
            'main': api.daily_expenditure,  # 日常支出列表
            'a': api.expense_statistics_amount  # 统计金额
        }
        return self._call_module_api('finance_daily_expenditure', methods, data=data, **kwargs)

    def finance_daily_income_assert(self, data='main', **kwargs):
        """财务管理|业务记账|日常收入"""
        api = self._get_cached_api('finance_daily_income')
        methods = {
            'main': api.daily_income,  # 日常收入列表
            'a': api.expense_statistics_amount  # 统计金额
        }
        return self._call_module_api('finance_daily_income', methods, data=data, **kwargs)

    def finance_exchanges_and_receivables_assert(self, data='main', **kwargs):
        """财务管理|业务记账|往来应收"""
        api = self._get_cached_api('finance_exchanges_and_receivables')
        methods = {
            'main': api.reconciliation_details_list,  # 对账详情
            'a': api.reconciliation_details_list_info  # 对账详情-单据详情
        }
        return self._call_module_api('finance_exchanges_and_receivables', methods, data=data, **kwargs)

    def finance_coping_with_each_other_assert(self, data='main', **kwargs):
        """财务管理|业务记账|往来应付"""
        api = self._get_cached_api('finance_coping_with_each_other')
        methods = {
            'main': api.reconciliation_details_list,  # 对账详情
            'a': api.reconciliation_details_list_info  # 对账详情-单据详情
        }
        return self._call_module_api('finance_coping_with_each_other', methods, data=data, **kwargs)

    def finance_prepay_receive_list_assert(self, data='main', **kwargs):
        """财务管理|业务记账|预付预收"""
        api = self._get_cached_api('finance_prepay_receive_list')
        methods = {
            'main': api.prepay_list,  # 预付、预收列表
        }
        return self._call_module_api('finance_prepay_receive_list', methods, data=data, **kwargs)

    def fulfillment_order_manage_assert(self, data='main', **kwargs):
        """运营中心|订单管理
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        api = self._get_cached_api('fulfillment_order_manage')
        methods = {
            'main': api.order_list,  # 订单列表
        }
        return self._call_module_api('fulfillment_order_manage', methods, data=data, **kwargs)

    def fulfillment_items_to_be_quoted_assert(self, data='main', **kwargs):
        """运营中心|待报价物品"""
        api = self._get_cached_api('fulfillment_items_to_be_quoted')
        methods = {
            'main': api.items_to_be_quoted_list,  # 列表
        }
        return self._call_module_api('fulfillment_items_to_be_quoted', methods, data=data, **kwargs)

    def fulfillment_returns_manage_assert(self, data='main', **kwargs):
        """运营中心|退货管理
        i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        api = self._get_cached_api('fulfillment_returns_manage')
        methods = {
            'main': api.merchant_details_list,  # 商户明细列表
            'a': api.item_detail_list,  # 物品明细列表
            'b': api.batch_detail_list  # 批次明细列表
        }
        return self._call_module_api('fulfillment_returns_manage', methods, data=data, **kwargs)

    def fulfillment_quality_manage_assert(self, data='main', **kwargs):
        """运营中心|质检管理
        [d]i类型 1未上传 2已上传
        """
        api = self._get_cached_api('fulfillment_quality_manage')
        methods = {
            'main': api.quality_manage_list,  # 待领取物品列表
            'a': api.items_in_quality_inspection_list,  # 质检中物品列表
            'b': api.re_examine_the_application_list,  # 重验申请列表
            'c': api.inspected_items_list,  # 已质检物品列表
            'd': api.product_image_shooting_list  # 商品图拍摄列表
        }
        return self._call_module_api('fulfillment_quality_manage', methods, data=data, **kwargs)

    def fulfillment_sales_and_shipment_manage_assert(self, data='main', **kwargs):
        """运营中心|销售发货管理"""
        api = self._get_cached_api('fulfillment_sales_and_shipment_manage')
        methods = {
            'main': api.sales_and_shipment_manage_item_list,  # 待发货 按物品
            'a': api.sales_and_shipment_manage_list,  # 待发货 按商户
            'b': api.snap_the_order_to_be_received_list,  # 待收货 按物品
            'c': api.sales_and_fulfillment_management_list,  # 待收货 按包裹
            'd': api.snap_machine_has_been_received_list,  # 已收货 按包裹
            'e': api.snap_machine_has_been_received_item_list,  # 已收货 按物品
        }
        return self._call_module_api('fulfillment_sales_and_shipment_manage', methods, data=data, **kwargs)

    def help_generate_order_assert(self, data='main', **kwargs):
        """帮卖管理|帮卖上架列表"""
        api = self._get_cached_api('help_generate_order')
        methods = {
            'main': api.help_list_of_orders,  # 订单列表
            'a': api.help_list_of_batches,  # 批次列表
            'b': api.initiate_a_list_of_helpers  # 发起帮卖列表
        }
        return self._call_module_api('help_generate_order', methods, data=data, **kwargs)

    def help_sell_list_of_goods_assert(self, data='main', **kwargs):
        """帮卖管理|帮卖来货列表"""
        api = self._get_cached_api('help_sell_the_list_of_goods')
        methods = {
            'main': api.help_incoming_goods_list,  # 订单列表
            'a': api.help_batch_no_list  # 批次列表
        }
        return self._call_module_api('help_sell_the_list_of_goods', methods, data=data, **kwargs)

    def help_service_configuration_assert(self, data='main', **kwargs):
        """帮卖管理|帮卖业务配置"""
        api = self._get_cached_api('help_service_configuration')
        methods = {
            'main': api.service_configuration,  # 帮卖业务配置列表
        }
        return self._call_module_api('help_service_configuration', methods, data=data, **kwargs)

    def inventory_address_manage_assert(self, data='main', **kwargs):
        """库存管理|出库管理|地址管理"""
        api = self._get_cached_api('inventory_address_manage')
        methods = {
            'main': api.address_manage,  # 列表
        }
        return self._call_module_api('inventory_address_manage', methods, data=data, **kwargs)

    def inventory_logistics_list_assert(self, data='main', **kwargs):
        """库存管理|入库管理|物流列表"""
        api = self._get_cached_api('inventory_logistics_list')
        methods = {
            'main': api.material_flow_list,  # 物流列表
            'a': api.material_flow_list_detail,  # 物流列表详情
        }
        return self._call_module_api('inventory_logistics_list', methods, data=data, **kwargs)

    def inventory_outbound_orders_list_assert(self, data='main', **kwargs):
        """库存管理|出库管理|仅出库订单列表"""
        api = self._get_cached_api('inventory_outbound_orders_list')
        methods = {
            'main': api.only_outbound_list,  # 仅出库列表
            'a': api.list_of_returned_orders,  # 退回单列表
            'b': api.only_outbound_order_details  # 仅出库订单详情
        }
        return self._call_module_api('inventory_outbound_orders_list', methods, data=data, **kwargs)

    def inventory_receive_items_assert(self, data='main', **kwargs):
        """库存管理|移交接收管理|接收物品"""
        api = self._get_cached_api('inventory_receive_items')
        methods = {
            'main': api.stay_work_list,  # 物品接收列表
            'a': api.receive_items,  # 移交单接收列表
            'b': api.receive_items_detail  # 移交单接收详情
        }
        return self._call_module_api('inventory_receive_items', methods, data=data, **kwargs)

    def inventory_count_assert(self, data='main', **kwargs):
        """库存管理|库存盘点"""
        api = self._get_cached_api('inventory_count')
        methods = {
            'main': api.inventory_count,  # 库存盘点列表
        }
        return self._call_module_api('inventory_count', methods, data=data, **kwargs)

    def inventory_warehouse_allocation_assert(self, data='main', **kwargs):
        """库存管理|库存调拨"""
        api = self._get_cached_api('inventory_warehouse_allocation')
        methods = {
            'main': api.warehouse_transfers,  # 库存调拨列表
        }
        return self._call_module_api('inventory_warehouse_allocation', methods, data=data, **kwargs)

    def inventory_list_assert(self, data='main', **kwargs):
        """库存管理|库存列表"""
        api = self._get_cached_api('inventory_list')
        methods = {
            'main': api.inventory_list,  # 库存列表
            'a': api.item_details_sell_info,  # 物品详情 销售信息
            'b': api.operation_log,  # 物品详情 操作日志
            'c': api.details_of_the_total_cost_of_inventory_count,  # 库存列表 总成本详情 统计
            'd': api.details_of_the_total_cost_of_inventory,  # 库存列表 总成本详情
            'e': api.details_of_total_inventory_revenue_count,  # 库存列表 总收入详情 统计
            'f': api.details_of_total_inventory_revenue  # 库存列表 总收入详情
        }
        if data in ['a', 'b']:
            return self._call_module_api('inventory_list', methods, data=data, **kwargs)
        else:
            return self._call_module_api('inventory_list', methods, data=data, **kwargs)

    def inventory_handover_record_assert(self, data='main', **kwargs):
        """库存管理|移交接收管理|移交记录"""
        api = self._get_cached_api('inventory_transfer_records')
        methods = {
            'main': api.receive_log,  # 移交记录列表
            'a': api.receive_log_detail,  # 移交记录列表 物品详情
        }
        return self._call_module_api('inventory_transfer_records', methods, data=data, **kwargs)

    def user_info_assert(self, data='main', **kwargs):
        """个人中心"""
        api = self._get_cached_api('user_info')
        methods = {
            'main': api.user_center,  # 个人中心信息
        }
        return self._call_module_api('user_info', methods, data=data, **kwargs)

    def message_release_list_assert(self, data='main', **kwargs):
        """消息管理|消息发布列表"""
        api = self._get_cached_api('message_release_list')
        methods = {
            'main': api.release_list,  # 消息发布列表
        }
        return self._call_module_api('message_release_list', methods, data=data, **kwargs)

    def platform_order_review_assert(self, data='main', **kwargs):
        """平台管理|订单管理|订单审核"""
        api = self._get_cached_api('platform_order_review')
        methods = {
            'main': api.order_review,  # 订单审核列表
        }
        return self._call_module_api('platform_order_review', methods, data=data, **kwargs)

    def platform_list_of_dark_auction_houses_assert(self, data='main', **kwargs):
        """平台管理|卖场管理|暗拍卖场列表
        i；1-已上架；2-待上架；3-已下架
        """
        api = self._get_cached_api('platform_list_of_dark_auction_houses')
        methods = {
            'main': api.list_of_dark_auction_houses,  # 暗拍卖场列表
            'a': api.view_session_details,  # 查看场次详情 场次列表
            'b': api.product_list,  # 查看场次详情 商品列表
        }
        return self._call_module_api('platform_list_of_dark_auction_houses', methods, data=data, **kwargs)

    def platform_list_of_direct_auction_houses_assert(self, data='main', **kwargs):
        """平台管理|卖场管理|直拍卖场列表"""
        api = self._get_cached_api('platform_list_of_direct_auction_houses')
        methods = {
            'main': api.list_of_stores,  # 直拍卖场列表
            'a': api.view_session_details,  # 查看场次详情 场次列表
            'b': api.product_list,  # 查看场次详情 商品列表
        }
        return self._call_module_api('platform_list_of_direct_auction_houses', methods, data=data, **kwargs)

    def platform_virtual_inventory_list_assert(self, data='main', **kwargs):
        """平台管理|虚拟库存|虚拟库存列表
        i：物品状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 7质检完成 8退货中 9退货已出库 10已退货
        """
        api = self._get_cached_api('platform_virtual_inventory_list')
        methods = {
            'main': api.virtual_inventory_list,  # 虚拟库存列表
        }
        return self._call_module_api('platform_virtual_inventory_list', methods, data=data, **kwargs)

    def platform_auction_product_manage_assert(self, data='main', **kwargs):
        """平台管理|虚拟库存|上拍商品管理
         i：类型 1可上拍商品 2已上拍商品 0待定价物品
        """
        api = self._get_cached_api('platform_auction_product_manage')
        methods = {
            'main': api.list_of_auctioned_products,  # 上拍商品管理列表
        }
        return self._call_module_api('platform_auction_product_manage', methods, data=data, **kwargs)

    def platform_items_to_be_specified_assert(self, data='main', **kwargs):
        """平台管理|运营中心|待指定物品"""
        api = self._get_cached_api('platform_items_to_be_specified')
        methods = {
            'main': api.item_to_be_specified_list,  # 待指定物品列表
        }
        return self._call_module_api('platform_items_to_be_specified', methods, data=data, **kwargs)

    def purchase_order_list_assert(self, data='main', i=None, **kwargs):
        """商品采购|采购管理|采购订单列表"""
        api = self._get_cached_api('purchase_order_list')
        methods = {
            'main': api.order_list,  # 采购订单列表
        }
        return self._call_module_api('purchase_order_list', methods, data=data, i=i, **kwargs)

    def purchase_supplier_manage_assert(self, data='main', **kwargs):
        """商品采购|供应商管理"""
        api = self._get_cached_api('purchase_supplier_manage')
        methods = {
            'main': api.supplier_manage,  # 供应商管理列表
        }
        return self._call_module_api('purchase_supplier_manage', methods, data=data, **kwargs)

    def purchase_after_sales_list_assert(self, data='main', **kwargs):
        """商品采购|采购售后管理|采购售后列表"""
        api = self._get_cached_api('purchase_after_sales_list')
        methods = {
            'main': api.after_sales_list,  # 采购售后列表
            'a': api.after_sales_detail  # 采购售后列表详情
        }
        return self._call_module_api('purchase_after_sales_list', methods, data=data, **kwargs)

    def purchase_work_order_assert(self, data='main', **kwargs):
        """商品采购|采购管理|采购工单"""
        api = self._get_cached_api('purchase_work_order')
        methods = {
            'main': api.work_orders_list,  # 采购工单列表
        }
        return self._call_module_api('purchase_work_order', methods, data=data, **kwargs)

    def purchase_un_shipped_order_list_assert(self, data='main', **kwargs):
        """商品采购|采购管理|未发货订单列表"""
        api = self._get_cached_api('purchase_un_shipped_order_list')
        methods = {
            'main': api.un_shipped_order_list,  # 未发货订单列表
        }
        return self._call_module_api('purchase_un_shipped_order_list', methods, data=data, **kwargs)

    def purchase_arrival_notices_assert(self, data='main', **kwargs):
        """商品采购|采购管理|到货通知单列表"""
        api = self._get_cached_api('purchase_arrival_notices')
        methods = {
            'main': api.arrival_notices_list,  # 到货通知单列表
        }
        return self._call_module_api('purchase_arrival_notices', methods, data=data, **kwargs)

    def purchase_items_to_be_received_assert(self, data='main', **kwargs):
        """商品采购|采购售后管理|待接收物品"""
        api = self._get_cached_api('purchase_items_to_be_received')
        methods = {
            'main': api.receive_items_list,  # 待接收物品
        }
        return self._call_module_api('purchase_items_to_be_received', methods, data=data, **kwargs)

    def purse_wallet_order_list_assert(self, data='main', **kwargs):
        """钱包管理|钱包订单列表"""
        api = self._get_cached_api('purse_wallet_order_list')
        methods = {
            'main': api.pending_payment,  # 钱包订单列表 待付款
            'a': api.confirm_to_the_payment  # 钱包订单列表 确认到款中
        }
        return self._call_module_api('purse_wallet_order_list', methods, data=data, **kwargs)

    def quality_record_list_assert(self, data='main', **kwargs):
        """质检管理|质检记录列表"""
        api = self._get_cached_api('quality_record_list')
        methods = {
            'main': api.quality_record_list,  # 质检记录列表
        }
        return self._call_module_api('quality_record_list', methods, data=data, **kwargs)

    def quality_content_template_assert(self, data='main', **kwargs):
        """质检管理|质检内容模版"""
        api = self._get_cached_api('quality_content_template')
        methods = {
            'main': api.content_template,  # 质检内容模版
        }
        return self._call_module_api('quality_content_template', methods, data=data, **kwargs)

    def quality_store_assert(self, data='main', **kwargs):
        """质检管理|先质检后入库"""
        api = self._get_cached_api('quality_store')
        methods = {
            'main': api.quality_store_list,  # 非库内物品列表
            'a': api.quality_inspection_list  # 非库内质检列表
        }
        return self._call_module_api('quality_store', methods, data=data, **kwargs)

    def attachment_goods_received_assert(self, data='main', **kwargs):
        """配件管理|入库管理|待接收物品"""
        api = self._get_cached_api('attachment_goods_received')
        methods = {
            'main': api.list_of_items_to_be_received,  # 待接收物品列表
        }
        return self._call_module_api('attachment_goods_received', methods, data=data, **kwargs)

    def repair_review_list_assert(self, data='main', **kwargs):
        """维修管理|维修审核列表"""
        api = self._get_cached_api('repair_review_list')
        methods = {
            'main': api.repair_audit_list,  # 维修审核列表
        }
        return self._call_module_api('repair_review_list', methods, data=data, **kwargs)

    def repair_items_assert(self, data='main', **kwargs):
        """维修管理|维修物品列表"""
        api = self._get_cached_api('repair_items')
        methods = {
            'main': api.repair_items,  # 维修物品列表
        }
        return self._call_module_api('repair_items', methods, data=data, **kwargs)

    def repair_project_list_assert(self, data='main', **kwargs):
        """维修管理|维修项目列表"""
        api = self._get_cached_api('repair_project_list')
        methods = {
            'main': api.project_list,  # 维修项目列表
            'a': api.model_list  # 维修项目列表-机型列表
        }
        return self._call_module_api('repair_project_list', methods, data=data, **kwargs)

    def repair_parts_manage_assert(self, data='main', **kwargs):
        """已维修管理|拆件管理"""
        api = self._get_cached_api('repair_parts_manage')
        methods = {
            'main': api.parts_manage_list,  # 维修物品列表
        }
        return self._call_module_api('repair_parts_manage', methods, data=data, **kwargs)

    def sell_after_sales_list_assert(self, data='main', **kwargs):
        """商品销售|销售售后管理|销售售后列表"""
        api = self._get_cached_api('sell_after_sales_list')
        methods = {
            'main': api.sales_and_after_sales_are_completed,  # 销售售后列表 销售售后完成
            'a': api.in_the_after_sales_service  # 销售售后列表 销售售后中
        }
        return self._call_module_api('sell_after_sales_list', methods, data=data, **kwargs)

    def sell_list_of_items_for_sale_assert(self, data='main', **kwargs):
        """商品销售|销售管理|销售中物品列表"""
        api = self._get_cached_api('sell_list_of_items_for_sale')
        methods = {
            'main': api.goods_list_for_sale,  # 销售中物品列表
        }
        return self._call_module_api('sell_list_of_items_for_sale', methods, data=data, **kwargs)

    def sell_sale_item_list_assert(self, data='main', **kwargs):
        """商品销售|销售管理|已销售物品列表"""
        api = self._get_cached_api('sell_sale_item_list')
        methods = {
            'main': api.sell_sale_item_list,  # 已销售物品列表
        }
        return self._call_module_api('sell_sale_item_list', methods, data=data, **kwargs)

    def sell_sold_order_assert(self, data='main', **kwargs):
        """商品销售|销售管理|已销售订单列表"""
        api = self._get_cached_api('sell_sold_order')
        methods = {
            'main': api.sold_order_list,  # 已销售订单列表
        }
        return self._call_module_api('sell_sold_order', methods, data=data, **kwargs)

    def sell_order_list_for_sale_assert(self, data='main', **kwargs):
        """商品销售|销售管理|销售中订单列表 """
        api = self._get_cached_api('sell_order_list_for_sale')
        methods = {
            'main': api.order_list_for_sale,  # 销售中订单列表
        }
        return self._call_module_api('sell_order_list_for_sale', methods, data=data, **kwargs)

    def sell_goods_received_assert(self, data='main', **kwargs):
        """商品销售|销售管理|待接收物品"""
        api = self._get_cached_api('sell_goods_received')
        methods = {
            'main': api.goods_received_list,  # 待接收物品
        }
        return self._call_module_api('sell_goods_received', methods, data=data, **kwargs)

    def sell_items_for_sale_assert(self, data='main', **kwargs):
        """商品销售|销售管理|待销售物品"""
        api = self._get_cached_api('sell_items_for_sale')
        methods = {
            'main': api.items_for_sale,  # 待销售物品
        }
        return self._call_module_api('sell_items_for_sale', methods, data=data, **kwargs)

    def sell_statics_assert(self, data='main', **kwargs):
        """商品销售|销售数据统计"""
        api = self._get_cached_api('sell_statics')
        methods = {
            'main': api.statics,  # 待销售物品
        }
        res = self._call_module_api('sell_statics', methods, data=data, **kwargs)
        return res

    def send_been_sent_repair_assert(self, data='main', **kwargs):
        """送修管理|已送修物品"""
        api = self._get_cached_api('send_been_sent_repair')
        methods = {
            'main': api.send_been_sent_repair,  # 已送修物品列表
        }
        return self._call_module_api('send_been_sent_repair', methods, data=data, **kwargs)

    def send_list_of_repair_orders_assert(self, data='main', **kwargs):
        """送修管理|送修单列表"""
        api = self._get_cached_api('send_list_of_repair_orders')
        methods = {
            'main': api.send_list,  # 送修单列表
        }
        return self._call_module_api('send_list_of_repair_orders', methods, data=data, **kwargs)

    def system_export_list_assert(self, data='main', **kwargs):
        """系统管理|导出列表 """
        api = self._get_cached_api('system_export_list')
        methods = {
            'main': api.export_list,  # 导出列表
        }
        return self._call_module_api('system_export_list', methods, data=data, **kwargs)

    def guarantee_order_manage_assert(self, data='main', **kwargs):
        """保卖管理|订单列表"""
        api = self._get_cached_api('guarantee_order_manage')
        methods = {
            'main': api.order_list,  # 订单列表
        }
        return self._call_module_api('guarantee_order_manage', methods, data=data, **kwargs)

    def guarantee_goods_manage_assert(self, data='main', **kwargs):
        """保卖管理|商品管理"""
        api = self._get_cached_api('guarantee_goods_manage')
        methods = {
            'main': api.order_list,  # 商品列表
        }
        return self._call_module_api('guarantee_goods_manage', methods, data=data, **kwargs)

    def guarantee_returns_manage_assert(self, data='main', **kwargs):
        """保卖管理|退货列表"""
        api = self._get_cached_api('guarantee_returns_manage')
        methods = {
            'main': api.item_detail_list,  # 退货列表
        }
        return self._call_module_api('guarantee_returns_manage', methods, data=data, **kwargs)

    def camera_after_sales_order_assert(self, data='main', **kwargs):
        """拍机管理|售后管理|售后订单"""
        api = self._get_cached_api('camera_after_sales_order')
        methods = {
            'main': api.after_sales_list,  # 售后订单列表
        }
        return self._call_module_api('camera_after_sales_order', methods, data=data, **kwargs)

    def camera_list_of_airport_visits_assert(self, data='main', **kwargs):
        """拍机管理|拍机场次列表"""
        api = self._get_cached_api('camera_after_sales_order')
        methods = {
            'main': api.list_of_airport_visits,  # 拍机场次列表
            'a': api.view_the_products_of_the_session,  # 拍机场次列表 查看场次商品
        }
        return self._call_module_api('camera_list_of_airport_visits', methods, data=data, **kwargs)

    def fulfillment_camera_after_sales_order_assert(self, data='main', **kwargs):
        """运营中心|拍机管理|售后管理|售后订单
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        api = self._get_cached_api('fulfillment_camera_after_sales_order')
        methods = {
            'main': api.camera_after_sales_order_list,  # 售后订单列表
        }
        return self._call_module_api('fulfillment_camera_after_sales_order', methods, data=data, **kwargs)

    def platform_grievance_manage_assert(self, data='main', **kwargs):
        """平台管理|壹准拍机|售后管理|申诉管理
        i订单类型 0待处理 1申诉成功 2申诉失败 3申诉取消
        """
        api = self._get_cached_api('platform_grievance_manage')
        methods = {
            'main': api.statement_list,  # 申诉管理列表
        }
        return self._call_module_api('platform_grievance_manage', methods, data=data, **kwargs)

    def platform_yz_auction_assert(self, data='main', **kwargs):
        """平台管理|壹准拍机|售后管理|售后订单
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        api = self._get_cached_api('platform_yz_auction')
        methods = {
            'main': api.after_sales_order_list,  # 售后订单列表
        }
        return self._call_module_api('platform_yz_auction', methods, data=data, **kwargs)

    def fulfillment_after_sales_return_manage_assert(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后退货管理
        i 类型  1待退货 2退货已出库
        """
        api = self._get_cached_api('fulfillment_after_sales_return_manage')
        methods = {
            'main': api.after_sales_return_list,  # 售后退货列表
        }
        return self._call_module_api('fulfillment_after_sales_return_manage', methods, data=data, **kwargs)

    def auction_my_assert(self, data='main', **kwargs):
        """保卖小程序-我的
        i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
        j：类型 1销售服务 2质检服务
        [b] i: 订单状态
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        j：类型 1销售服务 2质检服务
        """
        api = self._get_cached_api('auction_my')
        methods = {
            'main': api.sell_order_list,  # 销售物品 订单列表
            'a': api.sell_return_details,  # 销售物品 退货详情
            'b': api.order_list,  # 订单信息 订单列表
            'c': api.order_details  # 订单信息 订单详情
        }
        return self._call_module_api('auction_my', methods, data=data, **kwargs)

    def bidding_camera_assert(self, data='main', **kwargs):
        """拍机小程序-竞价列表"""
        api = self._get_cached_api('bidding_camera')
        methods = {
            'main': api.zhi_auction_list,  # 竞价列表 直拍
            'a': api.an_auction_list,  # 竞价列表 暗拍
        }
        return self._call_module_api('bidding_camera', methods, data=data, **kwargs)

    def bidding_my_assert(self, data='main', **kwargs):
        """拍机小程序-我的
        i：订单状态 1待支付 2待发货 3待收货 4已收货 5已售后 6已取消
        [a] i：订单状态 1待支付 2已支付 3已取消
        [b] i：订单状态 1待收货 2已收货
        [c] i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        api = self._get_cached_api('bidding_my')
        methods = {
            'main': api.racket_product_list,  # 拍机商品列表
            'a': api.auction_my_purchase_list,  # 我的购买列表
            'b': api.camera_my_package_list,  # 我的包裹列表
            'c': api.pat_machine_return_after_sales_list,  # 退货售后列表
        }
        return self._call_module_api('bidding_my', methods, data=data, **kwargs)

class MgAssert(BaseModuleAssert):
    """保卖小程序"""

    def mg_my_assert(self, headers=None, data='main', **kwargs):
        """我的
        i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
        j：类型 1销售服务 2质检服务
        [b] i: 订单状态
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        j：类型 1销售服务 2质检服务
        """
        api = self._get_cached_api('mg_my')
        methods = {
            'main': api.sell_order_list,  # 销售物品 订单列表
            'a': api.sell_return_details,  # 销售物品 退货详情
            'b': api.order_list,  # 订单信息 订单列表
            'c': api.order_details  # 订单信息 订单详情
        }
        return self._call_module_api('mg_my', methods, headers, data, **kwargs)


class McAssert(BaseModuleAssert):
    """拍机小程序"""

    def mc_camera_assert(self, headers=None, data='main', **kwargs):
        """竞价列表"""
        api = self._get_cached_api('mc_camera')
        methods = {
            'main': api.zhi_auction_list,  # 竞价列表 直拍
            'a': api.an_auction_list,  # 竞价列表 暗拍
        }
        return self._call_module_api('mc_camera', methods, headers, data, **kwargs)

    def mc_my_assert(self, headers=None, data='main', **kwargs):
        """我的
        i：订单状态 1待支付 2待发货 3待收货 4已收货 5已售后 6已取消
        [a] i：订单状态 1待支付 2已支付 3已取消
        [b] i：订单状态 1待收货 2已收货
        [c] i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        api = self._get_cached_api('mc_my')
        methods = {
            'main': api.racket_product_list,  # 拍机商品列表
            'a': api.auction_my_purchase_list,  # 我的购买列表
            'b': api.camera_my_package_list,  # 我的包裹列表
            'c': api.pat_machine_return_after_sales_list,  # 退货售后列表
        }
        return self._call_module_api('mc_my', methods, headers, data, **kwargs)

